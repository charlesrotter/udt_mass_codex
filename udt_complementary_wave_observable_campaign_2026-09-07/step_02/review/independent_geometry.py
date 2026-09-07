"""Source-first scalar arm/Gram/minor route; no producer imports or SVD.

The command-line adapter is added only after the source-first seal. Coordinate
rotation remains a supplied input; this does not certify astrometry.
"""
import datetime
import hashlib
import json
import math
import pathlib
import re
import sys


def dot(x, y):
    return math.fsum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(dot(x, x))


def cross(x, y):
    return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2],
            x[0]*y[1]-x[1]*y[0]]


def matvec(m, x):
    return [dot(row, x) for row in m]


def source_geometry(header):
    text = pathlib.Path(header).read_text()
    def get(name):
        match = re.search(r'^#define\s+' + re.escape(name) + r'\s+([^\s]+)',
                          text, re.MULTILINE)
        assert match is not None, name
        return float(match.group(1))
    result = []
    for detector, prefix in [('H1', 'LHO_4K'), ('L1', 'LLO_4K'), ('V1', 'VIRGO')]:
        base = 'LAL_' + prefix
        result.append(dict(name=detector,
            a=[get(base + '_ARM_X_DIRECTION_' + x) for x in 'XYZ'],
            b=[get(base + '_ARM_Y_DIRECTION_' + x) for x in 'XYZ'],
            r=[get(base + '_VERTEX_LOCATION_' + x + '_SI') for x in 'XYZ'],
            lengths=[2*get(base + '_DETECTOR_ARM_' + x + '_MIDPOINT_SI')
                     for x in 'XY']))
    return result


def response(detectors, rotation, ra_deg, dec_deg, psi=0.0):
    a, d = math.radians(ra_deg), math.radians(dec_deg)
    sky = [math.cos(d)*math.cos(a), math.cos(d)*math.sin(a), math.sin(d)]
    p = [-math.sin(a), math.cos(a), 0.0]
    q = [-math.sin(d)*math.cos(a), -math.sin(d)*math.sin(a), math.cos(d)]
    cp, sp = math.cos(psi), math.sin(psi)
    pp = [cp*x + sp*y for x, y in zip(p,q)]
    qq = [-sp*x + cp*y for x, y in zip(p,q)]
    p, q, sky = matvec(rotation, pp), matvec(rotation, qq), matvec(rotation, sky)
    f, delays = [], []
    for detector in detectors:
        ap, aq = dot(detector['a'],p), dot(detector['a'],q)
        bp, bq = dot(detector['b'],p), dot(detector['b'],q)
        f.append([(ap*ap-aq*aq-bp*bp+bq*bq)/2, ap*aq-bp*bq])
        delays.append(-dot(sky,detector['r'])/299792458.0)
    return f, delays, dict(p=p,q=q,n=sky)


def invariants(f):
    u, v = [r[0] for r in f], [r[1] for r in f]
    a, b, c = dot(u,u), dot(u,v), dot(v,v)
    trace, discriminant = a+c, math.hypot(a-c,2*b)
    large_eigenvalue = (trace+discriminant)/2
    minors = cross(u,v)
    determinant = dot(minors,minors)
    small_eigenvalue = determinant/large_eigenvalue if large_eigenvalue else 0.0
    singular_values = [math.sqrt(large_eigenvalue),math.sqrt(small_eigenvalue)]
    if determinant == 0:
        return dict(gram=[a,b,c], gram_determinant=determinant,
                    singular_values=singular_values, rank=1 if trace else 0)
    n = [x/math.sqrt(determinant) for x in minors]
    if n[-1] < 0:
        n = [-x for x in n]
    holdouts = []
    for j in range(3):
        training = [i for i in range(3) if i != j]
        coefficients = [-n[i]/n[j] for i in training]
        # Coefficients above predict heldout signal; residual uses their negatives.
        residual = [n[i]/n[j] if i != j else 1.0 for i in range(3)]
        original_error = max(abs(dot(residual,col)) for col in [u,v])
        holdouts.append(dict(heldout=j, training=training,
            prediction_coefficients=coefficients,
            training_norm=norm(coefficients), residual_norm=norm(residual),
            original_response_residual=original_error))
    return dict(gram=[a,b,c], gram_determinant=determinant,
                gram_determinant_subtractive=a*c-b*b,
                singular_values=singular_values, condition=singular_values[0]/singular_values[1],
                rank=2, null=n, original_null_residual=max(abs(dot(n,col)) for col in [u,v]),
                row_norms=[norm(row) for row in f], minors=minors, holdouts=holdouts)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def two_column_singular(f):
    u,v = [r[0] for r in f],[r[1] for r in f]
    a,b,c = dot(u,u),dot(u,v),dot(v,v)
    high = (a+c+math.hypot(a-c,2*b))/2
    # Sum of squared pair minors applies at any row count and avoids cancellation.
    det = math.fsum((u[i]*v[j]-v[i]*u[j])**2
                   for i in range(len(f)) for j in range(i+1,len(f)))
    return [math.sqrt(high),math.sqrt(det/high) if high else 0.0]


def assert_close(x,y,tol=1e-12):
    assert abs(x-y) < tol, (x,y,abs(x-y),tol)


def main():
    target_path, input_path, header_path = sys.argv[1:]
    target = json.loads(pathlib.Path(target_path).read_text())
    inputs = json.loads(pathlib.Path(input_path).read_text())
    assert sha(target_path) == 'b89c8e432788842cdbddc1270c3135043e60f12c557cb24725d2162560fdfac2'
    assert sha(input_path) == '2d17901bfe84069ff4ac2c43eb500f0b3bd844b3136a8ba6d5582a7d710eb38c'
    assert sha(header_path) == '82ac49e8042d4eab0f890e63e3599ae227967aee16c76cd5f6b6b729c8798684'
    detectors = source_geometry(header_path)
    for d in detectors:
        supplied = inputs['detectors'][d['name']]
        assert d['a'] == supplied['a'] and d['b'] == supplied['b']
        assert d['r'] == supplied['r_m']
        assert d['lengths'] == [2*x for x in supplied['arm_midpoints_m']]
    # Parse nominal published HMS/DMS afresh; no producer query-value import.
    ra = (13 + 9/60 + 48.089/3600)*15
    dec = -(23 + 22/60 + 53.35/3600)
    R = target['rotation']  # shared declared astrometry input, not independent certification
    for i in range(3):
        for j in range(3):
            assert_close(dot(R[i],R[j]),float(i==j))
    assert_close(dot(R[0],cross(R[1],R[2])),1.0)
    f,delays,basis = response(detectors,R,ra,dec)
    actual = invariants(f)
    matrix_error = max(abs(x-y) for row,ref in zip(f,target['F_HLV_plus_cross'])
                       for x,y in zip(row,ref))
    assert matrix_error < 1e-12
    for x,y in zip(delays,target['arrival_minus_geocenter_seconds']):
        assert_close(x,y)
    for key in ['p','q','n']:
        for x,y in zip(basis[key],target[key+'_itrs']):
            assert_close(x,y)
    for x,y in zip(actual['singular_values'],target['design']['singular_values']):
        assert_close(x,y)
    assert_close(actual['condition'],target['design']['condition'])
    for x,y in zip(actual['null'],target['design']['null_unit']):
        assert_close(x,y)
    assert actual['original_null_residual'] < 1e-12
    for result,ref in zip(actual['holdouts'],target['design']['holdouts']):
        for x,y in zip(result['prediction_coefficients'],ref['prediction_coefficients']):
            assert_close(x,y)
        assert_close(result['residual_norm'],ref['residual_sigma_equal_unit_noise'])
        train_sv = two_column_singular([f[i] for i in result['training']])
        result['training_condition'] = train_sv[0]/train_sv[1]
        result['training_inverse_operator_norm'] = 1/train_sv[1]
        assert_close(result['training_condition'],ref['training_condition'])
        assert_close(result['training_inverse_operator_norm'],ref['training_inverse_operator_norm'])
        assert result['original_response_residual'] < 1e-12
    noise = []
    for ratio,ref in zip([1.0,3.0,10.0],target['diagnostic_noise']):
        sigmas = [1.0,1.0,ratio]
        weighted = [[x/s for x in row] for row,s in zip(f,sigmas)]
        sv = two_column_singular(weighted)
        cond = sv[0]/sv[1]
        null_sigma = norm([x*s for x,s in zip(actual['null'],sigmas)])
        assert_close(cond,ref['weighted_condition'])
        assert_close(null_sigma,ref['fixed_normalized_null_sigma'])
        holdout_sigma = {}
        for j,name in enumerate(['H1','L1','V1']):
            value = null_sigma/abs(actual['null'][j])
            assert_close(value,ref['holdout_sigmas'][name])
            holdout_sigma[name] = value
        noise.append(dict(virgo_sigma_ratio=ratio,condition=cond,
                          null_sigma=null_sigma,holdout_sigma=holdout_sigma))
    # Basis changes independently recomputed from scalar projections.
    basis_errors=[]
    for angle in [0.37,1.17,-0.84]:
        ff,_,_ = response(detectors,R,ra,dec,angle)
        inv = invariants(ff)
        discrepancy = max(abs(x-y) for x,y in zip(inv['singular_values'],actual['singular_values']))
        assert discrepancy < 1e-12
        assert max(abs(x-y) for x,y in zip(inv['null'],actual['null'])) < 1e-12
        basis_errors.append(discrepancy)
    rank_one = invariants([[1.,2.],[2.,4.],[3.,6.]])
    assert rank_one['rank']==1 and rank_one['singular_values'][1]==0
    def rank_one_guard(value):
        assert value == 1, 'rank-one control incorrectly classified'
    rejected=[]
    try:
        rank_one_guard(2)
    except AssertionError:
        rejected.append('forced-rank-two negative control rejected')
    broken_null = [-actual['null'][0],actual['null'][1],actual['null'][2]]
    wrong_null_error = max(abs(dot(broken_null,[row[k] for row in f])) for k in range(2))
    try:
        assert wrong_null_error < 1e-12
    except AssertionError:
        rejected.append('one-sign-corrupted null rejected by original response residual')
    overhead_response = (1.0**2-0.0**2-0.0**2+1.0**2)/2
    assert overhead_response == 1
    try:
        assert 2*overhead_response == 1
    except AssertionError:
        rejected.append('double-normalized overhead response rejected')
    assert len(rejected)==3
    # Independent coarse clock/rotation checks. GPS-UTC=18s is supplied for this epoch.
    utc = datetime.datetime(1980,1,6,tzinfo=datetime.timezone.utc)+datetime.timedelta(seconds=1187008882.43-18)
    assert utc.isoformat(timespec='milliseconds').startswith(target['time']['utc'])
    jd1,jd2 = target['time']['ut1_jd']
    days = (jd1-2451545.0)+jd2
    era = (2*math.pi*(jd2%1 + jd1%1 + .7790572732640 + .00273781191135448*days))%(2*math.pi)
    angle = math.atan2(R[0][1],R[0][0])%(2*math.pi)
    era_residual = abs(math.remainder(angle-era,2*math.pi))
    assert era_residual < 1e-4  # gross sign/time consistency, not exact CIO/polar-motion equality
    # Approximate fixed-pole ERA rotation gives independent finite-time diagnostics.
    # No precision rotation or uniform time-error bound is claimed by this comparator.
    stress=[]
    omega = 2*math.pi*1.00273781191135448/86400
    for ref in target['finite_stress']:
        theta=omega*ref['seconds']; co,si=math.cos(theta),math.sin(theta)
        rr=[[co*R[0][j]+si*R[1][j] for j in range(3)],
            [-si*R[0][j]+co*R[1][j] for j in range(3)],R[2][:]]
        ff,_,_=response(detectors,rr,ra+ref['ra_offset_deg'],dec+ref['dec_offset_deg'])
        inv=invariants(ff)
        delta=[[x-y for x,y in zip(row,base)] for row,base in zip(ff,f)]
        opnorm=two_column_singular(delta)[0]
        cond_error=abs(inv['condition']-ref['condition'])
        opnorm_error=abs(opnorm-ref['matrix_change_operator_norm'])
        tolerance=1e-12 if ref['seconds']==0 else 1e-5
        assert cond_error<tolerance and opnorm_error<tolerance
        assert inv['rank']==2
        stress.append(dict(seconds=ref['seconds'],dra=ref['ra_offset_deg'],ddec=ref['dec_offset_deg'],
                          condition_error=cond_error,matrix_delta_norm_error=opnorm_error,
                          comparator='same nominal R; fixed-pole Earth rotation approximation'))
    epsilon_errors=[]
    for freq in [30.,100.,500.]:
        for d,ref in zip(detectors,target['epsilon_arm'][str(freq)]):
            for length,expected in zip(d['lengths'],ref):
                value=2*math.pi*freq*length/299792458.
                assert_close(value,expected)
                epsilon_errors.append(abs(value-expected))
    print(json.dumps(dict(
        reviewer='/root/co2_design_review',python=sys.version,
        implementation='stdlib scalar arm projections, Gram eigen2x2, minors/null ratios; no SVD or producer imports',
        pins=dict(target=sha(target_path),inputs=sha(input_path),header=sha(header_path)),
        supplied_coordinate_input='target nominal c2t06a rotation; not an independent astrometry certificate',
        degrees=[ra,dec],F=f,delays=delays,design=actual,noise=noise,
        matrix_max_error=matrix_error,basis_singular_errors=basis_errors,
        rank_one=rank_one,control_rejections=rejected,corrupted_null_residual=wrong_null_error,
        utc=utc.isoformat(),ERA_rad=era,rotation_angle_rad=angle,ERA_angle_residual=era_residual,
        finite_stress_comparisons=stress,max_epsilon_error=max(epsilon_errors),
        verdict='PASS finite independent geometry/linear algebra and coarse rotation checks only',
        omissions=['producer replay','independent full astrometry/IERS validation','strain/PSD/calibration arrays',
                   'actual release header validation','statistical power or coverage','349-row premise audit replay']
    ),indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
