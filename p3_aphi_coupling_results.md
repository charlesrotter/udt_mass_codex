> **CONDITIONS-CHANGED (2026-07-06 second-pass supersession sweep) — NOT a native-micro UDT result; mine for history.**
> Ran a fully-coupled round solve on the PRE-NATIVE EH-era frame B (G^μν=8πe^{(a+1)φ}T^μν, curvature UNCHANGED,
> vacuum=GR) — the everything-on P-series (self-contained solver, no branch_operator import, so it slipped the first
> sweep's frame-A grep). It banks a frame-B soliton (exists + converges) with an M_MS mass table AND studies the
> a(φ)=e^{+φ} MATTER WEIGHT — both retired by the 2026-07-01 native operator (EH-empty; matter is φ-BLIND, so the
> a(φ) weight is non-native). Re-run on the native operator before use. See branch_operator_contamination_ledger.md.

# P3 -- the a(phi) matter-coupling CAPABILITY: results

**Phase:** P3 of the everything-on solver (EVERYTHING_ON_SOLVER_BUILD_MAP.md, premise
ledger **L-a**).  **Driver:** Claude (Opus 4.8, 1M).  **Date:** 2026-06-20.
**Mode:** P3a/P3b = wiring + binding validation; P3c = OBSERVE (declared, separate).
**Branch:** p3-aphi-coupling.  **DATA-BLIND** (units L=sqrt(kappa/xi)=1; no mass/ratio/
wall number loaded, compared, or targeted; the M_MS-like numbers are dimensionless
soliton-mass solver diagnostics in native units).  **Append-never-edit.  NOT canon.**

Governing: EVERYTHING_ON_SOLVER_BUILD_MAP.md (L-a), POST_POSTULATE_PROGRAM.md, the
field-equation arc (udt_field_equations_derivation_results.md,
udt_a_exponent_derivation_results.md, a_function_both_extremes.py).  Builds on P2
(p2_matter_fullmetric_results.md + p2_VERIFIER.md): the native S^2 UNIT carrier whose
stress AND EL both live on the full off-diagonal metric (FD-gate proven).
Committed scripts IMMUTABLE; new files only; verifier-before-record.

---

## REGIME STAMP / PREMISE LEDGER

| Item | Value | chose / derived |
|---|---|---|
| source weight | **e^{(a+1)phi}** on the matter ACTION DENSITY (-> stress, EL) | DERIVED placement (field-eqn arc sec.3/2b) |
| phi identification | **phi = b** (g_rr = e^{2b} = e^{2phi}, CANON C-2026-06-18-1); read off the metric | DERIVED (not a new field) |
| a(phi) form | a(phi) = -1 + k*eps0^p*e^{-p phi} | DERIVED form (a_function_both_extremes.py) |
| BASELINE | k=0 => a=-1 => W==1 => GR | FIXED baseline (the validated zero point) |
| EXPLORATION params | k in {0.5,1.0}, p in {1,2}, eps0=1 | **DECLARED, NOT fitted** (visibility on native phi range) |
| modified conservation | div T = -(a+1) phi' T (Bianchi-forced; k=0 -> div T=0) | DERIVED (sympy + arc) |
| carrier / matter EL | native S^2 UNIT, F(r,th,ps) free, autograd EL on full off-diag metric | reused (P2) |
| metric | general 4x4, off-diag e_rt,e_rp,e_tp live; B=1/A FREE | reused (P1/P2) |
| time row | ZEROED | scoped out (P4) |
| grid | Cheb_r x GL_theta x Fourier_psi; Nr=40-48, Nth 8-12, Nps 4-8 | CHOSE (tractability) |

---

## 1. WHAT WAS BUILT (new files; committed scripts untouched)

- **`p3_aphi_matter.py`** -- the a(phi) capability:
  - `phi_from_metric(g)` = 0.5 ln(g_rr): phi READ OFF THE METRIC (phi=b), DERIVED
    identification (CANON C-2026-06-18-1), so the weight tracks the ACTUAL solved metric,
    no double bookkeeping / no separate phi field.
  - `a_of_phi`, `weight_W`: the declared a(phi) = -1 + k eps0^p e^{-p phi} and
    W(phi)=e^{(a+1)phi}=e^{k eps0^p e^{-p phi} phi}.  k=0 => a==-1 => W==1 (machine-exact).
  - `stress_s2_weighted`: Tw = W(phi) * T(L) -- the weight multiplies the Hilbert stress
    of the SAME density it weights (Tw = -2/sqrt(-g) d(sqrt(-g) W L)/dg = W T exactly,
    since phi is the external geometric multiplier, not a metric DOF varied here).
  - `matter_action_weighted`, `matter_el_s2_weighted`: S_w = int sqrt(-g) W L dV and its
    autograd EL.  The SAME weighted action builds the weighted stress AND the EL ->
    mutually consistent BY CONSTRUCTION -> modified conservation emerges (not imposed).
  - `modified_conservation_residual`: the generalized divT gate -- computes
    nabla_mu T^mu_nu, the forced exchange -(a+1) phi_,mu T^mu_nu, and the welded
    nabla_mu(W T^mu_nu).
- **`p3_validate_baseline.py`** -- P3b (the binding baseline validation) + the weighted
  round-S^2 solver `_solve_round_weighted` (identical to p2_round_s2_solver at k=0).
- **`p3_explore_aphi.py`** -- P3c: non-absorbability, the weighted FD-variational gate,
  the fixed-config structure observation, and the coupled round solve at k!=0.

### WHERE the weight is placed, and WHY (the placement = the smuggle-risk; cite the arc)

The arc banks (twice blind-verified):
`G^mu_nu = (8piG/c^4) e^{(a+1)phi} T^mu_nu`, curvature side UNCHANGED, vacuum=GR; the
modification is a UNIFORM weight on the matter SOURCE (udt_field_equations sec.3, sec.2b;
udt_a_exponent sec.0).  The weight is placed on the **matter ACTION density**:
`S_matter = int sqrt(-g) W(phi) L d^4x`, NOT hand-multiplied onto an assembled stress.
Three reasons (header of p3_aphi_matter.py): (1) it is the action the field equation
derives from, so this is the DERIVED placement; (2) phi is the geometric potential read
off the metric (phi=b), a position-field MULTIPLIER on the density, not a function of the
matter field; (3) consequently Tw=W T and EL=delta S_w/delta F carry the SAME W, so
stress & EL stay consistent and the modified conservation EMERGES from Bianchi rather
than being imposed.  **SMUGGLE FLAG (avoided):** weighting only ONE sector (kinetic X)
would smuggle a "which invariant is the mass" choice (the udta sec.3 a_eff split) -- we
do NOT; we weight the whole L (=L2+L4) uniformly, exactly as banked.

### The modified conservation (sympy-verified)

`nabla_mu(W T^mu_nu)=0` (Bianchi, curvature side unchanged) =>
`nabla_mu T^mu_nu = -(1/W) d_mu W T^mu_nu = -(a+1) phi_,mu T^mu_nu`.  For W=e^{(a+1)phi},
(dW/dphi)/W = a+1; a=-1 => coefficient 0 => standard div T=0.  This is exactly the arc's
`div T = -(a+1) phi' T`.

---

## 2. P3b -- BASELINE a=-1 (k=0) reproduces P2 EXACTLY (the BINDING validation)

`p3_validate_baseline.py`, on a representative NON-diagonal, position-dependent-phi config
(phi in [-0.4,0]; e_rt,e_rp,e_tp live):

| check | result | required |
|---|---|---|
| [1] weight at k=0 | max\|W-1\| = **0.000e+00** | 0 |
| [2] exchange coeff (a+1) at k=0 | max\|a+1\| = **0.000e+00** | 0 (modified-cons. term vanishes) |
| [3a] weighted stress vs P2 stress | max\|dT\| = **0.000e+00** (rel 0) | 0 |
| [3b] weighted EL vs P2 EL | max\|dEL\| = **0.000e+00** (rel 0) | 0 |
| round-S^2 M_MS (weighted k=0) | **122.982071**, Phi=2.04e-16 | == P2: 122.982071 |
| \|dM_MS\| | **0.000e+00** | ~0 |

**P3b VERDICT: PASS -- a=-1 reproduces P2 BITWISE.**  Weight identically 1, exchange term
identically 0, stress/EL/M_MS bit-for-bit identical to P2.  The wiring is correct.

---

## 3. P3c -- the a(phi)!=-1 EXPLORATION (OBSERVE, declared, SEPARATE)

**THIS IS NOT THE UDT ANSWER.**  The arc does NOT pin a (udt_a_exponent: a is
UNDER-DETERMINED; a=-1=GR fully admissible).  This is a DECLARED hypothesis with stated
(k,p,eps0), UNFORCED at the principle level, reporting STRUCTURE, data-blind.

### 3.1 Non-absorbability (the precondition -- MET)

The banked criterion (arc sec.2b, blind-verified): a CONSTANT a relabels to GR
(absorbable -- a global units rescale of the matter ruler removes a constant exponent);
only a POSITION-DEPENDENT a(phi), da/dphi != 0, is genuinely NON-absorbable (the
matter/metric ruler ratio e^{-(a+1)phi} RUNS with phi, which no global units choice
flattens).

| a(phi) | da/dphi max\|.\| | verdict |
|---|---|---|
| k=0 (a=-1) | **0.000e+00** | CONSTANT a -> ABSORBABLE = GR relabel (the baseline) |
| k=1,p=1,eps0=1 | **2.0e+01** | POSITION-DEPENDENT -> NON-ABSORBABLE, genuine |
| k=1,p=2,eps0=1 | **8.1e+02** | POSITION-DEPENDENT -> NON-ABSORBABLE, genuine |

The declared k!=0 a(phi) is a genuine FUNCTION of position; the exploration is NOT an
accidental constant relabel.  **Precondition MET.**

### 3.2 Consistency gate (weighted FD-variational + modified-conservation)

The weighted autograd EL equals the FD variation of the SAME weighted action on a FULL
off-diagonal metric (the decisive P2-style gate; the covariant divT operator is
gate-Nth-limited off-round on the dense-Newton driver -- P2 sec.3 -- so this is the clean
substitute):

| k | max rel-err (EL vs FD dS_w/dF) | modified-cons. exchange term (interior) |
|---|---|---|
| 0 | **1.3e-5** (FD floor) | **0.000e+00** (= standard div T=0, baseline) |
| 1 | **9.3e-6** (FD floor) | **4.7e-2** (genuine nonzero Bianchi source) |

=> weighted stress & EL are mutually consistent for k=0 AND k!=0; the modified
conservation term is exactly 0 at baseline and a genuine source at k!=0.

### 3.3 What the weight DOES to the structure (OBSERVE, not target)

**Fixed config** (phi in [-0.4,0]; eps0=1,p=1): over this SHALLOW positive-side-ish
range, (a+1)>0 and phi<0 => W=e^{(a+1)phi} < 1 -> the weight **SUPPRESSES** the source
here (honest sign note: my draft inline comment said "amplifies toward the core" -- on
THIS config's phi>=-0.4 range the realized effect is suppression; amplification W>1 would
require deeper phi where (a+1)phi changes character.  Reported as observed, not as a
target.):

| (k,p,eps0) | W(core/mid/seal) | rho(core) | M_diag | vs baseline |
|---|---|---|---|---|
| (0,1,1) baseline | [1.000,1.000,1.000] | 1.283e3 | 1.3267 | -- |
| (0.5,1,1) | [0.744,0.890,0.999] | 9.54e2 | 1.0888 | dM=-17.9%, drho_core=-25.6% |
| (1.0,1,1) | [0.554,0.792,0.997] | 7.10e2 | 0.9033 | dM=-31.9%, drho_core=-44.6% |

**Fully-coupled round solve** (same dense-Newton driver as P2; converges to floor):

| k | Phi | M_MS | tag |
|---|---|---|---|
| 0.0 | 2.04e-16 | **122.982071** | baseline (GR) |
| 0.5 | 6.16e-17 | **122.508006** | DECLARED a(phi)!=-1, UNFORCED, not the answer |
| 1.0 | 8.49e-16 | **121.718529** | DECLARED a(phi)!=-1, UNFORCED, not the answer |

**WHAT IS THERE:** (i) the weight is a genuine, non-absorbable, position-dependent
reweighting of the source that the solver carries cleanly; (ii) the coupled round soliton
**continues to exist and converge to floor** with the weight on -- a(phi)!=-1 does not
destroy the localized solution at this phi-range; (iii) the M_MS shift is SMALL (122.98
-> 121.72 over k=0..1) BECAUSE this round soliton's phi stays shallow (b core ~ -0.4 in
this configuration), so W stays near 1; the weight's leverage GROWS with deeper phi
(the e^{-p phi} carrier) -- the deep-core regime where the arc expects an O(1) departure
is NOT reached by this shallow round anchor (deferred; needs the deep-core P6 + P5).

---

## 4. AUDIT (every compromise, honestly)

- **PLACEMENT choice (the one load-bearing decision):** weight on the matter ACTION
  density (-> W T stress, W-carrying EL), the DERIVED placement per the arc.  Flagged;
  the alternative (single-sector / hand-patched-stress) was explicitly NOT taken (it
  would smuggle a mass-invariant choice).  phi=b read off the metric (DERIVED).
- **phi as external multiplier, NOT a varied metric DOF (a real subtlety):** the arc
  treats phi as the geometric potential; here phi=0.5 ln(g_rr).  In `stress_s2_weighted`
  W multiplies T as a scalar (Tw=W T).  This MATCHES the arc's banked source weight
  exactly.  CAVEAT (flagged): if one later varies phi=b AS a metric DOF inside the
  Hilbert variation, W would contribute an extra delta W/delta g term -- that is the
  curvature-side question the arc explicitly leaves to the (still-unbuilt) native
  curvature action (BUILD_MAP sec.VII caveat b).  P3 stays within the arc's GR-form
  field equation with the matter weight; this is scoped, not hidden.
- **a!=-1 is UNFORCED and NOT the answer:** stated everywhere.  a=-1=GR remains
  admissible (arc: a under-determined).  k,p,eps0 DECLARED, not fitted.  Non-absorbability
  shown (da/dphi!=0), so the exploration is not an accidental constant relabel.
- **Sign honesty:** over the tested shallow phi range the weight SUPPRESSES the source
  (W<1), not amplifies -- corrected in the report vs a loose inline comment.
- **Covariant divT gate is gate-Nth-limited off-round** (inherited from P2 sec.3) --
  reported as such, NOT forced; the FD-variational gate is the clean substitute and the
  weighted EL passes it (rel-err ~1e-5) for k=0 AND k=1.
- **Shallow-anchor limitation (the real scope cut):** the round soliton's phi stays
  shallow, so the weight's effect is modest; the deep-core O(1)-departure regime the arc
  anticipates is NOT reached here -- it needs the honest deep core (P6) and the
  research-grade driver for large-shear/deep-phi (P5).  Flagged, not a verdict.
- **No B=1/A injection, no Skyrme m*pi BC, no dropped/added term, no kept linearization.**
  Grep-clean across P3 files (autograd/spectral/FD-Jacobian = sanctioned exact numerics).
- **Time row ZEROED (P4).  The only other freeze.**
- **Data-blind?** CONFIRMED -- no mass/ratio/wall number loaded, compared, or targeted;
  (k,p,eps0) declared; diagnostics in native L-units only.

---

## 5. SCOPED STATUS

**P3 = DONE (capability wired + baseline validated bitwise) + the exploration delivered
as a declared, UNFORCED observation; the deep-phi regime deferred.**

DONE:
- The e^{(a+1)phi} weight is wired into the matter action -> stress -> autograd EL
  consistently with the field-eqn arc (DERIVED placement, flagged); the modified
  conservation div T=-(a+1)phi'T is implemented and sympy-verified (k=0 -> div T=0).
- **P3b BINDING validation: a=-1 (k=0) reproduces P2 BITWISE** (weight=1, exchange=0,
  stress/EL/M_MS all 0.0 difference).  The wiring is correct.
- **P3c:** the declared a(phi)!=-1 is shown NON-absorbable (da/dphi!=0), passes the
  weighted FD-variational consistency gate (k=0 and k=1, rel-err ~1e-5), and the
  coupled round soliton stays converged with a small M_MS shift; structure observed,
  UNFORCED, NEVER the answer.

DEFERRED (honestly):
- The DEEP-phi (core) regime where the arc expects an O(1) a(phi) departure: the shallow
  round anchor does not reach it -> needs the honest deep core (P6) + research-grade
  driver (P5).
- The covariant divT identity to floor off-round: gate-Nth-limited (inherited P2; the
  FD-variational gate substitutes).
- phi varied AS a metric DOF inside the Hilbert variation (curvature-side W contribution):
  the native curvature-action question (BUILD_MAP VII-b), out of P3 scope.

**What P4 inherits:** a weight-capable native S^2 matter sector whose stress AND EL carry
the e^{(a+1)phi} weight on the full off-diagonal metric, with a=-1 the validated GR
baseline and a(phi)!=-1 a declared, non-absorbable, consistency-gated exploration knob
(k,p,eps0).  P4 turns on the time row on top of this; the deep-phi leverage of the weight
awaits P5/P6.

---

## ATTACK HERE (for a blind verifier)

1. **Does a=-1 (k=0) REALLY reproduce P2 bitwise?**  Run `p3_validate_baseline.py`:
   max\|W-1\|, max\|a+1\|, max\|dT\|, max\|dEL\| must all be 0.000e+00, and the weighted
   round M_MS must equal P2's 122.982071 to 0.0.  If any is nonzero, the weight leaks
   into the baseline = wiring bug.
2. **Is the placement the DERIVED one, or a smuggle?**  Read p3_aphi_matter.py header +
   confirm W multiplies the WHOLE action density (L2+L4), not one sector, and that
   Tw=W*T (stress) and EL=autograd of the weighted action (same W).  A single-sector
   weight or a hand-patched stress (W on T but not on the EL's action) would be the
   smuggle -- check both carry the SAME W.
3. **Is a!=-1 genuinely NON-absorbable, or an accidental constant relabel?**
   `p3_explore_aphi.py` show_nonabsorbability: da/dphi=0 for k=0 (constant, absorbable)
   and da/dphi!=0 for k!=0 (position-dependent, genuine).  If the explored case had
   da/dphi=0 it would be an absorbable relabel -- confirm it does not.
4. **Is the weighted EL the true variation of the weighted action?**  weighted_fd_gate:
   autograd EL vs FD dS_w/dF on a full off-diagonal metric, rel-err ~1e-5 for k=0 AND
   k=1.  If it fails for k!=0, the EL does not carry the weight = inconsistent stress/EL.
5. **Does the modified-conservation exchange term vanish at baseline?**  rel exch term
   = 0.000e+00 at k=0 (a+1=0), nonzero at k=1.  If nonzero at k=0, the modified
   conservation is mis-wired.
6. **Discipline grep.**  `grep -nE "m\s*\*\s*PI"` over P3 files -> none (no Skyrme BC);
   `grep -nE "1/A|b=-a|a=-b"` -> only the labelled B=1/A-free construction in the test
   config (a=-b is a FREE choice there, not an injected tie in the solver).  a=-1
   baseline + time-zeroed the only freezes.  Data-blind: no wall number anywhere.
