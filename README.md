# review_1_python

Prácticas de Python para análisis de datos.

## Sesiones

| Sesión | Notebook | Abrir |
|---|---|---|
| Refuerzo de Python puro: diccionarios, estado acumulativo, `key`, `zip` y tablas (≈ 3 h 40 min) | [`sesiones/refuerzo_python_puro.ipynb`](sesiones/refuerzo_python_puro.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Smiledxd/review_1_python/blob/main/sesiones/refuerzo_python_puro.ipynb) |

## Utilidades (`tools/`)

- `python3 tools/generar_notebook.py`: genera el notebook (es la fuente de verdad; no lo edites a mano) y lo valida con `nbformat`. La celda de setup sale de `tools/celda_setup.py` y el contenido, de `tools/parte1.py`, `parte2.py`, `parte3.py` y `reto.py`.
- `python3 tools/verificar_notebook.py`: ejecuta el notebook con las soluciones y con las plantillas, recalcula los valores esperados de forma independiente, comprueba las trampas del reto final y que los verificadores detecten errores típicos inyectados.

Requieren `nbformat` (y `matplotlib` para la celda del gráfico).
