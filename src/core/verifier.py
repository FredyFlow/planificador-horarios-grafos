"""
Avance Preliminar (Fase 3): Verificador básico de propiedades matemáticas.
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from .coloring import ColoringResult
from .graph import ConflictGraph


@dataclass
class FormalVerificationReport:
    """Reporte preliminar de verificación de la coloración."""

    algorithm_name: str
    is_valid_proper_coloring: bool
    satisfies_handshaking_lemma: bool
    satisfies_upper_bound: bool
    num_colors_used: int
    delta_plus_one_upper_bound: int
    violating_edges: List[Tuple[str, str]] = field(default_factory=list)


def verify_coloring(graph: ConflictGraph, result: ColoringResult) -> FormalVerificationReport:
    """
    Verifica preliminarmente:
    1. Lema del Apretón de Manos: sum deg_G(v) = 2|E|.
    2. Condición de coloración propia: para toda {u, v} in E, c(u) != c(v).
    3. Cota superior de grado máximo: k <= Delta(G) + 1 (Proposición 3.2).

    TODO (Sprint 2 - Rol: QA Engineer / Danixa Rodas):
    Agregar verificación formal de partición en conjuntos independientes (Proposición 3.1)
    y certificado de optimalidad con el número de clique omega(G) (Proposición 3.3).
    """
    sum_degrees = sum(graph.degree_sequence().values())
    handshaking_ok = sum_degrees == 2 * graph.num_edges

    violating_edges: List[Tuple[str, str]] = []
    for conflict in graph.get_all_conflicts():
        u, v = conflict.u_id, conflict.v_id
        if result.assignment.get(u) == result.assignment.get(v):
            violating_edges.append((u, v))

    proper_ok = len(violating_edges) == 0 and len(result.assignment) == graph.num_vertices
    upper_bound = (graph.max_degree() + 1) if graph.num_vertices > 0 else 0
    upper_ok = result.num_colors <= upper_bound

    return FormalVerificationReport(
        algorithm_name=result.algorithm_name,
        is_valid_proper_coloring=proper_ok,
        satisfies_handshaking_lemma=handshaking_ok,
        satisfies_upper_bound=upper_ok,
        num_colors_used=result.num_colors,
        delta_plus_one_upper_bound=upper_bound,
        violating_edges=violating_edges,
    )
