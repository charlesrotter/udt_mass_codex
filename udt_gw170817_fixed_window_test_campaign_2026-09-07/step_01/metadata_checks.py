"""FW1 metadata/calibration only: never opens /strain/Strain DATA."""
import hashlib, json, re, subprocess, sys, tarfile
from pathlib import Path
import numpy as np

cache = Path(sys.argv[1])
catalogue = (cache/'official_O2_4k_hdf_md5.txt').read_text()
out = {'exposure':'headers, masks, calibration only; no strain samples', 'files':{}}
cores = [1187008516+100*j for j in range(40)]
# Full98s support must miss the fixed known-event exclusion [8680,8980).
cores = [s for s in cores if s+94 <= 1187008680 or s-4 >= 1187008980]
assert len(cores)==36
out['proposed_offsource_core_starts_gps']=cores
eligible=set(cores)
for det in ['H1','L1','V1']:
    path=cache/f'{det}_complete.hdf5'
    data=path.read_bytes()
    md5=hashlib.md5(data).hexdigest()
    match=[line for line in catalogue.splitlines() if f'{det}/' in line and '-1187008512-4096.hdf5' in line]
    assert len(match)==1 and match[0].split()[0]==md5
    meta=subprocess.check_output(['h5dump','-g','/meta',str(path)],text=True)
    header=subprocess.check_output(['h5dump','-A','-d','/strain/Strain',str(path)],text=True)
    assert '16777216' in header and '0.000244141' in header
    masks={}
    for name, dataset in [('dq','/quality/simple/DQmask'),('inj','/quality/injections/Injmask')]:
        raw=cache/f'{det}_{name}.bin'
        if not raw.exists():
            subprocess.run(['h5dump','-d',dataset,'-b','LE','-o',str(raw),str(path)],check=True,capture_output=True)
        x=np.fromfile(raw,dtype='<u4'); assert x.shape==(4096,)
        masks[name]={'all_values':np.unique(x).tolist(), 'sha256':hashlib.sha256(raw.read_bytes()).hexdigest()}
        for start in [1187008780]+cores:
            i=start-4-1187008512; z=x[i:i+98]
            assert z.shape==(98,)
            passes=bool(np.all((z&127)==127)) if name=='dq' else bool(np.all((z&23)==23))
            if start==1187008780: assert passes
            elif not passes: eligible.discard(start)
    assert masks['inj']['all_values']==([31] if det=='V1' else [23])
    out['files'][det]={'size_bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
        'official_md5_match':md5,'official_catalogue_line':match[0],
        'meta_dump_sha256':hashlib.sha256(meta.encode()).hexdigest(),
        'strain_header_sha256':hashlib.sha256(header.encode()).hexdigest(),'masks':masks}
    del data
cores=[s for s in cores if s in eligible]
out['offsource_core_starts_gps']=cores
out['training_core_starts_gps']=cores[:12]
out['reference_core_starts_gps']=cores[12:]
out['excluded_for_metadata']=[s for s in out['proposed_offsource_core_starts_gps'] if s not in eligible]
out['calibration']={}
for det, archive, member in [
 ('H1','LIGO_O2_cal_uncertainty.tgz','H1/Feb-22-2018_O2_LHO_GPSTime_1187008882_C02_RelativeResponseUncertainty_FinalResults.txt'),
 ('L1','LIGO_O2_cal_uncertainty.tgz','L1/Feb-22-2018_O2_LLO_GPSTime_1187008882_C02_RelativeResponseUncertainty_FinalResults.txt'),
 ('V1','Virgo_O2_cal_uncertainty.tgz','V1/V_calibrationUncertaintyEnvelope_magnitude5p1percent_phase40mraddeg20microsecond.txt')]:
    with tarfile.open(cache/archive) as tar:
        raw=tar.extractfile(member).read()
    import io
    a=np.loadtxt(io.BytesIO(raw)); assert a.shape[1]==7
    z=a[(a[:,0]>=30)&(a[:,0]<=500)]
    med=z[:,1]*np.exp(1j*z[:,2])
    out['calibration'][det]={'member':member,'sha256':hashlib.sha256(raw).hexdigest(),
       'rows':len(a),'sampled_band_rows':len(z),'sampled_band_endpoints_hz':z[[0,-1],0].tolist(),
       'max_sampled_median_true_over_model_distance':float(np.max(abs(med-1))),
       'max_sampled_median_model_over_true_distance':float(np.max(abs(1/med-1))),
       'sampled_pointwise_1sigma_extrema':{'magnitude_lower':float(z[:,3].min()),'magnitude_upper':float(z[:,5].max()),
           'phase_lower_rad':float(z[:,4].min()),'phase_upper_rad':float(z[:,6].max())},
       'joint_coverage_or_hard_bound':False}
out['controls']={'gps_start':1187008512,'duration':4096,'rate_hz':4096,'core_seconds':90,'padding_each_side_seconds':4,
 'all_support_DQ127':True,'all_support_no_transient_injections':True,'CW_free_HL':False,
 'hardware_CW_retained_for_background_screen_only':True,'event_strain_inspected':False}
print(json.dumps(out,indent=2,sort_keys=True))
