"""Módulo 1 — Diccionarios: agrupación y acumulación (50 min)."""

from constructor import Ejercicio


def agregar(libro):
    libro.md("""
# Módulo 1 — Diccionarios: agrupación y acumulación
⏱️ **50 min** · Objetivo: agrupar datos por categoría (total, conteo y más) con un solo recorrido, sin `KeyError` y entregando resultados redondeados.
""", id="m1-titulo")

    # ------------------------------------------------------------------
    # Concepto 1: ciclo de vida de una clave
    # ------------------------------------------------------------------
    libro.md("## 1. Ciclo de vida de una clave")
    libro.prediccion(
        ["línea 1 (print del arroz)", "línea 2 (print de \"leche\" in ...)", "línea 3 (¿qué se imprime al leer leche?)"],
        '''
inventario = {"arroz": 12, "azúcar": 8}

print(inventario["arroz"])              # línea 1
print("leche" in inventario)            # línea 2
try:
    print(inventario["leche"])          # línea 3
except KeyError as error:
    print("KeyError con la clave:", error)
''')
    libro.md("""
**Teoría corta**

- Una clave **nace cuando le asignas un valor**: `d["leche"] = 5`.
- `d[clave]` solo **lee**. Si la clave no existe, Python lanza `KeyError` (y tu programa se detiene).
- `clave in d` pregunta **sin riesgo** si la clave ya existe y devuelve `True` o `False`.

Por eso, antes de leer una clave que quizá no exista, pregunta con `if clave in d`.
""")
    libro.ejemplo('''
inventario = {"arroz": 12, "azúcar": 8}

for producto in ["arroz", "leche"]:
    if producto in inventario:
        print(f"{producto}: hay {inventario[producto]} unidades")
    else:
        print(f"{producto}: todavía no existe como clave")

inventario["leche"] = 5          # asignar CREA la clave
print(inventario)
''')

    # ------------------------------------------------------------------
    # Concepto 2: patrón categoría -> total / conteo con if/else
    # ------------------------------------------------------------------
    libro.md("## 2. Patrón clásico: categoría → total y categoría → conteo")
    libro.prediccion(
        ["el diccionario final `totales`"],
        '''
totales = {}
for categoria, monto in [("lácteos", 8.5), ("bebidas", 4.0), ("lácteos", 6.5)]:
    if categoria in totales:
        totales[categoria] += monto
    else:
        totales[categoria] = monto
print(totales)
''')
    libro.md("""
**Teoría corta**

El patrón tiene dos ramas:

- **`else` (la primera vez que aparece la clave):** se **inicializa** con el valor del elemento actual. Para un total es el `monto`; para un conteo es `1`.
- **`if` (las vueltas siguientes):** se **acumula** sobre lo que ya hay.

⚠️ Si en el `else` pones `= 0` para un total, **pierdes el primer monto de cada categoría**: el `0` reemplaza al valor de esa vuelta.

Mira la traza paso a paso (vuelta | elemento | estado | evento):
""")
    libro.ejemplo('''
ventas_demo = [
    ("2026-03-02", "lácteos", 8.50),
    ("2026-03-02", "abarrotes", 23.00),
    ("2026-03-03", "lácteos", 6.50),
    ("2026-03-03", "bebidas", 4.00),
    ("2026-03-04", "abarrotes", 15.00),
    ("2026-03-04", "lácteos", 9.00),
]

totales = {}
conteos = {}
vuelta = 0
print(f"{'vuelta':<7}| {'elemento':<36}| {'totales':<56}| evento")
for fecha, categoria, monto in ventas_demo:
    vuelta += 1
    if categoria in totales:
        totales[categoria] += monto
        conteos[categoria] += 1
        evento = f"'{categoria}' ya existía → se acumula"
    else:
        totales[categoria] = monto
        conteos[categoria] = 1
        evento = f"'{categoria}' es nueva → se inicializa"
    print(f"{vuelta:<7}| {str((fecha, categoria, monto)):<36}| {str(totales):<56}| {evento}")

print("\\nconteos:", conteos)
''')

    # ------------------------------------------------------------------
    # Concepto 3: .get
    # ------------------------------------------------------------------
    libro.md("## 3. `d.get(clave, 0)`: leer y acumular sin `if`")
    libro.prediccion(
        ["línea 1", "línea 2", "línea 3", "línea 4 (¿qué pasa al sumar 50 a lo que devuelve .get sin valor por defecto?)"],
        '''
ventas_por_dia = {"lunes": 120.0}

print(ventas_por_dia.get("lunes", 0))       # línea 1
print(ventas_por_dia.get("martes", 0))      # línea 2
print(ventas_por_dia.get("martes"))         # línea 3
try:
    print(ventas_por_dia.get("martes") + 50)    # línea 4
except TypeError as error:
    print("TypeError:", error)
''')
    libro.md("""
**Teoría corta**

- `d.get(clave, valor_por_defecto)` devuelve `d[clave]` si existe y, si no, el valor por defecto. **Nunca** lanza `KeyError`.
- Sin valor por defecto devuelve `None`, y `None + 50` da `TypeError`. Por eso, **al acumular, siempre pasa el valor por defecto** (`0` para totales y conteos).
- Acumular queda en una sola línea, sin `if/else`:

```python
totales[categoria] = totales.get(categoria, 0) + monto
```

- Con `.get` puedes llevar **varios acumuladores en un solo recorrido**: uno por diccionario (o por variable).
""")
    libro.ejemplo('''
ventas_demo = [
    ("2026-03-02", "lácteos", 8.50),
    ("2026-03-02", "abarrotes", 23.00),
    ("2026-03-03", "lácteos", 6.50),
    ("2026-03-03", "bebidas", 4.00),
    ("2026-03-04", "abarrotes", 15.00),
    ("2026-03-04", "lácteos", 9.00),
]

totales = {}
conteos = {}
vuelta = 0
print(f"{'vuelta':<7}| {'elemento':<36}| {'totales':<56}| conteos")
for fecha, categoria, monto in ventas_demo:
    vuelta += 1
    totales[categoria] = totales.get(categoria, 0) + monto   # total
    conteos[categoria] = conteos.get(categoria, 0) + 1       # conteo
    print(f"{vuelta:<7}| {str((fecha, categoria, monto)):<36}| {str(totales):<56}| {conteos}")
''')

    # ------------------------------------------------------------------
    # Concepto 4: recorridos
    # ------------------------------------------------------------------
    libro.md("## 4. Recorrer un diccionario: `for k in d`, `.keys()`, `.values()`, `.items()`")
    libro.prediccion(
        ["qué imprime el primer for", "keys()", "values()", "items()", "el dict tras subir 10 %", "qué pasa al agregar una clave dentro del for"],
        '''
precios = {"arroz": 4.5, "aceite": 9.9, "azúcar": 3.8}

for producto in precios:
    print(producto)
print(list(precios.keys()))
print(list(precios.values()))
print(list(precios.items()))

for producto in precios:                      # cambiar VALORES mientras recorres
    precios[producto] = round(precios[producto] * 1.1, 2)
print(precios)

copia = dict(precios)
try:
    for producto in copia:                    # agregar una CLAVE mientras recorres
        copia["leche"] = 5.0
except RuntimeError as error:
    print("RuntimeError:", error)
''')
    libro.md("""
**Teoría corta**

| Forma | Recorres | Cada vuelta te da |
|---|---|---|
| `for k in d` / `d.keys()` | las claves | `k` |
| `d.values()` | los valores | `v` |
| `d.items()` | pares | `(k, v)` → `for k, v in d.items():` |

- **Cambiar valores** de claves existentes mientras recorres **está bien**.
- **Agregar o quitar claves** mientras recorres da `RuntimeError: dictionary changed size during iteration`. Si necesitas eso, recorre una copia (`list(d)`) o arma un diccionario nuevo.
""")
    libro.ejemplo('''
stock = {"arroz": 12, "aceite": 0, "azúcar": 7}

for producto, unidades in stock.items():
    estado = "agotado" if unidades == 0 else "disponible"
    print(f"{producto:<8} {unidades:>3}  {estado}")

print("unidades en total:", sum(stock.values()))
''')

    # ------------------------------------------------------------------
    # Concepto 5: floats
    # ------------------------------------------------------------------
    libro.md("## 5. ¿Por qué sale `477.5799999999999`? Redondea al entregar")
    libro.prediccion(
        ["línea 1", "línea 2", "línea 3 (total sin redondear)", "línea 4 (total redondeado)"],
        '''
print(0.1 + 0.2)                            # línea 1
print(0.1 + 0.2 == 0.3)                     # línea 2

compras = [12.35, 8.20, 45.90, 3.15, 27.60, 9.85]
total = 0
for compra in compras:
    total += compra
print(total)                                # línea 3
print(round(total, 2))                      # línea 4
''')
    libro.md("""
**Teoría corta**

- Python guarda los decimales en **binario**. Números como `0.1` no caben exactos, y al sumar muchos aparecen restos diminutos (`107.04999999999998`).
- **No es un error tuyo** ni de Python: es cómo funcionan los `float`.
- Regla: **acumula sin redondear y redondea al entregar** el resultado, con `round(x, 2)`. Redondear en cada paso no arregla nada y ensucia el cálculo.
- Recorrer un diccionario para redondear sus valores **al final** es válido (cambiar valores está permitido):

```python
for categoria in totales:
    totales[categoria] = round(totales[categoria], 2)
```

- Para **comparar** decimales no uses `==`: usa `round(x, 2) == y` o `math.isclose(x, y)`.
""")
    libro.ejemplo('''
import math

totales = {"lácteos": 0, "snacks": 0}
datos = [("lácteos", 12.80), ("snacks", 2.20), ("lácteos", 9.60), ("snacks", 1.10),
         ("lácteos", 15.45), ("snacks", 3.50)]

for categoria, monto in datos:
    totales[categoria] = totales.get(categoria, 0) + monto
print("crudo:     ", totales)

for categoria in totales:                       # al entregar: redondea
    totales[categoria] = round(totales[categoria], 2)
print("redondeado:", totales)

print(totales["snacks"] == 6.8, math.isclose(totales["snacks"], 6.8))
''')

    # ------------------------------------------------------------------
    # Ejercicios
    # ------------------------------------------------------------------
    libro.md("## 🏋️ Ejercicios del módulo 1\nRecuerda: define primero tu predicción mental, escribe tu código y luego ejecuta la validación.")

    # ---- 1.1 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="1.1", titulo="Conteo por categoría", nivel="🟢 Básico",
        enunciado="""
Una bodega registró sus ventas de tres días como `(fecha, categoria, monto)`. Cuenta **cuántas ventas hubo por categoría** con el patrón `if / else`.

**Variable a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `conteo_por_categoria` | `dict` | categoría (`str`) → cantidad de ventas (`int`) |
""",
        datos='''
ventas = [
    ("2026-05-04", "abarrotes", 23.40),
    ("2026-05-04", "bebidas", 7.50),
    ("2026-05-04", "lácteos", 12.80),
    ("2026-05-05", "abarrotes", 41.10),
    ("2026-05-05", "snacks", 3.50),
    ("2026-05-05", "bebidas", 5.00),
    ("2026-05-06", "abarrotes", 18.90),
    ("2026-05-06", "lácteos", 9.60),
    ("2026-05-06", "bebidas", 7.50),
    ("2026-05-06", "limpieza", 14.20),
]
_ventas_originales = list(ventas)   # copia para la validación (no la toques)
''',
        plantilla='''
conteo_por_categoria = None   # dict: categoría → cantidad de ventas

# Tu código aquí
''',
        validacion='''
assert isinstance(conteo_por_categoria, dict), "conteo_por_categoria debe ser un dict: ¿lo creaste con {}?"
assert set(conteo_por_categoria) == {"abarrotes", "bebidas", "lácteos", "snacks", "limpieza"}, \\
    "Las categorías no coinciden: ¿falta alguna? La primera vez que aparece una clave hay que crearla."
assert sum(conteo_por_categoria.values()) == len(ventas), \\
    "Cada venta debe contarse una sola vez: ¿inicializaste en 0 en el else y perdiste la primera venta de cada categoría?"
assert conteo_por_categoria == {"abarrotes": 3, "bebidas": 3, "lácteos": 2, "snacks": 1, "limpieza": 1}, \\
    "Los conteos no coinciden: ¿estás sumando el monto en vez de sumar 1?"
assert ventas == _ventas_originales, "Cuidado: modificaste la lista original `ventas`."
''',
        pistas=[
            "Necesitas un diccionario vacío y, por cada venta, decidir: ¿la categoría ya está en el diccionario? Si ya está, suma 1; si no, créala.",
            "Estructura: conteo_por_categoria = {} y luego for fecha, categoria, monto in ventas: if categoria in conteo_por_categoria: (suma 1) else: (empieza en 1).",
        ],
        solucion='''
conteo_por_categoria = {}
for fecha, categoria, monto in ventas:
    if categoria in conteo_por_categoria:
        conteo_por_categoria[categoria] += 1      # vueltas siguientes: acumular
    else:
        conteo_por_categoria[categoria] = 1       # primera vez: inicializar en 1
''',
        errores="""Inicializar el conteo en 0 dentro del else: la primera venta de cada categoría no se cuenta.
Leer conteo_por_categoria[categoria] antes de crearla provoca KeyError.
Sumar el monto en lugar de 1 convierte el conteo en un total.""",
    ))

    # ---- 1.2 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="1.2", titulo="Total por categoría con `.get`", nivel="🟢 Básico",
        enunciado="""
Con las ventas de la semana `(fecha, categoria, monto)`, calcula el **total vendido por categoría** usando `.get(categoria, 0)` (sin `if / else`) y **entrega los totales redondeados a 2 decimales**.

**Variable a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `total_por_categoria` | `dict` | categoría (`str`) → total (`float`, redondeado a 2 decimales) |
""",
        datos='''
ventas_semana = [
    ("2026-05-11", "abarrotes", 24.90),
    ("2026-05-11", "lácteos", 12.80),
    ("2026-05-11", "snacks", 2.20),
    ("2026-05-12", "bebidas", 7.50),
    ("2026-05-12", "abarrotes", 18.35),
    ("2026-05-12", "lácteos", 9.60),
    ("2026-05-13", "limpieza", 14.20),
    ("2026-05-13", "abarrotes", 7.10),
    ("2026-05-13", "snacks", 1.10),
    ("2026-05-14", "lácteos", 15.45),
    ("2026-05-14", "bebidas", 5.00),
    ("2026-05-14", "snacks", 3.50),
    ("2026-05-14", "limpieza", 8.90),
    ("2026-05-15", "abarrotes", 31.60),
    ("2026-05-15", "bebidas", 6.30),
]
_ventas_originales = list(ventas_semana)   # copia para la validación (no la toques)
''',
        plantilla='''
total_por_categoria = None   # dict: categoría → total (float, 2 decimales)

# Tu código aquí
''',
        validacion='''
import math

esperado = {"abarrotes": 81.95, "lácteos": 37.85, "snacks": 6.80, "bebidas": 18.80, "limpieza": 23.10}

assert isinstance(total_por_categoria, dict), "total_por_categoria debe ser un dict: ¿lo creaste con {}?"
assert set(total_por_categoria) == set(esperado), "Las categorías no coinciden: ¿falta alguna?"
for categoria, total in esperado.items():
    assert math.isclose(total_por_categoria[categoria], total, abs_tol=0.005), \\
        f"El total de '{categoria}' no coincide: ¿sumaste todos sus montos? ¿perdiste el primero al inicializar?"
assert all(round(valor, 2) == valor for valor in total_por_categoria.values()), \\
    "¿Redondeaste a 2 decimales? Hay totales como 37.849999999999994: redondea con round(x, 2) al entregar."
assert ventas_semana == _ventas_originales, "Cuidado: modificaste la lista original `ventas_semana`."
''',
        pistas=[
            "Usa un solo renglón dentro del for: total_por_categoria[categoria] = total_por_categoria.get(categoria, 0) + monto. El redondeo va aparte, cuando el for ya terminó.",
            "Después del for, recorre el diccionario: for categoria in total_por_categoria: total_por_categoria[categoria] = round(total_por_categoria[categoria], 2). Cambiar valores mientras recorres está permitido.",
        ],
        solucion='''
total_por_categoria = {}
for fecha, categoria, monto in ventas_semana:
    total_por_categoria[categoria] = total_por_categoria.get(categoria, 0) + monto

for categoria in total_por_categoria:          # al entregar: redondear a 2 decimales
    total_por_categoria[categoria] = round(total_por_categoria[categoria], 2)
''',
        errores="""Usar .get(categoria) sin el 0 devuelve None y None + monto da TypeError.
Entregar el total sin redondear (37.849999999999994): es normal en float, se redondea al final.
Recorrer las ventas otra vez para redondear: basta recorrer el diccionario ya armado.""",
    ))

    # ---- 1.3 (bug) ---------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="1.3", titulo="Egresos por concepto", nivel="🟡 Intermedio", es_bug=True,
        enunciado="""
Con los movimientos de una cuenta `(fecha, concepto, monto)`, se quiere el **gasto por concepto**: solo los **egresos** (montos negativos), **guardados en positivo** y redondeados a 2 decimales. Los ingresos y los montos `0` **no** deben aparecer.

El código de la celda siguiente **corre sin errores pero da resultados incorrectos**. Encuentra el error y arréglalo.

**Variable a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `gasto_por_concepto` | `dict` | concepto (`str`) → gasto (`float`, positivo, 2 decimales) |

> 🔎 Ojo: aquí **sí** conviene ignorar los montos 0. No por el cálculo (sumar 0 no cambia un total), sino porque un movimiento de 0 **crearía una clave** que no debería existir.
""",
        datos='''
movimientos = [
    ("2026-06-01", "sueldo", 1500.00),
    ("2026-06-02", "alquiler", -600.00),
    ("2026-06-03", "mercado", -85.40),
    ("2026-06-04", "ajuste", 0.0),
    ("2026-06-06", "yape", 120.00),
    ("2026-06-07", "mercado", -62.30),
    ("2026-06-09", "transporte", -18.50),
    ("2026-06-12", "mercado", -47.15),
    ("2026-06-14", "ajuste", 0.0),
    ("2026-06-15", "transporte", -21.00),
]
_movimientos_originales = list(movimientos)   # copia para la validación (no la toques)
''',
        plantilla='''
# 🐛 Este código tiene un error típico. Arréglalo (puedes reescribirlo).
gasto_por_concepto = {}
for fecha, concepto, monto in movimientos:
    if monto != 0:
        gasto_por_concepto[concepto] = gasto_por_concepto.get(concepto, 0) + monto
''',
        validacion='''
import math

esperado = {"alquiler": 600.00, "mercado": 194.85, "transporte": 39.50}

assert isinstance(gasto_por_concepto, dict), "gasto_por_concepto debe ser un dict."
assert "sueldo" not in gasto_por_concepto and "yape" not in gasto_por_concepto, \\
    "¿Contaste ingresos como si fueran gastos? Solo cuentan los montos negativos."
assert "ajuste" not in gasto_por_concepto, \\
    "Un concepto con solo montos 0 no debe aparecer: ¿filtras con `monto != 0` en vez de `monto < 0`?"
assert all(valor > 0 for valor in gasto_por_concepto.values()), \\
    "¿Dejaste los egresos en negativo? Guárdalos en positivo (usa -monto)."
assert set(gasto_por_concepto) == set(esperado), "Los conceptos no coinciden con los egresos reales."
for concepto, gasto in esperado.items():
    assert math.isclose(gasto_por_concepto[concepto], gasto, abs_tol=0.005), \\
        f"El gasto de '{concepto}' no coincide: revisa qué sumas en cada vuelta."
assert all(round(valor, 2) == valor for valor in gasto_por_concepto.values()), \\
    "¿Redondeaste a 2 decimales al entregar?"
assert movimientos == _movimientos_originales, "Cuidado: modificaste la lista original `movimientos`."
''',
        pistas=[
            "Hay dos fallos en el mismo if/acumulación: uno decide QUÉ movimientos entran (mira quién pasa el filtro) y otro decide QUÉ SE SUMA (mira el signo). Además falta entregar redondeado.",
            "El filtro correcto para «solo egresos» es monto < 0: excluye ingresos (positivos) y ajustes (0) a la vez. Al acumular, suma -monto para guardar el gasto en positivo. Redondea con un for sobre el diccionario al final.",
        ],
        solucion='''
gasto_por_concepto = {}
for fecha, concepto, monto in movimientos:
    if monto < 0:                                            # solo egresos (excluye ingresos y 0)
        gasto_por_concepto[concepto] = gasto_por_concepto.get(concepto, 0) - monto   # en positivo

for concepto in gasto_por_concepto:                          # entregar redondeado
    gasto_por_concepto[concepto] = round(gasto_por_concepto[concepto], 2)
''',
        errores="""`monto != 0` deja pasar los ingresos: se mezclan con los gastos y además llegan con signo positivo/negativo mezclado.
Con `monto < 0` se descartan ingresos y ceros de una vez; al sumar -monto el gasto queda positivo.
Aquí ignorar el 0 importa porque evita crear la clave 'ajuste'; al calcular un saldo, en cambio, filtrar el 0 es innecesario.""",
    ))

    # ---- 1.4 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="1.4", titulo="Tres resultados en un solo recorrido", nivel="🔴 Integrador",
        enunciado="""
Un minimarket anotó sus compras a proveedores del mes como `(fecha, categoria, monto)` (todos los montos son gastos positivos). Calcula, **recorriendo la lista `gastos` una sola vez** para los totales y los conteos:

**Variables a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `total_por_categoria` | `dict` | categoría → total gastado (`float`, 2 decimales) |
| `cantidad_por_categoria` | `dict` | categoría → número de compras (`int`) |
| `promedio_por_categoria` | `dict` | categoría → total / cantidad (`float`, **redondeado** a 2 decimales) |
| `categoria_mayor_gasto` | `str` | categoría con mayor total, **buscada a mano** recorriendo `.items()` (sin `max`) |

Pistas de método: acumula total y cantidad en el mismo `for`; redondea y calcula el promedio **al entregar**, con el diccionario ya armado.
""",
        datos='''
gastos = [
    ("2026-07-01", "abarrotes", 342.50),
    ("2026-07-01", "limpieza", 58.90),
    ("2026-07-03", "bebidas", 126.40),
    ("2026-07-04", "abarrotes", 215.75),
    ("2026-07-06", "lácteos", 89.30),
    ("2026-07-08", "limpieza", 44.10),
    ("2026-07-09", "bebidas", 98.60),
    ("2026-07-11", "abarrotes", 187.20),
    ("2026-07-12", "lácteos", 76.90),
    ("2026-07-14", "snacks", 63.15),
    ("2026-07-15", "bebidas", 110.00),
    ("2026-07-15", "limpieza", 39.95),
]
_gastos_originales = list(gastos)   # copia para la validación (no la toques)
''',
        plantilla='''
total_por_categoria = None       # dict: categoría → total (float, 2 decimales)
cantidad_por_categoria = None    # dict: categoría → cantidad de compras (int)
promedio_por_categoria = None    # dict: categoría → promedio (float, 2 decimales)
categoria_mayor_gasto = None     # str: categoría con mayor total

# Tu código aquí
''',
        validacion='''
import math

tot = {"abarrotes": 745.45, "limpieza": 142.95, "bebidas": 335.00, "lácteos": 166.20, "snacks": 63.15}
cant = {"abarrotes": 3, "limpieza": 3, "bebidas": 3, "lácteos": 2, "snacks": 1}
prom = {"abarrotes": 248.48, "limpieza": 47.65, "bebidas": 111.67, "lácteos": 83.10, "snacks": 63.15}

assert isinstance(total_por_categoria, dict) and isinstance(cantidad_por_categoria, dict) \\
    and isinstance(promedio_por_categoria, dict), "Los tres resultados deben ser diccionarios."
assert set(total_por_categoria) == set(tot), "total_por_categoria: las categorías no coinciden."
for categoria, valor in tot.items():
    assert math.isclose(total_por_categoria[categoria], valor, abs_tol=0.005), \\
        f"Total de '{categoria}' incorrecto: ¿perdiste la primera compra al inicializar?"
assert all(round(v, 2) == v for v in total_por_categoria.values()), \\
    "¿Redondeaste los totales a 2 decimales?"
assert cantidad_por_categoria == cant, "cantidad_por_categoria incorrecta: cuenta 1 por compra, no el monto."
assert set(promedio_por_categoria) == set(prom), "promedio_por_categoria: las categorías no coinciden."
for categoria, valor in prom.items():
    assert math.isclose(promedio_por_categoria[categoria], valor, abs_tol=0.005), \\
        f"Promedio de '{categoria}' incorrecto: total / cantidad, redondeado a 2 decimales."
assert all(round(v, 2) == v for v in promedio_por_categoria.values()), \\
    "¿Redondeaste los promedios a 2 decimales?"
assert categoria_mayor_gasto == "abarrotes", \\
    "categoria_mayor_gasto incorrecta: compara TOTALES por categoría, no montos individuales."
assert gastos == _gastos_originales, "Cuidado: modificaste la lista original `gastos`."
''',
        pistas=[
            "Un solo for sobre gastos con dos acumuladores: total_por_categoria[categoria] = total_por_categoria.get(categoria, 0) + monto y lo mismo para cantidad_por_categoria (sumando 1).",
            "Después del for, recorre total_por_categoria.items(): calcula el promedio, redondea el total y busca el mayor con una variable que empiece en None (mayor_total = None; if mayor_total is None or total > mayor_total: ...). Cuidado: si redondeas el total dentro de ese recorrido, cambia el valor, no la clave.",
        ],
        solucion='''
total_por_categoria = {}
cantidad_por_categoria = {}
for fecha, categoria, monto in gastos:                       # un solo recorrido, dos acumuladores
    total_por_categoria[categoria] = total_por_categoria.get(categoria, 0) + monto
    cantidad_por_categoria[categoria] = cantidad_por_categoria.get(categoria, 0) + 1

promedio_por_categoria = {}
categoria_mayor_gasto = None
mayor_total = None                                           # centinela: aún no hay mejor
for categoria, total in total_por_categoria.items():
    promedio_por_categoria[categoria] = round(total / cantidad_por_categoria[categoria], 2)
    if mayor_total is None or total > mayor_total:
        mayor_total = total
        categoria_mayor_gasto = categoria

for categoria in total_por_categoria:                        # entregar redondeado
    total_por_categoria[categoria] = round(total_por_categoria[categoria], 2)
''',
        errores="""Promediar con el total ya redondeado o redondear antes de dividir cambia el resultado: calcula total / cantidad y redondea al entregar.
Buscar el máximo comparando montos sueltos en vez de totales por categoría.
Empezar mayor_total en 0 funciona aquí (todo es positivo) pero es el hábito que falla en el módulo 2: usa None.""",
    ))

    libro.volcar_soluciones("## 🔒 Soluciones del módulo 1\nAbre cada celda **solo después de intentarlo**.")
