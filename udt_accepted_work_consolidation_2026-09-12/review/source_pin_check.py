#!/usr/bin/env python3
"""One-shot documentary correspondence record, not a scientific verifier."""
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = 'ab6033469c37f63a0f3aa6527804b7e3cd2f5be6'
paths = []
def add(path, depth='full argument/source prose'):
    paths.append((path, depth))

for p in ('udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md',
          'startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md'):
    add(p, 'full current authority/adoption')
for p in (
    'udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30',
    'udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31',
    'udt_g311_universal_reciprocity_full_covariant_response_2026-09-01',
    'udt_g312_quiet_gr_response_constitution_discriminator_2026-09-01',
    'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01',
    'udt_g314_global_admissibility_actualization_type_classification_2026-09-01'):
    add(p+'/AUDIT_REPORT.md', 'full audit report; original executable suites not repeated')
    add(p+'/EXACT_DERIVATION.md')
for p in (
    'udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18',
    'udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19',
    'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05',
    'udt_g352_clock_rate_carried_measure_readout_2026-09-05'):
    add(p+'/AUDIT_REPORT.md', 'full controlling audit report; earlier full derivation/reviews not reopened')
for p in (
    'udt_native_response_discrimination_2026-09-09/step_01',
    'udt_native_response_discrimination_2026-09-09/step_02',
    'udt_gr_limit_campaign_2026-09-10/step_01',
    'udt_gr_limit_campaign_2026-09-10/step_02',
    'udt_response_foundations_campaign_2026-09-10'):
    add(p+'/CANDIDATE.md')
    add(p+'/review/DIRECT_REVIEW.md', 'full controlling substantive review')
for p in (
    'udt_two_shape_nonlinear_interaction_2026-09-11',
    'udt_two_shape_evolution_2026-09-11',
    'udt_exact_metric_kernel_expansion_2026-09-10'):
    add(p+'/INITIAL_CANDIDATE.md')
    add(p+'/review/REVIEW.md', 'controlling substantive review; TI2 opening155 lines reread after aggregate truncation; TI1 final omitted-check tail partially truncated')
for p in ('udt_ti1_banking_2026-09-11/BANKING_RECORD.md',
          'udt_ti2_banking_2026-09-11/BANKING_RECORD.md'):
    add(p, 'full exact acceptance overlay')
for p in ('INITIAL_CANDIDATE.md','REPAIR.md','DIRECT_REVIEW.md'):
    add('udt_null_clock_depth_integrability_assessment_2026-09-10/'+p)
add('udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md', 'acceptance/dependency/limits prose; aggregate read partly truncated')
add('udt_reviewed_backlog_banking_2026-09-10/BANKED_CLAIMS.json', 'targeted ND1/ND2/GL1/GL2/RF1/NCI1/ER1 acceptance and source pins; no all-claim read')

protected = ('archive/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
records = []
for p,depth in paths:
    assert not p.startswith(protected), p
    raw=(ROOT/p).read_bytes()
    baseline=subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
    assert raw==baseline, p+' differs from assigned baseline'
    records.append({'path':p,'sha256':hashlib.sha256(raw).hexdigest(),'read_depth':depth})

claims=json.loads((ROOT/'udt_reviewed_backlog_banking_2026-09-10/BANKED_CLAIMS.json').read_text())['claims']
selected={'ND1','ND2','GL1','GL2','RF1','NCI1','ER1'}
known={x['path']:x['sha256'] for x in records}
accepted=[]
def walk(x):
    if isinstance(x,dict):
        if x.get('path') in known and 'sha256' in x:
            assert known[x['path']]==x['sha256'], x['path']
            accepted.append(x['path'])
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
for x in claims:
    if x['id'] in selected: walk(x['source_assessment'])
assert known['udt_two_shape_nonlinear_interaction_2026-09-11/INITIAL_CANDIDATE.md']=='d2e4bd56154091e46cc89c9dc3dec227ff3662d11b045309e004b358bb45c85f'
assert known['udt_two_shape_evolution_2026-09-11/INITIAL_CANDIDATE.md']=='1d9b24c359636dd212f684b45793f2f02cfa8959df0e8a8dc0c19bcb5c8ae0a9'
ids={'G166','G176','G301','G310','G311','G312','G313','G314','G351','G352','G395','G396','G397','G398','G399','G400','G401','G402','G405','G413','G414'}
registry=(ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
rows=list(csv.DictReader(io.StringIO(registry.decode()),delimiter='\t'))
chosen=[x for x in rows if x['premise_id'] in ids]
assert len(rows)==397 and len(chosen)==len(ids)
assert registry==subprocess.check_output(['git','show',BASE+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=ROOT)
receipt={'kind':'documentary correspondence only; not source scientific replay',
 'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
 'assigned_baseline':BASE,'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'sources':records,'accepted_source_pin_matches':sorted(set(accepted)),
 'registry_count_metadata':len(rows),'registry_sha256':hashlib.sha256(registry).hexdigest(),
 'selected_rows':chosen,'parent_full397':'PENDING_RECEIPT; not inferred from row count or this check'}
with (OUT/'SOURCE_FIRST_PINS.json').open('x') as f:
    json.dump(receipt,f,indent=2);f.write('\n')
with (OUT/'SOURCE_READ_DEPTH.tsv').open('x') as f:
    w=csv.DictWriter(f,fieldnames=['path','sha256','read_depth'],delimiter='\t');w.writeheader();w.writerows(records)
print(json.dumps({'correspondence':'PASS','scientific_replay':False,'source_files':len(records),
 'selected_acceptance_pin_matches':len(set(accepted)),'registry_count_metadata':len(rows),
 'selected_rows':len(chosen),'parent_full397':'PENDING_RECEIPT'},sort_keys=True))
