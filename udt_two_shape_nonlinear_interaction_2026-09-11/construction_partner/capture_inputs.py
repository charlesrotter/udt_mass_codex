#!/usr/bin/env python3
"""Read only the explicitly load-bearing, unprotected inputs and print pins."""
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess

root=Path(__file__).resolve().parents[2]
rel=Path(__file__).resolve().parent.relative_to(root)
paths=['AGENTS.md','CLAUDE.md','CURRENT_SCIENTIFIC_PREMISES.tsv',
 '.claude/skills/no-shortcuts/SKILL.md','.claude/skills/completeness-map/SKILL.md',
 '.claude/skills/solution-space-not-imposition/SKILL.md','.claude/skills/verifier-before-record/SKILL.md',
 'udt_two_shape_nonlinear_interaction_2026-09-11/WORK_ORDER.md',
 'udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md',
 'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md',
 'udt_reviewed_backlog_banking_2026-09-10/capture_existing.py',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
 'udt_nonlinear_mode_realizability_campaign_2026-09-09/METHOD_REFERENCES.md']
nr='udt_nonlinear_mode_realizability_campaign_2026-09-09/'
for step in ['step_01/','step_02/']:
    paths += [nr+step+name for name in ['INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','review/ADVERSARIAL_REVIEW.md']]
paths += [nr+'step_02/'+name for name in ['DISCOVERY_HISTORY.md','review/SUMMARY_FIDELITY_REVIEW.md']]
ne='udt_nonlinear_ripple_geometry_2026-09-09/'
paths += [ne+name for name in ['INITIAL_CANDIDATE.md','review/DIRECT_REVIEW.md','review/SOURCE_FIRST.md','review/FIDELITY_REVIEW.md']]
paths += [str(rel/name) for name in ['CONSTRUCTION_FREEZE.md','raw_geometry.py','capture_inputs.py']]
rows=list(csv.DictReader((root/'CURRENT_SCIENTIFIC_PREMISES.tsv').open(),delimiter='\t'))
selected=[r for r in rows if r['premise_id'] in {'G303','G312','G324','G327','G388','G389','G394'}]
print(json.dumps({'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'first_observed_utc':'2026-09-11 04:50:31 UTC','context':'/root/two_shape_construction',
 'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'branch':subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip(),
 'status_names_only':subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','status','--short','--branch'],cwd=root,text=True),
 'python':platform.python_version(),'platform':platform.platform(),'logical_cpu_count':os.cpu_count(),
 'thread_environment':{k:os.getenv(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},
 'model_runtime':'UNATTESTED','selected_registry_rows':selected,
 'source_pins':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}},indent=2))
