"""F — finite-amplitude BASIN BEHAVIOR of the certified static carrier (dispatch 2026-07-16 PART B).

NOT physical time evolution: trajectories are trust-region minimization paths ("relaxation/basin
behavior", never dynamics). Premises: S2 carrier + L2+L4 = POSIT/CHOSE; 8-orientation discretization
DERIVED numerically; finite-grid positive Hessian at L=6/HBW=2 = OBSERVED/CERTIFIED; F outcomes =
OBSERVED numerical basin behavior per grid/box; EH/G not used; dynamics + infinite volume OPEN.
Operators: energy_noNull / grad_noNull / hvp_exact(_chunked) / the two no-null charges ONLY.

STAGES (env STAGE=):
  dirs    — build+verify perturbation directions per grid (seed agreement, Procrustes, complement
            projection, Grams, cross-grid alignment); saves noNull_F_dirs_N{N}.npz + JSON.
  gate    — small-amplitude symmetric quadratic gate vs EXACT HVP (3 grids, doublet dir + isolated).
  control — 2x identical unperturbed NK controls per grid (variability), U(1)-rotation invariance
            control, T/R geodesic controls (theta=0.10; all six at 128, representatives finer).
  ladder  — adaptive amplitude bracket at 128^3 (8 doublet-plane dirs + both isolated signs;
            theta ladder 0.05..1.20, bisect<=3 on first outcome change). Restart-safe.
  fine    — fine-grid confirmation at 192/256 per section 11.
Primary solve deflates ONLY exact U(1); T/R NOT held. Fixed boundary (2-layer pin). Endpoint classes
per section 10 with preregistered envelopes from measured control variability.
Outputs: noNull_F_{stage}_N{N}*.json + endpoint npz under F_endpoints/ + logs under F_evidence/.
"""
import os, gc, json, math, time, hashlib, numpy as np, torch
from noNull_energy import energy_noNull, grad_noNull, hvp_exact, hvp_exact_chunked
from noNull_precond import make_precond, mnorm
torch.set_default_dtype(torch.float64); dev = 'cuda' if torch.cuda.is_available() else 'cpu'

STAGE = os.environ.get('STAGE', 'dirs')
HBW = 2
GRIDS = {128: ('noNull_critical_field_128.npz', 'noNull_hess_refine_s128_0.npz', 'noNull_hess_refine_s128_1.npz'),
         192: ('noNull_critical_field_192.npz', 'noNull_hess_refine_s192_0.npz', 'noNull_hess_refine_s192_1.npz'),
         256: ('noNull_critical_field.npz', 'noNull_hess_refine_s0.npz', 'noNull_hess_refine_s1.npz')}
ANGLES = [k * math.pi / 4 for k in range(8)]
LADDER = (0.05, 0.10, 0.20, 0.40, 0.80, 1.20)
os.makedirs('F_endpoints', exist_ok=True); os.makedirs('F_evidence', exist_ok=True)

def ip(a, b): return float((a * b).sum())
def sha(p):
    hh = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): hh.update(b)
    return hh.hexdigest()

class Ctx:
    """Per-grid context: carrier + projectors + operators (certification conventions)."""
    def __init__(self, Ng):
        critf, s0f, s1f = GRIDS[Ng]
        d = np.load(critf)
        self.Ng = Ng; self.critf = critf; self.s0f = s0f; self.s1f = s1f
        self.N, self.L, self.h = int(d['N']), float(d['L']), float(d['h'])
        self.xi, self.kap = float(d['xi']), float(d['kappa'])
        n = torch.tensor(d['n'], device=dev); self.n0 = n / n.norm(dim=0, keepdim=True)
        self.precond, _ = make_precond(self.N, self.h, self.xi, dev)
        N = self.N
        self.FM = torch.zeros(N, N, N, device=dev); self.FM[HBW:-HBW, HBW:-HBW, HBW:-HBW] = 1.0
        ax = torch.linspace(-self.L, self.L, N, device=dev)
        self.Xg, self.Yg, self.Zg = torch.meshgrid(ax, ax, ax, indexing='ij')
        self.n_inf = torch.tensor([0., 0., -1.], device=dev).view(3, 1, 1, 1)
        self.hx = hvp_exact_chunked if Ng >= 256 else hvp_exact
    def freeproj(self, v, n): return (v - (v * n).sum(0, keepdim=True) * n) * self.FM
    def pin(self, n):
        w = HBW; ni = self.n_inf
        n = n.clone()
        n[:, :w, :, :] = ni; n[:, -w:, :, :] = ni
        n[:, :, :w, :] = ni; n[:, :, -w:, :] = ni
        n[:, :, :, :w] = ni; n[:, :, :, -w:] = ni
        return n / n.norm(dim=0, keepdim=True)
    def u1_of(self, n):
        u = self.freeproj(torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0), n)
        return u / (u.norm() + 1e-30)
    def tr_gens(self, n):
        dc = [(torch.roll(n, -1, a + 1) - torch.roll(n, 1, a + 1)) / (2 * self.h) for a in range(3)]
        gens = [dc[0], dc[1], dc[2], self.Yg * dc[2] - self.Zg * dc[1],
                self.Zg * dc[0] - self.Xg * dc[2], self.Xg * dc[1] - self.Yg * dc[0]]
        u1 = self.u1_of(n)
        raw = [self.freeproj(g, n) - ip(self.freeproj(g, n), u1) * u1 for g in gens]
        G = np.array([[ip(a, b) for b in raw] for a in raw])
        sv = np.sqrt(np.maximum(np.linalg.eigvalsh(0.5 * (G + G.T)), 0))[::-1]   # rank-revealing singular values
        Q = []
        for c in raw:
            c = c.clone()
            for o in Q: c = c - ip(c, o) * o
            nc = float(c.norm())
            if nc > 1e-10 * float(raw[0].norm() + 1): Q.append(c / nc)
        return Q, sv, u1
    def charges(self, n):
        N, h = self.N, self.h
        def hopf(F):
            B = torch.stack([F[(1, 2)], F[(2, 0)], F[(0, 1)]], 0)
            k1 = 2 * math.pi * torch.fft.fftfreq(N, d=h, device=dev)
            KX, KY, KZ = torch.meshgrid(k1, k1, k1, indexing='ij')
            k2 = KX * KX + KY * KY + KZ * KZ; k2[0, 0, 0] = 1.0
            dfw = lambda g, ax: (torch.roll(g, -1, ax) - g) / h
            cB = torch.stack([dfw(B[2], 1) - dfw(B[1], 2), dfw(B[0], 2) - dfw(B[2], 0), dfw(B[1], 0) - dfw(B[0], 1)], 0)
            A = torch.zeros_like(B)
            for c in range(3):
                Ak = torch.fft.fftn(-cB[c]) / (-k2); Ak[0, 0, 0] = 0.0; A[c] = torch.fft.ifftn(Ak).real
            return float((A * B).sum(0).sum() * h**3 / (16 * math.pi**2))
        def cross(a, b):
            return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
        dn = [(torch.roll(n, -1, a + 1) - n) / h for a in range(3)]
        Qf = hopf({(i, j): (n * cross(dn[i], dn[j])).sum(0) for i in range(3) for j in range(3) if i != j})
        F = {(i, j): torch.zeros(N, N, N, device=dev) for i in range(3) for j in range(3) if i != j}
        for s1 in (1, -1):
            for s2 in (1, -1):
                for s3 in (1, -1):
                    def dd(f, ax, s): return ((torch.roll(f, -1, ax) - f) / h if s == 1 else (f - torch.roll(f, 1, ax)) / h)
                    ds = [dd(n, 1, s1), dd(n, 2, s2), dd(n, 3, s3)]
                    for i in range(3):
                        for j in range(3):
                            if i != j: F[(i, j)] = F[(i, j)] + (n * cross(ds[i], ds[j])).sum(0) / 8
        Qs = hopf(F)
        return Qf, Qs
    def observables(self, n, ref=None):
        E, E2, E4 = [float(x) for x in energy_noNull(n, self.h, self.xi, self.kap)]
        Qf, Qs = self.charges(n)
        g = grad_noNull(n, self.h, self.xi, self.kap)
        u1 = self.u1_of(n)
        gf = self.freeproj(g, n); gf = gf - ip(gf, u1) * u1
        gn = float(mnorm(gf, h=self.h))
        mx = 0.0
        for a in range(3):
            dot = (n * torch.roll(n, -1, a + 1)).sum(0).clamp(-1, 1)
            mx = max(mx, float(torch.arccos(dot).max()))
        # rho4 localization + centroid
        rho4 = torch.zeros(self.N, self.N, self.N, device=dev)
        def dd(f, ax, s): return ((torch.roll(f, -1, ax) - f) / self.h if s == 1 else (f - torch.roll(f, 1, ax)) / self.h)
        def cross(a, b):
            return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
        for s1 in (1, -1):
            for s2 in (1, -1):
                for s3 in (1, -1):
                    ds = [dd(n, 1, s1), dd(n, 2, s2), dd(n, 3, s3)]
                    for i in range(3):
                        for j in range(3):
                            if i != j:
                                Fij = (n * cross(ds[i], ds[j])).sum(0)
                                rho4 = rho4 + 0.25 * self.kap * Fij * Fij / 8
        tot = float(rho4.sum()) + 1e-300
        cen = [float((rho4 * X).sum()) / tot for X in (self.Xg, self.Yg, self.Zg)]
        Am = torch.maximum(torch.maximum(self.Xg.abs(), self.Yg.abs()), self.Zg.abs())
        loc = {f'{a:g}': float(rho4[Am <= a].sum()) / tot for a in (1.0, 1.5, 2.0, 2.5)}
        rec = dict(E=E, E2=E2, E4=E4, Q_fwd=Qf, Q_sym=Qs, gf_mnorm=gn, theta_nn_max=mx,
                   centroid=cen, loc4=loc)
        if ref is not None:
            rec['displacement'] = float((n - ref).norm())
        del rho4, g, gf
        return rec

def geodesic(ctx, v, theta):
    """Pointwise geodesic: w = v / max|v|; n_theta = cos(theta|w|) n0 + sin(theta|w|) w/|w|."""
    wmax = float(v.norm(dim=0).max())
    w = v / (wmax + 1e-300)
    wn = w.norm(dim=0, keepdim=True)
    unit = w / (wn + 1e-300)
    ang = theta * wn
    nt = torch.cos(ang) * ctx.n0 + torch.sin(ang) * unit
    nt = torch.where(wn.expand_as(nt) > 1e-14, nt, ctx.n0)
    nt = nt / nt.norm(dim=0, keepdim=True)
    realized = float(ang.max())
    return nt, realized

def nk_relax(ctx, n, tag, target=0.05, budget=2400, maxstep=200, log=None):
    """Repaired moving-tangent trust-region NK (adapted verbatim from noNull_resolve STAGE=nk),
    U(1)-only deflation, fixed boundary, FULL per-step observables. Returns (n, traj, reached)."""
    h, xi, kap = ctx.h, ctx.xi, ctx.kap
    EPS = 1e-4; Md = h**3
    def gE(nn): return grad_noNull(nn, h, xi, kap)
    def defl(v, nn, u1): v = ctx.freeproj(v, nn); return v - ip(v, u1) * u1
    def hvp(v, nn, u1): v = defl(v, nn, u1); return defl((gE(nn + EPS * v) - gE(nn - EPS * v)) / (2 * EPS), nn, u1)
    def Aop(v, mu, nn, u1): return hvp(v, nn, u1) + mu * Md * defl(v, nn, u1)
    def btau(x, p, rad):
        a_ = ip(p, p); b_ = 2 * ip(x, p); c_ = ip(x, x) - rad * rad
        return (-b_ + max(b_ * b_ - 4 * a_ * c_, 0.0) ** 0.5) / (2 * a_ + 1e-30)
    def steihaug(b, mu, rad, nn, u1, maxit=60, tol=1e-2):
        def pc(v): return defl(ctx.precond(v), nn, u1)
        x = torch.zeros_like(b); r = b.clone(); z = pc(r); p = z.clone(); rz = ip(r, z); b0 = float(r.norm()) + 1e-30
        for j in range(maxit):
            Hp = Aop(p, mu, nn, u1); pHp = ip(p, Hp)
            if pHp <= 1e-30: return x + btau(x, p, rad) * p, 'negcurv', j
            al = rz / pHp; xn = x + al * p
            if float(xn.norm()) >= rad: return x + btau(x, p, rad) * p, 'boundary', j
            x = xn; r = r - al * Hp
            if float(r.norm()) < tol * b0: return x, 'converged', j
            z = pc(r); rz_new = ip(r, z); p = z + (rz_new / rz) * p; rz = rz_new
        return x, 'maxit', maxit
    mu, rad = 1.0, 2.0
    t0 = time.time(); traj = []; nstart = n.clone(); reached = False; guard = False
    for step in range(1, maxstep + 1):
        u1 = ctx.u1_of(n)
        g = defl(ctx.freeproj(gE(n), n), n, u1)
        gn = float(mnorm(g, h))
        if gn < target: reached = True; break
        # resolution guard
        mx = 0.0
        for a in range(3):
            dot = (n * torch.roll(n, -1, a + 1)).sum(0).clamp(-1, 1)
            mx = max(mx, float(torch.arccos(dot).max()))
        if mx >= math.pi / 2:
            guard = True; break
        delta, status, cgit = steihaug(-g, mu, rad, n, u1)
        Eo = float(energy_noNull(n, h, xi, kap)[0])
        n_try = ctx.pin(n + delta)
        Et = float(energy_noNull(n_try, h, xi, kap)[0])
        actual = Eo - Et
        Hd = Aop(delta, mu, n, u1); pred = -ip(g, delta) - 0.5 * ip(delta, Hd)
        rho = actual / (pred + 1e-30)
        acc = rho > 0.1 and actual > 0
        if acc: n = n_try; mu = max(mu * 0.5, 1e-7)
        else: mu = mu * 3.0
        if rho > 0.75 and status in ('boundary', 'negcurv'): rad = min(rad * 2, 16)
        elif rho < 0.25: rad = max(rad * 0.5, 1e-3)
        traj.append(dict(step=step, t=time.time() - t0, gf_mnorm=gn, E=Eo, mu=mu, rad=rad, rho=rho,
                         cg=status, cg_iters=cgit, accepted=bool(acc), pred=pred, actual=actual,
                         theta_nn_max=mx, displacement=float((n - nstart).norm())))
        if log: log(f"    [{tag}] step={step} gn={gn:.3e} E={Eo:.5f} rho={rho:+.2f} {status}({cgit}) {'ACC' if acc else 'rej'}")
        gc.collect(); torch.cuda.empty_cache()
        if time.time() - t0 > budget: break
    return n, traj, reached, guard

def logline(s, fname):
    print(s, flush=True)
    with open(fname, 'a') as f: f.write(s + '\n')

# ============================== STAGE dirs ==============================
if STAGE == 'dirs':
    LOG = 'F_evidence/F_dirs.log'
    allout = {}
    prev = None
    for Ng in (128, 192, 256):
        ctx = Ctx(Ng)
        d0 = np.load(ctx.s0f); d1 = np.load(ctx.s1f)
        # seed vectors: refine files store V = [dbl0, dbl1, isolated]
        V0 = [ctx.freeproj(torch.tensor(d0['V'][j], device=dev), ctx.n0) for j in range(3)]
        V1 = [ctx.freeproj(torch.tensor(d1['V'][j], device=dev), ctx.n0) for j in range(3)]
        Q_TR, sv, u1 = ctx.tr_gens(ctx.n0)
        def compl(v):
            v = ctx.freeproj(v, ctx.n0); v = v - ip(v, u1) * u1
            for q in Q_TR: v = v - ip(v, q) * q
            return v
        # orthonormalize each seed's doublet in the complement
        def onb2(a, b):
            a = compl(a); a = a / a.norm()
            b = compl(b); b = b - ip(a, b) * a; b = b / b.norm()
            return a, b
        a0, b0 = onb2(V0[0], V0[1]); a1, b1 = onb2(V1[0], V1[1])
        M = np.array([[ip(a0, a1), ip(a0, b1)], [ip(b0, a1), ip(b0, b1)]])
        U, S, Vt = np.linalg.svd(M)
        pang = [float(np.degrees(np.arccos(min(s, 1.0)))) for s in S]
        i0 = compl(V0[2]); i0 = i0 / i0.norm()
        i1 = compl(V1[2]); i1 = i1 / i1.norm()
        iso_ov = abs(ip(i0, i1))
        logline(f"N={Ng}: TR singular values {[f'{x:.3e}' for x in sv]}; doublet principal cosines "
                f"{[f'{s:.10f}' for s in S]} (angles deg {[f'{a:.2e}' for a in pang]}); iso overlap {iso_ov:.10f}", LOG)
        ok_seed = S.min() > 1 - 1e-6 and iso_ov > 1 - 1e-6
        if not ok_seed:
            logline(f"STOP: seed agreement does not reproduce certification at N={Ng}", LOG); raise SystemExit(1)
        # angular origin = seed-0 basis (Procrustes of seed1 documented via M/U/Vt)
        v5, v6, v7 = a0, b0, i0
        Ge = np.array([[ip(x, y) for y in (v5, v6, v7)] for x in (v5, v6, v7)])
        logline(f"N={Ng}: Euclid Gram-I max|err|={np.abs(Ge - np.eye(3)).max():.2e}; "
                f"M=h^3 I Gram = h^3*Gram (h^3={ctx.h**3:.4e}); tangency "
                f"{max(float((v * ctx.n0).sum(0).abs().max()) for v in (v5, v6, v7)):.2e}", LOG)
        np.savez(f'noNull_F_dirs_N{Ng}.npz', v5=v5.cpu().numpy(), v6=v6.cpu().numpy(), v7=v7.cpu().numpy(),
                 N=ctx.N, L=ctx.L, h=ctx.h, procrustes_M=M, tr_sv=sv,
                 src_s0=ctx.s0f, src_s1=ctx.s1f)
        allout[str(Ng)] = dict(tr_singvals=[float(x) for x in sv], principal_cosines=[float(s) for s in S],
                               principal_angles_deg=pang, iso_overlap=iso_ov,
                               gram_err=float(np.abs(Ge - np.eye(3)).max()),
                               dirs_file=f'noNull_F_dirs_N{Ng}.npz', dirs_sha=sha(f'noNull_F_dirs_N{Ng}.npz'))
        # cross-grid alignment (interpolate ONLY for overlap; reproject on destination)
        if prev is not None:
            pv = np.load(f'noNull_F_dirs_N{prev}.npz')
            ups = []
            for k in ('v5', 'v6'):
                z = torch.tensor(pv[k], device=dev).unsqueeze(0)
                zu = torch.nn.functional.interpolate(z, size=(ctx.N,) * 3, mode='trilinear', align_corners=True)[0]
                ups.append(compl(zu))
            ua, ub = onb2(ups[0], ups[1])
            Mx = np.array([[ip(ua, v5), ip(ua, v6)], [ip(ub, v5), ip(ub, v6)]])
            Ux, Sx, Vtx = np.linalg.svd(Mx)
            allout[str(Ng)]['crossgrid_from'] = prev
            allout[str(Ng)]['crossgrid_principal_cosines'] = [float(s) for s in Sx]
            allout[str(Ng)]['crossgrid_procrustes'] = Mx.tolist()
            logline(f"N={Ng}: cross-grid (from {prev}) principal cosines {[f'{s:.6f}' for s in Sx]}", LOG)
            del ups, ua, ub
        prev = Ng
        del ctx, V0, V1, Q_TR
        gc.collect(); torch.cuda.empty_cache()
    json.dump(allout, open('noNull_F_dirs.json', 'w'), indent=1)
    logline('wrote noNull_F_dirs.json', LOG)

# ============================== STAGE gate ==============================
elif STAGE == 'gate':
    LOG = 'F_evidence/F_gate.log'
    out = {}
    for Ng in (128, 192, 256):
        ctx = Ctx(Ng)
        dd = np.load(f'noNull_F_dirs_N{Ng}.npz')
        E0 = float(energy_noNull(ctx.n0, ctx.h, ctx.xi, ctx.kap)[0])
        res = {}
        for name in ('v5', 'v7'):
            v = torch.tensor(dd[name], device=dev)
            wmax = float(v.norm(dim=0).max()); w = v / wmax
            Hw = ctx.hx(ctx.n0, w, ctx.h, ctx.xi, ctx.kap)
            wHw = ip(w, Hw)
            sweep = {}
            trip = [2e-3, 1e-3, 5e-4]; enlarged = False
            for attempt in range(2):
                qs = {}
                for th in trip:
                    np_, _ = geodesic(ctx, v, th)   # geodesic uses w=v/max|v| internally: consistent
                    nm_, _ = geodesic(ctx, v, -th)
                    Ep = float(energy_noNull(np_, ctx.h, ctx.xi, ctx.kap)[0])
                    Em = float(energy_noNull(nm_, ctx.h, ctx.xi, ctx.kap)[0])
                    qs[f'{th:g}'] = (Ep + Em - 2 * E0) / th**2
                    del np_, nm_
                v1, v2 = qs[f'{trip[1]:g}'], qs[f'{trip[2]:g}']
                rel12 = abs(v1 - v2) / max(abs(v1), 1e-30)
                relH = abs(v2 - wHw) / max(abs(wHw), 1e-30)
                if rel12 < 1e-2 and relH < 1e-2:
                    sweep = dict(q=qs, wHw=wHw, rel_smallest_two=rel12, rel_vs_exactHVP=relH,
                                 enlarged=enlarged, gate='PASS'); break
                if attempt == 0:
                    trip = [2 * t for t in trip]; enlarged = True
                    logline(f"N={Ng} {name}: cancellation — enlarging preregistered triplet x2 (recorded)", LOG)
                else:
                    sweep = dict(q=qs, wHw=wHw, rel_smallest_two=rel12, rel_vs_exactHVP=relH,
                                 enlarged=enlarged, gate='FAIL')
            res[name] = sweep
            logline(f"N={Ng} {name}: q(theta)={ {k: round(x, 6) for k, x in sweep['q'].items()} } "
                    f"<w,Hw>={wHw:.6f} rel12={sweep['rel_smallest_two']:.2e} relH={sweep['rel_vs_exactHVP']:.2e} "
                    f"{sweep['gate']}", LOG)
            del v, Hw
        out[str(Ng)] = res
        if any(r['gate'] == 'FAIL' for r in res.values()):
            json.dump(out, open('noNull_F_gate.json', 'w'), indent=1)
            logline('STOP: no controlled quadratic window', LOG); raise SystemExit(1)
        del ctx; gc.collect(); torch.cuda.empty_cache()
    json.dump(out, open('noNull_F_gate.json', 'w'), indent=1)
    logline('GATE PASS at all grids; wrote noNull_F_gate.json', LOG)

# ============================== STAGE control ==============================
elif STAGE == 'control':
    Ng = int(os.environ.get('FN', '128'))
    LOG = f'F_evidence/F_control_N{Ng}.log'
    ctx = Ctx(Ng)
    out = {}
    # 1) two identical unperturbed controls
    ctrls = []
    for rep in (0, 1):
        n, traj, reached, guard = nk_relax(ctx, ctx.n0.clone(), f'ctrl{rep}', log=lambda s: logline(s, LOG))
        ob = ctx.observables(n, ref=ctx.n0)
        ob['reached'] = reached; ob['nsteps'] = len(traj)
        ctrls.append(ob)
        np.savez(f'F_endpoints/control_N{Ng}_rep{rep}.npz', n=n.cpu().numpy(), N=ctx.N, L=ctx.L, h=ctx.h)
        logline(f"control rep{rep}: E={ob['E']:.6f} gn={ob['gf_mnorm']:.3e} Qf={ob['Q_fwd']:.5f} reached={reached}", LOG)
        del n
    sigE = abs(ctrls[0]['E'] - ctrls[1]['E'])
    sigQ = max(abs(ctrls[0]['Q_fwd'] - ctrls[1]['Q_fwd']), abs(ctrls[0]['Q_sym'] - ctrls[1]['Q_sym']))
    sigL = max(abs(ctrls[0]['loc4'][k] - ctrls[1]['loc4'][k]) for k in ctrls[0]['loc4'])
    env = dict(tauE=max(5 * sigE, 1e-3), tauQ=max(5 * sigQ, 0.02), tauLoc=max(5 * sigL, 0.01),
               sigE=sigE, sigQ=sigQ, sigLoc=sigL)
    logline(f"variability: sigE={sigE:.2e} sigQ={sigQ:.2e} sigLoc={sigL:.2e} -> "
            f"tauE={env['tauE']:.3e} tauQ={env['tauQ']:.3f} tauLoc={env['tauLoc']:.3f}", LOG)
    out['controls'] = ctrls; out['envelopes'] = env
    # 2) finite exact-U(1) target rotation invariance control
    al = 0.7
    n0 = ctx.n0
    nrot = torch.stack([math.cos(al) * n0[0] - math.sin(al) * n0[1],
                        math.sin(al) * n0[0] + math.cos(al) * n0[1], n0[2]], 0)
    Er = float(energy_noNull(nrot, ctx.h, ctx.xi, ctx.kap)[0])
    E0 = float(energy_noNull(n0, ctx.h, ctx.xi, ctx.kap)[0])
    Qr = ctx.charges(nrot)
    out['u1_control'] = dict(alpha=al, dE=Er - E0, Q_fwd=Qr[0], Q_sym=Qr[1])
    logline(f"U(1) rotation control: dE={Er - E0:.3e} Qf={Qr[0]:.5f}", LOG)
    # 3) T/R geodesic controls at theta=0.10 (all six at 128; representatives finer)
    Q_TR, sv, u1 = ctx.tr_gens(ctx.n0)
    names = ['Tx', 'Ty', 'Tz', 'Rx', 'Ry', 'Rz']
    pick = range(6) if Ng == 128 else [0, 5]
    trc = {}
    for k in pick:
        nt, realized = geodesic(ctx, Q_TR[k], 0.10)
        n, traj, reached, guard = nk_relax(ctx, nt, f'TR-{names[k]}', log=lambda s: logline(s, LOG))
        ob = ctx.observables(n, ref=ctx.n0); ob['reached'] = reached; ob['realized_theta'] = realized
        trc[names[k]] = ob
        logline(f"T/R control {names[k]}: E={ob['E']:.6f} disp={ob['displacement']:.3f} Qf={ob['Q_fwd']:.5f}", LOG)
        del nt, n
        gc.collect(); torch.cuda.empty_cache()
    out['tr_controls'] = trc
    json.dump(out, open(f'noNull_F_control_N{Ng}.json', 'w'), indent=1)
    logline(f'wrote noNull_F_control_N{Ng}.json', LOG)

# ============================== STAGE ladder / fine ==============================
elif STAGE in ('ladder', 'fine'):
    Ng = int(os.environ.get('FN', '128'))
    LOG = f'F_evidence/F_{STAGE}_N{Ng}.log'
    ctx = Ctx(Ng)
    dd = np.load(f'noNull_F_dirs_N{Ng}.npz')
    v5 = torch.tensor(dd['v5'], device=dev); v6 = torch.tensor(dd['v6'], device=dev)
    v7 = torch.tensor(dd['v7'], device=dev)
    ctrl = json.load(open(f'noNull_F_control_N{Ng}.json'))
    env = ctrl['envelopes']; base = ctrl['controls'][0]
    outf = f'noNull_F_{STAGE}_N{Ng}.json'
    out = json.load(open(outf)) if os.path.exists(outf) else {}
    def classify(ob, reached, guard):
        if guard: return 'UNRESOLVED (pi/2 resolution guard)'
        if not reached or ob['gf_mnorm'] >= 0.05: return 'UNRESOLVED'
        dQf = abs(ob['Q_fwd'] - base['Q_fwd']); dQs = abs(ob['Q_sym'] - base['Q_sym'])
        slip = (abs(ob['Q_fwd']) < abs(base['Q_fwd']) - 0.4) and (abs(ob['Q_sym']) < abs(base['Q_sym']) - 0.4)
        if slip: return 'RESOLVED LATTICE TOPOLOGY SLIP'
        if (abs(ob['Q_fwd']) < abs(base['Q_fwd']) - 0.4) != (abs(ob['Q_sym']) < abs(base['Q_sym']) - 0.4):
            return 'SLIP CANDIDATE / UNRESOLVED'
        dE = ob['E'] - base['E']
        dloc = max(abs(ob['loc4'][k] - base['loc4'][k]) for k in ob['loc4'])
        if dQf < env['tauQ'] and dQs < env['tauQ'] and abs(dE) < env['tauE'] and dloc < env['tauLoc']:
            return 'RETURNED BASIN'
        if dE < -max(env['tauE'], 5e-3) and dQf < env['tauQ'] and dQs < env['tauQ']:
            return 'DISTINCT LOWER Q~1 STATIONARY POINT (pending repeat confirmation)'
        return 'OTHER STATIONARY BRANCH'
    def run_branch(dname, v, theta):
        key = f'{dname}_th{theta:g}'
        if key in out: return out[key]['class']
        nt, realized = geodesic(ctx, v, theta)
        ob0 = dict(E=float(energy_noNull(nt, ctx.h, ctx.xi, ctx.kap)[0]), realized_theta=realized)
        budget = {128: 2400, 192: 6000, 256: 14000}[Ng]
        n, traj, reached, guard = nk_relax(ctx, nt, key, budget=budget, log=lambda s: logline(s, LOG))
        ob = ctx.observables(n, ref=ctx.n0)
        cls = classify(ob, reached, guard)
        np.savez(f'F_endpoints/{STAGE}_N{Ng}_{key}.npz', n=n.cpu().numpy(), N=ctx.N, L=ctx.L, h=ctx.h)
        out[key] = dict(direction=dname, theta=theta, start=ob0, endpoint=ob, reached=bool(reached),
                        guard=bool(guard), nsteps=len(traj), traj=traj, cls=cls, **{'class': cls})
        json.dump(out, open(outf, 'w'), indent=1)
        logline(f"BRANCH {key}: class={cls} E={ob['E']:.6f} dE={ob['E'] - base['E']:+.4e} "
                f"Qf={ob['Q_fwd']:.5f} Qs={ob['Q_sym']:.5f} gn={ob['gf_mnorm']:.3e} disp={ob['displacement']:.3f}", LOG)
        del nt, n
        gc.collect(); torch.cuda.empty_cache()
        return cls
    def dirs_all():
        ds = []
        for k, alpha in enumerate(ANGLES):
            ds.append((f'dbl_a{k}', math.cos(alpha) * v5 + math.sin(alpha) * v6))
        ds.append(('iso_plus', v7)); ds.append(('iso_minus', -v7))
        return ds
    if STAGE == 'ladder':
        for dname, v in dirs_all():
            prev_cls = None
            for i, th in enumerate(LADDER):
                cls = run_branch(dname, v, th)
                if prev_cls is not None and cls != prev_cls:
                    lo, hi = LADDER[i - 1], th
                    for _ in range(3):
                        mid = 0.5 * (lo + hi)
                        cm = run_branch(dname, v, mid)
                        if cm == prev_cls: lo = mid
                        else: hi = mid
                    break
                prev_cls = cls
            else:
                logline(f"{dname}: no transition found within the registered resolved amplitude range", LOG)
        json.dump(out, open(outf, 'w'), indent=1)
        logline(f'ladder complete: wrote {outf}', LOG)
    else:  # fine
        # section 11: no 128 transition -> theta in {0.40,0.80,1.20} for two orthogonal doublet dirs + both iso signs
        FSET = json.loads(os.environ.get('F_FINE_SET', '[]')) or [
            ['dbl_a0', 0.40], ['dbl_a0', 0.80], ['dbl_a0', 1.20],
            ['dbl_a2', 0.40], ['dbl_a2', 0.80], ['dbl_a2', 1.20],
            ['iso_plus', 0.40], ['iso_plus', 0.80], ['iso_plus', 1.20],
            ['iso_minus', 0.40], ['iso_minus', 0.80], ['iso_minus', 1.20]]
        dmap = dict(dirs_all())
        for dname, th in FSET:
            run_branch(dname, dmap[dname], float(th))
        json.dump(out, open(outf, 'w'), indent=1)
        logline(f'fine complete: wrote {outf}', LOG)
print('STAGE', STAGE, 'done', flush=True)
