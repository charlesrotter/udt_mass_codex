# Branch G Characterization — "Gauge the Obstruction Away"

**Mode:** OBSERVE (report WHAT IS THERE; NOT verdict-hunting, NOT steering to a
desired answer). Builds on `native_dilation_weight_derivation_results.md`.
**Constructor:** Claude Opus 4.8 (1M), agent for udt_mass_codex, 2026-06-21.
**Compute:** CPU only (sympy/scipy), bounded analytic + small ODE shoots. No GPU,
no coupled jacrev solver, single process.
**Scripts (new, /tmp, nothing committed):** `branch_G_field_eqns.py`,
`branch_G_reduced_EL.py`, `branch_G_analysis.py`, `branch_G_vac{4,5,6}.py`,
`branch_G_falloff.py`, `branch_G_scalar_eqn.py`, `branch_G_X_and_boxf.py`.
All symbolic claims machine-checked unless tagged ANALYTIC; ODE results tagged NUMERIC.

The action under study (the weight doc's clean shift-invariant remnant):
```
S_G = INT sqrt(-g) [ f(phi) R + X f(phi) g^{mu nu} d_mu phi d_nu phi ],
      f(phi) = e^{+2 phi},   phi an INDEPENDENT player (not slaved),
      X = kinetic/curvature ratio (no-ghost + Cassini => X large NEGATIVE; |X|>~1.7e5).
```

---

## 0. PREMISE LEDGER (chose vs derived)

| # | Premise / choice | Status |
|---|---|---|
| G1 | Action S_G as written (f=e^{2phi}, single bare kinetic, X free) | INHERITED from the weight derivation (Branch G = its clean fork) |
| G2 | phi an INDEPENDENT two-player field | CHOSE (Charles 2026-06-21; consistent with weight doc P4) |
| G3 | Static spherical, areal chart ds^2=-A c^2 dt^2 + B dr^2 + r^2 dOmega^2 | CHOSE (CANON slice for EXHIBITING vacuum; A,B,phi all free, NOT slaved) |
| G4 | Field eqns from varying S_G w.r.t. g AND phi — NOT Brans-Dicke textbook | DERIVED (reduced-action EL from scratch; BD identity used only as a cross-check label) |
| G5 | Vacuum = no matter source (T=0) | CHOSE (the canon vacuum slice question) |
| G6 | Seed values for shoots: r0=2, A0=1-1/r0, phi(r0)=0, phi'(r0) varied | CHOSE (generic Schwarzschild-like seed + a scalar-charge dial; not tuned to any target) |
| G7 | no-ghost (2omega+3>0) and Cassini |gamma-1|<2.3e-5 windows on X | INHERITED constraints (weight doc Sec 9 + standard scalar-tensor health) |

---

## 1. FIELD EQUATIONS (derived from S_G, two-player) [DERIVED]

Varying S_G independently w.r.t. g_{mu nu} and phi (covariant form, f arbitrary,
then specialized to f=e^{2phi}, f'=2f):

**METRIC equation** (g-variation):
```
f G_{mu nu} + ( g_{mu nu} box - nabla_mu nabla_nu ) f
            - X f ( d_mu phi d_nu phi - 1/2 g_{mu nu} (d phi)^2 ) = 0.
```
The `(g box - nabla nabla) f` block is the non-minimal-coupling stress; it is
NON-ZERO whenever phi is non-constant (the broken-freeze door). The X-block is the
scalar's gradient stress.

**SCALAR equation** (phi-variation):
```
f'(phi) R - X f'(phi)(d phi)^2 - 2 X f(phi) box phi = 0
   =>  (divide by f'=2f)   R - X (d phi)^2 - X box phi = 0
   =>  box phi = R/X - (d phi)^2.
```
**OBSERVED STRUCTURE (central):** the scalar EOM has **NO potential V(phi) and NO
mass term.** phi is a MASSLESS scalar whose ONLY source is the curvature R (through
the f'R = 2f R term). This is the algebraic reason there is no intrinsic scale (Sec 4).

**Principle-7 flag:** I did NOT assume "this reduces to Brans-Dicke." I derived the
two equations from S_G's own variation. The BD label (omega=-X/4) is used ONLY as an
after-the-fact cross-check of the weak-field gamma, never as an input. No "folds to
the standard case" step was taken; where the f-derivative terms COULD have been
dropped to recover GR (constant f), I instead KEPT them and that is exactly what
opens the non-trivial vacuum (Sec 2).

**Explicit reduced SSS field equations** (areal chart, machine-derived via the
minisuperspace EL — see `branch_G_reduced_EL.py`, `branch_G_clean.py`):

- EL wrt B (the **Hamiltonian / "tt" constraint**, first-order, no second derivatives):
```
2 A B - X A r^2 (phi')^2 - 8 A r phi' - 2 A - 2 r^2 A' phi' - 2 r A' = 0
  =>  A' = A ( 2B - X r^2 (phi')^2 - 8 r phi' - 2 ) / ( 2 r ( r phi' + 1 ) ).   [the constraint]
```
- EL wrt A (the "rr" equation) and EL wrt phi (the scalar equation): two
  second-order equations supplying B'(r) and phi''(r) once A' is taken from the
  constraint. (Full machine forms in the script; they close consistently — the
  Bianchi-type dependency means the three EL equations yield {A', B', phi''} with
  one first-order constraint, exactly the right count for a two-player static system.)

**Self-consistency check [DERIVED]:** combining the trace of the metric equation
with the scalar equation gives the clean relation
```
box phi = [ 12 / (X - 6) ] (d phi)^2,        R = 6 box phi + (12 + X)(d phi)^2.
```
This is the lever for the X-limit (Sec 3).

---

## 2. VACUUM STRUCTURE [DERIVED + NUMERIC]

### 2a. The constant-phi branch IS exact Schwarzschild [DERIVED]
Setting phi=const (phi'=phi''=0) collapses the field equations to:
```
EL_B|phi'=0 :  -r A' + A B - A = 0      (the GR tt equation)
EL_A|phi'=0 :   r B' + B^2 - B = 0      (the GR rr equation)
EL_phi|phi'=0:  proportional to R       (scalar eqn becomes f' R = 0 => R = 0)
```
Substituting Schwarzschild A=1-2m/r, B=1/A, phi=const into all three EL equations
gives **EXACTLY 0** (machine-checked, `branch_G_analysis.py`). So:
> **Schwarzschild with ANY constant phi is an exact Branch-G vacuum solution, for every X.**
The constant mode of phi is pure gauge (R1), and on it the theory is GR verbatim.

### 2b. The genuinely two-player (phi' != 0) vacuum [NUMERIC, bounded shoots]
Seeding r0=2 with A0=1-1/r0 and dialing the scalar gradient phi'(r0) (an integration
constant = "scalar charge"), integrating outward to r=80-500
(`branch_G_vac6.py`, `branch_G_falloff.py`):

- **phi'(r0)=0 reproduces Schwarzschild exactly** (A B = 1.0000, phi stays 0) for ALL
  X — the GR branch is recovered as the zero-charge member.
- **phi'(r0) != 0 gives a smooth deformation:** A, B deviate from Schwarzschild
  continuously with the seed; phi grows from 0 toward a constant asymptote.
- **phi(r) is MONOTONE for every X (-2e5, -1e3, -10, -1) and every seed (1e-4 ... 1.0)**
  — NO turning point, NO oscillation, NO preferred radius (scanned, all MONOTONE).
- **Asymptotic falloff: phi'(r) ~ r^{-2.03}** (log-log fit, slope -2.032 over r=10..400).
  i.e. **phi ~ phi_inf - q/r**: a 1/r SCALAR-HAIR TAIL with a conserved scalar charge q
  (the integration-constant seed). The metric carries a matching m/r mass term.

### 2c. Verdict on the broken freeze
The weight doc's "box f != 0 in vacuum" is CONFIRMED: with phi non-constant the
f-derivative terms survive, so static-spherical vacuum is NOT frozen to Schwarzschild
ALONE — it is a **two-parameter family {m, q}** (mass + scalar charge) rather than the
one-parameter {m} of GR. BUT the extra structure is **scalar HAIR, not a new scale**:
it is the well-known massless-scalar-tensor solution family (Fisher / Janis-Newman-
Winicour / Brans Class-I type), a smooth deformation of Schwarzschild parameterized by
a free charge. It does NOT spontaneously become non-static, and it does NOT select a
radius. "Vacuum != GR" is TRUE (extra hair parameter); "vacuum is structured/discrete"
is FALSE at this slice.

---

## 3. THE X PARAMETER [DERIVED + NUMERIC]

**How X enters:** X is the dimensionless coefficient of the kinetic term relative to
f R. In the constraint A' it appears only multiplying (phi')^2 — i.e. it weights the
scalar's back-reaction on the geometry. In the combined relation
`box phi = 12/(X-6) (dphi)^2`, X controls the strength of the curvature-scalar coupling.

**Large-|X| (healthy) limit = the GR / decoupling limit [DERIVED]:**
```
box phi = [12/(X-6)] (dphi)^2  --(X -> -infinity)-->  box phi -> 0,
R = X (dphi)^2 + X box phi      -->  R -> 0 (back-reaction ~ 1/X).
```
So at X large negative, phi obeys the FREE massless wave equation box phi = 0 and its
gravitational back-reaction is O(1/X) — **the scalar decouples and the metric -> GR.**
This is precisely the Brans-Dicke omega -> infinity limit (omega = -X/4, so
|omega| -> infinity): BD at large |omega| IS general relativity, with corrections ~1/omega.
NUMERIC confirmation: at X=-2e5, small seeds keep A B within 1e-3 of 1 (GR), and the
deviation scales with the seed, not with any internal scale.

**What Branch G is CLOSE TO:** a massless Brans-Dicke / dilaton scalar-tensor theory at
large negative coupling — i.e. **GR plus a weakly-coupled massless scalar with 1/r hair.**
Not a special dilaton (no exponential potential, no Gauss-Bonnet coupling, no mass);
the e^{2phi} weight rides entirely inside the kinetic normalization (Brans frame).

**Does anything INTERNAL fix X? NO [DERIVED].**
- X is dimensionless (ratio of two coefficients both wearing e^{2phi}); R1/R2/R3 fix
  the shared weight but NOT the ratio (weight doc Sec 4/7).
- All constraints on X are INEQUALITIES, none a value:
  - no-ghost (2omega+3>0, omega=-X/4) => X < 6;
  - Cassini |gamma-1|=4/|X-8| < 2.3e-5 => |X-8| > 1.74e5 => X < -1.7e5.
  - Healthy + Cassini-safe window = the **half-line X <~ -1.7e5**.
- Nothing in Branch G's action, vacuum solutions, or self-consistency picks a point on
  that half-line. **X remains a FREE DIAL** (one continuous parameter), bounded but not
  fixed. The theory is a smooth one-parameter (X) family.

---

## 4. SCALE / DISCRETENESS [DERIVED + NUMERIC] — the headline OBSERVE

**Branch G has NO intrinsic length and NO candidate for discrete structure.** Evidence,
three independent angles, all converging:

1. **Algebraic (scalar EOM):** box phi = R/X - (dphi)^2 has **no potential, no mass term**
   — phi is massless. A massless scalar has no Compton length; nothing sets a scale. The
   ONLY would-be scale term in the weight derivation was the angular curvature potential
   `~ e^{2phi}` (the 2/r^2 survivor) — and Branch G is DEFINED by gauging exactly that
   term away. With it gone, no V(phi), no scale. [DERIVED]

2. **Numeric (vacuum profiles):** phi(r) is MONOTONE for every X and every seed; phi'(r)
   ~ 1/r^2 pure power-law hair. No oscillation, no turning point, no resonance, no
   quantization condition — the solution family is smoothly parameterized by two
   continuous integration constants {m, q} and one continuous coupling X. A continuum in
   every direction. [NUMERIC]

3. **Limit structure:** large-|X| -> GR + free scalar; small |X| -> stronger but still
   smooth, scale-free coupling. No corner of X produces a special length. [DERIVED]

**This CONFIRMS the brief's stated expectation (and the weight doc's diagnosis):** the
scale/discreteness candidate lived in the ANGULAR-curvature term, which is precisely
what Branch G removes. So Branch G is a **smooth one-parameter (X) scalar-tensor family
with no intrinsic scale.** The scale-carrying physics is in Branch P (keep the angular
potential), NOT here. (Reported as OBSERVE, not as a verdict against the program: it
isolates WHERE the scale must come from — it is not in the gauged-away remnant.)

---

## 5. CRISP SUMMARY (what is forced / open in Branch G)

**OBSERVED / FORCED:**
- Field eqns: `f G + (g box - nabla nabla)f - X f(dphi dphi - 1/2 g (dphi)^2)=0` and
  `R - X(dphi)^2 - X box phi = 0`; combined `box phi = 12/(X-6)(dphi)^2`.
- Scalar phi is MASSLESS, curvature-sourced, NO potential.
- Vacuum = Schwarzschild (constant-phi branch, exact, all X) deformed by a 1/r SCALAR
  HAIR when phi' != 0: a two-parameter {mass m, scalar charge q} family. phi(r) monotone,
  phi' ~ 1/r^2. "Vacuum != GR" (extra hair), but smooth, static, scale-free.
- Large-|X| (healthy, Cassini-safe) limit = GR + weakly (1/X)-coupled massless scalar;
  Branch G ~ massless Brans-Dicke at omega=-X/4 -> -infinity.

**OPEN / FREE:**
- X: bounded to the half-line X <~ -1.7e5 by ghost+Cassini, but NOTHING internal fixes a
  value. A free continuous dial.
- The integration constants {m, q}: continuous (no quantization condition).

**SCALE/DISCRETENESS VERDICT: NO.** Branch G, on its own, produces no natural length and
no discrete structure — it is a smooth one-parameter (X) scalar-tensor family with two
continuous hair charges, the angular scale-term having been gauged away by construction.
Any UDT discreteness must live in Branch P (the kept angular potential) or in
quantization, NOT in this clean remnant.

---

## 6. ATTACK HERE (for a future blind verifier)

1. **Reduced-action EL vs covariant eqns.** I derived the SSS equations from the
   minisuperspace EL (IBP of the A'' term, boundary dropped). Re-derive the covariant
   metric+scalar equations and reduce them directly; confirm the same A'-constraint and
   that the dropped boundary term doesn't change the bulk equations.
2. **The constant-phi = Schwarzschild claim.** Re-substitute; confirm all three EL = 0.
3. **The 1/r^2 falloff / monotonicity.** Re-shoot with independent seeds and a stiff
   integrator; confirm phi' ~ r^{-2} and no turning point appears at any X or large seed.
   Push r_max higher to rule out a far-field scale.
4. **box phi = 12/(X-6)(dphi)^2.** Re-derive from trace+scalar; check the X-6 (ghost
   pole near X=6 = the omega=-3/2 conformal point) is physical, not an artifact.
5. **No-potential claim.** Confirm S_G truly contains no V(phi); the only phi-dependence
   is the overall e^{2phi} weight, which in Brans frame is pure kinetic normalization —
   verify the Einstein-frame map yields a FLAT scalar potential (=> genuinely scale-free).
6. **X really unfixed.** Look for ANY internal selection (a soliton regularity condition,
   an asymptotic-flatness + horizon-regularity coincidence) that might quantize or pin X
   or q. I found none; a regular-horizon analysis was not done (flag).

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a976ad512774380cc
SUPPORTED. Recomputed independently (sympy + scipy shoots): const-phi vacuum = Schwarzschild
EXACTLY (EL_A=EL_B=EL_phi=0); phi'!=0 family has phi'*r^2 -> q (scalar charge), monotone, no
turning radius, no oscillation, NO emergent length. Branch G is a scale-free two-charge {m,q}
massless-scalar-tensor (Fisher/JNW/Brans-I) family; X stays a free dial. The scale physics is
provably NOT here.
