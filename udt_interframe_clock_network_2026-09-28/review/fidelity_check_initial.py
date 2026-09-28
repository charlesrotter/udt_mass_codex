"""Final lightweight correspondence/regression check; not a scientific replay."""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[2]
PKG=pathlib.Path(__file__).resolve().parents[1]
MAINTAINED={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','MEMORY.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
sys.path.insert(0,str(ROOT))
from verify_current_scientific_premises import validate_startup_surface


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def check_hash(base,path,expected):
    if hashlib.sha256((base/path).read_bytes()).hexdigest()!=expected:
        raise RuntimeError('hash mismatch: '+str(path))


launch=json.loads((PKG/'LAUNCH.json').read_text())
assert git('branch','--show-current')=='grok'
assert git('rev-parse','HEAD')==git('rev-parse','origin/grok')==launch['head']
changed=set(git('diff','--name-only').splitlines())
assert changed==MAINTAINED,changed
assert git('diff','--cached','--name-only')==''
assert git('diff','--check')==''
for path,h in launch['source_pins'].items():
    if path not in MAINTAINED:
        check_hash(ROOT,path,h)
freeze=json.loads((PKG/'CANDIDATE_FREEZE.json').read_text())
for path,h in freeze['candidate_and_checks'].items():
    check_hash(PKG,path,h)
for name,base in [('SOURCE_FIRST_SEAL.json',PKG/'review'),
                  ('DIRECT_CHECKS_SEAL.json',PKG/'review'),
                  ('DIRECT_REVIEW_SEAL.json',PKG)]:
    for path,h in json.loads((PKG/'review'/name).read_text())['sha256'].items():
        check_hash(base,path,h)
u=set(git('ls-files','--others','--exclude-standard').splitlines())
assert {p for p in u if not p.startswith(PKG.name+'/')}==set(launch['prior_untracked_paths'])
validate_startup_surface(ROOT)
runs={}
for name,expected in [('premise_audit',0),('startup_surface',0),('preservation',0),('network',1),('network_repaired',0)]:
    record=json.loads((PKG/'checks'/(name+'.json')).read_text())
    assert record['returncode']==expected and not record['timeout'],name
    out=(PKG/'checks'/(name+'.stdout')).read_text()
    err=(PKG/'checks'/(name+'.stderr')).read_text()
    if expected==0:
        assert 'PASS' in out and err=='',name
    else:
        assert 'AssertionError' in err and 'Matrix' in err,name
    runs[name]={k:record[k] for k in ['returncode','duration_seconds','maxrss_kib']}
assert '406-row premise registry' in (PKG/'checks/premise_audit.stdout').read_text()
size=sum(p.stat().st_size for p in PKG.rglob('*') if p.is_file())
assert size<2*1024**2,size
print(json.dumps({'status':'PASS','scope':'final byte correspondence and same-code startup regression only',
                  'head':launch['head'],'maintained':sorted(changed),'prior_untracked_paths':len(launch['prior_untracked_paths']),
                  'source_and_candidate_hashes':'match','review_seals':'match','startup_guard':'PASS',
                  'protected_payload_reads':False,'runs':runs,'package_bytes_before_final_report':size},indent=2))
