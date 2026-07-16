"""JSON/log consistency checker (Charles dispatch 2026-07-14, item 6).

Verifies every number copied into noNull_hess_h2fit_log.txt against the saved refine npz products
(and, where present, noNull_stability_evidence.json). Pure CPU; no GPU. Emits
noNull_evidence_checker_output.txt with per-item PASS/FAIL and an overall verdict.

Checks:
  A. The 3-grid table (doublet lam, isolated lam, eta_c, r_j per grid) vs npz contents.
  B. Pairwise h^2 slopes and both extrapolants (Richardson fine-pair; exact h^2+h^4 3-point)
     recomputed from npz and compared to the log's quoted values.
  C. Cross-seed consistency of the npz files themselves (doublet/isolated per grid).
  D. If noNull_stability_evidence.json exists: file-vs-recomputed eigenvalue agreement and the
     gate-language flags (doublet raw gate NOT met; deflated eta_c and isolated raw r_j gates met).
"""
import os, re, json, numpy as np

TOL_LAM = 5e-8      # table lam quoted to 8 dp
TOL_EXP = 0.05      # residuals quoted to ~2 sig figs (relative)
TOL_EXTRAP = 2e-4   # extrapolants quoted to 5 dp

results = []
def check(name, ok, detail):
    results.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

FILES = {128: ('noNull_hess_refine_s128_0.npz', 'noNull_hess_refine_s128_1.npz'),
         192: ('noNull_hess_refine_s192_0.npz', 'noNull_hess_refine_s192_1.npz'),
         256: ('noNull_hess_refine_s0.npz', 'noNull_hess_refine_s1.npz')}
H = {128: 0.09448819, 192: 0.06282723, 256: 0.04705882}

npz = {}
for N, (f0, f1) in FILES.items():
    d0, d1 = np.load(f0), np.load(f1)
    npz[N] = dict(
        dbl0=np.array(d0['lam_doublet']), dbl1=np.array(d1['lam_doublet']),
        iso0=float(d0['lam_isolated']), iso1=float(d1['lam_isolated']),
        eta0=float(d0['eta_c_doublet']), eta1=float(d1['eta_c_doublet']),
        rj0=float(d0['r_j_isolated']), rj1=float(d1['r_j_isolated']))

# C. cross-seed npz consistency
for N in FILES:
    z = npz[N]
    check(f'C: cross-seed doublet N={N}', abs(z['dbl0'] - z['dbl1']).max() < 1e-6,
          f"max diff {abs(z['dbl0']-z['dbl1']).max():.2e}")
    check(f'C: cross-seed isolated N={N}', abs(z['iso0'] - z['iso1']) < 1e-6,
          f"diff {abs(z['iso0']-z['iso1']):.2e}")

# A. table in the log
log = open('noNull_hess_h2fit_log.txt').read()
rows = re.findall(r'^#\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.e-]+)\s+([\d.e-]+)', log, re.M)
check('A: table rows found', len(rows) == 3, f'{len(rows)} rows')
for (Ns, dq, iq, eq, rq) in rows:
    N = int(Ns); z = npz[N]
    dbl_mean = float(np.mean(np.concatenate([z['dbl0'], z['dbl1']])))
    iso_mean = 0.5 * (z['iso0'] + z['iso1'])
    check(f'A: doublet lam N={N}', abs(float(dq) - dbl_mean) < TOL_LAM, f'log {dq} vs npz {dbl_mean:.8f}')
    check(f'A: isolated lam N={N}', abs(float(iq) - iso_mean) < TOL_LAM, f'log {iq} vs npz {iso_mean:.8f}')
    eta_max = max(z['eta0'], z['eta1']); rj_max = max(z['rj0'], z['rj1'])
    check(f'A: eta_c N={N}', abs(float(eq) - eta_max) / eta_max < TOL_EXP, f'log {eq} vs npz max {eta_max:.2e}')
    check(f'A: r_j N={N}', abs(float(rq) - rj_max) / rj_max < TOL_EXP, f'log {rq} vs npz max {rj_max:.2e}')
    check(f'A: gates N={N}', eta_max < 1e-3 and rj_max < 1e-3,
          f'eta_c(defl)={eta_max:.2e} r_j(iso,raw)={rj_max:.2e} (doublet RAW residual ~3.4e-2 is NOT this gate)')

# B. slopes + extrapolants
lam = {N: (float(np.mean(np.concatenate([npz[N]['dbl0'], npz[N]['dbl1']]))),
           0.5 * (npz[N]['iso0'] + npz[N]['iso1'])) for N in FILES}
h2 = {N: H[N]**2 for N in FILES}
quoted = dict(dbl_slope_coarse=+0.236, dbl_slope_fine=+0.501, iso_slope_coarse=-0.336, iso_slope_fine=-0.042,
              dbl_rich=0.24977, dbl_3pt=0.24943, iso_rich=0.32270, iso_3pt=0.32232)
for idx, name in ((0, 'dbl'), (1, 'iso')):
    l128, l192, l256 = lam[128][idx], lam[192][idx], lam[256][idx]
    cc = (l128 - l192) / (h2[128] - h2[192]); cf = (l192 - l256) / (h2[192] - h2[256])
    rich = l256 - cf * h2[256]
    A = np.array([[1, h2[N], h2[N]**2] for N in (128, 192, 256)])
    b = np.array([l128, l192, l256]); lam0q, _, _ = np.linalg.solve(A, b)
    check(f'B: {name} coarse slope', abs(cc - quoted[f'{name}_slope_coarse']) < 0.01, f'{cc:+.4f} vs quoted {quoted[f"{name}_slope_coarse"]:+.3f}')
    check(f'B: {name} fine slope', abs(cf - quoted[f'{name}_slope_fine']) < 0.01, f'{cf:+.4f} vs quoted {quoted[f"{name}_slope_fine"]:+.3f}')
    check(f'B: {name} Richardson', abs(rich - quoted[f'{name}_rich']) < TOL_EXTRAP, f'{rich:.5f} vs quoted {quoted[f"{name}_rich"]}')
    check(f'B: {name} 3-point', abs(lam0q - quoted[f'{name}_3pt']) < TOL_EXTRAP, f'{lam0q:.5f} vs quoted {quoted[f"{name}_3pt"]}')
    check(f'B: {name} extrapolants POSITIVE', rich > 0 and lam0q > 0, f'{rich:.5f}, {lam0q:.5f}')

# D. evidence JSON (if present)
if os.path.exists('noNull_stability_evidence.json'):
    ev = json.load(open('noNull_stability_evidence.json'))
    for Ns, g in ev['grids'].items():
        for sd, s in g['seeds'].items():
            lf = np.array(s['eigenvalues_file']); lr = np.array(s['eigenvalues_recomputed'])
            check(f'D: N={Ns} s{sd} file-vs-recomputed lam', abs(lf - lr).max() < 1e-6, f'max diff {abs(lf-lr).max():.2e}')
            fr = s['fullH_residuals']
            check(f'D: N={Ns} s{sd} doublet raw gate correctly NOT claimed',
                  (not fr['doublet0']['raw_gate_1e3_met']) and (not fr['doublet1']['raw_gate_1e3_met']),
                  f"raw rel residuals {fr['doublet0']['raw_rel_residual']:.2e}/{fr['doublet1']['raw_rel_residual']:.2e}")
            check(f'D: N={Ns} s{sd} isolated raw gate met', fr['isolated']['raw_gate_1e3_met'],
                  f"raw {fr['isolated']['raw_rel_residual']:.2e}")
            check(f'D: N={Ns} s{sd} doublet residual is T/R-dominated',
                  fr['doublet0']['frac_in_span_QTR'] > 0.9, f"frac {fr['doublet0']['frac_in_span_QTR']:.3f}")
            pb = s['perturbation_bound']
            spec = s['enlargedRR_spectrum_V_QTR_u1']
            # positivity margin is what the data supports (see perturbation_bound_algebra_note.md:
            # the verifier's +/-1.2e-3 is RETRACTED; within-span raw doublet = deflated +/- ~2e-2, all positive)
            check(f'D: N={Ns} s{sd} enlarged-RR spectrum all POSITIVE', min(spec) > 0,
                  f"min={min(spec):+.2e}; doublet neighbors {['%.4f'%x for x in pb['enlargedRR_doublet_neighbors']]}; "
                  f"||C||={pb['offdiag_coupling_norm_2']:.2e} gap={pb['spectral_gap']:.4f} bound={pb['second_order_bound']:.2e} "
                  f"obs_shift={pb['observed_shift_vs_deflated'][0]:+.1e}")
else:
    check('D: evidence JSON present', False, 'noNull_stability_evidence.json missing — run noNull_evidence_seal.py first')

npass = sum(1 for _, ok, _ in results if ok); nfail = len(results) - npass
verdict = 'ALL CONSISTENT' if nfail == 0 else f'{nfail} INCONSISTENCIES'
print(f'\n== CHECKER VERDICT: {verdict} ({npass}/{len(results)} checks pass) ==')
with open('noNull_evidence_checker_output.txt', 'w') as f:
    for name, ok, detail in results: f.write(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}\n")
    f.write(f'\n== CHECKER VERDICT: {verdict} ({npass}/{len(results)} checks pass) ==\n')
