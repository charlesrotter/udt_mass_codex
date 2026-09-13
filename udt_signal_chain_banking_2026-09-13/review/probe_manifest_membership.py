from pathlib import Path
from unittest.mock import patch
import hashlib,json,datetime,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import signal_chain_banking_guard as g
manifest_key=g.SIGNAL_CHAIN_PACKAGE+'/SOURCE_EVIDENCE_SHA256SUMS';manifest=ROOT/manifest_key
entries=[line.split(maxsplit=1) for line in manifest.read_text().splitlines()]
scope=json.loads((ROOT/g.SIGNAL_CHAIN_PACKAGE/'BANKED_CLAIMS.json').read_text())
controls={p for c in scope['claims'] for p in c['controlling_members']}
chosen=next(i for i,(h,n) in enumerate(entries) if n not in controls)
removed=entries[chosen][1];fake_name=removed.split('/')[0]+'/FORGED_UNTRACKED_MEMBER.md';fake=ROOT/fake_name;fake_data=b'Pretend untracked same-package member; in-memory only.\n'
entries[chosen]=[hashlib.sha256(fake_data).hexdigest(),fake_name]
forged=''.join(h+'  '+n+'\n' for h,n in entries).encode()
read_original=Path.read_bytes;is_file_original=Path.is_file;reads=[]
def read(p):
 if p==manifest:return forged
 if p==fake:reads.append(str(p));return fake_data
 return read_original(p)
def is_file(p):return True if p==fake else is_file_original(p)
# Temporarily update only the expected manifest digest in memory to exercise
# the semantic Git-membership check beyond the outer immutable manifest pin.
pins={**g.SIGNAL_CHAIN_PINS,manifest_key:hashlib.sha256(forged).hexdigest()}
error=None
with patch.dict(g.SIGNAL_CHAIN_PINS,pins,clear=True),patch.object(Path,'read_bytes',read),patch.object(Path,'is_file',is_file):
 try:g.validate_signal_chain_banking(ROOT)
 except SystemExit as exc:error=str(exc)
assert error=='SIGNAL exact baseline source membership failed',error
assert len(reads)==1
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_EQUAL_COUNT_FORGED_MEMBERSHIP_REJECTED','removed':removed,'forged':fake_name,'manifest_count':len(entries),'fake_file_reads':len(reads),'rejection':error,'scope':'In-memory semantic-membership test with outer manifest hash temporarily made consistent; no physical file created and no original evidence changed.'},indent=2))
