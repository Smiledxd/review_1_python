"""Portada y cierre del notebook."""

URL_COLAB = (
    "https://colab.research.google.com/github/Smiledxd/review_1_python/blob/main/"
    "sesiones/refuerzo_python_puro.ipynb"
)


def portada(libro):
    libro.md(f"""
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({URL_COLAB})

# 🧱 Refuerzo de Python puro
## Diccionarios, estado acumulativo y comparación de tuplas

Práctica intensiva de **≈ 3 h 40 min** con datos pequeños y realistas (ventas de bodega, movimientos de cuenta, kárdex de stock) en soles y con fechas ISO `AAAA-MM-DD`.
Solo usamos la **biblioteca estándar** de Python (`matplotlib` aparece una única vez, para un gráfico ilustrativo).
""", id="portada-titulo")

    libro.md("""
### ✅ Objetivos (marca una casilla cuando puedas hacerlo sin mirar)

**Módulo 1 — Diccionarios**
- ☐ Explicar por qué `d[clave]` da `KeyError` y evitarlo con `if clave in d`.
- ☐ Agrupar con el patrón `if / else` (inicializar en el `else`, sumar después).
- ☐ Acumular con `d.get(clave, 0)`.
- ☐ Recorrer con `for k in d`, `.keys()`, `.values()` y `.items()`, sabiendo qué se puede cambiar mientras recorres.
- ☐ Entender por qué aparece `477.5799999999999` y redondear al entregar el resultado.

**Módulo 2 — Estado acumulativo y control de flujo**
- ☐ Distinguir agregación final (`sum`) de seguimiento paso a paso.
- ☐ Arrancar el estado en su valor inicial (no en 0).
- ☐ Detectar eventos dentro del bucle: primero, todos y cruces (con el valor anterior).
- ☐ Buscar extremos a mano con `None` como centinela y guardar el registro completo.
- ☐ Elegir entre `break` y `continue` sin saltarte casos válidos.

**Módulo 3 — Tuplas y `key`**
- ☐ Predecir comparaciones de tuplas y de textos.
- ☐ Evitar la trampa de `min(lista_de_tuplas)`.
- ☐ Usar `key=` en `min`, `max` y `sorted`, incluido el desempate con una tupla.
- ☐ Combinar `zip` y `enumerate`.

**Reto final**
- ☐ Resolver un problema completo primero a tu manera y luego en **un solo recorrido**.
""", id="portada-objetivos")

    libro.md("""
### 🧭 Cómo usar este notebook

1. **Guarda una copia en tu Drive** (`Archivo → Guardar una copia en Drive`) para no perder tu trabajo.
2. **Ejecuta las celdas en orden**, de arriba abajo.
3. **Intenta antes de abrir pistas.** Cada ejercicio trae 1 o 2 celdas «💡 Pista» que aparecen colapsadas: haz doble clic o pulsa *Mostrar código* solo si estás atascado. Las **🔒 Soluciones** están al final de cada módulo.
4. Las celdas **🔮 Predice antes de ejecutar** tienen comentarios donde escribes tu predicción. Escríbela *antes* de ejecutar: equivocarte ahí es lo que más enseña.
5. Cada ejercicio es independiente: define sus propios datos en la misma celda. Al terminar tu código, ejecuta la celda de validación; si falla, el mensaje te apunta al error típico.

| Bloque | Tiempo |
|---|---|
| Portada | 5 min |
| Módulo 1 — Diccionarios: agrupación y acumulación | 50 min |
| Módulo 2 — Estado acumulativo y control de flujo | 70 min |
| Módulo 3 — Comparación de tuplas y parámetro `key` | 50 min |
| Reto final integrador | 40 min |
| Cierre | 5 min |
| **Total** | **≈ 3 h 40 min** |
""", id="portada-uso")

    libro.md("""
### 🎯 Errores típicos que vas a cazar hoy

1. **Arrancar el estado en 0 y «corregirlo» al final** (sumar el valor inicial después del bucle). El resultado final puede salir bien, pero los valores intermedios y los eventos quedan mal.
2. **Filtrar casos que no cambian nada** (sumar 0 no altera un saldo) o, al revés, **no filtrar donde sí importa** (un movimiento de 0 puede crear una clave que no debería existir).
3. **Usar 0 como valor inicial de un extremo.** Funciona por accidente cuando el 0 hace de filtro y falla cuando todos los valores son positivos. El centinela correcto es `None`.
4. **Leer una clave que aún no existe** (`KeyError`) o usar `.get(clave)` sin valor por defecto (`None + 1` da `TypeError`).
5. **Escribir un `for` distinto para cada resultado** en vez de llevar varios acumuladores en un solo recorrido.
6. **No redondear el resultado que se entrega** (`477.5799999999999`) o comparar decimales con `==`.
7. **`min(lista_de_tuplas)` sin `key`:** compara por el primer elemento (la fecha), no por el monto.
8. **Un `continue` mal ubicado** que se salta un caso válido antes de que el chequeo importante ocurra.
""", id="portada-errores")


def cierre(libro):
    libro.md("""
## 🏁 Cierre

### Checklist de autoevaluación
Marca solo lo que lograrías **sin abrir una pista**:

- ☐ Agrupo por categoría (total y conteo) con `.get` y un solo `for`.
- ☐ Redondeo al entregar y comparo decimales con `round` o `math.isclose`.
- ☐ Arranco el estado en su valor inicial y puedo explicar por qué.
- ☐ Distingo «estar en sobregiro» de «entrar en sobregiro» y sé qué variable me falta para lo segundo.
- ☐ Busco extremos con `None`, guardo el registro completo y decido el empate con `<` o `<=`.
- ☐ Sé cuándo un `continue` es seguro y cuándo se salta un caso válido.
- ☐ Predigo comparaciones de tuplas y de textos (fechas con y sin ceros).
- ☐ Uso `min`/`max`/`sorted` con `key`, incluido `key` que devuelve una tupla.
- ☐ Combino `zip` y `enumerate(..., start=1)`.

### Lo que viene (los mismos patrones con otras herramientas)

| Lo que practicaste hoy | Lo que viene |
|---|---|
| Agrupar en un diccionario (`d[k] = d.get(k, 0) + x`) | `GROUP BY` en SQL · `groupby` en pandas |
| Saldo acumulado paso a paso (running total) | `SUM() OVER (ORDER BY fecha)` en SQL · `cumsum` en pandas |
| `min(registros, key=...)` para hallar la fila del mínimo | `idxmin` en pandas |
| Varios acumuladores en un solo recorrido | `agg` con varias funciones · varias columnas en un `SELECT ... GROUP BY` |

Cuando llegues a esas herramientas, notarás que cada una hace por ti el recorrido que hoy escribiste a mano; entender lo que pasa dentro te permitirá detectar resultados raros.
""", id="cierre")
