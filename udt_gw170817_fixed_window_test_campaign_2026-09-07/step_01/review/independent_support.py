"""Reconstruct the proposed98s-support grid from independent text mask reads."""
import hashlib
import json
from pathlib import Path
import runpy
import struct

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/tmp/udt-gw170817-fixed-window-xshnIR')
helpers = runpy.run_path(str(Path(__file__).with_name('independent_metadata.py')))
data = helpers['data']
claims = json.loads((ROOT/'metadata_filtered_run.stdout').read_text())
start = 1187008512
proposed = []
for offset in range(4,4004,100):
    core = start+offset
    support = (core-4,core+94)
    if support[1] <= 1187008680 or support[0] >= 1187008980:
        proposed.append(core)
assert len(proposed) == 36
masks = {}
files = {}
catalogue = (CACHE/'official_O2_4k_hdf_md5.txt').read_text()
for detector in ['H1','L1','V1']:
    file = CACHE/(detector+'_complete.hdf5')
    digests = [hashlib.md5(),hashlib.sha256()]
    with file.open('rb') as stream:
        while True:
            block = stream.read(2**20)
            if not block: break
            for digest in digests: digest.update(block)
    md5,sha = [d.hexdigest() for d in digests]
    row = next(line for line in catalogue.splitlines()
               if line.split()[-1].startswith(detector+'/') and '-1187008512-4096.hdf5' in line)
    assert row.split()[0] == md5 == claims['files'][detector]['official_md5_match']
    assert sha == claims['files'][detector]['sha256']
    dq,_ = data(file,'/quality/simple/DQmask')
    inj,_ = data(file,'/quality/injections/Injmask')
    masks[detector]=(dq,inj)
    for name,array in [('dq',dq),('inj',inj)]:
        masksha=hashlib.sha256(struct.pack('<4096I',*array)).hexdigest()
        assert masksha == claims['files'][detector]['masks'][name]['sha256']
    files[detector]=dict(md5=md5,sha256=sha,bytes=file.stat().st_size)
failures={}
for core in proposed:
    bad=[]
    for detector,(dq,inj) in masks.items():
        for gps in range(core-4,core+94):
            index=gps-start
            if dq[index]&127 !=127 or inj[index]&23 !=23:
                bad.append(dict(detector=detector,gps=gps,dq=dq[index],inj=inj[index]))
    if bad: failures[core]=bad
eligible=[core for core in proposed if core not in failures]
assert eligible==claims['offsource_core_starts_gps']
assert eligible[:12]==claims['training_core_starts_gps']
assert eligible[12:]==claims['reference_core_starts_gps']
assert list(failures)==claims['excluded_for_metadata']
assert all(all(dq[gps-start]&127==127 and inj[gps-start]&23==23
                   for gps in range(1187008776,1187008874))
           for dq,inj in masks.values())
print(json.dumps(dict(files=files,proposed_count=len(proposed),eligible=eligible,
    failures=failures,training_count=12,reference_count=len(eligible)-12,
    conditional_rank_resolution=1/(len(eligible)-12+1),
    note='Rank resolution requires exchangeability for coverage; no statistical coverage asserted.',
    producer_metadata_code_imported=False,field_reader='reviewer h5dump text parser; raw producer masks not reused',
    strain_samples_inspected=False),indent=2,sort_keys=True))
