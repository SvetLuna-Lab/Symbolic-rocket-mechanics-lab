# Symbolic Rocket Mechanics Lab

Small **SymPy-based lab** for 1D vertical rocket mechanics.

The goal is to keep the model simple and transparent:

- symbolic equations of motion for a point-mass rocket in vertical flight;
- explicit Tsiolkovsky Δv formula as a SymPy expression;
- a clean starting point for teaching, experiments and further extensions
  (staging, drag models, numeric integrators).

This is not a full flight simulator. It is a symbolic “workbench”
for rocket intuition.

---

## Features

- **1D vertical rocket model**
  - altitude h(t), velocity v(t), mass m(t);
  - thrust T, gravity g, generic drag term D(t);
  - mass flow rate mdot with dm/dt = −mdot.

- **Symbolic equations of motion**
  - `vertical_rocket_equations()` returns:

    - dh/dt = v  
    - dv/dt = (T − D(t) − m g) / m  
    - dm/dt = −mdot

- **Tsiolkovsky rocket equation**
  - `tsiolkovsky_delta_v(Isp, g0, m0, mf)` returns a SymPy expression:
    \[
      \Delta v = I_{sp} \, g_0 \ln\left(\frac{m_0}{m_f}\right)
    \]
  - can be evaluated symbolically or numerically.

- **Small model container**
  - `VerticalRocketModel` gathers the key symbols and equations in one place.

---

## Project structure

```text
symbolic-rocket-mechanics-lab/
├─ src/
│  └─ symrock/
│     ├─ __init__.py         # package entry point
│     └─ rocket_1d.py        # symbolic 1D rocket model and Δv
├─ tests/
│  └─ test_rocket_equations.py  # basic checks for EOM and Δv
└─ README.md


Later this can be extended with:

integrators.py (numeric integration, e.g. with SciPy or custom schemes),

plots.py (altitude/velocity/acceleration vs time),

Jupyter notebooks for derivations and scenarios (staging, drag, etc.),

docs/Overview_EN.md / Overview_RU.md.


Quick start (symbolic)

import sympy as sp
from symrock import (
    t, h, v, m, g, T, D, mdot,
    vertical_rocket_equations,
    tsiolkovsky_delta_v,
)

# Get the equations of motion
eqs = vertical_rocket_equations()
print(eqs["h_dot"])  # dh/dt = v
print(eqs["v_dot"])  # dv/dt = (T - D(t) - m*g) / m
print(eqs["m_dot"])  # dm/dt = -mdot

# Tsiolkovsky Δv
Isp_val = 300.0
g0_val = 9.80665
m0_val = 500.0
mf_val = 200.0

dv_expr = tsiolkovsky_delta_v(Isp_val, g0_val, m0_val, mf_val)
print("Δv expression:", dv_expr)
print("Δv numeric:", float(sp.N(dv_expr)))


Tests

Once dependencies are installed (SymPy and NumPy), run:

pytest


The current tests verify:

the structure of the 1D equations of motion;

that tsiolkovsky_delta_v(...) matches the standard
Tsiolkovsky formula numerically.


Roadmap

Planned extensions:

numeric integration helpers (vertical ascent with gravity and drag);

simple staging scenarios (two-stage rocket with different thrust/propellant);

Jupyter notebooks for:

Lagrangian form of the vertical rocket model,

comparison between ideal Δv and integrated trajectories.

This lab is intended to complement the SymPy Nozzle Gasdynamics Lab
as a “second stage”: from local nozzle flow to the motion of the whole rocket.

