from pathlib import Path
import hashlib,json,subprocess,datetime,sys,platform
ROOT=Path.cwd(); BASE="bf1a58140ef3eaf438f18e3cc2dcd57df52d2549"
manifest=ROOT/"udt_signal_chain_banking_2026-09-13/SOURCE_EVIDENCE_SHA256SUMS"
entries=[line.split(maxsplit=1) for line in manifest.read_text().splitlines()]
paths=[p for h,p in entries]; packages=sorted({p.split("/")[0] for p in paths})
expected=subprocess.check_output(["git","ls-tree","-r","--name-only",BASE,"--",*packages],text=True).splitlines()
checks={"exact_count662":len(entries)==662,"no_duplicates":len(paths)==len(set(paths)),"sorted":paths==sorted(paths),"exact_baseline_membership":set(paths)==set(expected),"six_packages":len(packages)==6}
failures=[]
for digest,path in entries:
 data=(ROOT/path).read_bytes()
 old=subprocess.check_output(["git","show",BASE+":"+path])
 if hashlib.sha256(data).hexdigest()!=digest:failures.append({"path":path,"failure":"working_hash"})
 if hashlib.sha256(old).hexdigest()!=digest:failures.append({"path":path,"failure":"baseline_hash"})
checks["all_sources_authenticate"]=not failures
out={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"python":sys.version,"platform":platform.platform(),"baseline":BASE,"manifest_sha256":hashlib.sha256(manifest.read_bytes()).hexdigest(),"source_count":len(entries),"packages":packages,"checks":checks,"failures":failures,"verdict":"PASS" if all(checks.values()) else "FAIL"}
print(json.dumps(out,indent=2));sys.exit(0 if all(checks.values()) else 1)
