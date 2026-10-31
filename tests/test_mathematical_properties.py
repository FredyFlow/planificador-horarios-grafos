"""
Avance Preliminar (Fase 3): Pruebas de carga de datasets JSON/CSV.

TODO (Sprint 3 - Rol: QA Engineer / Danixa Rodas):
Incorporar la prueba sobre el Grafo Corona Bipartito S_3^0 = K_{3,3} \\ M para demostrar
empíricamente la ventaja del grado de saturación dinámico d_sat(v) de DSatur.
"""

import unittest
from pathlib import Path
from src.core.graph import ConflictGraph
from src.utils.loader import load_courses_from_csv, load_courses_from_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def test_json_and_csv_loaders_produce_identical_graphs() -> None:
    """
    Verifica que los datasets JSON y CSV de 6 asignaturas produzcan exactamente
    el mismo grafo G = (V, E) y la misma matriz de adyacencia A_G.
    """
    json_text = (DATA_DIR / "dataset_espoch_6_asignaturas.json").read_text(encoding="utf-8")
    csv_text = (DATA_DIR / "dataset_espoch_6_asignaturas.csv").read_text(encoding="utf-8")

    g_json = ConflictGraph.from_courses(load_courses_from_json(json_text))
    g_csv = ConflictGraph.from_courses(load_courses_from_csv(csv_text))

    assert g_json.adjacency_matrix() == g_csv.adjacency_matrix()
    assert g_json.degree_sequence() == g_csv.degree_sequence()


class TestMathematicalPropertiesPreliminaryUnittest(unittest.TestCase):
    def test_loaders(self) -> None:
        test_json_and_csv_loaders_produce_identical_graphs()


if __name__ == "__main__":
    unittest.main()
