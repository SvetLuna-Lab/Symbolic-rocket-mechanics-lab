# src/symrock/rocket_1d.py
"""
Symbolic 1D vertical rocket mechanics using SymPy.

This module focuses on a minimal point-mass rocket model:
- vertical motion h(t), velocity v(t), mass m(t),
- thrust T, gravity g, optional generic drag D,
- mass flow rate mdot (m decreases linearly with time),
- Tsiolkovsky rocket equation for ideal Δv.

It is deliberately simple: a starting point for teaching and experiments,
not a full-flight simulation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import sympy as sp

# Time variable
t = sp.symbols("t", real=True)

# State variables as functions of time
h = sp.Function("h")(t)  # altitude
v = sp.Function("v")(t)  # vertical velocity
m = sp.Function("m")(t)  # mass

# Parameters
g = sp.symbols("g", positive=True)       # gravitational acceleration
T = sp.symbols("T", real=True)          # thrust (can be > 0 or 0)
D = sp.Function("D")(t)                 # generic drag term D(t) ≥ 0

mdot = sp.symbols("mdot", positive=True)  # mass flow rate (|dm/dt|)


def vertical_rocket_equations() -> Dict[str, sp.Eq]:
    """
    Return the symbolic 1D vertical rocket equations as SymPy Eq objects.

    Model:
        - h(t): altitude
        - v(t): vertical velocity
        - m(t): mass
        - g: gravity (constant)
        - T: thrust (constant for this simple model)
        - D(t): drag term (generic function of time)
        - mdot: mass flow rate (positive scalar)

    Equations:
        dh/dt = v
        dv/dt = (T - D(t) - m*g) / m
        dm/dt = -mdot

    Returns
    -------
    dict
        {
          "h_dot":  Eq(dh/dt, v),
          "v_dot":  Eq(dv/dt, (T - D(t) - m*g) / m),
          "m_dot":  Eq(dm/dt, -mdot),
        }
    """
    h_dot = sp.diff(h, t)
    v_dot = sp.diff(v, t)
    m_dot = sp.diff(m, t)

    eq_h = sp.Eq(h_dot, v)
    eq_v = sp.Eq(v_dot, (T - D - m * g) / m)
    eq_m = sp.Eq(m_dot, -mdot)

    return {"h_dot": eq_h, "v_dot": eq_v, "m_dot": eq_m}


def tsiolkovsky_delta_v(Isp: sp.Symbol | float,
                        g0: sp.Symbol | float,
                        m0: sp.Symbol | float,
                        mf: sp.Symbol | float) -> sp.Expr:
    """
    Tsiolkovsky rocket equation for ideal Δv in vacuum:

        Δv = Isp * g0 * ln(m0 / mf),

    where
        Isp — specific impulse [s],
        g0  — reference gravity (usually 9.80665 m/s²),
        m0  — initial mass (wet mass),
        mf  — final mass  (dry mass).

    The function returns a SymPy expression that can be evaluated
    numerically via .subs(...) or sp.N(...).

    Parameters
    ----------
    Isp : float or SymPy symbol
        Specific impulse [s].
    g0  : float or SymPy symbol
        Reference gravitational acceleration [m/s^2].
    m0  : float or SymPy symbol
        Initial mass (must be > mf).
    mf  : float or SymPy symbol
        Final mass after propellant burnout.

    Returns
    -------
    sympy.Expr
        Δv expression Isp * g0 * log(m0 / mf).
    """
    Isp_sym = sp.sympify(Isp)
    g0_sym = sp.sympify(g0)
    m0_sym = sp.sympify(m0)
    mf_sym = sp.sympify(mf)

    return Isp_sym * g0_sym * sp.log(m0_sym / mf_sym)


@dataclass
class VerticalRocketModel:
    """
    Lightweight container for the 1D vertical rocket model.

    This class does not solve the equations; it just collects
    the key symbolic objects in one place.

    Attributes
    ----------
    t : SymPy symbol
        Time variable.
    h : SymPy function of t
        Altitude h(t).
    v : SymPy function of t
        Velocity v(t).
    m : SymPy function of t
        Mass m(t).
    g : SymPy symbol
        Gravity constant.
    T : SymPy symbol
        Thrust.
    D : SymPy function of t
        Drag term.
    mdot : SymPy symbol
        Mass flow rate (|dm/dt|).
    equations : dict
        Dictionary of SymPy Eq objects for dh/dt, dv/dt, dm/dt.
    """

    t: sp.Symbol = t
    h: sp.Expr = h
    v: sp.Expr = v
    m: sp.Expr = m
    g: sp.Symbol = g
    T: sp.Symbol = T
    D: sp.Expr = D
    mdot: sp.Symbol = mdot
    equations: Dict[str, sp.Eq] = None

    def __post_init__(self) -> None:
        if self.equations is None:
            self.equations = vertical_rocket_equations()
