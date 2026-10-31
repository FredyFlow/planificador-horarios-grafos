"""
Cargador de eventos académicos y restricciones desde archivos JSON o CSV,
además del generador del Ejemplo Mínimo Trabajado (6 asignaturas de la ESPOCH).
"""

import csv
import io
import json
from typing import List
from src.models.course import CourseEvent


def get_worked_example_6_courses() -> List[CourseEvent]:
    """
    Retorna la instancia canónica de 6 asignaturas de Ingeniería de Software (ESPOCH)
    empleada en la Sección de Ejemplo Mínimo Trabajado de la Investigación Formativa.
    """
    return [
        CourseEvent(
            id="v1",
            name="Matemáticas Discretas",
            professor="Mg. Miriam Ávila",
            semester="PAO 3",
            room="Aula 301",
            student_groups=("SW-3A",),
        ),
        CourseEvent(
            id="v2",
            name="Estructura de Datos",
            professor="Ing. Carlos Pérez",
            semester="PAO 3",
            room="Lab Cómputo 1",
            student_groups=("SW-3A",),
        ),
        CourseEvent(
            id="v3",
            name="Programación Orientada a Objetos",
            professor="Ing. Carlos Pérez",
            semester="PAO 2",
            room="Lab Cómputo 1",
            student_groups=("SW-2A",),
        ),
        CourseEvent(
            id="v4",
            name="Bases de Datos I",
            professor="Ing. Elena Torres",
            semester="PAO 3",
            room="Lab Cómputo 2",
            student_groups=("SW-3A",),
        ),
        CourseEvent(
            id="v5",
            name="Lógica de Programación",
            professor="Mg. Miriam Ávila",
            semester="PAO 1",
            room="Aula 201",
            student_groups=("SW-1A",),
        ),
        CourseEvent(
            id="v6",
            name="Estadística Aplicada",
            professor="Ing. Elena Torres",
            semester="PAO 2",
            room="Aula 301",
            student_groups=("SW-2A",),
        ),
    ]


def load_courses_from_json(json_content: str) -> List[CourseEvent]:
    """Parsea una cadena JSON con una lista de asignaturas."""
    raw = json.loads(json_content)
    items = raw.get("courses", raw) if isinstance(raw, dict) else raw
    courses: List[CourseEvent] = []
    for item in items:
        groups = item.get("student_groups", [])
        if isinstance(groups, str):
            groups = [g.strip() for g in groups.split(";") if g.strip()]
        courses.append(
            CourseEvent(
                id=str(item["id"]).strip(),
                name=str(item["name"]).strip(),
                professor=str(item.get("professor", "")).strip(),
                semester=str(item.get("semester", "")).strip(),
                room=str(item.get("room", "")).strip(),
                student_groups=tuple(groups),
            )
        )
    return courses


def load_courses_from_csv(csv_content: str) -> List[CourseEvent]:
    """Parsea una cadena CSV con encabezados: id,name,professor,semester,room,student_groups."""
    reader = csv.DictReader(io.StringIO(csv_content.strip()))
    courses: List[CourseEvent] = []
    for row in reader:
        raw_groups = row.get("student_groups", "") or ""
        groups = [g.strip() for g in raw_groups.split(";") if g.strip()]
        courses.append(
            CourseEvent(
                id=str(row["id"]).strip(),
                name=str(row["name"]).strip(),
                professor=str(row.get("professor", "")).strip(),
                semester=str(row.get("semester", "")).strip(),
                room=str(row.get("room", "")).strip(),
                student_groups=tuple(groups),
            )
        )
    return courses
