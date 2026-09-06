"""Portable evidence runner; only --review-root receives generated files."""
import argparse, datetime, hashlib, json, resource, subprocess, sys, time
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--repo",type=Path,required=True)
ap.add_argument("--review-root",type=Path,default=Path(__file__).resolve().parent)
args=ap.parse_args(); repo=args.repo.resolve(); out=args.review_root.resolve()
prefix="udt_g351_g352_content_bridge_campaign_2026-09-06/step_01/"
records=[]
def limits():
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))
def run(name,command,expected=0,guard=None,cwd=repo):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); tick=time.monotonic()
    p=subprocess.run(command,cwd=cwd,capture_output=True,timeout=60,preexec_fn=limits)
    for suffix,payload in [("stdout",p.stdout),("stderr",p.stderr)]:
        target=out/(name+"."+suffix)
        assert not target.exists(),"preserve existing evidence; choose a fresh output directory"
        target.write_bytes(payload)
    record={"name":name,"command":list(map(str,command)),"cwd":str(cwd),"start_utc":start,
            "duration_seconds":time.monotonic()-tick,"child_exit":p.returncode,
            "expected_exit":expected,"expected_guard":guard,
            "stdout_sha256":hashlib.sha256(p.stdout).hexdigest(),
            "stderr_sha256":hashlib.sha256(p.stderr).hexdigest()}
    records.append(record)
    assert p.returncode==expected,record
    if guard: assert ("AssertionError: "+guard).encode() in p.stderr,record
    return p.stdout

run("stage_b_candidate_auth",["sha256sum","--check",prefix+"FROZEN_CANDIDATE_SHA256SUMS"])
run("stage_b_source_auth",["sha256sum","--check",prefix+"SOURCE_SHA256SUMS"])
run("stage_b_stage_a_auth",["sha256sum","--check","STAGE_A_SHA256SUMS"],cwd=Path(__file__).resolve().parent)
run("stage_b_frozen_diff",["git","diff","--exit-code","b5963bd6c1441a7ef55292072c3ada01c99cf9e2","--",prefix])
run("stage_b_independent",[sys.executable,"-B",str(Path(__file__).resolve().parent/"stage_b_independent_witnesses.py"),"--repo",str(repo)])
baseline=run("stage_b_author_baseline",[sys.executable,"-B",prefix+"check_query_completions.py"])
assert baseline==(repo/prefix/"AUTHOR_RESULT.json").read_bytes()
mutants={"erase_weight":"total_amount_1","phase_blind":"phase_dependence_detected",
"observer_weighted_mu":"current_readout_match_0_4","gauge_rebuild_mu":"fixed_measure_gauge_0_2",
"coordinate_area_identity":"intrinsic_metric_cut_area"}
for name,guard in mutants.items():
    run("stage_b_"+name,[sys.executable,"-B",prefix+"check_query_completions.py","--mutation",name],1,guard)
result={"status":"PASS","python":sys.version,"records":records,"baseline_byte_identical":True,
"target_memory_bytes":512*1024**2,"child_timeout_seconds":60,
"max_child_rss_kib":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
target=out/"STAGE_B_REPLAY_RESULTS.json"; assert not target.exists(); target.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
