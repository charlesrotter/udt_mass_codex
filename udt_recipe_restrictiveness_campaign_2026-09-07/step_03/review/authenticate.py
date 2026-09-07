"""Read-only correspondence checks and retained execution chronology."""
import datetime
import hashlib
import json
from pathlib import Path

root=Path.cwd()
review=root/'udt_recipe_restrictiveness_campaign_2026-09-07/step_03/review'
step=review.parent
counts={}
for manifest in (step/'CANDIDATE_SHA256SUMS',step/'SOURCE_SHA256SUMS',
                 review/'STAGE_A_SHA256SUMS.stdout',review/'source_hashes.stdout'):
    lines=manifest.read_text().splitlines()
    for line in lines:
        digest,path=line.split(None,1)
        actual=hashlib.sha256((root/path).read_bytes()).hexdigest()
        assert actual==digest,(str(manifest),path,digest,actual)
    counts[str(manifest.relative_to(root))]=len(lines)
records={name:json.loads((step/(name+'.json')).read_text()) for name in
 ['author_corrected','mutant_harmonicity','mutant_fixed_phase','serial_author',
  'serial_mutant_harmonicity','serial_mutant_fixed_phase']}
def start(name):
    return datetime.datetime.fromisoformat(records[name]['started_utc']).timestamp()
overlap=start('author_corrected')+records['author_corrected']['duration_seconds']-start('mutant_harmonicity')
serial_gaps=[start(b)-start(a)-records[a]['duration_seconds'] for a,b in
 [('serial_author','serial_mutant_harmonicity'),('serial_mutant_harmonicity','serial_mutant_fixed_phase')]]
assert overlap>0 and all(gap>0 for gap in serial_gaps)
for a,b in [('author_corrected','serial_author'),('mutant_harmonicity','serial_mutant_harmonicity'),
             ('mutant_fixed_phase','serial_mutant_fixed_phase')]:
    for suffix in ('.stdout','.stderr'):
        assert (step/(a+suffix)).read_bytes()==(step/(b+suffix)).read_bytes(),(a,b,suffix)
print(json.dumps({'status':'PASS','manifest_members':counts,
 'retained_initial_capture_overlap_seconds':overlap,'corrected_serial_capture_gaps_seconds':serial_gaps,
 'three_author_serial_output_pairs':'BYTE_IDENTICAL','chronology_limit':'Capture interval overlap is not separately measured simultaneous instruction execution.'},indent=2))
