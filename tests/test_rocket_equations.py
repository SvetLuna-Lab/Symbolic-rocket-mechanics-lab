# tests/test_rocket_equations.py
"""
Basic tests for the symbolic 1D rocket mechanics lab.

We check:
- structure of the vertical rocket equations (dh/dt, dv/dt, dm/dt);
- Tsiolkovsky Δv formula for simple numeric values.
"""

import sympy as sp
import numpy as np

from symrock import (
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
)


def test_vertical_rocket_equations_structure():
    """Ensure that the vertical rocket equations have the expected form."""
    eqs = vertical_rocket_equations()

    # dh/dt = v
    eq_h = eqs["h_dot"]
    assert eq_h.lhs == sp.diff(h, t)
    assert eq_h.rhs == v

    # dv/dt = (T - D(t) - m*g)/m
    eq_v = eqs["v_dot"]
    assert eq_v.lhs == sp.diff(v, t)

    rhs_v = sp.simplify(eq_v.rhs * m)  # multiply both sides by m
    # Now: m * dv/dt = T - D - m * g   (up to algebraic equivalence)
    expected_rhs = T - D - m * g
    assert sp.simplify(rhs_v - expected_rhs) == 0

    # dm/dt = -mdot
    eq_m = eqs["m_dot"]
    assert eq_m.lhs == sp.diff(m, t)
    assert eq_m.rhs == -mdot


def test_tsiolkovsky_delta_v_numeric():
    """
    Check that Tsiolkovsky Δv matches the standard formula:

        Δv = Isp * g0 * ln(m0 / mf)
    """
    Isp_val = 300.0      # s
    g0_val = 9.80665     # m/s^2
    m0_val = 500.0       # kg (wet)
    mf_val = 200.0       # kg (dry)

    dv_expr = tsiolkovsky_delta_v(Isp_val, g0_val, m0_val, mf_val)
    dv_num = float(sp.N(dv_expr))

    dv_expected = Isp_val * g0_val * np.log(m0_val / mf_val)

    assert np.isclose(dv_num, dv_expected, rtol=1e-10, atol=1e-10)
    assert dv_num > 0.0
