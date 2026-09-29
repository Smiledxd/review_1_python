"""Parte 3 · Comparación de tuplas, `key`, `zip` y tablas (secciones 9 a 12)."""

from libro import Ejercicio


def agregar(nb):
    nb.md("""
---
# Parte 3 · Comparación de tuplas, `key`, `zip` y tablas
⏱️ 50 minutos · Secciones 9 a 12
""", id="parte-3")

    # ------------------------------------------------------------------ 9
    nb.md("""
---
## 9. Cómo compara Python tuplas y textos

### 📘 Concepto
**Tuplas:** se comparan **elemento por elemento, de izquierda a derecha**.
1. Compara el índice 0. Si son distintos, ahí se decide y **nada más se mira**.
2. Solo si empatan, pasa al índice 1, y así sucesivamente.
3. Si todo lo comparado es igual, la tupla más corta es la menor.

**Textos:** se comparan **carácter por carácter**, no como números: `"10" < "9"` es `True` porque `"1"` va antes que `"9"`.

Por eso las fechas ISO **con ceros** (`"2026-09-02"`, todas del mismo largo) ordenan bien como texto, y **sin ceros** (`"2026-9-10"`) no.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿True o False en la primera línea? ¿Qué orden sale en las dos últimas?
# Mi predicción:

a_ej = ("2026-09-10", -5)
b_ej = ("2026-09-02", -500)
for i in range(len(a_ej)):
    if a_ej[i] == b_ej[i]:
        print(f"índice {i}: {a_ej[i]!r} == {b_ej[i]!r} → empate, sigo")
    else:
        print(f"índice {i}: {a_ej[i]!r} vs {b_ej[i]!r} → decide aquí: {a_ej[i] < b_ej[i]}")
        break
print("a_ej < b_ej:", a_ej < b_ej)

print(sorted(["2026-10-01", "2026-09-15", "2026-09-02"]), "← con ceros: bien")
print(sorted(["2026-10-1", "2026-9-15", "2026-9-2"]), "← sin ceros: orden roto")
''')
    nb.ejercicio(Ejercicio(
        clave="9", titulo="Ejercicio 9: predicciones de comparación", check="check_ejercicio_9()",
        enunciado="""
Predice **sin ejecutar** (`True` o `False`; en `pred_min`, la tupla que devuelve):

| Variable | Expresión |
|---|---|
| `pred_a` | `("2026-11-03", 10) < ("2026-11-03", 9)` |
| `pred_b` | `("b", 1) < ("a", 99)` |
| `pred_c` | `(1, 500) < (1, 1000)` |
| `pred_d` | `("2026-10-5", 0) < ("2026-10-15", 0)` |
| `pred_e` | `"100" < "25"` |
| `pred_f` | `(7, 3) < (7, 3, 0)` |
| `pred_min` | `min(lista_prueba)` (mira `lista_prueba` en 📦 Tus datos) |
""",
        pistas=[
            "En cada par de tuplas mira **solo el índice 0**. Si son distintos, ahí se decide. Si empatan, pasa al índice 1.",
            "En los textos compara carácter por carácter desde la izquierda. Para `pred_min`, busca la fecha más antigua y, si hay dos con esa fecha, mira el monto.",
        ],
        solucion='''
pred_a = False   # empatan en la fecha; decide 10 < 9
pred_b = False   # decide el índice 0: "b" < "a" es False; el 99 no se mira
pred_c = True    # empatan en 1; decide 500 < 1000 (son números)
pred_d = False   # sin ceros se compara "5" con "1" como caracteres
pred_e = True    # "1" < "2"
pred_f = True    # todo lo comparado empata: la más corta es menor
pred_min = ("2026-04-20", 40.0)   # la fecha más antigua; en el empate de fecha decide el monto
''',
        errores="leer textos como números (`\"100\" < \"25\"` es `True`) o mirar el monto cuando la fecha ya decidió.",
    ))

    # ------------------------------------------------------------------ 10
    nb.md("""
---
## 10. La trampa de `min(lista_de_tuplas)` y el parámetro `key`

### 📘 Concepto
`min(movimientos)` compara **tuplas completas**, así que decide por el **índice 0, la fecha**: devuelve el movimiento más **antiguo**, no el de menor monto. `max` devuelve el más **reciente**. No da error: da un resultado con pinta razonable, pero incorrecto.

`key` le dice a Python **qué comparar**. Recibe una función que se aplica a cada elemento y devuelve el elemento **original**:

| Quiero | Código |
|---|---|
| movimiento de menor monto | `min(movs, key=lambda m: m[2])` |
| movimiento de mayor monto | `max(movs, key=lambda m: m[2])` |
| ordenar por monto, de menor a mayor | `sorted(movs, key=lambda m: m[2])` |
| ordenar de mayor a menor | `sorted(movs, key=lambda m: m[2], reverse=True)` |
| mayor monto y, si empatan, fecha más antigua | `sorted(movs, key=lambda m: (-m[2], m[0]))` |
| la clave con mayor valor de un diccionario | `max(d, key=d.get)` |

`lambda m: m[2]` es una función pequeña sin nombre: «dado `m`, devuelve `m[2]`». Si varios empatan en la `key`, `min` y `max` devuelven el **primero**.

⚠️ Con montos negativos, «el egreso más grande» es el número **más bajo**: `sorted(..., key=lambda m: m[2])` ya lo deja primero, y `reverse=True` lo manda al final.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿qué devuelve `min` sin key? ¿Y con key?
# Mi predicción:

movs_ej = [
    ("2026-03-01", "mercado", -45.20),
    ("2026-03-06", "sueldo", 1800.00),
    ("2026-03-09", "alquiler", -650.00),
    ("2026-03-14", "yape", 230.00),
    ("2026-03-20", "luz", -96.40),
]
print("min sin key :", min(movs_ej), "← el más ANTIGUO")
print("min con key :", min(movs_ej, key=lambda m: m[2]))
print("max con key :", max(movs_ej, key=lambda m: m[2]))
print("2 egresos más grandes:", sorted(movs_ej, key=lambda m: m[2])[:2])

gasto_ej = {"abarrotes": 320.5, "lácteos": 185.0, "bebidas": 402.25}
print("clave con mayor valor:", max(gasto_ej, key=gasto_ej.get))
print("ranking:", sorted(gasto_ej.items(), key=lambda kv: kv[1], reverse=True))
''')
    nb.ejercicio(Ejercicio(
        clave="10", titulo="Ejercicio 10 🐛: mayor ingreso, mayor egreso y top 3", check="check_ejercicio_10()",
        enunciado="""
La celda de abajo quiere obtener, de `movimientos_abril`:
1. `mayor_ingreso`: la tupla completa del movimiento con el monto más alto.
2. `mayor_egreso_abril`: la tupla completa del movimiento con el monto más negativo.
3. `top3_egresos`: lista con los 3 egresos más grandes, **del más negativo al menos negativo**.

Corre sin errores, pero los tres resultados están mal. Corrígela.
""",
        plantilla='''
# 🐛 Este código tiene errores. Corrígelo (puedes reescribirlo).
mayor_ingreso = max(movimientos_abril)
mayor_egreso_abril = min(movimientos_abril)

egresos_abril = []
for movimiento in movimientos_abril:
    if movimiento[2] < 0:
        egresos_abril.append(movimiento)
top3_egresos = sorted(egresos_abril, reverse=True)[:3]
''',
        pistas=[
            "Sin `key`, `max`, `min` y `sorted` comparan la tupla completa, empezando por el índice 0. ¿Qué hay en el índice 0?",
            "Agrega `key=lambda m: m[2]` en los tres. Para el top 3, como los egresos son negativos, el orden ascendente ya deja primero el más negativo: quita `reverse=True`.",
        ],
        solucion='''
mayor_ingreso = max(movimientos_abril, key=lambda m: m[2])        # compara por el monto
mayor_egreso_abril = min(movimientos_abril, key=lambda m: m[2])   # el más negativo es el mínimo

egresos_abril = []
for movimiento in movimientos_abril:
    if movimiento[2] < 0:
        egresos_abril.append(movimiento)
top3_egresos = sorted(egresos_abril, key=lambda m: m[2])[:3]      # ascendente: el más negativo primero
''',
        errores="`min`/`max`/`sorted` sin `key` comparan por la fecha. Con montos negativos, `reverse=True` "
                "deja primero el egreso más pequeño.",
    ))

    # ------------------------------------------------------------------ 11
    nb.md("""
---
## 11. `zip`, `enumerate` y `dict(zip(...))`

### 📘 Concepto
| Herramienta | Qué da | Ojo |
|---|---|---|
| `zip(a, b)` | pares `(a[0], b[0])`, `(a[1], b[1])`… de listas paralelas | se corta en la más corta, sin avisar |
| `enumerate(a, start=1)` | pares `(1, a[0])`, `(2, a[1])`… | sin `start=1` cuenta desde 0 |
| `dict(zip(claves, valores))` | un diccionario en **una línea** | si hay claves repetidas, gana la última |

Combinados: `for numero, (fecha, venta) in enumerate(zip(fechas, ventas), start=1):` (el par de `zip` va entre paréntesis).

Para un ranking con desempate, arma primero una lista de tuplas con todo lo que necesitas y ordénala con una `key` que devuelva una tupla: `key=lambda r: (-r[2], r[3])` ordena por el índice 2 de mayor a menor y, si empatan, por el índice 3 de menor a mayor.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿cuántos pares da zip? ¿Qué día gana el ranking y por qué?
# Mi predicción:

dias_ej = ["lunes", "martes", "miércoles", "jueves"]
ventas_ej = [120.0, 210.0, 95.5, 210.0, 80.0]      # ¡una venta de más!
clientes_ej = [30, 52, 25, 41]

print(list(zip(dias_ej, ventas_ej)), "← se cortó en la más corta")
print(dict(zip(dias_ej, ventas_ej)))

registros_ej = []
for numero, (dia, venta, clientes) in enumerate(zip(dias_ej, ventas_ej, clientes_ej), start=1):
    registros_ej.append((numero, dia, venta, clientes))
for puesto, registro in enumerate(sorted(registros_ej, key=lambda r: (-r[2], r[3])), start=1):
    print(f"{puesto}.º", registro)
''')
    nb.ejercicio(Ejercicio(
        clave="11", titulo="Ejercicio 11: ranking de días con desempate", check="check_ejercicio_11()",
        enunciado="""
`fechas_semana`, `ventas_dia` y `clientes_dia` son listas paralelas de una semana. Crea:
1. `venta_por_fecha`: diccionario `fecha → venta` en **una línea** con `dict(zip(...))`.
2. `ranking`: lista de tuplas `(numero_dia, fecha, venta, clientes)`, donde `numero_dia` va de 1 a 7. Ordénala de **mayor a menor venta** y, si dos días empatan en venta, primero el de **menos clientes**. Usa `enumerate(zip(...), start=1)`.
3. `dia_ganador` y `fecha_ganadora`: el número de día y la fecha del primer lugar.
""",
        pistas=[
            "Primero arma una lista con `append` recorriendo `enumerate(zip(fechas_semana, ventas_dia, clientes_dia), start=1)`. Después ordénala.",
            "`ranking = sorted(registros, key=lambda r: (-r[2], r[3]))`: el signo menos invierte el orden de la venta y `r[3]` desempata. El ganador es `ranking[0]`.",
        ],
        solucion='''
venta_por_fecha = dict(zip(fechas_semana, ventas_dia))

registros = []
for numero, (fecha, venta, clientes) in enumerate(zip(fechas_semana, ventas_dia, clientes_dia), start=1):
    registros.append((numero, fecha, venta, clientes))
ranking = sorted(registros, key=lambda r: (-r[2], r[3]))   # venta desc; empate: menos clientes

dia_ganador = ranking[0][0]
fecha_ganadora = ranking[0][1]
''',
        errores="ordenar solo por venta: los empates quedan en el orden original y gana otro día. "
                "Sin `start=1` los números de día empiezan en 0.",
    ))

    # ------------------------------------------------------------------ 12
    nb.md("""
---
## 12. Tablas: el mejor de cada fila

### 📘 Concepto
En una lista de listas, `tabla[i]` es la fila `i` y `tabla[i][j]` el valor de la fila `i`, columna `j`. Para un resultado **por fila**, recorre las filas y, dentro, trabaja con cada una:

```python
for nombre, fila in zip(nombres, tabla):         # una vuelta por fila
    mejor_j = 0
    for j in range(1, len(fila)):                 # un bucle dentro de otro
        if fila[j] > fila[mejor_j]:               # `>`: en el empate gana la primera columna
            mejor_j = j
```

Atajo: `fila.index(max(fila))` da la posición de la **primera** aparición del máximo. Las posiciones empiezan en 0: si te piden «mes 1 a 6», suma 1.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿en qué día (1 a 3) tuvo su mejor venta cada vendedor?
# Mi predicción:

vendedores_ej = ["Ana", "Luis"]
tabla_ej = [
    [120, 340, 340],     # Ana: empate entre el día 2 y el 3
    [200, 150, 310],     # Luis
]

for nombre, fila in zip(vendedores_ej, tabla_ej):
    mejor_j = 0
    for j in range(1, len(fila)):
        if fila[j] > fila[mejor_j]:
            mejor_j = j
    con_index = fila.index(max(fila))
    print(f"{nombre:<5} {fila} → mejor día {mejor_j + 1} (con .index: {con_index + 1}) | total {sum(fila)}")
''')
    nb.ejercicio(Ejercicio(
        clave="12", titulo="Ejercicio 12: el mejor mes de cada local", check="check_ejercicio_12()",
        enunciado="""
En `ventas_mensuales` cada fila es un local (en el orden de `locales`) y cada columna un mes (en el orden de `meses`, de enero a junio). Crea:
1. `total_por_local`: diccionario `local → venta total de sus 6 meses`.
2. `mejor_mes_por_local`: diccionario `local → número de mes (1 a 6)` en que tuvo su mayor venta. Si hay empate, el primer mes.
3. `local_top`: el local con mayor venta total.
""",
        pistas=[
            "Recorre `zip(locales, ventas_mensuales)`: en cada vuelta tienes el nombre y su fila completa. El total es `sum(fila)`.",
            "Para el mejor mes usa un bucle interno con `>` (o `fila.index(max(fila))`) y súmale 1. Para `local_top`: `max(total_por_local, key=total_por_local.get)` o una búsqueda a mano con `None`.",
        ],
        solucion='''
total_por_local = {}
mejor_mes_por_local = {}
for local, fila in zip(locales, ventas_mensuales):
    total_por_local[local] = sum(fila)
    mejor_j = 0
    for j in range(1, len(fila)):
        if fila[j] > fila[mejor_j]:          # `>`: en el empate se queda el primer mes
            mejor_j = j
    mejor_mes_por_local[local] = mejor_j + 1  # meses del 1 al 6

local_top = max(total_por_local, key=total_por_local.get)
''',
        errores="usar `>=` (en el empate gana el último mes) u olvidar sumar 1 a la posición.",
    ))
