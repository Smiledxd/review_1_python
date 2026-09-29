"""Fuente de verdad de `sesiones/refuerzo_python_puro.ipynb`.

Uso (desde la raíz del repo):
    python3 tools/generar_notebook.py

Arma el notebook (nbformat 4, kernel python3, sin outputs) con el formato de las sesiones:
setup activable con verificadores, 📘 Concepto → ejemplo → ✍️ Tu turno → ✅ Verificar → 💡 Pistas,
y soluciones plegadas en un anexo final. Luego lo valida con `nbformat.validate`.
"""

from pathlib import Path
import sys

import nbformat

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from libro import Libro  # noqa: E402
import parte1, parte2, parte3, reto  # noqa: E402

RAIZ = AQUI.parent
DESTINO = RAIZ / "sesiones" / "refuerzo_python_puro.ipynb"
URL_COLAB = ("https://colab.research.google.com/github/Smiledxd/review_1_python/blob/main/"
             "sesiones/refuerzo_python_puro.ipynb")


def portada(nb):
    nb.md(f"""
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({URL_COLAB})

# Refuerzo · Diccionarios, estado acumulativo y `key`

**Python puro** · ⏱️ Duración estimada: 3 h 40 min

## 🎯 Objetivos
Al terminar podrás:
1. Agrupar datos en un diccionario (conteos, totales, promedios) con `.get()` y sin `KeyError`.
2. Llevar un estado (saldo, stock) que arranca en su valor inicial y detectar eventos mientras avanza.
3. Buscar extremos a mano con `None` como centinela, guardando el registro completo y decidiendo los empates.
4. Usar `min`, `max` y `sorted` con `key`, y combinar `zip`, `enumerate` y `dict(zip(...))`.
5. Resolver un extracto bancario completo, primero a tu manera y luego en un solo recorrido.

## 📋 Qué debes saber antes
Listas, tuplas y diccionarios básicos, `if`/`elif`/`else`, `for`, `while`, `break`, `continue` y f-strings.

## 🧭 Cómo trabajar este notebook
- Guarda una copia en tu Drive (**Archivo → Guardar una copia en Drive**).
- Ejecuta el **⚙️ Setup** al empezar y las celdas **en orden**, con **Shift + Enter**.
- En cada ejemplo, lee la línea 🔮 y escribe tu predicción en el comentario **antes** de ejecutar.
- En cada ✍️ **Tu turno** escribe tu código debajo de `# Tu código aquí` y luego ejecuta ✅ **Verificar**. Si aparece ❌, lee el motivo: te dice qué error típico cometiste.
- Si te atascas, abre la 💡 **Pista** (hay dos, de menos a más ayuda). Las 🔒 **soluciones** están en el anexo final.
- Si modificas los datos por error, vuelve a ejecutar el setup.

| Bloque | Tiempo |
|---|---|
| Parte 1 · Diccionarios: agrupar y acumular (secciones 1-4) | 50 min |
| Parte 2 · Estado acumulativo y control de flujo (secciones 5-8) | 70 min |
| Parte 3 · Tuplas, `key`, `zip` y tablas (secciones 9-12) | 50 min |
| 🏋️ Reto final + 🚀 Nivel pro | 40 min |
| Portada y cierre | 10 min |

## 🎯 Errores típicos que vas a cazar hoy
1. Arrancar el estado en 0 y «corregirlo» al final: el resultado final coincide, pero los valores intermedios y los eventos quedan mal.
2. Filtrar el monto 0 donde no hace falta (en un saldo) y no filtrarlo donde sí importa (en un diccionario, donde crea una clave).
3. Usar 0 como valor inicial de un extremo: funciona por accidente con egresos y falla cuando todo es positivo.
4. Leer una clave que aún no existe (`KeyError`) o usar `.get()` sin valor por defecto (`None + 1`).
5. Escribir un `for` por cada resultado en vez de llevar varios acumuladores en un solo recorrido.
6. Entregar `477.5799999999999` en lugar de redondear, o comparar decimales con `==`.
7. `min(lista_de_tuplas)` sin `key`, que compara por la fecha y no por el monto.
8. Un `continue` que se salta un caso válido antes del chequeo importante.
""", id="portada")


def setup(nb):
    nb.md("""
## ⚙️ Setup
Ejecuta la celda siguiente **al empezar** (y otra vez si reinicias el entorno). Carga los datos de práctica y las funciones que revisan tus respuestas.

⚠️ **Ejecútala y no la edites.**
""", id="setup-intro")
    nb.codigo((AQUI / "celda_setup.py").read_text(encoding="utf-8")
              .replace("# (Este archivo es la fuente de la celda de setup del notebook: no se importa, se copia tal cual.)\n", ""),
              id="setup")
    nb.md("""
### 📦 Tus datos de hoy
Todos los ejercicios usan estas variables. Son datos fijos: siempre salen iguales.
""", id="datos-intro")
    nb.codigo('''
def mostrar(nombre, valor):
    if isinstance(valor, list) and valor and isinstance(valor[0], (tuple, list)):
        print(f"{nombre} =")
        for elemento in valor:
            print("   ", elemento)
    else:
        print(f"{nombre} = {valor}")

print("🧺 Parte 1 · Diccionarios")
for nombre in ["ventas_bodega", "movimientos_junio", "compras_mes"]:
    mostrar(nombre, globals()[nombre])
print("\\n💰 Parte 2 · Estado acumulativo")
for nombre in ["saldo_inicial_caja", "movimientos_caja", "saldo_inicial_cuenta", "movimientos_cuenta",
               "saldo_inicial_ahorro", "movimientos_ahorro", "saldo_inicial_agosto", "movimientos_agosto",
               "stock_inicial", "stock_minimo", "kardex"]:
    mostrar(nombre, globals()[nombre])
print("\\n🔢 Parte 3 · Tuplas, key y tablas")
for nombre in ["lista_prueba", "movimientos_abril", "fechas_semana", "ventas_dia", "clientes_dia",
               "locales", "meses", "ventas_mensuales"]:
    mostrar(nombre, globals()[nombre])
print("\\n🏋️ Reto final")
for nombre in ["saldo_inicial", "movimientos"]:
    mostrar(nombre, globals()[nombre])
''', id="datos")


def cierre(nb):
    nb.md("""
---
## ✅ Cierre: autoevaluación
Marca lo que puedes hacer sin mirar:
- [ ] Explicar por qué `d[clave]` da `KeyError` y cuándo usar `in` o `.get(clave, 0)`.
- [ ] Agrupar (conteo, total y promedio) con varios acumuladores en un solo `for`.
- [ ] Redondear al entregar y comparar decimales sin `==`.
- [ ] Explicar por qué el saldo arranca en `saldo_inicial` y no en 0.
- [ ] Distinguir «estar en rojo» de «entrar en rojo», y saber qué variable necesita lo segundo.
- [ ] Buscar un extremo con `None`, guardar el registro completo y decidir el empate con `<` o `<=`.
- [ ] Saber cuándo un `continue` es seguro y cuándo se salta un caso válido.
- [ ] Predecir comparaciones de tuplas y de textos, y evitar la trampa de `min(lista_de_tuplas)`.
- [ ] Usar `key` en `min`, `max` y `sorted`, incluida una `key` que devuelve una tupla.
- [ ] Combinar `zip`, `enumerate(..., start=1)` y `dict(zip(...))`, y encontrar el mejor de cada fila de una tabla.

### Lo que viene: los mismos patrones con otras herramientas
| Lo que practicaste hoy | En SQL | En pandas |
|---|---|---|
| Agrupar en un diccionario (`d[k] = d.get(k, 0) + x`) | `GROUP BY` | `groupby` |
| Saldo acumulado paso a paso | `SUM() OVER (ORDER BY fecha)` | `cumsum` |
| `min(registros, key=...)` para hallar la fila del mínimo | `ORDER BY ... LIMIT 1` | `idxmin` |
| Varios acumuladores en un solo recorrido | varias agregaciones en un `SELECT` | `agg` |

Esas herramientas harán por ti el recorrido que hoy escribiste a mano. Saber lo que pasa por dentro te ayudará a detectar resultados raros.
""", id="cierre")


def construir():
    nb = Libro()
    portada(nb)
    setup(nb)
    parte1.agregar(nb)
    parte2.agregar(nb)
    parte3.agregar(nb)
    reto.agregar(nb)
    cierre(nb)
    nb.anexo_soluciones()
    return nb.notebook()


def main():
    nb = construir()
    nbformat.validate(nb)
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, DESTINO)
    print(f"✅ {DESTINO.relative_to(RAIZ)}: {len(nb.cells)} celdas, nbformat {nb.nbformat}.{nb.nbformat_minor}")


if __name__ == "__main__":
    main()
