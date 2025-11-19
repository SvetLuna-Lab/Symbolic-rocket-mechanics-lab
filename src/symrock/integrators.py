# src/symrock/integrators.py
"""
Numeric integrators for the 1D vertical rocket model.

We use a simple explicit Runge–Kutta 4 (RK4) scheme on a uniform
time grid for the state:

    y = [h, v, m]

where
    h(t) — altitude,
    v(t) — vertical velocity,
    m(t) — mass.

Equations (consistent with rocket_1d.py):

    dh/dt = v
    dv/dt = (T - D(t, h, v, m) - m * g) / m
    dm/dt = -mdot

This is a teaching-oriented integrator, not a production flight
dynamics solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

import numpy as np


DragFn = Callable[[float, float, float, float], float]


@dataclass
class RocketParams:
    """
    Numeric parameters for the vertical rocket integration.

    Attributes
    ----------
    T : float
        Thrust [N].
    g : float
        Gravitational acceleration [m/s^2], e.g. 9.80665.
    mdot : float
        Mass flow rate [kg/s]. The mass decreases as dm/dt = -mdot.
    drag_fn : callable or None
        Optional drag model D(t, h, v, m) [N]. If None, drag is set to 0.
    """

    T: float
    g: float
    mdot: float
    drag_fn: DragFn | None = None

    def eval_drag(self, t: float, h: float, v: float, m: float) -> float:
        """Evaluate drag term or return 0.0 if drag_fn is not set."""
        if self.drag_fn is None:
            return 0.0
        return float(self.drag_fn(t, h, v, m))


def rocket_rhs(t: float, y: np.ndarray, params: RocketParams) -> np.ndarray:
    """
    Right-hand side of the 1D vertical rocket ODE system.

    Parameters
    ----------
    t : float
        Current time.
    y : ndarray, shape (3,)
        Current state [h, v, m].
    params : RocketParams
        Numeric parameters (T, g, mdot, drag_fn).

    Returns
    -------
    ndarray, shape (3,)
        Time derivative dy/dt = [dh/dt, dv/dt, dm/dt].
    """
    h, v, m = y

    # Once mass is depleted, freeze the state.
    if m <= 0.0:
        return np.array([0.0, 0.0, 0.0], dtype=float)

    D = params.eval_drag(t, h, v, m)

    dhdt = v
    dvdt = (params.T - D - m * params.g) / m
    dmdt = -params.mdot

    return np.array([dhdt, dvdt, dmdt], dtype=float)


def integrate_vertical_rocket(
    t0: float,
    t_end: float,
    dt: float,
    h0: float,
    v0: float,
    m0: float,
    params: RocketParams,
) -> Dict[str, np.ndarray]:
    """
    Integrate the 1D vertical rocket model using RK4 on a uniform grid.

    Parameters
    ----------
    t0 : float
        Initial time [s].
    t_end : float
        Final time [s]. Must satisfy t_end > t0.
    dt : float
        Time step [s]. Must be positive.
    h0 : float
        Initial altitude [m].
    v0 : float
        Initial vertical velocity [m/s].
    m0 : float
        Initial mass [kg].
    params : RocketParams
        Numeric parameters for the rocket.

    Returns
    -------
    dict
        {
          "t": ndarray,  # time nodes
          "h": ndarray,  # altitude profile
          "v": ndarray,  # velocity profile
          "m": ndarray,  # mass profile
        }
    """
    if dt <= 0.0:
        raise ValueError("Time step dt must be positive.")
    if t_end <= t0:
        raise ValueError("t_end must be greater than t0.")

    n_steps = int(np.floor((t_end - t0) / dt)) + 1
    t = t0 + np.arange(n_steps) * dt

    h = np.zeros(n_steps, dtype=float)
    v = np.zeros(n_steps, dtype=float)
    m = np.zeros(n_steps, dtype=float)

    h[0] = float(h0)
    v[0] = float(v0)
    m[0] = float(m0)

    for i in range(n_steps - 1):
        y = np.array([h[i], v[i], m[i]], dtype=float)

        # If mass is exhausted, freeze the state for remaining steps.
        if m[i] <= 0.0:
            h[i + 1 :] = h[i]
            v[i + 1 :] = 0.0
            m[i + 1 :] = 0.0
            break

        ti = t[i]

        k1 = rocket_rhs(ti, y, params)
        k2 = rocket_rhs(ti + 0.5 * dt, y + 0.5 * dt * k1, params)
        k3 = rocket_rhs(ti + 0.5 * dt, y + 0.5 * dt * k2, params)
        k4 = rocket_rhs(ti + dt, y + dt * k3, params)

        y_next = y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        h[i + 1], v[i + 1], m[i + 1] = y_next

    return {"t": t, "h": h, "v": v, "m": m}
