# Tier-D Round 3 — Pre-Registered Falsification Contract

Status: pre-registration, committed BEFORE evaluation. Created:
2026-06-11. Companion to sphi0_derivation_panel_results.md (the panel
record). No retuning after evaluation; no candidate additions; branch
assignment fixed below, from the derivations, not from fit.

## What is being tested

The S_phi0 derivation panel (2026-06-10/11) produced a small set of
CONDITIONAL coefficient readings — the only coefficient forms any route
licensed after two blind adversarial verifier passes. They were derived
data-blind (no lepton input; disclosures on record). This contract
freezes them for evaluation against the six banked wall numbers of
lepton_ladder_test_results.md.

Exclusions, fixed now: route C's Gaussian-determinant forms are NOT
evaluable (free normalization N and flat-direction measure — no
parameter-free number; verifier-endorsed strict verdict). Route B's
C_E1 = exp(eta) recount and all forms downstream of it are REFUTED
(verifier V1 claim 4, V2 claim 3) and excluded. No other forms exist in
the panel record.

## Frozen candidate set

C_E1 candidate (both branches): the frozen-model default reading only,
  E1-1: C_E1 = 1 (exact).

C_M1 candidates, intrinsic/local branch (evaluated against the LOCAL
wall triple only):
  M1-L1: C_M1 = 1 (graph reading; route A R1).
  M1-L2: C_M1 = exp(3*eta/4) = exp(1/24) = 1.042546905190
         (operator/eigenvalue-clock reading; routes A and B convergent).

C_M1 candidates, warped branch (evaluated against the WARPED wall
triple only):
  M1-W1: C_M1 = exp(eta*[B(2) - B(1/2)]) = 1.011519893216
         (same-mode-ratio reading; route A; the frozen-form-consistent
         extension per V1 claim 3), with
         B(λ) = I_{7/2}(6 sqrt λ)/I_{5/2}(6 sqrt λ).
  M1-W2: C_M1 = exp(eta*[B(2) - B(1/2)/2]) = 1.025283774326
         (eigenvalue-clock reading; route B; weaker textual support).

Ratio candidates: C_E1/C_M1 = 1/C_M1 for each branch-matched M1
candidate above (4 values; mechanical, no freedom).

Total comparisons: local slots {C_M1, C_E1, ratio} x {M1-L1, M1-L2}
(C_E1 fixed at 1) + warped slots x {M1-W1, M1-W2} = 12.

## Wall numbers (acceptance targets, unchanged from rounds 1-2)

Local:  C_M1 = 0.977679087638, C_E1 = 1.93121474779,
        ratio = 1.97530536575.
Warped: C_M1 = 0.936832609588, C_E1 = 1.81920864981,
        ratio = 1.94187161205.

## Classification rule (unchanged from rounds 1-2)

HIT: |fractional deviation| <= 1e-4. LEAD: <= 1e-3. Else MISS.
Look-elsewhere: 12 comparisons of pre-fixed values; at uniform-null hit
density comparable to rounds 1-2 (E[accidental] ~ 3e-5 per comparison),
E[total accidental hits] < 1e-3 — any HIT would be significant; the
candidate count is too small for accidental LEADs to be probable
(E ~ 1e-2).

## Pre-declared interpretation

- Any HIT: the matched reading's premise chain (named in the panel
  record) becomes the priority derivation target; not banked as
  evidence until the premises are derived.
- All MISS (the structurally expected outcome — all surviving C_M1
  candidates are >= 1, and the panel derived no mechanism producing
  C < 1): recorded as round-3 clean miss. The standing conclusion
  sharpens to: the coefficient object lives in the UNDERIVED pieces —
  the boundary measure / core-interior weight (now localized by the
  panel: core-side node weights get zero from the collar) and/or the
  P_f-variable resolution — and any candidate reading that dresses
  slots with positive-definite transfer actions on top of the frozen
  gamma cannot reach the wall numbers.
- No partial credit, no post-hoc inversions (1/C), no branch crossing,
  no new combinations. The quarantined 160/81 observation remains
  quarantined: no panel route produced the form 2(1-s^2), so it gains
  no status from this round.
