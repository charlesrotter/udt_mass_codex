"""Final metadata/source/table/status correspondence, not a scientific re-run."""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'udt_linked_stationary_signal_benchmark_2026-09-12'
REVIEW=PKG/'review'
checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'passed':bool(ok),'detail':detail})
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def command(*args):return subprocess.check_output(args,cwd=ROOT,text=True)
intake=json.loads((PKG/'FINAL_REVIEW_INTAKE.json').read_text())
for name,expected in intake['files'].items():
    actual=digest(ROOT/name);check('final intake '+name,actual==expected,actual)
nav={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
source_pins=json.loads((PKG/'SOURCE_PINS.json').read_text())
source_pins.update(json.loads((PKG/'SUPPLEMENTAL_SOURCE_PINS.json').read_text())['files'])
for name,expected in source_pins.items():
    if name in nav:continue
    actual=digest(ROOT/name);check('preserved source '+name,actual==expected,actual)
head=command('git','rev-parse','HEAD').strip()
origin=command('git','rev-parse','origin/grok').strip()
branch=command('git','branch','--show-current').strip()
check('pinned branch/head/local origin reference',branch=='grok' and head==origin=='c12db2562da1a5098f65a97ae0c924dec149ca4c',{'branch':branch,'head':head,'origin_grok':origin,'remote_freshness':'parent attributed; reviewer did not fetch'})
tracked=command('git','diff','--name-only').splitlines()
staged=command('git','diff','--cached','--name-only').splitlines()
check('tracked delta is five navigation files',set(tracked)==nav,tracked)
check('no staged changes at reviewer final check',not staged,staged)
launch=json.loads((PKG/'LAUNCH.json').read_text())
current=command('git','status','--short','--untracked-files=all')
original_now=''.join(line+'\n' for line in current.splitlines() if line.startswith('?? ') and not line[3:].startswith(PKG.name+'/'))
check('original unrelated untracked status names unchanged',original_now==launch['original_status'],{'count':len(original_now.splitlines()),'sha256':hashlib.sha256(original_now.encode()).hexdigest(),'payloads':'not read'})
check('tracked whitespace diff',subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True).returncode==0)
bench=json.loads((PKG/'checks/benchmark.stdout').read_text())
table=list(csv.DictReader((PKG/'BENCHMARK_TABLE.tsv').open(),delimiter='\t'))
check('table has every declared case',len(table)==len(bench['records'])==9)
column_map={'turning_radius':'p','clock_R_A_B':'clock_R_A_B','chi_clock':'chi_clock','psi_B_radians':'psi_B','angle_contrast_radians':'angle_contrast','roundtrip_cE_over_L':'roundtrip_cE_over_L','time_contrast_cE_over_L':'time_contrast_cE_over_L'}
for row,rec in zip(table,bench['records']):
    check('table case and readout fidelity '+str(rec['supplied_coefficients']),
          [float(row['supplied_a']),float(row['supplied_b'])]==rec['supplied_coefficients'] and
          all(float(row[k])==rec[v] for k,v in column_map.items()))
summary=json.loads((PKG/'CHECK_RESULTS.json').read_text())
for name,receipt in summary['parent_receipts'].items():
    check('aggregate receipt '+name,receipt==json.loads((PKG/'checks'/f'{name}.json').read_text()))
navout=(PKG/'checks/navigation.stdout').read_text().strip()
check('current navigation actual output',navout==summary['navigation_stdout'] and '359 passed, 1 deselected' in navout)
check('current full audit actual success and empty stderr','PASS: 398-row premise registry' in (PKG/'checks/current_full398.stdout').read_text() and (PKG/'checks/current_full398.stderr').stat().st_size==0)
comparison=json.loads((REVIEW/'CROSS_METHOD_COMPARISON.json').read_text())
for name,expected in comparison['hashes'].items():
    check('saved independent comparison input '+name,digest(PKG/name)==expected)
result={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','checks':checks,
        'final_intake_sha256':digest(PKG/'FINAL_REVIEW_INTAKE.json'),
        'later_publication_excluded':intake['excluded_later_mechanics'],
        'science_rerun':False,'reviewer_changed_paths':'review/ only; no git mutations',
        'script_sha256':digest(Path(__file__))}
with (REVIEW/'FINAL_CHECK_RESULT.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'failures':[c for c in checks if not c['passed']],'utc':result['utc']},sort_keys=True))
if result['status']!='PASS':raise SystemExit(1)
