"""Bounded CPU readouts on the fixed completed case list; no GPU calls."""
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
cases=['kasner_n16','kasner_n16_half','axial1_n16','axial1_n24','axial1_n24_half','axial1_n32','oblique1_n16','oblique1_n24','oblique1_n24_half','oblique1_n32','axial3_n24','oblique3_n24','phase1_n24']
reuse={'kasner_n16_half':B/'CLOCK_KASNER.json','axial1_n24_half':B/'CLOCK_AXIAL_HALF.json'}
(B/'clocks').mkdir(exist_ok=True)
def execute(name):
    if name in reuse:return name,str(reuse[name])
    path=B/'clocks'/f'{name}.json';command=[sys.executable,str(B/'clock_checks.py'),str(B/'histories'/f'{name}_window2.npz'),str(path)]
    if name.startswith('kasner'):command.append('--kasner')
    prefix=B/'checks'/f'clock_{name}';start=time.monotonic()
    with prefix.with_suffix('.stdout').open('x') as out,prefix.with_suffix('.stderr').open('x') as err:
        result=subprocess.run(command,stdout=out,stderr=err,timeout=90)
    with prefix.with_suffix('.json').open('x') as f:json.dump(dict(command=command,returncode=result.returncode,seconds=time.monotonic()-start),f,indent=2);f.write('\n')
    if result.returncode:raise RuntimeError('CLOCK_CASE_FAILED: '+name)
    return name,str(path)
with ThreadPoolExecutor(max_workers=2) as pool:mapping=dict(pool.map(execute,cases))
rows={k:json.loads(Path(q).read_text()) for k,q in mapping.items()};differences={}
for family in ['axial1','oblique1']:
    reference=rows[family+'_n32']['readouts']
    for suffix in ['n16','n24','n24_half']:
        key=family+'_'+suffix;differences[key+'_against_n32']=max(abs(a['logZ']-b['logZ']) for a,b in zip(rows[key]['readouts'],reference))
    differences[family+'_temporal']=max(abs(a['logZ']-b['logZ']) for a,b in zip(rows[family+'_n24']['readouts'],rows[family+'_n24_half']['readouts']))
report=dict(status='FINITE_CLOCK_BATCH_PASS' if max(differences.values())<2e-7 else 'CLOCK_REFINEMENT_UNRESOLVED',readout_paths=mapping,readout_sha256={k:hashlib.sha256(Path(q).read_bytes()).hexdigest() for k,q in mapping.items()},max_logZ_changes=differences,scope='Fixed supplied late-window queries; no sign filtering, long-path or observer-selection claim')
with (B/'CLOCK_RESULT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(report,indent=2))
if report['status']!='FINITE_CLOCK_BATCH_PASS':raise SystemExit(1)
