# BRANCH OPERATOR — explicit G/P switch (Branch-P push, Step A)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **Status:** BUILT + blind-verified
(VERIFIED-WITH-CAVEATS; caveats = scope notes). Mode: INFRASTRUCTURE / OBSERVE-setup, DATA-BLIND.
Files: `branch_operator.py`, `tests/test_branch_operator.py`.

## Why (the finding that motivated this)
The 2026-06-22 native-S² static solves ("native matter = a scale-free DEFECT") silently used the
DERIVED operator on **Branch G** (the branch that GAUGES THE ANGULAR-CURVATURE OBSTRUCTION AWAY) —
the branch choice was NOT in that solve's premise ledger (it was named only upstream in
matter_regrade R1). **Branch P** (keeps the angular curvature as a physical potential `−2U`,
U=e^{2φ}−1 — a scale-breaker) was characterized only in VACUUM and never coupled to the native
matter. Since the curvature fork IS the φ-angular tension (the standing hunch) and matter is the
scale-breaker, the "scale-free defect" headline is BRANCH-G-CONDITIONED and possibly an artifact.
Also: the gravity-operator code behind the native solves (`derive_gravity.py`) was UNCOMMITTED.
Step A makes the branch an EXPLICIT switch AND provides a committed, auditable operator.

## What was built
`branch_operator.py` — a thin, audited wrapper over the VALIDATED derived-operator assembly in
`b1prime_3d_offround_residual.py` (Branch-G `E^μ_ν = f G^μ_ν + (δ□f − ∇∇f) − Xf(∂φ∂φ − ½δ(∂φ)²) −
kap8 f T`, f=e^{2φ}). The branch is a REQUIRED, EXPLICIT, TAGGED parameter (unknown → ValueError;
no silent default). Branch P adds `+δ^μ_ν U(φ)` to the metric operator and `−2U'(φ)` to the φ-EOM,
U=e^{2φ}−1, U'=2e^{2φ}. Every constant tagged (X=−2e5 FREE, ξ=κ FREE, kap8=1 DERIVED).

## Verified
- **Flat (φ=0, T=0): max|E|(body)=9.6e-14**, both branches.
- **Branch-G = the derived operator:** `b1prime.E_mixed` is verbatim `matter_regrade` line 60 (same
  f, same terms); it's the operator production callers use. (Inherited validation; the wrapper is a
  pass-through for Branch G.)
- **Branch-P additions complete + correct signs** (cross-checked vs branch_P eq 1a/1b: metric eq
  carries `−g_mn U` → `+δ^μ_ν U` on the operator side; φ-EOM carries `−2U'`). Only these two terms
  change between branches; the matter sector (EL_Th) is branch-independent (U is φ-only). U, U'
  algebra machine-checked.
- **Vacuum discriminator:** on slaved-Schwarzschild, U∈[0.23,1.35]>0, so Branch P ≠ Branch G by
  exactly +δU — consistent with branch_P's distinct vacuum EOM `2(X−2)r²φ'' + 4(X−2)rφ' − 2(e^{2φ}−1)=0`
  vs Branch-G/Schwarzschild `2rφ' + e^{2φ}−1 = 0`. Box-f discriminator: const-φ → box f=4e-14 (terms
  vanish exactly); slaved-φ → box f=0.60 (vacuum ≠ GR).
- **∇E identity (Branch G):** ∇_μ E^μ_ν = −½ EOM_φ φ' EXACTLY at X=0 (the strongest base-operator
  check; the X≠0 bookkeeping term reproduces the documented regrade_2/3b state).
- Integrity harness intact: `pytest tests/` = 23 passed / 5 xfailed (the 5 unchanged).

## Caveats (honest — verifier-flagged)
- `E_P − E_G = δU` is TAUTOLOGICAL by construction; the load is carried by the NON-tautological
  checks (sign-vs-doc, the box-f vacuum≠GR discriminator, U-algebra) — all correct.
- Branch-G correctness is INHERITED from b1prime's prior validation; this module only independently
  establishes the branch-DELTA, not the base assembly (appropriate for a thin wrapper).
- The doc's matter factor "½ e^{2φ}T" vs the repo's "kap8 f T (kap8=1)" — handled honestly (reuse the
  validated kap8 convention; no second ½ injected). FLAGGED to re-confirm at the coupled-solve stage.

## Verifier trail
Independent spot-checks (driver) + blind adversarial verifier (fresh zero-context, agent
a55b8f7d34f43d590): VERIFIED-WITH-CAVEATS — base operator is the derived Branch-G op, Branch-P
signs correct, no smuggling, tags present, branch explicit.

## Next (Branch-P push)
Step B — native-S² matter with the RADIAL DOF LIVE (unfreeze the rigid slice) + the Branch-P
operator → static coupled residual. Step C — bounded static solve (Nr≤16, single process, NO
background-poll): does a localized body / selected scale appear? Step D — SEAL-INDEPENDENCE sweep
(the native-vs-imported-scale gate: does the scale track the matter or the cell size?). Gate
(Charles): OBSERVE for emergence; if none after sufficient development, import under Postulate A.
