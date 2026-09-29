"""Parte 1 · Diccionarios: agrupar y acumular (secciones 1 a 4)."""

from libro import Ejercicio


def agregar(nb):
    nb.md("""
---
# Parte 1 · Diccionarios: agrupar y acumular
⏱️ 50 minutos · Secciones 1 a 4
""", id="parte-1")

    # ------------------------------------------------------------------ 1
    nb.md("""
---
## 1. El ciclo de vida de una clave

### 📘 Concepto
Una clave **nace cuando le asignas un valor** (`d["leche"] = 5`). Hasta entonces no existe:

| Operación | Si la clave existe | Si no existe |
|---|---|---|
| `d[clave]` | devuelve el valor | `KeyError`: el programa se detiene |
| `clave in d` | `True` | `False` |
| `d[clave] = valor` | cambia el valor | **crea** la clave |

`in` pregunta por las **claves**, nunca por los valores.

**Patrón clásico para agrupar** (categoría → conteo o total):
```python
if categoria in conteo:
    conteo[categoria] += 1      # ya existía: acumular
else:
    conteo[categoria] = 1       # primera vez: nace con el valor de ESTA vuelta
```
⚠️ Si en el `else` pones `= 0`, la primera aparición de cada categoría se pierde.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿con cuánto termina "lácteos"? ¿En qué vuelta nace "bebidas"?
# Mi predicción:

pedidos_ej = [("lácteos", 8.50), ("abarrotes", 23.00), ("lácteos", 6.50), ("bebidas", 4.00), ("lácteos", 9.00)]

conteo_ej = {}
print(f"{'vuelta':<7}| {'elemento':<22}| {'conteo':<44}| evento")
for vuelta, (categoria, monto) in enumerate(pedidos_ej, start=1):
    if categoria in conteo_ej:
        conteo_ej[categoria] += 1
        evento = "ya existía → acumula"
    else:
        conteo_ej[categoria] = 1
        evento = "NACE la clave → empieza en 1"
    print(f"{vuelta:<7}| {str((categoria, monto)):<22}| {str(conteo_ej):<44}| {evento}")

try:
    print(conteo_ej["snacks"])
except KeyError as error:
    print("\\nKeyError: la clave", error, "nunca nació")
''')
    nb.ejercicio(Ejercicio(
        clave="1", titulo="Ejercicio 1: conteo por categoría", check="check_ejercicio_1()",
        enunciado="""
**Parte A.** `ventas_bodega` tiene tuplas `(fecha, categoria, monto)`. Crea `conteo_por_categoria`: un diccionario `categoría → cantidad de ventas`, con el patrón `if ... in ... / else`. No modifiques `ventas_bodega`.

**Parte B · casos borde.** Predice **sin ejecutar**:

| Variable | Pregunta |
|---|---|
| `pred_in_cero` | ¿qué valor da `"azúcar" in {"azúcar": 0}`? |
| `pred_in_valor` | ¿qué valor da `12 in {"arroz": 12}`? |
| `pred_error` | ¿qué error lanza `{"arroz": 12}["Arroz"]`? Escribe su nombre como texto (por ejemplo, `"ValueError"`). |
""",
        pistas=[
            "Crea el diccionario vacío **antes** del bucle. En cada vuelta pregunta si la categoría ya es clave.",
            "`for fecha, categoria, monto in ventas_bodega:` → si `categoria in conteo_por_categoria`, súmale 1; si no, créala **con 1**. "
            "En la parte B, recuerda que `in` mira solo las claves y que las mayúsculas cuentan.",
        ],
        solucion='''
# Parte A
conteo_por_categoria = {}
for fecha, categoria, monto in ventas_bodega:
    if categoria in conteo_por_categoria:
        conteo_por_categoria[categoria] += 1   # ya existía: acumular
    else:
        conteo_por_categoria[categoria] = 1    # primera vez: nace con 1

# Parte B
pred_in_cero = True       # la clave existe, aunque su valor sea 0
pred_in_valor = False     # `in` busca entre las claves, no entre los valores
pred_error = "KeyError"   # "Arroz" y "arroz" son claves distintas
''',
        errores="inicializar en 0 dentro del `else` hace que la primera venta de cada categoría no cuente. "
                "Sumar `monto` en lugar de 1 convierte el conteo en un total.",
    ))

    # ------------------------------------------------------------------ 2
    nb.md("""
---
## 2. `.get()` para acumular, y los decimales

### 📘 Concepto
`d.get(clave, defecto)` devuelve `d[clave]` si existe y, si no, `defecto`. Nunca lanza `KeyError`. Con él, acumular cabe en una línea y sin `if`:

```python
totales[categoria] = totales.get(categoria, 0) + monto
```

Sin valor por defecto, `.get()` devuelve `None`, y `None + monto` lanza `TypeError`. **Al acumular, pasa siempre el `0`.**

**¿Por qué sale `37.849999999999994`?** Python guarda los decimales en binario y valores como `0.1` no caben exactos, así que al sumar aparecen restos diminutos. No es un error tuyo:
- **Acumula sin redondear y redondea al entregar** el resultado, con `round(x, 2)`.
- Redondear los valores de un diccionario ya armado está permitido: `for c in d: d[c] = round(d[c], 2)`.
- Para comparar decimales no uses `==`: usa `round(x, 2) == y` o `math.isclose(x, y)`.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿el total de "snacks" sale exacto (6.8) o con restos?
# Mi predicción:
import math

ventas_ej = [("lácteos", 12.80), ("snacks", 2.20), ("lácteos", 9.60), ("snacks", 1.10), ("lácteos", 15.45), ("snacks", 3.50)]

totales_ej = {}
for categoria, monto in ventas_ej:
    totales_ej[categoria] = totales_ej.get(categoria, 0) + monto
    print(f"{categoria:<8} + {monto:>6.2f} → {totales_ej}")

print("\\nsin redondear:", totales_ej)
print("¿snacks == 6.8?", totales_ej["snacks"] == 6.8, "| ¿isclose?", math.isclose(totales_ej["snacks"], 6.8))
for categoria in totales_ej:
    totales_ej[categoria] = round(totales_ej[categoria], 2)
print("al entregar:  ", totales_ej)
''')
    nb.ejercicio(Ejercicio(
        clave="2", titulo="Ejercicio 2: total por categoría con `.get()`", check="check_ejercicio_2()",
        enunciado="""
**Parte A.** Con `ventas_bodega`, crea `total_por_categoria`: `categoría → total vendido`. Acumula con `.get(categoria, 0)` (sin `if/else`) y **entrega cada total redondeado a 2 decimales**.

**Parte B.** Predice **sin ejecutar**:

| Variable | Pregunta |
|---|---|
| `pred_igual` | ¿qué valor da `0.1 + 0.2 == 0.3`? |
| `pred_redondeado` | ¿qué valor da `round(0.1 + 0.2, 2) == 0.3`? |
| `pred_error_get` | ¿qué error lanza `{"lunes": 120.0}.get("martes") + 50`? Escribe su nombre como texto. |
""",
        pistas=[
            "Una sola línea dentro del `for`: lee lo que ya hay (o 0) con `.get` y súmale el monto. El redondeo va **después** del `for`.",
            "`total_por_categoria[categoria] = total_por_categoria.get(categoria, 0) + monto`. Luego recorre el diccionario y guarda "
            "`round(total_por_categoria[categoria], 2)` en la misma clave.",
        ],
        solucion='''
# Parte A
total_por_categoria = {}
for fecha, categoria, monto in ventas_bodega:
    total_por_categoria[categoria] = total_por_categoria.get(categoria, 0) + monto

for categoria in total_por_categoria:          # al entregar: redondear
    total_por_categoria[categoria] = round(total_por_categoria[categoria], 2)

# Parte B
pred_igual = False          # 0.1 + 0.2 da 0.30000000000000004
pred_redondeado = True
pred_error_get = "TypeError"   # .get sin defecto devuelve None, y None + 50 falla
''',
        errores="usar `.get(categoria)` sin el 0 (da `None` y luego `TypeError`) o entregar los totales sin redondear. "
                "Recorrer otra vez las ventas para redondear no hace falta: basta recorrer el diccionario.",
    ))

    # ------------------------------------------------------------------ 3
    nb.md("""
---
## 3. Recorrer un diccionario y cuándo filtrar el 0

### 📘 Concepto
| Forma | Cada vuelta te da |
|---|---|
| `for k in d` o `for k in d.keys()` | la clave |
| `for v in d.values()` | el valor |
| `for k, v in d.items()` | el par `(clave, valor)` |

- **Cambiar valores** de claves que ya existen mientras recorres está bien.
- **Agregar o quitar claves** mientras recorres lanza `RuntimeError: dictionary changed size during iteration`.

**¿Hay que filtrar los montos 0?** Depende de lo que calculas:
- En un **total o un saldo**, sumar 0 no cambia nada: no hace falta filtrarlo.
- En un **diccionario**, un movimiento de 0 **crea una clave** que no debería existir: ahí sí filtra.
- Para quedarte solo con egresos, el filtro es `monto < 0`, que deja fuera ingresos y ceros a la vez. `monto != 0` deja pasar los ingresos.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿qué claves tendrá `con_distinto_de_cero`? ¿Y `con_menor_que_cero`?
# Mi predicción:

movs_ej = [("sueldo", 900.0), ("mercado", -40.0), ("ajuste", 0.0), ("mercado", -25.5)]

con_distinto_de_cero = {}
con_menor_que_cero = {}
for concepto, monto in movs_ej:
    if monto != 0:
        con_distinto_de_cero[concepto] = con_distinto_de_cero.get(concepto, 0) + monto
    if monto < 0:
        con_menor_que_cero[concepto] = con_menor_que_cero.get(concepto, 0) - monto   # en positivo
print(con_distinto_de_cero)
print(con_menor_que_cero)

for concepto, gasto in con_menor_que_cero.items():
    print(f"{concepto:<8} S/ {gasto:>7.2f}")

try:
    for concepto in con_menor_que_cero:
        con_menor_que_cero["nuevo"] = 1.0      # agregar claves mientras recorres
except RuntimeError as error:
    print("RuntimeError:", error)
''')
    nb.ejercicio(Ejercicio(
        clave="3", titulo="Ejercicio 3 🐛: encuentra y arregla el bug", check="check_ejercicio_3()",
        enunciado="""
La celda de abajo quiere armar `egresos_por_concepto`: `concepto → gasto`, con **solo los egresos** de `movimientos_junio`, guardados **en positivo** y redondeados a 2 decimales. Corre sin errores, pero el resultado está mal.

Ejecútala, verifica, lee los ❌ y corrígela.
""",
        plantilla='''
# 🐛 Este código tiene errores. Corrígelo (puedes reescribirlo).
egresos_por_concepto = {}
for fecha, concepto, monto in movimientos_junio:
    if monto != 0:
        egresos_por_concepto[concepto] = egresos_por_concepto.get(concepto, 0) + monto
''',
        pistas=[
            "Hay tres cosas que revisar: **qué** movimientos pasan el filtro, **qué** se suma (mira el signo) y si el resultado se entrega redondeado.",
            "El filtro correcto es `monto < 0`. Al acumular, suma `-monto` para que quede en positivo. Al final, redondea recorriendo el diccionario.",
        ],
        solucion='''
egresos_por_concepto = {}
for fecha, concepto, monto in movimientos_junio:
    if monto < 0:                                # solo egresos: fuera ingresos y ceros
        egresos_por_concepto[concepto] = egresos_por_concepto.get(concepto, 0) - monto   # en positivo

for concepto in egresos_por_concepto:            # al entregar: redondear
    egresos_por_concepto[concepto] = round(egresos_por_concepto[concepto], 2)
''',
        errores="`monto != 0` deja pasar los ingresos y mezcla signos. Con `monto < 0` se descartan ingresos y ceros de una vez, "
                "y sumando `-monto` el gasto queda en positivo.",
    ))

    # ------------------------------------------------------------------ 4
    nb.md("""
---
## 4. Varios acumuladores en un solo recorrido

### 📘 Concepto
Si necesitas varios resultados de los mismos datos, no escribas un `for` para cada uno: **lleva varios acumuladores en un solo recorrido**.

Lo que depende de un diccionario **ya completo** (un promedio, la categoría con más ventas) va **después**, recorriendo ese diccionario con `.items()`.

**El mayor a mano**, sin `max`: empieza en `None` («todavía no hay ninguno») y reemplázalo cuando encuentres algo mejor:
```python
mejor = None
for clave, valor in d.items():
    if mejor is None or valor > d[mejor]:
        mejor = clave
```
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿qué categoría queda como `mas_vendida_ej`?
# Mi predicción:

ventas_ej = [("lácteos", 8.5), ("abarrotes", 23.0), ("lácteos", 6.5), ("bebidas", 4.0), ("abarrotes", 15.0)]

total_ej, cantidad_ej = {}, {}
for categoria, monto in ventas_ej:              # UN recorrido, dos acumuladores
    total_ej[categoria] = total_ej.get(categoria, 0) + monto
    cantidad_ej[categoria] = cantidad_ej.get(categoria, 0) + 1

mas_vendida_ej = None
for categoria, total in total_ej.items():      # después: recorrer el diccionario ya armado
    promedio = total / cantidad_ej[categoria]
    print(f"{categoria:<10} total {total:>6.2f} | {cantidad_ej[categoria]} ventas | promedio {promedio:.2f}")
    if mas_vendida_ej is None or total > total_ej[mas_vendida_ej]:
        mas_vendida_ej = categoria
print("más vendida:", mas_vendida_ej)
''')
    nb.ejercicio(Ejercicio(
        clave="4", titulo="Ejercicio 4: compras del mes en un solo recorrido", check="check_ejercicio_4()",
        enunciado="""
`compras_mes` tiene las compras a proveedores `(fecha, categoria, monto)`. **Recorriendo `compras_mes` una sola vez**, crea:
1. `compras_total`: `categoría → total comprado`, redondeado a 2 decimales.
2. `compras_cantidad`: `categoría → número de compras`.

Después, recorriendo el diccionario:

3. `compras_promedio`: `categoría → total / cantidad`, redondeado a 2 decimales.
4. `categoria_mas_compras`: la categoría con mayor total, buscada **a mano** con `None` (sin `max`).
""",
        pistas=[
            "Dentro del único `for` sobre `compras_mes` van dos líneas con `.get`: una suma el monto y otra suma 1. "
            "El promedio y la categoría mayor salen de un segundo `for` sobre `compras_total.items()`.",
            "Calcula el promedio con el total **sin redondear** y redondea el resultado. Para la mayor: `categoria_mas_compras = None` "
            "y `if categoria_mas_compras is None or total > compras_total[categoria_mas_compras]:`. Redondea los totales al final.",
        ],
        solucion='''
compras_total = {}
compras_cantidad = {}
for fecha, categoria, monto in compras_mes:        # un solo recorrido, dos acumuladores
    compras_total[categoria] = compras_total.get(categoria, 0) + monto
    compras_cantidad[categoria] = compras_cantidad.get(categoria, 0) + 1

compras_promedio = {}
categoria_mas_compras = None                       # centinela: todavía no hay ninguna
for categoria, total in compras_total.items():
    compras_promedio[categoria] = round(total / compras_cantidad[categoria], 2)
    if categoria_mas_compras is None or total > compras_total[categoria_mas_compras]:
        categoria_mas_compras = categoria

for categoria in compras_total:                    # al entregar: redondear
    compras_total[categoria] = round(compras_total[categoria], 2)
''',
        errores="comparar compras sueltas en vez de totales (la compra más grande no es de la categoría con más gasto) "
                "o escribir un `for` distinto para cada resultado.",
    ))
