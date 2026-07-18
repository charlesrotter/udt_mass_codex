# R1G readout-provenance correction preregistration

**Date:** 2026-07-18

**Base:** `ad8b00b1629c5594dd9d82b0fa82d3fafa3441d6`

**Branch:** `codex/reorg-r1g-provenance-audit-2026-07-18`

**Mode:** correction overlay only; no integration or moves

This record is committed before reopening the candidate or family contents for
the correction audit.

## Controlling provenance rule

A standard-theory comparison or downstream readout does not change a native
UDT operator into `MIXED`. `MIXED` is permitted only when imported structure
enters the tested functional/action, variation, equation of motion, coupling,
or another load-bearing step that determines the tested result.

The correction must record five independent fields:

1. `operator_provenance`;
2. `imported_action_or_coupling`;
3. `comparison_readout`;
4. `scientific_lifecycle`;
5. `migration_safety`.

Reference-only material must retain an explicit disclosure such as
`comparison_readout=GR_EINSTEIN_TENSOR;MISNER_SHARP` and
`role=REFERENCE_ONLY`; it may not silently disappear merely because it does not
alter operator provenance.

## Frozen audit universe

The correction reaudits these named B02/B03 rows:

- `cascade_bv16_cas.py`;
- `cascade_or_energy_cas.py`;
- `verify_universe_bv2_f_einstein.py`.

It also reaudits the complete five-file `C12_ENERGY_ORIENTATION` family from
the existing R1G family census, and checks whether `phi_source_derivation.py`
and `homog_alpha_test.py` retain imported/free alpha coupling inside their
tested action or coupling.

The expected totals—29 native, 2 mixed, 1 open for B02/B03, and 121 native / 0
mixed for the affected cascade census—are hypotheses, not acceptance targets.
Any feedback from GR readout into the action, variation, EOM, coupling, or
load-bearing derivation overrides those expectations and must be documented by
an exact dependency.

## Required outputs and failure gates

The correction will preserve the prior R1G records as Git history while
updating the current R1G tables, summaries, proposal, rule schema, verifier,
reports, and hashes. The verifier must independently reconstruct coverage and
exercise failures proving that:

- reference-only GR readout cannot demote a native operator;
- removing required readout disclosure fails;
- an imported coupling entering the tested action cannot be labeled
  reference-only.

All prior R1G gates remain binding: exact 32- and 121-row coverage, Git
history/content identity, July 1 ancestry boundary, fixed-record isolation,
zero research/current-registry changes, links/frontier targets, all six frozen
manifests and package identities, the known test baseline, and the original
54-path dirty checkout by status/lstat metadata only with contents `NOT_READ`.

No B02/B03 move, classifier application, `origin/grok` update, research
artifact edit, registry edit, fixed R0–R1F rewrite, physics continuation, or
GPU work is authorized.
