# H4·N4rev — flux-mass sign certification (corrected turnkey pipeline, real H3 field)

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | DERIVE-gated certification (close CF2 = sign of δm) on the corrected, MMS-validated turnkey pipeline, using the REAL H3 Q_H=1 shell-projected stress. |
| **Slice scope** | STATIC, Branch-P (W=1), single-object perturbative transverse response δh=−L_bare⁻¹T; native 2𝒦→φ channel (NO G=8πT). Real stress from `hopfion_arc_scripts_2026-07-05/prod_an256.npz` (N=256, L=6). ξ=κ=1 (data-blind gauge). Z_φ swept {1,8}. φ_amb swept for the far-field regime. |
| **Observing or targeting?** | OBSERVING the sign, aimed HARDEST at the standing hypothesis (prior positive-mass lean). Halt-don't-salvage: a δm<0 OR a non-certifiable sign is a FINDING — banked, not patched. NOT tuned to land positive (or negative). |
| **Verifier status** | Self blind-checks (r-window + grid scans) + independent blind adversarial pass (agent a79ec540e0269d8fe, 2026-07-10) framed to REFUTE the box-control (rescue a robust sign): box-control CONFIRMED. See §6. |
| **Build-on grade** | **CONDITIONAL / scoped negative** — CF2 does NOT close in the single-object frame; the sign is box-controlled. Confirms the prior Outcome D (`H4_N4rev_conditional_mass_response_results.md`); does NOT overturn it. Do NOT bank a mass sign; do NOT patch by fixing the cutoff. |
| **Re-run** | `PYTHONPATH=$(pwd) python3 h4_scripts/extract_stress_rtheta.py` (shell-projects → `h4_scripts/stress_rtheta_h3.npz`); `PYTHONPATH=$(pwd) python3 scratchpad/run_n4rev_real.py`. Pipeline: `n4rev_response_TURNKEY.py::run`, `h4_scripts/lbare_inverse.py`. |

### Premise ledger

| Item | Tag |
|------|-----|
| H3 field `prod_an256.npz` (N=256, L=6) | **DERIVED** (arrested-Newton, blind-verified Outcome A). Verified on disk: \|Q\|=0.9917, Ehat=286.52, E2/E4=0.9995 — exact banked match (regeneration unnecessary; on-disk field IS the banked one) |
| L_bare = r²f''−2rf'+2f (roots {1,2}) | **DERIVED** (linearized transverse EL of Branch-P action; `op_derive2.py`), unit-tested; GREENBUG-free inverse `lbare_inverse.py` |
| Perturbative δh=−L⁻¹T reduction | **FRAME** — valid for a sign only if the sign is cutoff-robust; magnitude NOT physical (ε≈10–15≫1 banked) |
| Z_φ ∈ {1,8} | **FREE fork** (not canon-frozen; live solvers use 8). Sign of δq is Z_φ-independent (Zf>0 divides); only regime crit depends on it |
| φ_amb (ambient depth) | **FREE physical input** — swept for the regime |
| ξ=κ=1 | **FREE data-blind gauge** |
| inner core cutoff r_lo | **CHOSE-BC** (Dirichlet f=0 at r_lo) — **this is the box-control knob** |
| native 2𝒦→φ, G=8πT forbidden | **THEORY** (Principle 7) |

---

## 1. What ran cleanly (solid)

- **H3 field verified** against banked invariants EXACTLY (|Q|=0.9917, Ehat=286.52, E2/E4=0.9995). The
  on-disk checkpoint is the banked field; no regeneration needed (and regenerating could land a
  differently-converged snapshot — using the banked field is both purer and cheaper).
- **Stress shell-projected** (`extract_stress_rtheta.py`): sector integrals trace≈−98, shear≈+146,
  T_rr≈+90 — signs and rough magnitudes reproduce banked (−90/+139/+90); ~5–9% on trace/shear is
  binning-resolution, sign structure identical.
- **Pipeline MMS re-validated:** S3 screened-φ stage converges at rate 4.00 (2nd order) at φ_amb∈{1,3};
  L_bare BVP interior residual ~7e-11; solve_Lphi residual ~6e-12 (verifier §6). GREENBUG genuinely gone.
- **Far-field REGIME (delivered, clean):** the screened-φ far-field is a **clean 1/r monopole for
  φ_amb > crit = ½ln(32/Z_φ)** (=1.733 at Z_φ=1, 0.693 at Z_φ=8) and **screened/oscillatory (no clean
  monopole; C1 read-radius dependent) for φ_amb < crit**. Matches the N4a corrected "deep⇒clean 1/r"
  reading. This half of the dispatch is delivered and solid.

---

## 2. CF2 sign — BOX-CONTROLLED (not certifiable in this frame)

The sign of δm = −δq **flips with the arbitrary inner core cutoff r_lo** (outer 6.0, Z_φ=1, φ_amb=3;
verifier-authoritative, grid-converged at each cutoff):

| inner cutoff r_lo | δq | δm=−δq | far-field C1 | mass sign |
|---|---|---|---|---|
| 0.2 | +47.3 | −47.3 | (spike-fragile) | **NEGATIVE** |
| **0.3** (turnkey default) | −2.81 | +2.81 | −(pos) | **POSITIVE** |
| 0.4 | +4.43 | −4.43 | +(neg) | **NEGATIVE** |
| 0.5 | +5.26 | −5.26 | +(neg) | **NEGATIVE** |
| 0.6 | +3.33 | −3.33 | +(neg) | **NEGATIVE** |

**Only the turnkey default r_lo=0.3 gives positive mass; every neighboring cutoff gives negative.** Both
readings (raw δq AND the far-field monopole C1) flip. The prior positive-mass lean was an artifact of
reading at 0.3.

**Root cause (structural, NOT the GREENBUG):** near the core the flux density `ell2 ~ 1/r²`
(verified: ell2·r² ≈ const ~150–195 as r→0), because the transverse response follows the growing root
(abar~r) and L_bare's indicial roots {1,2} leave **no decaying homogeneous mode** to anchor a convergent
monopole. Hence **∫ell2 dr diverges as r_lo→0** (∝1/r_lo, verified: partial ∫ to r=1 grows 2.3 → 9.3 →
66 → 326 → 741 → 1314 as r_lo: 0.3→0.25→0.2→0.15→0.12→0.10). The "mass" is not a convergent localized
quantity — it is a whole-cell property, exactly the prior Outcome-D diagnosis.

**Rescue attempts (all FAIL — no principled cutoff-robust sign exists):**
- *Far-field flux:* robust to the OUTER read radius (a real far-field statement) but its VALUE/sign is
  inherited from the divergent inner cutoff — not robust to r_lo. Not a rescue.
- *Regular-core (r_lo→0):* δq → +∞ (unbounded core artifact), and contradicts the intermediate-cutoff
  signs. Not a finite certifiable mass.
- *Reweightings* (∫ell2·r², ∫ell2·r⁴, singular-1/r² subtraction): each flips sign with the cutoff. Not a rescue.

---

## 3. Verdict

**The corrected pipeline does NOT close CF2.** The GREENBUG fix repaired the *magnitude* inflation, but the
*sign* was never the bug — it is **box-controlled** at the structural level (no decaying L_bare mode ⇒ core
divergence ⇒ cutoff-dependent sign). This **CONFIRMS Outcome D**; it does not overturn it. The honest
statement is **"no robust sign in the single-object frame"** — NOT positive (needs cutoff 0.3), NOT negative
(needs 0.4–0.6).

---

## 4. Solver-first accounting (mismatch → frame, not mechanism)

Per the N4 pre-registration's own halt logic, a non-closing CF2 **indicts the SINGLE-OBJECT frame first,
solver second, metric last, mechanism never.** The single-object core cutoff (Dirichlet f=0 at an arbitrary
r_lo) is exactly the knob doing the damage; the mass is not a localizable single-object flux. The mass lives
in the **whole-cell (N5) treatment** (seal flux M = Z_φ ρ_s² φ'(r_s), a whole-cell response — Registry #76),
not a divergent core integral. No mechanism is added; no cutoff is fixed to force a sign.

---

## 5. NOT claimed

- NOT: δm > 0 (positive mass) — that requires cherry-picking the r_lo=0.3 default; neighboring cutoffs give negative.
- NOT: δm < 0 (negative mass) — that requires cherry-picking r_lo∈{0.4,0.5,0.6}; no cutoff is privileged.
- NOT: a physical magnitude (perturbative frame invalid at ε≫1; and the integral diverges anyway).
- NOT: an overturn of Outcome D — this CONFIRMS it with the corrected pipeline.
- NOT: any mass, ratio, particle, or SNe/cosmology claim. No G=8πT. Data-blind throughout.
- The REGIME result (clean 1/r for φ_amb>crit, screened below) IS claimed — it is cutoff-robust and MMS-validated.

---

## 6. Verifier status — DONE (blind adversarial, agent a79ec540e0269d8fe, 2026-07-10)

Independent zero-context pass, framed to REFUTE the box-control (try hard to rescue a robust sign),
own regenerated numbers:
- **Sanity GREEN:** real stress (trace −97.9, shear +144.0), L_bare BVP residual 7.3e-11, solve_Lphi 5.9e-12.
- **Sign flip CONFIRMED** across r_lo∈{0.2…0.6}; grid-converged at each fixed cutoff (0.2: 35→52.4 over
  N=121→1921; 0.5: 5.41→5.21) — a cutoff effect, NOT a grid/numeric bug. (Corrected the author's [0.2]
  mislabel: δm is NEGATIVE there, and its value is itself spike-fragile — strengthening box-control.)
- **Divergence CONFIRMED:** ell2·r²≈const → ell2~1/r² → ∫ell2 dr ~ 1/r_lo diverges as r_lo→0.
- **All rescue attempts FAIL:** far-field flux (robust to outer radius only, value set by inner cutoff),
  regular-core (δq→+∞), reweightings (all sign-flip with cutoff). No principled cutoff-robust sign.
- **Overall: box-control CONFIRMED; the author is correct.** Verifier scratch: `scratchpad/verify.py … verify4.py`.
