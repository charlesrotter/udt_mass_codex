# UDT Mass Codex — Codex Working Instructions

Charles canonizes. Nothing enters `CANON.md` without his explicit sign-off.
This repository is an evidence ledger, not a place to turn a promising lead into a stronger claim.

## Mandatory startup

Work on branch `grok`. Do not trust a hash, branch count, or status quoted in a prompt or handoff.
At the start of every fresh session run, in order:

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

If a pull is blocked by local work, preserve and inspect that work. Never reset, overwrite, clean, or
stash user changes merely to make the pull succeed. If an untracked file collides with an identical
upstream file, prove that it is byte-identical and preserve a backup before moving it aside.

Before interpreting the frontier, read from disk in this exact order. **Bounded-startup rule:** do
not dump whole long files or recursively open every cited artifact during orientation. Read only the
marked/current sections below; expand to full reports, scripts, JSON, logs, or historical layers only
after the user's actual task makes them load-bearing.

1. `LIVE.md` — read only the range between `STARTUP_CURRENT_BEGIN` and `STARTUP_CURRENT_END`; its
   `CURRENT STATE` overrides every other status description. Do not read the remaining historical
   layers at startup.
2. `HANDOFF.md` — read only its `STARTUP_CURRENT_BEGIN` / `STARTUP_CURRENT_END` range.
3. `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` — initially read only `Current honest result`, `Current
   open discriminator`, and `Authority boundary`.
4. `angular_toric_closure_selector_2026-07-19/LAY_DECISION_TREE.md`, then
   `angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv` — the compact current theorem,
   counterfamily boundary, and two ordered gates. Read the full package `AUDIT_REPORT.md` only when
   the task requires its derivation or provenance.
5. `null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md` only when the exact reciprocal
   Hopf-orbit witness or its provenance becomes load-bearing, then
   `native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md` for the preceding carrier/topology
   classification only when that layer is relevant.
6. The exact scripts plus JSON/NPZ/log outputs load-bearing for the current return or task; none are
   part of generic startup orientation.
7. `stability_branch_follow_256_DECISION.md` when particle operator/stability history is relevant; it
   is durable lane evidence, not the global frontier.
8. `CLAUDE.md` sections `How we work`, `DRIVER TRIGGERS`, and repo discipline only; do not dump the
   whole charter at startup.
9. Only the specific full protocol under `.claude/skills/*/SKILL.md` triggered by the actual task;
   do not preload every skill.
10. The top/current summary in `INDEX.md` and `MEMORY.md`'s `TOP — CURRENT POINTER` for pointers only;
    neither can overrule `LIVE.md`.

For current artifact locations, use `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`. The R0–R1C
ownership, readiness, census, preregistration, and verification records are fixed historical
snapshots and must not be rewritten to mimic current paths. This is an operational navigation rule;
like every instruction in this file, it cannot overrule `LIVE.md`.

Then give Charles a short orientation report: actual HEAD and dirt, the current honest claim, its
premise stamps, the open gate, and the proposed bounded next action. Do not mutate files or launch a
long solve until that orientation is complete.

The bootstrap/stable-matter interpretation remains a working hypothesis. The bounded audit chain is
complete through angular–toric closure: the existing implementation is already full 3D Hopf-capable;
the reciprocal metric has an exact conditional Hopf-orbit-block witness; and `S3` plus free
diagonal/anti-diagonal Hopf actions are unique only after global toric eigencap premises are supplied.
Registered UDT does not yet derive the first missing gate—transverse spatial reciprocal realization
and periodicity—or the conditional second gate of finite-cell cap completion. Do not silently turn
either conditional theorem, the earlier celestial fiber, or the time-live proposal into authority to
adopt a carrier, section, torus, cap, framing, boundary, dynamical completion, run GPU work, or claim
a bootstrap parameter-selection theorem.

## Codex/Claude compatibility

`CLAUDE.md` and `.claude/skills/` contain binding project method even though their names are
Claude-specific. Read and apply them manually when their trigger applies. Codex must not assume that
`.claude/hooks/corral_trigger.py`, Claude project memory, background jobs, or Claude skill auto-loading
are active. The corresponding pauses are therefore manual and mandatory:

- before a solve: observing or targeting; whole frame or bounded slice; every physical choice tagged;
- before explaining a mismatch: solver completeness before any new mechanism;
- before a commit or verdict: preregistration, bounded scope, independent verification of the
  load-bearing premise, and premise audit;
- before words such as *proved*, *settled*, *stable*, *single basin*, *native*, or *derived*: state the
  exact regime and the remaining open scope.

Do not rely on conversational memory. Disk evidence wins.

## Binding UDT research rules

- Remain pure to UDT: **the metric is the theory**.
- Trace every claimed result explicitly to the UDT metric and the stated matter carrier.
- Keep the macro WR-L lane separate from the particle-mass/carrier lane.
- Do not import Lambda-CDM, Standard Model physics, quantum mechanics, QED, GR field equations,
  fluids, Q-balls, boson stars, or textbook mechanisms as UDT derivations. They may be comparison or
  readout tools only, clearly labeled.
- The `S^2` carrier is a `POSIT`, not a derived necessity. A replacement or emergence remains open.
- The conditional conformal-Lorentzian null-direction fiber is a celestial topological/conformal
  `S^2`; it does not by itself derive the carrier's fixed round target, section, transport, action,
  or boundary completion.
- An EH metric-only action is `CONDITIONAL` through the stated minimality premise; it is not native UDT
  merely because it is mathematically familiar.
- No fitting, fudge factors, hard physical cutoffs, effective corrections, or invented couplings.
- Numerical controls and consistent discretizations are allowed only when they do not change the
  tested continuum functional.
- Use full nonlinear covariant operators. Do not linearize without a controlled error and an explicit
  scope stamp.
- Audit algebra, signs, boundary conditions, operator provenance, convergence, raw evidence, and code
  before accepting or abandoning an approach.
- Use the labels `DERIVED`, `CHOSE`, `WORKING`, `OPEN`, `CONDITIONAL`, `POSIT`, and `OBSERVED`
  precisely. A numerical result is `OBSERVED`, not automatically physics or canon.
- Raw residual/backward error remains the certification gate. A preconditioned residual may diagnose
  or accelerate, but never silently replace it.

## Method

Default order is `MAP -> OBSERVE -> PONDER -> DERIVE`. MAP and PONDER with Charles are brief and in lay
language. Derivation begins only after the frame, assumptions, and premise ledger are visible and
Charles gives the go.

For every proposed computation, state:

1. the whole question and the exact bounded regime being sampled;
2. whether the question is metric-led or template-led;
3. every physical value, boundary condition, sign, chart, source, carrier, and action premise as
   `free-and-explored`, `pinned-by-THEORY` with a citation, or `pinned-by-HABIT`;
4. what degrees of freedom, sectors, branches, boundaries, and limits are not covered;
5. a preregistered falsification/certification contract and maximum allowed conclusion.

Characterize the solution space; do not filter it to demand a particle, lump, spectrum, smooth shape,
or expected answer. A negative is always premise-scoped. If a premise changes, re-grade every negative
that depended on it.

When a result disagrees with expectation, check in order: omitted terms/sectors/boundaries, numerical
convergence or bugs, frozen degrees of freedom, and incomplete solution-space exploration. Do not add a
mechanism to repair a mismatch.

## Evidence and banking

- Pre-register tests, tolerances, candidates, classifications, and conclusion wording before seeing
  outcomes. Do not retune after inspection.
- Independently recompute the load-bearing quantity from saved artifacts. Hunt circular checks,
  shared-code false independence, vacuous assertions, loose tolerances, and incomplete sampling.
- For a load-bearing result, use a fresh adversarial context and an independent implementation; use a
  different method or model family where practical. A same-code comparison is a regression check, not
  independent evidence.
- Preserve raw stdout/stderr, compact machine-readable outputs, exact commands, versions, parameters,
  array shapes, and SHA-256 manifests for large artifacts.
- Commit one logical evidence change at a time and push `grok`. Edit the canonical live file rather
  than proliferating `v2` scripts; git is the rollback trail.
- Do not edit `LIVE.md` or `CANON.md` unless the current dispatch or Charles explicitly authorizes it.
  Never overwrite grid artifacts; use grid-tagged and branch-tagged filenames.
- Preserve unrelated dirty and untracked files. Never use destructive git or filesystem commands.

Before banking any verdict, explicitly report the four gates:

1. preregistered;
2. full space, or bounded scope justified;
3. independently verified on the load-bearing premise;
4. every premise audited.

If any gate is absent, bank a `LEAD`, `OPEN`, or `VERIFIED-WITH-CAVEATS`, not a settled result.

## Numerical operations

- Use one GPU process at a time. Confirm the selected process, device, dtype, grid, memory estimate,
  output names, timeout, checkpoint/restart behavior, and stop conditions before launch.
- Prefer saved-field recomputation to repeating a relaxation.
- Bound exploratory work. Long production work requires a written dispatch and preregistered gates.
- Check GPU results with independent CPU/symbolic anchors where feasible.
- For corrected-carrier work, use the audited no-null `L2+L4` functional and its exact-HVP path; old
  centered-derivative tools are provenance only unless a task explicitly audits them.
- A relaxation trajectory is not physical time evolution. A finite box is not the infinite-volume
  limit. Positive sampled Ritz values alone are not stability certification.

## Communication

Keep returns concise but retain decisive equations and raw gates. Lead with what was actually learned,
then state what remains open. Separate observation, inference, and canonization. Charles owns the final
physics verdict.
