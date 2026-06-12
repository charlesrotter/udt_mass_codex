import sys; sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import numpy as np
src = open('/home/udt-admin/udt_mass_codex/w4b_coupled.py').read()
head = src.split('# ====')[0]
exec(compile(head, 'h', 'exec'))
import w4b_evolib as ev
cp = Coupled('M1'); g = cp.geo
kc = float(lin['M1_kc'])
for kk in (2*kc, -1.0):
    for amp, sig in ((0.1,0.10),(0.05,0.25),(0.02,0.25),(0.01,0.25),(0.005,0.25),(0.02,0.10),(0.005,0.10)):
        v0 = ev.bump_profile(g, amp, 'g1', sig_frac=sig)
        wts = cp.w_on_ts(v0, np.zeros_like(v0))
        Xs = cp.slice_solve(wts, kk)
        fc, _ = cp.f_on_rays(Xs)
        ok = np.all(np.isfinite(fc)) and fc.min() > 0.001
        dX = np.max(np.abs(Xs - cp.X_bg))
        print('k=%+.4f amp=%.3f sig=%.2f -> %s fmin=%.4g max|dX|=%.3g' % (kk, amp, sig, 'OK ' if ok else 'BLOW', fc.min() if np.all(np.isfinite(fc)) else float('nan'), dX), flush=True)
