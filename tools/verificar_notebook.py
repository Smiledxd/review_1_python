"""Verifica `sesiones/refuerzo_python_puro.ipynb`.

Uso (desde la raíz del repo):
    python3 tools/verificar_notebook.py

Qué comprueba:
 1. Estructura: nbformat 4 válido, kernel python3, sin outputs, solo biblioteca estándar, formato de cada ejercicio.
 2. Ejecuta el notebook completo dos veces:
    - con las SOLUCIONES del anexo en lugar de las plantillas: todo corre y cada ✅ Verificar termina en 🎉;
    - con las PLANTILLAS sin resolver: cada ✅ Verificar marca ❌ y ningún punto sale ✅ gratis.
 3. Recalcula los valores esperados de forma independiente (aquí sí: collections, itertools, statistics, heapq)
    y los compara con lo que producen las soluciones.
 4. Las trampas del reto final cambian el resultado y el verificador las reconoce con su mensaje.
 5. Mutantes (errores típicos inyectados en las soluciones) son detectados por los verificadores.
"""

import ast
import contextlib
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

resultados = []


def registrar(criterio, ok, detalle=""):
    resultados.append((criterio, ok))
    print(("✅" if ok else "❌"), criterio, ("— " + detalle) if detalle else "")


# ----------------------------------------------------------------------
# Lectura y ejecución
# ----------------------------------------------------------------------
def ejecutar(src, ns, nombre="celda"):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src, nombre, "exec"), ns)
    return buf.getvalue()


def celda(nb, id):
    return next(c for c in nb.cells if c.id == id)


def claves(nb):
    return [c.id[3:-len("-plantilla")] for c in nb.cells if c.id.startswith("ej-") and c.id.endswith("-plantilla")]


def soluciones(nb):
    sol = {}
    for k in claves(nb):
        texto = celda(nb, f"ej-{k}-solucion").source
        sol[k] = re.search(r"```python\n(.*?)\n```", texto, re.S).group(1)
    return sol


def correr(nb, modo, reemplazos=None):
    """Ejecuta todas las celdas de código en orden. modo: 'soluciones' o 'plantillas'.
    Devuelve (namespace, salidas de cada verificar, errores)."""
    sol = soluciones(nb)
    reemplazos = reemplazos or {}
    ns = {"__name__": "__main__"}
    salidas, errores = {}, []
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        src = c.source
        if c.id.endswith("-plantilla"):
            k = c.id[3:-len("-plantilla")]
            src = reemplazos.get(k, sol[k] if modo == "soluciones" else src)
        try:
            salida = ejecutar(src, ns, c.id)
        except Exception as e:  # noqa: BLE001
            errores.append(f"{c.id}: {type(e).__name__}: {e}")
            continue
        if c.id.endswith("-verificar"):
            salidas[c.id[3:-len("-verificar")]] = salida
    return ns, salidas, errores


def verificar_aislado(nb, k, codigo):
    """Setup + un solo código + su verificador, en un namespace nuevo."""
    ns = {"__name__": "__main__"}
    ejecutar(celda(nb, "setup").source, ns)
    ejecutar(codigo, ns, f"ej-{k}")
    return ejecutar(celda(nb, f"ej-{k}-verificar").source, ns), ns


# ----------------------------------------------------------------------
# Oráculos independientes
# ----------------------------------------------------------------------
def r2(x):
    return round(x, 2)


def saldos(inicial, movs):
    return list(itertools.accumulate((m[2] for m in movs), initial=inicial))[1:]


def agrupar(registros, filtro=lambda m: True, valor=lambda m: m[2]):
    g = defaultdict(list)
    for m in registros:
        if filtro(m):
            g[m[1]].append(valor(m))
    return g


def cruces(inicial, movs):
    s = saldos(inicial, movs)
    return sum(1 for a, b in itertools.pairwise([inicial] + s) if a >= 0 > b)


def oraculos(d):
    """d: los datos originales. Devuelve {variable: valor esperado} para todo el notebook."""
    e = {}
    # Parte 1
    e["conteo_por_categoria"] = dict(Counter(m[1] for m in d["ventas_bodega"]))
    e["pred_in_cero"], e["pred_in_valor"], e["pred_error"] = True, False, "KeyError"
    e["total_por_categoria"] = {c: r2(math.fsum(v)) for c, v in agrupar(d["ventas_bodega"]).items()}
    e["pred_igual"], e["pred_redondeado"], e["pred_error_get"] = False, True, "TypeError"
    e["egresos_por_concepto"] = {c: r2(math.fsum(v)) for c, v in
                                 agrupar(d["movimientos_junio"], lambda m: m[2] < 0, lambda m: -m[2]).items()}
    g = agrupar(d["compras_mes"])
    e["compras_total"] = {c: r2(math.fsum(v)) for c, v in g.items()}
    e["compras_cantidad"] = {c: len(v) for c, v in g.items()}
    e["compras_promedio"] = {c: r2(statistics.fmean(v)) for c, v in g.items()}
    e["categoria_mas_compras"] = max(g, key=lambda c: math.fsum(g[c]))
    # Parte 2
    s = saldos(d["saldo_inicial_caja"], d["movimientos_caja"])
    e["saldos_caja"], e["saldo_cierre"] = [r2(x) for x in s], r2(s[-1])
    movs, s = d["movimientos_cuenta"], saldos(d["saldo_inicial_cuenta"], d["movimientos_cuenta"])
    rojos = [m[0] for m, x in zip(movs, s) if x < 0]
    e["primer_rojo"], e["dias_en_rojo"] = rojos[0], rojos
    e["entradas_en_rojo"] = cruces(d["saldo_inicial_cuenta"], movs)
    e["primer_rojo_ahorro"] = next((m[0] for m, x in zip(d["movimientos_ahorro"],
                                    saldos(d["saldo_inicial_ahorro"], d["movimientos_ahorro"])) if x < 0), None)
    s = saldos(d["saldo_inicial_agosto"], d["movimientos_agosto"])
    i = min(range(len(s)), key=s.__getitem__)
    e["saldo_minimo"], e["fecha_saldo_minimo"] = r2(s[i]), d["movimientos_agosto"][i][0]
    e["pred_con_menor"], e["pred_con_menor_igual"] = "Proveedor B", "Proveedor C"
    deltas = [c if t == "entrada" else -c for _, t, c in d["kardex"]]
    st = list(itertools.accumulate(deltas, initial=d["stock_inicial"]))
    mn = d["stock_minimo"]
    e["stock_final"] = st[-1]
    e["fechas_bajo_minimo"] = [m[0] for m, x in zip(d["kardex"], st[1:]) if x < mn]
    e["fecha_recuperacion"] = next((m[0] for m, a, b in zip(d["kardex"], st, st[1:]) if a < mn < b), None)
    e["mayor_salida"] = max((m for m in d["kardex"] if m[1] == "salida"), key=lambda m: m[2])
    # Parte 3
    e.update(pred_a=False, pred_b=False, pred_c=True, pred_d=False, pred_e=True, pred_f=True,
             pred_min=sorted(d["lista_prueba"])[0])
    movs = d["movimientos_abril"]
    e["mayor_ingreso"] = max(movs, key=lambda m: m[2])
    e["mayor_egreso_abril"] = min(movs, key=lambda m: m[2])
    e["top3_egresos"] = heapq.nsmallest(3, [m for m in movs if m[2] < 0], key=lambda m: m[2])
    f, v, c = d["fechas_semana"], d["ventas_dia"], d["clientes_dia"]
    e["venta_por_fecha"] = {a: b for a, b in zip(f, v)}
    orden = sorted(range(len(f)), key=lambda j: (-v[j], c[j]))
    e["ranking"] = [(j + 1, f[j], v[j], c[j]) for j in orden]
    e["dia_ganador"], e["fecha_ganadora"] = orden[0] + 1, f[orden[0]]
    tabla = dict(zip(d["locales"], d["ventas_mensuales"]))
    e["total_por_local"] = {k: sum(fila) for k, fila in tabla.items()}
    e["mejor_mes_por_local"] = {k: max(range(len(fila)), key=fila.__getitem__) + 1 for k, fila in tabla.items()}
    e["local_top"] = max(e["total_por_local"], key=e["total_por_local"].get)
    # Reto y pro
    movs, si = d["movimientos"], d["saldo_inicial"]
    s = saldos(si, movs)
    gasto = {k: r2(math.fsum(x)) for k, x in agrupar(movs, lambda m: m[2] < 0, lambda m: -m[2]).items()}
    rojos = [m[0] for m, x in zip(movs, s) if x < 0]
    e.update(
        saldo_final=r2(si + math.fsum(m[2] for m in movs)),
        n_ingresos=sum(m[2] > 0 for m in movs), n_egresos=sum(m[2] < 0 for m in movs),
        gasto_por_concepto=gasto, mayor_egreso=min(movs, key=lambda m: m[2]),
        dias_sobregiro=rojos, veces_en_sobregiro=cruces(si, movs),
        primer_dia_sobregiro=rojos[0] if rojos else None, concepto_mas_gasto=max(gasto, key=gasto.get),
        saldo_por_fecha={m[0]: r2(x) for m, x in zip(movs, s)},
        ranking_conceptos=sorted(gasto.items(), key=lambda kv: (-kv[1], kv[0])),
        racha_mas_larga=max((len(list(grupo)) for rojo, grupo in itertools.groupby(x < 0 for x in s) if rojo), default=0),
    )
    return e


def iguales(a, b):
    if isinstance(b, bool) or b is None:
        return type(a) is type(b) and a == b
    if isinstance(b, float):
        return isinstance(a, (int, float)) and r2(a) == r2(b)
    if isinstance(b, dict):
        return isinstance(a, dict) and a.keys() == b.keys() and all(iguales(a[k], b[k]) for k in b)
    if isinstance(b, (list, tuple)):
        return type(a) is type(b) and len(a) == len(b) and all(iguales(x, y) for x, y in zip(a, b))
    return a == b


# ----------------------------------------------------------------------
# 1. Estructura
# ----------------------------------------------------------------------
def verificar_estructura(nb):
    nbformat.validate(nb)
    registrar("1a. nbformat 4 válido y kernel python3",
              nb.nbformat == 4 and nb.metadata["kernelspec"]["name"] == "python3", f"{len(nb.cells)} celdas")
    registrar("1b. sin outputs guardados",
              all(c.cell_type != "code" or (not c.outputs and c.execution_count is None) for c in nb.cells))

    codigos = [(c.id, c.source) for c in nb.cells if c.cell_type == "code"]
    codigos += [(f"solucion-{k}", s) for k, s in soluciones(nb).items()]
    permitidos = {"copy", "math", "matplotlib.pyplot"}
    malos = []
    for id_, src in codigos:
        for nodo in ast.walk(ast.parse(src)):
            if isinstance(nodo, ast.Import):
                malos += [(id_, a.name) for a in nodo.names if a.name not in permitidos]
            elif isinstance(nodo, ast.ImportFrom):
                malos.append((id_, nodo.module))
        malos += [(id_, p) for p in ("pandas", "numpy", "collections", "itertools") if p in src]
    registrar("1c. solo biblioteca estándar (+ matplotlib en el gráfico)", not malos, str(malos))

    texto = "\n".join(c.source for c in nb.cells).lower().replace("autoevaluación", "")
    prohibidas = [p for p in (r"pseint", r"curso", r"evaluaci", r"examen", r"profesor", r"\bnotas?\b", r"calificaci")
                  if re.search(p, texto)]
    registrar("1d. sin referencias a cursos, evaluaciones, notas ni PSeInt", not prohibidas, str(prohibidas))

    problemas = []
    if not celda(nb, "setup").source.startswith('#@title ⚙️ Setup: ejecuta esta celda y no la edites { display-mode: "form" }'):
        problemas.append("setup sin #@title")
    for k in claves(nb):
        if celda(nb, f"ej-{k}-verificar").source.splitlines()[0] != "# ✅ Verificar":
            problemas.append(f"{k}: verificar")
        pistas = [c for c in nb.cells if c.id == f"ej-{k}-pistas"]
        n = pistas[0].source.count("<details>") if pistas else 0
        if k != "pro" and not 1 <= n <= 2:
            problemas.append(f"{k}: {n} pistas")
        if "Error típico" not in celda(nb, f"ej-{k}-solucion").source:
            problemas.append(f"{k}: solución sin error típico")
    predicciones = sum(1 for c in nb.cells if c.cell_type == "code" and c.source.startswith("# 🔮 Predice antes de ejecutar"))
    registrar("1e. formato: setup activable, ✍️/✅/💡 por ejercicio, soluciones plegadas en el anexo",
              not problemas, f"{len(claves(nb))} ejercicios, {predicciones} ejemplos con 🔮" + (f"; {problemas}" if problemas else ""))
    anexo = [i for i, c in enumerate(nb.cells) if c.id == "anexo-titulo"][0]
    registrar("1f. ninguna solución visible fuera del anexo final",
              all(i > anexo for i, c in enumerate(nb.cells) if c.id.endswith("-solucion"))
              and all("<details>" in c.source for c in nb.cells if c.id.endswith("-solucion")))


# ----------------------------------------------------------------------
# 2 y 3. Ejecución con soluciones y con plantillas; oráculos
# ----------------------------------------------------------------------
def verificar_ejecucion(nb):
    ns, salidas, errores = correr(nb, "soluciones")
    malos = [k for k, s in salidas.items() if "🎉" not in s or "❌" in s]
    registrar("2a. con soluciones: todo corre y cada ✅ Verificar termina en 🎉",
              not errores and not malos and len(salidas) == len(claves(nb)),
              f"{len(salidas)} verificadores" + (f"; errores {errores}" if errores else "") + (f"; fallan {malos}" if malos else ""))
    for k in malos:
        print(salidas[k])

    esperado = oraculos(ns["_D"])
    distintos = [f"{v}: {ns.get(v)!r} ≠ {x!r}" for v, x in esperado.items() if not iguales(ns.get(v), x)]
    registrar("3.  valores recalculados de forma independiente coinciden con las soluciones",
              not distintos, f"{len(esperado)} variables" + (f"; {distintos}" if distintos else ""))

    intactos = [k for k in ns["_D"] if ns[k] != ns["_D"][k]]
    ns_p, salidas_p, errores_p = correr(nb, "plantillas")
    intactos += [k for k in ns_p["_D"] if ns_p[k] != ns_p["_D"][k]]
    registrar("2b. los ejemplos y las soluciones no modifican los datos del setup", not intactos, str(intactos))

    gratis = {k: s.count("✅") for k, s in salidas_p.items() if s.count("✅")}
    sin_error = [k for k, s in salidas_p.items() if "❌" not in s or "🎉" in s]
    registrar("2c. con plantillas sin resolver: cada verificador marca ❌ y ningún punto sale ✅ gratis",
              not errores_p and not gratis and not sin_error and len(salidas_p) == len(claves(nb)),
              f"{sum(s.count('❌') for s in salidas_p.values())} ❌ en {len(salidas_p)} verificadores"
              + (f"; ✅ gratis {gratis}" if gratis else "") + (f"; sin ❌ {sin_error}" if sin_error else "")
              + (f"; errores {errores_p}" if errores_p else ""))

    solos = []
    for k, codigo in soluciones(nb).items():
        salida, _ = verificar_aislado(nb, k, codigo)
        if "🎉" not in salida:
            solos.append(k)
    registrar("2d. cada solución funciona sola, solo con el setup", not solos, str(solos))

    arbol = ast.parse(soluciones(nb)["reto-b"])
    fors = [n for n in ast.walk(arbol) if isinstance(n, ast.For) and isinstance(n.iter, ast.Name) and n.iter.id == "movimientos"]
    registrar("2e. la solución del reto · Parte B recorre `movimientos` con un único for", len(fors) == 1, f"{len(fors)} for")


# ----------------------------------------------------------------------
# 4. Trampas del reto final
# ----------------------------------------------------------------------
def verificar_trampas(nb):
    _, ns = verificar_aislado(nb, "reto-a", soluciones(nb)["reto-a"])
    si, movs = ns["_D"]["saldo_inicial"], ns["_D"]["movimientos"]
    e = oraculos(ns["_D"])

    saldo, con_continue = si, []
    for fecha, _, monto in movs:
        if monto == 0:
            continue
        saldo += monto
        if saldo < 0:
            con_continue.append(fecha)
    mejor = None
    for m in movs:
        if m[2] < 0 and (mejor is None or m[2] <= mejor[2]):
            mejor = m
    trampas = [
        ("4a. min(movimientos) sin key", "mayor_egreso", min(movs), "más ANTIGUO"),
        ("4b. `continue` en el monto 0 antes del chequeo", "dias_sobregiro", con_continue, "`continue`"),
        ("4c. `<=` en vez de `<`", "mayor_egreso", mejor, "empate"),
        ("4d. saldo arrancando en 0", "saldo_final", r2(sum(m[2] for m in movs)), "saldo inicial"),
        ("4e. días en vez de entradas", "veces_en_sobregiro", len(e["dias_sobregiro"]), "no de entradas"),
    ]
    for nombre, var, valor, mensaje in trampas:
        original = ns[var]
        ns[var] = valor                      # los check_* leen este mismo namespace
        salida = ejecutar(celda(nb, "ej-reto-a-verificar").source, ns)
        ns[var] = original
        linea = next((l for l in salida.splitlines() if f"`{var}`" in l), "")
        registrar(f"{nombre}: cambia `{var}` y el verificador lo explica",
                  not iguales(valor, e[var]) and linea.startswith("❌") and mensaje in linea, f"{valor!r} → {linea[:110]}")

    s = saldos(si, movs)
    egresos = [m for m in movs if m[2] < 0]
    conceptos = Counter(m[1] for m in egresos)
    fechas = [m[0] for m in movs]
    checks = {
        "14-18 movimientos": 14 <= len(movs) <= 18,
        "saldo inicial positivo": si > 0,
        "fechas únicas y ordenadas": fechas == sorted(set(fechas)),
        "ajuste de 0 en un día en sobregiro": any(m[2] == 0 and x < 0 for m, x in zip(movs, s)),
        "empate en el mayor egreso": sum(m[2] == e["mayor_egreso"][2] for m in egresos) >= 2,
        "la fecha más antigua no es el mayor egreso": min(movs) != e["mayor_egreso"],
        "concepto con un solo egreso": 1 in conceptos.values(),
        "dos entradas en sobregiro": e["veces_en_sobregiro"] == 2,
    }
    registrar("4f. el dataset del reto activa todas las trampas", all(checks.values()),
              ", ".join(k for k, v in checks.items() if not v) or "todas activas")


# ----------------------------------------------------------------------
# 5. Mutantes: errores típicos inyectados en las soluciones
# ----------------------------------------------------------------------
MUTANTES = [
    ("1", "conteo_por_categoria[categoria] = 1 ", "conteo_por_categoria[categoria] = 0 ", "Inicializaste en 0"),
    ("1", "conteo_por_categoria[categoria] += 1", "conteo_por_categoria[categoria] += monto", "no un conteo"),
    ("2", "round(total_por_categoria[categoria], 2)", "total_por_categoria[categoria]", "sin redondear"),
    ("3", "if monto < 0:", "if monto != 0:", "ingresos"),
    ("3", ".get(concepto, 0) - monto", ".get(concepto, 0) + monto", "positivo"),
    ("4", "total > compras_total[categoria_mas_compras]", "total < compras_total[categoria_mas_compras]", "MENOR"),
    ("4", "round(total / compras_cantidad[categoria], 2)", "total / compras_cantidad[categoria]", "sin redondear"),
    ("5", "saldo = saldo_inicial_caja  ", "saldo = 0  ", "arrancaste el saldo en 0"),
    ("5", "saldos_caja.append(round(saldo, 2))", "saldos_caja.append(saldo)", "sin redondear"),
    ("5", "    saldo += monto  ", "    if monto == 0:\n        continue\n    saldo += monto  ", "un saldo por movimiento"),
    ("6", "        break                                   # ya", "        pass                                    # ya", "`break`"),
    ("6", "    saldo += monto                              # sin continue",
     "    if monto == 0:\n        continue\n    saldo += monto                              # sin continue", "`continue`"),
    ("6", "        if saldo_anterior >= 0:\n            entradas_en_rojo += 1", "        entradas_en_rojo += 1", "no de entradas"),
    ("7", "saldo_minimo = None    ", "saldo_minimo = 0       ", "centinela"),
    ("7", "saldo < saldo_minimo:", "saldo <= saldo_minimo:", "`<=`"),
    ("8", "cantidad > mayor_salida[2]", "cantidad >= mayor_salida[2]", "`>=`"),
    ("8", "stock_anterior < stock_minimo and stock > stock_minimo", "stock > stock_minimo", "stock anterior"),
    ("8", "    else:\n        stock -= cantidad\n        if mayor_salida",
     "    else:\n        stock -= cantidad\n    if True:\n        if mayor_salida", "ENTRADA"),
    ("10", "min(movimientos_abril, key=lambda m: m[2])", "min(movimientos_abril)", "más ANTIGUO"),
    ("10", "key=lambda m: m[2])[:3]", "key=lambda m: m[2], reverse=True)[:3]", "reverse=True"),
    ("11", "(-r[2], r[3])", "(-r[2],)", "desempate"),
    ("11", "start=1", "start=0", "start=1"),
    ("12", "if fila[j] > fila[mejor_j]:", "if fila[j] >= fila[mejor_j]:", "`>=`"),
    ("12", "mejor_j + 1", "mejor_j", "súmale 1"),
    ("reto-a", "mayor_egreso = min(movimientos, key=lambda m: m[2])", "mayor_egreso = min(movimientos)", "más ANTIGUO"),
    ("reto-a", "    saldo += monto                          # sin continue",
     "    if monto == 0:\n        continue\n    saldo += monto                          # sin continue", "`continue`"),
    ("reto-a", "    if monto > 0:\n        n_ingresos += 1", "    if monto >= 0:\n        n_ingresos += 1", "monto 0 como ingreso"),
    ("reto-a", "        if saldo_anterior >= 0:\n            veces_en_sobregiro += 1", "        veces_en_sobregiro += 1", "no de entradas"),
    ("reto-b", "monto < mayor_egreso[2]", "monto <= mayor_egreso[2]", "empate"),
    ("reto-b", "    saldo_anterior = saldo                         # al final", "    pass                                           # al final", "veces_en_sobregiro"),
    ("reto-b", "saldo = saldo_inicial\n", "saldo = 0\n", "saldo inicial"),
    ("pro", "        racha = 0", "        pass", "racha"),
    ("pro", "(-kv[1], kv[0])", "(kv[1], kv[0])", "menor a mayor"),
]


def verificar_mutantes(nb):
    sol = soluciones(nb)
    atrapados, escapados = 0, []
    for k, viejo, nuevo, mensaje in MUTANTES:
        if viejo not in sol[k]:
            escapados.append((k, "no aplicado", viejo[:30]))
            continue
        try:
            salida, _ = verificar_aislado(nb, k, sol[k].replace(viejo, nuevo, 1))
        except Exception as e:  # noqa: BLE001
            escapados.append((k, f"{type(e).__name__}", mensaje))
            continue
        if "❌" in salida and mensaje in salida:
            atrapados += 1
        else:
            escapados.append((k, mensaje, salida.strip().splitlines()[1:4]))
    registrar("5.  los verificadores detectan errores típicos inyectados y los nombran",
              not escapados, f"{atrapados}/{len(MUTANTES)}" + (f"; escapan {escapados}" if escapados else ""))


# ----------------------------------------------------------------------
# 6. Tamaño de los datos
# ----------------------------------------------------------------------
def verificar_tamano(nb):
    ns = {"__name__": "__main__"}
    ejecutar(celda(nb, "setup").source, ns)
    malos = [(k, len(v)) for k, v in ns["_D"].items()
             if isinstance(v, list) and k not in ("movimientos", "locales", "ventas_mensuales") and not 6 <= len(v) <= 15]
    registrar("6.  datos de los ejercicios entre 6 y 15 registros (reto: 14-18)",
              not malos and 14 <= len(ns["_D"]["movimientos"]) <= 18, str(malos))


def main():
    nb = nbformat.read(RUTA, as_version=4)
    verificar_estructura(nb)
    verificar_ejecucion(nb)
    verificar_trampas(nb)
    verificar_mutantes(nb)
    verificar_tamano(nb)
    fallidos = [r for r in resultados if not r[1]]
    print(f"\n{len(resultados) - len(fallidos)}/{len(resultados)} comprobaciones OK")
    sys.exit(1 if fallidos else 0)


if __name__ == "__main__":
    main()
