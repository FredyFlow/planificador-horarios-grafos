"""Núcleo matemático-discreto: Grafos de conflictos, algoritmos de coloración y verificador formal."""

from .coloring import ColoringResult, ColoringStep, DSaturColoring, WelshPowellColoring
from .graph import ConflictGraph
from .verifier import FormalVerificationReport, verify_coloring

__all__ = [
    "ConflictGraph",
    "ColoringStep",
    "ColoringResult",
    "WelshPowellColoring",
    "DSaturColoring",
    "FormalVerificationReport",
    "verify_coloring",
]
