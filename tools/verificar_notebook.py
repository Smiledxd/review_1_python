"""Verifica `sesiones/refuerzo_python_puro.ipynb`.

Uso (desde la raíz del repo):
    python3 tools/verificar_notebook.py

Criterios que comprueba:
 1. Estructura: nbformat 4 válido, kernel python3, sin outputs, solo biblioteca estándar.
 2. Con SOLUCIONES en lugar de plantillas: todo corre y todos los asserts pasan.
    Con PLANTILLAS sin resolver: la validación de cada ejercicio falla (ningún assert pasa gratis).
 3. Los valores esperados se recalculan de forma independiente (aquí sí: collections, itertools,
    statistics, heapq...) y coinciden con lo que producen las soluciones.
 4. Las trampas del reto final funcionan (min sin key, continue en montos 0, `<=` en el empate).
 5. Mutantes (errores típicos inyectados en las soluciones) son detectados por los asserts.
"""

import ast
import contextlib
import copy
import heapq
import io
import itertools
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import nbformat  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
RUTA = RAIZ / "sesiones" / "refuerzo_python_puro.ipynb"

resultados = []  # (criterio, ok, detalle)


def registrar(criterio, ok, detalle=""):
    resultados.append((criterio, ok, detalle))
    print(("✅" if ok else "❌"), criterio, ("— " + detalle) if detalle else "")


# ----------------------------------------------------------------------
# Utilidades de ejecución
# ----------------------------------------------------------------------
def ejecutar(src, ns, nombre="celda"):
    """Ejecuta `src` en `ns` capturando stdout. Devuelve el texto impreso."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src, nombre, "exec"), ns)
    return buf.getvalue()


def ns_nuevo():
    return {"__name__": "__main__"}


def es_ejercicio_plantilla(celda):
    return celda.id.startswith("ej-") and celda.id.endswith("-plantilla")


def ids_ejercicios(nb):
    return [c.id[3:-len("-plantilla")] for c in nb.cells if es_ejercicio_plantilla(c)]


def celda(nb, id):
    for c in nb.cells:
        if c.id == id:
            return c
    raise KeyError(id)


def usa_matplotlib(src):
    return "matplotlib" in src


# ----------------------------------------------------------------------
# Oráculos independientes: reciben el namespace (con los datos) y devuelven
# {variable: valor_esperado}. Usan herramientas que el notebook no usa.
# ----------------------------------------------------------------------
def r2(x):
    return round(x, 2)


def _acumular(saldo_inicial, movimientos):
    return list(itertools.accumulate((m[2] for m in movimientos), initial=saldo_inicial))[1:]


def o_1_1(ns):
    return {"conteo_por_categoria": dict(Counter(v[1] for v in ns["ventas"]))}


def o_1_2(ns):
    grupos = defaultdict(list)
    for _, cat, monto in ns["ventas_semana"]:
        grupos[cat].append(monto)
    return {"total_por_categoria": {c: r2(math.fsum(v)) for c, v in grupos.items()}}


def o_1_3(ns):
    grupos = defaultdict(list)
    for _, concepto, monto in ns["movimientos"]:
        if monto < 0:
            grupos[concepto].append(-monto)
    return {"gasto_por_concepto": {c: r2(math.fsum(v)) for c, v in grupos.items()}}


def o_1_4(ns):
    grupos = defaultdict(list)
    for _, cat, monto in ns["gastos"]:
        grupos[cat].append(monto)
    totales = {c: math.fsum(v) for c, v in grupos.items()}
    mejor = max(totales, key=totales.get)
    assert sorted(totales.values())[-1] != sorted(totales.values())[-2], "empate en el mayor gasto"
    return {
        "total_por_categoria": {c: r2(t) for c, t in totales.items()},
        "cantidad_por_categoria": {c: len(v) for c, v in grupos.items()},
        "promedio_por_categoria": {c: r2(statistics.fmean(v)) for c, v in grupos.items()},
        "categoria_mayor_gasto": mejor,
    }


def o_2_1(ns):
    saldos = _acumular(ns["saldo_inicial"], ns["movimientos"])
    return {"saldos": [r2(s) for s in saldos], "saldo_final": r2(saldos[-1])}


def _primer_negativo(saldo_inicial, movimientos):
    saldos = _acumular(saldo_inicial, movimientos)
    return next((m[0] for m, s in zip(movimientos, saldos) if s < 0), None)


def o_2_2(ns):
    return {
        "primer_dia_a": _primer_negativo(ns["saldo_inicial_a"], ns["movimientos_a"]),
        "primer_dia_b": _primer_negativo(ns["saldo_inicial_b"], ns["movimientos_b"]),
    }


def o_2_3(ns):
    saldos = _acumular(ns["saldo_inicial"], ns["movimientos"])
    i = min(range(len(saldos)), key=lambda k: saldos[k])      # primer índice del mínimo
    assert saldos.count(saldos[i]) == 2, "se esperaba un empate en el mínimo"
    return {"saldo_minimo": r2(saldos[i]), "fecha_saldo_minimo": ns["movimientos"][i][0]}


def o_2_4(ns):
    minimo = ns["stock_minimo"]
    kardex = ns["movimientos_kardex"]
    deltas = [c if t == "entrada" else -c for _, t, c in kardex]
    stocks = list(itertools.accumulate(deltas, initial=ns["stock_inicial"]))
    assert all(s != minimo for s in stocks), "el stock no debe caer exactamente en el mínimo"
    despues = stocks[1:]
    bajo = [m[0] for m, s in zip(kardex, despues) if s < minimo]
    recuperacion = next((m[0] for m, ant, s in zip(kardex, stocks, despues) if ant < minimo < s), None)
    salidas = [m for m in kardex if m[1] == "salida"]
    mayor = max(salidas, key=lambda m: m[2])                   # max devuelve el primero en empate
    assert sum(1 for m in salidas if m[2] == mayor[2]) > 1, "se esperaba empate en la mayor salida"
    return {"stock_final": stocks[-1], "fechas_bajo_minimo": bajo,
            "fecha_recuperacion": recuperacion, "mayor_salida": mayor}


def o_3_1(ns):
    exprs = {
        "pred_a": "('2026-11-03', 10) < ('2026-11-03', 9)",
        "pred_b": "('b', 1) < ('a', 99)",
        "pred_c": "(1, 500) < (1, 1000)",
        "pred_d": "('2026-10-5', 0) < ('2026-10-15', 0)",
        "pred_e": "'100' < '25'",
        "pred_f": "(7, 3) < (7, 3, 0)",
    }
    esperado = {k: eval(v) for k, v in exprs.items()}
    lp = ns["lista_prueba"]
    # mínimo por tupla: ordenar y tomar el primero
    esperado["pred_min"] = sorted(lp)[0]
    assert esperado["pred_min"] != min(lp, key=lambda t: t[1]), "min por fecha debe diferir del min por monto"
    return esperado


def o_3_2(ns):
    ordenados = sorted(ns["movimientos"], key=lambda m: m[2])
    assert ordenados[0] != min(ns["movimientos"]) and ordenados[-1] != max(ns["movimientos"])
    return {"mayor_ingreso": ordenados[-1], "mayor_egreso": ordenados[0]}


def o_3_3(ns):
    egresos = [m for m in ns["movimientos"] if m[2] < 0]
    esperado = heapq.nsmallest(3, egresos, key=lambda m: m[2])
    assert esperado != sorted(egresos)[:3]
    return {"top3_egresos": esperado}


def o_3_4(ns):
    f, v, c = ns["fechas"], ns["ventas"], ns["clientes"]
    orden = sorted(range(len(f)), key=lambda i: (-v[i], c[i]))
    ranking = [(i + 1, f[i], v[i], c[i]) for i in orden]
    ingenuo = max(range(len(v)), key=lambda i: v[i]) + 1       # el primero que alcanza el máximo
    assert ranking[0][0] != ingenuo, "el desempate debe cambiar al ganador"
    return {"ranking": ranking, "dia_ganador": ranking[0][0], "fecha_ganadora": ranking[0][1]}


def o_reto(ns):
    si, movs = ns["saldo_inicial"], ns["movimientos"]
    saldos = _acumular(si, movs)
    anteriores = [si] + saldos[:-1]
    gasto = defaultdict(list)
    for _, concepto, monto in movs:
        if monto < 0:
            gasto[concepto].append(-monto)
    totales = {c: math.fsum(v) for c, v in gasto.items()}
    egresos = [m for m in movs if m[2] < 0]
    valores = sorted(totales.values())
    assert valores[-1] != valores[-2], "no debe haber empate en el concepto con más gasto"
    return {
        "saldo_final": r2(si + math.fsum(m[2] for m in movs)),
        "n_ingresos": sum(1 for m in movs if m[2] > 0),
        "n_egresos": len(egresos),
        "gasto_por_concepto": {c: r2(t) for c, t in totales.items()},
        "mayor_egreso": min(egresos, key=lambda m: m[2]),
        "dias_sobregiro": sum(1 for s in saldos if s < 0),
        "veces_en_sobregiro": sum(1 for a, s in zip(anteriores, saldos) if a >= 0 and s < 0),
        "primer_dia_sobregiro": next((m[0] for m, s in zip(movs, saldos) if s < 0), None),
        "concepto_mas_gasto": max(totales, key=totales.get),
    }


ORACULOS = {
    "1-1": o_1_1, "1-2": o_1_2, "1-3": o_1_3, "1-4": o_1_4,
    "2-1": o_2_1, "2-2": o_2_2, "2-3": o_2_3, "2-4": o_2_4,
    "3-1": o_3_1, "3-2": o_3_2, "3-3": o_3_3, "3-4": o_3_4,
    "reto-a": o_reto, "reto-b": o_reto,
}
BUGS = {"1-3", "2-3", "3-3"}


def iguales(real, esperado):
    if isinstance(esperado, float) or isinstance(real, float):
        return isinstance(real, (int, float)) and r2(real) == r2(esperado) and \
            (not isinstance(esperado, float) or math.isclose(real, esperado, abs_tol=0.005))
    if isinstance(esperado, dict):
        return isinstance(real, dict) and real.keys() == esperado.keys() and \
            all(iguales(real[k], esperado[k]) for k in esperado)
    if isinstance(esperado, (list, tuple)):
        return type(real) is type(esperado) and len(real) == len(esperado) and \
            all(iguales(a, b) for a, b in zip(real, esperado))
    return real == esperado


# ----------------------------------------------------------------------
# Criterio 1: estructura
# ----------------------------------------------------------------------
def verificar_estructura(nb):
    nbformat.validate(nb)
    ok = nb.nbformat == 4 and nb.metadata["kernelspec"]["name"] == "python3"
    sin_outputs = all(
        c.cell_type != "code" or (not c.outputs and c.execution_count is None) for c in nb.cells
    )
    registrar("1a. nbformat 4 válido, kernel python3", ok, f"nbformat {nb.nbformat}.{nb.nbformat_minor}")
    registrar("1b. sin outputs guardados", sin_outputs)

    prohibidos = {"pandas", "numpy", "collections", "itertools"}
    permitidos = {"math", "matplotlib", "matplotlib.pyplot"}
    malos = []
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        for nodo in ast.walk(ast.parse(c.source)):
            nombres = []
            if isinstance(nodo, ast.Import):
                nombres = [a.name for a in nodo.names]
            elif isinstance(nodo, ast.ImportFrom):
                nombres = [nodo.module]
            for n in nombres:
                if n not in permitidos:
                    malos.append((c.id, n))
        if any(p in c.source for p in ("pandas", "numpy", "collections", "itertools")):
            malos.append((c.id, "menciona biblioteca prohibida"))
    registrar("1c. solo biblioteca estándar (+ matplotlib en el gráfico)", not malos, str(malos))

    texto = "\n".join(c.source for c in nb.cells).lower()
    texto_sin_auto = texto.replace("autoevaluación", "")      # «Checklist de autoevaluación» es parte del cierre pedido
    prohibidas = [p for p in ("pseint", "curso", "evaluación", "evaluacion", "examen", "profesor", "clase de")
                  if p in texto_sin_auto]
    registrar("1d. contenido sin referencias a cursos/evaluaciones/PSeInt", not prohibidas, str(prohibidas))
    registrar("1e. contenido en español con checklist y predicciones",
              texto.count("predice antes de ejecutar") >= 15, f"{texto.count('predice antes de ejecutar')} celdas de predicción")

    # formato de pistas y soluciones
    problemas = []
    for k in ids_ejercicios(nb):
        for c in nb.cells:
            if c.id.startswith(f"ej-{k}-pista-"):
                primera = c.source.splitlines()[0]
                if not re.fullmatch(r'# @title 💡 Pista \d \{ display-mode: "form" \}', primera):
                    problemas.append(c.id)
                arbol = ast.parse(c.source)
                if not all(isinstance(n, ast.Expr) for n in arbol.body):
                    problemas.append(c.id + " (no solo imprime)")
        sol = celda(nb, f"ej-{k}-solucion").source
        if not re.match(r'# @title 🔒 Solución .+ \(ábrela después de intentarlo\) \{ display-mode: "form" \}', sol):
            problemas.append(f"ej-{k}-solucion (título)")
        pistas = [c for c in nb.cells if c.id.startswith(f"ej-{k}-pista-")]
        if not 1 <= len(pistas) <= 2:
            problemas.append(f"ej-{k}: pistas={len(pistas)}")
        lineas = sol.split("# Error típico:\n")[1].split("\n\n")[0].splitlines()
        if not 2 <= len(lineas) <= 3:
            problemas.append(f"ej-{k}: {len(lineas)} líneas de error típico")
        val = ast.parse(celda(nb, f"ej-{k}-validacion").source)
        if any(isinstance(n, ast.Assert) and n.msg is None for n in val.body):
            problemas.append(f"ej-{k}: assert sin mensaje")
    registrar("1f. pistas (1-2, form, solo imprimen), soluciones (form, 2-3 líneas de error) y asserts con mensaje",
              not problemas, str(problemas))


# ----------------------------------------------------------------------
# Criterio 2 y 3: ejecución con soluciones (y oráculos)
# ----------------------------------------------------------------------
def correr_notebook_soluciones(nb, matplotlib_ok):
    ns = ns_nuevo()
    fallos, validaciones, omitidas = [], 0, []
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        if c.id.endswith("-solucion") or "-pista-" in c.id:
            # se ejecutan aparte; las pistas solo imprimen
            if "-pista-" in c.id:
                ejecutar(c.source, ns_nuevo(), c.id)
            continue
        if es_ejercicio_plantilla(c):
            k = c.id[3:-len("-plantilla")]
            src = celda(nb, f"ej-{k}-solucion").source
            local = ns_nuevo()                       # cada ejercicio en un namespace vacío
            try:
                ejecutar(src, local, f"ej-{k}-solucion")
                esperado = ORACULOS[k](local)
                for var, valor in esperado.items():
                    if not iguales(local.get(var), valor):
                        fallos.append(f"{k}: {var} = {local.get(var)!r} ≠ oráculo {valor!r}")
                salida = ejecutar(celda(nb, f"ej-{k}-validacion").source, local, f"ej-{k}-validacion")
                assert "✅" in salida
                validaciones += 1
            except Exception as e:  # noqa: BLE001
                fallos.append(f"{k}: {type(e).__name__}: {e}")
            continue
        if c.id.endswith("-validacion"):
            continue                                   # ya corrida junto con su ejercicio
        if usa_matplotlib(c.source) and not matplotlib_ok:
            omitidas.append(c.id)
            continue
        try:
            ejecutar(c.source, ns, c.id)
        except Exception as e:  # noqa: BLE001
            fallos.append(f"{c.id}: {type(e).__name__}: {e}")
    return fallos, validaciones, omitidas


def verificar_soluciones(nb):
    try:
        import matplotlib  # noqa: F401
        matplotlib_ok = True
    except ImportError:
        matplotlib_ok = False
    fallos, validaciones, omitidas = correr_notebook_soluciones(nb, matplotlib_ok)
    registrar("2a. con soluciones: todas las celdas corren y los asserts pasan",
              not fallos and validaciones == len(ids_ejercicios(nb)),
              f"{validaciones} validaciones OK" + (f"; omitidas (sin matplotlib): {omitidas}" if omitidas else "")
              + (f"; FALLOS: {fallos}" if fallos else ""))
    registrar("3.  valores esperados recalculados de forma independiente coinciden",
              not any("oráculo" in f for f in fallos), f"{len(ORACULOS)} oráculos")


def verificar_soluciones_standalone(nb):
    """Cada celda de solución también corre sola y es coherente con su validación (incluye el reto)."""
    malos = []
    for k in ids_ejercicios(nb):
        ns = ns_nuevo()
        try:
            ejecutar(celda(nb, f"ej-{k}-solucion").source, ns)
        except Exception as e:  # noqa: BLE001
            malos.append((k, str(e)))
    registrar("2b. cada celda de solución corre por sí sola", not malos, str(malos))


# ----------------------------------------------------------------------
# Criterio 2 (plantillas): ningún assert pasa gratis
# ----------------------------------------------------------------------
def verificar_plantillas(nb):
    malos = []
    total_asserts = 0
    for k in ids_ejercicios(nb):
        ns = ns_nuevo()
        ejecutar(celda(nb, f"ej-{k}-plantilla").source, ns, f"ej-{k}-plantilla")
        val_src = celda(nb, f"ej-{k}-validacion").source
        # 1) la validación completa debe fallar con AssertionError
        try:
            ejecutar(val_src, copy.copy(ns))
            malos.append(f"{k}: la validación pasó con la plantilla")
            continue
        except AssertionError:
            pass
        except Exception as e:  # noqa: BLE001
            malos.append(f"{k}: falló con {type(e).__name__} en vez de AssertionError")
            continue
        # 2) ningún assert individual pasa gratis (salvo el de integridad de datos y, en los bugs, ninguno)
        arbol = ast.parse(val_src)
        base = copy.copy(ns)
        def con_assert(n):
            return any(isinstance(x, ast.Assert) for x in ast.walk(n))

        for nodo in arbol.body:
            if not con_assert(nodo) and not isinstance(nodo, ast.Expr):
                exec(compile(ast.Module([nodo], []), "val", "exec"), base)
        for nodo in arbol.body:
            if not con_assert(nodo):
                continue
            total_asserts += 1
            interno = next(x for x in ast.walk(nodo) if isinstance(x, ast.Assert))
            mensaje = ast.unparse(interno.msg)
            integridad = "modificaste" in mensaje
            try:
                exec(compile(ast.Module([nodo], []), "val", "exec"), copy.copy(base))
                pasa = True
            except Exception:  # noqa: BLE001
                pasa = False
            if pasa and not integridad and k not in BUGS:
                malos.append(f"{k}: pasa gratis → {mensaje[:70]}")
    registrar("2c. con plantillas sin resolver, la validación de cada ejercicio falla y ningún assert pasa gratis",
              not malos, f"{total_asserts} asserts revisados" + (f"; {malos}" if malos else ""))


# ----------------------------------------------------------------------
# Criterio 4: trampas del reto final
# ----------------------------------------------------------------------
def verificar_trampas(nb):
    ns = ns_nuevo()
    ejecutar(celda(nb, "ej-reto-a-solucion").source, ns)
    si, movs = ns["saldo_inicial"], ns["movimientos"]
    esperado = o_reto(ns)
    detalles = []

    # a) min(movimientos) sin key
    ingenuo = min(movs)
    a = ingenuo != esperado["mayor_egreso"]
    detalles.append(f"min sin key → {ingenuo}")

    # b) continue en montos 0 antes del chequeo de sobregiro
    saldo, dias = si, 0
    for fecha, concepto, monto in movs:
        if monto == 0:
            continue
        saldo += monto
        if saldo < 0:
            dias += 1
    b = dias != esperado["dias_sobregiro"]
    detalles.append(f"con continue dias={dias} (correcto {esperado['dias_sobregiro']})")

    # c) `<=` en lugar de `<`
    mejor = None
    for m in movs:
        if m[2] < 0 and (mejor is None or m[2] <= mejor[2]):
            mejor = m
    c = mejor != esperado["mayor_egreso"]
    detalles.append(f"con <= → {mejor}")

    registrar("4a. min(movimientos) sin key da un resultado distinto", a, detalles[0])
    registrar("4b. `continue` en montos 0 antes del chequeo cambia dias_sobregiro", b, detalles[1])
    registrar("4c. `<=` en vez de `<` cambia mayor_egreso", c, detalles[2])

    # otras trampas declaradas
    saldos = _acumular(si, movs)
    egresos = [m for m in movs if m[2] < 0]
    conteo_concepto = Counter(m[1] for m in egresos)
    fechas = [m[0] for m in movs]
    checks = {
        "14-18 movimientos": 14 <= len(movs) <= 18,
        "saldo inicial positivo": si > 0,
        "fechas únicas y ordenadas": fechas == sorted(set(fechas)),
        "ajuste de 0 dentro de un día en sobregiro": any(m[2] == 0 and s < 0 for m, s in zip(movs, saldos)),
        "empate en el mayor egreso": sum(1 for m in egresos if m[2] == esperado["mayor_egreso"][2]) >= 2,
        "la fecha más antigua NO es el mayor egreso": min(movs)[0] != esperado["mayor_egreso"][0],
        "concepto con un solo movimiento": 1 in conteo_concepto.values(),
        "dos entradas distintas en sobregiro": esperado["veces_en_sobregiro"] == 2,
    }
    registrar("4d. el dataset activa todas las trampas pedidas", all(checks.values()),
              ", ".join(k for k, v in checks.items() if not v) or "todas activas")


# ----------------------------------------------------------------------
# Reto Parte B: un solo for
# ----------------------------------------------------------------------
def verificar_un_solo_for(nb):
    arbol = ast.parse(celda(nb, "ej-reto-b-solucion").source)
    sobre_movs = [n for n in ast.walk(arbol) if isinstance(n, ast.For)
                  and isinstance(n.iter, ast.Name) and n.iter.id == "movimientos"]
    registrar("2d. la solución de la Parte B recorre `movimientos` con un único for", len(sobre_movs) == 1,
              f"{len(sobre_movs)} for sobre movimientos")


# ----------------------------------------------------------------------
# Mutantes: errores típicos inyectados en las soluciones
# ----------------------------------------------------------------------
MUTANTES = [
    ("1-1", "conteo_por_categoria[categoria] = 1", "conteo_por_categoria[categoria] = 0", "inicializar el conteo en 0"),
    ("1-2", "round(total_por_categoria[categoria], 2)", "total_por_categoria[categoria]", "no redondear"),
    ("1-2", "total_por_categoria.get(categoria, 0) + monto", "monto", "no acumular"),
    ("1-3", "if monto < 0:", "if monto != 0:", "filtrar != 0 en vez de < 0"),
    ("1-3", ".get(concepto, 0) - monto", ".get(concepto, 0) + monto", "no invertir el signo"),
    ("1-4", "total > mayor_total", "total < mayor_total", "mínimo en vez de máximo"),
    ("1-4", "round(total / cantidad_por_categoria[categoria], 2)", "total / cantidad_por_categoria[categoria]", "promedio sin redondear"),
    ("2-1", "saldo = saldo_inicial            #", "saldo = 0            #", "arrancar el saldo en 0"),
    ("2-1", "saldos.append(round(saldo, 2))", "saldos.append(saldo)", "no redondear los saldos"),
    ("2-2", "break", "pass", "sin break (queda el último día)"),
    ("2-3", "saldo_minimo = None      ", "saldo_minimo = 0         ", "mínimo inicializado en 0"),
    ("2-3", "saldo < saldo_minimo:", "saldo <= saldo_minimo:", "<= (último empate)"),
    ("2-4", "cantidad > mayor_salida[2]", "cantidad >= mayor_salida[2]", ">= (último empate)"),
    ("2-4", "stock_anterior < stock_minimo and stock > stock_minimo", "stock > stock_minimo", "sin stock anterior"),
    ("3-2", "min(movimientos, key=lambda m: m[2])", "min(movimientos)", "min sin key"),
    ("3-3", "key=lambda m: m[2])[:3]", "key=lambda m: m[2], reverse=True)[:3]", "reverse=True con negativos"),
    ("3-4", "(-r[2], r[3])", "(-r[2], -r[3])", "desempate invertido"),
    ("3-4", "start=1", "start=0", "enumerate sin start=1"),
    ("reto-a", "movimiento[2] < mayor_egreso[2]", "movimiento[2] <= mayor_egreso[2]", "<= en el empate"),
    ("reto-a", "    saldo += monto\n    if saldo < 0:\n        dias_sobregiro += 1",
     "    if monto == 0:\n        continue\n    saldo += monto\n    if saldo < 0:\n        dias_sobregiro += 1",
     "continue en monto 0 antes del chequeo"),
    ("reto-a", "saldo = saldo_inicial\nfor fecha, concepto, monto in movimientos:\n    saldo += monto\nsaldo_final",
     "saldo = 0\nfor fecha, concepto, monto in movimientos:\n    saldo += monto\nsaldo_final", "saldo desde 0 (sin inicial)"),
    ("reto-a", "        if saldo_anterior >= 0:\n            veces_en_sobregiro += 1", "        veces_en_sobregiro += 1",
     "contar días como entradas"),
    ("reto-b", "monto < mayor_egreso[2]", "monto <= mayor_egreso[2]", "<= en el empate"),
    ("reto-b", "    saldo_anterior = saldo                            # al final de la vuelta",
     "    pass", "no actualizar saldo_anterior"),
    ("reto-b", "if monto > 0:\n        n_ingresos += 1\n    elif monto < 0:", "if monto >= 0:\n        n_ingresos += 1\n    elif monto < 0:",
     "contar el 0 como ingreso"),
]


def verificar_mutantes(nb):
    atrapados, escapados, no_aplicados = 0, [], []
    for k, viejo, nuevo, descripcion in MUTANTES:
        src = celda(nb, f"ej-{k}-solucion").source
        if viejo not in src:
            no_aplicados.append((k, descripcion))
            continue
        mutado = src.replace(viejo, nuevo)
        ns = ns_nuevo()
        try:
            ejecutar(mutado, ns, f"mutante-{k}")
            ejecutar(celda(nb, f"ej-{k}-validacion").source, ns, f"validacion-{k}")
            escapados.append((k, descripcion))
        except AssertionError:
            atrapados += 1
        except Exception as e:  # noqa: BLE001 — un crash también delata el error, pero lo anotamos
            escapados.append((k, f"{descripcion} → {type(e).__name__}"))
    registrar("5.  los asserts detectan errores típicos inyectados (mutantes)",
              not escapados and not no_aplicados,
              f"{atrapados}/{len(MUTANTES)} atrapados" + (f"; escapan: {escapados}" if escapados else "")
              + (f"; no aplicados: {no_aplicados}" if no_aplicados else ""))


# ----------------------------------------------------------------------
# Tamaño de los datos (6 a 15 registros, salvo el reto)
# ----------------------------------------------------------------------
def verificar_tamano_datos(nb):
    malos = []
    for k in ids_ejercicios(nb):
        if k.startswith("reto"):
            continue
        ns = ns_nuevo()
        ejecutar(celda(nb, f"ej-{k}-plantilla").source, ns)
        for nombre, valor in ns.items():
            if nombre.startswith("_") or not isinstance(valor, list) or not valor:
                continue
            if isinstance(valor[0], (tuple, str, float)) and nombre in (
                "ventas", "ventas_semana", "movimientos", "gastos", "movimientos_a", "movimientos_b",
                "movimientos_kardex", "lista_prueba", "fechas", "clientes",
            ) and not 6 <= len(valor) <= 15:
                malos.append((k, nombre, len(valor)))
    registrar("6.  datos de los ejercicios entre 6 y 15 registros", not malos, str(malos))


def main():
    nb = nbformat.read(RUTA, as_version=4)
    verificar_estructura(nb)
    verificar_soluciones(nb)
    verificar_soluciones_standalone(nb)
    verificar_plantillas(nb)
    verificar_un_solo_for(nb)
    verificar_trampas(nb)
    verificar_mutantes(nb)
    verificar_tamano_datos(nb)
    fallidos = [r for r in resultados if not r[1]]
    print(f"\n{len(resultados) - len(fallidos)}/{len(resultados)} comprobaciones OK")
    sys.exit(1 if fallidos else 0)


if __name__ == "__main__":
    main()
