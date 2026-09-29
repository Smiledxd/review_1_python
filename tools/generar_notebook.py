"""Fuente de verdad del notebook `sesiones/refuerzo_python_puro.ipynb`.

Uso (desde la raíz del repo):
    python3 tools/generar_notebook.py

Genera el notebook (nbformat 4, kernel python3, sin outputs) y lo valida con `nbformat.validate`.
"""

from pathlib import Path
import sys

import nbformat

sys.path.insert(0, str(Path(__file__).parent))

from constructor import Libro  # noqa: E402
import contenido_portada, modulo1, modulo2, modulo3, reto_final  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "sesiones" / "refuerzo_python_puro.ipynb"


def construir():
    libro = Libro()
    contenido_portada.portada(libro)
    modulo1.agregar(libro)
    modulo2.agregar(libro)
    modulo3.agregar(libro)
    reto_final.agregar(libro)
    contenido_portada.cierre(libro)
    return libro.notebook()


def main():
    nb = construir()
    nbformat.validate(nb)
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, DESTINO)
    print(f"✅ {DESTINO.relative_to(RAIZ)}: {len(nb.cells)} celdas, nbformat {nb.nbformat}.{nb.nbformat_minor}")


if __name__ == "__main__":
    main()
