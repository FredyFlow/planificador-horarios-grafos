"""
Avance Preliminar (Fase 3): Estructura base del Grafo Simple No Dirigido G = (V, E).

Definición Formal:
    Un grafo simple no dirigido es un par ordenado G = (V, E), donde:
    - V = {v_1, v_2, ..., v_n} es un conjunto finito no vacío de vértices (asignaturas).
    - E subseteq {{u, v} subseteq V | u != v} es un conjunto de pares no ordenados de vértices
      distintos llamados aristas (conflictos de simultaneidad).
"""

from typing import Dict, List, Optional, Set, Tuple
from src.models.course import ConflictDetail, CourseEvent, evaluate_conflict_predicate


class ConflictGraph:
    """
    Estructura de datos algebraica para representar el grafo de conflictos G = (V, E).
    Implementada desde cero sin librerías externas de grafos.
    """

    def __init__(self) -> None:
        self._vertex_order: List[str] = []
        self._vertices: Dict[str, CourseEvent] = {}
        self._adj_list: Dict[str, Set[str]] = {}
        self._conflicts: Dict[Tuple[str, str], ConflictDetail] = {}

    @property
    def vertices(self) -> List[str]:
        """Retorna la lista ordenada de identificadores de vértices V."""
        return list(self._vertex_order)

    @property
    def num_vertices(self) -> int:
        """Orden del grafo: |V| = n."""
        return len(self._vertex_order)

    @property
    def num_edges(self) -> int:
        """Tamaño del grafo: |E| = m."""
        return len(self._conflicts)

    def add_vertex(self, course: CourseEvent) -> None:
        """
        Inserta un vértice v en el conjunto V validando unicidad de clave.
        Lanza ValueError si el identificador ya fue registrado en V.
        """
        if course.id in self._vertices:
            raise ValueError(f"El vértice '{course.id}' ya pertenece al conjunto V.")
        self._vertex_order.append(course.id)
        self._adj_list[course.id] = set()
        self._vertices[course.id] = course

    def add_edge(self, u_id: str, v_id: str, reasons: Optional[List[str]] = None) -> None:
        """
        Inserta una arista no dirigida e = {u, v} en E garantizando irreflexividad y simetría.
        """
        if u_id == v_id:
            raise ValueError("Un grafo simple no admite lazos (u != v).")
        if u_id not in self._vertices or v_id not in self._vertices:
            raise KeyError("Ambos vértices deben pertenecer previamente a V.")

        self._adj_list[u_id].add(v_id)
        self._adj_list[v_id].add(u_id)

        canonical_key = (u_id, v_id) if u_id < v_id else (v_id, u_id)
        edge_reasons = tuple(reasons) if reasons else ("Conflicto explícito",)
        self._conflicts[canonical_key] = ConflictDetail(
            u_id=canonical_key[0],
            v_id=canonical_key[1],
            reasons=edge_reasons,
        )

    def build_conflicts_from_predicates(self) -> None:
        """
        Construye el conjunto de aristas E evaluando el predicado P(u, v) sobre todos
        los pares {u, v} subseteq V en tiempo O(|V|^2).
        """
        self._conflicts.clear()
        for v_id in self._vertex_order:
            self._adj_list[v_id].clear()

        n = len(self._vertex_order)
        for i in range(n):
            u_id = self._vertex_order[i]
            u_course = self._vertices[u_id]
            for j in range(i + 1, n):
                v_id = self._vertex_order[j]
                v_course = self._vertices[v_id]
                has_conflict, reasons = evaluate_conflict_predicate(u_course, v_course)
                if has_conflict:
                    self.add_edge(u_id, v_id, reasons)

    def neighbors(self, vertex_id: str) -> Set[str]:
        """Retorna la vecindad abierta N_G(v)."""
        return set(self._adj_list[vertex_id])

    def are_adjacent(self, u_id: str, v_id: str) -> bool:
        """Verifica si {u, v} in E en O(1) promedio."""
        return v_id in self._adj_list.get(u_id, set())

    def degree(self, vertex_id: str) -> int:
        """Retorna el grado deg_G(v) = |N_G(v)|."""
        return len(self._adj_list[vertex_id])

    def degree_sequence(self) -> Dict[str, int]:
        """Retorna el diccionario {v: deg_G(v)} para todo v in V."""
        return {v_id: len(self._adj_list[v_id]) for v_id in self._vertex_order}

    def max_degree(self) -> int:
        """Retorna el grado máximo Delta(G) = max_{v in V} deg_G(v)."""
        if not self._vertex_order:
            return 0
        return max(len(self._adj_list[v_id]) for v_id in self._vertex_order)

    def adjacency_matrix(self) -> List[List[int]]:
        """Construye la Matriz de Adyacencia simétrica A_G de dimensión n x n."""
        n = len(self._vertex_order)
        matrix: List[List[int]] = [[0] * n for _ in range(n)]
        for i, u_id in enumerate(self._vertex_order):
            for j, v_id in enumerate(self._vertex_order):
                if v_id in self._adj_list[u_id]:
                    matrix[i][j] = 1
        return matrix

    def get_all_conflicts(self) -> List[ConflictDetail]:
        """Retorna la lista de conflictos registrados en E."""
        return list(self._conflicts.values())

    @classmethod
    def from_courses(cls, courses: List[CourseEvent]) -> "ConflictGraph":
        """Instancia G = (V, E) a partir de una lista de asignaturas."""
        graph = cls()
        for course in courses:
            graph.add_vertex(course)
        graph.build_conflicts_from_predicates()
        return graph

    # TODO (Sprint 2 - Rol: Matemático / Giovanni Gavilanes):
    # Implementar el método `find_maximum_clique()` mediante Bron-Kerbosch con pivoteo
    # para calcular la cota inferior exacta omega(G) <= chi(G) (Proposición 3.3).
