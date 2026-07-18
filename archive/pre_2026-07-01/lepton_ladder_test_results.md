> **SUPERSEDED (2026-07-06 macro-spine pass) — the RETIRED 2026-06-10 typed-transfer / q=1/3-import ladder.**
> Rides an imported typed-transfer ladder (q=1/3, η=1/18, Bessel-B, fixed depths) from the "algebraic objects can be
> imports" era — NOT the native D2b depth ladder (cascade_stage*/ladder_*). Self-labeled "not canonical"; its verdict
> is falsification pressure (126/126 miss). No live claim. See pre_native_era_census.md.

# Lepton Ladder Test Results

Status: working audit, not canonical.
Created: 2026-06-10.
Pre-registered via `lepton_ladder_falsification_contract.md`, committed at
git hash `26fc757` BEFORE this test ran. Script:
`native_lepton_ladder_frozen_test.py` (all numbers below reproduce from it).
Alters nothing existing; new files only.

## Purpose

Run the pre-registered falsification test of the typed transfer ladder
against the observed lepton mass hierarchy with the model frozen before
any number was compared. The contract froze the model, both transfer
branches, the depths, the complete candidate lists, the tolerances
(HIT ≤ 1e-4, LEAD ≤ 1e-3, fractional), and the look-elsewhere accounting.
Nothing was added, removed, or reweighted after the run.

## The frozen model (as pre-registered)

```text
q = 1/3, eta = 1/18, eta/2 = 1/36, N = 3
gamma_local  = 3 exp(-1/36)  = 2.91781343135   (matches repo digits)
gamma_warped = 3 exp(-B/36)  = 2.94282464475
  B = I_{7/2}(6 sqrt 2)/I_{5/2}(6 sqrt 2) = 0.692726581294
  (mpmath at 40 digits, cross-checked against scipy.special.iv to <1e-12)
depth(M1, mu-like) = 5, depth(E1, tau-like) = 7
M2 conditionally demoted per Pbundle0 (frozen, not adjustable)
anchor m_e applied only after dimensionless ratios
targets: m_mu/m_e = 206.768282988, m_tau/m_e = 3477.22828002,
         m_tau/m_mu = 16.8170293324
```

Known-limitation disclosure (binding, from the contract): the required
coefficients were already published in this repo, so the candidate list
was not blind to them; only HIT-level matches could have carried weight.

## Findings

### T1 — pure equal-coefficient ladder (baseline pressure)

Signed fractional deviation = (predicted − observed)/observed:

| branch | gamma^5 vs mu/e | gamma^7 vs tau/e | gamma^2 vs tau/mu |
| --- | --- | --- | --- |
| local  | +0.0228 (+2.3%) | −0.4822 (−48.2%) | −0.4937 (−49.4%) |
| warped | +0.0674 (+6.7%) | −0.4503 (−45.0%) | −0.4850 (−48.5%) |

The bare frozen ladder misses the muon at the few-percent level and the
tau at the ~50% level, in both branches. Per T1 this is the baseline
falsification-pressure measurement; no pass threshold applied.

### T2 — required coefficients (DIAGNOSTIC ONLY, not evidence)

| branch | C_M1_req | C_E1_req | C_E1_req/C_M1_req |
| --- | --- | --- | --- |
| local  | 0.977679087638 | 1.93121474779 | 1.97530536575 |
| warped | 0.936832609588 | 1.81920864981 | 1.94187161205 |

### T3 — pre-declared candidate match: NO HIT, NO LEAD, anywhere

All 7 C_M1 candidates, all 7 C_E1 candidates, and all 49 mechanical
pairwise quotients were classified against the required values for BOTH
branches (126 classifications total). **Every single one is a MISS.**
Best approaches per slot (all far outside even the LEAD tolerance of
1e-3):

| slot | branch | best candidate | signed frac dev |
| --- | --- | --- | --- |
| C_M1 | local | exp(−eta/2) | −5.19e-3 |
| C_M1 | warped | exp(−eta) | +9.74e-3 |
| C_E1 | local | 2(1−eta/2) = 35/18 | +6.85e-3 |
| C_E1 | warped | 2 exp(−eta) | +4.00e-2 |
| ratio | local | D2/1 | +5.31e-3 |
| ratio | warped | (35/18)/1 | +1.32e-3 |

The nearest miss in the entire test is the warped-branch ratio quotient
(35/18)/1 at +1.32e-3 — outside the LEAD threshold by a factor of 1.3,
and in the wrong branch pairing to mean anything (the warped branch's
individual coefficients miss at the 1–10% level). It is recorded here
for calibration only and is NOT a lead.

Look-elsewhere accounting (mandatory; uniform null over the candidate
value range, E = K·2·tol·|required|/range — crude: the range is estimated
from the candidates themselves and the candidates cluster, so this
UNDERSTATES the accidental expectation near the clusters;
order-of-magnitude only):

| slot | K | range | E[accidental HITs] | E[accidental LEADs] |
| --- | --- | --- | --- | --- |
| C_M1 (local/warped)  | 7  | [0.667, 1.028], width 0.362 | 0.0038 / 0.0036 | 0.038 / 0.036 |
| C_E1 (local/warped)  | 7  | [1.5, 2.0], width 0.5       | 0.0054 / 0.0051 | 0.054 / 0.051 |
| ratio (local/warped) | 49 | [1.459, 3.0], width 1.541   | 0.0126 / 0.0124 | 0.126 / 0.124 |

Observed hits/leads (0 everywhere) are consistent with these null
expectations; the test had real discriminating power at the HIT level
(accidental HIT expectation ≤ ~1% per slot) and the model did not use it.

### T4 — branch handling

Confirmed mechanically: no branch averaging anywhere; no per-observable
branch choice; both branches run identically and reported in full. The
cross-branch split rule (one branch fitting one lepton, the other branch
the other → MISS for both) was not triggered — there were no hits or
leads in either branch to split.

### Context only — finite-cell diagnostics (NOT candidates)

Per the contract's final paragraph, compared as context, clearly labeled,
excluded from T3 and from the look-elsewhere counts:

| diagnostic | vs local required | vs warped required |
| --- | --- | --- |
| C_M1 = 1.1343262 | +16.0% | +21.1% |
| C_E1 = 2.10394   | +8.9%  | +15.7% |

The unexplained finite-cell numerics are nowhere near the required
coefficients either. They explain nothing here.

## Verdicts (per the contract's T5 rules)

1. **FALSIFICATION PRESSURE on the frozen [depths 5/7 + gamma] model.**
   T1 deviations are at the percent level or worse in every slot of both
   branches, and T3 produced no HIT and no LEAD among the 126
   pre-declared classifications. This is the contract's first verdict
   branch, exactly as pre-registered.
2. **No lead exists to bank or even to flag.** The nearest miss
   (warped-ratio (35/18)/1 at +1.32e-3) fails the LEAD tolerance; under
   the contract it has no status. Had it landed inside, the look-elsewhere
   expectation for that slot (~0.12 accidental leads) and the contract's
   "do not bank" rule would still have applied.
3. **The pre-declared native vocabulary, at one multiplicative
   coefficient per branch, cannot absorb the lepton hierarchy at the
   frozen depths.** The required corrections off the bare values are
   −2.23% (C_M1 vs 1) and −3.44% (C_E1 vs 2) in the local branch, but
   the declared vocabulary moves in steps of order eta/2 ≈ 2.78%, so its
   nearest members land −0.52% (exp(−eta/2)) and +0.69% (35/18) away —
   50–70x outside the HIT tolerance. The residuals sit between the rungs
   of the eta-ladder.
4. Explicitly NOT done, per the contract: no depth change, no eta/N/gamma
   change, no candidate added or removed, no M2 reinterpretation, no
   selective QED correction, no branch averaging, no better-branch-only
   reporting.

## Standing constraint

Any future derivation of the branch coefficients — the open Tier-D
functional or any successor — must produce, with NO access to lepton
data:

```text
local branch:  C_M1 = 0.977679087638
               C_E1 = 1.93121474779
               C_E1/C_M1 = 1.97530536575
warped branch: C_M1 = 0.936832609588
               C_E1 = 1.81920864981
               C_E1/C_M1 = 1.94187161205
```

to within 1e-4 fractional (the HIT tolerance) for the branch the
derivation itself selects — branch selection must also come from the
derivation, never from the fit (T4 rule). A derivation that instead
predicts different depths or a different gamma form is a NEW model and
requires a new pre-registered contract; it may not retroactively claim
this test. Until such a derivation exists, the frozen [depths 5/7 +
gamma, single coefficient per branch] lepton ladder stands recorded as
under falsification pressure, and these six numbers are the wall it
failed to climb.
