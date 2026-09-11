# Shell command record

Working directory throughout: `/home/udt-admin/udt_mass_codex`. These navigation
commands are transcribed from the tool calls; their original stdout was tool-only.
Captured subprocess argv, timestamps and streams are authoritative in each
capture's `.json`, `.stdout`, `.stderr`, `.capture_provenance.json`. Clock reads,
parent messages and apply_patch edits are tool actions rather than shell commands.
No shell command below writes outside construction_partner/.

Initial reads, in execution order (the two NR read blocks were independent calls
batched together; neither performed a scientific computation):

```bash
pwd && git status --short --branch && git rev-parse HEAD && cat AGENTS.md && cat udt_two_shape_nonlinear_interaction_2026-09-11/WORK_ORDER.md
rg -n '^#{1,3} |DRIVER TRIGGERS|repo discipline' CLAUDE.md && rg -n 'NR1|NR2|NE1|G388|G389|G394' udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md && rg --files udt_nonlinear_mode_realizability_campaign_2026-09-09/step_01 udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02 udt_nonlinear_ripple_geometry_2026-09-09 .claude/skills
sed -n '9,83p' CLAUDE.md && sed -n '121,134p' CLAUDE.md && cat udt_reviewed_backlog_banking_2026-09-10/capture_existing.py
cat .claude/skills/no-shortcuts/SKILL.md .claude/skills/completeness-map/SKILL.md .claude/skills/solution-space-not-imposition/SKILL.md .claude/skills/verifier-before-record/SKILL.md && cat udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md && cat udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md
cat udt_nonlinear_mode_realizability_campaign_2026-09-09/step_01/INITIAL_CANDIDATE.md udt_nonlinear_mode_realizability_campaign_2026-09-09/step_01/review/ADVERSARIAL_REVIEW.md udt_nonlinear_mode_realizability_campaign_2026-09-09/step_01/REVIEWED_RESULT.md
cat udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/INITIAL_CANDIDATE.md udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/review/ADVERSARIAL_REVIEW.md udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/review/SUMMARY_FIDELITY_REVIEW.md udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/REVIEWED_RESULT.md udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/DISCOVERY_HISTORY.md
cat udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/INITIAL_CANDIDATE.md && sed -n '1,115p' udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/review/ADVERSARIAL_REVIEW.md
cat udt_nonlinear_ripple_geometry_2026-09-09/INITIAL_CANDIDATE.md && cat udt_nonlinear_ripple_geometry_2026-09-09/review/DIRECT_REVIEW.md
cat udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py && cat udt_nonlinear_ripple_geometry_2026-09-09/review/SOURCE_FIRST.md && cat udt_nonlinear_ripple_geometry_2026-09-09/review/FIDELITY_REVIEW.md && rg -n 'G324|G327|METHOD_REFERENCES|pde2|CK' udt_nonlinear_mode_realizability_campaign_2026-09-09/SOURCE_PINS.tsv udt_nonlinear_mode_realizability_campaign_2026-09-09/METHOD_REFERENCES.md udt_reviewed_backlog_banking_2026-09-10/SOURCE_EVIDENCE_SHA256SUMS
```

The last command returned exit 2 because the guessed SOURCE_PINS.tsv did not
exist; its other reads succeeded. No scientific computation was attempted.

```bash
python3 - <<'PY'
import csv
from pathlib import Path
rows=list(csv.DictReader(Path('CURRENT_SCIENTIFIC_PREMISES.tsv').open(),delimiter='\t'))
print('columns',list(rows[0]))
for row in rows:
    if next(iter(row.values())) in {'G303','G312','G324','G327','G388','G389','G394'}:
        print(row)
PY
cat udt_nonlinear_mode_realizability_campaign_2026-09-09/METHOD_REFERENCES.md
```

Initial capture attempt (the second command after && did not execute because the
first failed; no raw_geometry_initial output existed until the later successful
attempt). Full commands are literal, including absolute stems:

```bash
python3 udt_reviewed_backlog_banking_2026-09-10/capture_existing.py /home/udt-admin/udt_mass_codex/udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/inputs 30 256 python3 udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/capture_inputs.py && python3 udt_reviewed_backlog_banking_2026-09-10/capture_existing.py /home/udt-admin/udt_mass_codex/udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/raw_geometry_initial 180 2048 python3 udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/raw_geometry.py
cat udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/inputs.stderr && cat udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/inputs.stdout
cp udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/capture_inputs.py udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/capture_inputs_initial.py
```

An apply_patch then changed only the metadata script's git-status argv to the
serial-index form recorded in SESSION_RECORD. No runtime configuration changed.

```bash
python3 udt_reviewed_backlog_banking_2026-09-10/capture_existing.py /home/udt-admin/udt_mass_codex/udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/inputs_serial 30 256 python3 udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/capture_inputs.py && python3 udt_reviewed_backlog_banking_2026-09-10/capture_existing.py /home/udt-admin/udt_mass_codex/udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/raw_geometry_initial 180 2048 python3 udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/raw_geometry.py
python3 - <<'PY'
import json
from pathlib import Path
p=Path('udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/raw_geometry_initial.stdout')
d=json.loads(p.read_text())
print(json.dumps({k:d[k] for k in ['status','python','sympy','checks']},indent=2))
print(json.dumps(d['observations']['family'],indent=2))
print(json.dumps({k:d['observations']['curvature'][k] for k in ['E_before_completion','E_completed_form','B','J','C_contract_starC']},indent=2))
PY
python3 udt_reviewed_backlog_banking_2026-09-10/capture_existing.py /home/udt-admin/udt_mass_codex/udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/mutant_omit_axial 180 2048 python3 udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/raw_geometry.py --mutant omit_axial_completion
python3 udt_reviewed_backlog_banking_2026-09-10/capture_existing.py /home/udt-admin/udt_mass_codex/udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/mutant_freeze_second_time 180 2048 python3 udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/raw_geometry.py --mutant freeze_second_time
cat udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/mutant_omit_axial.stderr && cat udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/mutant_freeze_second_time.stderr
```

Late source-scope and banking-pin reads, after writing the scientific result:

```bash
python3 - <<'PY'
import json
from pathlib import Path
obj=json.loads(Path('udt_reviewed_backlog_banking_2026-09-10/BANKED_CLAIMS.json').read_text())
print(type(obj).__name__)
if isinstance(obj,dict):
 print('top-level keys',list(obj))
 for k,v in obj.items():
  if k in {'G388','G389','G394'}: print(json.dumps({k:v},indent=2))
  elif isinstance(v,list):
   for row in v:
    if isinstance(row,dict) and any(row.get(kk) in {'G388','G389','G394'} for kk in ['id','premise_id','registry_id']): print(json.dumps(row,indent=2))
PY
cat udt_nonlinear_mode_realizability_campaign_2026-09-09/step_01/review/STAGE_A_INDEPENDENT.md udt_nonlinear_mode_realizability_campaign_2026-09-09/step_02/review/STAGE_A_INDEPENDENT.md udt_nonlinear_ripple_geometry_2026-09-09/REVIEWED_RESULT.md
```

Final correspondence command is recorded in closeout.json after execution:

```bash
python3 udt_reviewed_backlog_banking_2026-09-10/capture_existing.py /home/udt-admin/udt_mass_codex/udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/closeout 30 256 python3 udt_two_shape_nonlinear_interaction_2026-09-11/construction_partner/closeout.py
```
