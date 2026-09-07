"""Source-first independent finite checks; no observed sample input."""
import json
import platform
from pathlib import Path
import numpy as np

repo = Path(__file__).resolve().parents[3]
design = json.loads((repo / 'udt_complementary_wave_observable_campaign_2026-09-07/step_02/design_run.stdout').read_text())
F = np.array(design['F_HLV_plus_cross'])
det = F[0, 0]*F[1, 1]-F[0, 1]*F[1, 0]
b = np.array([-(F[2, 0]*F[1, 1]-F[2, 1]*F[1, 0])/det,
              -(F[0, 0]*F[2, 1]-F[0, 1]*F[2, 0])/det, 1.])

# Small discrete model: dense complex DFT, no FFT or author implementation.
n = 96
fs = 96.
t = np.arange(n)
freq = np.fft.fftfreq(n, 1/fs)
W = np.exp(-2j*np.pi*np.outer(t, t)/n)
P = np.ones(n)
P[[0, n//2]] = 0
tau = np.array(design['arrival_minus_geocenter_seconds'])
As = [W.conj().T @ np.diag(P*np.exp(2j*np.pi*freq*d)) @ W/n for d in tau]
invAs = [a.conj().T for a in As]
Pm = W.conj().T @ np.diag(P) @ W/n
rng = np.random.default_rng(541312)
h = np.real(rng.normal(size=(2, n)) @ Pm.T)
raw = np.array([np.real(invAs[i] @ (F[i] @ h)) for i in range(3)])
aligned = np.array([np.real(As[i] @ raw[i]) for i in range(3)])
denom = np.linalg.norm(aligned)
residual = b @ aligned
wrong_sign = b @ np.array([np.real(invAs[i] @ raw[i]) for i in range(3)])
wrong_b = b.copy()
wrong_b[0] = 0
early_window = np.hanning(n+1)[:-1]
wrong_taper = b @ np.array([np.real(As[i] @ (early_window*raw[i])) for i in range(3)])
ratio = lambda x: float(np.linalg.norm(x)/denom)
measured = {'correct_relative': ratio(residual), 'wrong_sign_relative': ratio(wrong_sign),
            'omit_H_relative': ratio(wrong_b @ aligned), 'premature_taper_relative': ratio(wrong_taper)}
checks = {'matrix_original_relative': float(np.linalg.norm(b @ F)/(np.linalg.norm(b)*np.linalg.norm(F))) < 1e-14,
          'correct_finite_operator': measured['correct_relative'] < 1e-10,
          'wrong_sign_rejected': measured['wrong_sign_relative'] > 1e-3,
          'omitted_H_rejected': measured['omit_H_relative'] > 1e-3,
          'premature_taper_noncommutation': measured['premature_taper_relative'] > 1e-3}

# Direct periodogram/Parseval and weighted real quadratic identity, independent
# of rFFT and any author PSD helper. Check scale cancellation at physical units.
m = 80
U = np.exp(-2j*np.pi*np.outer(np.arange(m), np.arange(m))/m)
w = (1-np.cos(2*np.pi*np.arange(m)/m))/2
r, s = rng.normal(size=(2, m))
psd = np.exp(np.linspace(-2, 3, m//2-1))
selected = np.arange(1, m//2)
def spectral(x):
    return (U @ (w*x))[selected]
weights = 2/(fs*np.sum(w*w)*len(selected)*psd)
def Q(x):
    z = spectral(x)
    return float(np.sum(weights*(z.real*z.real+z.imag*z.imag)))
cross = float(np.real(np.sum(weights*spectral(r).conj()*spectral(s))))
a = .7
direct = Q(r+a*s)
expanded = Q(r)+2*a*cross+a*a*Q(s)
checks['quadratic_direct_identity'] = abs(direct-expanded)/direct < 1e-13
z = U @ (w*r)
parseval = float(np.sum(abs(z)**2)/m)
time_power = float(np.dot(w*r, w*r))
checks['direct_DFT_parseval'] = abs(parseval-time_power)/time_power < 1e-13
checks['periodic_Hann_norm'] = abs(np.dot(w,w)-3*m/8) < 1e-12
correct_variance = float(np.real(np.array([1, 1j]) @ np.array([[1, .5j], [-.5j, 1]]) @ np.array([1, -1j])))
checks['complex_covariance_row_conjugation'] = abs(correct_variance-3) < 1e-14
checks['absolute_strain_guard_false_pass'] = np.linalg.norm(wrong_sign*1e-22) < 1e-10 and ratio(wrong_sign) > 1e-3
checks['all_passed'] = all(checks.values())
print(json.dumps({'scope':'synthetic finite method checks only; source-first; no observed arrays',
                  'python': platform.python_version(), 'numpy': np.__version__,
                  'b_determinant': b.tolist(), 'measured': measured, 'checks': checks,
                  'Q_direct': direct, 'Q_expanded': expanded,
                  'complex_covariance_variance': correct_variance,
                  'threshold_min_crossings': int(np.ceil(.9*168)),
                  'conditional_rank_resolution': 1/22}, indent=2))
assert all(checks.values())

