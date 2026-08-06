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

## Step 2 (done, exact, self-checked only): the mixed depth-screen holonomy — MODEL lands OT-REFRAME

**STILL A LEAD / UNBANKED. Single explicit model, driver-computed, self-checked only. Cold
verification and faithfulness-to-the-orchestra-2+2-branch check both REQUIRED before banking.**

Model: `ds^2 = -e^{-2phi}dt^2 + e^{2phi}dx^2 + R^2 dy^2`, phi=phi(t,x), R=R(t,x) (boost plane
+ one live screen). Full so(1,2) connection solved from Cartan; depth = timelike leg (0).
The screen's contribution to the DEPTH holonomy is the curvature R^0_2. Exact:

```text
R^0_2|_{dx^dy} = ( R_t phi_x - R_x phi_t + R_tx ) e^{phi}
```

KEY FACTS (exact):
1. This component is **TIME-LIVE ONLY**: on the stationary branch (phi_t=0, R_t=0) it
   reduces to R_x*0 - 0 + 0 = 0. The screen->depth loop period vanishes stationary.
2. Therefore stationary: depth is an endpoint function, and the screen weight `a` is a FREE
   CONSTANT weighting two exact forms (reproduces delta_a).
3. Time-live: R^0_2 is generically nonzero -> the depth cocycle acquires a nonzero loop
   period -> endpoint depth FAILS -> the free-constant `a` decomposition DISSOLVES.

VERDICT (model-scoped): **OT-REFRAME.** `a`-as-free-constant is a stationarity artifact
(supports Charles's hypothesis). Time-live it is replaced by a DETERMINED holonomy density
`R^0_2`, not a free number. The residual structure is a holonomy, not a constant.

THE PHI-ANGULAR COUPLING appears explicitly: the leading term `R_t phi_x - R_x phi_t` is a
genuine antisymmetric coupling between screen evolution and depth gradient (a Jacobian /
commutator of the screen and depth flows) — the phi-angular interaction, here as a concrete
curvature. If the screen is tied to depth, R=R(phi), it becomes (R'' phi_t phi_x + R' phi_tx)e^{phi}.

CHARLES'S c_eff INTUITION — consistent, honestly scoped: every depth/screen holonomy carries
exponential phi factors (e^{phi}, e^{2phi}, e^{-2phi}, e^{-3phi}). The angular contribution is
therefore phi-WEIGHTED (depth-dependent), NOT a constant modulation — which is the shape of
Charles's intuition (little effect near phi=0 / c_eff~c; exponentially significant at depth).
The precise "small at c~c, large at extreme" behavior follows from the exponential weighting
but its direction depends on the R-phi coupling and sign(phi); NOT claimed beyond the weighting.

## What must happen before this banks (per PREREGISTRATION and the K4/U(1) lesson)
- Faithfulness: confirm this diagonal 2+1 model is a genuine instance of the orchestra's
  2+2 stationary branch (that R^0_2's period is the same object as delta_a's `a`-weight),
  not a convenient strawman.
- Cold/different-method verifier: recompute the holonomy by an independent route (import no
  code here), and specifically attack OT-REFRAME (the owner-pleasing direction, since it
  supports Charles's hypothesis) — hunt for a frame/gauge choice that makes R^0_2 vanish, or
  a reason the identification with `a` fails.
- Only then a scoped bank + LIVE pointer.

## RETRACTION (2026-08-05): Step 2's OT-REFRAME conclusion is REFUTED

Two independent same-session adversarial reviews (from different directions) both kill the
Step-2 conclusion. Files: `ADVERSARIAL_REVIEW_1_gauge.md`, `ADVERSARIAL_REVIEW_2_faithfulness.md`.

**Review 2 (faithfulness) = REFUTE, and it is decisive.** `delta_a(p,q) = log[N(p)/N(q)]
+ a log[R(q)/R(p)] = F(p) - F(q)` with `F = log(N/R^a)`. It is the coboundary of a SCALAR,
so `d(delta_a-form) = 0` and its loop period is ZERO for EVERY `a`, stationary OR time-live.
No holonomy can obstruct it; therefore no holonomy — including `R^0_2` — can cut `a`. The
driver computed the curvature of the SEPARATE full-strain depth `delta_t` (the object the
orchestra §4/§7 explicitly distinguishes from `delta_a`) and mis-attached it to `delta_a`'s
`a`. Category error. Also: time-live the Killing norm is lost but the scalar clock norm
`N = e^{-phi} = sqrt(-g_tt)` survives single-valued, so `log N = -phi` stays exact and `a`
stays FREE. Correct model-scoped class: **OT-SURVIVE**.

**Review 1 (gauge/math) = NARROW, and it independently confirms the algebra while killing
the framing.** By an independent route (coordinate Christoffel -> Riemann -> frame, not
Cartan) it reproduced `R^0_2|_{dxdy} = (R_t phi_x - R_x phi_t + R_tx)e^{phi}` EXACTLY. But
`R^0_2` is a 2-form with more than the one component read: its `E0^E2` (depth-screen)
component is nonzero STATIONARILY — the (t,y) sectional curvature `K = e^{-2phi}R_x phi_x/R`,
a frame INVARIANT (not gaugeable). So "time-live only" (KEY FACTS 1-2) is FALSE as written;
the screen contributes to `delta_t`'s depth holonomy stationarily too. `R^0_2` is real, not a
gauge artifact — which is exactly why it cannot be the thing "time dissolves."

**F-STEER CATCH (the cause, recorded for the next driver):** the driver pre-declared the
OT-REFRAME "CURRENT LEAN" — the owner-pleasing direction (it supports Charles's hypothesis
that `a` is a stationarity artifact) — and Step 2 then landed there via the wrong object AND
one component of it. The primary preregistered falsifier (F-STEER) fired UNCAUGHT in the
driver's own derivation; the adversarial reviews caught it. Textbook owner-pleasing steering.

**CORRECTED OUTCOME (model-scoped): OT-SURVIVE.** `a` remains a free, unselected constant
time-live — exactly the orchestra's already-banked position. **Time-live does NOT select `a`
via exactness/holonomy; that mechanism is RULED OUT.** This is the probe's honest result: not
a new constraint, but a robustly-refuted one — Charles's time-live hypothesis for `a` does
not hold by this route.

**Honest residual (a DIFFERENT question, NOT a rescue):** Review 1 establishes that the
full-strain depth `delta_t` is genuinely path-dependent (real, non-gauge curvature, stationary
and time-live). Whether the physical depth is `delta_t` (path-dependent) or `delta_a`
(coboundary) is a legitimate open question — but it restores NO time-live-special constraint
on `a`, and must not be used to revive the retracted claim.

STATUS: Step 1 (the connection localization) stands as correct algebra. Step 2's conclusion is
RETRACTED. Nothing here banks. The probe's contract (PREREGISTRATION) is closed at OT-SURVIVE,
model-scoped, driver+2-adversarial-review, external review still owed for any bank.
