#!/usr/bin/env python3
"""Focused final documentary check, reusing the reviewed census helper only."""
import ast
import collections
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PKG=HERE.parent
DENY=('archive/','8_25/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
 'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
original=(HERE/'direct_correspondence.py').read_text()
assert hashlib.sha256(original.encode()).hexdigest()=='6625bda60bcd180aab5bd7c3c88732bd082a4e9b937c0f4db9d702b41a0db058'
old="        assert all(new[k]['family_topic']==f['topic'] for k in members)"
assert original.count(old)==1
tree=ast.parse(original.replace(old,"        assert len({new[k]['family_topic'] for k in members})==1"))
selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('safe','digest','tsv','validate_census')]
assert len(selected)==4
exec(compile(ast.Module(body=selected,type_ignores=[]),str(HERE/'direct_correspondence.py'),'exec'))

freeze=json.loads((PKG/'CORRECTED_REVIEW_FREEZE.json').read_text())
assert len(freeze['files'])==19
for p,h in freeze['files'].items():
    safe(p);assert digest((ROOT/p).read_bytes())==h,p
initial=json.loads((PKG/'INITIAL_FREEZE.json').read_text())
assert digest((PKG/'INITIAL_FREEZE.json').read_bytes())==freeze['initial_freeze_sha256']
for e in initial['files']:
    assert digest((PKG/e['snapshot']).read_bytes())==e['sha256'],e['snapshot']
for name in ('SOURCE_FIRST_SEAL.json','SUPPLEMENTAL_SOURCE_SEAL.json','DIRECT_REVIEW_SEAL.json'):
    for e in json.loads((HERE/name).read_text())['files']:
        assert digest((ROOT/e['path']).read_bytes())==e['sha256'],e['path']
registry_raw=(ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
registry=tsv(registry_raw)
assert registry_raw==subprocess.check_output(['git','show',initial['source_baseline']+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=ROOT)
coverage=tsv((PKG/'REGISTRY_COVERAGE.tsv').read_bytes())
families=tsv((PKG/'FAMILY_MAP.tsv').read_bytes())
validate_census(coverage,families)
pins=json.loads((PKG/'SOURCE_PINS.json').read_text())
ledger=tsv((PKG/'SOURCE_READ_LEDGER.tsv').read_bytes())
assert len(ledger)==len({r['path'] for r in ledger})==len(pins['files'])==147
assert {r['path']:r['sha256'] for r in ledger}==pins['files']
for p,h in pins['files'].items():
    safe(p);assert digest((ROOT/p).read_bytes())==h,p
    assert digest(subprocess.check_output(['git','show',pins['baseline']+':'+p],cwd=ROOT))==h,p
startup={'AGENTS.md','CLAUDE.md','CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv'}
startup|={'.claude/skills/'+n+'/SKILL.md' for n in ('completeness-map','no-shortcuts','verifier-before-record')}
by_path={r['path']:r for r in ledger}
assert all('attribution: review/SOURCE_FIRST_ASSESSMENT.md' in by_path[p]['reviewer_read_depth'] for p in startup)
assert all('not directly inspected in this reviewer context' not in r['reviewer_read_depth'] for r in ledger)
direct=json.loads((HERE/'DIRECT_REVIEW_SEAL.json').read_text())['direct_stage_source_additions']
assert all(by_path[e['path']]['sha256']==e['sha256'] and 'direct stage:' in by_path[e['path']]['reviewer_read_depth'] for e in direct)
gaps=tsv((PKG/'GAP_AND_REUSE_MAP.tsv').read_bytes())
assert len(gaps)==len({g['job_id'] for g in gaps})==13 and all(all(g.values()) for g in gaps)
account=(ROOT/'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md').read_text()
links=set(re.findall(r'\]\(([^)]+)\)',account))
for p in links:
    safe(p);assert (ROOT/p).is_file(),p
    assert p in pins['files'] or p.startswith(PKG.name+'/') or p=='UDT_RESEARCH_ROADMAP.md',p
assert len(links)==70
navigation=['CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','MEMORY.md','UDT_RESEARCH_ROADMAP.md']
actual_diff=subprocess.check_output(['git','diff','--']+navigation,cwd=ROOT)
assert actual_diff==(PKG/'checks/navigation_review.diff').read_bytes()
assert sorted(subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines())==navigation
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'],cwd=ROOT,text=True)
unrelated=[s for s in status.splitlines() if s.startswith('?? ') and not s[3:].startswith((PKG.name+'/','UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md'))]
assert len(unrelated)==46 and digest(('\n'.join(unrelated)+'\n').encode())=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
remote=subprocess.check_output(['git','rev-parse','origin/grok'],cwd=ROOT,text=True).strip()
assert head==remote==initial['source_baseline']
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='grok'
for stem in ('corrected_correspondence','navigation_final'):
    r=json.loads((PKG/'checks'/f'{stem}.json').read_text())
    assert r['returncode']==0 and r['timeout'] is False
    assert (PKG/'checks'/f'{stem}.stderr').read_bytes()==b''
assert '359 passed, 1 deselected' in (PKG/'checks/navigation_final.stdout').read_text()
result={'utc':datetime.now(timezone.utc).isoformat(),'meaning':'final byte/census/provenance correspondence only',
 'corrected_frozen_files':19,'initial_snapshots_unchanged':7,'earlier_reviewer_seals_unchanged':3,
 'registry_rows':397,'families':22,'jobs':13,'sources':147,'links':70,
 'startup_exposure_corrections':7,'direct_source_reads_correctly_imported':10,
 'dispositions':dict(collections.Counter(r['inspection_disposition'] for r in coverage)),
 'navigation_diff_matches':navigation,'head':head,'origin_grok':remote,'unrelated_names_preserved':46,
 'parent_navigation':'INSPECTED_PASS_359_1_DESELECTED; attributed execution; not rerun',
 'parent_current_fetch':'attributed checks/preintegration_sync.json; current refs independently match',
 'publication':'NOT_PERFORMED_OR_APPROVED_AS_COMPLETED_BY_THIS_CHECK',
 'new_scientific_runs':0}
with (HERE/'FINAL_CORRESPONDENCE.json').open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
