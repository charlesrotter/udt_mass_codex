# UDT H3 F Post-return Audit Repair + Codex Transition Dispatch

**Date:** 2026-07-17
**Branch:** `grok`
**Purpose:** correct the F evidence record and the stale native-action consistency test without
changing numerical fields, then make a fresh Codex workstation session self-orienting.
**Scope:** evidence/documentation repair only. No new carrier relaxation, no new F branch sweep, no G
rerun, no native-action arm, no canonization.

## 0. Stop conditions and authority

`LIVE.md` topmost `CURRENT STATE` remains the frontier authority. `CANON.md` is untouched. Preserve all
unrelated dirty and untracked work. Do not rewrite history or amend the existing F commits.

The strongest conclusion permitted by this repair is:

\[
\boxed{
\begin{gathered}
\text{No topology change, lower stationary state, or resolved basin exit was observed}\\
\text{in the preregistered finite-grid }L=6\text{ soft-direction slice.}\\
\text{The fine-grid endpoints all returned; the }128^3\text{ OTHER family is}\\
\text{consistent with the measured near-degenerate T/R box drift.}
\end{gathered}}
\]

`Single robust basin` may be retained only as a **strong finite-slice lead/inference**, not as a literal
classification of all 83 endpoints and not as physical dynamics or an infinite-volume theorem.

## 1. Mandatory startup and evidence read

Run exactly:

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

Do not trust the hashes or counts in this dispatch. Read, in order:

1. `LIVE.md`;
2. `HANDOFF.md`;
3. `stability_branch_follow_256_DECISION.md`;
4. `noNull_behavioral_F.py`, `verify_noNull_behavioral_F.py`, every `noNull_F_*.json` used below,
   the raw F logs, and the endpoint manifest/NPZ metadata;
5. `UDT_H3_BOUNDARY_AUDIT_PATCH_THEN_F_DISPATCH.md` Part B;
6. root `AGENTS.md`, then the relevant project-method text in `CLAUDE.md` and `.claude/skills/`.

Before editing, independently print and bank the exact per-grid endpoint count and class histogram,
the energy/displacement/charge ranges, the control results, and the list of trajectory-record keys.

## 2. Audit findings to reproduce, not assume

The chat-side audit of pulled commit `b8edad0` found the following. Recompute each from the files and
record any disagreement:

- `noNull_F_ladder_N128.json` contains **59**, not 58, endpoints: 1 `RETURNED BASIN` and 58
  `OTHER STATIONARY BRANCH`.
- `noNull_F_fine_N192.json` and `noNull_F_fine_N256.json` contain 12 endpoints each, all
  `RETURNED BASIN`; the exact total is **83**.
- The two control repeats at each grid take zero solver steps because their input carrier already
  satisfies the criticality gate. Therefore `sigma=0` is deterministic identity/replay, not a measured
  restart-variability estimate. The preregistered floor envelopes remain valid and must not be changed.
- At 128 cubed the endpoint displacement range is approximately 0.2 to 7.1, while the six T/R controls
  span approximately 3.6 to 19.7. Thus the former is not wholly `inside` the latter; it is bounded by
  its upper scale and overlaps it only partly.
- The T/R controls are not a single uniform shelf. In particular, representative translation energy
  offsets can change sign at fine grids. The negative Rz offset fades in magnitude with refinement;
  phrase this narrowly.
- The production small-amplitude gate is numerically strong: its finite-difference quadratic response
  agrees with the exact HVP at roughly 2 to 5 times 10^-8 relative error.
- The current independent verifier does **not actually use** its independently computed geodesic
  energies in that check. It evaluates one positive geodesic point and the base field, then compares a
  shared production `hvp_exact` result to production JSON. This is a verifier implementation gap, not
  evidence that the production gate failed.

## 3. Repair the independent small-amplitude check

Edit `verify_noNull_behavioral_F.py` in place. Do not import branch construction or classification
from `noNull_behavioral_F.py`.

For at least the saved `v5` direction at every grid, and preferably the isolated `v7` direction too:

1. reconstruct the independently normalized tangent direction from saved artifacts;
2. construct both exact pointwise geodesic fields `n(+theta)` and `n(-theta)` with the verifier's own
   implementation at the same preregistered theta used by production;
3. evaluate both with the verifier's own eight-orientation energy loop;
4. compute

   \[
   q_{\rm own}(\theta)=\frac{E(+\theta)-2E(0)+E(-\theta)}{\theta^2};
   \]

5. compare `q_own` directly with the production gate JSON value and with the exact-HVP quadratic form;
6. record all three raw values and relative discrepancies in `noNull_F_verify.json`.

The exact HVP remains shared audited derivative code unless the verifier independently differentiates
its own energy implementation. Label that comparison `shared exact-HVP cross-check`; do not call it an
independent Hessian implementation. The own-energy finite difference is the independent load-bearing
check.

Make each comparison a real named check that can fail. Remove unused values. Add a catch-proof test or
one-shot controlled mutation showing that perturbing the saved production q beyond tolerance makes the
new check red; restore the original artifact immediately and record the catch-proof output.

## 4. Repair the prose ledger

Edit `noNull_behavioral_F_results.md` in place:

- `58 branches` -> `59 branches` at 128 cubed;
- `~82 branches` -> `83 branches` exactly;
- state the exact class histogram: 1 RETURNED, 58 OTHER at 128; 24/24 RETURNED across the fine grids;
- replace `all returns` with `no resolved basin exit; all fine-grid endpoints returned`;
- correct the displacement comparison;
- distinguish the Rz negative-offset refinement trend from the full six-generator control set;
- describe control `sigma=0` as deterministic zero-step replay with preregistered floors, not observed
  stochastic/restart variability;
- update the verifier paragraph to distinguish the independent own-energy finite-difference check from
  the shared exact-HVP cross-check;
- mark `single robust basin` as `STRONG LEAD within the preregistered finite-grid slice`.

Reconcile the same wording in `LIVE.md`, `HANDOFF.md`, and `INDEX.md` only as needed to prevent a new
session from reading a stronger claim. This dispatch authorizes those narrow honesty corrections, but
no frontier advance and no `CANON.md` change.

Do not alter raw endpoint classes to make the prose cleaner. Do not change thresholds, envelopes,
fields, or production JSON except the regenerated verifier output.

## 5. Repair the stale native-action consistency test

The fresh Codex orientation correctly identified that `UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md` §1
still treats the superseded centered-carrier result

\[
M_N=2E_4=E_2+E_4\quad\text{to }0.05\%
\]

as the mandatory consistency test. Verify this against the current G and boundary-virial records, then
edit that draft narrowly. The corrected-carrier facts are:

\[
M_N^{(0)}=2E_4
\]

only **CONDITIONAL** on the EH lapse premise, while on a finite domain

\[
E_4-E_2=B_{\partial\Omega}+W_{\rm res},\qquad
M_N^{(0)}=E_{\rm carrier}+B_{\partial\Omega}+W_{\rm res}.
\]

For an exact critical point `W_res=0`; for the saved numerical carrier it is retained and reported.
The corrected `L=6` continuum audit has a persistent virial gap of approximately -2.7%, so
`2E4=E2+E4` is not a current finite-box identity. The boundary-stress explanation is a strong lead;
the local surface theorem and infinite-volume closure remain open.

Require every derivation arm to predict all three separately:

1. the source/lapse mass rule;
2. the finite-domain carrier virial/boundary relation;
3. the controlled limit, if any, in which the boundary and residual terms vanish.

Retain the old 0.05% statement only as explicitly `SUPERSEDED centered-operator provenance`, never as
current evidence or a pass criterion. Make no other mathematical or process change to the native-action
draft and do not launch its arms.

## 6. Codex startup bridge

Ensure the supplied root `AGENTS.md` is tracked. Verify that it:

- makes the exact pull/status/log sequence mandatory;
- preserves dirty work;
- establishes `LIVE.md -> HANDOFF.md -> stability decision -> exact evidence` as the first read chain;
- imports the binding method from `CLAUDE.md` and `.claude/skills/` manually;
- states explicitly that `.claude/hooks`, Claude memory, and Claude skill auto-loading do not enforce a
  Codex session;
- carries the UDT-purity, premise-label, raw-residual, verification, canon, and one-GPU-process rules;
- contains no volatile commit hash or duplicated frontier summary.

Start a fresh Codex 5.6 Sol session with no conversation history and only the repository. Ask it to
perform the startup sequence and return, without editing or computing:

1. actual HEAD/status;
2. current honest particle-lane claim and all premise stamps;
3. exact F endpoint counts/classes;
4. why `single robust basin` is a lead rather than a literal all-endpoint classification;
5. the current open choices and the next action authorized by `LIVE.md`.

Save the complete rehearsal transcript. If it misses any item, repair `AGENTS.md` and repeat once with
another fresh session. Do not feed the expected answer into the rehearsal prompt.

## 7. Verification and return

Run syntax checks, the repaired F verifier, its catch-proof, and the evidence consistency checker. Save
complete stdout/stderr and compact JSON. Confirm endpoint hashes are unchanged.

Commit and push two logical commits if both file groups changed:

1. F evidence/verifier and native-action-draft erratum;
2. Codex startup bridge and zero-context rehearsal.

Return and stop with:

- reproduced exact counts/ranges/control facts;
- repaired verifier checks and raw discrepancies;
- catch-proof result;
- unchanged endpoint-hash confirmation;
- corrected maximum conclusion wording;
- fresh Codex rehearsal verdict and any missed item;
- paths and commits;
- `git status --short --branch` and `git log -8 --oneline`;
- every unresolved issue.

Do not start F extensions, G extensions, the native-action arms, or canonization.
