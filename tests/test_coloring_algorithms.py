"""
Avance Preliminar (Fase 3): Prueba de simulación del algoritmo Welsh-Powell sobre
el Ejemplo Mínimo Trabajado de 6 asignaturas.

TODO (Sprint 2 - Rol: QA Engineer / Danixa Rodas):
Añadir las pruebas comparativas con DSatur y los casos de borde matemáticos
(grafo completo K_5, grafo nulo E=0 y ciclo impar C_5).
"""

import unittest
from src.core.coloring import WelshPowellColoring
from src.core.graph import ConflictGraph
from src.core.verifier import verify_coloring
from src.utils.loader import get_worked_example_6_courses


def test_preliminary_worked_example_welsh_powell() -> None:
    """
    Comprueba que el prototipo de Welsh-Powell resuelve el ejemplo trabajado
    de 6 asignaturas con k = 3 colores libres de conflictos.
    """
    graph = ConflictGraph.from_courses(get_worked_example_6_courses())
    wp_res = WelshPowellColoring.solve(graph)

    assert wp_res.num_colors == 3
    assert wp_res.color_classes == {
        1: ["v1", "v3"],
        2: ["v2", "v6", "v5"],
        3: ["v4"],
    }

    report = verify_coloring(graph, wp_res)
    assert report.is_valid_proper_coloring is True
    assert report.satisfies_handshaking_lemma is True
    assert report.satisfies_upper_bound is True


class TestColoringPreliminaryUnittest(unittest.TestCase):
    def test_worked_example_wp(self) -> None:
        test_preliminary_worked_example_welsh_powell()


if __name__ == "__main__":
    unittest.main()
