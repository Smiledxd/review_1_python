"""Reto final (Parte A libre, Parte B en un solo `for`) y Nivel pro."""

from libro import Ejercicio

VARIABLES = """
| Variable | Qué es |
|---|---|
| `saldo_final` | saldo después del último movimiento, redondeado a 2 decimales |
| `n_ingresos` / `n_egresos` | cantidad de montos mayores que 0 / menores que 0 |
| `gasto_por_concepto` | `concepto → total gastado`, solo egresos, **en positivo**, cada total redondeado a 2 decimales |
| `mayor_egreso` | la tupla completa del movimiento con el monto más negativo; si hay empate, **el primero** |
| `dias_sobregiro` | lista de fechas en que el saldo, **después** del movimiento, quedó por debajo de 0 |
| `veces_en_sobregiro` | cuántas veces el saldo **pasó** de ≥ 0 a < 0 |
| `primer_dia_sobregiro` | la primera fecha con saldo < 0 (`None` si nunca pasa) |
| `concepto_mas_gasto` | el concepto con mayor gasto total |
"""

SOLUCION_A = '''
# Saldo final: el estado arranca en saldo_inicial
saldo = saldo_inicial
for fecha, concepto, monto in movimientos:
    saldo += monto
saldo_final = round(saldo, 2)

# Conteos: el 0 no es ingreso ni egreso
n_ingresos = 0
n_egresos = 0
for fecha, concepto, monto in movimientos:
    if monto > 0:
        n_ingresos += 1
    elif monto < 0:
        n_egresos += 1

# Gasto por concepto: solo egresos, en positivo, redondeado al entregar
gasto_por_concepto = {}
for fecha, concepto, monto in movimientos:
    if monto < 0:
        gasto_por_concepto[concepto] = gasto_por_concepto.get(concepto, 0) - monto
for concepto in gasto_por_concepto:
    gasto_por_concepto[concepto] = round(gasto_por_concepto[concepto], 2)

# Mayor egreso: key compara por el monto; en el empate min devuelve el primero
mayor_egreso = min(movimientos, key=lambda m: m[2])

# Sobregiro: todos los días, las entradas y el primero
saldo = saldo_inicial
saldo_anterior = saldo
dias_sobregiro = []
veces_en_sobregiro = 0
primer_dia_sobregiro = None
for fecha, concepto, monto in movimientos:
    saldo += monto                          # sin continue: el ajuste de 0 también se revisa
    if saldo < 0:
        dias_sobregiro.append(fecha)
        if saldo_anterior >= 0:
            veces_en_sobregiro += 1
        if primer_dia_sobregiro is None:
            primer_dia_sobregiro = fecha
    saldo_anterior = saldo

# Concepto con más gasto
concepto_mas_gasto = max(gasto_por_concepto, key=gasto_por_concepto.get)
'''

SOLUCION_B = '''
saldo = saldo_inicial
saldo_anterior = saldo
n_ingresos = 0
n_egresos = 0
gasto_por_concepto = {}
mayor_egreso = None
dias_sobregiro = []
veces_en_sobregiro = 0
primer_dia_sobregiro = None

for movimiento in movimientos:                    # UN solo recorrido, todos los acumuladores
    fecha, concepto, monto = movimiento
    saldo += monto

    if monto > 0:
        n_ingresos += 1
    elif monto < 0:
        n_egresos += 1
        gasto_por_concepto[concepto] = gasto_por_concepto.get(concepto, 0) - monto
        if mayor_egreso is None or monto < mayor_egreso[2]:     # `<`: en el empate gana el primero
            mayor_egreso = movimiento

    if saldo < 0:
        dias_sobregiro.append(fecha)
        if saldo_anterior >= 0:
            veces_en_sobregiro += 1
        if primer_dia_sobregiro is None:
            primer_dia_sobregiro = fecha
    saldo_anterior = saldo                         # al final de la vuelta

# Al entregar: lo que depende del diccionario ya completo
saldo_final = round(saldo, 2)
concepto_mas_gasto = None
for concepto, gasto in gasto_por_concepto.items():
    if concepto_mas_gasto is None or gasto > gasto_por_concepto[concepto_mas_gasto]:
        concepto_mas_gasto = concepto
for concepto in gasto_por_concepto:
    gasto_por_concepto[concepto] = round(gasto_por_concepto[concepto], 2)
'''


def agregar(nb):
    nb.md(f"""
---
## 🏋️ Reto final: el extracto de octubre
⏱️ 40 minutos

`movimientos` es una lista de tuplas `(fecha, concepto, monto)`, una por día y en orden: los montos positivos son ingresos y los negativos, egresos. `saldo_inicial` es el saldo antes del primer movimiento. Hay un movimiento con monto 0 (un ajuste): no es ingreso ni egreso.

⚠️ Todas las trampas del notebook están activas: el ajuste de 0 cae en un día en sobregiro, hay **un empate** en el mayor egreso, el movimiento más antiguo **no** es el mayor egreso, hay conceptos con un solo egreso y la cuenta **entra dos veces** en sobregiro.

Crea (no modifiques `movimientos`):
{VARIABLES}
""", id="reto-titulo")
    nb.ejercicio(Ejercicio(
        clave="reto-a", titulo="Reto · Parte A: resuélvelo a tu manera", check='check_reto("A")', nivel="####",
        enunciado="Usa tantos recorridos como necesites: lo importante es que cada resultado sea correcto.",
        pistas=[
            "Piensa qué tipo de pregunta es cada resultado: un **total** (recorrido completo), un **estado** (el saldo, que arranca en `saldo_inicial`), "
            "un **evento** (primero, todos, entradas con `saldo_anterior`) o un **extremo** (`None` o `key`).",
            "Trampas: no filtres el monto 0 al calcular el saldo ni pongas un `continue` antes del chequeo de sobregiro; para el mayor egreso usa `key` o `<` "
            "(no `<=`); `saldo_anterior = saldo` va al final de la vuelta; redondea al entregar.",
        ],
        solucion=SOLUCION_A,
        errores="empezar el saldo en 0, saltar el monto 0 con `continue` antes del chequeo, usar `<=` o `min(movimientos)` sin `key`, "
                "y contar días en sobregiro como si fueran entradas.",
    ))
    nb.md("""
#### Parte B · Ahora, en un solo `for`
Rehaz **el mismo reto** con **un único recorrido** de `movimientos` que lleve todos los acumuladores a la vez. Solo lo que depende del diccionario **ya completo** (redondear el gasto y buscar el concepto con más gasto) puede ir después del `for`. Mismas variables, mismo verificador.
""", id="reto-b-intro")
    nb.ejercicio(Ejercicio(
        clave="reto-b", titulo="Reto · Parte B: un solo recorrido", check='check_reto("B")', nivel="####",
        enunciado="Declara todos los acumuladores **antes** del `for`, actualízalos dentro y entrega después.",
        pistas=[
            "Antes del `for`: `saldo`, `saldo_anterior`, los dos contadores, el diccionario, `mayor_egreso = None`, la lista, el contador de entradas y `primer_dia_sobregiro = None`.",
            "Dentro: `saldo += monto`; `if monto > 0` / `elif monto < 0` (ahí el gasto y el mayor egreso); luego `if saldo < 0` (días, entradas, primer día); "
            "y en la **última** línea, `saldo_anterior = saldo`.",
        ],
        solucion=SOLUCION_B,
        errores="actualizar `saldo_anterior` antes de usarlo, o buscar el concepto con más gasto mientras el diccionario todavía se está llenando.",
    ))

    nb.md("""
---
## 🚀 Nivel pro (opcional)
Con los datos del reto:
1. `saldo_por_fecha`: diccionario `fecha → saldo después de ese movimiento`, redondeado a 2 decimales. Arma primero una lista de fechas y otra de saldos, y construye el diccionario en **una línea** con `dict(zip(...))`.
2. `ranking_conceptos`: lista de tuplas `(concepto, gasto)` ordenada de **mayor a menor gasto** y, si empatan, por nombre en orden alfabético. Parte de un diccionario de gasto por concepto y usa `sorted(....items(), key=...)`.
3. `racha_mas_larga`: la mayor cantidad de movimientos **seguidos** con el saldo en rojo. Pista: un contador que sube en rojo y vuelve a 0 al salir, y otro que guarda el mejor.
""", id="pro-titulo")
    nb.ejercicio(Ejercicio(
        clave="pro", titulo="Nivel pro", check="check_pro()", nivel="####",
        enunciado="Estos tres ejercicios no tienen pistas: combinan lo que ya practicaste.",
        solucion='''
# 1. dict(zip(...)) en una línea, a partir de dos listas paralelas
fechas = []
saldos = []
saldo = saldo_inicial
for fecha, concepto, monto in movimientos:
    saldo += monto
    fechas.append(fecha)
    saldos.append(round(saldo, 2))
saldo_por_fecha = dict(zip(fechas, saldos))

# 2. Ranking: gasto descendente y, en el empate, nombre ascendente
gasto = {}
for fecha, concepto, monto in movimientos:
    if monto < 0:
        gasto[concepto] = gasto.get(concepto, 0) - monto
for concepto in gasto:
    gasto[concepto] = round(gasto[concepto], 2)
ranking_conceptos = sorted(gasto.items(), key=lambda kv: (-kv[1], kv[0]))

# 3. Racha: un contador que se reinicia y otro que guarda el mejor
racha = 0
racha_mas_larga = 0
for s in saldos:
    if s < 0:
        racha += 1
        if racha > racha_mas_larga:
            racha_mas_larga = racha
    else:
        racha = 0
''',
        errores="en la racha, contar todos los días en rojo sin reiniciar el contador al salir del rojo.",
    ))
