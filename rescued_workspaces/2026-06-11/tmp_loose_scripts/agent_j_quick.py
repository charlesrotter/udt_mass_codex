"""Quick targeted run of Agent J's eigenvalue scan with reduced N_GRID + n_scan
to fit within S52-002 wind-down time budget. Uses Agent J's exact functions
imported from cr_S52_002_J_schwarzschild_formT.py — same physics, smaller
discretization. Documents reduction explicitly per CLAUDE.md Rule 2 + Rule 8.
"""
import sys, os, json, time, numpy as np
# Block J's main() from auto-running on import: rename __main__ guard
import runpy
sys.path.insert(0, '/home/udt-admin/UDT/cr_next')
# Direct import — module's __name__ != '__main__' so main() is not called
import cr_S52_002_J_schwarzschild_formT as mod

REGIMES = mod.REGIMES
EPS_INNER = mod.EPS_INNER

# Reduced numerical parameters for time-budget compatibility
N_GRID_QUICK = 4000     # reduced from 20000
N_SCAN_QUICK = 1500     # reduced from 6000

results_quick = {
    'agent': 'J-quick',
    'dispatch': 'S52-002',
    'note': ('Time-budget-compatible reduction: N_GRID=4000 (vs J script 20000), '
             'n_scan=1500 (vs J script 6000). Same RK4 + Neumann residual + brentq '
             'physics. Reduction documented per CLAUDE.md Rule 2.'),
    'regimes': []
}

KAPPA = -1
t0 = time.time()
for reg in REGIMES:
    rS = reg['r_S']; r_star = reg['r_star']
    r_inner = rS * (1.0 + EPS_INNER)
    r_grid = np.linspace(r_inner, r_star, N_GRID_QUICK)
    G0, F0 = 0.0, 1.0
    print(f"START {reg['name']}: rS={rS} r*={r_star} r*/rS={reg['ratio']}",
          flush=True)
    t1 = time.time()
    evals = mod.find_eigenvalues_schwarzschild(
        KAPPA, r_grid, rS, G0, F0,
        E_min=0.05, E_max=5.0, n_scan=N_SCAN_QUICK, n_modes=5
    )
    dt = time.time() - t1
    phi_at = float(mod.phi_sch(r_star, rS))
    e2_at = float(np.exp(2*phi_at))
    redshift = float(1.0 / np.sqrt(1.0 - rS/r_star))
    rec = {
        'regime': reg['name'], 'r_S': rS, 'r_star': r_star, 'r_ratio': reg['ratio'],
        'phi_at_rstar': phi_at, 'e2phi_at_rstar': e2_at,
        'gravitational_redshift_at_rstar': redshift,
        'eigenvalues_kappa_minus_1': evals,
        'wall_time_s': float(dt),
    }
    results_quick['regimes'].append(rec)
    print(f"DONE {reg['name']}: dt={dt:.1f}s evals={evals[:5]}", flush=True)

print(f"TOTAL TIME: {time.time()-t0:.1f}s", flush=True)

with open('/home/udt-admin/UDT/cr_next/outputs/cr_S52_002_J_quick_results.json',
          'w') as f:
    json.dump(results_quick, f, indent=2)
print("WROTE cr_S52_002_J_quick_results.json", flush=True)
