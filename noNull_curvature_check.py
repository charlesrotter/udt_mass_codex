"""STEP 3a (cheap, decisive): does the corrected no-null operator remove the NEGATIVE curvature along the
old Nyquist eigenvectors? For M-normalized v (v^T M v = h^3||v||^2 = 1), the quadratic form
    q(v) = [E(n0+eps v) + E(n0-eps v) - 2 E(n0)] / eps^2  ->  <v, H v> = lam_phys  as eps->0.
Compute q(v) for v, v1, v2 under BOTH the centered energy (should reproduce lam_phys ~ -290,-270,-236,
confirming the FD Hessian) and the no-null energy (expected: LARGE POSITIVE -- the Nyquist modes now cost
energy, so they are no longer unstable). Also verify the quadratic regime (q stable as eps decreases)."""
import sys, json, numpy as np, torch
sys.path.insert(0, 'hopfion_arc_scripts_2026-07-05')
import fs_hopfion as m
from noNull_energy import energy_noNull, energy_centered
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

d0 = np.load('controlled_best_field.npz'); n0 = torch.tensor(d0['n'], device=dev)
h = float(d0['h']); xi = float(d0['xi']); kap = float(d0['kappa'])
n0 = n0 / n0.norm(dim=0, keepdim=True)
Z = np.load('stability_lowmode_256.npz')
modes = {'v': (torch.tensor(Z['v'], device=dev), float(Z['lam_phys'])),
         'v1': (torch.tensor(Z['v1'], device=dev), float(Z['lam1_phys'])),
         'v2': (torch.tensor(Z['v2'], device=dev), float(Z['lam2_phys']))}

def Ec(nn): return float(energy_centered(nn, h, xi, kap)[0])
def En(nn): return float(energy_noNull(nn, h, xi, kap)[0])
E0c = Ec(n0); E0n = En(n0)
print(f"# carrier E_centered={E0c:.5f}  E_noNull={E0n:.5f}  h={h:.5f}", flush=True)
print(f"# q(v) = [E(+eps)+E(-eps)-2E0]/eps^2 -> lam_phys (M-normalized v)\n", flush=True)

out = {'E0_centered': E0c, 'E0_noNull': E0n, 'modes': {}}
for name, (v, lam_saved) in modes.items():
    print(f"=== {name}  (saved lam_phys from centered block-LOBPCG = {lam_saved:.2f}) ===", flush=True)
    rec = {'lam_saved_centered': lam_saved, 'centered': {}, 'noNull': {}}
    for eps in (2e-3, 1e-3, 5e-4):
        qc = (Ec(n0 + eps * v) + Ec(n0 - eps * v) - 2 * E0c) / eps**2
        qn = (En(n0 + eps * v) + En(n0 - eps * v) - 2 * E0n) / eps**2
        rec['centered'][f'{eps:.0e}'] = qc; rec['noNull'][f'{eps:.0e}'] = qn
        print(f"  eps={eps:.0e}   q_centered={qc:+.3e}   q_noNull={qn:+.3e}", flush=True)
    out['modes'][name] = rec
    print(flush=True)

print("SUMMARY (eps=5e-4):", flush=True)
for name in modes:
    qc = out['modes'][name]['centered']['5e-04']; qn = out['modes'][name]['noNull']['5e-04']
    flip = "NEGATIVE->POSITIVE (artifact removed)" if qc < 0 and qn > 0 else ("still negative" if qn < 0 else "?")
    print(f"  {name}: centered={qc:+.2f}  noNull={qn:+.2f}   {flip}", flush=True)
json.dump(out, open('noNull_curvature_check_out.json', 'w'), indent=1)
print("\nsaved noNull_curvature_check_out.json")
