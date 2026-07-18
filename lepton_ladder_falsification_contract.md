# Lepton Ladder Falsification Contract (Pre-Registered)

Status: PRE-REGISTRATION — committed BEFORE the test is run.
Created: 2026-06-10.
Companion test script (to be written and run only AFTER this commit):
`native_lepton_ladder_frozen_test.py`.
Results doc (after): `archive/pre_2026-07-01/lepton_ladder_test_results.md`.
Alters nothing existing; new files only.

## Purpose

Test the typed transfer ladder against the observed lepton mass hierarchy
with the model FROZEN before any number is compared. This extends the
existing rules in `native_lepton_ratio_falsification_contract.py`
(pre-registration, M2 inclusion, coefficient independence, anchor order,
failure allowed) with a concrete frozen model, a pre-declared candidate
list, exact tolerances, and look-elsewhere accounting per the methodology
of `dimension_ladder_null_audit.md`.

## Known-limitation disclosure (binding)

The required-coefficient pressure values are ALREADY published in this repo
(`native_lepton_ratio_diagnostic_lane.py`: C_M1 ≈ 0.9777, C_E1 ≈ 1.9312,
ratio ≈ 1.9753), so the candidate list below cannot be truly blind to them.
Consequences, binding on the interpretation:

1. A candidate match at the PERCENT level is UNINFORMATIVE — the
   dimension-ladder null audit measured small-rational/native-expression
   coverage at 16-23%, so %-level matches are expected by chance.
2. Only a match at or below the HIT tolerance (0.01%) carries any weight,
   and even then it must survive the look-elsewhere accounting in T3.
3. No candidate may be added, removed, or reweighted after the test runs.

## The frozen model (no adjustable elements)

```text
q       = 1/3
eta     = 1/18
eta/2   = 1/36
N       = 3
gamma_local  = 3 exp(-1/36)            (interface-local H1 transfer branch)
gamma_warped = 3 exp(-B/36),  B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2))
                                        (warped bulk-DtN branch)
depth(M1, mu-like)  = 5                 (candidate-counted: n_close = 3 + 2(d-1), d=2)
depth(E1, tau-like) = 7                 (candidate-counted: d=3)
M2 stance: conditionally demoted per Pbundle0 (the active lane's standing
           stance) — its omission is PART of the frozen model and a
           falsification surface, not adjustable.
anchor: m_e, applied only after dimensionless ratios.
```

Targets (observed, as recorded in the repo's diagnostic lane):

```text
m_mu/m_e  = 206.768282988
m_tau/m_e = 3477.22828002
m_tau/m_mu = (ratio of the above)
```

Caveat noted, not corrected for: the measured ratios include
electromagnetic self-energy; the geometric model targets the full physical
ratio.

## Pre-registered tests

### T1 — pure equal-coefficient ladder

Predictions `gamma^5` (mu/e), `gamma^7` (tau/e), `gamma^2` (tau/mu), for
BOTH branches (local and warped), no coefficients. Record signed fractional
deviations from the targets. No pass threshold — this is the baseline
falsification-pressure measurement of the bare frozen ladder.

### T2 — required-coefficient extraction (diagnostic only)

`C_M1_req = (m_mu/m_e)/gamma^5`, `C_E1_req = (m_tau/m_e)/gamma^7`, and the
ratio `C_E1_req/C_M1_req`, both branches. These are DIAGNOSTICS. They are
not evidence and must not be promoted.

### T3 — pre-declared native candidate match

The COMPLETE candidate lists (each with its native rationale; nothing may
be added after the run):

For `C_M1` (mu-branch coefficient):

```text
1            (bare ladder)
exp(-eta/2)  (one extra one-sided transfer action)
exp(+eta/2)  (one transfer-action credit)
exp(-eta)    (one full transfer action)
1 - eta/2  = 35/36   (linearized one-sided transfer)
1 + eta/2  = 37/36   (linearized credit)
W(T8)      = 2/3     (active-image action weight)
```

For `C_E1` (tau-branch coefficient):

```text
2                       (E1 relative-shape plane dimension)
2 exp(-eta/2)
2 exp(-eta)
2 (1 - eta/2) = 35/18
3/2                     (T8/A3 inverse-ish small sector ratio)
5/3                     (S5/A3 image-split ratio)
D2 = sqrt(6) I_{7/2}(6 sqrt(6)) / I_{5/2}(6 sqrt(6))
                        (warped ell=2 DtN eigenvalue; typed-branch
                         angular-sector candidate)
```

For the ratio `C_E1/C_M1`: all 49 pairwise quotients of the above lists
(computed mechanically, no hand-picking).

Tolerances (binding):

```text
HIT:   |fractional deviation| <= 1e-4   (0.01%)
LEAD:  |fractional deviation| <= 1e-3   (0.1%) — flagged, then must
       survive look-elsewhere; NOT bankable by itself
MISS:  anything worse
```

Look-elsewhere accounting (mandatory in the results): for each slot,
report K (number of candidates), the candidate-value range, and the
expected number of accidental hits/leads under a uniform-null over that
range. Any hit/lead must be reported WITH this expectation next to it.

### T4 — branch handling

Both transfer branches are tested identically. PRE-REGISTERED: no
averaging, no per-observable branch choice. If one branch fits one lepton
and the other branch the other, that is a MISS for both (branch selection
must come from a future derivation, not from the fit).

### T5 — verdict rules

```text
If T1 deviations are at the percent level or worse (expected) AND T3
produces no HIT: record the result as FALSIFICATION PRESSURE on the frozen
[depths 5/7 + gamma] model. The pressure numbers become the standing
constraint any future derivation of the branch coefficients must hit.

If T3 produces a LEAD that survives look-elsewhere: record as a lead for
the named candidate ONLY, with its rationale, for future derivation work.
Do not bank.

If T3 produces a HIT that survives look-elsewhere: still NOT a derivation —
record as a sharp target and require the variational derivation of that
specific coefficient before any grade rises.
```

Explicitly FORBIDDEN after this commit: changing depths (5/7), eta, N, or
gamma's form; adding/removing candidates; reinterpreting the M2 stance;
applying QED corrections selectively; averaging branches; reporting only
the better branch.

## Relation to existing rules

This contract instantiates rules 1-5 of
`native_lepton_ratio_falsification_contract.py` with concrete frozen
content. Rule 3 (coefficient independence) is honored in the negative: NO
derived coefficients exist yet (the Tier-D functional is open), so T3 tests
only the pre-declared candidate forms; the finite-cell diagnostics
(C_M1 = 1.1343, C_E1 = 2.1039) are NOT candidates — they are unexplained
numerics and may only be compared as additional context, clearly labeled.
