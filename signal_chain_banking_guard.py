"""Exact conditional G416--G423 banking correspondence; not scientific proof."""
from pathlib import Path
import csv,hashlib,io,json,re,subprocess
SIGNAL_CHAIN_BANKING_IDS = tuple(f"G{i}" for i in range(416,424))
SIGNAL_CHAIN_PREFIXES = tuple((i+"\t").encode() for i in SIGNAL_CHAIN_BANKING_IDS)
SIGNAL_CHAIN_PACKAGE = "udt_signal_chain_banking_2026-09-13"
SIGNAL_CHAIN_BASE_SHA256 = "c614575c251a0e110146ae30b8c6f87d7d01862e3eab2da861b43c33537168e2"
SIGNAL_CHAIN_PINS = {'udt_signal_chain_banking_2026-09-13/WORK_ORDER.md': 'f77d7ff8f7c1fd684fd68da494491d977d2c6ccad102bcd1a5ce0297b2d6f84c', 'udt_signal_chain_banking_2026-09-13/BANKING_RECORD.md': '5e7070af6dcc549ecad8962dd0056ea7a08bb747140aa4484da26f4ba9dc2397', 'udt_signal_chain_banking_2026-09-13/BANKED_CLAIMS.json': '48d6e1233f8bc55683130eec5c2a9246c067fad0bc13368b2bcf9eb6ecd57599', 'udt_signal_chain_banking_2026-09-13/BANKED_ROWS.tsv': 'abce35323a1eaa328e224ef9305f8a59ab8b7fc1e933ca6ca660ff4c2362b163', 'udt_signal_chain_banking_2026-09-13/DISPOSITIONS.tsv': '65bfade755d0abeba7ddfb3016c9a0b94a062a8de2caf62fa0a30d9f56f14de4', 'udt_signal_chain_banking_2026-09-13/SOURCE_EVIDENCE_SHA256SUMS': '44bc5acb083274befe7e2c3df2fcdbd4103aa550447c948321f4aa380932f021', 'udt_signal_chain_banking_2026-09-13/SOURCE_MEMBERSHIP.json': '92fac2cf8856b235bfec9a65dfcef602d86462e4b6f64027866dbcd94d2f311c', 'udt_signal_chain_banking_2026-09-13/BANKING_RECORD_INITIAL.md': 'acd318302cd8e2d5c9205900c50fd226c14624b9437157e01f9aa6ef7aa21712', 'udt_signal_chain_banking_2026-09-13/ACCEPTANCE_FREEZE.json': '34e51716fb8a5552485cb4cb5b18422d5e8ddeec13d244cb9096e4940d5f61b2', 'udt_signal_chain_banking_2026-09-13/ACCEPTANCE_AMENDMENT.json': '16a3b0819fdb73ae0a2317e3f0edcfa13e92545f97870e31eb21baa9a9cc3f27', 'udt_signal_chain_banking_2026-09-13/review/REVIEW.md': '24d8f9b97f80aa8b109a77adece6f24840f6e4290e1a6915ffeec4842460e90a', 'udt_signal_chain_banking_2026-09-13/review/REVIEW_RECEIPT.json': '84b825fefc72ff9cd43ca0998fae12e3e670e6d23e027dcc06f22f8580aa4845', 'udt_signal_continuation_2026-09-13/WORK_ORDER.md': '72cdd8495380e08724949cc3b0c48297ad1696171b769dcf689b82b506685bd9'}
SIGNAL_CHAIN_ROW_SHA256 = {'G416': '778933de1014fa6e10d58bd5694211cb48623e40746636f2638739e4889044ce', 'G417': 'c77a3adb84364dc551e41a2866024dbed1c91ed7e55d9117acbde89161e46dca', 'G418': '2afdd5b6077d1b906f6def22227a006932e339571df9e76320315860c0fc8e85', 'G419': '03ca422999b331cf0f31d7ab8f4462563cc8abfc8c3c2ef39e9c6603b295fabd', 'G420': 'a362734b30cd29c62998079c30e8217f3ab5c654ba90b411b189b42871cd0d5a', 'G421': '0df0e6a4d22dbe934ebc6a8657b2762b98be720191906f530409bd0ddaf072c7', 'G422': '5710450ee76ee33c1313b83bf889d7779cfc899d361114f9644ef940d6fdfe18', 'G423': '38de6606ba354551299ab3677564a6951613d0c13f85feceeadf21c425c471e8'}
SIGNAL_CHAIN_GUARD_FILES = tuple(SIGNAL_CHAIN_PINS)
def require(ok,message):
    if not ok: raise SystemExit(message)
def without_signal_chain(raw:bytes, *, required:bool=False)->bytes:
    """Authenticate present additions on THIS snapshot; absence only historical."""
    lines=raw.splitlines(keepends=True)
    selected=[r for r in lines if r.startswith(SIGNAL_CHAIN_PREFIXES)]
    require((not selected and not required) or len(selected)==8,
            "SIGNAL current rows missing/partial/duplicate")
    if not selected: return raw
    ids=[r.split(b"\t")[0].decode() for r in selected]
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
    rows=list(csv.DictReader(io.StringIO(raw.decode()),delimiter="\t"))
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
    require(members.returncode==0 and {s.decode() for s in members.stdout.split(b"\0") if s}==actual_names,"SIGNAL exact baseline source membership failed")
