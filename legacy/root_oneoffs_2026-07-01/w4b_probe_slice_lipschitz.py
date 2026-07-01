import sys; sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import numpy as np
src = open('/home/udt-admin/udt_mass_codex/w4b_coupled.py').read()
head = src.split('# ====')[0]
exec(compile(head, 'h', 'exec'))
import w4b_evolib as ev
cp = Coupled('M1'); g = cp.geo
KAP, AMP = -1.0, 0.01
v0 = ev.bump_profile(g, AMP, 'g1', sig_frac=0.25)
vt0 = np.zeros_like(v0)
# slice response at T=0
wts0 = cp.w_on_ts(v0, vt0)
Xs0 = cp.slice_solve(wts0, KAP)
# evolve w for 64 steps on FROZEN background f (small change in w)
r = ev.evolve_np(g, v0, vt0, KAP, True, 64*0.5*float(np.min(g.dx))/1.6, cfl=0.5/1.6)
v1, vt1 = r['v'], r['vt']
print('w change over 64 steps: max|dv| =', np.max(np.abs(v1-v0)), 'max|vt1| =', np.max(np.abs(vt1)))
wts1 = cp.w_on_ts(v1, vt1)
Xs1 = cp.slice_solve(wts1, KAP)
ok0 = np.isfinite(Xs0).all(); ok1 = np.isfinite(Xs1).all()
print('resp0 finite', ok0, 'resp1 finite', ok1)
if ok0 and ok1:
    d01 = np.max(np.abs(Xs1-Xs0)); db = np.max(np.abs(Xs0-cp.X_bg))
    print('||f-resp change|| =', d01, ' vs ||resp0 - bg|| =', db, ' amplification =', d01/max(np.max(np.abs(v1-v0)),1e-300))
