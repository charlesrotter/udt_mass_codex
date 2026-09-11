"""TI3 read-only correspondence and publication scope; not scientific verification."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

root=Path(__file__).resolve().parents[1]
package=Path(__file__).resolve().parent
baseline='6b09b8caab189291a6ffc1956dea304bbe6da7cb'
navigation=['CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','UDT_RESEARCH_ROADMAP.md']
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git',*args],cwd=root,text=True)
assert git('branch','--show-current').strip()=='grok'
assert git('rev-parse','HEAD').strip()==baseline
assert git('rev-parse','origin/grok').strip()==baseline
assert sorted(git('diff','--name-only').splitlines())==navigation
assert not git('diff','--cached','--name-only').strip()
pins_checked={}
for name,base,key in [('SOURCE_PINS.json',root,'sources'),
                      ('CANDIDATE_FREEZE.json',package,'files')]:
    pins=json.loads((package/name).read_text())[key]
    for path,digest in pins.items():
        assert sha(base/path)==digest,(name,path)
    pins_checked[name]=len(pins)
for source,expected in [('udt_ti1_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS',103),
                        ('udt_ti2_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS',120)]:
    lines=(root/source).read_text().splitlines()
    assert len(lines)==expected
    for line in lines:
        digest,path=line.split(None,1)
        assert sha(root/path.strip())==digest,path
    pins_checked[source]=len(lines)
registry=(root/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
assert registry==subprocess.check_output(['git','show',baseline+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=root)
status=git('status','--porcelain=v1','--untracked-files=normal')
unrelated=''.join(line+'\n' for line in status.splitlines()
                  if line.startswith('?? ') and not line.endswith(package.name+'/'))
fingerprint=hashlib.sha256(unrelated.encode()).hexdigest()
assert fingerprint=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
assert len(unrelated.splitlines())==46
print(json.dumps({'verdict':'PASS','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'branch':'grok','HEAD':baseline,'local_origin_grok':baseline,'pins_checked':pins_checked,
 'registry397_byte_identical':True,'exact_tracked_changes':navigation,
 'original46_status_sha256':fingerprint,'protected_payloads':'not inspected; names/status only',
 'backup_completeness':'UNVERIFIED','pre_reboot_unsaved_state':'UNVERIFIED',
 'new_science':'TI3_CONDITIONAL_UNPROMOTED','publication':'future; not inferred from this check'},indent=2))
