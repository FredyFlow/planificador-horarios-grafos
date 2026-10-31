"""
Representación formal de asignaturas/eventos y predicado lógico de conflicto.

Modelo Matemático Discreto:
Cada asignatura se modela como una tupla con atributos discretos:
    v_i = (id, nombre, docente, semestre_pao, recurso_aula, grupos)

El predicado binario de conflicto P(u, v) para u != v se define como:
    P(u, v) <=> (doc(u) == doc(v)) v (pao(u) == pao(v)) v (aula(u) == aula(v)) v (grupos(u) n grupos(v) != 0)
"""

from dataclasses import dataclass, field
from typing import List, Set, Tuple


@dataclass(frozen=True)
class CourseEvent:
    """
    Representa un vértice v in V del grafo de conflictos académicos.
    """

    id: str
    name: str
    professor: str
    semester: str
    room: str
    student_groups: Tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "professor": self.professor,
            "semester": self.semester,
            "room": self.room,
            "student_groups": list(self.student_groups),
        }


@dataclass(frozen=True)
class ConflictDetail:
    """
    Representa una arista e = {u, v} in E junto con las proposiciones atómicas
    que justifican la incompatibilidad de simultaneidad.
    """

    u_id: str
    v_id: str
    reasons: Tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "u": self.u_id,
            "v": self.v_id,
            "reasons": list(self.reasons),
        }


def evaluate_conflict_predicate(u: CourseEvent, v: CourseEvent) -> Tuple[bool, List[str]]:
    """
    Evalúa formalmente el predicado lógico de conflicto P(u, v):
        P(u, v) <=> (u != v) ^ (p_doc v p_sem v p_room v p_grp)

    Donde:
        - p_doc: u y v comparten el mismo docente.
        - p_sem: u y v pertenecen al mismo nivel/semestre (PAO) y paralelo.
        - p_room: u y v requieren simultáneamente el mismo laboratorio/aula específica.
        - p_grp: la intersección de grupos estudiantiles de u y v no es vacía.

    Retorna:
        (es_conflicto: bool, razones: List[str])
    """
    if u.id == v.id:
        # Propiedad de irreflexividad: una asignatura no tiene arista consigo misma (grafo simple sin lazos)
        return False, []

    reasons: List[str] = []

    if u.professor.strip().lower() == v.professor.strip().lower() and u.professor.strip():
        reasons.append(f"Mismo docente ({u.professor})")

    if u.semester.strip().lower() == v.semester.strip().lower() and u.semester.strip():
        reasons.append(f"Mismo nivel/PAO ({u.semester})")

    if u.room.strip().lower() == v.room.strip().lower() and u.room.strip():
        reasons.append(f"Misma aula/laboratorio ({u.room})")

    set_u: Set[str] = {g.strip().lower() for g in u.student_groups if g.strip()}
    set_v: Set[str] = {g.strip().lower() for g in v.student_groups if g.strip()}
    shared_groups = set_u.intersection(set_v)
    if shared_groups:
        reasons.append(f"Grupos compartidos ({', '.join(sorted(shared_groups))})")

    return len(reasons) > 0, reasons
