"""Reto final integrador (40 min): una versión libre y otra en un solo `for`."""

from constructor import Ejercicio

DATOS = '''
saldo_inicial = 300.0
movimientos = [
    ("2026-10-01", "ventas", 180.50),
    ("2026-10-02", "proveedor", -220.30),
    ("2026-10-03", "luz", -85.60),
    ("2026-10-04", "proveedor", -350.00),
    ("2026-10-05", "ajuste", 0.00),
    ("2026-10-06", "ventas", 240.00),
    ("2026-10-07", "transporte", -32.50),
    ("2026-10-08", "alquiler", -350.00),
    ("2026-10-09", "yape", 95.75),
    ("2026-10-10", "ventas", 210.40),
    ("2026-10-11", "ventas", 150.25),
    ("2026-10-12", "internet", -69.90),
    ("2026-10-13", "proveedor", -60.20),
    ("2026-10-14", "yape", 120.00),
    ("2026-10-15", "agua", -28.60),
    ("2026-10-16", "proveedor", -41.15),
]
_movimientos_originales = list(movimientos)   # copia para la validación (no la toques)
'''

VARIABLES = '''
saldo_final = None            # float (2 decimales)
n_ingresos = None             # int: movimientos con monto > 0
n_egresos = None              # int: movimientos con monto < 0
gasto_por_concepto = None     # dict: concepto → gasto (positivo, 2 decimales), solo egresos
mayor_egreso = None           # tuple completa (fecha, concepto, monto); en empate, el primero
dias_sobregiro = None         # int: movimientos tras los cuales el saldo quedó < 0
veces_en_sobregiro = None     # int: cuántas veces el saldo pasó de >= 0 a < 0
primer_dia_sobregiro = None   # str o None
concepto_mas_gasto = None     # str: concepto con mayor gasto total
'''

VALIDACION = '''
import math

esperado_gasto = {"proveedor": 671.65, "luz": 85.60, "transporte": 32.50, "alquiler": 350.00,
                  "internet": 69.90, "agua": 28.60}

assert saldo_final == 58.65, \\
    "saldo_final debe ser 58.65: ¿el saldo arranca en saldo_inicial? ¿lo redondeaste a 2 decimales?"
assert n_ingresos == 6, "n_ingresos: cuenta solo los montos > 0 (el ajuste de 0 no es un ingreso)."
assert n_egresos == 9, "n_egresos: cuenta solo los montos < 0 (el ajuste de 0 no es un egreso)."
assert isinstance(gasto_por_concepto, dict), "gasto_por_concepto debe ser un dict."
assert "ajuste" not in gasto_por_concepto and "ventas" not in gasto_por_concepto and "yape" not in gasto_por_concepto, \\
    "gasto_por_concepto solo lleva egresos: ¿entró un ingreso o el ajuste de 0?"
assert set(gasto_por_concepto) == set(esperado_gasto), \\
    "Los conceptos no coinciden: revisa que estén todos los egresos, incluidos los de un solo movimiento."
for concepto, gasto in esperado_gasto.items():
    assert math.isclose(gasto_por_concepto[concepto], gasto, abs_tol=0.005), \\
        f"El gasto de '{concepto}' no coincide: egresos en positivo, todos los movimientos del concepto."
assert all(round(v, 2) == v for v in gasto_por_concepto.values()), "¿Redondeaste el gasto a 2 decimales?"
assert mayor_egreso is not None and mayor_egreso != ("2026-10-01", "ventas", 180.5), \\
    "¿Estás comparando por la fecha en vez del monto? min(movimientos) sin key devuelve el más antiguo."
assert mayor_egreso == ("2026-10-04", "proveedor", -350.0), \\
    "mayor_egreso: hay un empate en -350; con `<` gana el primero (2026-10-04), con `<=` el último."
assert dias_sobregiro == 5, \\
    "dias_sobregiro debe ser 5: ¿un `continue` en el monto 0 te saltó un día que sí estaba en sobregiro?"
assert veces_en_sobregiro == 2, \\
    "veces_en_sobregiro debe ser 2: cuenta cruces de >= 0 a < 0, no días (necesitas el saldo anterior)."
assert primer_dia_sobregiro == "2026-10-04", "primer_dia_sobregiro incorrecto: el primer día con saldo < 0."
assert concepto_mas_gasto == "proveedor", \\
    "concepto_mas_gasto: compara el gasto TOTAL por concepto, no el egreso más grande de un solo movimiento."
assert movimientos == _movimientos_originales, "Cuidado: modificaste la lista original `movimientos`."
'''

SOLUCION_LIBRE = '''
# --- saldo, conteos y sobregiro (varios recorridos, cada uno con un propósito) ---
saldo = saldo_inicial
for fecha, concepto, monto in movimientos:
    saldo += monto
saldo_final = round(saldo, 2)

n_ingresos = 0
n_egresos = 0
for fecha, concepto, monto in movimientos:
    if monto > 0:
        n_ingresos += 1
    elif monto < 0:
        n_egresos += 1

# --- gasto por concepto: solo egresos, en positivo ---
gasto_por_concepto = {}
for fecha, concepto, monto in movimientos:
    if monto < 0:                                   # excluye ingresos y el ajuste de 0
        gasto_por_concepto[concepto] = gasto_por_concepto.get(concepto, 0) - monto
for concepto in gasto_por_concepto:
    gasto_por_concepto[concepto] = round(gasto_por_concepto[concepto], 2)

# --- mayor egreso: registro completo, `<` conserva el primero en el empate ---
mayor_egreso = None
for movimiento in movimientos:
    if movimiento[2] < 0 and (mayor_egreso is None or movimiento[2] < mayor_egreso[2]):
        mayor_egreso = movimiento

# --- sobregiro: estado, eventos y primer día ---
saldo = saldo_inicial
saldo_anterior = saldo
dias_sobregiro = 0
veces_en_sobregiro = 0
primer_dia_sobregiro = None
for fecha, concepto, monto in movimientos:
    saldo += monto
    if saldo < 0:
        dias_sobregiro += 1                         # estar en sobregiro (incluye el monto 0)
        if saldo_anterior >= 0:
            veces_en_sobregiro += 1                 # entrar en sobregiro
        if primer_dia_sobregiro is None:
            primer_dia_sobregiro = fecha
    saldo_anterior = saldo

# --- concepto con más gasto, buscado a mano ---
concepto_mas_gasto = None
mayor_gasto = None
for concepto, gasto in gasto_por_concepto.items():
    if mayor_gasto is None or gasto > mayor_gasto:
        mayor_gasto = gasto
        concepto_mas_gasto = concepto
'''

SOLUCION_UN_FOR = '''
saldo = saldo_inicial
saldo_anterior = saldo
n_ingresos = 0
n_egresos = 0
gasto_por_concepto = {}
mayor_egreso = None
dias_sobregiro = 0
veces_en_sobregiro = 0
primer_dia_sobregiro = None

for movimiento in movimientos:                       # UN solo recorrido, varios acumuladores
    fecha, concepto, monto = movimiento
    saldo += monto

    if monto > 0:
        n_ingresos += 1
    elif monto < 0:
        n_egresos += 1
        gasto_por_concepto[concepto] = gasto_por_concepto.get(concepto, 0) - monto
        if mayor_egreso is None or monto < mayor_egreso[2]:
            mayor_egreso = movimiento

    if saldo < 0:
        dias_sobregiro += 1
        if saldo_anterior >= 0:
            veces_en_sobregiro += 1
        if primer_dia_sobregiro is None:
            primer_dia_sobregiro = fecha
    saldo_anterior = saldo                            # al final de la vuelta

# Al entregar: redondeos y el extremo por concepto (sobre el diccionario ya armado)
saldo_final = round(saldo, 2)
concepto_mas_gasto = None
mayor_gasto = None
for concepto, gasto in gasto_por_concepto.items():
    if mayor_gasto is None or gasto > mayor_gasto:
        mayor_gasto = gasto
        concepto_mas_gasto = concepto
for concepto in gasto_por_concepto:
    gasto_por_concepto[concepto] = round(gasto_por_concepto[concepto], 2)
'''


def agregar(libro):
    libro.md("""
# 🏆 Reto final integrador
⏱️ **40 min** · Un solo problema con **todas las trampas del notebook activas**.

Una bodega abre octubre con `saldo_inicial = 300.0` y 16 movimientos `(fecha, concepto, monto)`, con una fecha por movimiento y en orden cronológico. Necesitas un resumen del mes.

Fíjate desde el principio en lo que puede torcerse: un **ajuste de 0** que cae en pleno sobregiro, un **empate** en el mayor egreso, un mayor egreso que **no** es el movimiento más antiguo, conceptos con un solo movimiento y **dos entradas distintas** en sobregiro.

### Parte A — Resuélvelo como quieras
Puedes usar tantos recorridos como necesites. Deja cada resultado en su variable (nombre y tipo exactos):

| Nombre | Tipo | Contenido |
|---|---|---|
| `saldo_final` | `float` | saldo tras el último movimiento, 2 decimales |
| `n_ingresos` | `int` | cantidad de movimientos con monto > 0 |
| `n_egresos` | `int` | cantidad de movimientos con monto < 0 |
| `gasto_por_concepto` | `dict` | concepto → gasto (egresos en **positivo**, 2 decimales); solo conceptos con egresos |
| `mayor_egreso` | `tuple` | el movimiento completo del egreso más grande; **en empate gana el primero** |
| `dias_sobregiro` | `int` | movimientos tras los cuales el saldo quedó **< 0** |
| `veces_en_sobregiro` | `int` | veces que el saldo pasó de **≥ 0** a **< 0** |
| `primer_dia_sobregiro` | `str` o `None` | fecha del primer saldo < 0 (`None` si no hay) |
| `concepto_mas_gasto` | `str` | concepto con mayor gasto total (aquí no hay empate) |
""", id="reto-titulo")

    # Parte A
    libro.md("#### 🏆 Reto — Parte A: resuélvelo a tu manera", id="reto-a-enunciado")
    libro.codigo(DATOS.strip("\n") + "\n\n" + VARIABLES.strip("\n") + "\n\n# Tu código aquí",
                 id="ej-reto-a-plantilla")
    libro.codigo(VALIDACION.strip("\n") + '\n\nprint("✅ Reto Parte A superado")',
                 id="ej-reto-a-validacion")
    libro.codigo('# @title 💡 Pista 1 { display-mode: "form" }\n'
                 "print('Piensa en qué pregunta responde cada resultado: unos son totales (recorrido completo), otros son estados (saldo) y otros extremos (None + registro completo). Puedes usar un for por resultado.')",
                 id="ej-reto-a-pista-1")
    libro.codigo('# @title 💡 Pista 2 { display-mode: "form" }\n'
                 "print('Trampas: el saldo arranca en saldo_inicial; NO filtres el monto 0 al calcular el saldo (el día en sobregiro existe igual); el mayor egreso se busca con `<` y None; para contar entradas necesitas saldo_anterior, que se actualiza al final de la vuelta; redondea al entregar.')",
                 id="ej-reto-a-pista-2")

    # Parte B
    libro.md("""
### Parte B — Ahora, en un solo `for`
Resuelve **el mismo problema** con **un único recorrido** de `movimientos` que lleve todos los acumuladores a la vez (saldo, conteos, gasto por concepto, mayor egreso, sobregiro). Solo lo que dependa de un diccionario **ya armado** (redondeos, el concepto con más gasto) puede ir **después** del `for`.

Las mismas variables, nombre y tipo, y sus propios `assert`.
""", id="reto-b-enunciado")
    libro.codigo(DATOS.strip("\n") + "\n\n" + VARIABLES.strip("\n") + "\n\n# Tu código aquí (un solo for sobre movimientos)",
                 id="ej-reto-b-plantilla")
    libro.codigo(VALIDACION.strip("\n") + '\n\nprint("✅ Reto Parte B superado")',
                 id="ej-reto-b-validacion")
    libro.codigo('# @title 💡 Pista 1 { display-mode: "form" }\n'
                 "print('Declara todos los acumuladores ANTES del for (saldo, saldo_anterior, contadores, diccionario, mayor_egreso = None, primer_dia_sobregiro = None...). Dentro del for actualizas todos; después del for solo entregas.')",
                 id="ej-reto-b-pista-1")
    libro.codigo('# @title 💡 Pista 2 { display-mode: "form" }\n'
                 "print('Dentro del for: saldo += monto; if monto > 0 (ingreso) / elif monto < 0 (egreso: gasto y mayor egreso); luego if saldo < 0 (días, entradas con saldo_anterior, primer día); y al FINAL de la vuelta saldo_anterior = saldo. El concepto con más gasto se busca después, sobre el diccionario.')",
                 id="ej-reto-b-pista-2")

    libro.md("## 🔒 Soluciones del reto final\nAbre cada celda **solo después de intentarlo**.", id="reto-soluciones")
    errores_a = """Empezar el saldo en 0, filtrar el monto 0 con continue antes del chequeo de sobregiro, usar `<=` en el mayor egreso o min(movimientos) sin key.
Contar días en vez de entradas: veces_en_sobregiro necesita el saldo anterior.
Olvidar redondear gasto_por_concepto y saldo_final al entregar."""
    errores_b = """Actualizar saldo_anterior antes de usarlo (debe ser lo último de la vuelta).
Meter el monto 0 en n_ingresos / n_egresos o en el gasto: los ceros no son ingresos ni egresos.
Buscar el concepto con más gasto mientras el diccionario aún se está acumulando: hazlo cuando el gasto por concepto ya esté completo."""
    for sufijo, cod, err, titulo in (
        ("a", SOLUCION_LIBRE, errores_a, "Reto Parte A"),
        ("b", SOLUCION_UN_FOR, errores_b, "Reto Parte B (un solo for)"),
    ):
        comentarios = "\n".join(f"# {l}" for l in err.strip().splitlines())
        libro.codigo(
            f'# @title 🔒 Solución {titulo} (ábrela después de intentarlo) {{ display-mode: "form" }}\n'
            f"# Error típico:\n{comentarios}\n\n"
            + DATOS.strip("\n") + "\n\n" + cod.strip("\n"),
            id=f"ej-reto-{sufijo}-solucion",
        )
