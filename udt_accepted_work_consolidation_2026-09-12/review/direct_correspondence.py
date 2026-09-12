#!/usr/bin/env python3
"""Independent frozen-synthesis correspondence audit; not a scientific proof."""
import collections
import copy
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PKG=HERE.parent
DENY=('archive/','8_25/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
def safe(p):
    assert not Path(p).is_absolute() and '..' not in Path(p).parts and not p.startswith(DENY),p
def digest(b): return hashlib.sha256(b).hexdigest()
def tsv(raw): return list(csv.DictReader(io.StringIO(raw.decode()),delimiter='\t'))
freeze=json.loads((PKG/'INITIAL_FREEZE.json').read_text())
snapshots={}
for entry in freeze['files']:
    safe(entry['original_path']);safe(entry['snapshot'])
    raw=(PKG/entry['snapshot']).read_bytes()
    assert digest(raw)==entry['sha256'] and len(raw)==entry['bytes'],entry
    assert (ROOT/entry['original_path']).read_bytes()==raw,entry['original_path']
    snapshots[Path(entry['original_path']).name]=raw
registry_raw=(ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
assert registry_raw==subprocess.check_output(['git','show',freeze['source_baseline']+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=ROOT)
registry=tsv(registry_raw)
coverage=tsv(snapshots['REGISTRY_COVERAGE.tsv'])
families=tsv(snapshots['FAMILY_MAP.tsv'])
def validate_census(cov,fam):
    assert len(cov)==len(registry)==397
    old={r['premise_id']:r for r in registry}
    new={r['premise_id']:r for r in cov}
    assert len(new)==len(cov) and set(new)==set(old)
    for k,r in new.items():
        for output,input_name in {'term':'term','epistemic_label_exact':'epistemic_label',
          'active_use_exact':'active_use','controlling_source_exact':'controlling_source'}.items():
            assert r[output]==old[k][input_name],(k,output)
        assert r['inspection_disposition'] and 'PENDING' not in r['inspection_disposition']
    assert len(fam)==len({f['family_id'] for f in fam})==22
    membership=collections.Counter()
    for f in fam:
        members=f['premise_ids'].split(';')
        assert len(members)==int(f['count'])
        assert set(members)=={k for k,r in new.items() if r['family_id']==f['family_id']}
        assert all(new[k]['family_topic']==f['topic'] for k in members)
        membership.update(members)
    assert membership==collections.Counter({k:1 for k in old})
validate_census(coverage,families)
catches=[]
for kind in ('grade','duplicate','partition'):
    c,f=copy.deepcopy(coverage),copy.deepcopy(families)
    if kind=='grade': c[0]['epistemic_label_exact']='UNAUTHORIZED_UPGRADE'
    elif kind=='duplicate': c[-1]=copy.deepcopy(c[0])
    else: f[0]['premise_ids']=f[0]['premise_ids'].replace(';'+f[0]['premise_ids'].split(';')[-1],'')
    try: validate_census(c,f)
    except AssertionError: catches.append(kind)
    else: raise AssertionError('false pass: '+kind)

ledger=tsv(snapshots['SOURCE_READ_LEDGER.tsv'])
pins=json.loads(snapshots['SOURCE_PINS.json'])
assert len(ledger)==len({x['path'] for x in ledger})==len(pins['files'])==144
assert {x['path']:x['sha256'] for x in ledger}==pins['files']
for p,h in pins['files'].items():
    safe(p)
    assert digest((ROOT/p).read_bytes())==h,p
    assert digest(subprocess.check_output(['git','show',pins['baseline']+':'+p],cwd=ROOT))==h,p
try: safe(DENY[1]+'nonexistent_never_opened')
except AssertionError: catches.append('denied_before_read')
else: raise AssertionError('unsafe path accepted')
links=set(re.findall(r'\]\(([^)]+)\)',snapshots['UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md'].decode()))
for p in links:
    safe(p);assert (ROOT/p).is_file(),p
    assert p in pins['files'] or p.startswith(PKG.name+'/') or p=='UDT_RESEARCH_ROADMAP.md',p
gaps=tsv(snapshots['GAP_AND_REUSE_MAP.tsv'])
assert len(gaps)==len({g['job_id'] for g in gaps})==13 and all(all(g.values()) for g in gaps)
for seal_name in ('SOURCE_FIRST_SEAL.json','SUPPLEMENTAL_SOURCE_SEAL.json'):
    for e in json.loads((HERE/seal_name).read_text())['files']:
        assert digest((ROOT/e['path']).read_bytes())==e['sha256'],e['path']
startup_read_paths=['AGENTS.md','CLAUDE.md','CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv']
startup_read_paths += ['.claude/skills/'+n+'/SKILL.md' for n in ('completeness-map','no-shortcuts','verifier-before-record')]
underreports=[r['path'] for r in ledger if r['path'] in startup_read_paths and r['reviewer_read_depth']=='not directly inspected in this reviewer context']
assert set(underreports)==set(startup_read_paths)
additions=[
 'udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/AUDIT_REPORT.md',
 'udt_g276_proper_clock_ce_scale_anchor_reconciliation_2026-08-26/AUDIT_REPORT.md',
 'native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md',
 'native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv',
 'udt_scientific_arc_recovery_checkpoint_2026-08-04/MASS_BRANCH_AUTHORITY_MAP.tsv',
 'udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md',
 'udt_g349_finite_null_wavefront_patch_area_2026-09-04/AUDIT_REPORT.md']
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'],cwd=ROOT,text=True)
unrelated=[s for s in status.splitlines() if s.startswith('?? ') and not s[3:].startswith((PKG.name+'/','UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md'))]
assert len(unrelated)==46 and digest(('\n'.join(unrelated)+'\n').encode())=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='grok'
result={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
 'meaning':'independent documentary correspondence, not scientific proof or suite replay',
 'frozen_files_authenticated':len(freeze['files']),'current_candidate_equals_initial':True,
 'registry_rows':len(coverage),'families':len(families),'jobs':len(gaps),'pinned_sources':len(pins['files']),
 'links':len(links),'metadata_corruptions_rejected':catches,
 'inspection_dispositions':dict(collections.Counter(r['inspection_disposition'] for r in coverage)),
 'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'parent_navigation_dirt':[s[3:] for s in status.splitlines() if not s.startswith('?? ')],
 'preserved_unrelated_untracked_names':len(unrelated),
 'documentary_objection_D1_startup_read_underreports':sorted(underreports),
 'direct_stage_source_additions':[{'path':p,'sha256':pins['files'][p],
 'read_depth':'full controlling audit or ledger; originals and scientific implementations not replayed'} for p in additions]}
with (HERE/'DIRECT_CORRESPONDENCE.json').open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('direct_stage_source_additions','python','inspection_dispositions')},indent=2))
