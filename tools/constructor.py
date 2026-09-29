"""Utilidades para construir el notebook: celdas, ejercicios y ensamblado.

El notebook se genera SIEMPRE con `tools/generar_notebook.py`; no se edita a mano.
"""

from dataclasses import dataclass, field
import re

import nbformat


def _slug(texto):
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


@dataclass
class Ejercicio:
    num: str  # "1.1"
    titulo: str
    nivel: str  # "🟢 Básico", "🟡 Intermedio", ...
    enunciado: str  # markdown: enunciado, datos de entrada y variables a crear
    datos: str  # código: datos del ejercicio (van en la misma celda que la plantilla)
    plantilla: str  # código sin resolver (o con el bug) tras los datos
    validacion: str  # asserts (sin el print final)
    pistas: list = field(default_factory=list)
    solucion: str = ""  # código que reemplaza a la plantilla
    errores: str = ""  # 2 o 3 líneas sobre el error típico
    es_bug: bool = False

    @property
    def clave(self):
        return self.num.replace(".", "-")


class Libro:
    """Acumula celdas en orden y las convierte en un nbformat 4.5 sin outputs."""

    def __init__(self):
        self.celdas = []
        self._n = 0
        self._soluciones = []  # soluciones pendientes de volcar al final del módulo

    # --- celdas sueltas -------------------------------------------------
    def _id(self, prefijo):
        self._n += 1
        return f"{prefijo}-{self._n:03d}"

    def md(self, texto, id=None):
        self.celdas.append(
            nbformat.v4.new_markdown_cell(texto.strip("\n"), id=id or self._id("md"))
        )

    def codigo(self, texto, id=None):
        self.celdas.append(
            nbformat.v4.new_code_cell(texto.strip("\n"), id=id or self._id("cod"))
        )

    def prediccion(self, lineas_a_predecir, codigo, titulo="🔮 Predice antes de ejecutar"):
        """Celda de predicción: comentarios para escribir y luego el código."""
        cabecera = [f"# {titulo}", "# Escribe tu predicción aquí, ANTES de ejecutar:"]
        for linea in lineas_a_predecir:
            cabecera.append(f"#   {linea} → ")
        self.codigo("\n".join(cabecera) + "\n\n" + codigo.strip("\n"))

    def ejemplo(self, texto):
        self.codigo(texto)

    # --- ejercicios ------------------------------------------------------
    def ejercicio(self, ej):
        k = ej.clave
        cab = f"### {ej.nivel} Ejercicio {ej.num} — {ej.titulo}"
        if ej.es_bug:
            cab = f"### 🐛 Ejercicio {ej.num} — {ej.titulo} (encuentra y arregla el bug)"
        self.md(cab + "\n\n" + ej.enunciado.strip("\n"), id=f"ej-{k}-enunciado")
        self.codigo(ej.datos.strip("\n") + "\n\n" + ej.plantilla.strip("\n"),
                    id=f"ej-{k}-plantilla")
        val = ej.validacion.strip("\n") + f'\n\nprint("✅ Ejercicio {ej.num} superado")'
        self.codigo(val, id=f"ej-{k}-validacion")
        for i, pista in enumerate(ej.pistas, start=1):
            self.codigo(
                f'# @title 💡 Pista {i} {{ display-mode: "form" }}\n'
                f"print({pista!r})",
                id=f"ej-{k}-pista-{i}",
            )
        self._soluciones.append(ej)

    def volcar_soluciones(self, encabezado):
        self.md(encabezado, id=self._id("md-soluciones"))
        for ej in self._soluciones:
            comentarios = "\n".join(f"# {l}" for l in ej.errores.strip().splitlines())
            texto = (
                f'# @title 🔒 Solución {ej.num} (ábrela después de intentarlo) '
                f'{{ display-mode: "form" }}\n'
                f"# Error típico:\n{comentarios}\n\n"
                + ej.datos.strip("\n") + "\n\n" + ej.solucion.strip("\n")
            )
            self.codigo(texto, id=f"ej-{ej.clave}-solucion")
        self._soluciones = []

    # --- salida -----------------------------------------------------------
    def notebook(self):
        nb = nbformat.v4.new_notebook()
        nb.cells = self.celdas
        nb.metadata = {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
            "colab": {"provenance": [], "toc_visible": True},
        }
        return nb
