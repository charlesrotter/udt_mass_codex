# Native S² Matter on the Derived Operator — First Solve (RIGID slice = scale-free defect; the FULL object has a native radial DOF, unsolved)

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND, EMERGENCE-LED. **Status: BANKED — blind-verified
SUPPORTED-WITH-REVISIONS** (solver a37f373f640070876; verifier a77ae86f05269b650). **NOT canon.**
**Driver:** Claude Opus 4.8 (1M). 2026-06-21. The decisive Stage-2 solve of the COMPLETE 4-D SOLVER:
UDT's genuinely native matter object solved on the derived operator for the FIRST time.

## 0. CONTEXT
The object-identity re-derivation (archive/pre_2026-07-01/matter_object_identity_native_vs_import_results.md) established UDT's
native matter is the S²/π₂ winding (the round-gate soliton was the imported S³ baryon). This push SOLVED
the native object on the derived operator. **Key verifier revision: the first solve froze a legitimate
native DOF (a radial twist that stays ON S²) — so its "defect" verdict is SLICE-SCOPED, not a verdict on
the native object.**

## 1. WHAT WAS SOLVED (the rigid slice)
Native matter = degree-1 S² winding n=x/r=(sinθ cos mψ, sinθ sin mψ, cosθ), m=1, native cross-product (ε_abc)
L4 + L2, on the derived operator S=∫√−g[e^{2φ}R + X e^{2φ}(∂φ)² + e^{2φ}L_m], X=−2e5, kap8=1, ξ=κ=2e-2.
**RIGID:** n taken r-independent (no radial DOF). Unknowns A(r),B(r),φ(r), B=1/A free. Converged |F|~5e-8.

## 2. RESULT (the rigid slice — CONFIRMED algebra)
- **L_m = (−κ/2 − r²ξ)/r⁴** (verified independently).
- **T^t_t = T^r_r EXACTLY** (verified) ⇒ B=1/A holds to leading order; only a ~1/|X| scalar-hair break
  (NO matter-kinetic break — the qualitative contrast with the imported S³ object). [Revision: the exact
  EL_A−EL_B ∝ (A'+B') holds only in the hairless limit; in general it carries φ' terms suppressed by 1/|X|.]
- **SCALE-FREE GLOBAL-MONOPOLE DEFICIT:** ρ=κ/(2r⁴)+ξ/r² strictly monotone (no interior peak ⇒ no body/
  size); deficit e^{2B}→2/(2−ξ) depends only on dimensionless ξ. [Revision: the exact 2/(2−ξ) rides a
  factor-2 source-normalization convention; G=T convention gives 1/(1−ξ). Qualitative claims unaffected.]
- Tiny 1/|X| Fisher/JNW {q} hair.

## 3. THE TWO LOAD-BEARING REVISIONS (verifier — why this is SLICE-SCOPED, not a native verdict)
**R1 — the rigid reading IS a smuggled slice (decisive).** A unit-3-vector S² field can carry genuine
**radial texture WITHOUT escaping to S³**: the radial twist n with ψ→ψ+g(r) (a target-space rotation of the
hedgehog) stays exactly on S² yet has a nonzero radial kinetic term −(ξ/2)e^{−2B}sin²θ g'(r)². This native
radial DOF is exactly what supplies p_r (breaking the exact T^t_t=T^r_r / B=1/A), can produce a ρ-peak (a
real body/size), and can help regulate the core — ALL frozen by construction in the rigid slice. So
"scale-free defect, not a particle" is a property of the **rigid slice**, NOT of the native S² object.
(Corrects the over-strong "any radial profile = S³ import": a radial TWIST is native; only the 4th-component
escape Θ(core)=π was the S³ import. The round-gate object's Θ(r)-as-cosΘ(r) 4-vector sweep IS still the S³
import — that stands; but a native on-S² radial twist is a DIFFERENT, legitimate DOF.)
**R2 — the core is milder + maybe self-regulating.** The bare flat-measure ∫ρr²dr diverges, but with the
metric's PROPER measure e^B r² it softens to a LOGARITHMIC divergence (not κ/2r_c). No interior horizon
(e^{2B}→0), but e^{2A}=e^{−2B}→+∞ as r→0 (the result's "e^{2A} O(1)" was the edge value only). And the
operator's OWN scalar hair (e^{2φ}=e^{−2q/r}→0 at the core if q>0) is an OVERLOOKED candidate cap the
frozen-φ rigid analysis structurally could not test. So "finite-cell excision is the ONLY native regulator"
is NOT established — the hair cap and the radial-twist are both untested native candidates.

## 4. HONEST VERDICT (banked scope)
**BANKED (slice-scoped):** the RIGID degree-1 S² winding on the derived operator is a scale-free
global-monopole-type defect with a (log-)divergent core, B=1/A-to-1/|X|, no body. **NOT banked as a verdict
on UDT's native matter** — its radial twist DOF and its scalar hair (both able to localize a body / regulate
the core) are UNTESTED. Consistent with [[full-dimensional-complete-solver]]: a frozen-DOF slice yields no
verdict on the metric.

## 5. THE REAL NEXT STEP (Charles-directed: solve the fuller native freedom)
Solve the native S² object with its **radial DOF LIVE** — the radial twist g(r) (and ultimately the full
2-angle field Θ_t(r,θ,ψ),Φ_t(r,θ,ψ), free_s2_matter.py), staying ON S² (NO S³ escape), with **φ live**
(so the hair cap can fire), on the derived operator. Does a LOCALIZED, core-regulated native S² body appear
(a real particle), or does it stay a defect? THAT is the genuine native matter object. This is the decisive
test the rigid slice could not deliver.

## 6. PREMISE LEDGER
| item | status |
|---|---|
| native L2 + cross-product L4, n=x/r | DERIVED (CANON C-2026-06-14-1) |
| **rigid n=x/r (no radial DOF)** | **CHOSE — a SLICE (verifier R1); the native radial twist g(r) is a frozen legitimate on-S² DOF** |
| derived operator, X=−2e5, kap8=1, ξ=κ=2e-2 | DERIVED upstream / CHOSE (healthy value, source strength) |
| r_core=0.1, R_cell=8, finite-cell excision | CHOSE (canon D3) — but core is log-divergent + hair-cap candidate (R2), not excision-only |
| static, round | CHOSE (scope; off-round/time-live = later stages) |

## 7. ATTACK HERE (future)
1. Solve with the radial twist g(r) live (φ live): does B=1/A break, a body localize, the core self-regulate?
2. Does the scalar hair q>0 fire the e^{2φ} core cap (a coupled-solve output, not fixable blind)?
3. Re-confirm the deficit normalization convention (2/(2−ξ) vs 1/(1−ξ)).
4. The full 2-angle native field (free_s2_matter) off-round + time-live = the complete-solver stages.
