# F — finite-amplitude basin behavior of the certified carrier (RESULTS)

**Date:** 2026-07-17 · **Dispatch:** `UDT_H3_BOUNDARY_AUDIT_PATCH_THEN_F_DISPATCH.md` PART B · grok
**Observing or targeting:** OBSERVING — basin characterization along the certified soft directions;
all endpoint classes preregistered; both return and transition were full-credit outcomes. DATA-BLIND.
**Verifier status:** independent verifier `verify_noNull_behavioral_F.py` **PASS 51/51**. Its
load-bearing small-amplitude check independently reconstructs the `v5` and `v7` tangents, constructs
both pointwise geodesics, and evaluates all three energies with its own eight-orientation loop at
every grid: own finite-difference q vs production q agrees to 0–6.7e-10 relative. Comparison with
the shared audited `hvp_exact` path (not an independent Hessian implementation) agrees to
0.92–1.66e-7 relative. All classification predicates replay identically from raw JSON. The
production gate itself remains stronger still at 2–5e-8 relative at its smallest amplitude
(registered gate 1e-2). Catch-proof: a controlled 0.1% mutation of saved production q made the new
check RED at tolerance 1e-6; the artifact was restored byte-for-byte.
**NOT claimed:** physical dynamics or dynamical stability (trajectories are trust-region relaxation
paths); infinite-volume basin; native matter emergence; any particle-mass statement. The L=7.5 scouts
were NOT used as F backgrounds.

## Premise ledger (per dispatch §5)
Carrier+L2+L4 POSIT/CHOSE · discretization DERIVED numerically · L=6/HBW=2 positive Hessian
OBSERVED/CERTIFIED · F outcomes = OBSERVED numerical basin behavior per grid · EH/G not used.

## Directions & gates
Seed agreement reproduces certification (doublet principal cosines 1−4e-10; iso overlap 1−3e-9);
T/R full-rank; complement projection to 1e-8; cross-grid alignment cosines 0.9998/0.99998.
The two nominal control repeats at each grid are deterministic zero-step identity replays because
the saved carrier already passes the criticality gate; their zero differences are not a measured
restart-variability estimate. The preregistered floors remain unchanged: τ_E=1e-3, τ_Q=0.02,
τ_loc=0.01. U(1) rotation gives dE=0 exactly. The T/R θ=0.10 controls form a nonuniform family of
near-degenerate displaced copies (shallow box walls): specifically the negative Rz offset fades in
magnitude, −2.22e-3 (128³) → −4.12e-4 (192³) → −1.62e-4 (256³). This narrow trend is consistent
with the marginal-wall finding; the full six-generator set is not called one uniform shelf (the
representative Tx offset changes sign at the fine grids).

## 128³ bracket (59 branches: 8 doublet-plane dirs + both iso signs; θ 0.05→1.20 + bisections)
**No transition found within the registered resolved amplitude range.** Topology held everywhere
(Q_f −0.967, Q_s −0.966, all endpoints); no distinct lower state (all |dE| ≤ 2.3e-3 vs the −5e-3
gate). Exact classes: **1 RETURNED BASIN, 58 OTHER STATIONARY BRANCH**. Endpoint displacements span
0.214–7.105, while the six T/R controls span 3.608–19.749: the endpoint range overlaps the control
range only partly and is bounded by its upper scale; it is not wholly inside it. Preregistered
envelopes were applied AS REGISTERED: the near-degenerate T/R box-drift evidence is consistent with
the 58 OTHER endpoints, but their raw classes are retained rather than relabeled. The single bisected
bracket (iso_plus 0.05/0.10) marks a class change/drift onset, not a resolved basin exit.

## Fine-grid confirmation (§11 set: θ∈{0.4,0.8,1.2} × {dbl_a0, dbl_a2, iso±})
**192³: 12/12 RETURNED BASIN** (dE within −4.1e-4; Q_f −0.986 stable).
**256³: 12/12 RETURNED BASIN** (dE within ±1.6e-4; Q_f −0.9923 stable; one branch drifted
displacement 126 along the near-degenerate drift family and still returned
energetically+topologically).
Across the fine grids **24/24 endpoints classify RETURNED BASIN**. Together with the narrowing Rz
wall offset, this supports a single-basin interpretation of the sampled slice, but does not convert
the 58 raw 128³ OTHER classifications into returns.

## Conclusion (post-return audit maximum)
**No topology change, lower stationary state, or resolved basin exit was observed in the
preregistered finite-grid L=6 soft-direction slice. The fine-grid endpoints all returned; the
128³ OTHER family is consistent with the measured near-degenerate T/R box drift.** Exact census:
83 endpoints over three grids (128³: 1 RETURNED, 58 OTHER; fine grids: 24/24 RETURNED).

**Single robust basin is a STRONG LEAD within this preregistered finite-grid slice**, not a literal
classification of all 83 endpoints. Not dynamics; not infinite-volume; not a mass statement.
