# Conditional C2 Time/Fiber-Shift Jacobi Audit — Preregistration

Date: 2026-07-20  
Base: `61f6bc01e5732b3bc59120d506bd6b2716646369`  
Branch: `codex/c2-time-fiber-shift-jacobi-2026-07-20`  
Mode: CPU-only exact curvature expansion and linearized full-equation classification

## Whole question

Inside the frozen `UNIQUE-CONDITIONAL` pre-scale metric-only `C^2` branch, what stationary solutions
appear when the smallest omitted off-diagonal coframe degree of freedom is opened: a connection
between time and the conditional reciprocal angular fiber?

This audit observes the shift sector. It does not target rotation, a particle, mass, a spectrum, or
an expected clock law.

## Whole frame and why this is one bounded tile

The pure unrestricted question would vary all ten four-metric components, any native material field,
the complete finite-cell boundary/corner data, and global bootstrap conditions with no stationary or
toric restriction. That complete action and boundary problem remain open.

The registered stationary coframe is

`e0 = N(eta) d tau`,

`e1 = b H(eta) d eta`,

`e2 = b sin(eta)cos(eta) d delta`,

`e3 = b s[cos^2(eta)d xi1 + sin^2(eta)d xi2 + W(eta)d tau]`,

with `delta=xi1-xi2`, `0<=eta<=pi/2`, both angles of period `2pi`, and

`g4 = epsilon_t e0^2 + e1^2 + e2^2 + e3^2`.

The physical stationary check uses `epsilon_t=-1` and noncompact `tau`. Positive-definite
continuation `epsilon_t=+1` is a comparison/soundness check only; agreement of signs or roots is not
assumed.

The first tile is the **Jacobi sector about the already full-equation-tested round CSN class**:

`N=1`, `H=1`, `s=1`, `W=epsilon w(eta)`.

This does not freeze backreaction and then call the result nonlinear. It asks only whether the exact
quadratic `C^2` action and linearized full Bach equation contain regular non-gauge shift directions.
Backreaction in `N,H,s` begins at even order under `W->-W`; any finite-amplitude branch, bifurcation,
or nonlinear selection remains explicitly open and requires a later unrestricted reduced/full-
component solve.

## Premise and choice ledger

| Object | Classification |
|---|---|
| Metric is the theory | `pinned-by-THEORY` |
| CSN class before scale selection | `FOUNDING` |
| `C^2` bulk | `UNIQUE-CONDITIONAL` under the frozen action-class premises |
| Reciprocal-toric coframe and smooth primitive caps | `CONDITIONAL CANDIDATE PREMISE` |
| Stationarity and one time/fiber shift | `pinned-by-HABIT / BOUNDED SLICE`; unrestricted time dependence and other shifts remain open |
| Lorentzian sign `epsilon_t=-1` | `free-and-explored` as the physical stationary branch; Euclidean sign separately checked |
| `N=H=s=1` background | `pinned-by-the prior conditional full Bach solution`, cited to `c2_variable_lapse_selector_2026-07-20/` |
| Shift profile `w(eta)` | `free-and-explored` in the smooth torus-invariant Jacobi function space |
| Constant part of `w` | retained and classified; expected coordinate/gauge orbit but not removed before calculation |
| Overall scale `b` | quotient/calibration under CSN; tracked but not selected |
| Smooth caps | `CONDITIONAL MATHEMATICAL DOMAIN`, not the physical finite-cell wall |
| Physical finite-cell boundary/corner action | `OPEN / NOT SUPPLIED` |
| Carrier, section, soldering, matter action | `OPEN`; excluded |
| `c`, `G`, electron mass, `Xmax`, total mass/density | absent from the dimensionless Jacobi equation; no calibration performed |

No acceptance test may discard a profile because it looks non-particle-like, oscillatory, singular,
or unexpected. Profiles are classified by equation, regularity class, action norm, and gauge status.

## Candidate and completeness census frozen before algebra

Retain separately:

1. constant `w`, including its exact coordinate transformation and global caveats;
2. all smooth cap-regular solutions of the Lorentzian linearized Bach equation;
3. the positive-definite continuation and any signature-dependent roots;
4. solutions with nonzero quadratic Weyl action and zero-action/conformally-flat directions;
5. endpoint logarithmic, pole, or non-normalizable strata as characterized branches, not erased data;
6. boundary-supported solutions on a physical interval as open when compact cap regularity excludes
   them;
7. other time/radial, time/base, and moving-basis connections as omitted fields;
8. nonlinear `N,H,s,W` backreaction and disconnected finite-amplitude branches as omitted branch
   coverage;
9. alternative topology, genuine time dependence, and acceleration as omitted dynamical coverage.

## Exact tests

1. Construct the full 4D metric from the coframe before expanding in `epsilon`.
2. Compute Riemann, Ricci, scalar, Weyl-squared density, and the coefficient quadratic in `epsilon`
   independently for `epsilon_t=-1` and `+1`.
3. Derive the Euler-Lagrange/Jacobi equation for arbitrary `w(eta)` before inserting any trial mode.
4. Verify the same linear equation from the `tau-fiber` Bach component or an independently derived
   equivalent full-field variation. A reduced equation alone is not a full-equation verdict.
5. Solve/classify the complete local ODE and impose only the registered smooth-cap regularity. Preserve
   every local singular branch in the census.
6. Demonstrate directly whether constant `w` is an exact coordinate copy; record any global
   time/angle identification caveat.
7. Check CSN/common-homothety weight and the absence of scale and material anchors.
8. Exercise catches against silently setting `w=0`, treating constant `w` as physical rotation,
   promoting a linear result to nonlinear closure, importing GR frame dragging, or calling caps the
   physical wall.

## Certification and falsification contract

`NO_REGULAR_NON_GAUGE_SHIFT_JACOBI_MODE_IN_SLICE` requires complete local solution of the linearized
full Bach equation and proof that every smooth capped solution is an exact gauge/coordinate direction.

`REGULAR_NON_GAUGE_SHIFT_JACOBI_MODES_EXIST_IN_SLICE` requires an explicit complete regular basis,
non-gauge witness, and independent residual/Bach check. It does not prove a nonlinear branch or
stability.

If reduced variation and the full Bach component disagree, or the full component cannot be derived,
the result remains `OPEN / REDUCED-ONLY LEAD`.

## Maximum allowed conclusion

At most this audit may classify the stationary torus-invariant time/fiber **linearized** shift sector
about the conditional round compact `C^2` solution.

It cannot derive or adopt the unrestricted metric, complete action, physical boundary, nonlinear
shift branch, acceleration principle, time-live dynamics, scale, `Xmax`, carrier, source, electron
mass, or material action. No GPU work, canonization, repository reorganization, or startup-control
edit is authorized.
