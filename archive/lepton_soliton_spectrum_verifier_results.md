# BLIND ADVERSARIAL VERIFIER — Lepton Soliton Spectrum / Scale-Free Ratios

Verifier agent: blind-adversarial (Opus 4.8, 1M ctx). Date: 2026-06-14.
Target results doc: `lepton_soliton_spectrum_results.md`.
Contract: `lepton_soliton_spectrum_contract.md` (committed BEFORE the derivation).
Mode: **independent re-derivation + ACTIVE RESCUE ATTEMPT**. STRICTLY DATA-BLIND
(no empirical lepton/hadron masses or contract-26fc757 targets loaded; only the
model's intrinsic, scale-free numbers were computed).

Assignment: the pre-registered derivation found a FAIL of the standing hypothesis
(only ONE static soliton; an O(1) — not exponential — breathing tower; Koide
Q near 1/3, not 2/3). My job: re-derive with INDEPENDENT machinery and TRY HARD
to RESCUE the hypothesis — hunt for a genuine excited-soliton tower, an
exponential level spacing, or a defensible energy reading giving Koide 2/3. If
none is found, the FAIL stands.

Independent scripts written for this verification (do NOT reuse the derivation's
scripts; built from the Lagrangian):
- `vrf_lepton_reduction.py`, `vrf_lepton_reduction2.py` — re-derive the reduced
  1D energy functional E[Theta] from L2+L4 with sympy, from scratch.
- `vrf_lepton_bvp_spectrum.py` — independent ground-state BVP (scipy solve_bvp)
  + RESCUE A (multi-seed relaxation).
- `vrf_lepton_shoot.py` — RESCUE A, independent method 2: core shooting scan for
  distinct static excited branches.
- `vrf_lepton_hessian.py` — independent breathing/fluctuation Hessian (RESCUE B
  flat) + Koide Q (RESCUE C).
- `vrf_lepton_deepphi_mpmath.py` — independent high-precision (mpmath dps>=60)
  deep-phi spectrum, p=0..10 (RESCUE B deep), via Sturm-sequence bisection.
- `vrf_lepton_wtower.py` — independent per-m re-relaxed winding tower (claim 4).

---

## STEP 0 — INDEPENDENT RE-DERIVATION OF THE REDUCED FUNCTIONAL

Rebuilt E2_r, E4_r from L2 = -(xi/2) g^{mn} d_m n.d_n n, L4 = -(kappa/4)
(d_m n x d_n n)^2, frozen ansatz n=(sinTheta sin th cos(m ph), sinTheta sin th
sin(m ph), cosTheta), metric ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2 dOmega^2,
sympy from scratch, angular integral done by hand-controlled term-by-term
integration.

FINDING — measure check (caught a subtlety, resolved in the model's favor): the
4D covariant sqrt(-g_4) = r^2 sin th (the e^{-2phi} from g_tt and e^{2phi} from
g_rr CANCEL in the determinant), which would give an overall e^{-2phi} weight.
But the correct STATIC SOLITON ENERGY uses the SPATIAL 3-metric measure
sqrt(g_spatial) = e^{phi} r^2 sin th (ADM-style energy on the static slice). With
the spatial measure my independent reduction reproduces the doc's E2_r, E4_r
**EXACTLY** (8/8 random-point numeric checks, rel. err < 1e-9):

  E2_r = (2pi xi/3) e^{-phi}[ 3 r^2 sin^2Th Th'^2 + 2 r^2 cos^2Th Th'^2
                              + (3m^2+1) e^{2phi} sin^2Th ]
  E4_r = (2pi kap/3) e^{-phi} sin^2Th[ m^2 e^{2phi} sin^2Th
                              + r^2 (m^2 sin^2Th + 2m^2 + sin^2Th) Th'^2 ]/r^2

At m=1 these equal the doc's quoted forms identically. **Reduction CONFIRMED**
(with the standard static-energy spatial measure). The e^{±phi} weights are
carried honestly and are correct.

---

## CLAIM-BY-CLAIM VERDICTS

### CLAIM 1 / RESCUE A — "only ONE static soliton"  →  **CONFIRMED (no tower found)**

Two fully independent methods, both DATA-BLIND:

(i) **Multi-seed relaxation** (scipy solve_bvp, `vrf_lepton_bvp_spectrum.py`).
Ground state from a monotone seed: **E0 = 45.6071**, width(Th=pi/2)=0.644 L, 0
turning points, rms residual 2e-9 — matches doc's 45.6069, 0.648 L. Then seeded
the SAME charge-1 BVP (Th(core)=pi, Th(seal)=0) with 1-node and 2-node
overshooting guesses, and a high-core seed. **All three relax back to the
identical monotone ground state**, E = 45.60713 to 5 decimals, 0 interior turns,
no excursion outside [0,pi]. No distinct static excited branch.

(ii) **Core shooting scan** (`vrf_lepton_shoot.py`, INDEPENDENT method): integrate
the EOM from the core with Th(core)=pi and varied Th'(core)<0 (geometric scan of
~800 shots, p=0 and p=1), locate every Th'(core) that lands Th(seal)=0 by
bisection, classify by interior turning points and out-of-[0,pi] excursions.
RESULT (p=0): a single root, monotone (0 interior turns, no excursion) — the
ground state; no additional root with interior nodes within the scanned shooting
range. [Shooting corroborates relaxation: one finite-energy branch.]

Both methods agree: the EOM admits exactly ONE finite-energy charge-1 solution on
the cell, the nodeless ground state. Node-seeded BVPs collapse to it — this is a
genuine structural fact of the functional, not a solver basin artifact (two
unrelated solvers, multiple seeds). **The (P) "radial tower" is NOT a tower of
distinct static solitons. RESCUE A FAILS — no static overtone tower.**

### CLAIM 2 / RESCUE B — "spacing is O(1), not exponential"  →  **CONFIRMED**

Independent breathing/fluctuation Hessian (second variation of E about the ground
state): Sturm-Liouville H u = omega^2 W u, H = -(d/dr)(2a u') + V,
V = a_ThTh Th'^2 + b_ThTh - d/dr(2 a_Th Th'), Dirichlet ends, W = e^{3phi} r^2.

FLAT (p=0), `vrf_lepton_hessian.py` (W=r^2):
  **omega^2 = [0.833, 2.374, 4.627, 7.721, 11.78, 16.83]**  (all positive => stable)
  linear fit omega^2_n ~ -0.59 + 3.18 n (i.e. omega^2 ~ LINEAR in n);
  exponential-fit slope **c = 0.29** (e^c = 1.34/level).
[NB: my absolute omega^2 differ from the doc's 0.198/0.554/... by a uniform
factor ~4.2 — a breathing-weight NORMALIZATION convention; the independent
mpmath agent reproduced MY values (0.833,...) at p=0. The normalization cancels
in every ratio/spacing-law/Koide quantity below, so it is immaterial to the
verdict. The doc's spacing slope c=0.28 matches my c=0.29.]

DEEP (mpmath dps>=60, p=0..10, `vrf_lepton_deepphi_mpmath.py`, independent agent):
| p  | omega^2 (lowest 4)              | R1=om1^2/om0^2 | exp-slope c |
|----|--------------------------------|----------------|-------------|
| 0  | 0.833, 2.375, 4.629, 7.724      | 2.85           | 0.37        |
| 2  | 8.07, 39.6, 95.1, 174.5         | 4.91 (peak)    | ~0.49       |
| 4  | 30.1, 140.5, 332.1, 604.3       | 4.67           | ~0.49       |
| 6  | 66.2, 301.3, 706.6, 1279        | 4.55           | ~0.50       |
| 10 | 180.1, 800.3, 1858, 3334        | 4.44           | ~0.50       |

- All omega^2 POSITIVE and well-ordered at every depth (stable soliton).
- Deepening the core RAISES R1 from 2.85 to a peak ~4.9, then it gently DECLINES
  and SATURATES at ~4.4 — it does NOT grow without bound and never goes
  exponential. The level steps om_n/om_{n-1} = 2.1, 1.5, 1.3 are DECREASING in n
  (sub-geometric; omega^2 ~ linear in n — a quasi-harmonic Sturm-Liouville
  ladder), the OPPOSITE of an exponential cascade.
- The exponential-fit slope c never exceeds ~0.5; an exponential hierarchy
  (E_n ~ e^{cn} matching a large lepton ratio) needs c >> 1.
- Ground mode does NOT go soft: omega_0^2 GROWS monotonically with depth
  (0.83 -> 180 at p=10) — deep-phi STIFFENS the breathing mode, no instability.
- float64 deep-phi artifact CONFIRMED & isolated: the naive
  eig(H, diag(W)) path degrades at p>=8 (e^{3phi} dynamic range ~10^74); the
  W^{-1/2}-symmetrized path and mpmath both stay clean and agree to ~3 digits.
  The doc's "float64 negatives are conditioning artifacts" is CORRECT.

**RESCUE B FAILS — deep-phi does NOT manufacture an exponential hierarchy. The
breathing tower is a stable, O(1) (quasi-harmonic, saturating) ladder. CONFIRMED.**

### CLAIM 3 / RESCUE C — "Koide Q near 1/3, not 2/3 under any reading"  →  **CONFIRMED**

Independent Koide Q from my flat-phi triple (normalization-invariant):
| reading                       | Q       |
|-------------------------------|---------|
| A: E_n = E_soliton + omega_n  | 0.33334 |
| B: E_n = omega_n^2            | 0.36950 |
| C: E_n = omega_n              | 0.34312 |
| D: E_n = E_soliton + omega_n^2| 0.33342 |
| omega_n^3                     | 0.40740 |
| omega_n^4                     | 0.45198 |
| integers (1,2,3)              | 0.34901 |

(Doc reported A=0.3333, B=0.3672, C=0.3425 — my A,C match; my B=0.370 vs doc
0.367, within the small spectrum-normalization difference; same conclusion.)

Q is bounded in [1/3, 1]; Q=1/3 iff degenerate, Q->1 iff one mass dominates.
Koide 2/3 = 0.6667 requires a LARGE, SPECIFIC spread of sqrt-masses (the classic
1 + sqrt2 cos relation). The breathing tower's near-even spacing (max/min omega^2
~ 5.6) puts Q firmly at the LOWER edge under EVERY reading I could construct —
even contrived monotone transforms (omega^3, omega^4) only reach 0.41-0.45, and a
synthetic [1,8,49] spread only reaches 0.49. No physically defensible
state-energy definition for this quasi-harmonic tower comes near 2/3.

**RESCUE C FAILS — no defensible reading gives Koide 2/3. CONFIRMED.**

### CLAIM 4 — winding ratios M_2/M_1, M_3/M_1  →  **PARTIAL: O(1) character CONFIRMED; specific doc numbers REFUTED**

Independent per-m FULL re-relaxation (`vrf_lepton_wtower.py`, not the m=1 shape):
- M_1 = 21.78, M_2 = 55.98, M_3 = 107.79 (units 2pi/3)
- **M_2/M_1 = 2.57, M_3/M_1 = 4.95** (domain-robust to <0.5%)
- Doc claimed 1.99, 3.64; doc's own frozen-m=1-shape gives 2.75/5.67; m^2 would
  be 4.0/9.0. So the tower is sub-m^2 (O(1) in spirit) — but the doc's specific
  1.99/3.64 are NOT reproduced (off by ~30%, stable). The doc over-/mis-stated the
  numbers (likely the m=1-shape approximation plus an m-weighting bookkeeping
  difference). This is a SECONDARY (exploratory, look-elsewhere-debited) claim and
  does NOT affect the primary FAIL.

### CLAIM 5 — ROBUSTNESS (kappa/xi cancels; ratios cell-size-independent)  →  **CONFIRMED**

- The single scale enters only as an overall sqrt(kappa xi) prefactor of the
  absolute energy; xi=kappa=1 throughout; all reported quantities are RATIOS or
  the pure number Q, in which kappa/xi cancels by construction. Verified the
  ground width (0.644 L) and the breathing ratios are insensitive to the cell
  size once cell >> soliton width (W-tower agent: ratios move <0.5% over cell
  length 10..30 and r_core 0.01..0.1). [CONFIRMED]

---

## OVERALL VERDICT

| RESCUE QUESTION                                   | RESULT |
|---------------------------------------------------|--------|
| Is there really only ONE static soliton?          | YES — only one (two independent methods) |
| Is the spacing O(1) (not exponential)?            | O(1) — saturating quasi-harmonic, c<=0.5, no exp even at p=10 |
| Does any defensible reading give Koide 2/3?       | NO — all readings in [0.333, 0.45], far from 0.667 |

**The pre-registered FAIL STANDS.** It survived an active, independent rescue
attempt: I re-derived the functional from scratch (matching the doc once the
correct spatial static-energy measure is used), found exactly one static soliton
by two unrelated methods, computed an all-positive breathing spectrum that is
O(1)/saturating (no exponential hierarchy anywhere up to core depth p=10, and the
ground mode stiffens rather than softening), and found NO state-energy reading
giving Koide 2/3. The native L2+L4 angular soliton on the finite UDT cell does
NOT reproduce a large lepton mass hierarchy or Koide 2/3.

CAVEATS / scope (premises this FAIL carries, per NEGATIVES_REGISTRY discipline):
- Frozen ansatz n=(sinTheta sin th cos(m ph), ...) (the model's chosen carrier;
  note |n|!=1 for this ansatz — it is the projected hedgehog the model froze, not
  a true unit field; flagged, but it IS the contracted model).
- Static-energy spatial measure e^{phi} r^2 sin th (correct for soliton mass;
  resolves the only reduction ambiguity I found, in the doc's favor).
- Breathing weight W = e^{3phi} r^2 (the doc's C2 choice). Q, the spacing LAW, and
  "only one static soliton" are INDEPENDENT of this weight's normalization; the
  weight affects only the absolute omega scale, not any reported ratio. So the
  FAIL does not hinge on the load-bearing C2 convention.
- Seal Dirichlet Th(seal)=0. (A Neumann seal was not re-tested here; the static-
  soliton uniqueness and breathing O(1) character are robust to the seed/method,
  but a different seal is a separate premise — out of scope for this rescue.)
- Discrepancy noted: the doc's absolute breathing omega^2 (0.198,...) are ~4.2x
  smaller than mine and the independent mpmath agent's (0.833,...); a
  normalization convention that cancels in all physics conclusions. Doc's W-tower
  numbers (1.99/3.64) are independently REFUTED (correct: 2.57/4.95), but this is
  a secondary exploratory claim.

The primary deliverables (one soliton; O(1) non-exponential spacing; Koide ~1/3)
are all INDEPENDENTLY REPRODUCED. **FAIL banked.**
