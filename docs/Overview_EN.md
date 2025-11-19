# Symrock in the cascade: from nozzle to rocket

This lab is the **second stage** in a small aerospace mechanics cascade:

1. **SymPy Nozzle Gasdynamics Lab**  
   Local, quasi-1D isentropic flow in a nozzle:
   - `symgas` package (nozzle lab),
   - symbolic isentropic relations \(T/T_0, p/p_0, \rho/\rho_0, A/A^*(M)\),
   - numeric profiles and basic engineering plots.

2. **Symbolic Rocket Mechanics Lab** (this repository)  
   Motion of the whole vehicle in 1D vertical flight:
   - `symrock` package,
   - symbolic equations of motion \(h(t), v(t), m(t)\),
   - Tsiolkovsky \(\Delta v\) in symbolic form,
   - simple RK4 integrator and trajectory plots.

The idea is to keep each lab small and focused, but **connect them conceptually**:

- the nozzle lab gives intuition for local exhaust physics and effective exhaust
  velocity;
- the rocket lab uses that intuition to reason about vehicle-level motion,
  mass flow and achievable \(\Delta v\).

In a more complete research line, a third step could appear:

3. **Guidance / multi-stage / re-entry lab (future)**  
   - staging scenarios (multi-stage rockets),
   - simple guidance laws in 2D or 3D,
   - basic re-entry profiles,
   - coupling with atmosphere and drag models.

For now, `symrock` stays deliberately lightweight:

- it is easy to read as a **teaching notebook**,
- it can be used as a minimal **testbed** for new ideas in rocket mechanics,
- it aligns naturally with the nozzle lab in style and structure.

---

## Related repositories

- **SymPy Nozzle Gasdynamics Lab (`symgas`)**  
  Repository: `sympy-nozzle-gasdynamics-lab`  
  Focus: symbolic and numeric quasi-1D nozzle flow.

- **Symbolic Rocket Mechanics Lab (`symrock`)** (this repo)  
  Focus: 1D vertical rocket motion, Δv, simple numeric trajectories.
