# Symbolic Rocket Mechanics Lab (`symrock`)

Small **SymPy-based lab** for 1D vertical rocket mechanics.

This project keeps the model deliberately simple and transparent:

- symbolic equations of motion for a point-mass rocket in vertical flight;
- explicit Tsiolkovsky Δv formula as a SymPy expression;
- a tiny RK4 integrator for numeric trajectories;
- minimal plotting helpers and Jupyter notebooks.

It is not a full flight-dynamics simulator.  
Think of it as a compact **workbench**: part textbook, part notebook, part Python package.

---

## Motivation

The lab is designed as the **second stage** in a small aerospace mechanics cascade:

1. **SymPy Nozzle Gasdynamics Lab (`symgas`)**  
   Quasi-1D isentropic flow in a nozzle: local gasdynamics, Mach number, area–Mach relation.

2. **Symbolic Rocket Mechanics Lab (`symrock`)** (this repository)  
   Motion of the entire vehicle in 1D vertical flight:
   altitude, velocity, mass, thrust, gravity, simple mass flow.

The nozzle lab gives intuition about exhaust and effective exhaust velocity.  
The rocket lab uses that intuition to reason about **vehicle-level motion and Δv**.

---

## Features

### Symbolic core

- **State and parameters** (in `src/symrock/rocket_1d.py`):
  - time: `t`,
  - altitude: `h(t)`,
  - vertical velocity: `v(t)`,
  - mass: `m(t)`,
  - gravity: `g`,
  - thrust: `T`,
  - generic drag term: `D(t)`,
  - mass flow rate: `mdot` (mass decreases as `dm/dt = -mdot`).

- **Equations of motion**:
  - `vertical_rocket_equations()` returns a dict of SymPy `Eq` objects:
    - `dh/dt = v`,
    - `dv/dt = (T - D(t) - m g) / m`,
    - `dm/dt = -mdot`.

- **Tsiolkovsky rocket equation**:
  - `tsiolkovsky_delta_v(Isp, g0, m0, mf)`:
    \[
      \Delta v = I_{sp} \, g_0 \ln\left(\frac{m_0}{m_f}\right)
    \]
  - returns a SymPy expression that can be evaluated symbolically or numerically.

- **Model container**:
  - `VerticalRocketModel` dataclass gathers the key symbols and equations in one place.

All of this is exported through `symrock.__init__` for convenient import.

---

## Numeric integrator

In `src/symrock/integrators.py`:

- `RocketParams` dataclass:
  - `T` — thrust \[N\],
  - `g` — gravitational acceleration \[m/s²\],
  - `mdot` — mass flow rate \[kg/s\],
  - optional `drag_fn(t, h, v, m)` — generic drag model \[N\] (can be `None`).

- `rocket_rhs(t, y, params)`:
  - right-hand side of the 1D ODE system for `y = [h, v, m]`.

- `integrate_vertical_rocket(...)`:
  - simple explicit RK4 on a uniform time grid,
  - integrates from `(t0, h0, v0, m0)` to `t_end` with time step `dt`,
  - returns a dict with arrays:
    - `"t"` – time nodes,
    - `"h"` – altitude profile,
    - `"v"` – velocity profile,
    - `"m"` – mass profile,
  - once mass becomes non-positive, the state is frozen for the remaining steps
    (to avoid unphysical behavior).

This integrator is designed for **teaching and quick experiments**, not for production flight code.

---

## Plotting helpers

In `src/symrock/plots.py`:

- `plot_altitude(t, h, ...)`  
  Altitude vs time.

- `plot_velocity(t, v, ...)`  
  Vertical velocity vs time.

- `plot_altitude_and_velocity(t, h, v, ...)`  
  Both curves on a shared time axis.

All plotting functions use Matplotlib only and keep styling intentionally simple.

---

## Project structure

```text
symbolic-rocket-mechanics-lab/
├─ src/
│  └─ symrock/
│     ├─ __init__.py              # package entry point, exports core symbols and helpers
│     ├─ rocket_1d.py             # symbolic 1D rocket model and Tsiolkovsky Δv
│     ├─ integrators.py           # RK4-based numeric integration for [h, v, m]
│     └─ plots.py                 # simple altitude/velocity plotting utilities
├─ notebooks/
│  ├─ 01_vertical_rocket_symbolic.ipynb  # symbolic EOM, m(t) law, Δv example
│  └─ 02_vertical_rocket_numeric.ipynb   # numeric trajectory and plots
├─ docs/
│  └─ Overview_EN.md              # cascade overview: nozzle lab → rocket lab
├─ tests/
│  └─ test_rocket_equations.py    # EOM structure and Δv numeric check
├─ CHANGELOG.md                   # project history (starting from v0.1.0)
├─ requirements.txt               # runtime deps: sympy, numpy, matplotlib
├─ requirements-dev.txt           # dev deps: pytest
├─ pytest.ini                     # pytest configuration
├─ pyproject.toml                 # packaging config (symrock, src layout)
├─ LICENSE                        # MIT License
├─ .gitignore                     # ignore Python, build, notebook cache, etc.
└─ README.md                      # this file



Installation

Create and activate a virtual environment (recommended), then:

pip install -r requirements.txt


For editable install of the symrock package:

pip install -e 

After that you can import symrock from anywhere in that environment.



Quick symbolic example

import sympy as sp
from symrock import (
    t, h, v, m, g, T, D, mdot,
    vertical_rocket_equations,
    tsiolkovsky_delta_v,
)

# Get symbolic equations of motion
eqs = vertical_rocket_equations()
print(eqs["h_dot"])  # dh/dt = v
print(eqs["v_dot"])  # dv/dt = (T - D(t) - m*g) / m
print(eqs["m_dot"])  # dm/dt = -mdot

# Tsiolkovsky Δv for a simple case
Isp_val = 300.0     # s
g0_val = 9.80665    # m/s^2
m0_val = 500.0      # kg (wet mass)
mf_val = 200.0      # kg (dry mass)

dv_expr = tsiolkovsky_delta_v(Isp_val, g0_val, m0_val, mf_val)
print("Δv expression:", dv_expr)
print("Δv numeric:", float(sp.N(dv_expr)))


You can use the SymPy expressions for further symbolic work:
differentiation, parameter sweeps, simplifications, etc.



Quick numeric example

import numpy as np

from symrock.integrators import RocketParams, integrate_vertical_rocket

# Scenario parameters (toy model)
T = 15000.0           # thrust [N]
g = 9.80665           # gravity [m/s^2]
mdot = 5.0            # mass flow rate [kg/s]

m0 = 500.0            # initial mass [kg]
h0 = 0.0              # initial altitude [m]
v0 = 0.0              # initial vertical velocity [m/s]

t0 = 0.0              # start time [s]
t_end = 60.0          # end time [s]
dt = 0.1              # time step [s]

params = RocketParams(T=T, g=g, mdot=mdot, drag_fn=None)

result = integrate_vertical_rocket(
    t0=t0,
    t_end=t_end,
    dt=dt,
    h0=h0,
    v0=v0,
    m0=m0,
    params=params,
)

t = result["t"]
h = result["h"]
v = result["v"]
m = result["m"]

print(f"Final time: t = {t[-1]:.1f} s")
print(f"Final altitude: h = {h[-1]:.1f} m")
print(f"Final vertical velocity: v = {v[-1]:.1f} m/s")
print(f"Final mass: m = {m[-1]:.1f} kg")


For a visual view of the trajectory, use plotting helpers in a notebook.



Plotting example (Jupyter)

%matplotlib inline

from symrock.plots import (
    plot_altitude,
    plot_velocity,
    plot_altitude_and_velocity,
)

_ = plot_altitude(t, h, title="Altitude vs time")
_ = plot_velocity(t, v, title="Vertical velocity vs time")
_ = plot_altitude_and_velocity(
    t, h, v,
    title="Vertical rocket trajectory: altitude and velocity",
)


For full examples, see:

notebooks/01_vertical_rocket_symbolic.ipynb

notebooks/02_vertical_rocket_numeric.ipynb



Running tests

Install dev dependencies and run pytest:


pip install -r requirements-dev.txt
pytest


Current tests (tests/test_rocket_equations.py) verify:

the structure of the symbolic equations of motion;

that `tsiolkovsky_delta_v(...)` matches the standard Tsiolkovsky expression `Δv = I_sp * g_0 * ln(m_0 / m_f)` for a simple case.



Related labs

This project is part of a small aerospace mechanics cascade:

SymPy Nozzle Gasdynamics Lab (symgas)
Quasi-1D isentropic nozzle flow, isentropic ratios, area–Mach relation.
Focus: local gasdynamics.

Symbolic Rocket Mechanics Lab (symrock) (this repository)
1D vertical rocket motion, Tsiolkovsky Δv, simple trajectories.
Focus: vehicle-level motion.

Together they form a clean line from nozzle physics to rocket mechanics,
with room for future stages (guidance, multi-stage flight, re-entry).



Versioning and changelog

Current version: v0.1.0.

The project uses a simple semantic-style versioning:

MAJOR — breaking changes in the API or structure,

MINOR — new features, backward compatible,

PATCH — internal fixes and small improvements.

All notable changes are documented in CHANGELOG.md.
Tagged versions and downloadable archives are available in the GitHub Releases section.



License

This project is released under the MIT License.
See the LICENSE file for the full text.


