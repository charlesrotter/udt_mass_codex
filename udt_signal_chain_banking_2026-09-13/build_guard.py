from pathlib import Path
import hashlib,json
p=Path('udt_signal_chain_banking_2026-09-13')
names=['WORK_ORDER.md','BANKING_RECORD.md','BANKED_CLAIMS.json','BANKED_ROWS.tsv','DISPOSITIONS.tsv','SOURCE_EVIDENCE_SHA256SUMS','SOURCE_MEMBERSHIP.json','BANKING_RECORD_INITIAL.md','ACCEPTANCE_FREEZE.json','ACCEPTANCE_AMENDMENT.json']
for n in ['review/REVIEW.md','review/REVIEW_RECEIPT.json']:
 if (p/n).is_file(): names.append(n)
pins={str(p/n):hashlib.sha256((p/n).read_bytes()).hexdigest() for n in names}
authority_work_order='udt_signal_continuation_2026-09-13/WORK_ORDER.md'
pins[authority_work_order]=hashlib.sha256(Path(authority_work_order).read_bytes()).hexdigest()
rows=(p/'BANKED_ROWS.tsv').read_bytes().splitlines(keepends=True)[1:]
rowhash={r.split(b'\t')[0].decode():hashlib.sha256(r).hexdigest() for r in rows}
s='''"""Exact conditional G416--G423 banking correspondence; not scientific proof."""
from pathlib import Path
import csv,hashlib,io,json,re,subprocess
SIGNAL_CHAIN_BANKING_IDS = tuple(f"G{i}" for i in range(416,424))
SIGNAL_CHAIN_PREFIXES = tuple((i+"\\t").encode() for i in SIGNAL_CHAIN_BANKING_IDS)
SIGNAL_CHAIN_PACKAGE = "udt_signal_chain_banking_2026-09-13"
SIGNAL_CHAIN_BASE_SHA256 = "c614575c251a0e110146ae30b8c6f87d7d01862e3eab2da861b43c33537168e2"
'''+f'SIGNAL_CHAIN_PINS = {pins!r}\nSIGNAL_CHAIN_ROW_SHA256 = {rowhash!r}\n'+'''SIGNAL_CHAIN_GUARD_FILES = tuple(SIGNAL_CHAIN_PINS)
def require(ok,message):
    if not ok: raise SystemExit(message)
def without_signal_chain(raw:bytes, *, required:bool=False)->bytes:
    """Authenticate present additions on THIS snapshot; absence only historical."""
    lines=raw.splitlines(keepends=True)
    selected=[r for r in lines if r.startswith(SIGNAL_CHAIN_PREFIXES)]
    require((not selected and not required) or len(selected)==8,
            "SIGNAL current rows missing/partial/duplicate")
    if not selected: return raw
    ids=[r.split(b"\\t")[0].decode() for r in selected]
    require(set(ids)==set(SIGNAL_CHAIN_BANKING_IDS) and len(set(ids))==8,
            "SIGNAL current rows missing/partial/duplicate")
    for ident,row in zip(ids,selected):
        require(hashlib.sha256(row).hexdigest()==SIGNAL_CHAIN_ROW_SHA256[ident],
                "SIGNAL exact row/scope changed: "+ident)
    return b"".join(r for r in lines if not r.startswith(SIGNAL_CHAIN_PREFIXES))
def validate_signal_chain_banking(root:Path, *, authenticate_sources:bool=True)->None:
    payloads={}
    for name,expected in SIGNAL_CHAIN_PINS.items():
        target=root/name
        require(target.is_file(),"SIGNAL guard file missing: "+name)
        raw=target.read_bytes()
        require(hashlib.sha256(raw).hexdigest()==expected,"SIGNAL guard file changed: "+name)
        payloads[name]=raw
    scope=json.loads(payloads[SIGNAL_CHAIN_PACKAGE+"/BANKED_CLAIMS.json"])
    raw=(root/"CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
    original=without_signal_chain(raw,required=True)
    require(hashlib.sha256(original).hexdigest()==SIGNAL_CHAIN_BASE_SHA256,
            "SIGNAL changed an original398 registry byte")
    expected=payloads[SIGNAL_CHAIN_PACKAGE+"/BANKED_ROWS.tsv"].splitlines(keepends=True)
    require(raw.splitlines(keepends=True)[:9]==expected,"SIGNAL row/header/order changed")
    rows=list(csv.DictReader(io.StringIO(raw.decode()),delimiter="\\t"))
    by_id={r["premise_id"]:r for r in rows}
    require(len(rows)==len(by_id)==406,"SIGNAL current406 count/uniqueness changed")
    admitted=set(by_id)-set(SIGNAL_CHAIN_BANKING_IDS)
    require([c["id"] for c in scope["claims"]]==list(SIGNAL_CHAIN_BANKING_IDS),"SIGNAL claim membership changed")
    for c in scope["claims"]:
        require(by_id[c["id"]]==c["claim"],"SIGNAL claim transcription changed")
        require(set(c["required_registry_ids"])<=admitted,"SIGNAL dependency closure changed")
        require(not set(c["controls_and_source_credit"])&set(c["required_registry_ids"]),"SIGNAL dependency/control conflation")
        admitted.add(c["id"])
    if not authenticate_sources: return
    authority=root/scope["authority_source"]
    require(authority.is_file() and hashlib.sha256(authority.read_bytes()).hexdigest()==scope["authority_sha256"],"SIGNAL authority source changed")
    entries=[line.split(maxsplit=1) for line in payloads[SIGNAL_CHAIN_PACKAGE+"/SOURCE_EVIDENCE_SHA256SUMS"].decode().splitlines()]
    require(len(entries)==len({name for _,name in entries})==662,"SIGNAL original source membership changed")
    membership=json.loads(payloads[SIGNAL_CHAIN_PACKAGE+"/SOURCE_MEMBERSHIP.json"])
    counts={k:0 for k in scope["source_packages"]}
    for expected_hash,name in entries:
        path=Path(name)
        require(not path.is_absolute() and ".." not in path.parts and path.parts[0] in counts and re.fullmatch(r"[0-9a-f]{64}",expected_hash) is not None,"SIGNAL unsafe source path")
        counts[path.parts[0]]+=1
        source=root/path
        require(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest()==expected_hash,"SIGNAL original source evidence changed: "+name)
    require(counts==membership["packages"],"SIGNAL source package counts changed")
    actual_names={name for _,name in entries}
    for c in scope["claims"]:
        require(set(c["controlling_members"])<=actual_names,"SIGNAL controlling source absent")
    base=scope["baseline_head"]
    frozen=subprocess.run(["git","show",base+":CURRENT_SCIENTIFIC_PREMISES.tsv"],cwd=Path(__file__).resolve().parent,capture_output=True,timeout=15,check=False)
    require(frozen.returncode==0 and frozen.stdout==original,"SIGNAL baseline registry correspondence failed")
    members=subprocess.run(["git","ls-tree","-rz","--name-only",base,"--",*scope["source_packages"]],cwd=Path(__file__).resolve().parent,capture_output=True,timeout=15,check=False)
    require(members.returncode==0 and {s.decode() for s in members.stdout.split(b"\\0") if s}==actual_names,"SIGNAL exact baseline source membership failed")
'''
Path('signal_chain_banking_guard.py').write_text(s)
