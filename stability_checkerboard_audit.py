"""STEP 1 of the corrected-operator plan (Charles + collaborating AI, 2026-07-11): audit the negative
Hessian eigenvectors for CHECKERBOARD / Nyquist content. The energy AND hopf_charge use the centered
first difference D^c f=(f_{i+1}-f_{i-1})/2h (fs_hopfion.py:48), which ANNIHILATES the checkerboard mode
f_i=(-1)^i exactly. If the negative cluster lives in that null, it is an OPERATOR artifact (a change to
384^3 does NOT remove an exact Nyquist null), not a physical/continuum instability.

Diagnostics per eigenvector v (v, v1, v2 = the three converged negative modes):
  R_cb(v) = sum_ax||D^c_ax v||^2 / sum_ax||D^+_ax v||^2       (forward diff D^+ f=(f_{i+1}-f_i)/h has NO
             null) -- SMALL R_cb => the mode is invisible to the centered operator => checkerboard-like.
  nyq     = fraction of spectral power with max_ax|k_ax| > 0.9 k_Nyquist (power piled on the Nyquist faces).
  stag    = ||low-pass( v * (-1)^{i+j+k} )|| / ||v||  -- large => v IS a modulated checkerboard.
  theta_max on the carrier n0 (max nearest-neighbor angle) for context.
Calibrated against a SMOOTH reference (R_cb~1, nyq~0) and a PURE-CHECKERBOARD reference (R_cb~0, nyq~1)."""
import sys, json, numpy as np, torch
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
torch.set_default_dtype(torch.float64); dev = m.dev

Z = np.load('stability_lowmode_256.npz')
N = int(Z['N']); L = float(Z['L']); h = float(Z['h'])
vecs = {'v(lam=%.1f)' % float(Z['lam_phys']): torch.tensor(Z['v'], device=dev),
        'v1(lam=%.1f)' % float(Z['lam1_phys']): torch.tensor(Z['v1'], device=dev),
        'v2(lam=%.1f)' % float(Z['lam2_phys']): torch.tensor(Z['v2'], device=dev)}
n0 = torch.tensor(np.load('controlled_best_field.npz')['n'], device=dev)
n0 = n0 / n0.norm(dim=0, keepdim=True)

def Dc(f, ax): return (torch.roll(f, -1, ax) - torch.roll(f, 1, ax)) / (2 * h)   # centered (has Nyquist null)
def Dp(f, ax): return (torch.roll(f, -1, ax) - f) / h                            # forward  (no null)
ii = torch.arange(N, device=dev)
IX, IY, IZ = torch.meshgrid(ii, ii, ii, indexing='ij')
sgn = ((IX + IY + IZ) % 2 == 0).double() * 2 - 1                                 # (-1)^{i+j+k}
kk = 2 * np.pi * torch.fft.fftfreq(N, d=h).to(dev); knyq = np.pi / h
KX, KY, KZ = torch.meshgrid(kk, kk, kk, indexing='ij')
kmax_ax = torch.maximum(torch.maximum(KX.abs(), KY.abs()), KZ.abs())
nyq_mask = (kmax_ax > 0.9 * knyq)

def R_cb(v):                                     # v: (3,N,N,N)
    num = sum((Dc(v[c], a)**2).sum() for c in range(3) for a in range(3))
    den = sum((Dp(v[c], a)**2).sum() for c in range(3) for a in range(3))
    return float(num / (den + 1e-300))
def nyq_frac(v):
    p = sum((torch.fft.fftn(v[c]).abs()**2) for c in range(3))
    return float(p[nyq_mask].sum() / (p.sum() + 1e-300))
def stag(v):                                     # ||low-pass(v * (-1)^{i+j+k})|| / ||v||
    tot = 0.0
    for c in range(3):
        w = torch.fft.fftn(v[c] * sgn)
        w[kmax_ax > 0.5 * knyq] = 0                                              # keep only low-k content
        tot += float((torch.fft.ifftn(w).real**2).sum())
    return float((tot / (float((v**2).sum()) + 1e-300))**0.5)
def theta_max(nn):
    mx = 0.0
    for a in range(3):
        dot = (nn * torch.roll(nn, -1, a + 1)).sum(0).clamp(-1, 1)
        mx = max(mx, float(torch.arccos(dot).max()))
    return mx

# calibration references
torch.manual_seed(0)
env = torch.exp(-((IX - N / 2)**2 + (IY - N / 2)**2 + (IZ - N / 2)**2) / (2 * (N / 8)**2))
smooth = torch.stack([env * torch.cos(2 * np.pi * IX / (N / 4)) for _ in range(3)], 0)
cb = torch.stack([env * sgn for _ in range(3)], 0)                               # pure checkerboard * envelope
print("=== CALIBRATION ===", flush=True)
print(f"  SMOOTH ref:       R_cb={R_cb(smooth):.4f}  nyq={nyq_frac(smooth):.4f}  stag={stag(smooth):.4f}")
print(f"  CHECKERBOARD ref: R_cb={R_cb(cb):.4f}  nyq={nyq_frac(cb):.4f}  stag={stag(cb):.4f}")
print(f"\n=== CARRIER n0: theta_max(nearest-neighbor) = {theta_max(n0):.4f} rad ===")
print("\n=== NEGATIVE EIGENVECTORS ===", flush=True)
out = {'calibration': {'smooth_R_cb': R_cb(smooth), 'cb_R_cb': R_cb(cb),
                       'smooth_nyq': nyq_frac(smooth), 'cb_nyq': nyq_frac(cb)},
       'carrier_theta_max': theta_max(n0), 'modes': {}}
for name, v in vecs.items():
    r = R_cb(v); ny = nyq_frac(v); st = stag(v)
    verdict = 'CHECKERBOARD-DOMINATED' if r < 0.2 else ('checkerboard-contaminated' if r < 0.6 else 'smooth-dominated')
    print(f"  {name:16s}  R_cb={r:.4f}  nyq={ny:.4f}  stag={st:.4f}  -> {verdict}", flush=True)
    out['modes'][name] = {'R_cb': r, 'nyq_frac': ny, 'stag': st, 'verdict': verdict}
json.dump(out, open('stability_checkerboard_audit_out.json', 'w'), indent=1)
print("\nsaved stability_checkerboard_audit_out.json")
