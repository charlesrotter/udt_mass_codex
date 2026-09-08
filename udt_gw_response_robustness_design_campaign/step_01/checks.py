"""RD1 finite anchors and defect controls; no strain, fits or continuum certification."""
import hashlib
import json
import math
import os
import pathlib
import platform
from fractions import Fraction

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = pathlib.Path(__file__).resolve().parent
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    assert os.environ.get(key) == '1', key

F = np.array([[.07637694310459259, .8871504798012285],
              [.1329497294997055, -.7412364124394045],
              [-.15740052456055761, .25736508570623207]])
B = np.linalg.inv(F[:2])
S = F[2] @ B
bn, sn = np.linalg.norm(B, 2), np.linalg.norm(S)
assert np.linalg.norm(B @ F[:2] - np.eye(2)) < 1e-14
assert np.linalg.norm(S @ F[:2] - F[2]) < 1e-14

# Actual assertions that defective conclusions fail; never compare only booleans.
caught = []
def reject(name, assertion):
    try:
        assertion()
    except AssertionError:
        caught.append(name)
    else:
        raise AssertionError('defect falsely passed: ' + name)

def require(test):
    assert test

rng = np.random.Generator(np.random.PCG64(801209))
rows = []
for j in range(80):
    dt = rng.normal(size=(2, 2))
    dt *= .003 / np.linalg.norm(dt, 2)
    dv = rng.normal(size=2)
    dv *= .004 / np.linalg.norm(dv)
    nt, nv = rng.normal(size=2) * .002, float(rng.normal() * .002)
    # Wide amplitude range exposes inappropriate absolute tolerances.
    h = rng.normal(size=2) * 10.**((j % 9) - 4)
    yt, yv = (F[:2] + dt) @ h + nt, (F[2] + dv) @ h + nv
    kappa = np.linalg.norm(B @ dt, 2)
    rho = np.linalg.norm(dv - S @ dt)
    eta_b, eta_r = np.linalg.norm(B @ nt), abs(nv - S @ nt)
    hbound = (np.linalg.norm(B @ yt) + eta_b) / (1 - kappa)
    rbound = rho * hbound + eta_r
    hmargin, rmargin = hbound - np.linalg.norm(h), rbound - abs(yv - S @ yt)
    assert hmargin >= -1e-12 * max(hbound, np.linalg.norm(h))
    assert rmargin >= -1e-12 * max(rbound, abs(yv - S @ yt))
    rows.append(dict(kappa=float(kappa), hmargin=float(hmargin), rmargin=float(rmargin)))

# Dropping waveform amplitude is a real false pass at a rescaled valid input.
hh = np.array([1e4, 0.])
dv = np.array([.01, 0.])
leakage = abs(dv @ hh)
reject('amplitude_free_error', lambda: require(leakage <= np.linalg.norm(dv)))
assert leakage == 100.

# Common response need not leak in the fixed model; training inequality can fail
# as a sufficient bound without declaring model absence.
C = np.array([[1.01, .02], [0., .99]])
assert np.linalg.norm(F[2] @ C - S @ F[:2] @ C) < 1e-14
yt = np.zeros(2)
yv = 1.
assert abs(yv - S @ yt) > 0.  # Nonvacuity at zero budgets.
rank_one_training = np.array([[1., 0.]])
rank_one_holdout = np.array([[2., 0.]])
assert np.linalg.matrix_rank(rank_one_training) == 1
assert np.linalg.norm(rank_one_training @ np.array([0., 1.])) == 0
for hidden in (-100., 0., 100.):
    test_h = np.array([3., hidden])
    assert np.linalg.norm(rank_one_holdout @ test_h - 2*rank_one_training @ test_h) == 0

# Exact finite noncommutation and common-window spectral mixing anchors.
signals = [Fraction(1), Fraction(1)]
common_average = sum(signals) / 2
null_at_second = [-Fraction(1), Fraction(1)]
# Channel1 h(t)=1; channel2 t*h(t)=(0,1). Average first then null at t=1.
mixed = null_at_second[0] * common_average + null_at_second[1] * Fraction(1, 2)
assert mixed == -Fraction(1, 2)
reject('varying_response_commutes_with_common_filter', lambda: require(mixed == 0))
n = 16
index = np.arange(n)
out_of_band = np.exp(2j * np.pi * 3 * index / n)
window = np.cos(2 * np.pi * index / n)
before = np.fft.fft(out_of_band) / n
after = np.fft.fft(window * out_of_band) / n
assert abs(before[2]) < 1e-14 and abs(after[2] - .5) < 1e-14
reject('retained_band_bounds_windowed_signal', lambda: require(abs(after[2]) < 1e-14))

# Kernel examples. Analytic proof, not sampled eigenvalues, establishes positivity.
def kernel(s, a=1., b=4.):
    s = np.asarray(s)
    return 2*b*np.sinc(2*b*s) - 2*a*np.sinc(2*a*s)

times = np.array([0., .08, .21, .39])
gram = kernel(times[:, None] - times[None, :])
v = np.array([.2, -.1, .7, -.3])
coeff = np.linalg.solve(gram, v)
replay = gram @ coeff
interpolation_error = np.linalg.norm(replay-v)/np.linalg.norm(v)
assert interpolation_error < 1e-12
assert np.linalg.eigvalsh(gram)[0] > 0

# Independent frequency quadrature check of the kernel interpolant's norm.
freq = np.linspace(1., 4., 20001)
hat = np.exp(-2j*np.pi*freq[:, None]*times) @ coeff
quadrature_norm2 = float(2*np.trapezoid(abs(hat)**2, freq))
exact_norm2 = float(v @ coeff)
assert abs(quadrature_norm2/exact_norm2-1) < 1e-7

# Schur-complement conditional holdout range; inspect both attainable endpoints.
g = gram[:3, :3]
q = gram[:3, 3]
train = v[:3]
h0_norm2 = float(train @ np.linalg.solve(g, train))
prediction = float(q @ np.linalg.solve(g, train))
p_norm2 = float(gram[3, 3] - q @ np.linalg.solve(g, q))
assert p_norm2 > 0
hmax = math.sqrt(h0_norm2 + .4)
radius = math.sqrt(p_norm2 * (hmax*hmax-h0_norm2))
endpoint_norms = []
for sign in (-1, 1):
    target = np.r_[train, prediction + sign*radius]
    norm2 = float(target @ np.linalg.solve(gram, target))
    assert abs(norm2/(hmax*hmax)-1) < 1e-12
    endpoint_norms.append(norm2)
reject('training_uniquely_fixes_distinct_holdout', lambda: require(radius == 0))

taus = [Fraction('0.018826632251513074'), Fraction('0.015560840809109985'),
        Fraction('-0.006330543633799644')]
separations = []
for i in range(3):
    for j in range(i):
        delta = (taus[i] - taus[j]) * 4096
        assert delta.denominator != 1
        separations.append(str(delta))
assert np.all(F[:, 0] != 0)

# Source-form arm expression (NumPy normalized sinc) and analytic-bound anchors.
def transfer(x, mu):
    return .5*(np.exp(1j*x*(1-mu))*np.sinc(x*(1+mu)/np.pi)
               + np.exp(-1j*x*(1+mu))*np.sinc(x*(1-mu)/np.pi))

arm_max_excess = -math.inf
for x in (-3., -.1, -.02, 0., .02, .1, 3.):
    for mu in np.linspace(-1, 1, 41):
        t = transfer(x, mu)
        bound = min(2., 2*abs(x), abs(x*mu)+(2/3)*x*x*(1+mu*mu))
        excess = abs(t-1)-bound
        arm_max_excess = max(arm_max_excess, float(excess))
        assert excess <= 2e-14 and abs(t) <= 1+2e-14
    assert abs(transfer(x, 0) - np.sinc(2*x/np.pi)) < 1e-14
x = math.pi*500*4000/299792458.
reject('extra_pi_convention', lambda: require(abs(transfer(x,.6)-transfer(math.pi*x,.6)) < 1e-12))
xl, xv = x, math.pi*500*3000/299792458.
el, ev = xl+4*xl*xl/3, xv+4*xv*xv/3
kt, rr = bn*math.sqrt(2)*el, ev+sn*math.sqrt(2)*el
assert kt < 1

print(json.dumps(dict(
    passed=True, scope='Finite checks; general proofs in candidate; no empirical certificate',
    python=platform.python_version(), numpy=np.__version__, dtype='float64/complex128; Fraction controls',
    seed=801209, source_script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    shapes=dict(F=list(F.shape), kernel_gram=list(gram.shape), quadrature=len(freq)),
    tolerances=dict(operator=1e-14, leakage_relative=1e-12, quadrature_relative=1e-7),
    B_norm=float(bn), S=S.tolist(), S_norm=float(sn), sufficient_delta_T_threshold=float(1/bn),
    leakage_cases=rows, defects_actually_rejected=caught,
    window_mixing=dict(before=float(abs(before[2])), after=float(abs(after[2]))),
    interpolation=dict(relative_residual=float(interpolation_error), norm_squared=exact_norm2,
                       quadrature_norm_squared=quadrature_norm2, min_eigenvalue=float(np.linalg.eigvalsh(gram)[0])),
    holdout=dict(h0_norm_squared=h0_norm2, prediction=prediction, p_norm_squared=p_norm2,
                 H_max=hmax, sharp_radius=radius, endpoint_norm_squared=endpoint_norms),
    asynchronous_nominal_fractional_sample_differences=separations,
    arm=dict(max_sampled_bound_excess=arm_max_excess, nominal_LIGO_row_bound=el,
             nominal_Virgo_row_bound=ev, arm_only_kappa=float(kt), arm_only_rho=float(rr)),
    data_exposure='No strain or new support; exact nominal constants only'
), sort_keys=True, indent=2))
