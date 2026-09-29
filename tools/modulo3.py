"""Módulo 3 — Comparación de tuplas y parámetro `key` (50 min)."""

from constructor import Ejercicio


def agregar(libro):
    libro.md("""
# Módulo 3 — Comparación de tuplas y parámetro `key`
⏱️ **50 min** · Objetivo: saber **qué compara Python** cuando le pides `min`, `max` o `sorted` sobre tuplas, y decírselo con `key` para que compare lo que tú necesitas.
""", id="m3-titulo")

    # ------------------------------------------------------------------
    # Concepto 1: comparación de tuplas
    # ------------------------------------------------------------------
    libro.md("## 1. Cómo compara Python dos tuplas")
    libro.prediccion(
        ["línea 1", "línea 2", "línea 3", "línea 4"],
        '''
print(('2026-09-10', -5) < ('2026-09-02', -500))      # línea 1
print((3, 'b') < (3, 'c'))                            # línea 2
print((2, 100) < (10, 0))                             # línea 3
print((5, 0, 1) < (5, 0))                             # línea 4
''')
    libro.md("""
**Teoría corta**

Python compara tuplas **elemento por elemento, de izquierda a derecha**:

1. Compara el índice 0. Si son **distintos**, ahí se decide y **nada más se mira**.
2. Solo si **empatan**, pasa al índice 1, y así sucesivamente.
3. Si todo lo comparado es igual, la tupla **más corta** es la menor.

Por eso `('2026-09-10', -5) < ('2026-09-02', -500)` es `False`: la fecha ya decide, y el monto ni se mira.
""")
    libro.ejemplo('''
a = ('2026-09-10', -5)
b = ('2026-09-02', -500)

for i in range(min(len(a), len(b))):
    if a[i] == b[i]:
        print(f"índice {i}: {a[i]!r} == {b[i]!r} → empate, sigo con el siguiente")
    else:
        print(f"índice {i}: {a[i]!r} vs {b[i]!r} → decide aquí: a < b es {a[i] < b[i]}")
        break

print("resultado completo:", a < b)
''')

    # ------------------------------------------------------------------
    # Concepto 2: textos
    # ------------------------------------------------------------------
    libro.md("## 2. Comparar textos: `'10' < '9'` y las fechas")
    libro.prediccion(
        ["línea 1", "línea 2", "línea 3", "línea 4", "línea 5"],
        '''
print('10' < '9')                                                 # línea 1
print('2026-09-10' < '2026-09-02')                                # línea 2
print('2026-9-10' < '2026-9-2')                                   # línea 3
print(sorted(['2026-10-01', '2026-09-15', '2026-09-02']))        # línea 4
print(sorted(['2026-9-10', '2026-9-2', '2026-10-1']))            # línea 5
''')
    libro.md("""
**Teoría corta**

- Los textos se comparan **carácter por carácter**, no como números: `'10' < '9'` es `True` porque `'1'` va antes que `'9'`.
- Las fechas ISO **con ceros** (`AAAA-MM-DD`, todas del mismo largo) **ordenan bien como texto**: comparar textos equivale a comparar fechas.
- **Sin ceros** (`'2026-9-10'`) el orden se rompe. Solución: convertir cada parte a `int` y comparar `(año, mes, día)` como tupla de números.
""")
    libro.ejemplo('''
con_ceros = ["2026-10-01", "2026-09-15", "2026-09-02"]
sin_ceros = ["2026-9-15", "2026-10-1", "2026-9-2"]

print("con ceros, ordenadas como texto:", sorted(con_ceros))
print("sin ceros, ordenadas como texto:", sorted(sin_ceros), "← orden roto")

convertidas = []
for texto in sin_ceros:
    anio, mes, dia = texto.split("-")
    convertidas.append((int(anio), int(mes), int(dia)))
print("sin ceros, como tuplas de números:", sorted(convertidas), "← orden correcto")
''')

    # ------------------------------------------------------------------
    # Concepto 3: la trampa de min(lista_de_tuplas)
    # ------------------------------------------------------------------
    libro.md("## 3. La trampa: `min(lista_de_tuplas)`")
    libro.prediccion(
        ["línea 1 (min de la lista)", "línea 2 (max de la lista)"],
        '''
movimientos = [
    ("2026-04-01", "mercado", -45.20),
    ("2026-04-06", "sueldo", 1800.00),
    ("2026-04-09", "alquiler", -650.00),
    ("2026-04-14", "yape", 230.00),
    ("2026-04-20", "luz", -96.40),
]
print(min(movimientos))          # línea 1
print(max(movimientos))          # línea 2
''')
    libro.md("""
**Teoría corta**

`min(movimientos)` compara **tuplas completas**, así que decide por el **índice 0: la fecha**. Devuelve el movimiento más **antiguo**, no el de **menor monto**. Con `max` pasa lo mismo: el más **reciente**.

Es una trampa silenciosa: no da error, da un resultado con pinta razonable pero incorrecto. Si tu dato interesante no está en el índice 0, necesitas decirle a Python **qué comparar**: eso es `key`.
""")
    libro.ejemplo('''
movimientos = [
    ("2026-04-01", "mercado", -45.20),
    ("2026-04-06", "sueldo", 1800.00),
    ("2026-04-09", "alquiler", -650.00),
    ("2026-04-14", "yape", 230.00),
    ("2026-04-20", "luz", -96.40),
]

print("min sin key      :", min(movimientos), "← el más ANTIGUO")

# Módulo 2 (a mano): centinela None + registro completo
mejor_registro = None
for registro in movimientos:
    if mejor_registro is None or registro[2] < mejor_registro[2]:
        mejor_registro = registro
print("a mano por monto :", mejor_registro)

# Lo mismo con key (siguiente sección)
print("min con key      :", min(movimientos, key=lambda m: m[2]))
''')

    # ------------------------------------------------------------------
    # Concepto 4: key
    # ------------------------------------------------------------------
    libro.md("## 4. El parámetro `key` en `min`, `max` y `sorted`")
    libro.prediccion(
        ["línea 1", "línea 2", "línea 3 (primeros 2 elementos)", "línea 4", "línea 5"],
        '''
movs = [("2026-03-09", "internet", -80.0), ("2026-03-01", "luz", -45.0),
        ("2026-03-05", "mercado", -80.0), ("2026-03-12", "yape", 150.0)]

print(min(movs, key=lambda m: m[2]))                             # línea 1
print(max(movs, key=lambda m: m[2]))                             # línea 2
print(sorted(movs, key=lambda m: (m[2], m[0]))[:2])              # línea 3

gasto = {"abarrotes": 320.5, "lácteos": 185.0, "bebidas": 402.25}
print(max(gasto, key=gasto.get))                                 # línea 4
print(max(gasto.items(), key=lambda kv: kv[1]))                  # línea 5
''')
    libro.md("""
**Teoría corta**

- `key` recibe una función que Python aplica a **cada elemento** para obtener **lo que se compara**. El elemento devuelto es el original, no la clave.
- `lambda m: m[2]` es una función pequeña sin nombre: «dado `m`, devuelve `m[2]`» (el monto).
- Sirve igual en `min`, `max` y `sorted`. En `sorted`, `reverse=True` ordena de mayor a menor.
- **Desempate:** haz que `key` devuelva una **tupla**. `lambda m: (-m[2], m[0])` ordena por monto **descendente** (el signo menos invierte) y, si empatan, por fecha **ascendente**.
- Si dos elementos empatan en la clave, `min` y `max` devuelven **el primero** que aparece.
- Diccionarios: `max(d, key=d.get)` devuelve la **clave** con mayor valor; `max(d.items(), key=lambda kv: kv[1])` devuelve el **par** `(clave, valor)`.
""")
    libro.ejemplo('''
ventas = [("2026-03-09", "abarrotes", 90.0), ("2026-03-01", "lácteos", 120.0),
          ("2026-03-05", "bebidas", 120.0), ("2026-03-12", "snacks", 45.0)]

print("mayor monto (empate → el primero):", max(ventas, key=lambda v: v[2]))
print("menor monto:", min(ventas, key=lambda v: v[2]))

print("\\nranking de mayor a menor, desempate por fecha más antigua:")
for posicion, venta in enumerate(sorted(ventas, key=lambda v: (-v[2], v[0])), start=1):
    print(f"  {posicion}. {venta}")

print("\\nmás reciente:", max(ventas, key=lambda v: v[0]))
''')

    # ------------------------------------------------------------------
    # Concepto 5: zip y enumerate
    # ------------------------------------------------------------------
    libro.md("## 5. `zip` y `enumerate`")
    libro.prediccion(
        ["línea 1", "línea 2", "línea 3, 4 y 5 (el for)"],
        '''
fechas = ["2026-05-01", "2026-05-02", "2026-05-03"]
ventas = [120.0, 95.5, 210.0, 80.0]

print(list(zip(fechas, ventas)))                                 # línea 1
print(list(enumerate(fechas, start=1)))                          # línea 2
for numero, (fecha, venta) in enumerate(zip(fechas, ventas), start=1):
    print(numero, fecha, venta)                                  # líneas 3 a 5
''')
    libro.md("""
**Teoría corta**

- **`zip(a, b)`** recorre **listas paralelas** a la vez, emparejando por posición: `(a[0], b[0])`, `(a[1], b[1])`… **Se corta en la más corta**: los elementos sobrantes se ignoran sin avisar.
- **`enumerate(a, start=1)`** te da la **posición** junto al elemento: `(1, a[0])`, `(2, a[1])`… Úsalo cuando necesitas el número de orden («día 3»).
- **Combinados:** `for numero, (x, y) in enumerate(zip(a, b), start=1):` — el par va entre paréntesis porque `zip` entrega una tupla dentro de la tupla de `enumerate`.
""")
    libro.ejemplo('''
dias = ["lunes", "martes", "miércoles"]
ventas = [120.0, 95.5, 210.0, 80.0]      # ¡una más que los días!

print("zip se corta en la más corta:", len(list(zip(dias, ventas))), "pares de", len(ventas), "ventas")

mejor_numero, mejor_dia, mejor_venta = None, None, None
for numero, (dia, venta) in enumerate(zip(dias, ventas), start=1):
    print(f"día {numero}: {dia:<10} S/ {venta:>7.2f}")
    if mejor_venta is None or venta > mejor_venta:
        mejor_numero, mejor_dia, mejor_venta = numero, dia, venta
print(f"\\nmejor: día {mejor_numero} ({mejor_dia}) con S/ {mejor_venta:.2f}")
''')

    # ------------------------------------------------------------------
    # Ejercicios
    # ------------------------------------------------------------------
    libro.md("## 🏋️ Ejercicios del módulo 3")

    # ---- 3.1 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="3.1", titulo="Predicciones evaluadas", nivel="🟢 Básico",
        enunciado="""
Escribe **tu predicción** para cada expresión **sin ejecutarla** (`True` o `False`; en la última, la tupla que devuelve `min`). La validación evalúa las expresiones reales y compara con lo que escribiste.

**Variables a crear**

| Nombre | Tipo | Expresión a predecir |
|---|---|---|
| `pred_a` | `bool` | `('2026-11-03', 10) < ('2026-11-03', 9)` |
| `pred_b` | `bool` | `('b', 1) < ('a', 99)` |
| `pred_c` | `bool` | `(1, 500) < (1, 1000)` |
| `pred_d` | `bool` | `('2026-10-5', 0) < ('2026-10-15', 0)` |
| `pred_e` | `bool` | `'100' < '25'` |
| `pred_f` | `bool` | `(7, 3) < (7, 3, 0)` |
| `pred_min` | `tuple` | `min(lista_prueba)` |
""",
        datos='''
lista_prueba = [("2026-05-01", 30.0), ("2026-04-20", 90.0), ("2026-05-01", 25.0),
                ("2026-04-27", 15.5), ("2026-05-09", 12.0), ("2026-04-20", 40.0)]
''',
        plantilla='''
# Escribe True o False (sin ejecutar la expresión):
pred_a = None   # ('2026-11-03', 10) < ('2026-11-03', 9)
pred_b = None   # ('b', 1) < ('a', 99)
pred_c = None   # (1, 500) < (1, 1000)
pred_d = None   # ('2026-10-5', 0) < ('2026-10-15', 0)
pred_e = None   # '100' < '25'
pred_f = None   # (7, 3) < (7, 3, 0)
pred_min = None # la tupla que devuelve min(lista_prueba)
''',
        validacion='''
assert pred_a is (('2026-11-03', 10) < ('2026-11-03', 9)), \\
    "pred_a: las fechas empatan en el índice 0, así que decide el índice 1 (¿10 < 9?)."
assert pred_b is (('b', 1) < ('a', 99)), \\
    "pred_b: se decide en el índice 0 ('b' vs 'a'); el 99 no se mira."
assert pred_c is ((1, 500) < (1, 1000)), \\
    "pred_c: empatan en el índice 0; decide 500 < 1000 (son números, no textos)."
assert pred_d is (('2026-10-5', 0) < ('2026-10-15', 0)), \\
    "pred_d: sin cero, se comparan los caracteres '5' y '1'; los textos no se comparan como números."
assert pred_e is ('100' < '25'), \\
    "pred_e: son textos, se compara carácter por carácter: '1' contra '2'."
assert pred_f is ((7, 3) < (7, 3, 0)), \\
    "pred_f: todo lo comparado empata; la tupla más corta es la menor."
assert pred_min == min(lista_prueba), \\
    "pred_min: min compara la tupla completa, empezando por el índice 0 (la fecha), no por el monto."
''',
        pistas=[
            "En cada tupla, mira SOLO el índice 0. Si son distintos, ahí se decide y el resto no importa. Si empatan, pasa al índice 1.",
            "Para los textos, compara carácter por carácter desde la izquierda: '100' vs '25' se decide en el primer carácter. Para min(lista_prueba), busca la fecha (índice 0) más antigua y, si hay empate de fecha, mira el monto.",
        ],
        solucion='''
pred_a = False   # empatan en la fecha; 10 < 9 es False
pred_b = False   # 'b' < 'a' es False: decide el índice 0
pred_c = True    # empatan en 1; 500 < 1000
pred_d = False   # '5' < '1' es False: comparación de caracteres
pred_e = True    # '1' < '2'
pred_f = True    # todo empata: la más corta es menor
pred_min = ("2026-04-20", 40.0)   # fecha más antigua; en el empate de fecha decide el monto (40.0 < 90.0)
''',
        errores="""Leer los textos como números: '100' < '25' es True porque se compara '1' con '2'.
Mirar el monto cuando la fecha ya decidió: el índice 1 solo entra si el índice 0 empata.
Creer que min(lista_prueba) devuelve el menor monto: devuelve la fecha más antigua (y, si empatan, el menor monto de esas).""",
    ))

    # ---- 3.2 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="3.2", titulo="Mayor ingreso y mayor egreso con `key`", nivel="🟡 Intermedio",
        enunciado="""
Con los movimientos de abril `(fecha, concepto, monto)`, obtén el **movimiento completo** de mayor ingreso y el de mayor egreso (el monto más negativo) usando `max` y `min` con `key`.

**Variables a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `mayor_ingreso` | `tuple` | movimiento con el monto más alto |
| `mayor_egreso` | `tuple` | movimiento con el monto más bajo (más negativo) |
""",
        datos='''
movimientos = [
    ("2026-04-01", "mercado", -45.20),
    ("2026-04-03", "yape", 230.00),
    ("2026-04-06", "sueldo", 1800.00),
    ("2026-04-08", "alquiler", -650.00),
    ("2026-04-10", "transporte", -58.00),
    ("2026-04-13", "luz", -96.40),
    ("2026-04-17", "yape", 415.50),
    ("2026-04-19", "internet", -79.90),
    ("2026-04-22", "ajuste", 0.00),
    ("2026-04-25", "mercado", -188.75),
]
_movimientos_originales = list(movimientos)   # copia para la validación (no la toques)
''',
        plantilla='''
mayor_ingreso = None   # tuple (fecha, concepto, monto)
mayor_egreso = None    # tuple (fecha, concepto, monto)

# Tu código aquí
''',
        validacion='''
assert isinstance(mayor_ingreso, tuple) and isinstance(mayor_egreso, tuple), \\
    "Ambos resultados deben ser tuplas completas (fecha, concepto, monto), no solo el monto."
assert mayor_ingreso == ("2026-04-06", "sueldo", 1800.0), \\
    "mayor_ingreso incorrecto: ¿estás comparando por la fecha en vez del monto? (max sin key devuelve la fecha más reciente)"
assert mayor_egreso == ("2026-04-08", "alquiler", -650.0), \\
    "mayor_egreso incorrecto: ¿usaste min(movimientos) sin key? Eso devuelve la fecha más antigua, no el monto más bajo."
assert movimientos == _movimientos_originales, "Cuidado: modificaste la lista original `movimientos`."
''',
        pistas=[
            "Tanto max como min aceptan key=...: una función que recibe un movimiento y devuelve LO QUE SE COMPARA. Aquí, el monto.",
            "mayor_ingreso = max(movimientos, key=lambda m: m[2]) y mayor_egreso = min(movimientos, key=lambda m: m[2]). El mayor egreso es el monto MÁS NEGATIVO, o sea el mínimo.",
        ],
        solucion='''
mayor_ingreso = max(movimientos, key=lambda m: m[2])   # compara por el monto (índice 2)
mayor_egreso = min(movimientos, key=lambda m: m[2])    # el egreso más grande es el monto más negativo
''',
        errores="""min(movimientos) / max(movimientos) sin key comparan por la fecha (índice 0): devuelven el más antiguo / el más reciente.
Usar max para el egreso: el monto más grande en valor absoluto es el MÁS BAJO, o sea el mínimo.
Devolver solo el monto (m[2]) en vez del movimiento completo.""",
    ))

    # ---- 3.3 (bug) ---------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="3.3", titulo="Top 3 de egresos", nivel="🟡 Intermedio", es_bug=True,
        enunciado="""
De los movimientos de mayo `(fecha, concepto, monto)`, se quiere el **top 3 de egresos**: los tres egresos más grandes (montos más negativos), **ordenados del mayor al menor egreso**, como lista de tuplas completas.

El código siguiente **corre sin errores pero da un resultado incorrecto**. Encuentra el error y arréglalo.

**Variable a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `top3_egresos` | `list` de `tuple` | los 3 egresos más grandes, del más negativo al menos negativo |
""",
        datos='''
movimientos = [
    ("2026-05-02", "mercado", -73.60),
    ("2026-05-03", "yape", 180.00),
    ("2026-05-05", "alquiler", -520.00),
    ("2026-05-07", "luz", -88.15),
    ("2026-05-09", "sueldo", 1400.00),
    ("2026-05-11", "internet", -79.90),
    ("2026-05-14", "transporte", -32.40),
    ("2026-05-18", "proveedor", -245.30),
    ("2026-05-21", "mercado", -110.25),
]
_movimientos_originales = list(movimientos)   # copia para la validación (no la toques)
''',
        plantilla='''
# 🐛 Este código tiene un error típico. Arréglalo (puedes reescribirlo).
egresos = []
for movimiento in movimientos:
    if movimiento[2] < 0:
        egresos.append(movimiento)

top3_egresos = sorted(egresos)[:3]
''',
        validacion='''
assert isinstance(top3_egresos, list) and len(top3_egresos) == 3, "top3_egresos debe ser una lista de 3 movimientos."
assert all(m[2] < 0 for m in top3_egresos), "¿Incluiste ingresos? Solo cuentan los montos negativos."
assert top3_egresos[0] == ("2026-05-05", "alquiler", -520.0), \\
    "El primero debe ser el egreso más grande (alquiler). ¿Estás ordenando por la fecha en vez del monto? sorted sin key compara la tupla completa."
assert top3_egresos == [("2026-05-05", "alquiler", -520.0),
                        ("2026-05-18", "proveedor", -245.3),
                        ("2026-05-21", "mercado", -110.25)], \\
    "El top 3 no coincide: ordena por el monto. Con negativos, el mayor egreso es el número MÁS BAJO (cuidado con reverse=True)."
assert movimientos == _movimientos_originales, "Cuidado: modificaste la lista original `movimientos`."
''',
        pistas=[
            "sorted(egresos) sin key compara tuplas completas: ¿por qué campo ordena primero? Mira el índice 0 de cada movimiento.",
            "Dile a sorted qué comparar: key=lambda m: m[2]. Como los egresos son negativos, el orden ascendente ya deja primero el más negativo (no uses reverse=True). Luego corta con [:3].",
        ],
        solucion='''
egresos = []
for movimiento in movimientos:
    if movimiento[2] < 0:
        egresos.append(movimiento)

top3_egresos = sorted(egresos, key=lambda m: m[2])[:3]   # por monto, ascendente: el más negativo primero
''',
        errores="""sorted(lista_de_tuplas) sin key ordena por la fecha: el «top 3» resulta ser los tres egresos más antiguos.
Con montos negativos, reverse=True deja PRIMERO el egreso más pequeño; el orden ascendente es el correcto.
Olvidar filtrar los ingresos mete montos positivos al ranking.""",
    ))

    # ---- 3.4 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="3.4", titulo="Ranking de días con desempate", nivel="🔴 Integrador",
        enunciado="""
Un minimarket registró en tres listas paralelas las ventas y los clientes de una semana. Con `zip` y `enumerate(..., start=1)` arma un **ranking de días**:

- Ordena de **mayor a menor venta**.
- Si dos días empatan en venta, va primero el que tuvo **menos clientes**.
- Cada elemento del ranking es la tupla `(numero_dia, fecha, venta, clientes)`, donde `numero_dia` es la posición del día en la semana (el primero es 1).

**Variables a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `ranking` | `list` de `tuple` | los 7 días ordenados como se indica |
| `dia_ganador` | `int` | número de día (1 a 7) del primer lugar |
| `fecha_ganadora` | `str` | fecha del primer lugar |
""",
        datos='''
fechas = ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09", "2026-10-10", "2026-10-11"]
ventas = [412.50, 388.00, 455.20, 455.20, 301.75, 520.60, 520.60]
clientes = [96, 90, 101, 88, 70, 115, 104]
_originales = (list(fechas), list(ventas), list(clientes))   # copias para la validación (no las toques)
''',
        plantilla='''
ranking = None          # list de tuplas (numero_dia, fecha, venta, clientes)
dia_ganador = None      # int
fecha_ganadora = None   # str

# Tu código aquí
''',
        validacion='''
esperado = [
    (7, "2026-10-11", 520.6, 104),
    (6, "2026-10-10", 520.6, 115),
    (4, "2026-10-08", 455.2, 88),
    (3, "2026-10-07", 455.2, 101),
    (1, "2026-10-05", 412.5, 96),
    (2, "2026-10-06", 388.0, 90),
    (5, "2026-10-09", 301.75, 70),
]
assert isinstance(ranking, list) and len(ranking) == 7, \\
    "ranking debe ser una lista de 7 tuplas: ¿zip se cortó por listas de distinto largo?"
assert all(isinstance(r, tuple) and len(r) == 4 for r in ranking), \\
    "Cada elemento debe ser (numero_dia, fecha, venta, clientes)."
assert sorted(r[0] for r in ranking) == [1, 2, 3, 4, 5, 6, 7], \\
    "Los números de día deben ir del 1 al 7: ¿usaste enumerate(..., start=1)?"
assert ranking[0][2] == 520.6 and ranking[-1][2] == 301.75, \\
    "El ranking debe ir de MAYOR a MENOR venta: ¿ordenaste al revés?"
assert ranking == esperado, \\
    "El ranking no coincide: en empate de venta va primero el de MENOS clientes. Prueba key=lambda r: (-r[2], r[3])."
assert dia_ganador == 7, \\
    "dia_ganador debe ser 7: hay un empate en la venta más alta y gana el día con menos clientes."
assert fecha_ganadora == "2026-10-11", "fecha_ganadora debe salir del primer lugar del ranking."
assert (fechas, ventas, clientes) == _originales, "Cuidado: modificaste alguna de las listas originales."
''',
        pistas=[
            "Primero une las tres listas en una sola lista de tuplas, agregando el número de día: for numero, (fecha, venta, cli) in enumerate(zip(fechas, ventas, clientes), start=1). Después ordena esa lista.",
            "Ordena con sorted(registros, key=lambda r: (-r[2], r[3])): el signo menos invierte el orden de la venta y r[3] desempata por clientes. El ganador es ranking[0].",
        ],
        solucion='''
registros = []
for numero, (fecha, venta, cantidad_clientes) in enumerate(zip(fechas, ventas, clientes), start=1):
    registros.append((numero, fecha, venta, cantidad_clientes))

# venta descendente (-r[2]); si empatan, menos clientes primero (r[3])
ranking = sorted(registros, key=lambda r: (-r[2], r[3]))

dia_ganador = ranking[0][0]
fecha_ganadora = ranking[0][1]
''',
        errores="""Ordenar solo por venta con reverse=True no desempata: los empates quedan en el orden original (gana el día 6 en vez del 7).
Poner el signo menos en el desempate equivocado: -r[3] daría prioridad a MÁS clientes.
Usar enumerate sin start=1: el día ganador saldría 6 en vez de 7.""",
    ))

    libro.volcar_soluciones("## 🔒 Soluciones del módulo 3\nAbre cada celda **solo después de intentarlo**.")
