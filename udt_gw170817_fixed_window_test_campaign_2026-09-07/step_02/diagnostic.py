"""Same-author bounded diagnosis; frozen statistic and exclusions unchanged."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from scipy import fft
import screen as s

with np.load(s.HERE/'PSD_training.npz',allow_pickle=False) as p:
    psd=np.interp(s.fc[s.band],p['frequency_hz'],p['residual_psd_scaled'])
weight=np.sqrt(2/(s.fs*s.w2*s.K*psd))
rows=[]; dest=s.CACHE/'diagnostic';dest.mkdir(exist_ok=True)
for start in [1187010216,1187011516]:
    xs=s.channels(start)
    z=np.array([fft.rfft(s.w*s.b[i]*xs[i])[s.band]*weight for i in range(3)])
    qi=np.sum(abs(z)**2,axis=1)
    cross=[float(2*np.vdot(z[i],z[j]).real) for i,j in [(0,1),(0,2),(1,2)]]
    q=float(np.sum(abs(z.sum(axis=0))**2));recon=float(qi.sum()+sum(cross))
    assert abs(q-recon)/q<1e-10
    rawstats=[]
    for d in s.cfg['detector_order']:
        original=s.CACHE/'offsource'/f'{d}_{start}_98s_f64le.bin'
        x=np.fromfile(original,dtype='<f8');imax=int(np.argmax(abs(x)))
        row=dict(detector=d,raw_peak_absolute_strain=float(abs(x[imax])),
          raw_peak_gps=start-4+imax/s.fs,raw_rms_strain=float(np.sqrt(np.mean(x*x))))
        if start==1187011516:
            out=dest/f'{d}_{start}_repeat.bin';assert not out.exists()
            cmd=['h5dump','-d','/strain/Strain','-s',str(s.allowed(start)),'-c',str(s.n),
                 '-b','LE','-o',str(out),str(s.CACHE/f'{d}_complete.hdf5')]
            run=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=15)
            row.update(reextract_command=cmd,reextract_sha256=s.sha(out),
              original_sha256=s.sha(original),stdout=run.stdout,stderr=run.stderr)
            assert row['reextract_sha256']==row['original_sha256']
        rawstats.append(row)
    rows.append(dict(core_gps=start,Q=q,weighted_detector_diagonal_Q=qi.tolist(),
      cross_terms_HL_HV_LV=cross,decomposition_relative_error=abs(q-recon)/q,raw_statistics=rawstats))
print(json.dumps(dict(scope='same-author exposed-record implementation/data diagnosis, NOT retuned analysis or physical classification',
 unchanged_frozen_statistic=True,records=rows,event_samples_read=False),indent=2))
