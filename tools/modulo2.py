"""Módulo 2 — Estado acumulativo y control de flujo (70 min)."""

from constructor import Ejercicio

DATOS_DEMO = '''
saldo_inicial_demo = 60.0
movimientos_demo = [
    ("2026-02-01", "ventas", 45.00),
    ("2026-02-02", "proveedor", -120.00),
    ("2026-02-03", "ventas", 10.00),
    ("2026-02-04", "ajuste", 0.00),
    ("2026-02-05", "ventas", 40.00),
    ("2026-02-06", "luz", -40.00),
    ("2026-02-07", "ventas", 55.00),
    ("2026-02-08", "agua", -25.00),
]
'''


def agregar(libro):
    libro.md("""
# Módulo 2 — Estado acumulativo y control de flujo
⏱️ **70 min** · Objetivo: llevar un **estado** (saldo, stock) que cambia en cada vuelta, detectar **eventos** mientras avanza y buscar extremos sin trampas.
""", id="m2-titulo")

    # ------------------------------------------------------------------
    # Concepto 1: agregación final vs paso a paso
    # ------------------------------------------------------------------
    libro.md("## 1. Agregación final (`sum`) vs seguimiento paso a paso")
    libro.prediccion(
        ["línea 1 (saldo_inicial + sum)", "línea 2 (la lista de saldos)", "línea 3 (el saldo más bajo)"],
        '''
saldo_inicial = 60.0
montos = [45.0, -120.0, 10.0, 0.0, 40.0, -40.0, 55.0, -25.0]

print(saldo_inicial + sum(montos))          # línea 1

saldos = []
saldo = saldo_inicial
for monto in montos:
    saldo += monto
    saldos.append(saldo)
print(saldos)                                # línea 2
print(min(saldos))                           # línea 3
''')
    libro.md("""
**Teoría corta**

- **Agregación final** (`sum`, `len`, `min`…): un solo número al final. Responde «¿cuánto quedó?».
- **Seguimiento paso a paso:** guardas el estado en cada vuelta (una lista de saldos). Responde «¿**cuándo** pasó?», «¿**cuántos** días?», «¿**cuál fue el peor** momento?».
- Con los mismos datos, `sum` te da el saldo final, pero **no** te dice si en el camino la cuenta quedó en rojo.

Traza (vuelta | elemento | estado | evento):
""")
    libro.ejemplo(DATOS_DEMO + '''
saldo = saldo_inicial_demo
saldos = []
print(f"saldo inicial: {saldo:.2f}")
print(f"{'vuelta':<7}| {'fecha':<11}| {'monto':>8} | {'saldo':>8} | evento")
vuelta = 0
for fecha, concepto, monto in movimientos_demo:
    vuelta += 1
    saldo += monto
    saldos.append(saldo)
    evento = "en rojo" if saldo < 0 else ""
    print(f"{vuelta:<7}| {fecha:<11}| {monto:>8.2f} | {saldo:>8.2f} | {evento}")

print()
print("saldo final con sum:", saldo_inicial_demo + sum(m[2] for m in movimientos_demo))
print("saldo final paso a paso:", saldos[-1], "| saldo más bajo:", min(saldos))
''')

    # ------------------------------------------------------------------
    # Concepto 2: el estado arranca en el valor inicial
    # ------------------------------------------------------------------
    libro.md("## 2. El estado arranca en el valor inicial, no en 0")
    libro.prediccion(
        ["vuelta 1: saldo_mal saldo_bien", "vuelta 2: saldo_mal saldo_bien", "vuelta 3: saldo_mal saldo_bien", "última línea (True o False)"],
        '''
saldo_inicial = 60.0
montos = [45.0, -120.0, 10.0]

saldo_mal = 0                  # arrancar en 0...
saldo_bien = saldo_inicial     # ...vs. arrancar en el valor inicial
for monto in montos:
    saldo_mal += monto
    saldo_bien += monto
    print(saldo_mal, saldo_bien)

print(saldo_mal + saldo_inicial == saldo_bien)
''')
    libro.md("""
**Teoría corta**

Arrancar en 0 y sumar `saldo_inicial` **al final** da el mismo resultado final, y por eso parece correcto. Pero los **valores intermedios están mal**: cada saldo del camino está desplazado por `saldo_inicial`, así que cualquier pregunta sobre el camino (¿estuvo en rojo?, ¿cuál fue el mínimo?) da respuestas falsas.

**Regla:** el estado nace con el valor que tenía **antes** del primer elemento.
""")
    libro.ejemplo(DATOS_DEMO + '''
saldo_mal = 0
saldo_bien = saldo_inicial_demo
vuelta = 0
print(f"{'vuelta':<7}| {'monto':>8} | {'saldo_mal':>9} | {'saldo_bien':>10} | ¿rojo según mal? | ¿rojo según bien?")
for fecha, concepto, monto in movimientos_demo:
    vuelta += 1
    saldo_mal += monto
    saldo_bien += monto
    print(f"{vuelta:<7}| {monto:>8.2f} | {saldo_mal:>9.2f} | {saldo_bien:>10.2f} | {str(saldo_mal < 0):<16} | {saldo_bien < 0}")
''')

    # ------------------------------------------------------------------
    # Concepto 3: eventos dentro del bucle
    # ------------------------------------------------------------------
    libro.md("## 3. Eventos dentro del bucle: primero, todos y cruces")
    libro.prediccion(
        ["dias_en_rojo", "entradas (veces que la cuenta ENTRA en rojo)"],
        '''
saldo = 60.0
saldo_anterior = saldo
dias_en_rojo = 0
entradas = 0
for monto in [45.0, -120.0, 10.0, 0.0, 40.0, -40.0, 55.0, -25.0]:
    saldo += monto
    if saldo < 0:
        dias_en_rojo += 1
        if saldo_anterior >= 0:
            entradas += 1
    saldo_anterior = saldo
print(dias_en_rojo, entradas)
''')
    libro.md("""
**Teoría corta**

Tres preguntas distintas sobre el mismo recorrido:

| Pregunta | Patrón |
|---|---|
| **Primer** día en sobregiro | guarda la fecha y `break` (deja `None` si nunca ocurre) |
| **Todos** los días en sobregiro | `lista.append(fecha)` en cada vuelta con `saldo < 0` |
| **Cruces** de ≥ 0 a < 0 | necesitas recordar el `saldo_anterior` |

Diferencia clave:
- **Estar** en sobregiro es un *estado*: `saldo < 0` (basta el saldo actual).
- **Entrar** en sobregiro es un *evento*: `saldo_anterior >= 0 and saldo < 0` (necesitas el pasado).

⚠️ Actualiza `saldo_anterior = saldo` **al final** de cada vuelta, después de haberlo usado.
""")
    libro.ejemplo(DATOS_DEMO + '''
# a) PRIMER día en sobregiro: break y None si nunca ocurre
primer_dia = None
saldo = saldo_inicial_demo
for fecha, concepto, monto in movimientos_demo:
    saldo += monto
    if saldo < 0:
        primer_dia = fecha
        break
print("primer día en sobregiro:", primer_dia)

# b) TODOS los días en sobregiro
dias_en_rojo = []
saldo = saldo_inicial_demo
for fecha, concepto, monto in movimientos_demo:
    saldo += monto
    if saldo < 0:
        dias_en_rojo.append(fecha)
print("días en sobregiro:", dias_en_rojo)

# c) CRUCES (entradas y salidas) con traza
saldo = saldo_inicial_demo
saldo_anterior = saldo
entradas = 0
vuelta = 0
print()
print(f"{'vuelta':<7}| {'fecha':<11}| {'monto':>8} | {'anterior → nuevo':<19}| {'en rojo':<8}| evento")
for fecha, concepto, monto in movimientos_demo:
    vuelta += 1
    saldo += monto
    if saldo_anterior >= 0 and saldo < 0:
        evento = "ENTRA en sobregiro"
        entradas += 1
    elif saldo_anterior < 0 and saldo >= 0:
        evento = "SALE del sobregiro"
    elif saldo < 0:
        evento = "sigue en sobregiro"
    else:
        evento = "-"
    print(f"{vuelta:<7}| {fecha:<11}| {monto:>8.2f} | {saldo_anterior:>7.2f} → {saldo:>7.2f} | {str(saldo < 0):<8}| {evento}")
    saldo_anterior = saldo          # se actualiza AL FINAL de la vuelta
print("\\nentradas en sobregiro:", entradas)
''')
    libro.md("**Gráfico ilustrativo** (aquí sí usamos `matplotlib`): el saldo en el tiempo, la línea del 0 y los días en sobregiro marcados.")
    libro.ejemplo(DATOS_DEMO + '''
import matplotlib.pyplot as plt

dias, saldos = [], []
dias_rojos, saldos_rojos = [], []
saldo = saldo_inicial_demo
for fecha, concepto, monto in movimientos_demo:
    saldo += monto
    dias.append(fecha[5:])                  # "02-01"
    saldos.append(saldo)
    if saldo < 0:
        dias_rojos.append(fecha[5:])
        saldos_rojos.append(saldo)

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.axhspan(min(saldos) - 15, 0, color="#c0392b", alpha=0.07)          # zona en rojo
ax.plot(dias, saldos, color="#2a6fbb", linewidth=2, marker="o", markersize=6,
        label="Saldo al cierre del día")
ax.scatter(dias_rojos, saldos_rojos, color="#c0392b", s=90, zorder=3,
           label="Día en sobregiro")
ax.axhline(0, color="#444444", linewidth=1.2)                          # línea del 0
ax.set_title("Saldo de la cuenta día a día (S/)")
ax.set_xlabel("Día (mes-día)")
ax.set_ylabel("Saldo (S/)")
ax.grid(axis="y", color="#dddddd", linewidth=0.8)
ax.legend(frameon=False, loc="upper right")
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
plt.show()
''')

    # ------------------------------------------------------------------
    # Concepto 4: extremos a mano
    # ------------------------------------------------------------------
    libro.md("## 4. Extremos a mano: `None` como centinela y el registro completo")
    libro.prediccion(
        ["línea 1 (menor venta con menor = 0)", "línea 2 (menor venta con None)", "línea 3 (fecha con `<` en el empate)", "línea 4 (fecha con `<=` en el empate)"],
        '''
ventas_dia = [("2026-04-01", 38.5), ("2026-04-02", 52.0), ("2026-04-03", 29.9), ("2026-04-04", 61.4)]

menor = 0
for fecha, venta in ventas_dia:
    if venta < menor:
        menor = venta
print(menor)                                   # línea 1

menor = None
for fecha, venta in ventas_dia:
    if menor is None or venta < menor:
        menor = venta
print(menor)                                   # línea 2

empate = [("2026-04-01", 30.0), ("2026-04-02", 25.0), ("2026-04-03", 25.0)]
mejor_valor, mejor_registro = None, None
for registro in empate:
    if mejor_valor is None or registro[1] < mejor_valor:
        mejor_valor, mejor_registro = registro[1], registro
print(mejor_registro[0])                       # línea 3

mejor_valor, mejor_registro = None, None
for registro in empate:
    if mejor_valor is None or registro[1] <= mejor_valor:
        mejor_valor, mejor_registro = registro[1], registro
print(mejor_registro[0])                       # línea 4
''')
    libro.md("""
**Teoría corta**

- Un **centinela** es un valor especial que significa «todavía no hay ninguno». `None` es el centinela correcto porque **no puede confundirse con un dato real**.
- Patrón: `mejor_valor = None`, `mejor_registro = None`; en el `if`, pregunta primero `mejor_valor is None or ...` (con `is`, no `==`).
- **Guarda el registro completo** (`mejor_registro`), no solo el valor: así recuperas fecha y concepto sin recorrer otra vez.
- **Inicializar en 0 es un bug latente.** Con `monto_mas_negativo = 0` funciona cuando hay egresos, porque el 0 hace de filtro. Pero si todos los datos son positivos (la venta más pequeña) el 0 «gana» y nunca se actualiza.
- **Empates:** con `<` te quedas con el **primero** que alcanzó el extremo; con `<=`, con el **último**.
""")
    libro.ejemplo('''
conjuntos = {
    "movimientos mixtos (hay egresos)": [("2026-04-01", 120.0), ("2026-04-02", -35.0), ("2026-04-03", -80.0)],
    "solo ventas (todo positivo)": [("2026-04-01", 38.5), ("2026-04-02", 52.0), ("2026-04-03", 29.9)],
}

for nombre, registros in conjuntos.items():
    con_cero = 0
    con_none = None
    registro_none = None
    for registro in registros:
        if registro[1] < con_cero:
            con_cero = registro[1]
        if con_none is None or registro[1] < con_none:
            con_none = registro[1]
            registro_none = registro
    print(f"{nombre}\\n   inicializando en 0 → {con_cero}\\n   inicializando en None → {registro_none}\\n")
''')

    # ------------------------------------------------------------------
    # Concepto 5: break vs continue
    # ------------------------------------------------------------------
    libro.md("## 5. `break` vs `continue` (y una trampa)")
    libro.prediccion(
        ["dias_en_rojo con el continue mal puesto (¿4 o 3?)", "dias_en_rojo sin el continue"],
        '''
movimientos = [("2026-02-01", "ventas", 45.0), ("2026-02-02", "proveedor", -120.0),
               ("2026-02-03", "ventas", 10.0), ("2026-02-04", "ajuste", 0.0),
               ("2026-02-05", "ventas", 40.0), ("2026-02-06", "luz", -40.0)]

saldo = 60.0
dias_en_rojo = 0
for fecha, concepto, monto in movimientos:
    if monto == 0:
        continue                 # «sumar 0 no cambia nada, lo salto»
    saldo += monto
    if saldo < 0:
        dias_en_rojo += 1
print(dias_en_rojo)              # con el continue

saldo = 60.0
dias_en_rojo = 0
for fecha, concepto, monto in movimientos:
    saldo += monto
    if saldo < 0:
        dias_en_rojo += 1
print(dias_en_rojo)              # sin el continue
''')
    libro.md("""
**Teoría corta**

- **`break`:** termina el bucle completo. Úsalo cuando ya tienes la respuesta (el primer día en rojo).
- **`continue`:** salta al **siguiente elemento**; todo lo que hay **debajo** del `continue`, en esa vuelta, **no se ejecuta**.
- **La trampa:** un `continue` para saltar montos 0, puesto **antes** del chequeo de sobregiro, se salta un día que **sí estaba** en sobregiro (el saldo sigue negativo aunque el monto sea 0). El día existe aunque el monto no cambie nada.
- Regla práctica: antes de escribir un `continue`, pregunta «¿todo lo que viene después es irrelevante para este elemento?». Con saldos, casi nunca lo es: **sumar 0 no cambia el saldo, así que no hace falta filtrarlo**.
""")

    libro.ejemplo(DATOS_DEMO + '''
# Misma cuenta, dos versiones: el continue mal ubicado se salta el 2026-02-04
for version in ("con continue antes del chequeo", "sin continue (correcta)"):
    saldo = saldo_inicial_demo
    dias_en_rojo = []
    print(version)
    for fecha, concepto, monto in movimientos_demo:
        if version.startswith("con") and monto == 0:
            print(f"   {fecha}  monto 0 → continue: se salta el chequeo")
            continue
        saldo += monto
        if saldo < 0:
            dias_en_rojo.append(fecha)
        print(f"   {fecha}  saldo {saldo:>7.2f}  {'en rojo' if saldo < 0 else ''}")
    print(f"   → días en sobregiro: {len(dias_en_rojo)}\\n")
''')

    # ------------------------------------------------------------------
    # Ejercicios
    # ------------------------------------------------------------------
    libro.md("## 🏋️ Ejercicios del módulo 2")

    # ---- 2.1 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="2.1", titulo="Saldos paso a paso", nivel="🟢 Básico",
        enunciado="""
Una bodega abre junio con `saldo_inicial = 250.0`. Con sus movimientos `(fecha, concepto, monto)`, calcula el **saldo después de cada movimiento** y el saldo final.

**Variables a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `saldos` | `list` de `float` | saldo al cierre de **cada** movimiento, redondeado a 2 decimales |
| `saldo_final` | `float` | último saldo, redondeado a 2 decimales |
""",
        datos='''
saldo_inicial = 250.0
movimientos = [
    ("2026-06-01", "proveedor", -180.50),
    ("2026-06-02", "ventas del día", 95.20),
    ("2026-06-03", "ajuste", 0.0),
    ("2026-06-04", "luz", -64.30),
    ("2026-06-05", "ventas del día", 132.75),
    ("2026-06-06", "agua", -28.10),
    ("2026-06-07", "proveedor", -90.00),
    ("2026-06-08", "ventas del día", 210.40),
]
_movimientos_originales = list(movimientos)   # copia para la validación (no la toques)
''',
        plantilla='''
saldos = None        # list de float (2 decimales), un saldo por movimiento
saldo_final = None   # float (2 decimales)

# Tu código aquí
''',
        validacion='''
assert isinstance(saldos, list), "saldos debe ser una lista: ¿la creaste con [] y usaste append?"
assert len(saldos) == len(movimientos), \\
    "Debe haber un saldo por cada movimiento: ¿filtraste los montos 0? Sumar 0 no cambia el saldo, pero ese día existe."
assert saldos[0] == 69.5, \\
    "El primer saldo debe ser saldo_inicial + primer monto (250 - 180.50): ¿arrancaste el saldo en 0?"
assert all(round(s, 2) == s for s in saldos), "¿Redondeaste a 2 decimales cada saldo que guardas?"
assert saldos == [69.5, 164.7, 164.7, 100.4, 233.15, 205.05, 115.05, 325.45], \\
    "Los saldos no coinciden: revisa que el estado acumule (saldo += monto) y no se reinicie."
assert saldo_final == 325.45, "saldo_final debe ser 325.45 (redondeado a 2 decimales)."
assert movimientos == _movimientos_originales, "Cuidado: modificaste la lista original `movimientos`."
''',
        pistas=[
            "Necesitas una variable de estado (saldo) y una lista vacía (saldos). En cada vuelta: actualiza el estado y guarda una copia del estado en la lista.",
            "saldo = saldo_inicial (¡no 0!), saldos = []; for fecha, concepto, monto in movimientos: saldo += monto; saldos.append(round(saldo, 2)). Al final, saldo_final sale del último saldo.",
        ],
        solucion='''
saldo = saldo_inicial            # el estado arranca en el valor inicial
saldos = []
for fecha, concepto, monto in movimientos:
    saldo += monto               # incluye los montos 0: no hace falta filtrarlos
    saldos.append(round(saldo, 2))
saldo_final = round(saldo, 2)
''',
        errores="""Arrancar saldo en 0 y sumar saldo_inicial al final: saldo_final sale bien pero cada saldo intermedio está desplazado.
Filtrar el monto 0 elimina un día de la lista aunque el saldo de ese día existe.
Guardar saldo sin round deja valores como 164.70000000000002.""",
    ))

    # ---- 2.2 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="2.2", titulo="Primer día de sobregiro", nivel="🟡 Intermedio",
        enunciado="""
Halla la **fecha del primer día** en que el saldo queda **por debajo de 0**. Usa `break` y `None` como resultado cuando **nunca** ocurre. Se prueba con dos cuentas: una que sí entra en sobregiro (`a`) y una que nunca lo hace (`b`).

**Variables a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `primer_dia_a` | `str` o `None` | fecha ISO del primer saldo < 0 en `movimientos_a` |
| `primer_dia_b` | `str` o `None` | igual, para `movimientos_b` (debe quedar `None` si nunca ocurre) |

Escribe el mismo recorrido dos veces (una por cuenta): en otra sesión verás cómo evitar la repetición.
""",
        datos='''
saldo_inicial_a = 120.0
movimientos_a = [
    ("2026-07-01", "proveedor", -75.00),
    ("2026-07-02", "ventas", 60.00),
    ("2026-07-03", "luz", -50.00),
    ("2026-07-04", "ajuste", 0.00),
    ("2026-07-05", "proveedor", -98.50),
    ("2026-07-06", "ventas", 40.00),
    ("2026-07-07", "ventas", 70.00),
]

saldo_inicial_b = 500.0
movimientos_b = [
    ("2026-07-01", "proveedor", -120.00),
    ("2026-07-02", "ventas", 85.50),
    ("2026-07-03", "agua", -31.20),
    ("2026-07-04", "luz", -58.90),
    ("2026-07-05", "ventas", 60.00),
    ("2026-07-06", "proveedor", -140.25),
]
_originales = (list(movimientos_a), list(movimientos_b))   # copias para la validación (no las toques)
''',
        plantilla='''
primer_dia_a = "sin resolver"   # str o None
primer_dia_b = "sin resolver"   # str o None

# Tu código aquí
''',
        validacion='''
assert primer_dia_a == "2026-07-05", \\
    "primer_dia_a incorrecto. Si obtienes '2026-07-06' te falta el break; si arrancaste el saldo en 0 el sobregiro aparece demasiado pronto."
assert primer_dia_b is None, \\
    "primer_dia_b debe ser None: en la cuenta b nunca hay sobregiro. ¿Devolviste 0, '' o la última fecha?"
assert (movimientos_a, movimientos_b) == _originales, "Cuidado: modificaste una de las listas originales."
''',
        pistas=[
            "Parte de primer_dia = None (aún no hay). Recorre con el saldo arrancando en saldo_inicial; en el momento en que saldo < 0, guarda la fecha y sal del bucle.",
            "saldo = saldo_inicial_a; primer_dia_a = None; for fecha, concepto, monto in movimientos_a: saldo += monto; if saldo < 0: primer_dia_a = fecha; break. Repite con la cuenta b, empezando de nuevo saldo y primer_dia_b.",
        ],
        solucion='''
saldo = saldo_inicial_a
primer_dia_a = None                      # centinela: todavía no hay sobregiro
for fecha, concepto, monto in movimientos_a:
    saldo += monto
    if saldo < 0:
        primer_dia_a = fecha
        break                            # ya tengo la respuesta: salgo del bucle

saldo = saldo_inicial_b                  # el estado se reinicia con SU valor inicial
primer_dia_b = None
for fecha, concepto, monto in movimientos_b:
    saldo += monto
    if saldo < 0:
        primer_dia_b = fecha
        break
''',
        errores="""Sin break el bucle sigue y se queda con el último día en rojo en vez del primero.
Inicializar primer_dia con "" o 0 en lugar de None: cuando nunca hay sobregiro entregas un dato falso.
Olvidar reiniciar saldo antes de la segunda cuenta arrastra el saldo de la primera.""",
    ))

    # ---- 2.3 (bug) ---------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="2.3", titulo="Saldo mínimo y su fecha", nivel="🟡 Intermedio", es_bug=True,
        enunciado="""
La cuenta abre agosto con `saldo_inicial = 400.0` y **nunca baja de 0**. Se quiere el **saldo más bajo alcanzado** después de un movimiento y la **fecha** en que ocurrió (si hay empate, la primera).

El código siguiente **corre sin errores pero da un resultado incorrecto**. Encuentra el error y arréglalo.

**Variables a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `saldo_minimo` | `float` | menor saldo tras un movimiento (2 decimales) |
| `fecha_saldo_minimo` | `str` | fecha ISO de ese saldo (la primera si hay empate) |
""",
        datos='''
saldo_inicial = 400.0
movimientos = [
    ("2026-08-01", "proveedor", -150.00),
    ("2026-08-02", "ventas", 80.00),
    ("2026-08-03", "luz", -95.50),
    ("2026-08-04", "ventas", 120.30),
    ("2026-08-05", "alquiler", -200.00),
    ("2026-08-06", "ajuste", 0.00),
    ("2026-08-07", "ventas", 99.00),
    ("2026-08-08", "agua", -44.10),
]
_movimientos_originales = list(movimientos)   # copia para la validación (no la toques)
''',
        plantilla='''
# 🐛 Este código tiene un error típico. Arréglalo (puedes reescribirlo).
saldo = saldo_inicial
saldo_minimo = 0
fecha_saldo_minimo = None
for fecha, concepto, monto in movimientos:
    saldo += monto
    if saldo < saldo_minimo:
        saldo_minimo = saldo
        fecha_saldo_minimo = fecha
''',
        validacion='''
assert fecha_saldo_minimo is not None, \\
    "fecha_saldo_minimo quedó en None: ¿inicializaste saldo_minimo en 0? Aquí ningún saldo baja de 0, así que nunca se actualiza."
assert saldo_minimo != 0, \\
    "saldo_minimo quedó en 0: el 0 «gana» porque todos los saldos son positivos. Usa None como centinela."
assert round(saldo_minimo, 2) == 154.8, "saldo_minimo incorrecto: debe ser el menor saldo tras un movimiento (154.8)."
assert fecha_saldo_minimo == "2026-08-05", \\
    "La fecha es la del PRIMER día con ese saldo mínimo: ¿usaste <= y te quedaste con el último empate?"
assert round(saldo_minimo, 2) == saldo_minimo, "¿Redondeaste saldo_minimo a 2 decimales?"
assert movimientos == _movimientos_originales, "Cuidado: modificaste la lista original `movimientos`."
''',
        pistas=[
            "Pregúntate qué pasa con el valor inicial del mínimo cuando NINGÚN saldo es menor que él. ¿Quién es el «mejor hasta ahora» antes de mirar el primer movimiento?",
            "Cambia saldo_minimo = 0 por None y ajusta la condición del if para que el primer saldo siempre se acepte: if saldo_minimo is None or saldo < saldo_minimo. Redondea al final.",
        ],
        solucion='''
saldo = saldo_inicial
saldo_minimo = None                                   # centinela: aún no hay mínimo
fecha_saldo_minimo = None
for fecha, concepto, monto in movimientos:
    saldo += monto
    if saldo_minimo is None or saldo < saldo_minimo:  # `<` conserva el primero en un empate
        saldo_minimo = saldo
        fecha_saldo_minimo = fecha
saldo_minimo = round(saldo_minimo, 2)
''',
        errores="""Inicializar el mínimo en 0 solo funciona si hay saldos negativos; con saldos positivos el 0 nunca se supera.
Con `<=` en lugar de `<` el empate lo gana el último día (2026-08-06) y no el primero.
Guardar solo el valor y no la fecha obliga a recorrer otra vez para encontrarla.""",
    ))

    # ---- 2.4 ---------------------------------------------------------
    libro.ejercicio(Ejercicio(
        num="2.4", titulo="Kárdex de un producto", nivel="🔴 Integrador",
        enunciado="""
Una bodega lleva el kárdex del aceite de 1 L: `stock_inicial = 40` unidades y `stock_minimo = 15`. Cada movimiento es `(fecha, tipo, cantidad)` con `tipo` igual a `"entrada"` (suma) o `"salida"` (resta). **En un solo recorrido**, obtén:

**Variables a crear**

| Nombre | Tipo | Contenido |
|---|---|---|
| `stock_final` | `int` | stock tras el último movimiento |
| `fechas_bajo_minimo` | `list` de `str` | fecha de cada movimiento tras el cual el stock queda **< `stock_minimo`** |
| `fecha_recuperacion` | `str` o `None` | **primera** fecha en que el stock pasa de estar bajo el mínimo a **> `stock_minimo`** |
| `mayor_salida` | `tuple` | el movimiento **completo** de mayor cantidad entre las **salidas** (en empate, el primero) |
""",
        datos='''
stock_inicial = 40
stock_minimo = 15
movimientos_kardex = [
    ("2026-09-01", "salida", 12),
    ("2026-09-02", "salida", 9),
    ("2026-09-03", "salida", 7),
    ("2026-09-04", "salida", 4),
    ("2026-09-05", "entrada", 20),
    ("2026-09-06", "salida", 15),
    ("2026-09-07", "salida", 3),
    ("2026-09-08", "entrada", 30),
    ("2026-09-09", "salida", 15),
    ("2026-09-10", "salida", 15),
]
_kardex_original = list(movimientos_kardex)   # copia para la validación (no la toques)
''',
        plantilla='''
stock_final = None           # int
fechas_bajo_minimo = None    # list de str
fecha_recuperacion = None    # str o None
mayor_salida = None          # tuple (fecha, tipo, cantidad)

# Tu código aquí
''',
        validacion='''
assert stock_final == 10, "stock_final debe ser 10: ¿las entradas suman y las salidas restan?"
assert fechas_bajo_minimo == ["2026-09-03", "2026-09-04", "2026-09-06", "2026-09-07", "2026-09-10"], \\
    "fechas_bajo_minimo incorrecta: es el stock DESPUÉS de cada movimiento el que se compara con el mínimo."
assert fecha_recuperacion == "2026-09-05", \\
    "fecha_recuperacion: es la primera vez que el stock pasa de estar bajo el mínimo a superarlo (necesitas el stock anterior)."
assert mayor_salida is not None and mayor_salida[1] == "salida", \\
    "mayor_salida debe ser una salida: ¿incluiste las entradas (como la de 30 unidades)?"
assert mayor_salida == ("2026-09-06", "salida", 15), \\
    "mayor_salida debe ser la tupla completa de la primera salida de 15: ¿usaste >= y te quedaste con el último empate?"
assert movimientos_kardex == _kardex_original, "Cuidado: modificaste la lista original `movimientos_kardex`."
''',
        pistas=[
            "Lleva estas variables de estado: el stock (empieza en stock_inicial), la lista de fechas, la fecha de recuperación (empieza en None), y la mayor salida (empieza en None). Para la recuperación necesitas también el stock anterior.",
            "En cada vuelta: guarda stock_anterior = stock; suma o resta según el tipo; si stock < stock_minimo, agrega la fecha; si fecha_recuperacion es None y stock_anterior < stock_minimo y stock > stock_minimo, guarda la fecha. La mayor salida se actualiza solo dentro de las salidas, con mayor_salida is None or cantidad > mayor_salida[2].",
        ],
        solucion='''
stock = stock_inicial
fechas_bajo_minimo = []
fecha_recuperacion = None
mayor_salida = None
for movimiento in movimientos_kardex:            # un solo recorrido, cuatro resultados
    fecha, tipo, cantidad = movimiento
    stock_anterior = stock
    if tipo == "entrada":
        stock += cantidad
    else:
        stock -= cantidad
        if mayor_salida is None or cantidad > mayor_salida[2]:   # `>` estricto: gana el primero
            mayor_salida = movimiento                            # registro completo
    if stock < stock_minimo:
        fechas_bajo_minimo.append(fecha)
    if fecha_recuperacion is None and stock_anterior < stock_minimo and stock > stock_minimo:
        fecha_recuperacion = fecha
stock_final = stock
''',
        errores="""Comparar con el stock mínimo sin recordar el stock anterior: no distingues «estar bajo» de «volver a superarlo».
Buscar la mayor cantidad entre todos los movimientos incluye entradas (la de 30 unidades).
Con `>=` en vez de `>` el empate lo gana la última salida de 15.""",
    ))

    libro.volcar_soluciones("## 🔒 Soluciones del módulo 2\nAbre cada celda **solo después de intentarlo**.")
