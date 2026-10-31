"""
Avance Preliminar (Fase 3): Estructura base del servidor API REST con FastAPI.

TODO (Sprint 3 - Rol: Desarrolladora Full Stack / UI - Geomayra Vilca):
Integrar los endpoints de carga de archivos JSON/CSV (`/api/upload`) y la comparación
visual en tiempo real entre Welsh-Powell y DSatur.
"""

from typing import Any, Dict
from fastapi import FastAPI
from src.core.coloring import WelshPowellColoring
from src.core.graph import ConflictGraph
from src.core.verifier import verify_coloring
from src.utils.loader import get_worked_example_6_courses

app = FastAPI(
    title="Planificador de Horarios mediante Coloración de Grafos - ESPOCH (Avance Fase 3)",
    version="0.1.0",
)


@app.get("/api/status")
def status() -> Dict[str, str]:
    """Verifica el estado del servidor en Fase 3."""
    return {
        "status": "ok",
        "phase": "Fase 3 - Investigación Formativa (Prototipo Preliminar)",
        "group": "Grupo 3 - Ingeniería de Software ESPOCH",
    }


@app.get("/api/example")
def run_preliminary_worked_example() -> Dict[str, Any]:
    """
    Ejecuta la simulación preliminar sobre el Ejemplo Mínimo Trabajado (6 asignaturas).
    """
    courses = get_worked_example_6_courses()
    graph = ConflictGraph.from_courses(courses)
    wp_result = WelshPowellColoring.solve(graph)
    verif = verify_coloring(graph, wp_result)

    return {
        "num_vertices": graph.num_vertices,
        "num_edges": graph.num_edges,
        "max_degree": graph.max_degree(),
        "adjacency_matrix": graph.adjacency_matrix(),
        "welsh_powell_assignment": wp_result.assignment,
        "color_classes": wp_result.color_classes,
        "num_colors_used": wp_result.num_colors,
        "is_valid_proper_coloring": verif.is_valid_proper_coloring,
    }
