# Adversarial Review 1 — gauge/frame attack on Step 2 (R^0_2 "time-live only")

Date: 2026-08-05. Reviewer: cold adversarial pass, zero derivation-code imported.
Method: coordinate Christoffel -> coordinate Riemann -> orthonormal-frame projection
(sympy 1.13.1, from scratch). The driver used Cartan structure equations; I did NOT.

**VERDICT: NARROW** (the algebra is exactly right; the *conclusion* "time-live only /
stationary depth is an endpoint function" is overstated and survives only under an
unstated restriction to purely spatial, equal-time loops).

Scripts: `scratchpad/indep_riemann.py`, `scratchpad/full_components.py`,
`scratchpad/sectional.py`.

---

## 1. Independent recompute (DIFFERENT method) — the expression is EXACT

Metric `ds^2 = -e^{-2phi}dt^2 + e^{2phi}dx^2 + R^2 dy^2`, phi=phi(t,x), R=R(t,x),
frame E0=e^{-phi}dt, E1=e^{phi}dx, E2=R dy. Coordinate Riemann projected to the frame:

```
R^0_2 |_{dx^dy}  (coeff of coordinate dx^dy in the curvature 2-form Omega^0_2)
   = ( R_t phi_x - R_x phi_t + R_tx ) e^{phi}
```

`claim - independent = 0` symbolically. **The driver's expression is reproduced exactly
by an independent route.** No algebra error. Point 1 PASSES for the driver.

## 2. Gauge attack — FAILS in the direction the driver feared, but exposes the real flaw

The driver asked me to "hunt for a frame/gauge choice that makes R^0_2 vanish." I could
NOT — and here is why that request was aimed at the wrong object. `R^0_2` is not the
scalar above; it is a curvature **2-form** with THREE coordinate components. Computing all
of them (frame-index form R^0_{2 CD}, i.e. the actual parallel-transport generator mixing
depth-leg E0 into screen-leg E2):

```
E0^E1 plane : 0
E1^E2 plane : ( R_t phi_x - R_x phi_t + R_tx ) / R          <- the driver's component
E0^E2 plane : [ (R_t phi_t + R_tt) e^{4phi} + R_x phi_x ] e^{-2phi} / R
```

On the **stationary branch (phi_t=0, R_t=0)**:

```
E1^E2 : 0                                   (driver's "time-live only" — TRUE for THIS one)
E0^E2 : e^{-2phi} R_x phi_x / R             (GENERICALLY NONZERO)   <-- driver dropped this
```

The depth->screen holonomy generator has a second component, in the **depth x screen
(time-screen) plane**, that is nonzero on the stationary branch. It is **not** a gauge
artifact: `E0 = ∂_t`-direction and `E2 = ∂_y`-direction are BOTH Killing (metric is
t-independent stationarily and y-independent always), so the 2-plane they span is
geometrically distinguished and its sectional curvature is a coordinate/frame **invariant**:

```
K(t,y) = R_{tyty}/(g_tt g_yy) ,  stationary  =  e^{-2phi} R_x phi_x / R   (INVARIANT, nonzero)
```

So no local Lorentz rotation of the E2 leg, boost mixing E2 into E1, nor reparametrization
y->f(y)/redefinition of R can make the depth-screen curvature vanish while preserving the
physics — it is a real sectional curvature. **The gauge attack fails: the holonomy is real.**
But that is precisely what refutes the driver: the screen's contribution to the depth
holonomy does NOT vanish stationarily. What vanishes stationarily is only its **spatial
(x,y)-loop** realization (the E1^E2 component). The "time-live only" label is an artifact of
reading ONE component of a frame-covariant object.

## 3. The real obstruction

"Depth is an endpoint function" <=> the full curvature 2-form `Omega^0_2 = 0` on the
relevant loops (integrability of the 0-leg transport). The driver attacked the right OBJECT
(`Omega^0_2`) but evaluated only its `dx^dy` coefficient. The invariant obstruction is the
2-form as a whole; stationarily `Omega^0_2 != 0` through its E0^E2 component, so depth is
**already** non-integrable on the stationary branch for any loop with time extent. The
free-constant `a` picture is exact only if `a`/`delta_a` is defined by strictly spatial
(equal-time) loops — a scope the driver never stated.

## 4. Stationary-only / on-shell

- Full holonomy: **NOT** time-live only. E0^E2 stays nonzero stationarily.
- On-shell R=R(phi), stationary: `K(t,y) = e^{-2phi} F'(phi) phi_x^2 / F`, nonzero generically
  (vanishes only where phi_x=0, i.e. seat/turning points). It does **not** vanish on the
  reciprocal-lock branch generically.

## Single strongest point against the claim

The claim identifies `R^0_2` with the single scalar `(R_t phi_x - R_x phi_t + R_tx)e^{phi}`
and calls it "time-live only." But `R^0_2` is a curvature 2-form whose depth-screen
component is the **gauge-invariant** sectional curvature `K(t,y)_stat = e^{-2phi} R_x phi_x/R`,
**nonzero on the stationary branch**. The screen therefore contributes to depth holonomy
*stationarily*; only the spatial-loop period is time-live. OT-REFRAME's premise "stationary
depth is an endpoint function, a is a free constant, time dissolves it" survives ONLY if the
`a`-holonomy is restricted to equal-time spatial loops — an unstated, load-bearing scope.
Absent that restriction, KEY FACTS 1-2 are false as written.
