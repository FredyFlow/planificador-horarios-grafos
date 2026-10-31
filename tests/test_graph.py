"""
Avance Preliminar (Fase 3): Pruebas unitarias iniciales del grafo de conflictos G = (V, E).
"""

import unittest
from src.core.graph import ConflictGraph
from src.models.course import CourseEvent
from src.utils.loader import get_worked_example_6_courses


def test_worked_example_graph_structure() -> None:
    """
    Verifica que el ejemplo trabajado de 6 asignaturas de la ESPOCH construya
    exactamente |V| = 6, |E| = 8 y Delta(G) = 4.
    """
    courses = get_worked_example_6_courses()
    graph = ConflictGraph.from_courses(courses)

    assert graph.num_vertices == 6
    assert graph.num_edges == 8
    assert graph.max_degree() == 4

    expected_degrees = {
        "v1": 4,
        "v2": 3,
        "v3": 2,
        "v4": 3,
        "v5": 1,
        "v6": 3,
    }
    assert graph.degree_sequence() == expected_degrees

    matrix = graph.adjacency_matrix()
    assert len(matrix) == 6
    for i in range(6):
        assert matrix[i][i] == 0
        for j in range(6):
            assert matrix[i][j] == matrix[j][i]


def test_irreflexive_and_symmetric_invariants() -> None:
    """Verifica que un grafo simple rechace lazos (u == v) y mantenga simetría."""
    g = ConflictGraph()
    g.add_vertex(CourseEvent("A", "Curso A", "Doc 1", "PAO 1", "Aula 1"))
    g.add_vertex(CourseEvent("B", "Curso B", "Doc 2", "PAO 2", "Aula 2"))

    raised = False
    try:
        g.add_edge("A", "A")
    except ValueError:
        raised = True
    assert raised is True

    g.add_edge("A", "B", ["Conflicto manual"])
    assert g.are_adjacent("A", "B") is True
    assert g.are_adjacent("B", "A") is True

    # Verificar validación de clave única en add_vertex
    duplicate_raised = False
    try:
        g.add_vertex(CourseEvent("A", "Duplicado", "Doc 1", "PAO 1", "Aula 1"))
    except ValueError:
        duplicate_raised = True
    assert duplicate_raised is True


def test_predicate_irreflexivity_and_symmetry() -> None:
    """
    Verifica directamente sobre evaluate_conflict_predicate(u, v) las propiedades
    de irreflexividad P(v, v) == False y simetría P(u, v) == P(v, u).
    """
    from src.models.course import evaluate_conflict_predicate

    courses = get_worked_example_6_courses()
    for u in courses:
        has_self_conflict, _ = evaluate_conflict_predicate(u, u)
        assert has_self_conflict is False
        for v in courses:
            c_uv, _ = evaluate_conflict_predicate(u, v)
            c_vu, _ = evaluate_conflict_predicate(v, u)
            assert c_uv == c_vu


class TestGraphUnittest(unittest.TestCase):
    def test_worked_example(self) -> None:
        test_worked_example_graph_structure()

    def test_invariants(self) -> None:
        test_irreflexive_and_symmetric_invariants()

    def test_predicate_properties(self) -> None:
        test_predicate_irreflexivity_and_symmetry()


if __name__ == "__main__":
    unittest.main()
