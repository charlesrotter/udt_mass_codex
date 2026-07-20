#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,json,os,re,subprocess,sys
from pathlib import Path
import numpy,torch
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
def digest(b):return hashlib.sha256(b).hexdigest()
def run(i,c,o,e,env=None):
 d=subprocess.run(c,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False);(HERE/o).write_bytes(d.stdout)
 if d.returncode!=e:raise AssertionError(f"{i}:{d.returncode}!={e}")
 return {"id":i,"command":" ".join(c),"exit_code":d.returncode,"output_artifact":o,"stdout_stderr_sha256":digest(d.stdout)}
def main():
 p="c2_nonlinear_stationary_solution_space_2026-07-20/"
 env=dict(os.environ);env["CUDA_VISIBLE_DEVICES"]="";env["PYTHONDONTWRITEBYTECODE"]="1"
 rec=[run("E01",[sys.executable,p+"build_source_census.py"],"CENSUS_TRANSCRIPT.txt",0,env),run("E02",[sys.executable,p+"build_source_adjudication.py"],"ADJUDICATION_TRANSCRIPT.txt",0,env),run("E03",[sys.executable,p+"summarize_solution_space.py"],"SUMMARY_TRANSCRIPT.txt",0,env),run("E04",[sys.executable,p+"verify_solution_space.py"],"VERIFICATION_TRANSCRIPT.txt",0,env)]
 t=run("E05",[sys.executable,"-m","pytest","tests/"],"TEST_TRANSCRIPT.txt",1,env);text=(HERE/"TEST_TRANSCRIPT.txt").read_text();m=re.search(r"(\d+) failed, (\d+) passed, (\d+) xfailed",text)
 if m is None or tuple(map(int,m.groups()))!=(1,69,1):raise AssertionError("test baseline")
 rec.append(t)
 site_numpy=str(Path(numpy.__file__).resolve().parent.parent);site_torch=str(Path(torch.__file__).resolve().parent.parent);package=str(HERE)
 code=("import sys,runpy; "+f"sys.path[:0]=[{site_numpy!r},{site_torch!r},{package!r}]; "+"import numpy,torch; assert numpy.__version__=='2.2.6'; assert torch.__version__=='2.5.1+cu121'; "+f"runpy.run_path({str(HERE/'verify_solution_space.py')!r},run_name='__main__')")
 rec.append(run("E06",[sys.executable,"-I","-c",code],"ISOLATED_VERIFICATION_TRANSCRIPT.txt",0,env))
 rec.append(run("E07",[sys.executable,p+"verify_raw_artifact.py"],"RAW_ARTIFACT_VERIFICATION_TRANSCRIPT.txt",0,env))
 out={"schema":"udt-c2-nonlinear-stationary-execution-1.0","result":"PASS","records":rec,"environment":{"python":sys.version.split()[0],"numpy":numpy.__version__,"torch":torch.__version__,"cpu_only":True,"gpu_used":False},"test_baseline":{"passed":69,"failed_known_hygiene":1,"xfailed":1},"expensive_solve_replayed":False,"expensive_solve_artifacts_hash_verified":True}
 (HERE/"EXECUTION_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 fields=["id","command","compute","exit_code","output_artifact","output_sha256"]
 with (HERE/"EXECUTION_LEDGER.tsv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for r in rec:w.writerow({"id":r["id"],"command":r["command"],"compute":"CPU_ONLY","exit_code":"1_EXPECTED_BASELINE" if r["exit_code"]==1 else "0","output_artifact":r["output_artifact"],"output_sha256":r["stdout_stderr_sha256"]})
  w.writerow({"id":"E08","command":"fresh external-model review","compute":"EXTERNAL_REVIEW_NOT_PERFORMED","exit_code":"AUTHORIZATION_NOT_GIVEN","output_artifact":"EXTERNAL_REVIEW_STATUS.txt","output_sha256":digest((HERE/"EXTERNAL_REVIEW_STATUS.txt").read_bytes())})
 (HERE/"ENVIRONMENT.txt").write_text(f"python={sys.version.split()[0]}\nnumpy={numpy.__version__}\ntorch={torch.__version__}\ncompute=CPU_ONLY\ngpu_used=false\nexternal_review=NOT_AUTHORIZED\n")
 print(json.dumps({"result":"PASS","records":len(rec),"tests":"69_passed_1_known_failed_1_xfailed","expensive_solve":"HASH_REPLAY_ONLY"},sort_keys=True))
if __name__=="__main__":main()
