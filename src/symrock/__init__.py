# src/symrock/__init__.py
"""
symrock: SymPy-based 1D rocket mechanics lab.

This package currently provides:
- vertical_rocket_equations() – symbolic 1D equations of motion,
- tsiolkovsky_delta_v(...)   – ideal rocket Δv formula,
- VerticalRocketModel        – small container for the symbolic model.
"""

from .rocket_1d import (
    t,
    h,
    v,
    m,
    g,
    T,
    D,
    mdot,
    vertical_rocket_equations,
    tsiolkovsky_delta_v,
    VerticalRocketModel,
)

__all__ = [
    "t",
    "h",
    "v",
    "m",
    "g",
    "T",
    "D",
    "mdot",
    "vertical_rocket_equations",
    "tsiolkovsky_delta_v",
    "VerticalRocketModel",
]
