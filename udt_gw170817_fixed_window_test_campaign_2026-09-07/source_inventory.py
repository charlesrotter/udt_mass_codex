"""Explicit permitted public cache inventory; never searches protected paths."""
from pathlib import Path
import hashlib,json
root=Path('/tmp/udt-gw170817-fixed-window-xshnIR')
files={
 'H1_complete.hdf5':'https://gwosc.org/archive/data/O2_4KHZ_R1/1186988032/H-H1_GWOSC_O2_4KHZ_R1-1187008512-4096.hdf5',
 'L1_complete.hdf5':'https://gwosc.org/archive/data/O2_4KHZ_R1/1186988032/L-L1_GWOSC_O2_4KHZ_R1-1187008512-4096.hdf5',
 'V1_complete.hdf5':'https://gwosc.org/archive/data/O2_4KHZ_R1/1186988032/V-V1_GWOSC_O2_4KHZ_R1-1187008512-4096.hdf5',
 'official_O2_4k_hdf_md5.txt':'https://gwosc.org/archive/md5/O2_4KHZ_R1/strain-hdf.txt',
 'LIGO_O2_cal_uncertainty.tgz':'https://dcc.ligo.org/public/0177/T2100313/003/LIGO_O2_cal_uncertainty.tgz',
 'Virgo_O2_cal_uncertainty.tgz':'https://dcc.ligo.org/public/0177/T2100313/003/Virgo_O2_cal_uncertainty.tgz',
 'noise_subtraction.pdf':'https://arxiv.org/pdf/1809.05348',
 'swope.pdf':'https://arxiv.org/pdf/1710.05452'}
for d in ['H1','L1','V1']:
 files[d+'_links.json']=f'https://gwosc.org/archive/links/O2_4KHZ_R1/{d}/1187008700/1187008950/json/'
out=[]
for file,url in files.items():
 p=root/file; h=hashlib.sha256()
 with p.open('rb') as f:
  while chunk:=f.read(1024*1024):h.update(chunk)
 out.append(dict(path=str(p),url=url,bytes=p.stat().st_size,sha256=h.hexdigest()))
total=sum(x['bytes'] for x in out)
assert total<1024**3
print(json.dumps(dict(sources=out,network_body_bytes=total,cap_bytes=1024**3,
 accounting='Initial partials plus exact continuations equal complete H/L sizes; local copies and extracted text/masks are not extra network bytes. HTTP framing/headers excluded. No repeat full strain transfer.',
 partials_preserved=['H1.hdf5','L1.hdf5'],source_grade='public observation/measurement documentation, not native UDT law'),indent=2))
