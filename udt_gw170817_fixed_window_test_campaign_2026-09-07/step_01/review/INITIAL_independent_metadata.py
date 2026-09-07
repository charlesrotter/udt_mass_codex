"""Read only whitelisted header/meta/quality fields from completed HDF5 files."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

CACHE = Path('/tmp/udt-gw170817-fixed-window-xshnIR')
CORE = (1187008780, 1187008870)
COMMANDS = []


def h5read(file, path, attribute=False):
    allowed = (path.startswith('/meta/') or path.startswith('/quality/') or
               (attribute and path in ('/strain/Strain/Xspacing', '/strain/Strain/Npoints', '/strain/Strain/Xstart')))
    assert allowed, 'never expose observational strain samples'
    command = ['h5dump', '-y', '-w0', '-m', '%.17g', '-a' if attribute else '-d', path, str(file)]
    COMMANDS.append(command)
    run = subprocess.run(command, check=True, capture_output=True, text=True, timeout=5)
    assert not run.stderr
    block = re.search(r'\bDATA\s*\{(.*?)\}', run.stdout, re.S)
    assert block, path
    return block.group(1).strip(), hashlib.sha256(run.stdout.encode()).hexdigest()


def data(file, path, attribute=False):
    block, digest = h5read(file, path, attribute)
    if block.startswith('"'):
        result = re.findall(r'"([^"]*)"', block)
    else:
        result = [float(x) if ('.' in x or 'e' in x.lower()) else int(x)
                  for x in re.findall(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?', block)]
    return result, digest


def segments(good, start):
    starts = [i for i, flag in enumerate(good) if flag and (i == 0 or not good[i-1])]
    ends = [i+1 for i, flag in enumerate(good) if flag and (i+1 == len(good) or not good[i+1])]
    return [[start+a, start+b] for a,b in zip(starts,ends)]


def summarize(detector):
    file = CACHE / (detector+'_complete.hdf5')
    keys = ['Detector','GPSstart','Duration','FrameType','StrainChannel']
    meta, field_hashes = {}, {}
    for key in keys:
        found, digest = data(file, '/meta/'+key)
        assert len(found) == 1
        meta[key] = found[0]
        field_hashes['/meta/'+key] = digest
    for key in ['Xspacing','Npoints','Xstart']:
        found,digest = data(file, '/strain/Strain/'+key, attribute=True)
        assert len(found) == 1
        meta[key] = found[0]
        field_hashes['/strain/Strain/'+key] = digest
    assert meta['Detector'] == detector
    assert meta['GPSstart'] == meta['Xstart'] == 1187008512
    assert meta['Duration'] == 4096 and meta['Npoints'] == 16777216
    assert meta['Xspacing'] == 1/4096
    expected = {'H1':('H1_CLEANED_HOFT_C02','H1:DCH-CLEAN_STRAIN_C02'),
                'L1':('L1_CLEANED_HOFT_C02','L1:DCH-CLEAN_STRAIN_C02'),
                'V1':('V1O2Repro2A','V1:Hrec_hoft_V1O2Repro2A_16384Hz')}
    assert (meta['FrameType'], meta['StrainChannel']) == expected[detector]
    dqnames, _ = data(file, '/quality/simple/DQShortnames')
    injnames, _ = data(file, '/quality/injections/InjShortnames')
    dq, field_hashes['DQmask'] = data(file, '/quality/simple/DQmask')
    inj, field_hashes['Injmask'] = data(file, '/quality/injections/Injmask')
    assert len(dq) == len(inj) == 4096
    assert dqnames == ['DATA','CBC_CAT1','CBC_CAT2','CBC_CAT3','BURST_CAT1','BURST_CAT2','BURST_CAT3']
    assert injnames == ['NO_CBC_HW_INJ','NO_BURST_HW_INJ','NO_DETCHAR_HW_INJ','NO_CW_HW_INJ','NO_STOCH_HW_INJ']
    start = meta['GPSstart']
    a,b = CORE[0]-start,CORE[1]-start
    predicates = {'DATA_all_NO_HW_INJ':[(x&1)==1 and (y&31)==31 for x,y in zip(dq,inj)],
                  'all_DQ_all_NO_HW_INJ':[(x&127)==127 and (y&31)==31 for x,y in zip(dq,inj)]}
    return dict(file=str(file),bytes=file.stat().st_size,meta=meta,field_dump_sha256=field_hashes,
                dq_names=dqnames,inj_names=injnames,dq_mask_counts=dict(Counter(dq)),
                injection_mask_counts=dict(Counter(inj)),
                core_dq_counts=dict(Counter(dq[a:b])),core_inj_counts=dict(Counter(inj[a:b])),
                valid_segments={name:segments(flags,start) for name,flags in predicates.items()},
                proposed_core_pass={name:all(flags[a:b]) for name,flags in predicates.items()},
                note='Two published mask predicates are diagnostics, not an outcome-selected window rule.')


if __name__ == '__main__':
    result = {name:summarize(name) for name in ['H1','L1','V1']}
    print(json.dumps(dict(python=sys.version,results=result,commands=COMMANDS,
                         h5dump_version=subprocess.check_output(['h5dump','-V'],text=True).strip(),
                         outcome_exposure='No strain samples, PSD or event contrast; only whitelisted metadata and masks.'),indent=2,sort_keys=True))
