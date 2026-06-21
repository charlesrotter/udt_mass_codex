# Branch P Characterization — the Retained Angular-Curvature Potential

**Mode:** OBSERVE (report WHAT IS THERE; not verdict-hunting; the discreteness
hunch is TESTED, not confirmed-by-construction). Builds on
`native_dilation_weight_derivation_results.md` (the weight derivation; Sec 3 = the
surviving e^{2phi} potential after IBP).
**Constructor:** Claude Opus 4.8 (1M), agent for udt_mass_codex, 2026-06-21.
**Compute:** CPU only (sympy/scipy/numpy), bounded analytic + small ODE solves.
Scripts: `/tmp/branchP_{fieldeq,covariant,solve,scale,discrete,coupled}.py`.
**Status:** UNVERIFIED (no blind verifier pass yet) — record-candidate, not banked.

---

## 0. THE RETAINED OBJECT (re-derived, not invented)

From the weight derivation Sec 3, the weighted curvature density (areal SSS slice,
weight f=e^{2phi}) reduces, after IBP, to the shift-invariant BULK plus the
NON-invariant survivor:
```
sqrt(-g) e^{2phi} R  ->  2c sin(th)[ -2 r^2 phi'^2 + 2 r phi' + (e^{2phi} - 1) ]
```
The `(e^{2phi} - 1)` term is the survivor — the transverse/angular curvature `2/r^2`
weighted by e^{2phi} (the measure r^2 having absorbed the 1/r^2). Branch P KEEPS this
as a genuine source, i.e. an intrinsic potential
```
U(phi) = e^{2phi} - 1     (the retained angular-curvature potential).
```
This is the EXACT object Sec 3 isolated (verified `branchP_covariant.py`: the raw
covariant density `sqrt(-g)·(2/r^2)(e^{2phi}-1)` simplifies to `2(e^{2phi}-1)`,
r-independent — the survivor IS U(phi), no invention).

---

## 1. FIELD EQUATIONS (two-player, retained potential EXPLICIT)

Action:
```
S_P = INT sqrt(-g) [ f(phi) R + X f(phi) g^{mn} d_m phi d_n phi - 2 U(phi) ],
      f(phi) = e^{2phi},   U(phi) = e^{2phi} - 1,   phi INDEPENDENT.
```
(The "-2U" packaging puts the survivor on the same footing as a scalar potential; the
factor is bookkeeping.)

### (a) phi variation (covariant)
```
f'(phi) R  +  X f'(phi)(dphi)^2  -  2X nabla_m( f nabla^m phi )  -  2 U'(phi) = 0,
f'=2e^{2phi},  U'=2e^{2phi}.
```
i.e.  `2e^{2phi} R + 2X e^{2phi}(dphi)^2 - 2X[box phi + 2(dphi)^2]e^{2phi} - 4e^{2phi} = 0`.

### (b) metric variation (covariant, scalar-tensor WITH potential)
```
f G_mn + (g_mn box - nabla_m nabla_n) f
      = X f[ d_m phi d_n phi - 1/2 g_mn (dphi)^2 ]  -  g_mn U(phi).
```
The retained potential enters the metric equation as `- g_mn U(phi)` — a genuine
geometric SOURCE (an intrinsic, phi-dependent "cosmological-like" term), which is
exactly what Branch P asserts.

**PRINCIPLE-7 FLAGS (where "reduces to standard" is interrogated):**
- The R-coefficient f=e^{2phi} is NON-CONSTANT, so `(g_mn box - nabla_n nabla_n)f`
  does NOT vanish (Sec 5: box f = 2phi''+4phi'/r ≠ 0). Vacuum does NOT reduce to GR —
  the f-derivative terms survive. NO "folds to Einstein" step taken.
- The `-g_mn U(phi)` term is NOT dropped as "absorbable into Lambda": U is
  phi-DEPENDENT, so it cannot be gauged into a constant. Kept explicit.

### (c) Reduced radial phi-equation (areal SSS, the solve target)
Reduced radial density (per 2c sin th), combining f R bulk + X kinetic:
```
L_red = (X-2) r^2 phi'^2 + 2 r phi' + (e^{2phi} - 1).
```
Euler-Lagrange (sympy, `branchP_fieldeq.py`):
```
2(X-2) r^2 phi''  +  4(X-2) r phi'  -  2(e^{2phi}-1) = 0
=>   phi''  =  -2 phi'/r  +  (e^{2phi} - 1) / [ (X-2) r^2 ].          (***)
```
Let A = X-2. (***) is the master equation characterized below.

---

## 2. WHAT THE POTENTIAL DOES (numeric, bounded scipy)

### 2.1 The potential is a RUNAWAY, not a well
`U(phi)=e^{2phi}-1`, `U'(phi)=2e^{2phi} ≠ 0` for all finite phi. It has NO interior
minimum. Its only zero is at phi=0. So:
- The only UNIFORM (phi'=phi''=0) solution is phi=0 (where U=0).
- The potential gives phi a preferred VALUE (phi→0, the U=0 point), **not** a
  confining well around a nonzero depth.

### 2.2 The potential PINS phi's value (healthy window) — phi relaxes to 0
Integrating (***) (`branchP_solve.py`, `branchP_coupled.py`):
- For the HEALTHY / Cassini window (X large negative; the verifier's ghost-free,
  Cassini-safe window in the weight doc), A<0 and phi RELAXES toward 0:
  X=-2e5 → phi flat; X=-50 → 0.5↦0.26; X=-10 → 0.5↦0.03; X=-3 → 0.5↦0.000 at r=1e3.
- For X>2 (A>0, the ghost/Cassini-failing side) the outward branch RUNS AWAY / blows
  up (phi→-9 or integration fails). This side is already excluded by ghost+Cassini in
  the weight doc; here it also fails to give a bounded profile.

So in the physically-admissible window the retained potential acts as a RESTORING
agent that drives phi to its U=0 value. It LOCALIZES phi's VALUE (an asymptotic pin),
producing a smooth relaxing profile — NOT a sharp soliton, NOT a sized lump.

---

## 3. SCALE / DISCRETENESS — the HONEST verdict (tested HARD, not flattered)

### 3.1 The master equation is SCALE-INVARIANT — NO intrinsic length
Under r → μr, equation (***) maps to ITSELF (every term scales as 1/μ², verified
analytically `branchP_scale.py`). The deeper reason (`branchP_coupled.py`): the
angular curvature `2/r^2` carries a scale, but the measure `r^2` EXACTLY cancels it —
`sqrt(-g)·U_density = 2(e^{2phi}-1)`, r-independent. **The action carries no preferred
r.** Any solution with a feature at r=r* has a one-parameter family of rescaled copies.

=> **There is NO intrinsic length scale.** The orbit-area radius r is a coordinate
LABEL (an observable, yes — Sec 3's "cell size is physical" is correct in THAT sense),
but the DYNAMICS does not SELECT a value of it. Branch P gives phi a preferred VALUE,
not a preferred SIZE.

### 3.2 Linear structure: power-law, with a log-periodic sub-regime
Linearizing (***) about phi=0 (e^{2phi}-1≈2phi) gives an EQUIDIMENSIONAL (Euler)
equation `phi'' + (2/r)phi' - (2/A)phi/r^2 = 0`, indicial `s^2 + s - 2/A = 0`,
`s = [-1 ± sqrt(1+8/A)]/2`. Discriminant D = 1 + 8/A:
- **D>0** (A>0, or A<-8 i.e. X<-6 — includes the healthy large-negative-X window):
  two REAL powers → pure power-law, scale-free, NO oscillation, NO discreteness.
- **D<0** (-8<A<0, i.e. -6<X<2): COMPLEX powers → `r^{-1/2} cos(omega ln r)`,
  LOG-PERIODIC (self-similar), the only "oscillatory" regime.

Note the healthy Cassini window (X≈-1.7e5) sits in the D>0, plain power-law regime —
NO oscillation there at all.

### 3.3 The log-periodic regime is NOT a discrete spectrum
Tested HARD (`branchP_discrete.py`):
- Both indicial roots have Re(s) = -1/2 < 0 → BOTH linear solutions DIVERGE as r→0.
  **No regular-at-center solution exists.** The center BC that normally quantizes a
  radial problem is ABSENT — there is nothing to pair a seal against.
- The log-periodic oscillation accumulates infinitely many zero-crossings as r→0
  (self-similar): NO lowest mode, NO gap, NO discrete ladder. It is a continuous
  self-similarity, not a quantized set.
- Confirmed numerically: inward integration from r=10 drives phi→-54 (singular
  center), oscillation crossings accumulate toward r→0.

### 3.4 Could a SEAL produce discreteness? — only by IMPORTING a scale (flagged loud)
A "seal radius R" plus a center BC would, for a self-similar equation, quantize ratios
(log-periodic → discrete allowed R_n in geometric progression). BUT:
- There is NO regular center solution, so the inner half of the BVP pair does not
  exist natively (3.3).
- A seal radius R is an EXTERNALLY IMPOSED length — the equation fixes no scale, so R
  is **CHOSEN, not derived**. This is exactly the imported-boundary scar (cf. the
  imported winding-BC). Any "discreteness" obtained this way would be a property of the
  imposed seal, NOT of Branch P's metric. **I do not claim it.**

### 3.5 DISCRETENESS VERDICT
- **Intrinsic length scale: NO.** The retained angular potential's r-dependence is
  cancelled by the measure; the phi-sector equation is scale-invariant.
- **Sized soliton / cell: NO** (from the phi-sector alone). phi relaxes to a value;
  it does not lock a size.
- **Discreteness mechanism: NO** native one. The only candidate (log-periodic +
  seal) requires (i) a center BC that does not exist (no regular center) and (ii) an
  IMPORTED seal scale. Both premises are chosen, not derived → not bankable as native.
- What the potential DOES give natively: a preferred phi VALUE (phi→0) and a healthy
  relaxation basin in the ghost-free/Cassini window. A VALUE-pin, not a SIZE-pin.

This is the adversarial reading. The hunch (angular curvature → discreteness) is
**not confirmed** at the level of the static phi-sector: the angular term enters as a
runaway value-potential, scale-free, with no center regularity to quantize.

---

## 4. WHERE THE SCALE-CARRYING SECTOR LIVES (structural, NOT solved)

The weight doc's Sec 9 deepening: the SAME anisotropy obstructs BOTH the angular
curvature AND the time-live kinetic sector (g^{tt}~e^{+2phi} vs g^{rr}~e^{-2phi} carry
OPPOSITE shift-weight under reciprocity; once d_t phi ≠ 0 no single weight
invariantizes both). Structurally:
- In the STATIC angular sector alone (this document), the obstruction is a scale-free
  value-potential — it does NOT carry a length scale (Sec 3). The measure cancels its r.
- The TIME sector carries a DIFFERENT structure: d_t phi has NO r^2-measure cancellation
  protecting it, and the opposite-sign reciprocity means the obstruction there is a
  genuine kinetic (dynamical) one, not a static potential. A time-derivative term
  carries its own scale (a frequency), which the static analysis cannot cancel.
- Therefore the scale-carrying mechanism, IF one exists in Branch P, is expected to
  live in the phi-TIME interaction (or the phi-angular-time triple), NOT in the static
  phi-angular sector that this document fully characterized as scale-free. This matches
  the standing phi-angular(-time) hunch — but RELOCATES the active ingredient from the
  static angular potential (shown inert on scale) to the time-live sector.
- NOT SOLVED here (deferred heavy time-live solver). Stated structurally only.

---

## 5. PREMISE LEDGER (chose vs derived; BC flagged LOUD)

| # | Premise / choice | Status |
|---|---|---|
| Q1 | Retained term = U(phi)=e^{2phi}-1 (the Sec-3 survivor) | DERIVED (re-derived, sympy) |
| Q2 | Action S_P = f R + X f (dphi)^2 - 2U, f=e^{2phi}, phi independent | DERIVED form from weight doc; "-2U" packaging CHOSE (bookkeeping) |
| Q3 | f-variation & g-variation covariant equations | DERIVED (standard scalar-tensor variation) |
| Q4 | Reduced radial phi-equation (***) | DERIVED (sympy EL of L_red) |
| Q5 | Areal SSS static slice for the solve | CHOSE (CANON C-2026-06-18-1; same slice as weight doc) |
| Q6 | X in the healthy window (large negative) | constraint from weight doc (ghost+Cassini) — carried, not re-derived |
| Q7 | phi=0 chosen as the reference/asymptotic value | DERIVED (U's only zero; not an external pick) |
| **B1** | **A "seal radius" R as outer BC** | **CHOSE — and it IMPORTS a scale the equation lacks. Flagged: this is exactly where discreteness would be smuggled. NOT used to claim discreteness.** |
| **B2** | **Regular-at-center BC** | **CANNOT be imposed (no regular center exists, Re s=-1/2<0). Flagged: the usual quantizing BC is ABSENT natively.** |
| Q8 | r is a physical orbit-area LABEL (not dynamically selected) | DERIVED (measure cancels 2/r^2) |

---

## 6. ANALYTIC vs NUMERIC vs OPEN

- ANALYTIC: field equations (1); U runaway/no-well (2.1); scale-invariance of (***)
  (3.1); indicial equation & log-periodic regime (3.2); no-regular-center (3.3);
  measure-cancels-curvature (3.4/Q8).
- NUMERIC (bounded scipy, grids ≤600 pts): relaxation basin / phi→0 in healthy window
  (2.2); inward blowup & crossing-accumulation in log-periodic regime (3.3).
- OPEN (NOT solved, deferred): the time-live sector (Sec 4) — whether the phi-TIME
  obstruction carries a scale/frequency that the static angular sector does not. This
  is the live remaining route for Branch P to carry a scale; this document shows the
  STATIC angular sector does not.
- OPEN: chart-robustness of the scale-invariance was checked only in the areal slice
  here (the weight doc's verifier confirmed the obstruction itself is chart-robust;
  the scale-invariance argument rests on the measure/curvature cancellation which is
  covariant, but a second chart was not run — minor flag).

---

## 7. HEADLINE (honest, OBSERVE-mode)

Branch P keeps the angular-curvature survivor `U(phi)=e^{2phi}-1` as a genuine
potential. Natively it gives phi a preferred VALUE (phi→0) and a healthy relaxation
basin in the ghost-free/Cassini window — a VALUE-pin. It does **NOT** give a preferred
SIZE: the master phi-equation is scale-invariant (the r^2 measure cancels the 2/r^2
curvature), so there is no intrinsic length, no sized soliton, and no native
discreteness. The only oscillatory regime is log-periodic (self-similar), which is a
CONTINUOUS self-similarity with no regular center and no lowest mode — not a quantized
spectrum; turning it into a discrete set would require an IMPORTED seal scale and a
center BC that does not exist (both flagged). The hunch that the angular curvature
seeds discreteness is **NOT confirmed in the static phi-angular sector** — that sector
is scale-free. The remaining live candidate for a scale-carrier is the phi-TIME sector
(the same anisotropy obstructs it, but without the measure cancellation that neuters
the static angular term), which this document does not solve.

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a976ad512774380cc
SUPPORTED (all four claims). Recomputed independently: (2) the reduced equation is genuinely
SCALE-INVARIANT under r->mu r (every term ~1/mu^2, shown term-by-term) — the r^2 measure cancels
the 2/r^2 angular curvature; U=e^{2phi}-1 is a pure runaway that pins phi's VALUE (->0), not a
SIZE. (3) Indicial roots in the healthy window (X~-1.7e5) are real, both Re(s)<0 (no regular
center, no quantizing BC); the only log-periodic regime is the ghost/Cassini-EXCLUDED X in (-6,2),
and even there nodes accumulate at r->0 with no lowest mode / no gap = continuous self-similarity,
not quantization. (4) RELOCATION-TO-TIME is a SOUND POINTER, not an overclaim (the doc is correctly
hedged): a time-derivative term g^{tt}(d_t phi)^2 escapes the r^2 measure cancellation. BUT the
verifier discretized the LINEARIZED time-live operator (the new vacuum!=GR operator) on boxes
R=50..400 and found omega*R = 2.584 CONSTANT => omega~1/R => STILL BOX-CONTROLLED (continuum),
like prior time-live work. So linear time-live does NOT give a scale either. The ONLY remaining
classical redoubt is the genuinely NONLINEAR time-live solve (breathers/back-reaction, vacuum!=GR)
— UNADDRESSED, deferred (= the P5e heavy solver). Static angular sector scale-free: CONFIRMED.
