#!/usr/bin/env python3
import datetime,json,pathlib,subprocess,time
p=pathlib.Path(__file__).resolve().parent
cmd=['python3','-B',str(p/'check_documentation_closure.py')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
with (p/'closure.stdout').open('xb') as out,(p/'closure.stderr').open('xb') as err:
    result=subprocess.run(cmd,cwd='/home/udt-admin/udt_mass_codex',stdout=out,stderr=err,timeout=60)
record={'command':cmd,'cwd':'/home/udt-admin/udt_mass_codex','start_utc':start,
        'actual_exit':result.returncode,'wall_seconds':round(time.monotonic()-t,6)}
with (p/'CLOSURE_RUN.json').open('x') as f: json.dump(record,f,indent=2)
assert result.returncode==0
data=json.loads((p/'closure.stdout').read_text())
print(json.dumps({k:v for k,v in data.items() if k!='all_three_way_byte_comparisons'},indent=2))
