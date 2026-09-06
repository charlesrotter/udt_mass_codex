#!/usr/bin/env python3
"""Read-only, pinned documentation/archive correspondence; no science replay."""
import hashlib,json,pathlib,subprocess,sys
repo=pathlib.Path('/home/udt-admin/udt_mass_codex')
original=pathlib.Path('/tmp/udt-content-step02-review-fJvt8Q')
prefix='udt_g351_g352_content_bridge_campaign_2026-09-06'
arch=repo/prefix/'step_02/review'
pin='c5d537b24cd52f74cb7e4ed30cbb1d7c4385f683'
def git(*args):
    p=subprocess.run(['git',*args],cwd=repo,capture_output=True,timeout=60)
    assert p.returncode==0,(args,p.returncode,p.stderr.decode())
    return p.stdout
def sha(b): return hashlib.sha256(b).hexdigest()
listed=(original/'ARCHIVE_FILES.txt').read_text().splitlines()
def names(path):
    return sorted(str(p.relative_to(path)) for p in path.rglob('*') if p.is_file())
assert len(listed)==len(set(listed))==65
assert names(original)==sorted(listed)
assert names(arch)==sorted(listed)
gitnames=git('ls-tree','-r','--name-only',pin,'--',prefix+'/step_02/review').decode().splitlines()
assert sorted(p.removeprefix(prefix+'/step_02/review/') for p in gitnames)==sorted(listed)
comparisons=[]
for name in listed:
    source=(original/name).read_bytes()
    target=(arch/name).read_bytes()
    pinned=git('show',pin+':'+prefix+'/step_02/review/'+name)
    assert source==target==pinned,name
    comparisons.append({'path':name,'sha256':sha(source),'bytes':len(source),
                        'original_current_archive_pinned_git_identical':True})
manifest=(original/'REVIEW_SHA256SUMS').read_text().splitlines()
assert len(manifest)==64
for row in manifest:
    expected,name=row.split('  ',1)
    assert sha((original/name).read_bytes())==expected
    assert sha((arch/name).read_bytes())==expected

record_path=prefix+'/step_02/REVIEW_RECORD.md'
record=git('show',pin+':'+record_path)
assert record==(repo/record_path).read_bytes()
log_path=prefix+'/CAMPAIGN_LOG.md'
log=git('show',pin+':'+log_path).decode()
current=(repo/log_path).read_text()
def step2_excerpt(text):
    lines=text.splitlines(); row=[line for line in lines if line.startswith('| 2 |')]
    start=next(i for i,line in enumerate(lines) if line.startswith('Step2 direct review'))
    end=next((i for i in range(start+1,len(lines)) if lines[i].startswith('Step3')),len(lines))
    return '\n'.join(row+lines[start:end])+'\n'
excerpt=step2_excerpt(log)
assert excerpt==step2_excerpt(current)
assert sha((arch/'STAGE_B_ADVERSARIAL_REVIEW.md').read_bytes())=='c151956601b855a3d7295ee51a97d4b4435d84f65954ccbc7e1c02eb0174f097'
print(json.dumps({'status':'PASS_DOCUMENTATION_AND_ARCHIVE_CORRESPONDENCE',
 'reviewed_pin':pin,'actual_HEAD':git('rev-parse','HEAD').decode().strip(),
 'python':sys.version.split()[0],
 'archived_files':65,'payload_hashes':64,
 'all_three_way_byte_comparisons':comparisons,
 'review_record_sha256':sha(record),'review_record_current_matches_pin':True,
 'pinned_campaign_log_sha256':sha(log.encode()),
 'step2_excerpt_sha256':sha(excerpt.encode()),
 'step2_excerpt_current_matches_pin':True,'reviewed_step2_excerpt':excerpt,
 'whole_current_log_matches_pin':current==log,
 'step3_evaluated':False,'science_replayed':False,'original_and_repo_write_operations':False},indent=2))
