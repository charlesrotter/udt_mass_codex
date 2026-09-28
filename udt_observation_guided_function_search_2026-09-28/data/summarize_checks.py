#!/usr/bin/env python3
"""No new fits: summarize frozen sensitivities and finite release-schema diagnostics."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,gzip
import numpy as np
from scipy.spatial import cKDTree
import fit_empirical as fe

P=Path(__file__).resolve().parent;O=P/'results'


def main():
    d=np.genfromtxt(P/'raw/Pantheon+SH0ES.dat',names=True,dtype=None,encoding=None)
    with gzip.open(P/'raw/Pantheon+SH0ES_STAT+SYS.cov.gz','rt') as f:
        n=int(f.readline());raw=np.loadtxt(f).reshape(n,n)
    primary=(d['IS_CALIBRATOR']==0)&(d['zHD']>.023)
    masks={'primary':primary,'zgt0p01':(d['IS_CALIBRATOR']==0)&(d['zHD']>.01),
           'zgt0p05':(d['IS_CALIBRATOR']==0)&(d['zHD']>.05),'primary_zlt1':primary&(d['zHD']<1)}
    domains={k:[float(d['zHD'][v].min()),float(d['zHD'][v].max())] for k,v in masks.items()}
    full=json.loads((O/'full_fits.json').read_text());sens=json.loads((O/'sensitivity.json').read_text())
    zgrid=np.geomspace(max(v[0] for v in domains.values()),min(v[1] for v in domains.values()),400)
    def fr(s):return {'beta':np.array(s['beta']),'vc':np.array(s['parameter_covariance']),
                      'knots':np.log1p(s['knots_z']) if s['family']=='F4' else fe.KN}
    comparison=[]
    for s in sens:
        f=s['family'];c=fe.curves(f,zgrid,fr(s));baseline=fe.curves(f,zgrid,fr(full[f]))
        fractional=np.expm1(c['log_F_over_F_at_z0p1']-baseline['log_F_over_F_at_z0p1'])
        comparison.append({'variant':s['variant'],'family':f,
            'max_abs_fractional_relative_shape_change':float(np.max(np.abs(fractional))),
            'max_abs_d_logF_dx_change':float(np.max(np.abs(c['d_log_F_dx']-baseline['d_log_F_dx']))),
            'chi2':s['chi2'],'dof':s['dof'],'aicc':s['aicc_without_common_constant']})
    output={'sample_domains':domains,'comparison_grid':[float(zgrid[0]),float(zgrid[-1]),len(zgrid)],
            'comparison_normalization':'F(z)/F(.1), same as relative DL or DA shape departures',
            'sensitivity_json_note':'Its original fixed common_grid_curves include boundary z=.05 and1 that can sit just outside a cut sample. Use this exact common-data-domain summary for no-extrapolation comparisons.',
            'comparisons':comparison}
    fe.save_json(O/'sensitivity_summary.json',output)
    # Finite diagnostic declared here before observing matches: same sky within5 arcsec,
    # peak-date difference<10 days and redshift difference<.001 flags possible aliases.
    ra=np.deg2rad(d['RA']);dec=np.deg2rad(d['DEC']);xyz=np.column_stack([np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)])
    pairs=cKDTree(xyz).query_pairs(2*np.sin(np.deg2rad(5/3600)/2))
    aliases=[]
    for i,j in pairs:
        if d['CID'][i]!=d['CID'][j] and abs(d['PKMJD'][i]-d['PKMJD'][j])<10 and abs(d['zHD'][i]-d['zHD'][j])<.001:
            aliases.append({'i':i,'j':j,'CID_i':str(d['CID'][i]),'CID_j':str(d['CID'][j]),'both_primary':bool(primary[i] and primary[j])})
    finite_diags={'diagnostic_status':'post-fit source-schema check, no fit tuning',
        'possible_cross_CID_aliases_same_sky_time_redshift':aliases,
        'alias_criterion':'within5 arcsec, abs(PKMJD difference)<10 days, abs(zHD difference)<.001; not an exhaustive identity census',
        'CID_casefold_unique':len(set(str(c).casefold() for c in d['CID'])),
        'primary_covariance_raw_asymmetry_max_abs':float(np.max(np.abs((raw-raw.T)[np.ix_(primary,primary)]))),
        'official_covariance_used':'full STAT+SYS submatrix; plotting error column never used',
        'issue_sources':[]}
    for n in [6,10,13]:
        for suffix in ['', '_comments']:
            path=P/f'raw/issue_{n}{suffix}.json'
            finite_diags['issue_sources'].append({'path':str(path.relative_to(P)),
                'url':f'https://api.github.com/repos/PantheonPlusSH0ES/DataRelease/issues/{n}'+('/comments' if suffix else ''),
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    fe.save_json(O/'schema_diagnostic.json',finite_diags)
    print(json.dumps(output,indent=2));print(json.dumps(finite_diags,indent=2))


if __name__=='__main__':main()
