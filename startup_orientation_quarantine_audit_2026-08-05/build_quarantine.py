#!/usr/bin/env python3
"""Build the preregistered startup/orientation quarantine deterministically."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "startup_orientation_history_2026-08-05"

EXPECTED = {
    "LIVE.md": "e5799c95824a5877cfedbd625b67ed6e68559f9becbf7541561333f0903e72b2",
    "HANDOFF.md": "d103140cb43c547c04750f83636a3e9f7eba3a747653c7e581c5ed6f600c1410",
    "INDEX.md": "9af54308d17322d59e8de610dd109a5aa8df38e52c9c657cc2c2383a7728ab7a",
    "README.md": "239c0e3c64b283feaadaacabc9a3e29e4db003bff082eee38d6f4d3a1317f5f4",
    "MEMORY.md": "8c25ba692a5c6117930c15e0e23b8354cb4575cda42edae94792dd09ae6f69d8",
    "AGENTS.md": "ca754afde36a0ff6cb6ffc47a65ed9c1d19889334ccbd7a1f82b5d636a46bb95",
    "CLAUDE.md": "59b2b74da1e087a608bccdafdac24a8f902799c396e129e3720e8bb5670b1a2e",
    "research/README.md": "d0f6284a607e7d6f4c1cebcef3c65a75e6f8db5bdf4070a127443e97ac9e1b2c",
    "research/_registry/README.md": "aeead8a0d928cbec33ad29f47f85440f63d43e790e05c3753100a3ae7efb50a4",
}

SNAPSHOT_NAMES = {
    "LIVE.md": "LIVE.pre_cleanup.md",
    "HANDOFF.md": "HANDOFF.pre_cleanup.md",
    "INDEX.md": "INDEX.pre_cleanup.md",
    "README.md": "README.pre_cleanup.md",
    "MEMORY.md": "MEMORY.pre_cleanup.md",
    "AGENTS.md": "AGENTS.pre_cleanup.md",
    "CLAUDE.md": "CLAUDE.pre_cleanup.md",
    "research/README.md": "research_README.pre_cleanup.md",
    "research/_registry/README.md": "research_registry_README.pre_cleanup.md",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_source(name: str) -> bytes:
    source = ROOT / name
    data = source.read_bytes()
    if digest(data) != EXPECTED[name]:
        raise SystemExit(f"PREHASH_MISMATCH:{name}:{digest(data)}")
    return data


def freeze_sources() -> dict[str, str]:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    texts: dict[str, str] = {}
    for name in EXPECTED:
        destination = ARCHIVE / SNAPSHOT_NAMES[name]
        if destination.exists():
            data = destination.read_bytes()
        else:
            data = exact_source(name)
            shutil.copyfile(ROOT / name, destination)
        if digest(destination.read_bytes()) != EXPECTED[name]:
            raise SystemExit(f"ARCHIVE_HASH_MISMATCH:{destination.relative_to(ROOT)}")
        texts[name] = data.decode("utf-8")
    return texts


def through_marker(text: str, marker: str) -> str:
    at = text.index(marker) + len(marker)
    return text[:at].rstrip() + "\n"


def build_live(text: str) -> str:
    return through_marker(text, "<!-- STARTUP_CURRENT_END -->") + """

## Historical orientation archive

All prior LIVE layers and durable historical narration formerly embedded below the current marker
are preserved byte-for-byte in
[`archive/startup_orientation_history_2026-08-05/LIVE.pre_cleanup.md`](archive/startup_orientation_history_2026-08-05/LIVE.pre_cleanup.md).
They are evidence and context, not startup authority. Use `CANON.md` for canon and
`CURRENT_RESEARCH_PROGRAM.md` for the active dependency spine. The machine-readable premise source
is `CURRENT_SCIENTIFIC_PREMISES.tsv`.
"""


def build_handoff(text: str) -> str:
    return through_marker(text, "<!-- STARTUP_CURRENT_END -->") + """

## Historical handoff archive

All prior handoff layers formerly embedded below the current marker are preserved byte-for-byte in
[`archive/startup_orientation_history_2026-08-05/HANDOFF.pre_cleanup.md`](archive/startup_orientation_history_2026-08-05/HANDOFF.pre_cleanup.md).
They are not resume authority. Current premise status is machine-readable in
`CURRENT_SCIENTIFIC_PREMISES.tsv`.
"""


def build_memory(text: str) -> str:
    prefix = text[: text.index("## PRIOR TOP")].rstrip()
    return prefix + """


## Historical memory archive

Prior TOP entries, the durable macro chronology, and older lesson summaries are preserved
byte-for-byte in
[`archive/startup_orientation_history_2026-08-05/MEMORY.pre_cleanup.md`](archive/startup_orientation_history_2026-08-05/MEMORY.pre_cleanup.md).
They are historical pointers, not the live frontier.

Machine-readable current premise status: `CURRENT_SCIENTIFIC_PREMISES.tsv`.
"""


def build_agents(text: str) -> str:
    route_start = text.index("Before interpreting the frontier")
    registry_start = text.index("For the 1,114 fixed-base artifact identities")
    science_start = text.index("The bootstrap/stable-matter interpretation")
    method_start = text.index("## Codex/Claude compatibility")
    route = """Before interpreting the frontier, read from disk in this exact order. **Bounded-startup rule:**
do not dump whole long files or recursively open cited evidence during orientation.

1. `LIVE.md` — read only `STARTUP_CURRENT_BEGIN` through `STARTUP_CURRENT_END`; it overrides every
   other status description.
2. `HANDOFF.md` — read only its matching current block.
3. `CURRENT_RESEARCH_PROGRAM.md` — the active dependency spine and bounded next question.
4. `CURRENT_SCIENTIFIC_PREMISES.md`, then `CURRENT_SCIENTIFIC_PREMISES.tsv` — the source-precedence
   registry for high-risk terms. Any disagreement with LIVE or a cited source is a mandatory stop.
5. The one current bounded audit and exact evidence named by the research program, only to the depth
   required by the user's task.
6. `stability_branch_follow_256_DECISION.md` only when particle operator/stability history is
   relevant; it is durable lane evidence, not the global frontier.
7. `CLAUDE.md` sections `How we work`, `DRIVER TRIGGERS`, and repo discipline only.
8. Only the specific protocol under `.claude/skills/*/SKILL.md` triggered by the actual task.
9. `INDEX.md` and `MEMORY.md` for compact pointers only; neither can overrule LIVE.

`UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` is a historical compatibility path, not a generic startup
read. Open it only when a task makes its dated evidence load-bearing. Its exact root path is retained
because historical verifiers depend on it.

**Compact semantic regression guard:** the founding character acts on **supplied ordered depth**;
pointwise `phi` is a presentation potential on the supplied factorization, not a claimed universal
physical scalar. `CHOSE_COMPARISON_CONFIGURATION` remains comparison-only;
`CHALLENGED_OWNER_POSTULATE_NOT_DERIVED` keeps strong local CSN inactive. The generic metric count is
a generic configuration-arena count. `X_max` is a `WORKING_FOUNDATIONAL_FRAME` for the
positional-dilation asymptote, not a material wall, preferred center, radial edge, or finite-cell
seal. Authoritative fields and sources are in `CURRENT_SCIENTIFIC_PREMISES.tsv`.

"""
    navigation_contract = text[registry_start:science_start]
    status_rule = """Scientific status belongs in `LIVE.md`, `CURRENT_RESEARCH_PROGRAM.md`, and the current premise
registry—not in this operational file. Historical startup/status prose is quarantined in
`archive/startup_orientation_history_2026-08-05/AGENTS.pre_cleanup.md`.

"""
    return text[:route_start] + route + navigation_contract + status_rule + text[method_start:]


def build_claude(text: str) -> str:
    prefix = text[: text.index("## Orientation")].rstrip()
    return prefix + """


## Orientation

- Work on `grok` and perform the exact synchronization/status sequence in `AGENTS.md`.
- `LIVE.md` is the first read and wins every status disagreement. Follow it with `HANDOFF.md`,
  `CURRENT_RESEARCH_PROGRAM.md`, and the current premise registry.
- This file is binding method, not scientific status. Read only the sections triggered by the task.
- Use `INDEX.md` and `MEMORY.md` as compact pointer checks after current authority is understood.
- `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` and the byte-identical control snapshots under
  `archive/startup_orientation_history_2026-08-05/` are historical evidence, not generic startup.
- Current artifact locations come from `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`; fixed R0-R1C
  inventories remain historical snapshots.
- Run `python3 -m pytest tests/` when verification is required; trust the current run rather than a
  count copied into this charter.
"""


def build_registry_readme(text: str) -> str:
    durable_start = text.index("`ROOT_OWNERSHIP.tsv` and `MIGRATION_READINESS.tsv`")
    durable = text[durable_start:]
    return """# Research registry semantics

These tables govern artifact navigation and reorganization classification; they do not govern
scientific premise meanings. Read root `LIVE.md`, `HANDOFF.md`, `CURRENT_RESEARCH_PROGRAM.md`, and
`CURRENT_SCIENTIFIC_PREMISES.md` / `CURRENT_SCIENTIFIC_PREMISES.tsv` first. The current bounded
law-order result is `udt_native_law_order_architecture_audit_2026-08-05/AUDIT_REPORT.md`. A conflict
between these controls and a cited source is a mandatory stop.

The dated scientific checkpoint prose formerly embedded here is preserved in
`archive/startup_orientation_history_2026-08-05/research_registry_README.pre_cleanup.md`. The
registry facts below remain the current reorganization/navigation semantics and do not create
scientific authority.

""" + durable


INDEX = """# INDEX — current repository map

`LIVE.md` is the only guaranteed-current status file and wins every disagreement.

## Startup

1. Synchronize `grok` exactly as specified in `AGENTS.md`.
2. Read the marked current block in `LIVE.md`.
3. Read the marked current block in `HANDOFF.md`.
4. Read `CURRENT_RESEARCH_PROGRAM.md`.
5. Read `CURRENT_SCIENTIFIC_PREMISES.md` and `CURRENT_SCIENTIFIC_PREMISES.tsv`.
6. Open only the current audit and load-bearing evidence routed by those controls.
7. Apply the task-triggered method in `CLAUDE.md` and `.claude/skills/`.

## Current scientific routing

- `CURRENT_RESEARCH_PROGRAM.md` — active dependency chain, banked structure, retired shortcuts,
  open joints, and next bounded investigation.
- `CURRENT_SCIENTIFIC_PREMISES.md` / `.tsv` — effective source-precedence and premise stamps.
- `udt_native_law_order_architecture_audit_2026-08-05/AUDIT_REPORT.md` — current bounded law-order
  audit; response-first is a working test priority, not a derived physical law.
- `udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md` — controlling
  `X_max` correction: a working observer-pair positional-dilation asymptote, not a boundary.
- `stability_branch_follow_256_DECISION.md` — durable particle operator/stability history, only when
  that separate lane is relevant.
- `research/README.md` and `research/_registry/CURRENT_ARTIFACT_PATHS.tsv` — lane navigation and
  current paths for the 1,114 fixed-base identities.

## Durable controls and ledgers

- `AGENTS.md` — startup and operational rules.
- `CLAUDE.md` — binding research method; not frontier status.
- `CANON.md` — Charles-canonized statements, append-only.
- `NEGATIVES_REGISTRY.md` — premise-scoped negatives.
- `PROVENANCE.md` — evidence provenance.

## Historical navigation

- `archive/startup_orientation_history_2026-08-05/` — byte-identical pre-cleanup startup controls,
  quarantine map, and compatibility registry.
- `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` — retained root compatibility path for dated historical
  evidence; not generic startup authority.
- `HANDOFF_ARCHIVE.md` and `archive/LIVE_*.md` — earlier session/frontier layers.
- `archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md` — pre-lean index history.
- `reorganization_r0/` through `reorganization_r1h/` — fixed organization evidence; do not rewrite
  them to represent current paths.

## Repository layout

- root — live controls and still-rooted research artifacts;
- `research/` — lane navigation and the small number of authorized migrated artifacts;
- `archive/` — historical evidence and quarantined orientation layers;
- `evidence/`, lane-specific audit directories, and data directories — load-bearing records opened
  only when routed by the active task.
"""


README = """# UDT repository

This repository is an evidence ledger. `LIVE.md` is the only guaranteed-current scientific status
file; `CANON.md` changes only with Charles's explicit sign-off.

## Start here

After synchronizing `grok` exactly as directed by `AGENTS.md`, read:

1. the marked current block in `LIVE.md`;
2. the marked current block in `HANDOFF.md`;
3. `CURRENT_RESEARCH_PROGRAM.md`;
4. `CURRENT_SCIENTIFIC_PREMISES.md` and `CURRENT_SCIENTIFIC_PREMISES.tsv`;
5. only the current audit and exact evidence those controls make load-bearing.

Then apply the targeted method sections in `CLAUDE.md` and the task-triggered protocol under
`.claude/skills/`. Use `INDEX.md` and `MEMORY.md` only as compact pointer checks. `AGENTS.md` supplies
operational instructions but cannot overrule `LIVE.md`.

## Navigation

- `CURRENT_RESEARCH_PROGRAM.md` — current scientific dependency spine and bounded next work.
- `udt_native_law_order_architecture_audit_2026-08-05/AUDIT_REPORT.md` — current bounded law-order
  result routed by that program.
- `udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md` — controlling
  working positional-dilation asymptote frame; its realization and value remain open.
- `research/README.md` — research-lane navigation.
- `research/_registry/CURRENT_ARTIFACT_PATHS.tsv` — current paths for the fixed-base artifact set.
- `INDEX.md` — concise control, lane, ledger, and archive map.
- `CANON.md`, `NEGATIVES_REGISTRY.md`, `PROVENANCE.md` — durable status/evidence ledgers.

## Historical material

Previous startup layers are preserved byte-for-byte under
`archive/startup_orientation_history_2026-08-05/`. They are historical evidence, not current
authority. `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` remains at root solely as a historical
compatibility path for exact-path verifiers and must not be used as generic startup.

The R0-R1H reorganization evidence remains fixed. Current locations come from
`research/_registry/CURRENT_ARTIFACT_PATHS.tsv`; no further content migration is implied or
authorized by this navigation cleanup.
"""


RESEARCH_README = """# Research lane navigation

This directory is a navigation overlay, not a scientific authority and not a copy of the research
record. Root `LIVE.md` wins every status disagreement.

## Current route

Read root `LIVE.md` and `HANDOFF.md`, then `CURRENT_RESEARCH_PROGRAM.md` and
`CURRENT_SCIENTIFIC_PREMISES.md` / `CURRENT_SCIENTIFIC_PREMISES.tsv`. The current bounded result is
`udt_native_law_order_architecture_audit_2026-08-05/AUDIT_REPORT.md`: law/variation ownership,
admitted complete solutions, source/mass roles, and bootstrap's missing return form one ordered
closure chain. Response-first is a working test priority, not a derived law; action-first remains
conditional and admissible.

The controlling `X_max` source is
`udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md`. It records the
working observer-pair positional-dilation asymptote, not a material wall, preferred center, radial
edge, finite-cell seal, or boundary term. The exact law and value remain open.

## Lanes

- `foundations/` — foundational and metric-led navigation.
- `native_action/` — native-action and variation-domain navigation.
- `particle_mass/` — carrier-conditional stability and mass-program navigation.
- `macro/` — macro/WR-L/SNe navigation.
- `_registry/` — fixed-base ownership/readiness snapshots plus current path/classification overlays.

Lane READMEs and inventories are pointers only. For the fixed-base set, use
`_registry/CURRENT_ARTIFACT_PATHS.tsv` for present locations and
`_registry/CURRENT_CLASSIFICATION.tsv` for the effective classification overlay. No further
migration is authorized.

## Historical route

The former 335-line current/parent/prior science tour is preserved byte-for-byte at
`../archive/startup_orientation_history_2026-08-05/research_README.pre_cleanup.md`. It is historical
navigation, not startup authority. The dated root `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` likewise
remains only as an exact-path historical compatibility record.
"""


def main() -> None:
    texts = freeze_sources()
    outputs = {
        "LIVE.md": build_live(texts["LIVE.md"]),
        "HANDOFF.md": build_handoff(texts["HANDOFF.md"]),
        "MEMORY.md": build_memory(texts["MEMORY.md"]),
        "AGENTS.md": build_agents(texts["AGENTS.md"]),
        "CLAUDE.md": build_claude(texts["CLAUDE.md"]),
        "INDEX.md": INDEX,
        "README.md": README,
        "research/README.md": RESEARCH_README,
        "research/_registry/README.md": build_registry_readme(texts["research/_registry/README.md"]),
    }
    for name, content in outputs.items():
        (ROOT / name).write_text(content, encoding="utf-8")
    print(f"PASS: froze {len(EXPECTED)} exact snapshots and rebuilt {len(outputs)} controls")


if __name__ == "__main__":
    main()
