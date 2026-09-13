from pathlib import Path
import sys,os,hashlib,json
sourcepath=Path("/home/udt-admin/udt_mass_codex/udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py")
source=sourcepath.read_text()
assert hashlib.sha256(source.encode()).hexdigest()=="8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef"
seconds,mib,prefix,*command=sys.argv[1:];seconds=int(seconds);mib=int(mib)
assert 1<=seconds<=900 and 1<=mib<=2048
for name in ["OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"]:os.environ[name]="1"
changes={"(512 * 1024**2, 512 * 1024**2)":f"({mib} * 1024**2, {mib} * 1024**2)","(60, 60)":f"({seconds}, {seconds})","timeout=60":f"timeout={seconds}","address_space_bytes=512 * 1024**2":f"address_space_bytes={mib} * 1024**2","cpu_seconds=60":f"cpu_seconds={seconds}"}
for a,b in changes.items():assert a in source;source=source.replace(a,b)
prefix=str(Path(prefix).resolve())
meta=Path(prefix+".capture_provenance.json");assert not meta.exists()
meta.write_text(json.dumps({"source":str(sourcepath),"source_sha256":hashlib.sha256(sourcepath.read_bytes()).hexdigest(),"adapted_capture_sha256":hashlib.sha256(source.encode()).hexdigest(),"limits":{"seconds":seconds,"mib":mib},"thread_environment":{n:os.environ[n] for n in ["OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"]},"command":command},indent=2)+"\n")
sys.argv=[str(sourcepath),prefix,str(Path.cwd()),*command]
exec(compile(source,str(sourcepath),"exec"),{"__name__":"__main__","__file__":str(sourcepath)})
