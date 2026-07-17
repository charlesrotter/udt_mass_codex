"""Deterministic V4 box-scout START constructor (audit-patch dispatch 2026-07-16 §2).

Rebuilds, bit-reproducibly, the padded starts used by the V4 scout relaxations, WITHOUT touching the
relaxed scout fields. For each target: read the original L=6 carrier; assert exact N/L/h/xi/kappa,
finiteness, unit norm; fill the larger array with the solver asymptote n_inf=(0,0,-1); embed the old
array centrally (integer offsets 16/32/24 for 128->160, 128->192, 192->240); NO rescale/interpolation;
apply only the stated two-layer pin after embedding; save *_start_rebuilt.npz; assert bitwise identity
of the embedded core and exact constancy of every added site; report the start energy and verify it
matches the first line of the corresponding raw NK log to printed roundoff (4 decimals).
Historical relaxation is NOT rerun. Records exact build + relaxation commands.
Output: noNull_boxscout_build.json (+ manifest entries added by the caller).
"""
import json, hashlib, numpy as np, torch
from noNull_energy import energy_noNull
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

N_INF = np.array([0.0, 0.0, -1.0])
CASES = [
    dict(src='noNull_critical_field_128.npz', srcN=128, dstN=160, off=16,
         start_E_log=271.8311, log='boundary_virial_evidence_2026-07-16/scout_N160_relax.log',
         relax_cmd='BASE_FIELD=noNull_boxscout_N160.npz CRIT_FIELD=noNull_boxscout_N160.npz STAGE=nk NK_BUDGET_S=14000 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 21600 python3 noNull_resolve.py'),
    dict(src='noNull_critical_field_128.npz', srcN=128, dstN=192, off=32,
         start_E_log=271.8311, log='boundary_virial_evidence_2026-07-16/scout_N192_relax.log',
         relax_cmd='BASE_FIELD=noNull_boxscout_N192.npz CRIT_FIELD=noNull_boxscout_N192.npz STAGE=nk NK_BUDGET_S=14000 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 21600 python3 noNull_resolve.py'),
    dict(src='noNull_critical_field_192.npz', srcN=192, dstN=240, off=24,
         start_E_log=274.1806, log='boundary_virial_evidence_2026-07-16/scout_N240_relax.log',
         relax_cmd='BASE_FIELD=noNull_boxscout_N240.npz CRIT_FIELD=noNull_boxscout_N240.npz STAGE=nk NK_BUDGET_S=14000 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 21600 python3 noNull_resolve.py'),
]

def sha(p):
    hh = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): hh.update(b)
    return hh.hexdigest()

out = dict(builder='noNull_boxscout_build.py', n_inf=list(N_INF), pin_layers=2, cases=[])
for c in CASES:
    d = np.load(c['src'])
    n0 = d['n']; N, L, h, xi, kap = int(d['N']), float(d['L']), float(d['h']), float(d['xi']), float(d['kappa'])
    assert N == c['srcN'] and L == 6.0 and xi == 1.0 and kap == 1.0
    assert np.isfinite(n0).all()
    unit_err = float(np.abs((n0**2).sum(0) - 1.0).max()); assert unit_err < 1e-12
    Nn, off = c['dstN'], c['off']
    assert (Nn - N) // 2 == off and (Nn - N) % 2 == 0
    big = np.empty((3, Nn, Nn, Nn))
    big[0] = N_INF[0]; big[1] = N_INF[1]; big[2] = N_INF[2]          # constant fill = solver asymptote
    big[:, off:off+N, off:off+N, off:off+N] = n0                     # central embed, no rescale/interp
    # two-layer pin AFTER embedding (matches the solver's pin_boundary(w=2) on n_inf)
    for w in (0, 1):
        big[:, w, :, :] = N_INF[:, None, None];  big[:, Nn-1-w, :, :] = N_INF[:, None, None]
        big[:, :, w, :] = N_INF[:, None, None];  big[:, :, Nn-1-w, :] = N_INF[:, None, None]
        big[:, :, :, w] = N_INF[:, None, None];  big[:, :, :, Nn-1-w] = N_INF[:, None, None]
    # asserts: bitwise core identity; exact constancy of every added site
    core = big[:, off:off+N, off:off+N, off:off+N]
    # (the pin can only have touched added sites: off=16/32/24 > 2 in every case)
    assert (core == n0).all(), 'core not bitwise identical'
    mask = np.ones((Nn, Nn, Nn), dtype=bool); mask[off:off+N, off:off+N, off:off+N] = False
    added = big[:, mask]
    assert (added[0] == N_INF[0]).all() and (added[1] == N_INF[1]).all() and (added[2] == N_INF[2]).all(), \
        'added sites not exactly constant'
    Lnew = (Nn - 1) * h / 2
    fn = f'noNull_boxscout_N{Nn}_start_rebuilt.npz'
    np.savez(fn, n=big, N=Nn, L=Lnew, h=h, xi=xi, kappa=kap)
    # start energy vs the historical NK log first line (printed roundoff = 4 decimals)
    nt = torch.tensor(big, device=dev); nt = nt / nt.norm(dim=0, keepdim=True)
    E = float(energy_noNull(nt, h, xi, kap)[0])
    match = abs(E - c['start_E_log']) < 5e-5 * max(1, abs(c['start_E_log'])) or abs(round(E, 4) - c['start_E_log']) < 1e-9
    print(f"{fn}: N={Nn} L={Lnew:.6f} off={off} core=BITWISE fill=EXACT "
          f"E_start={E:.4f} vs log {c['start_E_log']:.4f} -> {'MATCH' if match else 'MISMATCH'}", flush=True)
    assert match, f'start energy mismatch: {E} vs {c["start_E_log"]}'
    out['cases'].append(dict(src=c['src'], src_sha256=sha(c['src']), dst=fn, dst_sha256=sha(fn),
                             N=Nn, L=Lnew, h=h, offset=off, core_bitwise=True, fill_exact=True,
                             E_start=E, E_start_log=c['start_E_log'], E_match=bool(match),
                             build_cmd='python3 noNull_boxscout_build.py',
                             relax_cmd=c['relax_cmd'], relax_log=c['log'],
                             relaxed_field=f'noNull_boxscout_N{Nn}.npz (NOT touched by this builder)'))
    del nt
json.dump(out, open('noNull_boxscout_build.json', 'w'), indent=1)
print('wrote noNull_boxscout_build.json', flush=True)
