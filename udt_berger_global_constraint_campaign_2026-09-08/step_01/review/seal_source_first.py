#!/usr/bin/env python3
"""Pin only the authorized source-first inputs and reviewer artifacts."""
import datetime
import hashlib
import json
from pathlib import Path

here=Path(__file__).resolve().parent
root=here.parents[2]
sources=[
    "AGENTS.md", "CLAUDE.md", "CURRENT_SCIENTIFIC_PREMISES.tsv",
    ".claude/skills/verifier-before-record/SKILL.md",
    ".claude/skills/no-shortcuts/SKILL.md",
    ".claude/skills/completeness-map/SKILL.md",
    ".claude/skills/solution-space-not-imposition/SKILL.md",
    "startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md",
    "startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md",
    "udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md",
    "udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/AUDIT_REPORT.md",
    "udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02/EXACT_DERIVATION.md",
    "udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02/AUDIT_REPORT.md",
    "udt_berger_global_constraint_campaign_2026-09-08/WORK_ORDER.md",
    "udt_berger_global_constraint_campaign_2026-09-08/step_01/QUESTION.md",
    "udt_berger_global_constraint_campaign_2026-09-08/step_01/REVIEW_DISPATCH.md",
    "udt_berger_global_constraint_campaign_2026-09-08/STARTUP_AUDIT.json",
    "udt_berger_global_constraint_campaign_2026-09-08/STARTUP_AUDIT.command.txt",
    "udt_berger_global_constraint_campaign_2026-09-08/STARTUP_AUDIT.stdout",
    "udt_berger_global_constraint_campaign_2026-09-08/STARTUP_AUDIT.stderr",
]
digest=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
prefix=root/"udt_berger_global_constraint_campaign_2026-09-08"
receipt=json.loads((prefix/"STARTUP_AUDIT.json").read_text())
assert receipt["returncode"]==0 and not receipt["timeout"]
assert receipt["stdout"]==(prefix/"STARTUP_AUDIT.stdout").read_text()
assert receipt["stderr"]==(prefix/"STARTUP_AUDIT.stderr").read_text()
rows=[line for line in (root/"CURRENT_SCIENTIFIC_PREMISES.tsv").read_text().splitlines()
      if line.split("\t",1)[0] in {"G310","G312","G315","G330"}]
assert len(rows)==4
(here/"SOURCE_REGISTRY_ROWS.tsv").write_text("\n".join(rows)+"\n")
(here/"SOURCE_INPUT_SHA256SUMS").write_text("".join(f"{digest(root/p)}  {p}\n" for p in sources))
record={"sealed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "reviewer":"/root/bg1_review", "fresh_context":True,
        "different_model":"UNTESTED", "author_candidate_exposure":False,
        "author_code_or_outputs_exposure":False,
        "startup_receipt_streams_authenticated":True,
        "startup_independently_replayed":False,
        "parent_reported_HEAD":"8784f168bf08473b202fc9485eedefcfff920859",
        "command":"python3 -B udt_berger_global_constraint_campaign_2026-09-08/step_01/review/seal_source_first.py"}
(here/"SOURCE_FIRST_SEAL.json").write_text(json.dumps(record,indent=2)+"\n")
artifacts=["SOURCE_FIRST.md","independent_check.py","run_check.py","seal_source_first.py",
           "independent_check.stdout","independent_check.stderr","independent_check.run.json",
           "SOURCE_REGISTRY_ROWS.tsv","SOURCE_INPUT_SHA256SUMS","SOURCE_FIRST_SEAL.json"]
(here/"SOURCE_FIRST_SHA256SUMS").write_text("".join(f"{digest(here/p)}  {p}\n" for p in artifacts))
print(json.dumps(record,indent=2))
