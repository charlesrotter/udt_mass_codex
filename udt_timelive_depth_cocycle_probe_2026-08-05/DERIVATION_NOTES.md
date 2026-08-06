# Derivation notes — time-live depth cocycle probe

Date: 2026-08-05
**STATUS: LEAD / WORKING NOTE — UNBANKED. NOT A RESULT.** Cold/different-method
verification pending per PREREGISTRATION §6. Nothing here may be cited as proven,
confirmed, or a result; the four-check does not apply to a working note.

## Step 1 (done, exact, self-verified only): localize where time-live enters the transport

Reciprocal-lock metric (banked): `ds^2 = -e^{-2phi}dt^2 + e^{2phi}dx^2` (alpha=-phi,
beta=+phi). Orthonormal coframe `E0=e^{-phi}dt, E1=e^{phi}dx`. Cartan structure equations
give the boost spin-connection exactly:

```text
omega^0_1 = -e^{-2phi} phi_x dt  +  e^{2phi} phi_t dx
```

- The `dt` component `-e^{-2phi} phi_x` is the STATIONARY (static-depth) transport.
- The `dx` component `e^{2phi} phi_t` is the **time-live component**: it is identically
  zero on the stationary branch (`phi_t=0`) and nonzero only when depth evolves in time.

Boost curvature (endpoint-frame-invariant; single boost in 2D, exact):

```text
R^0_1 = [ e^{-2phi}(phi_xx - 2 phi_x^2) ] + [ e^{4phi}(phi_tt + 2 phi_t^2) ]  (coeff of dt^dx)
        \___ stationary part ___________/   \___ NEW time-live part __________/
```

The second bracket is present ONLY time-live. So the time-live branch activates exactly one
new connection component and one new curvature term. This is the precise seat through which
any time-live modification of the depth cocycle — and hence any effect on the stationary
angular-modulation parameter `a` — must come.

## What this is and is NOT

- IS: an exact localization of the time-live entry point in the depth transport. Correct,
  self-checked with sympy.
- IS NOT: an answer to Q1/Q2. `a` lives in the mixed **depth-screen** cocycle's exactness
  (the `N`-term vs `R`-term decomposition), not in the pure boost transport. The boost
  curvature being nonzero is ordinary spacetime curvature; the relevant question is whether
  the mixed depth-screen 1-form stays EXACT (endpoint depth, `a` a free constant) or acquires
  a nonzero loop PERIOD time-live (path label required, endpoint decomposition fails).

## Next step (the actual Q1/Q2 derivation)

Carry a live screen/area coordinate `R`, form the mixed depth-screen depth 1-form that
`delta_a` integrates on the stationary branch, and compute its exterior derivative
(loop-period density) time-live. Decide among:
- OT-COLLAPSE: closure/single-valuedness forces the angular weight (Charles's hypothesis);
- OT-SURVIVE: the mixed form stays closed with free period -> `a`-analog persists;
- OT-REFRAME: the mixed form is non-exact time-live -> `a` is not the right variable; the
  freedom is a holonomy, not a constant.

CURRENT LEAN (a lean, not a claim): the orchestra's own banked statement — "endpoint-only
depth requires all admissible loop periods to vanish; otherwise the path label must remain"
— plus the newly-activated time-live curvature term suggest OT-REFRAME is more likely than
a clean OT-COLLAPSE: time-live probably dissolves the endpoint `N`/`R` split into a genuine
path cocycle whose residual freedom is a holonomy. This must be DERIVED, not assumed; it
could land OT-SURVIVE or OT-COLLAPSE instead.
