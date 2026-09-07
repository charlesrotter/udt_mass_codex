"""R1 frozen OFFSOURCE-only finite-statistic screen. Not a physical event null."""
import hashlib,json,platform,subprocess,sys,time
from pathlib import Path
import numpy as np
import scipy
from scipy import fft,signal

HERE=Path(__file__).resolve().parent
PKG=HERE.parent; REPO=PKG.parent
CACHE=Path('/tmp/udt-gw170817-fixed-window-xshnIR')
FREEZE=PKG/'step_01/FREEZE.json'
assert hashlib.sha256(FREEZE.read_bytes()).hexdigest()=='fa0506eaea5ef20dcd92aabf3b2d1a0efc7fb75ef6c7272c00e5e6764c591324'
cfg=json.loads(FREEZE.read_text())
meta_path=PKG/'step_01/metadata_filtered_run.stdout'
assert hashlib.sha256(meta_path.read_bytes()).hexdigest()=='9e6c1d6fa98e14e0b2c060e18d4e7b46aacc35890aff46c51474ca03ce1f74af'
meta=json.loads(meta_path.read_text())
design_path=REPO/cfg['design_dependency']
assert hashlib.sha256(design_path.read_bytes()).hexdigest()==cfg['design_sha256']
design=json.loads(design_path.read_text())
F=np.array(design['F_HLV_plus_cross']); tau=np.array(design['arrival_minus_geocenter_seconds'])
b=np.r_[-np.linalg.solve(F[:2].T,F[2]),1.]
assert np.linalg.norm(b@F)/np.linalg.norm(F)<1e-12
fs=4096; n=98*fs; nc=90*fs; pad=4*fs; scale=1e21
f=fft.rfftfreq(n,1/fs); fc=fft.rfftfreq(nc,1/fs)
core_bins=np.arange(len(fc))
band=(core_bins>=30*90)&(core_bins<=500*90); K=int(band.sum()); assert K==42301
w=signal.windows.hann(nc,sym=False); w2=float(w@w)
train=meta['training_core_starts_gps']; refs=meta['reference_core_starts_gps']
assert len(train)==12 and len(refs)==21

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk:=stream.read(1024**2):h.update(chunk)
    return h.hexdigest()

def allowed(start):
    assert start in train+refs, 'unfrozen support'
    lo,hi=start-4,start+94
    assert hi<=1187008680 or lo>=1187008980, 'event exclusion'
    assert lo>=1187008512 and hi<=1187012608
    return (lo-1187008512)*fs

def dump(obj):
    print(json.dumps(obj,indent=2,sort_keys=True))

def extract(det):
    assert det in cfg['detector_order']
    src=CACHE/f'{det}_complete.hdf5'
    assert sha(src)==meta['files'][det]['sha256']
    dest=CACHE/'offsource'; dest.mkdir(exist_ok=True)
    rows=[]
    for start in train+refs:
        index=allowed(start); out=dest/f'{det}_{start}_98s_f64le.bin'
        assert not out.exists(), 'never overwrite observed extracts'
        cmd=['h5dump','-d','/strain/Strain','-s',str(index),'-c',str(n),'-b','LE','-o',str(out),str(src)]
        t=time.monotonic(); r=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
        assert r.returncode==0, r.stderr
        x=np.fromfile(out,dtype='<f8'); assert x.shape==(n,) and np.isfinite(x).all()
        rows.append(dict(core_gps=start,support_gps=[start-4,start+94],sample_start=index,
          count=n,dtype='<f8',bytes=out.stat().st_size,sha256=sha(out),command=cmd,
          duration_seconds=time.monotonic()-t,stdout=r.stdout,stderr=r.stderr,returncode=r.returncode))
    try: allowed(1187008780)
    except AssertionError: rejected=True
    else: rejected=False
    assert rejected
    dump(dict(mode='offsource extraction only',detector=det,source_sha256=sha(src),
      reserved_support_guard_rejects=True,records=rows,event_samples_read=False))

def shift(x,dt):
    z=fft.rfft(x); z[0]=0;z[-1]=0
    return fft.irfft(z*np.exp(2j*np.pi*f*dt),n=n)

def channels(start):
    allowed(start)
    xs=[]
    for d,dt in zip(cfg['detector_order'],tau):
        p=CACHE/'offsource'/f'{d}_{start}_98s_f64le.bin'
        manifest=json.loads((HERE/f'{d}_extract_run.stdout').read_text())
        expected=[row['sha256'] for row in manifest['records'] if row['core_gps']==start]
        raw=p.read_bytes(); assert len(expected)==1 and hashlib.sha256(raw).hexdigest()==expected[0]
        x=np.frombuffer(raw,dtype='<f8')*scale
        assert x.shape==(n,) and np.isfinite(x).all()
        xs.append(shift(x,dt)[pad:pad+nc])
    return np.array(xs)

def synthetic(family,phase):
    low,high=cfg['injection_spectral_families_hz'][family]
    # Exact Fourier-bin labels own inclusive endpoints; rounded rfftfreq does not.
    bins=np.arange(len(f))
    active=(bins>=low*98)&(bins<=high*98)
    assert active[low*98] and active[high*98]
    assert int(active.sum())==(high-low)*98+1
    rng=np.random.Generator(np.random.PCG64(352170817+1000*family+phase))
    z=np.zeros(len(f),complex); m=int(active.sum())
    z[active]=rng.standard_normal(m)+1j*rng.standard_normal(m)
    x=fft.irfft(z,n=n)
    norm=np.sqrt(np.sum(x[pad:pad+nc]**2)/fs); assert norm>0
    return x/norm

def method_checks():
    h=np.array([synthetic(0,0),synthetic(1,1)])
    raw=np.array([shift(row@h,-dt) for row,dt in zip(F,tau)])
    aligned=np.array([shift(x,dt) for x,dt in zip(raw,tau)])
    denom=np.linalg.norm(aligned)
    good=float(np.linalg.norm(b@aligned)/denom)
    wrong_sign=float(np.linalg.norm(b@np.array([shift(x,-dt) for x,dt in zip(raw,tau)]))/denom)
    broken=b.copy();broken[0]=0
    wrong_coeff=float(np.linalg.norm(broken@aligned)/denom)
    assert good<1e-10 and wrong_sign>1e-3 and wrong_coeff>1e-3
    physical=raw/scale
    physical_aligned=np.array([shift(x,dt) for x,dt in zip(physical,tau)])
    physical_good=float(np.linalg.norm(b@physical_aligned)/np.linalg.norm(physical_aligned))
    physical_wrong=float(np.linalg.norm(broken@physical_aligned)/np.linalg.norm(physical_aligned))
    assert physical_good<1e-10 and physical_wrong>1e-3
    a=synthetic(2,2); via_v=shift(shift(a,-tau[2]),tau[2])
    injection_relative=float(np.linalg.norm(via_v-a)/np.linalg.norm(a))
    assert injection_relative<1e-10
    hrss=float(np.sqrt(np.sum(a[pad:pad+nc]**2)/fs))
    assert abs(hrss-1)<1e-12
    return dict(correct_null_relative=good,wrong_sign_relative=wrong_sign,
        missing_H_term_relative=wrong_coeff,physical_scale_correct_relative=physical_good,
        physical_scale_wrong_relative=physical_wrong,V_injection_roundtrip_relative=injection_relative,
        injection_hrss_scaled=hrss,b=b.tolist(),tau_seconds=tau.tolist(),
        exact_domain='finite cyclic zeroDC/Nyquist static response only; not upstream/continuum retention')

welch_args=dict(fs=fs,window='hann',nperseg=4*fs,noverlap=2*fs,detrend='constant',scaling='density',average='mean')
def training():
    matrices=[]; direct=[]; each=[]
    for start in train:
        xs=channels(start); r=b@xs
        freq,sr=signal.welch(r,**welch_args); direct.append(sr)
        c=np.empty((3,3,len(freq)),complex)
        for i in range(3):
            for j in range(i,3):
                _,c[i,j]=signal.csd(xs[i],xs[j],**welch_args)
                c[j,i]=c[i,j].conj()
        recon=np.einsum('i,ijf,j->f',b,c,b).real
        rel=float(np.linalg.norm(sr-recon)/np.linalg.norm(sr))
        assert rel<1e-10
        matrices.append(c); each.append(dict(core_gps=start,covariance_reconstruction_relative=rel))
    psd=np.mean(direct,axis=0); cov=np.mean(matrices,axis=0)
    interp=np.interp(fc[band],freq,psd)
    assert np.isfinite(interp).all() and (interp>0).all()
    floor_count=int(np.sum(interp<1e-60*scale**2)); assert floor_count==0
    dest=HERE/'PSD_training.npz'
    with dest.open('xb') as stream:np.savez_compressed(stream,frequency_hz=freq,residual_psd_scaled=psd,
       spectral_covariance_scaled=cov,per_window_residual_psd_scaled=np.array(direct),
       training_core_gps=np.array(train),strain_multiplier=np.array(scale))
    bdiag=np.einsum('i,iif,i->f',b,cov,b).real
    good=(freq>=30)&(freq<=500)
    dump(dict(mode='offsource PSD training',PSD_artifact_sha256=sha(dest),records=each,
       retained_floor_count=floor_count,PSD_units='(strain*1e21)^2/Hz; divide by1e42 for strain2/Hz',
       b=b.tolist(),cross_term_relative_band_L2=float(np.linalg.norm((psd-bdiag)[good])/np.linalg.norm(psd[good])),
       noise_independence_assumed=False,method_checks=method_checks(),event_samples_read=False,
       versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)))

def evaluate():
    with np.load(HERE/'PSD_training.npz',allow_pickle=False) as saved:
        psd=np.interp(fc[band],saved['frequency_hz'],saved['residual_psd_scaled'])
    assert (psd>0).all() and np.isfinite(psd).all() and not np.any(psd<1e-18)
    weights=np.sqrt(2/(fs*w2*K*psd))
    def feature(r):return fft.rfft(w*r)[band]*weights
    zr=[]; q=[]; first_core=None
    for start in refs:
        core=b@channels(start)
        if first_core is None:first_core=core.copy()
        z=feature(core); zr.append(z);q.append(float(np.vdot(z,z).real))
    zr=np.array(zr);q=np.array(q);threshold=float(q.max())
    grid=np.array(cfg['effect_grid'])*scale
    families=[]; coeff_c=[]; coeff_u=[]; s_hash=[]
    direct_check=[]
    for fam in range(3):
        crosses=[]; cs=[]; us=[]; critical=[]
        for phase in range(8):
            full=synthetic(fam,phase); core=full[pad:pad+nc]
            s_hash.append(dict(family=fam,phase=phase,full_scaled_f64_sha256=hashlib.sha256(full.tobytes()).hexdigest()))
            zs=feature(core); u=float(np.vdot(zs,zs).real)
            c=np.real(zr.conj()@zs)
            values=q[:,None]+2*c[:,None]*grid[None,:]+u*grid[None,:]**2
            crosses.append(values>threshold);cs.append(c);us.append(u)
            critical.append((-c+np.sqrt(c*c+u*(threshold-q)))/u/scale)
            for amp in [1.,3.]:
                zdirect=feature(first_core+amp*core)
                direct=float(np.vdot(zdirect,zdirect).real)
                quad=float(q[0]+2*amp*c[0]+amp*amp*u)
                rel=abs(direct-quad)/max(abs(direct),abs(quad))
                assert rel<1e-10;direct_check.append(rel)
        frac=np.mean(np.array(crosses),axis=(0,1))
        crit=np.sort(np.array(critical).ravel()); n90=int(np.ceil(.9*len(crit)))
        families.append(dict(band_hz=cfg['injection_spectral_families_hz'][fam],
          crossing_fractions=frac.tolist(),target_crossing_fraction=float(frac[4]),
          survives_target=bool(frac[4]>=.9),finite_90percent_crossing_hrss=float(crit[n90-1])))
        coeff_c.append(cs);coeff_u.append(us)
    dest=HERE/'reinjection_coefficients_R1.npz'
    with dest.open('xb') as stream:np.savez_compressed(stream,reference_Q=q,threshold=threshold,
      cross_terms=np.array(coeff_c),signal_Q=np.array(coeff_u),grid_hrss=np.array(cfg['effect_grid']),
      reference_core_gps=np.array(refs))
    dump(dict(mode='frozen offsource descriptive sensitivity',reference_core_gps=refs,reference_Q=q.tolist(),
      threshold=threshold,rank_resolution_if_exchangeable=1/22,
      median_Q_first10=float(np.median(q[:10])),median_Q_last11=float(np.median(q[10:])),
      max_over_min_Q=float(q.max()/q.min()),grid_hrss=cfg['effect_grid'],families=families,
      survives_all_families=all(x['survives_target'] for x in families),
      reinjection_coefficients_sha256=sha(dest),synthetic_field_hashes=s_hash,
      direct_quadratic_max_relative_error=max(direct_check),
      observed_strain_scope='33 offsource supports only; event UNEXAMINED',
      interpretation='finite in-sample fractions, NOT population power/confidence/physical event constraint',
      freeze_sha256=sha(FREEZE),metadata_sha256=sha(meta_path),producer_sha256=sha(__file__),
      versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)))

if __name__=='__main__':
    if sys.argv[1]=='extract':extract(sys.argv[2])
    elif sys.argv[1]=='train':training()
    elif sys.argv[1]=='evaluate':evaluate()
    elif sys.argv[1]=='method':dump(method_checks())
    else:raise ValueError('Unknown mode; no event mode exists')
