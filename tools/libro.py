"""Constructor de celdas con el formato de las sesiones:
📘 Concepto → ejemplo → ✍️ Tu turno → ✅ Verificar → 💡 Pistas, y soluciones en un anexo final."""

from dataclasses import dataclass, field

import nbformat


@dataclass
class Ejercicio:
    clave: str        # "1", "reto-a", "pro"... (se usa en los ids de las celdas)
    titulo: str       # "Ejercicio 1: conteo por categoría"
    enunciado: str    # markdown debajo del título
    check: str        # llamada que verifica, p. ej. "check_ejercicio_1()"
    solucion: str     # código de la solución (va en el anexo)
    errores: str      # 1-3 frases sobre el error típico
    pistas: list = field(default_factory=list)
    plantilla: str = "# Tu código aquí\n"
    nivel: str = "###"


class Libro:
    def __init__(self):
        self.celdas = []
        self.resueltos = []
        self._n = 0

    def _id(self, prefijo):
        self._n += 1
        return f"{prefijo}-{self._n:03d}"

    def md(self, texto, id=None):
        self.celdas.append(nbformat.v4.new_markdown_cell(texto.strip("\n"), id=id or self._id("md")))

    def codigo(self, texto, id=None):
        self.celdas.append(nbformat.v4.new_code_cell(texto.strip("\n"), id=id or self._id("cod")))

    def ejercicio(self, ej):
        k = ej.clave
        self.md(f"{ej.nivel} ✍️ Tu turno · {ej.titulo}\n{ej.enunciado.strip()}", id=f"ej-{k}-enunciado")
        self.codigo(ej.plantilla, id=f"ej-{k}-plantilla")
        self.codigo(f"# ✅ Verificar\n{ej.check}", id=f"ej-{k}-verificar")
        if ej.pistas:
            bloques = [f"<details><summary>💡 Pista {i}</summary>\n\n{p.strip()}\n</details>"
                       for i, p in enumerate(ej.pistas, start=1)]
            self.md("\n\n".join(bloques), id=f"ej-{k}-pistas")
        self.resueltos.append(ej)

    def anexo_soluciones(self):
        self.md("""
---
## 📎 Anexo · Soluciones
Ábrelas **solo después de intentarlo** y de leer lo que te dice ✅ Verificar. Cada solución usa los datos del setup: si quieres ejecutarla, cópiala en la celda de su ejercicio.
""", id="anexo-titulo")
        for ej in self.resueltos:
            self.md(
                f"<details><summary>🔒 {ej.titulo}</summary>\n\n"
                f"```python\n{ej.solucion.strip()}\n```\n\n"
                f"**Error típico:** {ej.errores.strip()}\n</details>",
                id=f"ej-{ej.clave}-solucion",
            )

    def notebook(self):
        nb = nbformat.v4.new_notebook()
        nb.cells = self.celdas
        nb.metadata = {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
            "colab": {"provenance": [], "toc_visible": True},
        }
        return nb
