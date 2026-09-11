"""Independent hostile harness; changes supplied read bytes only, never source files."""
from pathlib import Path
import csv
import datetime
import hashlib
import io
import json
import platform
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import ti2_banking_guard as current
import ti1_banking_guard as ti1
import verify_current_scientific_premises as historical

REGISTRY = ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv'
raw_read = Path.read_bytes
raw = raw_read(REGISTRY)
lines = raw.splitlines(keepends=True)
row_index = next(i for i,line in enumerate(lines) if line.startswith(b'G414\t'))
original_row = lines[row_index]
outcomes = []

def reject(name, action, expected):
    try:
        action()
    except SystemExit as exc:
        assert expected in str(exc), (name,str(exc))
        outcomes.append({'name':name,'result':'REJECTED','message':str(exc)})
    else:
        raise AssertionError('False pass: '+name)

def supplied(payload, action, *, second=None):
    reads=[]
    original_open=Path.open
    def value(path):
        reads.append(path)
        return second if second is not None and len(reads)>1 else payload
    def read(path):
        if path == REGISTRY:
            return value(path)
        return raw_read(path)
    def opened(path,mode='r',*args,**kwargs):
        if path==REGISTRY:
            data=value(path)
            return io.BytesIO(data) if 'b' in mode else io.StringIO(data.decode())
        return original_open(path,mode,*args,**kwargs)
    with patch.object(Path,'read_bytes',read),patch.object(Path,'open',opened):
        action()
    assert len(reads)==1, ('registry snapshot reread',len(reads))

current.validate_ti2_banking(ROOT)
outcomes.append({'name':'current_full_source_guard','result':'PASS'})
for field in range(9):
    fields = original_row.rstrip(b'\n').split(b'\t')
    fields[field] += b' PHYSICALLY_ADOPTED_WITHOUT_LIMITS'
    mutated = list(lines)
    mutated[row_index] = b'\t'.join(fields)+b'\n'
    expected = 'TI2 current row missing/duplicate' if field==0 else 'TI2 exact row/scope changed'
    supplied(b''.join(mutated),lambda:reject('current_field_'+str(field),
        lambda:current.validate_ti2_banking(ROOT,authenticate_sources=False),expected))

for mode in ['missing','duplicate','reorder','old_row','header']:
    changed = list(lines)
    if mode=='missing': changed.pop(row_index)
    elif mode=='duplicate': changed.insert(row_index,original_row)
    elif mode=='reorder': changed[row_index],changed[row_index+1]=changed[row_index+1],changed[row_index]
    elif mode=='old_row':
        i=next(i for i,x in enumerate(changed) if x.startswith(b'G312\t'))
        changed[i]=changed[i].replace(b'FILTER',b'DERIVED',1)
    else: changed[0]=changed[0].replace(b'term',b'wrong_term',1)
    supplied(b''.join(changed),lambda:reject('current_'+mode,
        lambda:current.validate_ti2_banking(ROOT,authenticate_sources=False),'TI2'))

poison_row=original_row.replace(b'NOT_PHYSICAL_ADOPTION',b'PHYSICAL_LAW_ADOPTED',1)
assert poison_row != original_row
poison=raw.replace(original_row,poison_row,1)
old=current.without_ti2(raw,required=True)
assert current.without_ti2(old)==old
reject('current_cannot_lack_G414',lambda:current.without_ti2(old,required=True),'TI2 current row missing/duplicate')
assert current.without_ti2(raw.replace(b'G312\t',b'G312_POISON\t',1)) == old.replace(b'G312\t',b'G312_POISON\t',1)
supplied(raw,lambda:current.validate_ti2_banking(ROOT,authenticate_sources=False),second=poison)
outcomes.append({'name':'current_one_snapshot','result':'PASS'})

guards=[
    ('validate_ti1_banking',ti1.validate_ti1_banking),
    *[(name,getattr(historical,name)) for name in [
    'validate_conditional_banking','validate_shared_constraint_banking',
    'validate_persistence_banking','validate_restrictiveness_banking',
    'validate_source_metric_banking','validate_reconstruction_banking',
    'validate_coupled_banking','validate_vacuum_scale_banking',
    'validate_berger_banking','validate_closed_fibre_banking',
    'validate_neighboring_tidal_banking','validate_reviewed_backlog_banking']]
]
for name,function in guards:
    supplied(poison,lambda:reject('history_poison_'+name,
        lambda:function(ROOT,authenticate_sources=False),'TI2 exact row/scope changed'),second=raw)
    supplied(raw,lambda:function(ROOT,authenticate_sources=False),second=poison)
    outcomes.append({'name':'history_clean_one_snapshot_'+name,'result':'PASS'})
supplied(poison,lambda:reject('authority_same_snapshot_poison',
    lambda:historical.validate_gr_filter_authority(ROOT),'TI2 exact row/scope changed'),second=raw)

for name in current.TI2_GUARD_FILES:
    target=ROOT/name
    seen=[]
    def read(path):
        data=raw_read(path)
        if path==target:
            seen.append(path)
            return data+b'\nUNAUTHORIZED_UPGRADE\n'
        return data
    with patch.object(Path,'read_bytes',read):
        reject('acceptance_poison_'+name,lambda:current.validate_ti2_banking(ROOT,authenticate_sources=False),'TI2 guard file changed')
    assert seen

source_names=[
    'INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','DISCOVERY_AND_FREEZE.md',
    'review/REVIEW.md','review/FINAL_FIDELITY.md','initial_rate.py',
    'checks/mutant_omit_spatial_ricci_rate.json','review/adm_rate.stderr'
]
for name in source_names:
    target=ROOT/'udt_two_shape_evolution_2026-09-11'/name
    seen=[]
    def read(path):
        data=raw_read(path)
        if path==target:
            seen.append(path)
            return data+b'\nLIMITS_OR_FAILURES_ERASED\n'
        return data
    with patch.object(Path,'read_bytes',read):
        reject('source_poison_'+name,lambda:current.validate_ti2_banking(ROOT),'TI2 original source evidence changed')
    assert seen

# Exercise the actual replay adapter before it could fall back to a historical source.
# Suppress scratch copying, writes and any replay process; no scientific package is read.
class NoScratch:
    def __init__(self,*args,**kwargs): pass
    def __enter__(self): return str(Path(__file__).resolve().parent/'_uncreated_probe')
    def __exit__(self,*args): return False
def forbidden(*args,**kwargs):
    raise AssertionError('poison reached historical fallback/write/replay')
with patch.object(historical.tempfile,'TemporaryDirectory',NoScratch), \
     patch.object(historical.shutil,'copytree',lambda *a,**k:None), \
     patch.object(historical,'read_tsv',lambda *a,**k:[{'path':'CURRENT_SCIENTIFIC_PREMISES.tsv','sha256':hashlib.sha256(old).hexdigest()}]), \
     patch.object(historical,'frozen_git_source_bytes',forbidden), \
     patch.object(Path,'write_bytes',forbidden), \
     patch.object(historical.subprocess,'run',forbidden):
    supplied(poison,lambda:reject('replay_poison_before_projection_and_fallback',
        lambda:historical.replay_package_with_current_registry_rows_removed(Path('hypothetical_review_adapter'),()),
        'TI2 exact row/scope changed'),second=raw)

assert raw_read(REGISTRY)==raw
print(json.dumps({
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verdict':'PASS','python':platform.python_version(),
    'runtime_model_version':'UNATTESTED','cases':len(outcomes),
    'actual_outcomes':outcomes,
    'source_and_registry_mutation':'supplied read bytes only; no real file edits',
    'independence':'separate-context harness; production guards reused as object of tests, not science proof',
    'omissions':'Full397 and original symbolic/Fraction science are not rerun.'
},indent=2))
