"""Build artifact_manifest.json (Charles dispatch 2026-07-14, item 5).

For every critical field, Ritz warm-start file, refined-vector file, and blind-verifier hunt file
used in the H3 stability certification: path, byte size, SHA-256, N/L/h/HBW, dtype, array names +
shapes, originating command (best-effort from run logs / session record), git HEAD, CUDA/PyTorch
versions, and mtime timestamps. NPZ files are gitignored/large — this manifest is their fingerprint.
"""
import os, json, hashlib, subprocess, datetime, numpy as np
import torch

HBW = 2   # free-mask width used throughout the certification

ARTIFACTS = {
    # critical fields
    'noNull_critical_field.npz':      'STAGE=nk … python3 noNull_resolve.py (256^3 NK to ||g_f||_M-1=0.0157; 2026-07-12)',
    'noNull_critical_field_192.npz':  'TARGET_N=192 SRC=noNull_critical_field.npz python3 noNull_downsample.py ; then BASE_FIELD=CRIT_FIELD=noNull_critical_field_192.npz STAGE=nk NK_BUDGET_S=6000 timeout 7200 python3 noNull_resolve.py (converged 0.0173; 2026-07-13)',
    'noNull_critical_field_128.npz':  'TARGET_N=128 SRC=noNull_critical_field.npz python3 noNull_downsample.py ; then BASE_FIELD=CRIT_FIELD=noNull_critical_field_128.npz STAGE=nk NK_BUDGET_S=6000 timeout 7200 python3 noNull_resolve.py (converged 0.0411; 2026-07-12)',
    # Ritz warm-start files that still exist (NOTE: the 256^3 raw ritz files noNull_hess_ritz_bw2_s{0,1}.npz
    # were OVERWRITTEN by the 192^3 run before N-tagging was added — recorded here as the 192^3 data they now hold)
    'noNull_hess_ritz_bw2_s0.npz':      'BASE_FIELD=CRIT_FIELD=noNull_critical_field_192.npz STAGE=hess HESS_BW=2 HESS_BS=12 HESS_SEEDS=0,1 timeout 86400 python3 noNull_resolve.py — seed 0 (192^3; filename pre-dates N-tagging; 2026-07-13)',
    'noNull_hess_ritz_bw2_s1.npz':      'same command — seed 1 (192^3; 2026-07-13)',
    'noNull_hess_ritz_bw2_N128_s0.npz': 'BASE_FIELD=CRIT_FIELD=noNull_critical_field_128.npz STAGE=hess HESS_BW=2 HESS_BS=12 HESS_SEEDS=0,1 timeout 21600 python3 noNull_resolve.py — seed 0 (2026-07-14, post-N-tagging)',
    'noNull_hess_ritz_bw2_N128_s1.npz': 'same command — seed 1 (2026-07-14)',
    # refined (converged) vectors — the certification products
    'noNull_hess_refine_s0.npz':     'SEED_RITZ=noNull_hess_ritz_bw2_s0.npz(256^3 data at the time) TAG=0 timeout 14400 python3 noNull_hess_refine.py (GATE PASS it=38; 2026-07-13)',
    'noNull_hess_refine_s1.npz':     'SEED_RITZ=noNull_hess_ritz_bw2_s1.npz(256^3 data at the time) TAG=1 timeout 21600 python3 noNull_hess_refine.py (GATE PASS it=47; 2026-07-13)',
    'noNull_hess_refine_s192_0.npz': 'CRIT=noNull_critical_field_192.npz SEED_RITZ=noNull_hess_ritz_bw2_s0.npz TAG=192_0 timeout 21600 python3 noNull_hess_refine.py (GATE PASS it=23; 2026-07-14)',
    'noNull_hess_refine_s192_1.npz': 'CRIT=noNull_critical_field_192.npz SEED_RITZ=noNull_hess_ritz_bw2_s1.npz TAG=192_1 timeout 21600 python3 noNull_hess_refine.py (GATE PASS it=24; 2026-07-14)',
    'noNull_hess_refine_s128_0.npz': 'CRIT=noNull_critical_field_128.npz SEED_RITZ=noNull_hess_ritz_bw2_N128_s0.npz TAG=128_0 timeout 14400 python3 noNull_hess_refine.py (GATE PASS it=19; 2026-07-14)',
    'noNull_hess_refine_s128_1.npz': 'CRIT=noNull_critical_field_128.npz SEED_RITZ=noNull_hess_ritz_bw2_N128_s1.npz TAG=128_1 timeout 14400 python3 noNull_hess_refine.py (GATE PASS it=19; 2026-07-14)',
    # blind-verifier hunt blocks (its own LOBPCG final vectors, N=128; copied from session scratchpad)
    'hunt_u1_s0.npz':    'blind verifier verify_hunt.py — full-space hunt (u1-only deflation), own LOBPCG, random seed variant s0 (2026-07-14)',
    'hunt_u1tr_s1.npz':  'blind verifier verify_hunt.py — genuine-subspace hunt (u1+6 T/R deflation), own LOBPCG, random seed variant s1 (2026-07-14)',
    # Schur-complement inertia seal solution blocks (Charles dispatch 2026-07-14; certified 07-14..16)
    'noNull_schur_Z_N128.npz': 'SCHUR_GRIDS=128 CG_TOL_REL=1e-6->refineX python3 noNull_schur_inertia.py (PASS, margin +2.00e-6; 2026-07-14)',
    'noNull_schur_Z_N192.npz': 'SCHUR_GRIDS=192 CG_TOL_REL=1e-4 python3 noNull_schur_inertia.py (PASS, margin +3.31e-7; 2026-07-15)',
    'noNull_schur_Z_N256.npz': 'SCHUR_GRIDS=256 CG_TOL_REL=1e-4 python3 noNull_schur_inertia.py (PASS, margin +4.14e-9 exact-op; 2026-07-16)',
}

def sha256(path, bufsize=1 << 22):
    hh = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(bufsize)
            if not b: break
            hh.update(b)
    return hh.hexdigest()

git_head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
man = dict(
    purpose='H3 stability certification artifact fingerprints (NPZ gitignored/large; this manifest is the auditable record)',
    generated=datetime.datetime.now().isoformat(timespec='seconds'),
    git_HEAD=git_head,
    torch_version=torch.__version__, cuda_version=torch.version.cuda,
    device=torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu',
    HBW_free_mask_width=HBW,
    artifacts={})

for path, cmd in ARTIFACTS.items():
    if not os.path.exists(path):
        man['artifacts'][path] = dict(status='MISSING', originating_command=cmd); continue
    st = os.stat(path)
    d = np.load(path)
    arrays = {k: dict(shape=list(d[k].shape), dtype=str(d[k].dtype)) for k in d.files}
    meta = {}
    for k in ('N', 'L', 'h', 'xi', 'kappa'):
        if k in d.files and d[k].ndim == 0: meta[k] = float(d[k])
    man['artifacts'][path] = dict(
        status='present', bytes=st.st_size, sha256=sha256(path),
        mtime=datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),
        params=meta, arrays=arrays, originating_command=cmd)
    print(f"hashed {path} ({st.st_size/1e6:.0f} MB)", flush=True)

json.dump(man, open('artifact_manifest.json', 'w'), indent=1)
print('wrote artifact_manifest.json', flush=True)
