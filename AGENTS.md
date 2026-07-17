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

Before interpreting the frontier, read from disk in this exact order:

1. `LIVE.md` — its topmost `CURRENT STATE` overrides every other status description.
2. `HANDOFF.md` — top/current block only.
3. `stability_branch_follow_256_DECISION.md` — for the decision and operator history.
4. The exact scripts plus JSON/NPZ/log outputs load-bearing for the current return or task.
5. `CLAUDE.md` sections `How we work`, `DRIVER TRIGGERS`, and repo discipline.
6. The relevant full protocols under `.claude/skills/*/SKILL.md`.
7. `INDEX.md` and the top of `MEMORY.md` for pointers only; neither can overrule `LIVE.md`.

Then give Charles a short orientation report: actual HEAD and dirt, the current honest claim, its
premise stamps, the open gate, and the proposed bounded next action. Do not mutate files or launch a
long solve until that orientation is complete.

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
