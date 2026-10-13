"""Bounded packaging correspondence; never read inherited/protected payloads."""
import datetime,hashlib,json,subprocess
from pathlib import Path

root=Path('.')
campaign='udt_goal_research_campaign_2026-10-13/'
freeze_path=campaign+'INTEGRATION_FREEZE.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=Path(freeze_path).read_bytes()
assert sha(blob)=='f11f4f2289730b27688fe93abef2f3f2dd46bcda94a8588fa132ec772cc68cf5'
f=json.loads(blob); accepted=f['accepted_sha256']
prior_bytes=Path(f['prior_review_record']).read_bytes()
assert sha(prior_bytes)==f['prior_review_record_sha256']
prior=json.loads(prior_bytes)['accepted_sha256']
changed=sorted(k for k in prior if k in accepted and prior[k]!=accepted[k])
added=sorted(set(accepted)-set(prior));removed=sorted(set(prior)-set(accepted))
assert changed==sorted(f['inherited_changed'])
assert added==sorted(f['added']) and removed==sorted(f['removed'])==[]
assert len(prior)-len(changed)==f['inherited_unchanged_count']
allowed_changed={'UDT_DEVELOPMENT.md','CURRENT_RESEARCH_PROGRAM.md','LIVE.md','HANDOFF.md','INDEX.md','MEMORY.md','UDT_RESEARCH_ROADMAP.md','development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json','development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'}
assert set(changed)==allowed_changed
assert all(k.startswith(campaign) for k in added)
checked={}
for k in changed+added:
 actual=sha(Path(k).read_bytes());assert actual==accepted[k],k
 checked[k]=actual
# Check the preserved first integration, not earlier scientific source payloads.
first_bytes=Path(f['initial_integration_freeze']).read_bytes()
assert sha(first_bytes)==f['initial_integration_freeze_sha256']=='7dee4ca228f513be62fae0abce92cdf15b887a806825ab39939a3f767d6650da'
first=json.loads(first_bytes)['accepted_sha256']
assert sorted(k for k in first if first[k]!=accepted[k])==sorted(f['changed_from_first_freeze'])
assert sorted(set(accepted)-set(first))==sorted(f['added_from_first_freeze'])
texts_bytes=Path(f['initial_text_snapshot']).read_bytes()
assert sha(texts_bytes)==f['initial_text_snapshot_sha256']
texts=json.loads(texts_bytes)
assert set(texts)==allowed_changed
assert all(sha(v.encode())==first[k] for k,v in texts.items())
baseline=json.loads(Path(campaign+'BASELINE.json').read_text())
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
assert head==baseline['head'] and branch=='grok'
names=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0')
unrelated=sorted(n for n in names if n and not n.startswith(campaign))
assert unrelated==sorted(baseline['existing_untracked_names_only'])
whitespace=subprocess.run(['git','diff','--check'],capture_output=True,text=True)
assert whitespace.returncode==0,whitespace.stdout+whitespace.stderr
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_BOUNDED_CORRESPONDENCE',freeze=freeze_path,freeze_sha256=sha(blob),accepted_count=len(accepted),inherited_unchanged_count=f['inherited_unchanged_count'],inherited_changed_count=len(changed),added_count=len(added),current_content_hashed_count=len(checked),checked_sha256=checked,initial_texts_checked=len(texts),head=head,branch=branch,unrelated_names_preserved=len(unrelated),diff_whitespace='PASS',limits='Inherited unchanged map entries compared with prior accepted map, not read/rehashed/reproved. Only nine authorized changed documents and campaign additions read for hash checks. No protected/unrelated content read. Byte identity is not substantive review, chronology, empirical validation or promotion.')
dest=Path(campaign+'review_fidelity/FINAL_BINDING_CHECK.json')
with dest.open('x') as h:json.dump(out,h,indent=2);h.write('\n')
print(json.dumps({k:v for k,v in out.items() if k!='checked_sha256'},indent=2))
