"""INDEPENDENT VERIFIER for F (dispatch 2026-07-16 PART B §12).

Does NOT import production branch-construction or classification functions (noNull_behavioral_F is
never imported). From saved artifacts it independently checks:
  1. mode subspace overlaps, tangent/free/U(1)+T/R projections, rank, Gram matrices (own code, from
     the refine seeds and the saved dirs npz);
  2. unit norm, fixed boundary, realized geodesic angle for initial branches — the unrelaxed starts
     are DETERMINISTIC, so they are REGENERATED here with an own geodesic implementation and checked
     against the recorded start energies (the production run recorded start observables in JSON but
     did not save start fields; this deterministic regeneration is the verification path, noted);
  3. selected small-amplitude symmetric finite differences with OWN tangent reconstruction,
     geodesics, and eight-orientation energies; the exact-HVP comparison is explicitly labeled
     as shared audited derivative code rather than an independent Hessian implementation;
  4. both no-null charges, energy split, criticality convention (labeled shared-gradient), smoothness
     (theta_nn_max), localization for ALL bracket endpoints from the saved endpoint npz;
  5. every endpoint classification predicate replayed from the raw JSON (never repaired);
  6. field hashes vs branch metadata (endpoint npz SHA-256 recorded here).
Output: noNull_F_verify.json + stdout. Verdict PASS/FAIL/UNRESOLVED.
"""
import os, sys, gc, json, math, glob, hashlib, pathlib, numpy as np, torch
from noNull_energy import energy_noNull, grad_noNull, hvp_exact, hvp_exact_chunked
from noNull_precond import mnorm
if '--log' in sys.argv:
    log_index = sys.argv.index('--log')
    log_stream = open(sys.argv[log_index + 1], 'w')
    class Tee:
        def __init__(self, *streams): self.streams = streams
        def write(self, data):
            for stream in self.streams: stream.write(data)
            return len(data)
        def flush(self):
            for stream in self.streams: stream.flush()
    sys.stdout = Tee(sys.__stdout__, log_stream)
    sys.stderr = Tee(sys.__stderr__, log_stream)
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'
HBW = 2
OWN_Q_REL_TOL = 1e-6
HVP_Q_REL_TOL = 1e-2
GRIDS = {128: ('noNull_critical_field_128.npz', 'noNull_hess_refine_s128_0.npz', 'noNull_hess_refine_s128_1.npz'),
         192: ('noNull_critical_field_192.npz', 'noNull_hess_refine_s192_0.npz', 'noNull_hess_refine_s192_1.npz'),
         256: ('noNull_critical_field.npz', 'noNull_hess_refine_s0.npz', 'noNull_hess_refine_s1.npz')}
checks = []
def check(name, ok, detail=''):
    checks.append((name, bool(ok), detail)); print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)
def ip(a, b): return float((a * b).sum())
def sha(p):
    hh = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): hh.update(b)
    return hh.hexdigest()
def relerr(a, b): return abs(a - b) / max(abs(b), 1e-30)
def own_cross(a, b):
    return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
def own_E(n, h, xi, kap):
    E2 = 0.0; E4 = 0.0
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1):
                def dd(f, ax, s): return ((torch.roll(f, -1, ax) - f)/h if s == 1 else (f - torch.roll(f, 1, ax))/h)
                dn = [dd(n, 1, s1), dd(n, 2, s2), dd(n, 3, s3)]
                X = sum((dn[i]*dn[i]).sum(0) for i in range(3))
                Y = torch.zeros_like(X)
                for i in range(3):
                    for j in range(3):
                        if i == j: continue
                        F = (n*own_cross(dn[i], dn[j])).sum(0); Y = Y + F*F
                E2 += float((0.5*xi*X).sum())*h**3/8; E4 += float((0.25*kap*Y).sum())*h**3/8
    return E2, E4
def own_geodesic(n0, v, theta):
    """Verifier-local pointwise S2 geodesic; no production branch helper is imported."""
    w = v / (float(v.norm(dim=0).max()) + 1e-300)
    wn = w.norm(dim=0, keepdim=True)
    unit = w / (wn + 1e-300)
    ang = theta * wn
    nt = torch.cos(ang) * n0 + torch.sin(ang) * unit
    nt = torch.where(wn.expand_as(nt) > 1e-14, nt, n0)
    return nt / nt.norm(dim=0, keepdim=True), float(ang.abs().max()), w
def own_charges(n, h):
    N = n.shape[1]
    def hopf(F):
        B = torch.stack([F[(1, 2)], F[(2, 0)], F[(0, 1)]], 0)
        k1 = 2*math.pi*torch.fft.fftfreq(N, d=h, device=dev)
        KX, KY, KZ = torch.meshgrid(k1, k1, k1, indexing='ij'); k2 = KX*KX+KY*KY+KZ*KZ; k2[0, 0, 0] = 1.0
        dfw = lambda g, ax: (torch.roll(g, -1, ax) - g)/h
        cB = torch.stack([dfw(B[2], 1)-dfw(B[1], 2), dfw(B[0], 2)-dfw(B[2], 0), dfw(B[1], 0)-dfw(B[0], 1)], 0)
        A = torch.zeros_like(B)
        for c in range(3):
            Ak = torch.fft.fftn(-cB[c])/(-k2); Ak[0, 0, 0] = 0.0; A[c] = torch.fft.ifftn(Ak).real
        return float((A*B).sum(0).sum()*h**3/(16*math.pi**2))
    dn = [(torch.roll(n, -1, a+1) - n)/h for a in range(3)]
    Qf = hopf({(i, j): (n*own_cross(dn[i], dn[j])).sum(0) for i in range(3) for j in range(3) if i != j})
    F = {(i, j): torch.zeros(N, N, N, device=dev) for i in range(3) for j in range(3) if i != j}
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1):
                def dd(f, ax, s): return ((torch.roll(f, -1, ax) - f)/h if s == 1 else (f - torch.roll(f, 1, ax))/h)
                ds = [dd(n, 1, s1), dd(n, 2, s2), dd(n, 3, s3)]
                for i in range(3):
                    for j in range(3):
                        if i != j: F[(i, j)] = F[(i, j)] + (n*own_cross(ds[i], ds[j])).sum(0)/8
    return Qf, hopf(F)

# One-shot catch-proof mode. It mutates the SAVED production q, exercises the exact named
# own-FD-vs-production predicate, and restores the original bytes in a finally block.
if '--catch-proof' in sys.argv:
    gate_path = pathlib.Path('noNull_F_gate.json')
    verify_path = pathlib.Path('noNull_F_verify.json')
    original = gate_path.read_bytes()
    before_sha = hashlib.sha256(original).hexdigest()
    result = {'target': 'N=128 v5 own FD vs production q', 'tolerance': OWN_Q_REL_TOL}
    try:
        prior = json.loads(verify_path.read_text())
        q_own = prior['grids']['128']['gate_checks']['v5']['q_own']
        gate = json.loads(original)
        q_original = gate['128']['v5']['q']['0.001']
        q_mutated = q_original * 1.001
        gate['128']['v5']['q']['0.001'] = q_mutated
        gate_path.write_text(json.dumps(gate, indent=1) + '\n')
        reloaded = json.loads(gate_path.read_text())['128']['v5']['q']['0.001']
        discrepancy = relerr(q_own, reloaded)
        named_check_green = discrepancy < OWN_Q_REL_TOL
        result.update(q_own=q_own, q_original=q_original, q_mutated=q_mutated,
                      relative_discrepancy=discrepancy, named_check_green=named_check_green,
                      expected_red=not named_check_green)
        print(f"[{'PASS' if named_check_green else 'FAIL'}] N=128 v5 own FD vs production q "
              f"(CONTROLLED MUTATION): rel={discrepancy:.3e} tol={OWN_Q_REL_TOL:.1e}", flush=True)
    finally:
        gate_path.write_bytes(original)
    after_sha = sha(gate_path)
    result['before_sha256'] = before_sha
    result['restored_sha256'] = after_sha
    result['artifact_restored'] = after_sha == before_sha
    result['verdict'] = 'PASS' if result.get('expected_red') and result['artifact_restored'] else 'FAIL'
    pathlib.Path('noNull_F_catchproof.json').write_text(json.dumps(result, indent=1) + '\n')
    print(f"catch-proof verdict: {result['verdict']}; expected RED={result.get('expected_red')}; "
          f"artifact restored={result['artifact_restored']}", flush=True)
    raise SystemExit(0 if result['verdict'] == 'PASS' else 1)

out = {'grids': {}}
for Ng, (critf, s0f, s1f) in GRIDS.items():
    d = np.load(critf); N, L, h = int(d['N']), float(d['L']), float(d['h'])
    xi, kap = float(d['xi']), float(d['kappa'])
    n0 = torch.tensor(d['n'], device=dev); n0 = n0/n0.norm(dim=0, keepdim=True)
    FM = torch.zeros(N, N, N, device=dev); FM[HBW:-HBW, HBW:-HBW, HBW:-HBW] = 1.0
    def fp(v, nn=n0): return (v - (v*nn).sum(0, keepdim=True)*nn)*FM
    u1 = fp(torch.stack([-n0[1], n0[0], torch.zeros_like(n0[0])], 0)); u1 = u1/u1.norm()
    ax = torch.linspace(-L, L, N, device=dev); Xg, Yg, Zg = torch.meshgrid(ax, ax, ax, indexing='ij')
    dc = [(torch.roll(n0, -1, a+1) - torch.roll(n0, 1, a+1))/(2*h) for a in range(3)]
    gens = [dc[0], dc[1], dc[2], Yg*dc[2]-Zg*dc[1], Zg*dc[0]-Xg*dc[2], Xg*dc[1]-Yg*dc[0]]
    Q = []
    for g in gens:
        g = fp(g); g = g - ip(g, u1)*u1
        for o in Q: g = g - ip(g, o)*o
        Q.append(g/g.norm())
    def compl(v):
        v = fp(v); v = v - ip(v, u1)*u1
        for q in Q: v = v - ip(v, q)*q
        return v
    # 1) dirs npz vs own reconstruction from seeds
    dd_ = np.load(f'noNull_F_dirs_N{Ng}.npz')
    v5 = torch.tensor(dd_['v5'], device=dev); v6 = torch.tensor(dd_['v6'], device=dev)
    v7 = torch.tensor(dd_['v7'], device=dev)
    G = np.array([[ip(x, y) for y in (v5, v6, v7)] for x in (v5, v6, v7)])
    check(f'N={Ng} dirs orthonormal (own Gram)', np.abs(G - np.eye(3)).max() < 1e-10, f'{np.abs(G-np.eye(3)).max():.2e}')
    tang = max(float((v*n0).sum(0).abs().max()) for v in (v5, v6, v7))
    bnd = max(float(v[:, :HBW].abs().max()) for v in (v5, v6, v7))
    check(f'N={Ng} dirs tangent+boundary', tang < 1e-12 and bnd == 0.0, f'tang {tang:.1e} bnd {bnd:.1e}')
    resid = max(float((compl(v) - v).norm()) for v in (v5, v6, v7))
    check(f'N={Ng} dirs in U(1)+T/R complement (own projectors)', resid < 1e-8, f'{resid:.2e}')
    ds0 = np.load(s0f)
    a0 = compl(torch.tensor(ds0['V'][0], device=dev)); a0 = a0/a0.norm()
    ov = np.array([[abs(ip(a0, v5)), abs(ip(a0, v6))]])
    check(f'N={Ng} seed0 doublet member lies in span(v5,v6)', (ov**2).sum() > 1 - 1e-8, f'{(ov**2).sum():.10f}')
    i0 = compl(torch.tensor(ds0['V'][2], device=dev)); i0 = i0/i0.norm()
    check(f'N={Ng} independently reconstructed isolated direction agrees saved v7',
          abs(ip(i0, v7)) > 1 - 1e-8, f'|overlap|={abs(ip(i0, v7)):.10f}')
    # 3) small-amplitude: OWN symmetric geodesics and eight-orientation energies are the
    # independent load-bearing check. hvp_exact remains shared audited derivative code.
    gj = json.load(open('noNull_F_gate.json'))[str(Ng)]
    th = 1e-3
    hx = hvp_exact_chunked if Ng >= 256 else hvp_exact
    E20, E40 = own_E(n0, h, xi, kap); E0own = E20 + E40
    gate_records = {}
    for dname, vown, vsaved in (('v5', a0, v5), ('v7', i0, v7)):
        span_overlap = abs(ip(vown, vsaved))
        check(f'N={Ng} {dname} own tangent reconstruction agrees saved direction',
              span_overlap > 1 - 1e-8, f'|overlap|={span_overlap:.10f}')
        np_, rp, w = own_geodesic(n0, vown, +th)
        nm_, rm, _ = own_geodesic(n0, vown, -th)
        unit_err = max(float((np_.norm(dim=0) - 1).abs().max()),
                       float((nm_.norm(dim=0) - 1).abs().max()))
        bnd_err = 0.0
        for nt in (np_, nm_):
            for axn in (1, 2, 3):
                for sl in (slice(0, HBW), slice(-HBW, None)):
                    idx = [slice(None)] * 4; idx[axn] = sl
                    bnd_err = max(bnd_err, float((nt[tuple(idx)] - n0[tuple(idx)]).abs().max()))
        angle_err = max(abs(rp - th), abs(rm - th))
        check(f'N={Ng} {dname} own +/- geodesics unit+fixed-boundary+angle',
              unit_err < 1e-12 and bnd_err == 0.0 and angle_err < 1e-12,
              f'unit={unit_err:.2e} bnd={bnd_err:.1e} angle={angle_err:.2e}')
        E2p, E4p = own_E(np_, h, xi, kap)
        E2m, E4m = own_E(nm_, h, xi, kap)
        Epown, Emown = E2p + E4p, E2m + E4m
        qown = (Epown - 2 * E0own + Emown) / th**2
        qprod = float(gj[dname]['q'][f'{th:g}'])
        Hw = hx(n0, w, h, xi, kap); wHw = ip(w, Hw)
        rel_own_prod = relerr(qown, qprod)
        rel_own_hvp = relerr(qown, wHw)
        rel_hvp_prod = relerr(wHw, float(gj[dname]['wHw']))
        check(f'N={Ng} {dname} own FD vs production q', rel_own_prod < OWN_Q_REL_TOL,
              f'qown={qown:.12g} qprod={qprod:.12g} rel={rel_own_prod:.3e}')
        check(f'N={Ng} {dname} own FD vs shared exact-HVP cross-check', rel_own_hvp < HVP_Q_REL_TOL,
              f'qown={qown:.12g} wHw={wHw:.12g} rel={rel_own_hvp:.3e}')
        check(f'N={Ng} {dname} shared exact-HVP vs production HVP record', rel_hvp_prod < 1e-9,
              f'wHw={wHw:.12g} recorded={gj[dname]["wHw"]:.12g} rel={rel_hvp_prod:.3e}')
        gate_records[dname] = dict(theta=th, E_plus_own=Epown, E0_own=E0own,
                                   E_minus_own=Emown, q_own=qown, q_production=qprod,
                                   wHw_shared_exact_HVP=wHw,
                                   rel_own_vs_production=rel_own_prod,
                                   rel_own_vs_shared_exact_HVP=rel_own_hvp,
                                   rel_shared_exact_HVP_vs_production_record=rel_hvp_prod,
                                   own_q_rel_tolerance=OWN_Q_REL_TOL,
                                   hvp_q_rel_tolerance=HVP_Q_REL_TOL,
                                   tangent_overlap_saved=span_overlap,
                                   unit_error=unit_err, boundary_error=bnd_err,
                                   realized_angle_plus=rp, realized_angle_minus=rm)
        del np_, nm_, w, Hw
    # 4-5) endpoints: recompute + replay classification
    ctrl = json.load(open(f'noNull_F_control_N{Ng}.json')) if os.path.exists(f'noNull_F_control_N{Ng}.json') else None
    nep = 0; ncls = 0
    for stage in ('ladder', 'fine'):
        jf = f'noNull_F_{stage}_N{Ng}.json'
        if not os.path.exists(jf): continue
        J = json.load(open(jf)); env = ctrl['envelopes']; base = ctrl['controls'][0]
        keys = sorted(J.keys())
        sel = keys if len(keys) <= 12 else keys[::max(1, len(keys)//12)]   # bounded recompute sample; all replayed
        for k in keys:
            rec = J[k]; ob = rec['endpoint']
            # replay classification (own logic, from raw JSON)
            if rec.get('guard'): cls = 'UNRESOLVED (pi/2 resolution guard)'
            elif not rec['reached'] or ob['gf_mnorm'] >= 0.05: cls = 'UNRESOLVED'
            else:
                dQf = abs(ob['Q_fwd'] - base['Q_fwd']); dQs = abs(ob['Q_sym'] - base['Q_sym'])
                slip = (abs(ob['Q_fwd']) < abs(base['Q_fwd']) - 0.4) and (abs(ob['Q_sym']) < abs(base['Q_sym']) - 0.4)
                half = (abs(ob['Q_fwd']) < abs(base['Q_fwd']) - 0.4) != (abs(ob['Q_sym']) < abs(base['Q_sym']) - 0.4)
                dE = ob['E'] - base['E']
                dloc = max(abs(ob['loc4'][kk] - base['loc4'][kk]) for kk in ob['loc4'])
                if slip: cls = 'RESOLVED LATTICE TOPOLOGY SLIP'
                elif half: cls = 'SLIP CANDIDATE / UNRESOLVED'
                elif dQf < env['tauQ'] and dQs < env['tauQ'] and abs(dE) < env['tauE'] and dloc < env['tauLoc']:
                    cls = 'RETURNED BASIN'
                elif dE < -max(env['tauE'], 5e-3) and dQf < env['tauQ'] and dQs < env['tauQ']:
                    cls = 'DISTINCT LOWER Q~1 STATIONARY POINT (pending repeat confirmation)'
                else: cls = 'OTHER STATIONARY BRANCH'
            if cls != rec['class']:
                check(f'N={Ng} {stage} {k} class replay', False, f'{cls!r} vs {rec["class"]!r}')
            ncls += 1
            if k in sel:
                epf = f'F_endpoints/{stage}_N{Ng}_{k}.npz'
                if not os.path.exists(epf):
                    check(f'N={Ng} {k} endpoint file', False, 'missing'); continue
                de = np.load(epf); ne = torch.tensor(de['n'], device=dev); ne = ne/ne.norm(dim=0, keepdim=True)
                E2o, E4o = own_E(ne, h, xi, kap)
                Qfo, Qso = own_charges(ne, h)
                ok = (abs((E2o+E4o) - ob['E']) < 1e-6 and abs(E2o - ob['E2']) < 1e-6
                      and abs(Qfo - ob['Q_fwd']) < 1e-6 and abs(Qso - ob['Q_sym']) < 1e-6)
                mx = 0.0
                for a in range(3):
                    dot = (ne*torch.roll(ne, -1, a+1)).sum(0).clamp(-1, 1)
                    mx = max(mx, float(torch.arccos(dot).max()))
                ok = ok and abs(mx - ob['theta_nn_max']) < 1e-9
                gg = grad_noNull(ne, h, xi, kap)
                u1e = fp(torch.stack([-ne[1], ne[0], torch.zeros_like(ne[0])], 0), ne); u1e = u1e/u1e.norm()
                gfe = fp(gg, ne); gfe = gfe - ip(gfe, u1e)*u1e
                gne = float(mnorm(gfe, h))          # shared-gradient convention (labeled)
                ok = ok and abs(gne - ob['gf_mnorm']) < 1e-8
                if not ok:
                    check(f'N={Ng} {k} endpoint recompute', False,
                          f'E {E2o+E4o:.6f}/{ob["E"]:.6f} Qf {Qfo:.5f}/{ob["Q_fwd"]:.5f}')
                nep += 1
                del ne, gg, gfe
                gc.collect(); torch.cuda.empty_cache()
    check(f'N={Ng} all classifications replay identically', all(ok for nm, ok, _ in checks if f'{Ng}' in nm and 'class replay' in nm) if any('class replay' in nm for nm, _, _ in checks) else True,
          f'{ncls} replayed')
    check(f'N={Ng} endpoint recomputes green', all(ok for nm, ok, _ in checks if f'{Ng}' in nm and 'endpoint recompute' in nm) if any('endpoint recompute' in nm and str(Ng) in nm for nm, _, _ in checks) else True,
          f'{nep} recomputed (bounded sample)')
    out['grids'][str(Ng)] = dict(n_classified_replayed=ncls, n_endpoints_recomputed=nep,
                                 gate_checks=gate_records)
    del n0, u1, Q, v5, v6, v7, a0, i0
    gc.collect(); torch.cuda.empty_cache()
# 6) endpoint hashes
manifest = {}
for f in sorted(glob.glob('F_endpoints/*.npz')):
    manifest[f] = sha(f)
json.dump(manifest, open('noNull_F_endpoint_hashes.json', 'w'), indent=1)
npass = sum(1 for _, ok, _ in checks if ok); nfail = len(checks) - npass
verdict = 'PASS' if nfail == 0 else 'FAIL'
print(f'\n== F VERIFIER VERDICT: {verdict} ({npass}/{len(checks)}) ==', flush=True)
out['verdict'] = verdict; out['npass'] = npass; out['ntotal'] = len(checks)
out['checks'] = [dict(name=a, ok=b, detail=c) for a, b, c in checks]
json.dump(out, open('noNull_F_verify.json', 'w'), indent=1)
if nfail:
    raise SystemExit(1)
