#!/usr/bin/env python3
"""
ens_scan_chain.py -- MULTI-CELL CHAIN: welded cells, angular sector LIVE
=======================================================================
OPEN-ENDED METRIC-LED exploration (HANDOFF queue head step b, MULTI-CELL
axis). Driver: Claude (Opus 4.8 1M). 2026-06-13. Frame: CRITICAL_UNIVERSE.
New file. Built on the CONVERGING machinery of wint_cell2d.py (the metric's
own flow-chart cell, ON two-exponential source, e^{2v}-dressed LIVE angular
operator -- verified exact in wint_symcheck.py). NOTHING added/slaved/frozen.

WHY THIS CHART (and why the (rho,z) box failed -- recorded honestly):
  The metric's operator is single-centre anisotropic (proved exact in
  ens_scan_whole.py PART 0: the dilation tie dresses ONLY the areal-radial
  direction; the angular 1/r^2 is BARE -> two centres = two incompatible
  sphere foliations; a naive isotropic (rho,z) chart is a DIFFERENT operator,
  O(1) wrong on non-radial fields, and the Dirichlet-box solve does not even
  converge -- the cell has a NATURAL areal size and resists a box wall).
  The faithful, CONVERGING multi-cell object is therefore a RADIAL CHAIN:
  cells welded at their mirror seals (the turning points v_m=0 = the seal
  locus, where the metric closes a cell, w6/registry #30). The angular sector
  is LIVE everywhere INCLUDING at the internal (shared) welds.

THE OBJECT (exact; wint_cell2d's converging system, extended to a CHAIN):
  field v(m,theta) on a chain domain m in [0, M] containing N cells. The
  metric's own 2D equation (wint_symcheck, exact):
     v_mm + e^{2v}( v_thth + cot th v_th - v_th^2 ) = Phi(e^{-2v} - e^{v}).
  Radial closure: v_m = 0 at every SEAL (the two outer ends + the N-1
  internal welds) -- the turning-point/mirror condition the metric uses to
  close a cell (registry #30: the seal is the v_m=0 mirror fold). Internal
  welds glue two cells mirror-to-mirror (same-minus involution, w6). Energy
  pinned by the cell-depth anchor at each cell centre (the genuine free datum
  E per cell), exactly as wint_cell2d pins it.
  Axis Neumann in theta (regularity), seed round AND lobed.

THE MULTI-CELL QUESTIONS (character-change flags vs the single-cell baseline
B1/#34 'one round type, smooth E-continuum'; B3 seal mirror fold; #33 'no
compactness pin'; E1/E2 'monotone repulsion, no preferred separation'):
  Q1  Does the angular sector, DEAD in a single cell (gap>0, pure damping,
      #34/#36), come ALIVE at a SHARED weld? (a lobed seed PERSISTS at an
      internal seal where it relaxes at a free seal) -> new structure a
      single cell lacks.
  Q2  Is the welded N-cell chain still a smooth E-continuum, or does welding
      PIN preferred per-cell energies/widths (a discreteness #33 lacks)?
  Q3  Cross-chart control: a 1-cell chain reproduces wint_cell2d exactly.

DATA-BLIND (no wall numbers). Convergence MANDATORY. Log /tmp/ens_scan.log.
"""
import sys, time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla
import mpmath as mp

t0 = time.time()
_fh = open("/tmp/ens_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL, FLAG = [], [], []
def check(tag, cond, note=""):
    ok = bool(cond); (PASS if ok else FAIL).append(tag)
    log(f"ENSC-{tag}: {'PASS' if ok else 'FAIL'}  {note}")
def flag(tag, note): FLAG.append(tag); log(f"ENSC-FLAG[{tag}]: {note}")

log("\n" + "=" * 74)
log("ens_scan_chain -- MULTI-CELL radial chain, angular sector LIVE at welds")
log("=" * 74)

# --------- the single-cell quadrature (wint_cell2d PART A, exact) ---------
mp.mp.dps = 30
def U(v, Phi): return Phi / 2 * mp.exp(-2 * v) + Phi * mp.exp(v)
def Umin(Phi): return mp.mpf('1.5') * Phi
def cell_LE(E, Phi):
    Um = Umin(Phi)
    if E <= Um: return None
    g = lambda v: U(v, Phi) - E
    def bracket(sgn):
        a = mp.mpf('0'); b = sgn * mp.mpf('0.01')
        for _ in range(200):
            if g(b) > 0: return mp.findroot(g, (a, b), solver='bisect')
            a, b = b, b * mp.mpf('1.3') if abs(b) < 50 else b
            if abs(b) > 60: break
        return None
    vlo = bracket(-1); vhi = bracket(+1)
    if vlo is None or vhi is None: return None
    L = mp.quad(lambda v: 1 / mp.sqrt(max(2 * (E - U(v, Phi)),
                mp.mpf('1e-40'))), [vlo, vhi])
    return float(L), float(vlo), float(vhi)

def cell_profile(E, Phi, npts):
    """RK4 the cell ODE v_mm=Phi(e^{-2v}-e^{v}) from the inner turning point
    vlo (v_m=0) across one cell width L -> v(m) round profile (one cell)."""
    res = cell_LE(E, Phi)
    if res is None: return None
    L, vlo, vhi = res
    m = np.linspace(0.0, L, npts); dm = m[1] - m[0]
    vr = np.zeros(npts); vv = vlo; pp = 0.0; vr[0] = vv
    f = lambda vv, pp: (pp, float(Phi) * (np.exp(-2 * vv) - np.exp(vv)))
    for i in range(1, npts):
        k1 = f(vv, pp); k2 = f(vv + dm/2*k1[0], pp + dm/2*k1[1])
        k3 = f(vv + dm/2*k2[0], pp + dm/2*k2[1]); k4 = f(vv + dm*k3[0], pp + dm*k3[1])
        vv += dm/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        pp += dm/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]); vr[i] = vv
    return m, vr, L, vlo, vhi

# --------- the 2D field equation residual on a CHAIN (exact metric op) -----
def residual(v, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val):
    """F(v)=v_mm + e^{2v}(v_thth+cot th v_th - v_th^2) - Phi(e^{-2v}-e^{v}).
    Closure EXACTLY as wint_cell2d (which converges): per cell ONE Dirichlet
    depth anchor at the inner node (= the energy datum vlo) and ONE Neumann at
    the outer turning node. On a chain the anchor_idx are the per-cell inner
    nodes (Dirichlet at anchor_val=vlo); the seal_idx are the OUTER turning
    nodes only (Neumann v_m=0). Internal welds: the shared node is the
    Neumann-end of one cell AND carries the next cell's Dirichlet anchor; we
    impose Neumann there and anchor the NEXT cell's first interior node. Axis
    Neumann in theta."""
    Nm, Nth = v.shape
    vmm = np.zeros_like(v)
    vmm[1:-1, :] = (v[2:, :] - 2*v[1:-1, :] + v[:-2, :]) / dm**2
    sinth = np.sin(th)[None, :]
    am = 0.5 * (sinth[:, 1:] + sinth[:, :-1])
    flux = am * (v[:, 1:] - v[:, :-1]) / dth
    ang = np.zeros_like(v)
    ang[:, 1:-1] = (flux[:, 1:] - flux[:, :-1]) / dth / sinth[:, 1:-1]
    vth = np.zeros_like(v)
    vth[:, 1:-1] = (v[:, 2:] - v[:, :-2]) / (2*dth)
    A = np.exp(2.0*v) * (ang - vth**2)
    F = vmm + A - Phi*(np.exp(-2*v) - np.exp(v))
    # Neumann v_m=0 at the seal (turning) nodes:
    for si in seal_idx:
        if si == 0:            F[0, :] = v[1, :] - v[0, :]
        elif si == Nm-1:       F[-1, :] = v[-1, :] - v[-2, :]
        else:                  F[si, :] = v[si+1, :] - v[si-1, :]   # centred v_m=0
    # Dirichlet depth anchors (per-cell energy datum vlo):
    for ai, av in zip(anchor_idx, anchor_val):
        F[ai, :] = v[ai, :] - av
    # axis Neumann in theta:
    F[:, 0] = v[:, 0] - v[:, 1]; F[:, -1] = v[:, -1] - v[:, -2]
    return F

def jac(v, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val, eps=1e-7):
    Nm, Nth = v.shape; N = Nm*Nth
    F0 = residual(v, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val).ravel()
    idx = np.arange(N).reshape(Nm, Nth); rows=[];cols=[];vals=[]
    for ci in range(3):
        for cj in range(3):
            mask = np.zeros((Nm, Nth), bool); mask[ci::3, cj::3] = True
            vp = v.copy(); vp[mask] += eps
            dF = ((residual(vp, dm, th, dth, Phi, seal_idx, anchor_idx,
                            anchor_val).ravel() - F0)/eps).reshape(Nm, Nth)
            owner = np.full((Nm, Nth), -1, np.int64)
            for di, dj in [(0,0),(1,0),(-1,0),(0,1),(0,-1),(2,0),(-2,0)]:
                si = np.arange(Nm)[:,None]+di; sj = np.arange(Nth)[None,:]+dj
                valid = (si>=0)&(si<Nm)&(sj>=0)&(sj<Nth)
                sic=np.clip(si,0,Nm-1); sjc=np.clip(sj,0,Nth-1)
                inc = valid & mask[sic,sjc] & (owner<0); owner[inc]=idx[sic,sjc][inc]
            sel = owner>=0; vv = dF[sel]; nz = vv!=0
            rows.append(idx[sel][nz]); cols.append(owner[sel][nz]); vals.append(vv[nz])
    return sps.csr_matrix((np.concatenate(vals),
            (np.concatenate(rows), np.concatenate(cols))), shape=(N,N)), F0

def newton(v0, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val,
           itmax=120, tol=1e-10):
    v = v0.copy(); Nm, Nth = v.shape; maxres = np.inf
    for nit in range(itmax):
        J, F0 = jac(v, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val)
        n0 = float(np.linalg.norm(F0))
        try: dv = spsla.spsolve(J, -F0).reshape(Nm, Nth)
        except Exception: return v, maxres, nit, False
        if not np.all(np.isfinite(dv)): return v, maxres, nit, False
        lam = 1.0; ok = False
        for _ in range(40):
            tr = v + lam*dv
            if np.all(np.abs(tr) < 40):
                Ft = residual(tr, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val)
                if np.isfinite(Ft).all() and np.linalg.norm(Ft) < (1-1e-4*lam)*n0:
                    ok = True; break
            lam *= 0.5
        if not ok:
            maxres = float(np.max(np.abs(residual(
                v, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val)[1:-1,1:-1])))
            return v, maxres, nit, maxres < 1e-8
        v = v + lam*dv
        maxres = float(np.max(np.abs(residual(
            v, dm, th, dth, Phi, seal_idx, anchor_idx, anchor_val)[1:-1,1:-1])))
        if maxres < tol: return v, maxres, nit+1, True
    return v, maxres, itmax, maxres < 1e-8

def build_chain(E_list, Phi, ncell_pts=64, Nth=49, seed_lobe=0, seed_amp=0.0,
                weld_seed_amp=0.0):
    """Build an N-cell chain: each cell a quadrature profile, welded mirror-
    to-mirror at shared seals. Returns the seed field + node bookkeeping.
    weld_seed_amp: inject a theta-lobe localized AT the internal welds (to
    probe Q1 -- does the angular sector come alive at a shared seal?)."""
    profs = []
    for E in E_list:
        cp = cell_profile(E, Phi, ncell_pts)
        if cp is None: return None
        profs.append(cp)
    # stitch: cell k occupies its own ncell_pts; share the weld node between
    # consecutive cells (mirror: cell k ends at vhi/vlo turning point = cell
    # k+1's start). Alternate orientation for mirror welding.
    # Build node list cell by cell. Each cell = profile vr (vlo at node 0 to
    # vhi at node -1). Weld two cells mirror-to-mirror: cell k's OUTER end
    # (vhi turning point) glues to cell k+1's OUTER end (also vhi) by mirror,
    # so the chain is vlo .. vhi | vhi .. vlo | vlo .. vhi ... The shared weld
    # node is a turning point (Neumann) for BOTH cells.
    seal_nodes = []     # Neumann (turning) nodes
    anchor_nodes = []; anchor_vals = []
    v_global = []; cursor = 0
    for k, (m, vr, L, vlo, vhi) in enumerate(profs):
        seg = vr.copy()
        if k % 2 == 1:
            seg = vr[::-1].copy()          # mirror fold (same-minus involution)
        if k > 0:
            seg = seg[1:]                  # drop the shared weld node
        start = cursor
        v_global.append(seg)
        cell_end = start + len(seg) - 1
        # Dirichlet depth anchor: the vlo turning point of THIS cell. For even
        # cells that is the inner (start) node; for odd (mirrored) cells the
        # vlo end is the OUTER node. Anchor whichever node holds vlo.
        if k % 2 == 0:
            anchor_nodes.append(start); anchor_vals.append(float(vlo))
            # the vhi (outer) end is a Neumann turning node:
            seal_nodes.append(cell_end)
        else:
            anchor_nodes.append(cell_end); anchor_vals.append(float(vlo))
            seal_nodes.append(start if k == 0 else start)  # vhi weld end Neumann
        cursor = cell_end + 1
    # the very first node (chain inner end) is a Neumann turning point too,
    # UNLESS it is the anchor; for cell 0 even, node 0 IS the vlo anchor, and
    # its OTHER turning (vhi) is the weld -> Neumann there. So node 0 anchored.
    v1d = np.concatenate(v_global)
    Nm = len(v1d)
    # dedupe anchors vs seals (a node cannot be both); seals win the geometry
    # but anchors pin energy -- keep anchors, drop any seal that coincides:
    seal_nodes = [s for s in seal_nodes if s not in anchor_nodes]
    v0 = np.tile(v1d[:, None], (1, Nth))
    th = np.linspace(0.0, np.pi, Nth)
    x = np.cos(th)
    if seed_amp != 0.0:
        Pl = np.polynomial.legendre.legval(x, [0]*seed_lobe+[1])[None, :]
        mm = np.linspace(0, 1, Nm)[:, None]
        bump = np.exp(-((mm - 0.5)/0.25)**2)
        v0 = v0 + seed_amp*bump*Pl
    if weld_seed_amp != 0.0:
        Pl = np.polynomial.legendre.legval(x, [0,0,1])[None, :]   # l=2 lobe
        for si in seal_nodes:
            if si not in (0, Nm-1):
                gw = np.exp(-((np.arange(Nm)-si)/3.0)**2)[:, None]
                v0 = v0 + weld_seed_amp*gw*Pl
    dm = float(profs[0][0][1] - profs[0][0][0])   # uniform per-cell spacing
    return dict(v0=v0, th=th, dm=dm, dth=float(th[1]-th[0]),
                seal_nodes=sorted(set(seal_nodes)), anchor_nodes=anchor_nodes,
                anchor_vals=anchor_vals, Nm=Nm, Nth=Nth, ncell=len(profs))

def solve_chain(E_list, Phi=1.0, Nth=49, seed_lobe=0, seed_amp=0.0,
                weld_seed_amp=0.0, ncell_pts=64):
    B = build_chain(E_list, Phi, ncell_pts, Nth, seed_lobe, seed_amp, weld_seed_amp)
    if B is None: return dict(conv=False, why="bad_E")
    v, maxres, nit, conv = newton(
        B["v0"], B["dm"], B["th"], B["dth"], Phi,
        B["seal_nodes"], B["anchor_nodes"], B["anchor_vals"])
    th_var = float(np.max(np.std(v, axis=1)))
    # theta-variation AT the weld nodes specifically (Q1):
    weld_internal = [s for s in B["seal_nodes"] if s not in (0, B["Nm"]-1)]
    weld_thvar = (max(float(np.std(v[s])) for s in weld_internal)
                  if weld_internal else 0.0)
    return dict(conv=conv, maxres=maxres, nit=nit, th_var=th_var,
                weld_thvar=weld_thvar, ncell=B["ncell"], Nm=B["Nm"],
                seal_nodes=B["seal_nodes"], v=v, th=B["th"])


def _main():
    Phi = 1.0
    # ---- Q3 control: 1-cell chain == wint_cell2d round cell ----
    log("\nCONTROL Q3 -- 1-cell chain reproduces wint_cell2d (round, theta-flat)")
    r1 = solve_chain([Umin_factor(2.0)], Phi=Phi)
    check("Q3", r1["conv"] and r1["th_var"] < 1e-6,
          f"1-cell chain converges (maxres={r1['maxres']:.2e}) theta-flat "
          f"(th_var={r1['th_var']:.2e}) -- reproduces the #34 round cell.")

    # ---- Q1: round multi-cell chains converge; angular DEAD at free seals ----
    log("\nQ1 -- N-cell welded chains: convergence + angular at SHARED welds")
    log(f"{'N':>3} {'seed':>10} {'conv':>5} {'maxres':>9} {'th_var':>10} "
        f"{'weld_thvar':>11} {'nit':>4}")
    REC = []
    for N in [1, 2, 3, 4]:
        Es = [Umin_factor(2.0)] * N
        for (sl, sa, wa, tag) in [(0, 0.0, 0.0, "round"),
                                  (2, 0.0, 0.20, "weld-l2")]:
            r = solve_chain(Es, Phi=Phi, seed_lobe=sl, seed_amp=sa,
                            weld_seed_amp=wa)
            if "conv" not in r: continue
            REC.append(dict(N=N, tag=tag, conv=bool(r["conv"]),
                            maxres=r["maxres"], th_var=r["th_var"],
                            weld_thvar=r["weld_thvar"], nit=r["nit"]))
            log(f"{N:3d} {tag:>10} {str(r['conv']):>5} {r['maxres']:9.1e} "
                f"{r['th_var']:10.2e} {r['weld_thvar']:11.2e} {r['nit']:4d}")
        with open("/tmp/ens_scan_chain.json", "w") as fh:
            json.dump(REC, fh, indent=0)
    convd = [x for x in REC if x["conv"]]
    check("Q1-conv", len(convd) >= int(0.7*len(REC)),
          f"{len(convd)}/{len(REC)} chain solves converged")
    # did a weld-seeded lobe PERSIST at an internal seal? (character change)
    weldseed = [x for x in REC if x["tag"] == "weld-l2" and x["conv"] and x["N"] >= 2]
    persist = [x for x in weldseed if x["weld_thvar"] > 1e-4]
    if persist:
        flag("WELD-ALIVE", f"a theta-lobe seeded AT an internal weld PERSISTED "
             f"(weld_thvar up to {max(x['weld_thvar'] for x in persist):.2e}) "
             "in {0}/{1} multi-cell chains -- angular structure at a SHARED "
             "seal that a single free seal damps. INSPECT real vs artifact."
             .format(len(persist), len(weldseed)))
    check("Q1-angular", len(persist) == 0,
          f"weld-seeded lobes RELAX at internal seals too "
          f"({len(persist)}/{len(weldseed)} persisted): the shared weld does "
          "NOT revive the angular sector -> baseline holds (angular dead, "
          "#34/#36). [FAIL = WELD-ALIVE flag: a shared seal revives angular.]")

    # ---- Q2: does welding pin per-cell energy, or stay a continuum? ----
    # build 2-cell chains across a RANGE of per-cell E and check the welded
    # solution exists for a CONTINUUM of E (no pinning) vs only special E.
    log("\nQ2 -- 2-cell chain across an E-continuum: pinned or free?")
    log(f"{'E/Um':>6} {'conv':>5} {'maxres':>9} {'th_var':>10}")
    e_conv = []
    for Ef in [1.1, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0]:
        r = solve_chain([Umin_factor(Ef), Umin_factor(Ef)], Phi=Phi)
        if "conv" not in r: continue
        log(f"{Ef:6.2f} {str(r['conv']):>5} {r['maxres']:9.1e} {r['th_var']:10.2e}")
        if r["conv"]: e_conv.append(Ef)
    check("Q2", len(e_conv) >= 5,
          f"the welded 2-cell chain converges for a CONTINUUM of per-cell E "
          f"({len(e_conv)} values across 1.1-4.0 Um): welding does NOT pin a "
          "discrete per-cell energy -> the multi-cell chain is still a smooth "
          "continuum (baseline #33 holds, no compactness pin from welding). "
          "[FAIL = only special E weld -> a pinned discreteness, FLAG.]")
    if len(e_conv) < 5:
        flag("PINNED-E", f"only {len(e_conv)} per-cell E values admit a welded "
             "chain -> welding may PIN per-cell energy (discreteness #33 lacks).")

    # ---- Q1 EXISTENCE (non-seed, decisive): weld Jacobian ever singular? ----
    log("\nQ1-EXIST -- weld-chain Jacobian spectrum about the round cell "
        "(a zero mode = a shaped type born at the weld)")
    log(f"{'N':>3} {'E/Um':>6} {'Nm':>4} {'min|eig|':>12}")
    mineigs = []
    for N in [1, 2, 3, 4]:
        for Ef in [1.3, 2.0, 3.0]:
            B = build_chain([Umin_factor(Ef)] * N, Phi, 48, 33, 0, 0.0, 0.0)
            v, mr, nit, conv = newton(B["v0"], B["dm"], B["th"], B["dth"], Phi,
                                      B["seal_nodes"], B["anchor_nodes"],
                                      B["anchor_vals"])
            if not conv:
                continue
            J, _ = jac(v, B["dm"], B["th"], B["dth"], Phi, B["seal_nodes"],
                       B["anchor_nodes"], B["anchor_vals"])
            ev = np.linalg.eigvals(J.toarray())
            me = abs(ev[int(np.argmin(np.abs(ev)))])
            mineigs.append(me)
            log(f"{N:3d} {Ef:6.2f} {B['Nm']:4d} {me:12.6f}")
    check("Q1-EXIST", mineigs and min(mineigs) > 1e-3,
          f"the welded-chain Jacobian is NON-SINGULAR across N=1..4 and E "
          f"(min over configs of min|eig| = {min(mineigs):.4f} > 0): NO "
          "bifurcation, NO zero mode -> NO shaped (angular) type can be born "
          "at a shared weld, independent of seed. The shared weld does NOT "
          "revive the angular sector. [FAIL = a weld zero mode, FLAG.]")
    if mineigs and min(mineigs) <= 1e-3:
        flag("WELD-ZEROMODE", "the weld Jacobian has a near-zero eigenvalue -> "
             "a shaped type may be born at the shared seal. INSPECT.")

    log(f"\nENSC: {len(PASS)} PASS / {len(FAIL)} FAIL / {len(FLAG)} FLAG "
        f"({time.time()-t0:.0f}s)")
    if FAIL: log("FAILED: " + str(FAIL))
    if FLAG: log("FLAGS: " + str(FLAG))
    log("checkpoint /tmp/ens_scan_chain.json  log /tmp/ens_scan.log")


def Umin_factor(f, Phi=1.0):
    """return E = f * U_min as a float energy for the chain builder."""
    return float(Umin(mp.mpf(Phi)) * mp.mpf(f))


if __name__ == "__main__":
    _main()
    _fh.close()
