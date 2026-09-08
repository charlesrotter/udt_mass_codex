"""Final read-only correspondence check; no source audit or Git mutation."""
import hashlib
import json
from pathlib import Path
import subprocess

root=Path('/home/udt-admin/udt_mass_codex')
r=Path(__file__).resolve().parent
p=r.parent
checks=[]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def check(name,ok):
    assert ok,name
    checks.append(name)
auth=json.loads((r/'source_authentication.stdout').read_text())
for path,digest in auth['sha256'].items():check('source_unchanged_'+path,sha(root/path)==digest)
candidate=json.loads((r/'candidate_comparison_run.stdout').read_text())
for path,digest in candidate['candidate_sha256'].items():
    check('candidate_unchanged_'+path,sha(p/path)==digest)
    check('candidate_snapshot_'+path,sha(r/'candidate_snapshots'/path)==digest)
seal=json.loads((r/'SOURCE_FIRST_SEAL.json').read_text())
for entry in seal['files']:check('source_seal_'+entry['path'],sha(r/entry['path'])==entry['sha256'])
check('seal_unchanged',sha(r/'SOURCE_FIRST_SEAL.json')=='e660419a384249f59e191c268674c3274d5aa96b4b5296dce4a52767abe86629')
captures=[]
for name in ['source_first_run','source_authentication','spacetime_independent_run',
             'author_regression','author_mutations_replay','candidate_comparison_run','additional_mutations_run']:
    rec=json.loads((r/(name+'.json')).read_text())
    check('captured_success_'+name,rec['returncode']==0 and not rec['timeout'])
    check('captured_limits_'+name,rec['address_space_bytes']==536870912 and rec['cpu_seconds']==60 and rec['duration_seconds']<60)
    check('captured_stderr_'+name,(r/(name+'.stderr')).read_bytes()==b'')
    captures.append(dict(name=name,**rec))
mut=json.loads((r/'additional_mutations_run.stdout').read_text())
for result in mut['results']:
    check('actual_mutant_saved_'+result['name'],sha(r/result['mutant_path'])==result['mutant_sha256'])
check('mutation_disposition',mut['author_rejections']==6 and mut['author_false_passes_independently_detected']==2)
for ref in ['HEAD','origin/grok']:
    proc=subprocess.run(['git','rev-parse',ref],cwd=root,capture_output=True,check=True)
    check('git_'+ref,proc.stdout.decode().strip()=='8593f11cd96a575be3513d1ec56e92ac4f5811ff')
result=dict(status='PASS',check_count=len(checks),checks=checks,captures=captures,
            review_report_sha256=sha(r/'REVIEW_REPORT.md'),
            review_scope_sha256=sha(r/'REVIEW_SCOPE.md'),
            maximum_exact_child_seconds=max(v['duration_seconds'] for v in captures),
            maximum_exact_child_RSS_KiB=max(v['maxrss_kib'] for v in captures),
            caveat='correspondence only; no remote sync, full358 replay, scientific promotion or independent proof of protected-file preservation')
print(json.dumps(result,indent=2,sort_keys=True))
