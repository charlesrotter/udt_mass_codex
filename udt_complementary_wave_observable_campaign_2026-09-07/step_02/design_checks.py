"""Finite static network design; no strain arrays, PSD estimates, or source fit."""
import hashlib
import importlib.metadata
import itertools
import json
import math
from pathlib import Path
import platform
import re
import sys

import astropy
from astropy import units as u
from astropy.time import Time, TimeDelta
from astropy.utils import iers
import erfa
import numpy as np

ROOT = Path(__file__).resolve().parent
raw = (ROOT / 'design_inputs.json').read_bytes()
inp = json.loads(raw)
tol = inp['controls']['numeric_tolerance']
names = inp['detector_order']
det = [inp['detectors'][k] for k in names]
arms = np.asarray([[x['a'], x['b']] for x in det], dtype=np.float64)
positions = np.asarray([x['r_m'] for x in det], dtype=np.float64)
lengths = 2*np.asarray([x['arm_midpoints_m'] for x in det], dtype=np.float64)
source_verified = False
if len(sys.argv) == 2:
    source = Path(sys.argv[1]).read_bytes()
    assert hashlib.sha256(source).hexdigest() == inp['source_sha256']
    constants = dict(re.findall(rb'^#define\s+(LAL_\w+)\s+([-+0-9.eE]+)\s', source, re.M))
    for d in det:
        prefix = 'LAL_' + d['source_prefix']
        for i, xyz in enumerate('XYZ'):
            for axis, key in [('X', 'a'), ('Y', 'b')]:
                assert float(constants[f'{prefix}_ARM_{axis}_DIRECTION_{xyz}'.encode()]) == d[key][i]
            assert float(constants[f'{prefix}_VERTEX_LOCATION_{xyz}_SI'.encode()]) == d['r_m'][i]
        for i, axis in enumerate('XY'):
            assert float(constants[f'{prefix}_DETECTOR_ARM_{axis}_MIDPOINT_SI'.encode()]) == d['arm_midpoints_m'][i]
    source_verified = True

# No downloads or permissive out-of-range IERS fallback.
iers.conf.auto_download = False
iers.conf.iers_degraded_accuracy = 'error'
table = iers.IERS_B.open(iers.IERS_B_FILE)
t0 = Time(inp['query']['gps'], format='gps')
ra = math.radians(15*sum(x/y for x,y in zip(inp['query']['ra_hms'], [1,60,3600])))
dec = -math.radians(sum(x/y for x,y in zip(inp['query']['dec_negative_dms'], [1,60,3600])))
c = inp['controls']['c_E_m_per_s']
D = (np.einsum('ni,nj->nij', arms[:,0], arms[:,0])
     -np.einsum('ni,nj->nij', arms[:,1], arms[:,1]))/2
norm_errors = np.sum(arms*arms,axis=2)-1
assert np.max(np.abs(norm_errors)) < 1e-8

def geometry(ra0, dec0, seconds=0):
    t = t0+TimeDelta(seconds, format='sec')
    dut1, st = table.ut1_utc(t, return_status=True)
    xp, yp, sp = table.pm_xy(t, return_status=True)
    assert int(st) == iers.FROM_IERS_B and int(sp) == iers.FROM_IERS_B
    t.delta_ut1_utc = dut1.to_value(u.s)
    tt, ut1 = t.tt, t.ut1
    R = erfa.c2t06a(tt.jd1, tt.jd2, ut1.jd1, ut1.jd2, xp.to_value(u.rad), yp.to_value(u.rad))
    assert np.max(np.abs(R@R.T-np.eye(3))) < tol
    n = np.array([math.cos(dec0)*math.cos(ra0), math.cos(dec0)*math.sin(ra0), math.sin(dec0)])
    p = np.array([-math.sin(ra0),math.cos(ra0),0.0])
    q = np.cross(n,p)
    n,p,q = R@n, R@p, R@q
    assert np.max(np.abs(np.array([n,p,q])@np.array([n,p,q]).T-np.eye(3))) < tol
    ep, ec = np.outer(p,p)-np.outer(q,q), np.outer(p,q)+np.outer(q,p)
    F = np.array([[np.sum(d*ep),np.sum(d*ec)] for d in D])
    time_meta = dict(utc=t.utc.isot, tt_jd=[tt.jd1,tt.jd2], ut1_jd=[ut1.jd1,ut1.jd2],
                     dut1_seconds=float(dut1.to_value(u.s)), xp_rad=float(xp.to_value(u.rad)),
                     yp_rad=float(yp.to_value(u.rad)), iers_status=int(st))
    return F,n,p,q,R,time_meta

def summary(F):
    sv = np.linalg.svd(F,compute_uv=False)
    rank = int(np.sum(sv > inp['controls']['rank_threshold']))
    result = {'rank':rank, 'singular_values':sv.tolist()}
    if rank != 2:
        return result
    q = np.cross(F[:,0],F[:,1]); q /= np.linalg.norm(q)
    if q[-1] < 0:
        q = -q
    residual = float(np.max(np.abs(q@F)))
    assert residual < tol
    result.update(condition=float(sv[0]/sv[1]), null_unit=q.tolist(), null_residual=residual)
    holdouts = []
    for j in range(3):
        ids = [i for i in range(3) if i != j]
        ft = F[ids]
        coeff = np.linalg.solve(ft.T,F[j])
        assert np.max(np.abs(coeff@ft-F[j])) < tol
        b = np.zeros(3); b[j]=1; b[ids]=-coeff
        assert np.max(np.abs(b@F)) < tol
        holdouts.append(dict(heldout=names[j],training=[names[i] for i in ids],
            prediction_coefficients=coeff.tolist(), residual_row=b.tolist(),
            training_condition=float(np.linalg.cond(ft)),
            training_inverse_operator_norm=float(1/np.linalg.svd(ft,compute_uv=False)[-1]),
            residual_sigma_equal_unit_noise=float(np.linalg.norm(b))))
    result['holdouts'] = holdouts
    return result

F,n,p,q,R,tm = geometry(ra,dec)
base = summary(F)
assert base['rank'] == 2
# Polarization basis change cannot create or remove a signal/null direction.
angle = 0.37
pp,qq = math.cos(angle)*p+math.sin(angle)*q, -math.sin(angle)*p+math.cos(angle)*q
fp = np.array([[np.sum(d*(np.outer(pp,pp)-np.outer(qq,qq))),
                np.sum(d*(np.outer(pp,qq)+np.outer(qq,pp)))] for d in D])
assert np.max(np.abs(fp@fp.T-F@F.T)) < tol
assert np.max(np.abs(np.asarray(base['null_unit'])@fp)) < tol
# Known arm geometry anchors normalization independently of real-site output.
overhead = np.diag([0.5,-0.5,0.0])
eplus = np.diag([1.0,-1.0,0.0])
assert np.sum(overhead*eplus) == 1
assert np.sum(2*overhead*eplus) != 1  # actual wrong-factor comparator
rank1 = summary(np.array([[1.,0.],[2.,0.],[0.,0.]]))
assert rank1['rank'] == 1 and 'null_unit' not in rank1
# Frozen-delay sign is tied to phase t+n.r/c: t_arrival-t_geo=-n.r/c.
delays = -positions@n/c
assert np.max(np.abs(delays)) < 0.022

stress = []
for dt, dra, ddec in itertools.product(inp['controls']['time_offsets_seconds'],
                                     inp['controls']['ra_dec_stress_degrees'],
                                     inp['controls']['ra_dec_stress_degrees']):
    fs,*_ = geometry(ra+math.radians(dra),dec+math.radians(ddec),dt)
    ss = summary(fs)
    stress.append(dict(seconds=dt,ra_offset_deg=dra,dec_offset_deg=ddec,
                       rank=ss['rank'], condition=ss.get('condition'),
                       matrix_change_operator_norm=float(np.linalg.norm(fs-F,2))))
qnull = np.asarray(base['null_unit'])
noise = []
for ratio in inp['controls']['virgo_to_ligo_noise_sigma_ratios']:
    sigma = np.array([1.,1.,ratio])
    fw = F/sigma[:,None]
    noise.append(dict(sigma_HLV=sigma.tolist(),weighted_condition=float(np.linalg.cond(fw)),
        fixed_normalized_null_sigma=float(np.linalg.norm(qnull*sigma)),
        holdout_sigmas={h['heldout']:float(np.linalg.norm(np.asarray(h['residual_row'])*sigma))
                       for h in base['holdouts']}))
print(json.dumps(dict(
    evidence='finite float64 geometric design, no observational arrays or physical error certification',
    input_sha256=hashlib.sha256(raw).hexdigest(), official_source_decimal_match=source_verified,
    versions=dict(python=platform.python_version(),numpy=np.__version__,astropy=astropy.__version__,
                  pyerfa=erfa.__version__,iers_data=importlib.metadata.version('astropy-iers-data')),
    iers_file_sha256=hashlib.sha256(Path(iers.IERS_B_FILE).read_bytes()).hexdigest(),
    nominal_query_degrees=[math.degrees(ra),math.degrees(dec)], time=tm,
    rotation=R.tolist(), n_itrs=n.tolist(), p_itrs=p.tolist(), q_itrs=q.tolist(),
    F_HLV_plus_cross=F.tolist(), arm_norm_squared_errors=norm_errors.tolist(),
    arm_cross_dots=np.sum(arms[:,0]*arms[:,1],axis=1).tolist(), arm_lengths_m=lengths.tolist(),
    arrival_minus_geocenter_seconds=delays.tolist(), design=base, diagnostic_noise=noise,
    finite_stress=stress,
    epsilon_arm={str(f):(2*math.pi*f*lengths/c).tolist()
                 for f in inp['controls']['arm_control_frequencies_hz']},
    checks=dict(original_null_residual=True,holdout_original_residuals=True,
                polarization_basis_invariance=True,overhead_factor_anchor=True,
                rank_one_separator=True,iers_historical_not_extrapolated=True),
    scope='Static response and finite stress controls only; no measured PSD, statistical power, coverage, or release eligibility'
),indent=2,sort_keys=True))
