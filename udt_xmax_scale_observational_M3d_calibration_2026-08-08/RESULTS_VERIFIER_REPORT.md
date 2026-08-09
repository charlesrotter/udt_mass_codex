# M3d — BLIND RESULTS-VERIFIER REPORT (Leg A + Leg B)

Verifier: fresh-context blind pass, 2026-08-09, branch grok. No commit. Primary brief =
the F-FAIR-MOCK adjudication. All Leg A metrics recomputed from raw checkpoint jsons;
Leg B arithmetic re-derived; DES Y6 anchor web-confirmed.

## HEADLINE — the fairness-direction call
The split metric has TWO gates: ratio = max/min(θ) ≥ 1.75 (center SEPARATION) AND
σ = |θL−θQ|/hypot(σL,σQ) ≥ 3.8 (significance). The too-clean bias cuts them OPPOSITE ways:
- **ratio gate:** too-clean → centers recovered precisely (M1 scatter ~4.6%) → under-scatter
  → HARDER to reach 1.75. This gate BINDS: mock ratio caps at 1.14 (vi)/1.23 (vii) vs 1.75.
- **σ gate:** too-clean → smaller errors → EASIER to clear 3.8σ (the reviewer's point).
Net: the mock's binding failure is the center-SEPARATION, which the too-clean bias suppresses,
so 0/30 IS genuinely confounded → **CAL-OBSTRUCTED(fairness) is the honest verdict, not a dodge.**
The "a clean mock that still can't fake it is a stronger re-firm" intuition is valid ONLY on the
σ axis, not the binding ratio axis, so it does NOT overturn CAL-OBSTRUCTED. Quantitatively: faking
ratio 1.75 needs ~30% center displacement (~6σ of mock scatter); broadband inflates errors ~2–3×
(from 4.9–10.4× dchi2 → sqrt), taking center scatter ~4.6%→~10–14%, close to but short of the
~15–20% needed. So 0/30 leans WEAKLY toward re-firm but is not dischargeable.
**Amendment owed:** Leg A phrases the bias as cleanly "biases the rate LOW" — it is two-directional
(ratio-low, σ-high); the low direction binds. Otherwise the reasoning holds.

## Item verdicts
1. **F-FAIR-MOCK (primary) — SUSTAINED (amend wording).** (a) Amplitude match REAL: mock median
   A_b40 0.0054/0.0083/0.0228 vs real 0.0069/0.0087/0.0153 — matched by construction (1.00 shell
   over-amp because f_pair=median 0.318 > its solved 0.191; disclosed). (b) "Too clean" REAL:
   mock median dchi2 69.2/121.1/212.1/183.6 vs real 13.99/22.82/43.37/17.59 → ratios
   4.95/5.31/4.89/10.44 — reproduced EXACTLY; real values trace byte-exact to banked M3 nosys
   `bao_results_nosys.json`. (c) Direction: see headline.
2. **Metrics — SUSTAINED (exact reproduction).** M1 vi mean|bias_ln|=0.0650, median_scatter=0.0456;
   M2 vi antidrift 0.6667 (mean +0.050, sd 0.856) → DOWNGRADE; vii 0.0667; M3 0/15+0/15=0/30,
   binom 95% upper 0.09503; M4 implied-ℓ 47.0–76.0 Mpc, 0% outside 40–80. Every number matches
   legA_metrics.json. **M2 DOWNGRADE direction is correct & conservative** (cleaner mock recovers a
   gentle drift BETTER → the true false-positive rate ≥ 0.67; a fair noisier mock only raises it).
   **M4 CAL-OBSTRUCTED correct** (clean→too-tight; can't exclude noise reaching 4–212).
3. **Threshold application — SUSTAINED, no bending.** Mechanical rule applied to point estimates
   (M3→RE-FIRMS, M2→DOWNGRADE) exactly per prereg. The CAL-OBSTRUCTED override on M3/M4 is
   LEGITIMATE per prereg §0/§5 fairness primacy — and note it BLOCKS a verdict (RE-FIRMS) that would
   FAVOR the anomaly: correct hypothesis-discipline direction, the opposite of a dodge. Doubly
   justified on M3: N=30 cannot resolve below p≈0.033, so p<0.01 is unreachable regardless.
4. **Leg B — SUSTAINED.** Pulls −3.73/−0.17/−1.21/−5.64/−0.66, global χ²=47.6/5, LRG-only 15.4/3,
   excl-QSO 15.8/4 all reproduce EXACTLY; DES conversions (Y6 2.937, Y3 3.028, Y1 2.945) correct;
   **DES Y6 anchor web-confirmed: D_M/r_d=19.51±0.41 at z=0.85** (arXiv:2402.10696). CAL-MIXED(legB)
   fairly stated: z≈1 LRG match (−1.2σ) AND the global miss (p~1e-9) both carried; the −5.6σ QSO
   point and its wide-bin/no-comparator caveats honestly disclosed.
5. **F-RETRO / honesty — CLEAN.** Prereg frozen (962bd0c6) before any mock; the broadband-clustered
   fair re-test correctly DEFERRED (running it post-0/30 would be F-RETRO); no observational tuning;
   equivalence_check byte-exact (dw=dcov=0). **One deviation flagged:** prereg §1 said "N_mock=25
   MINIMUM"; ran 15 (n_real_decision.json, 6.13h>6h budget). Transparently disclosed but IS below the
   frozen minimum — immaterial to verdicts (even 2×25=50→95% upper 0.058>0.01 can't discharge M3).

## FINAL VERDICT: SUSTAINED-AMENDED
CAL-MIXED stands. Amendments: (1) state the fairness bias as two-directional (ratio-low binds,
σ-high) and note 0/30 leans WEAKLY re-firm rather than being fully uninformative; (2) flag the
N=15<25-minimum prereg deviation explicitly (harmless to conclusions). No metric, arithmetic, or
provenance error found; the too-clean diagnosis and the CAL-OBSTRUCTED(fairness) calls are correct.
