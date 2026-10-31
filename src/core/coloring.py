"""
Avance Preliminar (Fase 3): Simulación base de Coloración de Grafos.

En esta fase de Investigación Formativa se incluye el prototipo funcional del
algoritmo voraz de Welsh-Powell (1967) para validar el Ejemplo Mínimo Trabajado
de 6 asignaturas de la ESPOCH. El algoritmo dinámico DSatur (Brélaz, 1979) queda
estructurado para su implementación completa en el Sprint 2.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from .graph import ConflictGraph


@dataclass
class ColoringStep:
    """Representa un paso en la traza de ejecución del algoritmo de coloración."""

    step_number: int
    vertex_id: str
    assigned_color: int
    vertex_degree: int
    saturation_degree: int
    neighbor_colors: List[int]
    explanation: str


@dataclass
class ColoringResult:
    """Resultado de la ejecución de un algoritmo de coloración sobre G = (V, E)."""

    algorithm_name: str
    assignment: Dict[str, int]
    color_classes: Dict[int, List[str]]
    num_colors: int
    steps: List[ColoringStep] = field(default_factory=list)
    initial_vertex_order: List[str] = field(default_factory=list)


class WelshPowellColoring:
    """
    Prototipo preliminar del Algoritmo de Welsh-Powell (1967) por orden decreciente de grado.
    Complejidad temporal: O(|V|^2). Complejidad espacial: O(|V| + |E|).
    """

    @staticmethod
    def solve(graph: ConflictGraph) -> ColoringResult:
        vertices = graph.vertices
        if not vertices:
            return ColoringResult("Welsh-Powell", {}, {}, 0)

        order_index = {v_id: idx for idx, v_id in enumerate(vertices)}
        degrees = graph.degree_sequence()

        # Ordenar por grado decreciente deg_G(v)
        sorted_vertices = sorted(
            vertices,
            key=lambda v_id: (-degrees[v_id], order_index[v_id]),
        )

        assignment: Dict[str, int] = {}
        color_classes: Dict[int, List[str]] = {}
        steps: List[ColoringStep] = []
        current_color = 0
        step_counter = 0

        while len(assignment) < len(sorted_vertices):
            current_color += 1
            color_classes[current_color] = []

            for v_id in sorted_vertices:
                if v_id in assignment:
                    continue

                has_conflict_in_class = any(
                    graph.are_adjacent(v_id, u_id) for u_id in color_classes[current_color]
                )
                if not has_conflict_in_class:
                    step_counter += 1
                    neighbor_colors = sorted(
                        {assignment[nb] for nb in graph.neighbors(v_id) if nb in assignment}
                    )
                    assignment[v_id] = current_color
                    color_classes[current_color].append(v_id)
                    steps.append(
                        ColoringStep(
                            step_number=step_counter,
                            vertex_id=v_id,
                            assigned_color=current_color,
                            vertex_degree=degrees[v_id],
                            saturation_degree=len(neighbor_colors),
                            neighbor_colors=neighbor_colors,
                            explanation=f"Asignado a clase independiente C_{current_color}.",
                        )
                    )

        ordered_assignment = {v_id: assignment[v_id] for v_id in vertices}
        return ColoringResult(
            algorithm_name="Welsh-Powell",
            assignment=ordered_assignment,
            color_classes=color_classes,
            num_colors=current_color,
            steps=steps,
            initial_vertex_order=sorted_vertices,
        )


class DSaturColoring:
    """
    Esqueleto para el Algoritmo DSatur (Degree of Saturation - Brélaz, 1979).
    """

    @staticmethod
    def solve(graph: ConflictGraph) -> ColoringResult:
        # TODO (Sprint 2 - Rol: Desarrollador de Algoritmos / Joseph Cuñas):
        # Implementar la selección dinámica del vértice con máximo grado de saturación
        # d_sat(v) = |{c(u) | u in N_G(v) \ U}| (donde U es el conjunto de vértices no coloreados)
        # con desempate por grado deg_G(v).
        raise NotImplementedError(
            "El algoritmo DSatur está programado para implementarse en el Sprint 2."
        )
