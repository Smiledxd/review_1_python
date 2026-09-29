"""Parte 2 · Estado acumulativo y control de flujo (secciones 5 a 8)."""

from libro import Ejercicio

CUENTA_EJ = '''movimientos_ej = [
    ("2026-02-01", "ventas", 45.00),
    ("2026-02-02", "proveedor", -120.00),
    ("2026-02-03", "ventas", 10.00),
    ("2026-02-04", "ajuste", 0.00),
    ("2026-02-05", "ventas", 40.00),
    ("2026-02-06", "luz", -40.00),
    ("2026-02-07", "ventas", 55.00),
    ("2026-02-08", "agua", -25.00),
]
saldo_inicial_ej = 60.0'''


def agregar(nb):
    nb.md("""
---
# Parte 2 · Estado acumulativo y control de flujo
⏱️ 70 minutos · Secciones 5 a 8
""", id="parte-2")

    # ------------------------------------------------------------------ 5
    nb.md("""
---
## 5. El estado arranca en su valor inicial

### 📘 Concepto
- **Agregación final** (`sum`, `len`): un número al final. Responde «¿cuánto quedó?».
- **Seguimiento paso a paso**: guardas el estado en cada vuelta (una lista de saldos). Responde «¿**cuándo** pasó?», «¿**cuántos** días?», «¿cuál fue el **peor** momento?».

El estado **nace con el valor que tenía antes del primer movimiento**:
```python
saldo = saldo_inicial        # no 0
for fecha, concepto, monto in movimientos:
    saldo += monto
    saldos.append(saldo)
```
Si arrancas en 0 y sumas `saldo_inicial` al final, el saldo final coincide, y por eso parece correcto. Pero **cada saldo intermedio está desplazado**, y todo lo que preguntes sobre el camino (¿estuvo en rojo?, ¿cuál fue el mínimo?) sale mal.
""")
    nb.codigo(f'''
# 🔮 Predice antes de ejecutar: ¿en qué vueltas dicen cosas distintas las dos columnas "¿rojo?"?
# Mi predicción:

{CUENTA_EJ}

saldo_mal = 0                   # arranca en 0 (bug)
saldo_bien = saldo_inicial_ej   # arranca en el valor inicial
print(f"{{'vuelta':<7}}| {{'monto':>8}} | {{'saldo_mal':>9}} | {{'saldo_bien':>10}} | ¿rojo (mal)? | ¿rojo (bien)?")
for vuelta, (fecha, concepto, monto) in enumerate(movimientos_ej, start=1):
    saldo_mal += monto
    saldo_bien += monto
    print(f"{{vuelta:<7}}| {{monto:>8.2f}} | {{saldo_mal:>9.2f}} | {{saldo_bien:>10.2f}} | {{str(saldo_mal < 0):<12}} | {{saldo_bien < 0}}")

print("\\nsaldo final (mal + inicial):", saldo_mal + saldo_inicial_ej, "| saldo final (bien):", saldo_bien)
''')
    nb.md("**Gráfico ilustrativo** (aquí sí usamos `matplotlib`): el saldo día a día, la línea del 0 y los días en sobregiro marcados.")
    nb.codigo(f'''
import matplotlib.pyplot as plt

{CUENTA_EJ}

dias_ej, saldos_ej, dias_rojos_ej, saldos_rojos_ej = [], [], [], []
saldo = saldo_inicial_ej
for fecha, concepto, monto in movimientos_ej:
    saldo += monto
    dias_ej.append(fecha[5:])                  # "02-01"
    saldos_ej.append(saldo)
    if saldo < 0:
        dias_rojos_ej.append(fecha[5:])
        saldos_rojos_ej.append(saldo)

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.axhspan(min(saldos_ej) - 15, 0, color="#c0392b", alpha=0.07)       # zona en rojo
ax.plot(dias_ej, saldos_ej, color="#2a6fbb", linewidth=2, marker="o", markersize=6, label="Saldo al cierre del día")
ax.scatter(dias_rojos_ej, saldos_rojos_ej, color="#c0392b", s=90, zorder=3, label="Día en sobregiro")
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
    nb.ejercicio(Ejercicio(
        clave="5", titulo="Ejercicio 5: saldos paso a paso", check="check_ejercicio_5()",
        enunciado="""
La caja de una bodega abre con `saldo_inicial_caja` y registra `movimientos_caja` `(fecha, concepto, monto)`. Crea:
1. `saldos_caja`: lista con el saldo **después de cada movimiento**, cada uno redondeado a 2 decimales (uno por movimiento, también el del ajuste de 0).
2. `saldo_cierre`: el último saldo, redondeado a 2 decimales.
""",
        pistas=[
            "Necesitas una variable de estado (el saldo) y una lista vacía. En cada vuelta: actualiza el estado y guarda una copia redondeada en la lista.",
            "`saldo = saldo_inicial_caja` (¡no 0!), `saldos_caja = []`; dentro del `for`: `saldo += monto` y `saldos_caja.append(round(saldo, 2))`. "
            "No filtres el monto 0: ese día también tiene saldo.",
        ],
        solucion='''
saldo = saldo_inicial_caja            # el estado arranca en el valor inicial
saldos_caja = []
for fecha, concepto, monto in movimientos_caja:
    saldo += monto                    # el monto 0 no cambia el saldo, pero el día cuenta
    saldos_caja.append(round(saldo, 2))
saldo_cierre = round(saldo, 2)
''',
        errores="arrancar en 0 y sumar el saldo inicial al final (el cierre sale bien, los intermedios no) "
                "o filtrar el monto 0 y perder un día de la lista.",
    ))

    # ------------------------------------------------------------------ 6
    nb.md("""
---
## 6. Eventos dentro del bucle: el primero, todos y los cruces

### 📘 Concepto
Tres preguntas distintas sobre el mismo recorrido:

| Pregunta | Patrón |
|---|---|
| El **primer** día en rojo | `primero = None` antes; al encontrarlo, guarda la fecha y `break` |
| **Todos** los días en rojo | `lista.append(fecha)` en cada vuelta con `saldo < 0` |
| **Cuántas veces entra** en rojo | recuerda `saldo_anterior` y cuenta cuando `saldo_anterior >= 0 and saldo < 0` |

- **Estar** en rojo es un estado: basta el saldo actual.
- **Entrar** en rojo es un evento: necesitas el saldo **anterior**. Actualízalo **al final** de cada vuelta, después de usarlo.

**`break` vs `continue`:** `break` termina el bucle entero. `continue` salta al siguiente elemento, y todo lo que hay **debajo** de él no se ejecuta en esa vuelta. Un `continue` para «saltar los montos 0», puesto **antes** del chequeo de sobregiro, se salta un día que **sí** estaba en rojo.
""")
    nb.codigo(f'''
# 🔮 Predice antes de ejecutar: ¿cuántos días en rojo hay? ¿Cuántas veces ENTRA la cuenta en rojo?
# Mi predicción:

{CUENTA_EJ}

saldo = saldo_inicial_ej
saldo_anterior = saldo
entradas_ej = 0
print(f"{{'vuelta':<7}}| {{'fecha':<11}}| {{'monto':>8}} | {{'anterior → nuevo':<19}}| evento")
for vuelta, (fecha, concepto, monto) in enumerate(movimientos_ej, start=1):
    saldo += monto
    if saldo_anterior >= 0 and saldo < 0:
        evento = "ENTRA en rojo"
        entradas_ej += 1
    elif saldo_anterior < 0 and saldo >= 0:
        evento = "SALE del rojo"
    elif saldo < 0:
        evento = "sigue en rojo"
    else:
        evento = "-"
    print(f"{{vuelta:<7}}| {{fecha:<11}}| {{monto:>8.2f}} | {{saldo_anterior:>7.2f}} → {{saldo:>7.2f}} | {{evento}}")
    saldo_anterior = saldo          # se actualiza AL FINAL de la vuelta
print("\\nentradas en rojo:", entradas_ej)
''')
    nb.codigo(f'''
# 🔮 Predice antes de ejecutar: ¿cuántos días en rojo cuenta cada versión?
# Mi predicción:

{CUENTA_EJ}

for version in ("con continue antes del chequeo", "sin continue (correcta)"):
    saldo = saldo_inicial_ej
    dias_rojo_ej = []
    for fecha, concepto, monto in movimientos_ej:
        if version.startswith("con") and monto == 0:
            continue                          # se salta TODO lo de abajo en esta vuelta
        saldo += monto
        if saldo < 0:
            dias_rojo_ej.append(fecha)
    print(f"{{version:<31}} → {{dias_rojo_ej}}")
''')
    nb.ejercicio(Ejercicio(
        clave="6", titulo="Ejercicio 6: sobregiro, el primero, todos y las entradas", check="check_ejercicio_6()",
        enunciado="""
Con `saldo_inicial_cuenta` y `movimientos_cuenta`, crea:
1. `primer_rojo`: la fecha del **primer** día en que el saldo queda por debajo de 0. Usa `break`.
2. `dias_en_rojo`: lista con **todas** las fechas en que el saldo, después del movimiento, quedó por debajo de 0.
3. `entradas_en_rojo`: cuántas veces el saldo **pasó** de ≥ 0 a < 0.
4. `primer_rojo_ahorro`: lo mismo que el punto 1, pero con `saldo_inicial_ahorro` y `movimientos_ahorro`. Esa cuenta nunca queda en rojo, así que el resultado debe ser `None`.

El recorrido con `break` tiene que ir aparte, porque corta el bucle. Los puntos 2 y 3 caben en un solo recorrido.
""",
        pistas=[
            "Para el punto 1 empieza con `primer_rojo = None`. Cada recorrido reinicia su saldo con **su** saldo inicial. "
            "Para el 3 necesitas `saldo_anterior`, que arranca igual que el saldo.",
            "Dentro del `for` de los puntos 2 y 3: `saldo += monto`; `if saldo < 0:` agrega la fecha y, si además `saldo_anterior >= 0`, suma una entrada; "
            "en la **última** línea de la vuelta, `saldo_anterior = saldo`. No pongas `continue` con el monto 0.",
        ],
        solucion='''
# 1. Primer día en rojo: break
saldo = saldo_inicial_cuenta
primer_rojo = None
for fecha, concepto, monto in movimientos_cuenta:
    saldo += monto
    if saldo < 0:
        primer_rojo = fecha
        break                                   # ya tengo la respuesta

# 2 y 3. Todos los días en rojo y las entradas, en un solo recorrido
saldo = saldo_inicial_cuenta
saldo_anterior = saldo
dias_en_rojo = []
entradas_en_rojo = 0
for fecha, concepto, monto in movimientos_cuenta:
    saldo += monto                              # sin continue: el ajuste de 0 también se revisa
    if saldo < 0:
        dias_en_rojo.append(fecha)              # ESTAR en rojo
        if saldo_anterior >= 0:
            entradas_en_rojo += 1               # ENTRAR en rojo
    saldo_anterior = saldo                      # al final de la vuelta

# 4. Otra cuenta: si nunca pasa, queda None
saldo = saldo_inicial_ahorro
primer_rojo_ahorro = None
for fecha, concepto, monto in movimientos_ahorro:
    saldo += monto
    if saldo < 0:
        primer_rojo_ahorro = fecha
        break
''',
        errores="olvidar el `break` (te quedas con el último día), contar días en vez de entradas, "
                "o poner un `continue` en el monto 0 que se salta un día en rojo.",
    ))

    # ------------------------------------------------------------------ 7
    nb.md("""
---
## 7. Extremos a mano: `None` como centinela

### 📘 Concepto
Un **centinela** es un valor que significa «todavía no hay ninguno». `None` es el correcto porque no puede confundirse con un dato real.

```python
mejor_valor, mejor_registro = None, None
for registro in registros:
    if mejor_valor is None or registro[2] < mejor_valor:     # `is None`, no `== None`
        mejor_valor, mejor_registro = registro[2], registro   # guarda el registro COMPLETO
```

- **Inicializar en 0 es un bug latente.** Para el egreso más grande funciona, porque el 0 hace de filtro. Pero si todos los valores son positivos (la venta más pequeña, el saldo mínimo de una cuenta que nunca baja de 0), el 0 «gana» y nunca se actualiza.
- **Guarda el registro completo**, no solo el valor: así tienes la fecha sin recorrer otra vez.
- **Empates:** con `<` te quedas con el **primero** que alcanzó el extremo; con `<=`, con el **último**.
""")
    nb.codigo('''
# 🔮 Predice antes de ejecutar: ¿qué imprime cada versión en cada lista?
# Mi predicción:

listas_ej = {
    "con egresos": [("2026-04-01", 120.0), ("2026-04-02", -35.0), ("2026-04-03", -80.0)],
    "solo ventas": [("2026-04-01", 38.5), ("2026-04-02", 52.0), ("2026-04-03", 29.9)],
}

for nombre, registros in listas_ej.items():
    menor_cero = 0                           # centinela equivocado
    menor_none, registro_none = None, None   # centinela correcto
    for registro in registros:
        if registro[1] < menor_cero:
            menor_cero = registro[1]
        if menor_none is None or registro[1] < menor_none:
            menor_none, registro_none = registro[1], registro
    print(f"{nombre:<12} | empezando en 0 → {menor_cero:<6} | empezando en None → {registro_none}")
''')
    nb.ejercicio(Ejercicio(
        clave="7", titulo="Ejercicio 7 🐛: el saldo mínimo", check="check_ejercicio_7()",
        enunciado="""
**Parte A.** La celda de abajo busca el **saldo más bajo** de agosto (después de cada movimiento) y la **fecha** en que ocurrió. Si hay empate, vale la primera fecha. Crea o corrige `saldo_minimo` (redondeado a 2 decimales) y `fecha_saldo_minimo`. El código corre sin errores, pero el resultado está mal.

**Parte B.** Con esta lista, predice **sin ejecutar** el nombre del proveedor que queda como «más barato» en cada caso:

```python
precios_proveedor = [("Proveedor A", 12.5), ("Proveedor B", 11.9), ("Proveedor C", 11.9), ("Proveedor D", 13.0)]
mejor = None
for p in precios_proveedor:
    if mejor is None or p[1] < mejor[1]:      # en la otra versión: p[1] <= mejor[1]
        mejor = p
```

| Variable | Pregunta |
|---|---|
| `pred_con_menor` | ¿`mejor[0]` con `<`? |
| `pred_con_menor_igual` | ¿`mejor[0]` con `<=`? |
""",
        plantilla='''
# 🐛 Parte A: este código tiene un error típico. Corrígelo (puedes reescribirlo).
saldo = saldo_inicial_agosto
saldo_minimo = 0
fecha_saldo_minimo = None
for fecha, concepto, monto in movimientos_agosto:
    saldo += monto
    if saldo < saldo_minimo:
        saldo_minimo = saldo
        fecha_saldo_minimo = fecha

# Parte B: tus predicciones
''',
        pistas=[
            "¿Qué pasa con el valor inicial del mínimo si **ningún** saldo es menor que él? ¿Quién es «el mejor hasta ahora» antes de mirar el primer movimiento?",
            "Cambia `saldo_minimo = 0` por `None` y la condición por `saldo_minimo is None or saldo < saldo_minimo`. Mantén `<` para quedarte con la primera fecha y redondea al final.",
        ],
        solucion='''
# Parte A
saldo = saldo_inicial_agosto
saldo_minimo = None                              # centinela: aún no hay mínimo
fecha_saldo_minimo = None
for fecha, concepto, monto in movimientos_agosto:
    saldo += monto
    if saldo_minimo is None or saldo < saldo_minimo:   # `<`: en el empate gana el primero
        saldo_minimo = saldo
        fecha_saldo_minimo = fecha
saldo_minimo = round(saldo_minimo, 2)

# Parte B
pred_con_menor = "Proveedor B"         # con `<` el empate no reemplaza: queda el primero
pred_con_menor_igual = "Proveedor C"   # con `<=` el empate sí reemplaza: queda el último
''',
        errores="inicializar el mínimo en 0: si todos los saldos son positivos, nunca se actualiza. "
                "Con `<=` el empate lo gana el último día.",
    ))

    # ------------------------------------------------------------------ 8
    nb.md("""
---
## 8. Todo junto: un kárdex en un solo recorrido

### 📘 Concepto
Antes de escribir el bucle, **haz la lista de tus variables de estado y su valor inicial**. Es la mitad del ejercicio:

| Qué quiero saber | Variable | Empieza en |
|---|---|---|
| el valor actual | `stock` | `stock_inicial` |
| todas las veces que pasa algo | una lista | `[]` |
| la primera vez que pasa algo | `fecha_...` | `None` |
| un cruce (antes sí, ahora no) | `stock_anterior` | se guarda al inicio de cada vuelta |
| el extremo de un subconjunto | `mayor_...` | `None` |

Dentro del bucle, cada variable se actualiza en su momento, y el orden importa.
""")
    nb.ejercicio(Ejercicio(
        clave="8", titulo="Ejercicio 8: kárdex del aceite", check="check_ejercicio_8()",
        enunciado="""
`kardex` tiene los movimientos del aceite de 1 L como `(fecha, tipo, cantidad)`, donde `tipo` es `"entrada"` (suma) o `"salida"` (resta). El stock arranca en `stock_inicial` y el mínimo aceptable es `stock_minimo`. **En un solo recorrido**, crea:
1. `stock_final`: el stock después del último movimiento.
2. `fechas_bajo_minimo`: lista con las fechas en que el stock, después del movimiento, quedó **por debajo** de `stock_minimo`.
3. `fecha_recuperacion`: la **primera** fecha en que el stock pasa de estar bajo el mínimo a **superarlo** (`> stock_minimo`). `None` si nunca ocurre.
4. `mayor_salida`: la tupla completa de la **salida** con más unidades. Si hay empate, la primera.
""",
        pistas=[
            "Variables de estado: `stock` (empieza en `stock_inicial`), `fechas_bajo_minimo = []`, `fecha_recuperacion = None`, `mayor_salida = None`. "
            "Para la recuperación guarda `stock_anterior = stock` al **inicio** de cada vuelta.",
            "Si el tipo es salida, resta y compara con la mayor salida (`mayor_salida is None or cantidad > mayor_salida[2]`). "
            "Luego: `if stock < stock_minimo` agrega la fecha; `if fecha_recuperacion is None and stock_anterior < stock_minimo and stock > stock_minimo` guarda la fecha.",
        ],
        solucion='''
stock = stock_inicial
fechas_bajo_minimo = []
fecha_recuperacion = None
mayor_salida = None
for movimiento in kardex:                        # un solo recorrido, cuatro resultados
    fecha, tipo, cantidad = movimiento
    stock_anterior = stock
    if tipo == "entrada":
        stock += cantidad
    else:
        stock -= cantidad
        if mayor_salida is None or cantidad > mayor_salida[2]:   # `>`: en el empate gana la primera
            mayor_salida = movimiento                            # registro completo
    if stock < stock_minimo:
        fechas_bajo_minimo.append(fecha)
    if fecha_recuperacion is None and stock_anterior < stock_minimo and stock > stock_minimo:
        fecha_recuperacion = fecha
stock_final = stock
''',
        errores="buscar la mayor cantidad entre todos los movimientos (incluye entradas), "
                "o detectar la recuperación sin el stock anterior.",
    ))
