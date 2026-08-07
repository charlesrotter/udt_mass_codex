# ADVERSARIAL REVIEW 1 — algebra / at-source (Step 3)

Date: 2026-08-06. Reviewer: independent adversarial agent (fresh context). Method: ALL
recomputations performed in fresh sympy, written from the flux identity and the metric alone —
NO step-3 code opened or imported (`step3_checks.py` untouched; independence preserved).
Scripts: scratchpad `adv1_a.py` (core-seat onset; general activation; no-ρ-pin counterfactual)
and `adv1_b.py` (off-core dipole; boost test; C4/C5/C6). All source citations re-read at source.
NOT committed by this reviewer.

## Attack 1 — the core-seat quartic (the single load-bearing step): **CONFIRMED**

Independent re-derivation, method deliberately different from the notes' (undetermined
coefficients in the φ-EL φ'' = 4e^{−2φ}ρ'²/(Zρ²) − 2φ'ρ'/ρ with φ(0)=φ_c, φ'(0)=0, rather
than the flux-integral iteration):

- Generic member ρ = ρ_c + (a/2)t² + (b₃/6)t³ (both core pins on): z(t) coefficients at
  t¹, t², t³ are IDENTICALLY ZERO; t⁴ coefficient = a²e^{−2φ_c}/(3Zρ_c²) — exact match.
  z', z'', z''' vanish at the seat as claimed (φ' ∝ t³; and φ''(r_c) = 4e^{−2φ_c}ρ'(r_c)²/(Zρ_c²)
  = 0 rides exactly on the ρ-pin).
- Proper-distance conversion independently reverted: z(d) coefficients d¹..d³ ≡ 0,
  d⁴ coefficient = a²e^{−6φ_c}/(3Zρ_c²) — exact match, including the depth-amplification
  factor e^{−6φ_c}. Areal-excess form z = 4e^{−2φ_c}/(3Zρ_c²)·(ρ−ρ_c)² matches through t⁴.
- General activation ρ' = a·t^α: verified at α = 2 (all coefficients below t^{2α+2} vanish;
  leading coefficient = 4a²e^{−2φ_c}/((2α+1)(2α+2)Zρ_c²) exact). Degeneracy only flattens:
  no strike weakens.

**The transplant hypothesis FAILS.** At source (`universe_cell_fold_jc_sigma_results.md:37-38`
and the derived-pin table line 106): the inner EVEN fold's stationarity ALONE pins
**φ'(r_c) = 0 AND ρ'(r_c) = 0** at the CORE (φ_c, ρ_c free). The seam pin ρ'(r_s) = 0 is a
SEPARATE, fold-closure-only pin (Step-2 CUT-4). Step 3 did not transplant a seam pin; the
core ρ-pin is the even-core geometry's own, and it is shared by 𝒜_fold and 𝒜_glue by
construction (Step-2 §II: "Cell geometry unchanged").

**Counterfactual computed anyway** (the review's own stress test): with φ'(r_c) = 0 only and
ρ'(r_c) = b ≠ 0, the onset is QUADRATIC: z = 2b²e^{−2φ_c}/(Zρ_c²)·t² + O(t³) (in proper d:
coefficient 2b²e^{−4φ_c}/(Zρ_c²)). **The t¹ coefficient is STILL zero** — φ'(obs) = 0 alone
kills the linear term. So even if the ρ-pin were somehow struck from the record, the fold/glue
× core-seat D1-lin STRIKE would NOT flip (quadratic has no linear onset; this is exactly the
already-banked √z observe of `simple_metric_lowz_linear_native_derive.md` §2). The quartic
sharpening changes the exponent, not any verdict. No strike flips under either reading.

## Attack 2 — outer-closure blindness: **CONFIRMED**

Structural argument, checked at source: z(d) at an interior seat depends only on the local
germ of (φ, ρ); φ is slaved to ρ via the IVP launched from the INNER end (Φ(r_c) = 0,
φ'(r_c) = 0), so the germ at any seat r < r_s is a functional of ρ on [r_c, r] only — the
seam never enters at any finite order of the low-z expansion. Step-2 §II.2 defines 𝒜_glue as
𝒜_fold with ONLY the seam ρ-pin dropped; the inner even-core end (ρ'(r_c) = 0 + the same
φ-IVP) is verbatim UNCHANGED — the glue relaxes NOTHING at the inner end. (The one thing glue
adds — the free seam functional B — lives at r_s and touches no interior formula.) Hence every
Q3b formula carries verbatim to 𝒜_glue and "glue-as-admitted equally struck" is correct. The
only inner-end relaxation anywhere on the record is the free-core FORK, which Step 3 carries
explicitly as the (correctly labeled) non-admitted row 5. No missed relaxation found.

## Attack 3 — the off-core dipole: **CONFIRMED** (no boost escape at this order)

Independent series + reversion to proper d (both directions):
z_out = p₁e^{−φ₀}d + p₂e^{−2φ₀}d² + O(d³); z_in = −p₁e^{−φ₀}d + p₂e^{−2φ₀}d² + O(d³)
— exact match including the (nontrivial) cancellation of all p₁² cross-terms in the
reversion. Dipole = p₁e^{−φ₀}d = H*d EXACTLY through d² (the entire leading signal);
monopole = p₂e^{−2φ₀}d² = (e^{−2φ₀}φ''₀/2)d², quadratic only. Both match.

Blueshift direction: CUT-3 (flat-then-strictly-rising φ, forced within S + even core + the
anchor's Z > 0) gives p₁ = φ'(r_obs) > 0 at every off-core seat; inward sources sit at lower
φ ⇒ z_in < 0. Looking inward = toward the core = toward the φ-floor = down-depth: HALF-SKY
BLUESHIFT at leading order is correct (the d² monopole shifts the zero-z boundary at higher
order; the leading-order statement is exact as stated).

Boost escape: NO. A local observer boost adds a kinematic dipole −(v/c)cosθ·(1+z) whose
leading term is INDEPENDENT of source distance; the position dipole is ∝ d. Total dipole
coefficient = H*d − v/c: it can be zeroed on exactly ONE distance shell (v = cH*d₀), leaving
a residual dipole ∝ H*(d − d₀) at every other shell (and a spurious constant dipole as
d → 0). A position dipole is not absorbable by any fixed boost at this order. The notes'
dipole/monopole → ∞ as d → 0 ratio statement also verified (∝ 1/d).

## Attack 4 — C4/C5/C6: **ALL CONFIRMED**

- **C4:** with 1+z = (1−r/X)^{−1/2}, D_A = r (chart-origin seat condition re-read at source,
  `simple_metric_DA_native_derive.md` §1 — the derivation is genuinely conditional on the
  observer at the areal origin, rays converging to a point), d_L = (1+z)²r:
  eliminating r gives d_L/X = (1+z)² − 1 = z(z+2) EXACTLY. Low-z: z = (d_L/X)/2 − (d_L/X)²/8
  + O³, i.e. slope 1/(2X); and H* = e^{−φ(0)}φ_L'(0) = 1/(2X) — consistent. Match.
- **C5:** flux identity re-derived under φ_L from scratch: (Zρ²φ_L')' = 4e^{−2φ_L}ρ'²
  reduces exactly to 4(m/X)u² − (Z/m)u − Z/(2m²) = 0, u = ρ'/ρ, m = X−r (the Step-2 quadratic
  re-obtained independently, sign-for-sign). u = 1/r (ρ = r) leaves a residual that is NOT
  identically zero (vanishes only at isolated cubic-in-r roots, measure zero) — ρ = r is NOT
  an S-realization of φ_L on any interval. Residue R-a stands, including its consequence:
  the WR-L areal sector (r²) and the S-embedded areal sector (ρ₊²) differ, so the banked
  d_L = (1+z)²·r does not automatically transfer in-cell.
- **C6:** at r = 0 the quadratic gives roots (Z ± √(Z²+8Z))/(8X); u₊(0) = (Z+√(Z²+8Z))/(8X)
  — exact match; root product −XZ/(8m³) < 0 (opposite signs, neither zero). u₊ finite on
  [0, r₀] ⇒ ρ(0) = ρ(r₀)exp(−∫u₊) > 0: no areal center along u₊. Residue R-b stands, and
  with it the load-bearing conditionality: D_A = r's seat condition (areal radius → 0 at the
  observer) is UNSATISFIABLE in-cell along u₊, so row 5's D1-shape entry is rightly
  CONDITIONAL on the open in-cell D_A derivation.

## Attack 5 — Q3a seat adjudication: **CONFIRMED (as scoped in the notes)**

Canon re-read at source (CANON.md:235ff and 577ff). C-2026-07-02-1: "the physical content is
the DIFFERENCE Δφ = φ(CMB fold) − φ(core) = ln(1101) (1+z = e^Δφ)". C-2026-08-06-2 keeps the
FORM and writes Δφ_cell = ln(T_emit/T_CMB) with T_CMB = 2.725 K MEASURED — i.e., measured by
the actual receiver. The static readout (native, unchanged) is 1+z = e^{φ(emit)−φ(obs)}.
Equating the OBSERVED ratio to e^{Δφ_cell} with emission at the fold forces φ(obs) = φ(core)
— one inference step, exactly as the notes tag it (DERIVED-from-canon-form). Within the
admitted classes {φ = φ_c} is precisely the flat segment [r_c, r*] where φ' = 0 IS forced
(CUT-3 + the flux identity). Precision note (no amendment needed — the notes already carry
it): the canon pins the seat's φ-VALUE, not φ' = 0 per se; "φ' = 0 forced" is
CLASS-CONDITIONAL. Under the free-core fork the floor point has φ' ≠ 0 while RETAINING the
equality form — which is exactly row 5's D3 entry. A φ' ≠ 0 receiver inside the admitted
classes is admissible ONLY by re-anchoring (observed span < cell span), which breaks the
canon equality — carried as the named Q3a cost. The adjudication is sound and honestly
double-carried; the WR-L seat does NOT satisfy the canon form without strain inside the
admitted classes.

## Additional checks

- The φ-shift absorbability used throughout (Step-2 C3 lemma) rechecked structurally: all
  Step-3 formulas depend on φ only through differences and e^{−2φ}-weighted combinations
  consistent with the Z-rescale; coefficients quoted in canon convention are so labeled.
- c_eff two-point ratio (1+z)^{−2}: trivial from dr/dt = ce^{−2φ}; holds.
- F-DATA rail: the derivation notes contain no fit, no χ², no data-file reference beyond
  citations of banked structural results. Clean as claimed (this reviewer also touched no data).

## Verdict

| Claim | Verdict |
|---|---|
| Core-seat quartic z = [ρ''(r_c)²e^{−6φ_c}/(3Zρ_c²)]d⁴ | **CONFIRMED** (exact, both methods) |
| ρ-pin at core is at-source (not transplanted) | **CONFIRMED** (fold JC doc line 37/106) |
| No-ρ-pin counterfactual | quadratic, but t¹ ≡ 0 ⇒ **NO strike flips** |
| Outer-closure blindness / glue equally struck | **CONFIRMED** (inner end verbatim shared) |
| Off-core pure dipole + half-sky blueshift | **CONFIRMED**; boost escape REFUTED (one-shell only) |
| C4 z(z+2) exact; C5 ρ=r fails; C6 ρ(0)>0 | **ALL CONFIRMED** (independent re-derivations) |
| Q3a canon receiver-pin | **CONFIRMED as scoped** (value-pin; φ'=0 class-conditional, already so stated) |

**S3-MIXED: SUSTAINED.** No cell of the Q3d table changes. No amendment required; one
precision note (Q3a value-vs-derivative pin) is already carried in the notes' own row 5.
Same-session-repo caveat: this review is independent in code and derivation method but ran
inside the same repository; the external bar for any hard bank still applies.
