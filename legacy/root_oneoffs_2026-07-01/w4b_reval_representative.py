"""Representative revalidation (W4-B, 2026-06-12): the full reval pass
(all 174 invalid cells at cfl 0.0625) costs ~3 h; this representative
pass re-runs the M1 decision-relevant invalid cells at cfl 0.125
(drift ~256x below the cfl-0.5 core, passes G1) with T_end as core.
PREMISE (recorded): M2/M4 invalid cells are banked-by-analogy only if
every M1 representative keeps its label; otherwise the full pass must
be run. Writes /tmp/w4b_reval.json in the assembler's format."""
import sys, json
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import numpy as np, w4b_evolib as ev
npz = np.load('/tmp/w4b_bg.npz')
cat = json.load(open('/tmp/w4b_p3_catalog.json'))
geo = ev.Geo(npz, 'M1', Nu=24, Nx=1024)
T_end = 12.0 * float(np.max(geo.xmax))
rows = [r for r in cat if r['group'].startswith('core_M1')
        and ((not r['valid']) or r['label'] == 'COLLAPSE+')
        and (abs(r['amp']) == 1e-2 or r['label'] == 'COLLAPSE+')]
rows = [r for r in rows if (not r['label'] == 'COLLAPSE+')
        or (abs(r['kappa']) <= 1 and abs(r['amp']) == 1e-2)]
print('representative cells:', len(rows), flush=True)
VEQ = {}
v0s, refs, kl, dcl, metas = [], [], [], [], []
for r in rows:
    pert = ev.bump_profile(geo, r['amp'], r['profile'])
    base = 0.0; ref = np.zeros_like(pert)
    if r['init'] == 'eq+bump':
        if r['kappa'] not in VEQ:
            VEQ[r['kappa']] = ev.equilibrium_newton(geo, r['kappa'])[0]
        if VEQ[r['kappa']] is None: continue
        base = VEQ[r['kappa']]; ref = base
    v0s.append(base + pert); refs.append(ref)
    kl.append(r['kappa']); dcl.append(r['dcell']); metas.append(r)
OUT = []
for dc in (True, False):
    sel = [i for i in range(len(kl)) if dcl[i] == dc]
    if not sel: continue
    print('batch dcell=%s NB=%d' % (dc, len(sel)), flush=True)
    resb = ev.evolve_torch(geo, np.array([v0s[i] for i in sel]),
                           np.zeros((len(sel), geo.Nu, geo.Nx)),
                           np.array([kl[i] for i in sel]), dc, T_end,
                           cfl=0.125, n_mon=50)
    for j, i in enumerate(sel):
        r = metas[i]
        lab, diag = ev.classify_batch(resb, j, abs(r['amp']))
        OUT.append(dict(member='M1', dcell=dc, kappa=r['kappa'],
                        amp=r['amp'], init=r['init'],
                        core_label=r['label'], reval_label=lab,
                        edrift=float(diag.get('edrift', np.nan)),
                        valid=bool(diag.get('valid', False)),
                        vmin_last=float(resb['vmin_last'][j]),
                        vmax_last=float(resb['vmax_last'][j]),
                        freq=float(diag.get('freq', np.nan)),
                        banked=bool(diag.get('valid', False))))
        print(' k=%+9.3g a=%+6.2g %7s core=%-14s -> %-14s drift=%.1e vlast=(%+.2f,%+.2f)'
              % (r['kappa'], r['amp'], r['init'], r['label'], lab,
                 diag.get('edrift', np.nan), resb['vmin_last'][j],
                 resb['vmax_last'][j]), flush=True)
json.dump(OUT, open('/tmp/w4b_reval.json', 'w'), indent=1)
print('done.', flush=True)
