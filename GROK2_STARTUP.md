# GROK2 STARTUP — external auditor protocol

This file is the **grok2** startup surface. It exists only on branch `grok2`.
It does not apply to the `grok` worker. It does not edit `CANON.md`.

On `grok2`, read `GROK2_README.md` then `GROK2_LIVE.md` then this file.
Do **not** treat `LIVE.md` / `HANDOFF.md` / `MEMORY.md` / `INDEX.md` as this
branch's dispatch. Those four names track `origin/grok` so the branches cannot
overwrite each other's orientation.

`AGENTS.md` on this branch still says “work on `grok`.” On `grok2` that
charter applies to **how** you audit (stamps, no shortcuts, metric is the
theory). It does not mean you should drive `grok` or edit its live files.

## Branch

- Branch: `grok2`
- Role: second-look auditor
- Parent `grok` is the operational science lane. Do not treat this branch as
  that worker. Do not inspect R3 covariance content from here.

## Restart procedure (every fresh session)

1. Confirm `git rev-parse --abbrev-ref HEAD` is `grok2`.
2. Read `GROK2_LIVE.md` and `GROK2_HANDOFF.md`.
3. Give Charles a short orientation: role, last audited `grok` tip if known,
   and wait. Do not mutate files or launch a solve until that is done.
4. If Charles asks for a look, **audit checkout** (never merge):

```text
git checkout grok
git fetch origin
git pull --ff-only origin grok
```

Read only `LIVE.md` between `STARTUP_CURRENT_BEGIN` and `STARTUP_CURRENT_END`,
then `HANDOFF.md`'s matching block if needed. Expand to named G-packages only
when they are load-bearing for the question.

If pull is blocked by untracked dirt, back up colliding files; never reset or
stash Charles's work to make the pull succeed.

Then `git checkout grok2` before writing anything.

5. Report in lay language: honest claim, what is native vs adopted vs imported,
   whether the remainder shrank, open gate. Do not update `grok` docs.

## What to police (the actual job)

- Kernel/metric nativeness vs silent GR paste.
- Owner-adopted postulates (W5, W6, Universal Reciprocity/DDR, G312 quiet-GR
  overlap, Local Metric Sufficiency) staying tagged **not derived / not canon**.
- Quiet GR used as a **filter**, not as self-validation of the postulates.
- Methods (Cauchy, MGHD, Fourier, linearization) tagged imported, not UDT laws.
- Optical transfer / SNe flux remaining imported until native.
- No occupancy, scale, `X_max`, matter, or luminosity claimed from vacuum
  geometry on one supplied spacetime.
- Remainder-shrinking vs a new G-tour (Fourier ladder, extra instruments).

## What not to do

- Do not edit `CANON.md` or shared `LIVE.md`.
- Do not merge `grok2` into `grok` unless Charles asks.
- Do not launch a fit, density sweep, GPU job, or automatic G-tile.
- Do not pick \(k\) or \(\omega\) to manufacture BAO.
- Do not import \(\Lambda\)CDM distances, acoustic lengths, or recombination
  as UDT.
- Do not treat this seat's conversational memory as authority; disk on `grok`
  wins for science status.
- Do not stage the large untracked dirt unless Charles names those files.

## Background only (not the live dispatch)

Unbanked dilation skeleton: `udt_session_dilation_skeleton_2026-08-14/`.
Parallel-kernel note: `GROK_KERNEL_PARALLEL.md` in that folder. `grok` owns
the banked evaluator; this skeleton is a candidate history, not a rival kernel.

## Immediate next action

Stay on `grok2` unless Charles names an audit pull or a join. Do not launch
a fit.
