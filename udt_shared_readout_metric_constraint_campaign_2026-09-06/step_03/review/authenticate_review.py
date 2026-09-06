"""Bounded byte correspondence and replay disposition; no scientific imports."""
import hashlib
import json
import pathlib
import subprocess

repo=pathlib.Path('/home/udt-admin/udt_mass_codex')
review=pathlib.Path('/tmp/tri_step03_review.pUqgBY2V')
step=repo/'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_03'
pin='70034a6faa9264bf054eb473d5eb7a0889f3d2de'
digest=lambda b:hashlib.sha256(b).hexdigest()
records=[]
for manifest in ('CANDIDATE_SHA256SUMS','SOURCE_SHA256SUMS'):
    for row in (step/manifest).read_text().splitlines():
        want,path=row.split(None,1)
        actual=digest((repo/path).read_bytes())
        assert want==actual,(path,want,actual)
        pinned=None
        if manifest=='SOURCE_SHA256SUMS' and not path.startswith('udt_shared_readout_'):
            pinned=digest(subprocess.check_output(['git','show',pin+':'+path],cwd=repo))
            assert actual==pinned,(path,actual,pinned)
        records.append(dict(manifest=manifest,path=path,sha256=actual,pinned_source_sha256=pinned))
for row in (review/'stage_a_seal.stdout').read_text().splitlines():
    want,path=row.split(None,1)
    assert digest((review/path).read_bytes())==want,path
baseline=(review/'author_replay_baseline.stdout').read_bytes()
assert baseline==(step/'author_exact.stdout').read_bytes()
baseline_data=json.loads(baseline)
assert baseline_data['status']=='PASS' and baseline_data['guard_count']==15
disposition=json.loads((step/'MUTATION_DISPOSITION.json').read_text())
mutants=[]
for row in disposition['rows']:
    mode=row['mode']
    actual=json.loads((review/f'author_replay_{mode}.stdout').read_text())
    assert actual==row['observed']
    execution=json.loads((review/f'author_replay_{mode}.json').read_text())
    assert execution['returncode']==1 and not execution['timeout']
    assert (review/f'author_replay_{mode}.stderr').read_bytes()==b''
    mutants.append(dict(mode=mode,guard=actual['guard'],returncode=1))
method_paths=['AGENTS.md','CLAUDE.md','CROSS_MODEL_VERIFY.md',
 '.claude/skills/no-shortcuts/SKILL.md','.claude/skills/completeness-map/SKILL.md',
 '.claude/skills/verifier-before-record/SKILL.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/WORK_ORDER.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py']
print(json.dumps(dict(records=records,
 current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
 current_branch=subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip(),
 method_current_hashes={p:digest((repo/p).read_bytes()) for p in method_paths},
 candidate_files=5,source_files=9,pinned_scientific_sources=6,
 stage_a_seal_unchanged=True,author_baseline_stdout_byte_identical=True,
 replay_guard_count=baseline_data['guard_count'],mutants=mutants,
 all_pass=True),indent=2))
