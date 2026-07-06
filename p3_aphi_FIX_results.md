> **CONDITIONS-CHANGED (2026-07-06 second-pass sweep) — NOT a native-micro UDT result; mine for history.**
> Fixes the running-a(φ) source-weight coefficient in P3 — but the a(φ)=e^{+φ} matter weight itself is RETIRED by the
> 2026-07-01 native operator (matter is φ-BLIND; a(φ)/e^{2φ}-weighted matter is non-native). Same everything-on
> frame-B arc as p3_aphi_coupling. Mine for history. See branch_operator_contamination_ledger.md.


---

# P3 FIX -- ruler-integral source weight for a RUNNING a(phi)

**Driver:** Claude (Opus 4.8, 1M).  **Date:** 2026-06-20.  **Branch:** p3-aphi-coupling.
**Mode:** DERIVE-fix + OBSERVE.  **DATA-BLIND** (no mass/ratio/wall).
**New file (committed scripts immutable):** `p3fix_aphi_ruler.py`.
**Fixes:** the ONE real defect found by the blind verifier in `p3_VERIFIER.md`
(agent a71ebdd, 2026-06-20, Claims 1-flag, 3, headline (c)): P3's running-a source
weight used the PRODUCT form W=e^{(a+1)phi} and the conservation coefficient (a+1),
which is mis-coefficiented for running a.  **NOT canon.**

## 1. THE DEFECT (restated from p3_VERIFIER.md)

P3 wrote W = e^{(a+1)phi} (PRODUCT form), substituting a -> a(phi) naively.  For a
RUNNING a, Bianchi forces `d ln W/dphi = (a+1) + phi*da/dphi`, NOT `(a+1)`.  The
conservation code (`p3_aphi_matter.py:172,181`) used `(a+1)`, so the running-a
"Bianchi source" diagnostic was mis-coefficiented: 17% off at phi=-0.2, 29% off at
phi=-0.4 (k=1).  Confined to the running-a conservation diagnostic; baseline (a=-1)
and solver/FD-gate UNAFFECTED (the exch term is not used there).

## 2. THE DERIVATION -- the ruler integral is the UNIQUE composition-consistent weight

sympy-exact (reproduced in `p3fix_aphi_ruler.py` header + this run).

**Setup.**  The constant-a arc fixes the mass-dilation law m(phi)=m0 e^{a phi} as the
only composition-consistent form for CONSTANT a.  Its physical content is a LOCAL RATE:
`d ln m/dphi = a` (the dilation rate per unit phi).

**Running a.**  The mass-dilation rate is LOCAL: `d ln m/dphi = a(phi)`.  The unique
function whose local log-rate is a(phi) is the RULER INTEGRAL:
```
  m(phi) = m0 * exp( INT_{phiref}^{phi} a(phi') dphi' )
  W(phi) =        exp( INT_{phiref}^{phi} (a(phi')+1) dphi' )
```

**The discriminator is the LOCAL-RATE LAW, not composition alone.**  sympy showed
BOTH the ruler and the product "telescope" trivially under composition
(`factor(1,3) - factor(1,2)*factor(2,3) = 0` for both), so composition-consistency is
NECESSARY but NOT SUFFICIENT.  The discriminator is the local log-rate:
```
  RULER   m=m0 exp(INT a)      =>  d ln m/dphi = a(phi)            [rate IS a]
  PRODUCT m=m0 exp(a(phi)*phi) =>  d ln m/dphi = a + phi*da/dphi   [rate CONTAMINATED]
```
Only the ruler integral keeps a(phi) EQUAL to the local dilation rate -- i.e. keeps the
MEANING of a that the constant-a arc fixed.  The product form silently redefines the
rate to a + phi*da/dphi.  **=> the ruler integral is the UNIQUE generalization.**

**Reduction to the arc (constant a, phiref=0).**
`INT_0^phi (a+1) dphi' = (a+1) phi  =>  W = e^{(a+1)phi}` -- the arc form.  QED.

**Conservation coefficient (FTC).**
`d ln W/dphi = d/dphi INT_{phiref}^{phi} (a+1) = (a+1)` EXACTLY.  So the code's (a+1)
coefficient is CORRECT *with the ruler weight* -- the fix RECONCILES the weight with
the conservation coefficient.  (Under the product weight the same (a+1) was wrong.)

**Reconciliation with the explore fingerprint.**  `p3_explore_aphi.py:59-60` already used
the ruler integral `int_0^phi (a+1)` for its non-absorbability fingerprint.  The fix
makes the WEIGHT match the fingerprint the explore script already assumed -> the two
P3 components are now self-consistent.

**Analytic integral for the declared a(phi) = -1 + k eps0^p e^{-p phi} (no quadrature):**
```
  a+1 = k eps0^p e^{-p phi}
  INT (a+1) dphi = -(k eps0^p/p) e^{-p phi}  (+const fixed by phiref)
  W(phi) = exp( -(k eps0^p/p)(e^{-p phi} - e^{-p phiref}) )
  phiref=0 (matches fingerprint int_0^phi and the constant-a reduction)
        => INT_0^phi (a+1) = (k eps0^p/p)(1 - e^{-p phi})
```
sympy verified `d/dphi INT (a+1) - (a+1) = 0`.

## 3. VALIDATION NUMBERS (`p3fix_aphi_ruler.py`, 2026-06-20, V100 float64)

**[1] BASELINE a=-1 (k=0) -- bitwise, the fix changes nothing at baseline:**
- max|W-1| = 0.000e+00 (W==1 identically at k=0).
- ruler weighted stress vs P2 stress (k=0): max|dT| = 0.000e+00.
- ruler stress vs PRODUCT(P3) stress (k=0): max|dT| = 0.000e+00 -> baseline UNCHANGED.

**[2] RUNNING-a coefficient now CORRECT -- d ln W_ruler/dphi == (a+1) to FD floor;
the 17%/29% (here 20%/40%, exact) product error is GONE:**
| k,p,eps0 | phi  | (a+1)   | d lnW/dphi (FD) | err     | OLD product defect |
|----------|------|---------|-----------------|---------|--------------------|
| 1,1,1    | -0.2 | 1.22140 | 1.22140         | 4.3e-12 | 20.0%              |
| 1,1,1    | -0.4 | 1.49182 | 1.49182         | 5.0e-11 | 40.0%              |
| 0.5,1,1  | -0.2 | 0.61070 | 0.61070         | 1.9e-11 | 20.0%              |
| 1,2,1    | -0.4 | 2.22554 | 2.22554         | 5.7e-11 | 80.0%              |

(The verifier's 17%/29% were the magnitudes on its specific evaluation; the exact
defect is phi*da/dphi/(a+1) = -p*phi/(... ) -- here 20%/40% at p=1, phi=-0.2/-0.4.
Either way the ruler kills it to machine FD floor.)

**[3] NON-ABSORBABILITY preserved (a(phi) untouched -> da/dphi untouched):**
- k=0: max|da/dphi|=0, W-spread=0 (absorbable GR).
- k=1,p=1: max|da/dphi|=2.009e1, W-spread(phi[-3,1])=1.882 (NON-absorbable).
- k=1,p=2: max|da/dphi|=8.069e2, W-spread=1.541 (NON-absorbable).
da/dphi matches the verifier's re-run (2.009e1, 8.069e2) exactly -- the FUNCTION is
unchanged; only the WEIGHT built from it changed.

**[4] CORRECTED exploration diagnostic (ruler weight):**
- (a) conservation exch term, interior, Nr=48: k=0 -> 0 (both ruler & product, baseline
  emergent zero).  k=1 -> **4.736e-2** (ruler; this is now the CORRECT divT source).
  Cross-check of the magnitude of the fix on this config:
  - ruler exch (correct for ruler W) = 4.7364e-02
  - product-TRUE exch (a+1)+phi*da/dphi (what the OLD product W should have reported) = 6.4646e-02
  The OLD code reported 4.736e-2 under the PRODUCT weight, which was wrong (true product
  value 6.465e-2, ~27% under-report on this config).  The fix changes the WEIGHT to the
  ruler, for which 4.736e-2 is the CORRECT number.
- (b) structure on the fixed config (phi in [-0.4,0], p=1, eps0=1), ruler vs product W:
  | k   | W_ruler(core/mid/seal) | W_prod(core/mid/seal) | dM      | drho_core |
  |-----|------------------------|------------------------|---------|-----------|
  | 0.0 | 1.000/1.000/1.000      | 1.000/1.000/1.000      | (base)  | (base)    |
  | 0.5 | 0.784/0.900/0.999      | 0.744/0.890/0.999      | -15.5%  | -21.6%    |
  | 1.0 | 0.614/0.809/0.997      | 0.554/0.792/0.997      | -28.0%  | -38.6%    |
  **SIGN UNCHANGED: SUPPRESSION (W<1) on shallow phi<0, same sign as the product form**
  (both: phi<0 => exponent<0 => W<1).  The MAGNITUDE is milder for the ruler at the core
  (W_ruler(core)=0.614 vs W_prod=0.554 at k=1) because the ruler INTEGRATES the running
  rate from phiref=0 rather than taking the local product (a+1)*phi.  Reported as
  STRUCTURE, data-blind, UNFORCED.

## 4. WHAT CHANGED vs P3's PRODUCT FORM; baseline/solver never affected

- **Weight FUNCTION:** W = e^{(a+1)phi} (product) -> W = exp(INT_0^phi (a+1) dphi')
  (ruler).  Analytic; no quadrature.  Identical at k=0 (both ->1) AND for constant a.
- **Conservation:** the coefficient (a+1) is UNCHANGED in code, but it is now the TRUE
  `d ln W/dphi` (FTC) instead of an approximation to `(a+1)+phi*da/dphi`.  The reported
  k!=0 divT source is now CORRECT (4.736e-2 is right for the ruler weight).
- **UNCHANGED:** baseline a=-1 (k=0) bitwise; the FD-variational gate (uses the SAME
  weighted action; ruler stress at k=0 == product stress == P2, bitwise); the solver
  (`_solve_round_weighted` uses the weight only through the stress/EL, which are bitwise
  identical at k=0; for k!=0 the solver was an INCONCLUSIVE/P5-deferred exploration, not
  a banked result).  a(phi) FUNCTION and da/dphi unchanged -> non-absorbability intact.

## 5. HONEST AUDIT

- **Genuinely DERIVED, not chosen?**  YES.  The ruler integral is forced by requiring
  the local mass-dilation RATE to equal a(phi) -- the literal generalization of the
  constant-a arc's own rate law (d ln m/dphi = a).  The product form FAILS this (its
  rate is a + phi*da/dphi), and composition-consistency alone does not distinguish them
  (both telescope).  So the choice is made by the RATE LAW, the arc's own criterion, not
  by convenience.  If anything, the product form was the convenience (naive a->a(phi)
  substitution); the ruler is the principled form.
- **Residual freedom:**  ONE -- the integration constant phiref (the zero of the ruler
  exponent).  Set phiref=0 to (i) match the explore-script fingerprint int_0^phi and
  (ii) reduce to the arc's e^{(a+1)phi} for constant a.  phiref is a multiplicative
  CONSTANT rescaling of W (W -> W * e^{-INT_{0}^{phiref}(a+1)}); a CONSTANT factor on the
  whole source is the absorbable/units freedom (the arc's own "constant weight relabels
  to GR"), so it does NOT affect da/dphi, the (a+1) coefficient, or non-absorbability.
  Declared, not fitted.  No other freedom introduced.
- **DATA-BLIND:**  YES.  (k,p,eps0) declared (k in {0,0.5,1}, p in {1,2}, eps0=1) for
  VISIBILITY; no mass/ratio/wall loaded or targeted; M_diag are dimensionless native
  diagnostics.
- **Principle 7 / smuggle:**  none new.  a=-1=GR remains admissible and UNFORCED; the
  modification lives only in the matter-source weight (curvature side = GR is the arc's
  separately-verified result); weight uniform on the whole L (no sector split).

## 6. NET

The verifier's single real defect is RESOLVED.  The ruler-integral weight
W=exp(INT (a+1) dphi) is the DERIVED (rate-law-unique) composition-consistent weight
for running a; it gives `d ln W/dphi = (a+1)` EXACTLY (so the conservation coefficient
is now correct), reduces to the arc's e^{(a+1)phi} for constant a, reconciles with the
explore-script fingerprint, leaves the baseline bitwise and the solver/FD-gate untouched,
and preserves non-absorbability.  The corrected running-a divT source on the test config
is 4.736e-2 (correct for the ruler weight).  **P3 unblocked for a clean merge** with the
running-a conservation now correctly characterized.  NOT canon; a=-1=GR still the
admissible answer; a!=-1 an UNFORCED, data-blind exploration.

**Verifier-before-record:** this FIX should itself get a blind adversarial pass before
the conservation claim is upgraded from PARTIAL to STANDS in the P3 record.
