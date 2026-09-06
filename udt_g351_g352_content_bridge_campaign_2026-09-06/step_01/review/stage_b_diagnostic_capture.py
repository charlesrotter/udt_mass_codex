import argparse,datetime,hashlib,json,resource,subprocess,sys,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True)
args=ap.parse_args();out=Path(__file__).resolve().parent
prefix="udt_g351_g352_content_bridge_campaign_2026-09-06/step_01/"
def limits():
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))
records=[]
for name,command,expected in [
 ("stage_b_parser_diff",["diff","-u",prefix+"diagnostics/INITIAL_check_query_completions.py",prefix+"check_query_completions.py"],1),
 ("stage_b_parser_equivalence",[sys.executable,"-B",str(out/"stage_b_parser_check.py")],0)]:
    tick=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    r=subprocess.run(command,cwd=args.repo,capture_output=True,timeout=60,preexec_fn=limits)
    for suffix,data in [("stdout",r.stdout),("stderr",r.stderr)]:
        target=out/(name+"."+suffix);assert not target.exists();target.write_bytes(data)
    records.append({"command":command,"cwd":str(args.repo),"start_utc":start,
     "duration_seconds":time.monotonic()-tick,"child_exit":r.returncode,"expected_exit":expected,
     "stdout_sha256":hashlib.sha256(r.stdout).hexdigest(),"stderr_sha256":hashlib.sha256(r.stderr).hexdigest()})
    assert r.returncode==expected
target=out/"STAGE_B_PARSER_DIAGNOSTIC.json";assert not target.exists()
target.write_text(json.dumps({"status":"PASS","records":records},indent=2)+"\n")
print(target.read_text())
