#@title ⚙️ Setup: ejecuta esta celda y no la edites { display-mode: "form" }
# Prepara los datos de práctica y carga las funciones que revisan tus respuestas.
# (Este archivo es la fuente de la celda de setup del notebook: no se importa, se copia tal cual.)
import copy
import math

# ======================================================================
# Datos de práctica
# ======================================================================

# ---------- Parte 1 · Diccionarios ----------
ventas_bodega = [  # (fecha, categoria, monto en soles)
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

movimientos_junio = [  # (fecha, concepto, monto): + ingreso, - egreso, 0 ajuste
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

compras_mes = [  # (fecha, categoria, monto) compras a proveedores
    ("2026-07-01", "abarrotes", 242.50),
    ("2026-07-01", "limpieza", 58.90),
    ("2026-07-03", "bebidas", 365.40),
    ("2026-07-04", "abarrotes", 215.75),
    ("2026-07-06", "lácteos", 89.30),
    ("2026-07-08", "limpieza", 44.10),
    ("2026-07-09", "bebidas", 98.60),
    ("2026-07-11", "abarrotes", 187.20),
    ("2026-07-12", "lácteos", 76.90),
    ("2026-07-14", "snacks", 63.15),
    ("2026-07-15", "abarrotes", 110.00),
    ("2026-07-15", "limpieza", 39.95),
]

# ---------- Parte 2 · Estado acumulativo ----------
saldo_inicial_caja = 250.0
movimientos_caja = [
    ("2026-06-01", "proveedor", -180.50),
    ("2026-06-02", "ventas del día", 95.20),
    ("2026-06-03", "ajuste", 0.0),
    ("2026-06-04", "luz", -64.30),
    ("2026-06-05", "ventas del día", 132.75),
    ("2026-06-06", "agua", -28.10),
    ("2026-06-07", "proveedor", -90.00),
    ("2026-06-08", "ventas del día", 210.40),
]

saldo_inicial_cuenta = 150.0
movimientos_cuenta = [
    ("2026-07-01", "proveedor", -90.00),
    ("2026-07-02", "ventas", 45.50),
    ("2026-07-03", "alquiler", -180.00),
    ("2026-07-04", "ajuste", 0.00),
    ("2026-07-05", "ventas", 120.00),
    ("2026-07-06", "luz", -62.30),
    ("2026-07-07", "ventas", 38.40),
    ("2026-07-08", "agua", -15.20),
]

saldo_inicial_ahorro = 500.0
movimientos_ahorro = [
    ("2026-07-01", "proveedor", -120.00),
    ("2026-07-02", "ventas", 85.50),
    ("2026-07-03", "agua", -31.20),
    ("2026-07-04", "luz", -58.90),
    ("2026-07-05", "ventas", 60.00),
    ("2026-07-06", "proveedor", -140.25),
]

saldo_inicial_agosto = 400.0
movimientos_agosto = [
    ("2026-08-01", "proveedor", -150.00),
    ("2026-08-02", "ventas", 80.00),
    ("2026-08-03", "luz", -95.50),
    ("2026-08-04", "ventas", 120.30),
    ("2026-08-05", "alquiler", -200.00),
    ("2026-08-06", "ajuste", 0.00),
    ("2026-08-07", "ventas", 99.00),
    ("2026-08-08", "agua", -44.10),
]

stock_inicial = 40      # unidades de aceite de 1 L
stock_minimo = 15
kardex = [  # (fecha, tipo, cantidad)
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

# ---------- Parte 3 · Tuplas y key ----------
lista_prueba = [
    ("2026-05-01", 30.0), ("2026-04-20", 90.0), ("2026-05-01", 25.0),
    ("2026-04-27", 15.5), ("2026-05-09", 12.0), ("2026-04-20", 40.0),
]

movimientos_abril = [
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

fechas_semana = ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09", "2026-10-10", "2026-10-11"]
ventas_dia = [412.50, 388.00, 455.20, 455.20, 301.75, 520.60, 520.60]
clientes_dia = [96, 90, 101, 88, 70, 115, 104]

locales = ["Centro", "Mercado", "Paradero"]
meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio"]
ventas_mensuales = [  # filas: locales; columnas: meses
    [4200, 3980, 4510, 4510, 4105, 3890],
    [5120, 4870, 5340, 5010, 5490, 5230],
    [2890, 3150, 2760, 3320, 3040, 3320],
]

# ---------- Reto final y nivel pro ----------
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

# Copia privada: los verificadores no dependen de lo que cambies arriba.
_D = copy.deepcopy({k: globals()[k] for k in [
    "ventas_bodega", "movimientos_junio", "compras_mes",
    "saldo_inicial_caja", "movimientos_caja", "saldo_inicial_cuenta", "movimientos_cuenta",
    "saldo_inicial_ahorro", "movimientos_ahorro", "saldo_inicial_agosto", "movimientos_agosto",
    "stock_inicial", "stock_minimo", "kardex",
    "lista_prueba", "movimientos_abril", "fechas_semana", "ventas_dia", "clientes_dia",
    "locales", "meses", "ventas_mensuales", "saldo_inicial", "movimientos",
]})

# ======================================================================
# Herramientas de verificación
# ======================================================================
_FALTA = object()


def _igual(a, b, tol=0.0051):
    """Compara exigiendo el mismo tipo en None/bool/str y tolerancia en decimales."""
    if b is None or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(b, (int, float)):
        return isinstance(a, (int, float)) and not isinstance(a, bool) and abs(a - b) <= tol
    if isinstance(b, (list, tuple)):
        return (type(a) is type(b) and len(a) == len(b)
                and all(_igual(x, y, tol) for x, y in zip(a, b)))
    if isinstance(b, dict):
        return isinstance(a, dict) and set(a) == set(b) and all(_igual(a[k], b[k], tol) for k in b)
    return type(a) is type(b) and a == b


def _redondeado(valor):
    """True si ningún decimal de `valor` tiene más de 2 cifras."""
    if isinstance(valor, float):
        return round(valor, 2) == valor
    if isinstance(valor, dict):
        return all(_redondeado(v) for v in valor.values())
    if isinstance(valor, (list, tuple)):
        return all(_redondeado(v) for v in valor)
    return True


def _corto(valor, n=70):
    texto = repr(valor)
    return texto if len(texto) <= n else texto[:n] + "…"


def _saldos(inicial, movs):
    """Saldo después de cada movimiento."""
    resultado = []
    for i in range(len(movs)):
        resultado.append(inicial + math.fsum(m[2] for m in movs[:i + 1]))
    return resultado


class _Revision:
    def __init__(self, titulo):
        self.titulo = titulo
        self.errores = 0
        print(f"── {titulo} ──")

    def ok(self, msg):
        print(f"✅ {msg}")

    def mal(self, msg):
        self.errores += 1
        print(f"❌ {msg}")

    def var(self, nombre, tipo=None):
        valor = globals().get(nombre, _FALTA)
        if valor is _FALTA:
            self.mal(f"No encuentro `{nombre}`. ¿Ejecutaste tu celda? ¿Escribiste bien el nombre?")
            return _FALTA
        if tipo is not None and type(valor) is not tipo:
            self.mal(f"`{nombre}` es de tipo {type(valor).__name__} y se esperaba {tipo.__name__}.")
            return _FALTA
        return valor

    def valor(self, nombre, esperado, tipo=None, pista="revisa el cálculo", trampas=(), reglas=(),
              redondeo=False):
        """Compara sin mostrar el valor esperado. `trampas`: (valor_de_un_error_típico, mensaje).
        `reglas`: (función que detecta un error típico, mensaje)."""
        v = self.var(nombre, tipo)
        if v is _FALTA:
            return
        if _igual(v, esperado):
            if redondeo and not _redondeado(v):
                self.mal(f"`{nombre}` tiene el valor correcto, pero sin redondear: usa round(..., 2) al entregar el resultado.")
            else:
                self.ok(f"`{nombre}` es correcto.")
            return
        for regla, mensaje in reglas:
            try:
                activa = regla(v)
            except Exception:
                activa = False
            if activa:
                self.mal(f"`{nombre}`: {mensaje}")
                return
        for trampa, mensaje in trampas:
            if _igual(v, trampa):
                self.mal(f"`{nombre}` vale {_corto(v)}: {mensaje}")
                return
        self.mal(f"`{nombre}` vale {_corto(v)}; {pista}.")

    def prediccion(self, nombre, esperado):
        v = self.var(nombre)
        if v is _FALTA:
            return
        normal = v.strip().lower() if isinstance(v, str) else v
        objetivo = esperado.strip().lower() if isinstance(esperado, str) else esperado
        if _igual(normal, objetivo, tol=1e-9):
            self.ok(f"`{nombre}` es correcto.")
        else:
            self.mal(f"`{nombre}` no es correcto. Razónalo otra vez y luego compruébalo ejecutando la expresión en una celda nueva.")

    def fin(self):
        if self.errores == 0:
            print(f"🎉 ¡{self.titulo} superado!")
        else:
            cuantos = "el punto marcado" if self.errores == 1 else f"los {self.errores} puntos marcados"
            print(f"🔁 Corrige {cuantos} con ❌ y vuelve a verificar.")


def _sin_cambios(r, nombre):
    if globals().get(nombre) != _D[nombre]:
        r.mal(f"`{nombre}` cambió. No debes modificar los datos originales: vuelve a ejecutar el setup y revisa tu código.")


def _por_clave(registros, i_clave, valor):
    """Diccionario clave -> lista de valores, en orden de aparición."""
    grupos = {}
    for reg in registros:
        grupos.setdefault(reg[i_clave], []).append(valor(reg))
    return grupos


# ---------------------------- Parte 1 ----------------------------
def check_ejercicio_1():
    r = _Revision("Ejercicio 1 · Parte A")
    grupos = _por_clave(_D["ventas_bodega"], 1, lambda v: v[2])
    esperado = {c: len(ms) for c, ms in grupos.items()}
    r.valor("conteo_por_categoria", esperado, dict, "cada venta suma 1 a su categoría",
            reglas=[(lambda d: any(type(x) is not int for x in d.values()),
                     "hay valores con decimales: eso es un total en soles, no un conteo. Suma 1 por venta, no el monto.")],
            trampas=[({c: n - 1 for c, n in esperado.items()},
                      "a cada categoría le falta 1. ¿Inicializaste en 0 dentro del `else`? La primera venta también cuenta.")])
    _sin_cambios(r, "ventas_bodega")
    r.fin()

    r = _Revision("Ejercicio 1 · Parte B")
    r.prediccion("pred_in_cero", "azúcar" in {"azúcar": 0})
    r.prediccion("pred_in_valor", 12 in {"arroz": 12})
    try:
        {"arroz": 12}["Arroz"]
        error = "ninguno"
    except Exception as e:
        error = type(e).__name__
    r.prediccion("pred_error", error)
    r.fin()


def check_ejercicio_2():
    r = _Revision("Ejercicio 2 · Parte A")
    grupos = _por_clave(_D["ventas_bodega"], 1, lambda v: v[2])
    esperado = {c: round(math.fsum(ms), 2) for c, ms in grupos.items()}
    sin_primero = {c: round(math.fsum(ms[1:]), 2) for c, ms in grupos.items()}
    r.valor("total_por_categoria", esperado, dict, "suma todos los montos de cada categoría",
            trampas=[(sin_primero, "a cada categoría le falta su primer monto: ¿la inicializaste en 0 en vez de acumular desde la primera venta?")],
            redondeo=True)
    _sin_cambios(r, "ventas_bodega")
    r.fin()

    r = _Revision("Ejercicio 2 · Parte B")
    r.prediccion("pred_igual", 0.1 + 0.2 == 0.3)
    r.prediccion("pred_redondeado", round(0.1 + 0.2, 2) == 0.3)
    try:
        {"lunes": 120.0}.get("martes") + 50
        error = "ninguno"
    except Exception as e:
        error = type(e).__name__
    r.prediccion("pred_error_get", error)
    r.fin()


def check_ejercicio_3():
    r = _Revision("Ejercicio 3")
    movs = _D["movimientos_junio"]
    grupos = _por_clave([m for m in movs if m[2] < 0], 1, lambda m: -m[2])
    esperado = {c: round(math.fsum(ms), 2) for c, ms in grupos.items()}
    ingresos = {m[1] for m in movs if m[2] > 0}
    ceros = {m[1] for m in movs if m[2] == 0}
    r.valor("egresos_por_concepto", esperado, dict, "suma, en positivo, los egresos de cada concepto",
            reglas=[(lambda g: bool(ingresos & set(g)),
                     "tiene conceptos de ingresos: el filtro `monto != 0` deja pasar los ingresos. Solo cuentan los montos negativos."),
                    (lambda g: bool(ceros & set(g)),
                     "tiene un concepto que solo tuvo montos 0: aquí sí hay que filtrarlo, o crea una clave que no debería existir."),
                    (lambda g: any(x < 0 for x in g.values()),
                     "hay gastos negativos: guárdalos en positivo (suma `-monto`).")],
            redondeo=True)
    _sin_cambios(r, "movimientos_junio")
    r.fin()


def check_ejercicio_4():
    r = _Revision("Ejercicio 4")
    grupos = _por_clave(_D["compras_mes"], 1, lambda m: m[2])
    totales = {c: math.fsum(ms) for c, ms in grupos.items()}
    r.valor("compras_total", {c: round(t, 2) for c, t in totales.items()}, dict,
            "suma los montos de cada categoría", redondeo=True,
            trampas=[({c: round(math.fsum(ms[1:]), 2) for c, ms in grupos.items()},
                      "a cada categoría le falta su primera compra.")])
    r.valor("compras_cantidad", {c: len(ms) for c, ms in grupos.items()}, dict,
            "cuenta 1 por compra (no sumes el monto)")
    r.valor("compras_promedio", {c: round(totales[c] / len(ms), 2) for c, ms in grupos.items()}, dict,
            "promedio = total / cantidad de la categoría", redondeo=True)
    mayor_suelta = sorted(_D["compras_mes"], key=lambda m: -m[2])[0][1]
    r.valor("categoria_mas_compras", sorted(totales, key=lambda c: -totales[c])[0], str,
            "debería ser la categoría con mayor TOTAL",
            trampas=[(mayor_suelta, "es la categoría de la compra suelta más grande; compara los TOTALES por categoría."),
                     (sorted(totales, key=lambda c: totales[c])[0], "es la categoría con MENOR total: revisa la comparación.")])
    _sin_cambios(r, "compras_mes")
    r.fin()


# ---------------------------- Parte 2 ----------------------------
def check_ejercicio_5():
    r = _Revision("Ejercicio 5")
    movs = _D["movimientos_caja"]
    saldos = _saldos(_D["saldo_inicial_caja"], movs)
    r.valor("saldos_caja", [round(s, 2) for s in saldos], list, "cada saldo es el anterior más el monto del día",
            reglas=[(lambda v: len(v) != len(movs),
                     f"debe tener un saldo por movimiento ({len(movs)}). ¿Saltaste el monto 0? Sumar 0 no cambia el saldo, pero ese día existe.")],
            trampas=[([round(s, 2) for s in _saldos(0, movs)],
                      "¿arrancaste el saldo en 0? Debe arrancar en `saldo_inicial_caja`.")],
            redondeo=True)
    r.valor("saldo_cierre", round(saldos[-1], 2), float, "debería ser el último saldo",
            trampas=[(round(saldos[-1] - _D["saldo_inicial_caja"], 2), "falta el saldo inicial.")], redondeo=True)
    _sin_cambios(r, "movimientos_caja")
    r.fin()


def check_ejercicio_6():
    r = _Revision("Ejercicio 6")
    movs = _D["movimientos_cuenta"]
    saldos = _saldos(_D["saldo_inicial_cuenta"], movs)
    rojos = [m[0] for m, s in zip(movs, saldos) if s < 0]
    anteriores = [_D["saldo_inicial_cuenta"]] + saldos[:-1]
    desde_cero = [m[0] for m, s in zip(movs, _saldos(0, movs)) if s < 0]
    r.valor("primer_rojo", rojos[0], str, "debería ser la fecha del primer saldo menor que 0",
            trampas=[(rojos[-1], "es el ÚLTIMO día en rojo: ¿te falta el `break`?"),
                     (desde_cero[0], "¿arrancaste el saldo en 0 en vez de en `saldo_inicial_cuenta`?")])
    r.valor("dias_en_rojo", rojos, list, "deberían ser todas las fechas con saldo menor que 0, en orden",
            trampas=[([m[0] for m, s in zip(movs, saldos) if s < 0 and m[2] != 0],
                      "falta un día: ¿un `continue` con el monto 0 se saltó el chequeo? Ese día el saldo seguía en rojo.")])
    r.valor("entradas_en_rojo", sum(1 for a, s in zip(anteriores, saldos) if a >= 0 > s), int,
            "cuenta las veces que el saldo PASA de >= 0 a < 0",
            trampas=[(len(rojos), "eso es la cantidad de días en rojo, no de entradas: compara con el saldo anterior.")])
    ahorro = [m[0] for m, s in zip(_D["movimientos_ahorro"], _saldos(_D["saldo_inicial_ahorro"], _D["movimientos_ahorro"])) if s < 0]
    r.valor("primer_rojo_ahorro", ahorro[0] if ahorro else None, None,
            "esta cuenta nunca queda en rojo: debe quedar en `None` (no en 0, \"\" ni una fecha)")
    _sin_cambios(r, "movimientos_cuenta")
    _sin_cambios(r, "movimientos_ahorro")
    r.fin()


def check_ejercicio_7():
    r = _Revision("Ejercicio 7 · Parte A")
    movs = _D["movimientos_agosto"]
    saldos = _saldos(_D["saldo_inicial_agosto"], movs)
    minimo = sorted(saldos)[0]
    fechas_min = [m[0] for m, s in zip(movs, saldos) if s == minimo]
    r.valor("saldo_minimo", round(minimo, 2), None, "debería ser el menor saldo tras un movimiento",
            trampas=[(0, "todos los saldos son positivos, así que el 0 inicial «gana» y nunca se reemplaza. Usa `None` como centinela.")],
            redondeo=True)
    r.valor("fecha_saldo_minimo", fechas_min[0], None, "debería ser la fecha del saldo mínimo",
            trampas=[(None, "nunca se actualizó: con el mínimo inicializado en 0 ningún saldo lo supera. Usa `None` como centinela."),
                     (fechas_min[-1], "hay un empate y te quedaste con el último: usa `<` (no `<=`) para conservar el primero.")])
    _sin_cambios(r, "movimientos_agosto")
    r.fin()

    r = _Revision("Ejercicio 7 · Parte B")
    precios = [("Proveedor A", 12.5), ("Proveedor B", 11.9), ("Proveedor C", 11.9), ("Proveedor D", 13.0)]
    for nombre, estricto in (("pred_con_menor", True), ("pred_con_menor_igual", False)):
        mejor = None
        for p in precios:
            if mejor is None or (p[1] < mejor[1] if estricto else p[1] <= mejor[1]):
                mejor = p
        r.prediccion(nombre, mejor[0])
    r.fin()


def check_ejercicio_8():
    r = _Revision("Ejercicio 8")
    minimo = _D["stock_minimo"]
    stocks = [_D["stock_inicial"]]
    for _, tipo, cant in _D["kardex"]:
        stocks.append(stocks[-1] + (cant if tipo == "entrada" else -cant))
    despues = stocks[1:]
    fechas = [m[0] for m in _D["kardex"]]
    r.valor("stock_final", stocks[-1], int, "las entradas suman y las salidas restan, desde `stock_inicial`")
    r.valor("fechas_bajo_minimo", [f for f, s in zip(fechas, despues) if s < minimo], list,
            "compara el stock DESPUÉS de cada movimiento con `stock_minimo`")
    recuperacion = [f for f, a, s in zip(fechas, stocks, despues) if a < minimo < s]
    r.valor("fecha_recuperacion", recuperacion[0] if recuperacion else None, None,
            "es la primera vez que el stock pasa de estar bajo el mínimo a superarlo",
            trampas=[([f for f, s in zip(fechas, despues) if s > minimo][0],
                      "ese día el stock supera el mínimo, pero no venía de estar bajo: necesitas el stock anterior.")])
    salidas = [m for m in _D["kardex"] if m[1] == "salida"]
    tope = sorted(m[2] for m in salidas)[-1]
    empatadas = [m for m in salidas if m[2] == tope]
    r.valor("mayor_salida", empatadas[0], tuple, "debería ser la tupla completa de la mayor salida",
            trampas=[(sorted(_D["kardex"], key=lambda m: m[2])[-1], "es una ENTRADA: busca solo entre las salidas."),
                     (empatadas[-1], "hay un empate y te quedaste con la última: usa `>` (no `>=`).")])
    _sin_cambios(r, "kardex")
    r.fin()


# ---------------------------- Parte 3 ----------------------------
def check_ejercicio_9():
    r = _Revision("Ejercicio 9")
    r.prediccion("pred_a", ("2026-11-03", 10) < ("2026-11-03", 9))
    r.prediccion("pred_b", ("b", 1) < ("a", 99))
    r.prediccion("pred_c", (1, 500) < (1, 1000))
    r.prediccion("pred_d", ("2026-10-5", 0) < ("2026-10-15", 0))
    r.prediccion("pred_e", "100" < "25")
    r.prediccion("pred_f", (7, 3) < (7, 3, 0))
    r.prediccion("pred_min", min(_D["lista_prueba"]))
    r.fin()


def check_ejercicio_10():
    r = _Revision("Ejercicio 10")
    movs = _D["movimientos_abril"]
    por_monto = sorted(movs, key=lambda m: m[2])
    egresos = [m for m in por_monto if m[2] < 0]
    r.valor("mayor_ingreso", por_monto[-1], tuple, "debería ser el movimiento con el monto más alto",
            trampas=[(max(movs), "es el movimiento más RECIENTE: `max` sin `key` compara por la fecha.")])
    r.valor("mayor_egreso_abril", por_monto[0], tuple, "debería ser el movimiento con el monto más bajo",
            trampas=[(min(movs), "es el movimiento más ANTIGUO: `min` sin `key` compara por la fecha.")])
    solo_egresos = [m for m in movs if m[2] < 0]
    r.valor("top3_egresos", egresos[:3], list, "deberían ser los 3 egresos más grandes, del más negativo al menos negativo",
            trampas=[(sorted(solo_egresos, reverse=True)[:3], "están ordenados por FECHA: `sorted` sin `key` compara la tupla completa."),
                     (sorted(solo_egresos, key=lambda m: m[2], reverse=True)[:3],
                      "con `reverse=True` los negativos quedan al revés: primero el egreso más pequeño.")])
    _sin_cambios(r, "movimientos_abril")
    r.fin()


def check_ejercicio_11():
    r = _Revision("Ejercicio 11")
    f, v, c = _D["fechas_semana"], _D["ventas_dia"], _D["clientes_dia"]
    registros = [(i + 1, f[i], v[i], c[i]) for i in range(len(f))]
    ranking = sorted(registros, key=lambda t: (-t[2], t[3]))
    r.valor("venta_por_fecha", {f[i]: v[i] for i in range(len(f))}, dict, "cada fecha debería apuntar a su venta")
    r.valor("ranking", ranking, list, "ordena por venta de mayor a menor y, si empatan, menos clientes primero",
            reglas=[(lambda x: sorted(t[0] for t in x) == list(range(len(f))),
                     "los números de día empiezan en 0: usa `enumerate(..., start=1)`.")],
            trampas=[(sorted(registros, key=lambda t: -t[2]), "falta el desempate: si la venta empata, va primero el de menos clientes."),
                     (sorted(registros, key=lambda t: (-t[2], -t[3])), "el desempate está invertido: menos clientes va primero.")])
    r.valor("dia_ganador", ranking[0][0], int, "debería ser el número de día (1 a 7) del primer lugar",
            trampas=[(ranking[1][0], "¿aplicaste el desempate por clientes? ¿empezaste a contar en 1?")])
    r.valor("fecha_ganadora", ranking[0][1], str, "debería ser la fecha del primer lugar del ranking")
    for nombre in ("fechas_semana", "ventas_dia", "clientes_dia"):
        _sin_cambios(r, nombre)
    r.fin()


def check_ejercicio_12():
    r = _Revision("Ejercicio 12")
    tabla = _D["ventas_mensuales"]
    totales = {loc: sum(fila) for loc, fila in zip(_D["locales"], tabla)}
    primero, ultimo, base_cero = {}, {}, {}
    for loc, fila in zip(_D["locales"], tabla):
        posiciones = [j for j in range(len(fila)) if fila[j] == sorted(fila)[-1]]
        primero[loc] = posiciones[0] + 1
        ultimo[loc] = posiciones[-1] + 1
        base_cero[loc] = posiciones[0]
    r.valor("total_por_local", totales, dict, "cada local debería apuntar a la suma de su fila")
    r.valor("mejor_mes_por_local", primero, dict, "cada local debería apuntar al número de mes (1 a 6) de su mayor venta",
            trampas=[(ultimo, "en los empates te quedaste con el último mes: usa `>` (no `>=`), o `.index()`, que da el primero."),
                     (base_cero, "los meses van del 1 al 6: a la posición súmale 1.")])
    r.valor("local_top", sorted(totales, key=lambda k: -totales[k])[0], str, "debería ser el local con mayor venta total")
    _sin_cambios(r, "ventas_mensuales")
    r.fin()


# ------------------------- Reto y nivel pro -------------------------
def _reto_esperado():
    si, movs = _D["saldo_inicial"], _D["movimientos"]
    saldos = _saldos(si, movs)
    anteriores = [si] + saldos[:-1]
    grupos = _por_clave([m for m in movs if m[2] < 0], 1, lambda m: -m[2])
    gasto = {c: round(math.fsum(ms), 2) for c, ms in grupos.items()}
    return movs, saldos, anteriores, gasto


def check_reto(parte="A"):
    r = _Revision(f"Reto final · Parte {parte}")
    si = _D["saldo_inicial"]
    movs, saldos, anteriores, gasto = _reto_esperado()
    montos = [m[2] for m in movs]
    r.valor("saldo_final", round(saldos[-1], 2), float, "debería ser el saldo inicial más todos los montos",
            trampas=[(round(math.fsum(montos), 2), "falta el saldo inicial: el saldo arranca en `saldo_inicial`, no en 0.")],
            redondeo=True)
    r.valor("n_ingresos", sum(1 for x in montos if x > 0), int, "cuenta solo los montos mayores que 0",
            trampas=[(sum(1 for x in montos if x >= 0), "¿contaste el monto 0 como ingreso? El ajuste no es ingreso ni egreso.")])
    r.valor("n_egresos", sum(1 for x in montos if x < 0), int, "cuenta solo los montos menores que 0",
            trampas=[(sum(1 for x in montos if x <= 0), "¿contaste el monto 0 como egreso? El ajuste no es ingreso ni egreso.")])
    ingresos_o_cero = {m[1] for m in movs if m[2] >= 0} - set(gasto)
    r.valor("gasto_por_concepto", gasto, dict, "algún total no coincide: suma, en positivo, todos los egresos de cada concepto",
            reglas=[(lambda g: bool(ingresos_o_cero & set(g)),
                     "tiene conceptos que no son egresos (ingresos o el ajuste de 0): solo cuentan los montos negativos."),
                    (lambda g: any(x < 0 for x in g.values()), "hay gastos negativos: guárdalos en positivo."),
                    (lambda g: set(g) != set(gasto), "faltan conceptos: ¿incluiste los que tienen un solo egreso?")],
            redondeo=True)
    por_monto = sorted(movs, key=lambda m: m[2])
    empatados = [m for m in movs if m[2] == por_monto[0][2]]
    r.valor("mayor_egreso", por_monto[0], tuple, "debería ser la tupla completa del movimiento con el monto más negativo",
            trampas=[(min(movs), "es el movimiento más ANTIGUO: `min(movimientos)` sin `key` compara por la fecha."),
                     (empatados[-1], "hay un empate y te quedaste con el último: usa `<` (no `<=`) para conservar el primero.")])
    rojos = [m[0] for m, s in zip(movs, saldos) if s < 0]
    r.valor("dias_sobregiro", rojos, list, "deberían ser las fechas en que el saldo, tras el movimiento, quedó por debajo de 0",
            trampas=[([m[0] for m, s in zip(movs, saldos) if s < 0 and m[2] != 0],
                      "falta un día: ¿un `continue` con el monto 0 se saltó el chequeo? Ese día la cuenta seguía en sobregiro."),
                     ([m[0] for m, s in zip(movs, _saldos(0, movs)) if s < 0],
                      "¿arrancaste el saldo en 0? Debe arrancar en `saldo_inicial`.")])
    r.valor("veces_en_sobregiro", sum(1 for a, s in zip(anteriores, saldos) if a >= 0 > s), int,
            "cuenta las veces que el saldo PASA de >= 0 a < 0",
            trampas=[(len(rojos), "eso es la cantidad de días en sobregiro, no de entradas: compara con el saldo anterior.")])
    r.valor("primer_dia_sobregiro", rojos[0] if rojos else None, None, "debería ser la primera fecha con saldo menor que 0",
            trampas=[(rojos[-1] if rojos else None, "es el ÚLTIMO día en sobregiro: ¿te falta el `break` o la condición `is None`?")])
    mayor_suelto = por_monto[0][1]
    r.valor("concepto_mas_gasto", sorted(gasto, key=lambda c: -gasto[c])[0], str,
            "debería ser el concepto con mayor gasto TOTAL",
            trampas=[] if mayor_suelto == sorted(gasto, key=lambda c: -gasto[c])[0] else
            [(mayor_suelto, "es el concepto del egreso suelto más grande; compara los TOTALES.")])
    _sin_cambios(r, "movimientos")
    r.fin()


def check_pro():
    r = _Revision("Nivel pro")
    movs, saldos, _, gasto = _reto_esperado()
    r.valor("saldo_por_fecha", {m[0]: round(s, 2) for m, s in zip(movs, saldos)}, dict,
            "cada fecha debería apuntar al saldo que quedó tras su movimiento", redondeo=True)
    ranking = sorted(gasto.items(), key=lambda kv: (-kv[1], kv[0]))
    r.valor("ranking_conceptos", ranking, list, "deberían ser tuplas (concepto, gasto) de mayor a menor gasto",
            trampas=[(ranking[::-1], "está de menor a mayor: invierte el orden (signo menos en la `key` o `reverse=True`).")])
    racha = mejor = 0
    for s in saldos:
        racha = racha + 1 if s < 0 else 0
        mejor = mejor if mejor >= racha else racha
    r.valor("racha_mas_larga", mejor, int, "cuenta la mayor cantidad de movimientos SEGUIDOS con saldo en rojo",
            trampas=[(sum(1 for s in saldos if s < 0), "eso es el total de días en rojo; la racha son días seguidos (se reinicia al salir del rojo).")])
    _sin_cambios(r, "movimientos")
    r.fin()


print("✅ Setup listo. Datos cargados y verificadores activos.")
