# M3b Phase-2 — THE FREEZE: in-sample ruler ℓ + the frozen BOSS prediction

Prereg `PREREGISTRATION.md` (commit af9fa75d, binding). Machinery: `measure_ell.py`,
output `run_output.txt`. Banked DESI + SNe ONLY — **ZERO BOSS contact**. This document is
the frozen out-of-sample prediction; it is committed BEFORE any BOSS file is touched (F-RETRO:
the commit hash is the timestamp). IN-SAMPLE, disclosed as such — NO fit to BOSS.

## Premise stamps (all travel)
- **SNe-anchor (F-ANCHOR):** every absolute Mpc rides M_B = −19.253 ± 0.027 (SH0ES ladder,
  mode B). ℓ in Mpc is anchor-conditional; ℓ/R_w is anchor-free.
- **P1-conditional:** r(z) = R_w[1 − (1+z)^(−2/n)] with the P1 profile, n = 1/inv_n,
  inv_n = 0.947 [0.9284, 0.9658], X_eff = 2086.0 [2059.1, 2113.2] Mpc → n = 1.05597,
  **R_w = 2202.7 Mpc [2132.0, 2276.2]**.
- **SKY-ROBUST-only:** ℓ fit to the audit-graded (2d9933d1, CONSOLIDATED) SKY-ROBUST shells;
  SELECTION-SUSPECT + B6-artifact excluded. PRIMARY = 3 SKY-ROBUST; VARIANT = + 2 INCONCLUSIVE.
- **Center error DERIVED, not stored:** the DESI JSON stores σ_b = bump *width*, not a center
  error. Used σ_center = σ_b / √Δχ² (standard peak-localization: positional error = width /
  detection-S/N). Stated so a re-grader can re-weight.
- **Covariance caveat inherited:** diagonal jackknife (M2 condition) on every DESI σ.

## 1. The ruler ℓ — set × weight-variant table

| set | variant | ℓ (Mpc) | ℓ interval (fit+anchor) | χ²/dof = threading | ℓ/R_w |
|---|---|---|---|---|---|
| PRIMARY (3 SKY-ROBUST) | sys   | **58.34** | [57.01, 59.70] | **288.4/2 = 144.2** | 0.02649 |
| PRIMARY (3 SKY-ROBUST) | nosys | 58.51 | [57.17, 59.87] | 276.2/2 = 138.1 | 0.02656 |
| VARIANT (+2 INCONCL.)  | sys   | 59.85 | [58.46, 61.28] | 296.4/4 = 74.1 | 0.02717 |
| VARIANT (+2 INCONCL.)  | nosys | 59.97 | [58.57, 61.40] | 283.3/4 = 70.8 | 0.02722 |

ℓ is **weight-variant STABLE to ~0.3%** (sys↔nosys), consistent with the M3 finding that the
strong-shell cluster is not an imaging-weight artifact. ℓ ≈ 58–60 Mpc.

## 2. ℓ/R_w — the D3 dimensionless target (anchor-free)

**ℓ/R_w = 0.0265 [0.0251, 0.0280]** (PRIMARY sys) — ℓ is **2.65% of the wall R_w**. This is the
dimensionless number the discreteness program would have to predict; it is a MEASUREMENT (D3
stands: no native amount). ℓ = 58.34 Mpc = 0.0265 R_w.

## 3. Threading quality = the drift tension, quantified (honest, not hidden)

**A single global ℓ does NOT thread the shells — χ²/dof = 144 (PRIMARY).** The magnitudes are the
right SCALE (ℓ ~ 58–60 Mpc; the 2.3–2.4° cluster alone sits near the ~70 Mpc P1 curve — the QSO
0.95–1.10 shell at 1.39° pulls the weighted ℓ down to ~58), but the DIRECTION is wrong:

- **LRG same-tracer baseline z 0.725 → 1.025:** the ruler predicts θ FALLS 2.357° → 2.059°
  (−1.48 log-bins, Δlnθ=0.0914). Observed θ RISES 2.365° → 2.438° (+0.33 bins). **Mismatch =
  +1.81 bins, opposite sign = anti-drift** — reproduces the audit's "~1–1.5 bins opposite drift"
  (REAL; no selection channel explains it; thread centers stable — AUDIT CONSOLIDATED).
- **Same-z tracer split at z=1.025:** LRG θ = 2.438° vs QSO θ = 1.392° → **1.75× (+6.13 bins) at
  ONE redshift.** A single ruler ℓ = θ·r(z) mathematically forbids two θ at one z; this is the
  dominant contribution to χ². The 2.3–2.4° thread is an LRG-cluster feature the QSO shell does
  not share at its own z.

VERDICT: ℓ is a MAGNITUDE, not a threaded ruler. The in-sample thread is scale-suggestive,
direction-inconsistent. Reported at equal temperature (F-STEER).

## 4. THE FROZEN OUT-OF-SAMPLE PREDICTION (committed before BOSS contact)

θ_BAO(z) = ℓ_PRIMARY(sys) / r(z), ℓ = 58.34 Mpc [57.01, 59.70], evaluated at BOSS DR12 coverage.
BOSS's actual shell binning is set in Phase 3 by density (Δz per cap, floor 5e4 weighted); this
table is θ(z) = ℓ/r(z) at representative z — the frozen numbers to test.

| sample | z | θ_pred (deg) | interval (deg) |
|---|---|---|---|
| LOWZ  | 0.20 | 5.197 | [4.997, 5.405] |
| LOWZ  | 0.25 | 4.403 | [4.231, 4.582] |
| LOWZ  | 0.30 | 3.875 | [3.722, 4.035] |
| LOWZ  | 0.35 | 3.500 | [3.359, 3.647] |
| LOWZ  | 0.40 | 3.220 | [3.089, 3.357] |
| CMASS | 0.45 | 3.004 | [2.880, 3.133] |
| CMASS | 0.50 | 2.831 | [2.713, 2.954] |
| CMASS | 0.55 | 2.691 | [2.577, 2.809] |
| CMASS | 0.60 | 2.575 | [2.465, 2.689] |
| CMASS | 0.65 | 2.477 | [2.371, 2.588] |

Interval = ℓ interval propagated with the r(z) inv_n/X_eff corners (anchor band). The predicted
θ FALLS monotonically with z (the ruler's geometric behavior). Whether BOSS reproduces DESI's
observed ANTI-drift is itself part of the test (§6) and is reported either way.

## 5. Frozen pass/fail (from PREREGISTRATION §3, cited not re-derived)
- **PASS (strong):** BOSS feature at global trials-corr p < 0.01 AND frozen ℓ predicts θ_BAO
  within jackknife errors across ≥ 2 BOSS shells.
- **PARTIAL:** feature at ℓ′ ≠ frozen ℓ (beyond errors) → ℓ not universal; report neutrally.
- **NULL (first-class):** no feature at threshold → O-D lives; the DESI thread stands alone.

## 6. Per-origin BOSS expectations (from the closed D0 matrix — cited, not re-derived)
- **O-D (mundane / decorrelated systematics):** NO feature in BOSS — the cheapest kill.
- **O-A / O-C / O-E (real angular feature):** a feature threading the frozen ℓ, tracer-universal
  (BOSS galaxies share DESI's ℓ), carrying **O-A's anti-drift behavior** (§3) if that origin.
- **Feature at a DIFFERENT ℓ:** ℓ NOT universal → frame-map / viewing-artifact strain.

Status: **verified-LEAD ceiling** (in-sample, disclosed). Blind results-verifier owed before
banking (re-run the fit; audit F-RETRO timeline against git). This closes the freeze; the main
loop commits, THEN Phase 3 opens BOSS.
