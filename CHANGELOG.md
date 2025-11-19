# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and the project aims to follow a semantic-style versioning scheme.

## [0.1.0] - 2025-11-19

### Added

- Initial symbolic 1D vertical rocket model:
  - `t, h(t), v(t), m(t)` as state variables.
  - Parameters `g`, `T`, generic drag term `D(t)`, and mass flow rate `mdot`.
  - `vertical_rocket_equations()` returning the ODE system:
    - `dh/dt = v`,
    - `dv/dt = (T - D(t) - m g) / m`,
    - `dm/dt = -mdot`.
  - `tsiolkovsky_delta_v(Isp, g0, m0, mf)` for ideal Δv in vacuum.
  - `VerticalRocketModel` dataclass as a small symbolic container.

- Numeric integration utilities:
  - `RocketParams` dataclass (thrust, gravity, mass flow rate, optional drag).
  - `rocket_rhs(...)` as the RHS of the 1D ODE system.
  - `integrate_vertical_rocket(...)` using RK4 on a uniform time grid.

- Plotting helpers:
  - `plot_altitude(...)`,
  - `plot_velocity(...)`,
  - `plot_altitude_and_velocity(...)`.

- Notebooks:
  - `01_vertical_rocket_symbolic.ipynb` – symbolic model, mass law, Tsiolkovsky Δv.
  - `02_vertical_rocket_numeric.ipynb` – simple numeric trajectory and plots.

- Project infrastructure:
  - `requirements.txt` (sympy, numpy, matplotlib),
  - `requirements-dev.txt` (pytest),
  - `pytest.ini`,
  - `tests/test_rocket_equations.py`,
  - initial `README.md` describing structure and usage.
