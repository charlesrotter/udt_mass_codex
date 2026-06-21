#!/usr/bin/env python3
"""
p5c_barriers.py -- P5c-step-4 BARRIER HEIGHTS between same-charge floored basins
(string / NEB method) + FULL-DIRECTION (metric+matter) stability.  DIAGNOSTIC ONLY.

Driver: claude-opus-4-8[1m].  2026-06-20.  OBSERVE (not target).  DATA-BLIND.
Branch: p5c-barriers.  NEW FILE (committed full3d_*/p5c_* reused as imports only;
NEVER edited).

THE QUESTION (Charles, OBSERVE-not-target): are the >=5 distinct same-charge floored
solutions a GENUINE DURABLE FAMILY (HIGH barriers between basins => distinct objects
that cannot slump into each other) or METASTABLE WIGGLES of one object (LOW barriers
=> not a family)?  We MEASURE the barrier; we do NOT go in wanting a family.

------------------------------------------------------------------------------------
WHY this is a genuine NEB, NOT a "blend toward an endpoint" (the prior artifact):
  The shelved 'melt' test BLENDED u=(1-s)basin+s*round and re-solved with ALL DOF
  free -- which just let the field flow to whichever well the blend was nearest, and
  was (correctly) condemned as biased dynamics.  A NEB/string is different: it pins
  the IMAGE'S POSITION ALONG THE PATH (the projection onto the chord between the two
  fixed floored endpoints) and relaxes EVERYTHING PERPENDICULAR to that chord.  No
  image can slide to an endpoint -- each is held at its own path coordinate s_k -- so
  the relaxed string traces the LOWEST ENERGY RIDGE connecting the two basins, and
  max-S along it is the genuine saddle/barrier.  Endpoints are FIXED (the saved floored
  solutions).  This is the standard transition-state construction, not a blend.

METHOD (string with a chord constraint, constraint-respecting per image):
  endpoints  u_A, u_B  = two SAVED floored basins (interpolate between SAVED fields --
                         no full re-solve from scratch).
  chord      e = (u_B - u_A) / |u_B - u_A|    (unit direction in field space)
  image k    s_k in (0,1):  start  u_k0 = (1-s_k) u_A + s_k u_B  (BC rows re-pinned).
  For each interior image we MINIMIZE the residual Phi subject to holding its chord
  projection at s_k:  i.e. damped-Gauss-Newton steps on the residual, with the step
  PROJECTED to remove its component along e after each update (P_perp du), and a
  restorer that re-pins <u_k - u_A, e> = s_k|u_B-u_A| each iter.  This relaxes the
  image perpendicular to the path (NEB transverse relaxation) while its position along
  the path is frozen -> it cannot collapse to an endpoint.
  ENERGY along the string = the native matter action S (= p5c_basins.energy_proxy,
  recomputed inline; the committed matter_action has a cosmetic RETURN bug, not in the
  value).  BARRIER = max_k S(u_k_relaxed) - max(S(u_A), S(u_B))  (above the HIGHER
  endpoint).  We ALSO report barrier/gap where gap = |S(basin) - S(round)|.

INTERPRETATION (stated UP FRONT, observe-not-target):
  - barrier >> the round<->basin energy gap AND >> numerical noise  => GENUINE distinct
    durable objects (family plausible).
  - barrier ~ 0 / comparable to noise                              => metastable wiggles
    / not distinct (not a family).
  We report the NUMBERS and which criterion they meet -- no verdict-hunting.

ANTI-HANG (binding, #1 -- FOUR+ prior agents hung):
  - SINGLE clean process per pair, SEQUENTIAL, never concurrent.  ONE pair per call.
  - RECOMPUTE ON SAVED FIELDS: endpoints are loaded; only the (few) interior images
    are relaxed, with a BOUNDED per-image iter cap.  Nr=12 only (the saved basin set).
  - 5 images default (3 interior to relax); each interior image <= NEBIT transverse
    GN iters; full pair << 6 min at Nr=12.  NEVER background poll.  If over budget,
    REDUCE images / iters and report "throughput-limited".

USAGE (one pair per process):
  python3 p5c_barriers.py pair NR A B [NIMG] [NEBIT]   # barrier for basin pair A<->B
  python3 p5c_barriers.py report NR                     # assemble barrier table
"""
import os, sys, time, json, glob, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import (Grid3D, attach_coord_weight, residuals, diagnostics,
    build_metric, field_dn, DEV)
from full3d_solver import residual_vector, unpack, pack
from full3d_newton import jacobian_jacrev, residual_vector_vsafe
import whole_metric_3d_matter as MAT
import whole_metric_3d_core as CORE

P, KAP8 = 0.4, 0.05
BASINS = ['round', 'oblate', 'pert_s', 'prolate', 'toroidal']


def make_grid(NR):
    NTH = 6 if NR == 12 else 8
    G = Grid3D(NR, NTH, 8, rc=0.05, cell=14.0); return attach_coord_weight(G)


def load_u(NR, name):
    return torch.load(f"/tmp/p5c_basin_{NR}_{name}.pt")['u'].to(DEV)


def action_S(G, u):
    """native matter action S = int sqrt(-g)(L2+L4) dV on field u (inline; avoids the
       cosmetic return bug in the committed matter_action -- identical algebra)."""
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d); ginv = CORE.metric_inverse(g)
    dn = field_dn(G, Th, m=1); Gmn = MAT.field_metric(dn)
    L, _, _, _ = MAT.lagrangian(ginv, Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    return float((sqrtg * L * G.wvol_coord).sum())


def repin_bc(G, u, p=P):
    """re-pin the BC rows of an interpolated seed so it starts charge-1 winding."""
    a, b, c, d, Th = unpack(u, G)
    Th = Th.clone(); Th[0] = np.pi; Th[-1] = 0.0
    a = a.clone(); a[-1] = 0.0
    b = b.clone(); b[0] = -p
    c = c.clone(); c[0] = 0.0; c[-1] = 0.0
    d = d.clone(); d[0] = 0.0; d[-1] = 0.0
    return pack(a, b, c, d, Th)


def relax_image_transverse(G, u_init, u_A, e, chordlen, s_k, nebit, wbc=30.0):
    """Relax one string image PERPENDICULAR to the chord e, holding its chord
       projection at s_k*chordlen.  Damped Gauss-Newton on the residual; after each
       step project OUT the along-chord component of du (P_perp) and restore the exact
       chord position.  Endpoints are NEVER moved (only interior images call this).
       Returns (u_relaxed, Phi, S, its)."""
    u = u_init.detach().clone()
    lam = 1e-4
    target_proj = s_k * chordlen
    nU = u.numel(); I = torch.eye(nU, device=u.device)

    def restore(uu):
        # re-pin BCs then snap chord projection back to target (move only along e)
        uu = repin_bc(G, uu)
        proj = float(torch.dot(uu - u_A, e))
        uu = uu + (target_proj - proj) * e
        return uu

    u = restore(u)
    F = residual_vector_vsafe(u, G, P, KAP8, m=1, wbc=wbc)
    Phi = float((F*F).sum())
    its = 0
    for it in range(nebit):
        if Phi < 1e-12:
            break
        J, F = jacobian_jacrev(u, G, P, KAP8, m=1, wbc=wbc, chunk_size=256)
        accepted = False
        for _try in range(10):
            try:
                Jaug = torch.cat([J, math.sqrt(lam)*I], dim=0)
                Faug = torch.cat([-F, torch.zeros(nU, device=u.device)], dim=0)
                du = torch.linalg.lstsq(Jaug, Faug).solution
            except Exception:
                lam *= 4.0; continue
            # PROJECT OUT the along-chord component -> transverse-only move (NEB)
            du = du - torch.dot(du, e) * e
            un = restore(u + du)
            Pn = float((residual_vector_vsafe(un, G, P, KAP8, m=1, wbc=wbc)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.25, 1e-14); accepted = True; break
            lam *= 4.0
        its = it + 1
        if not accepted:
            break
    S = action_S(G, u)
    return u, Phi, S, its


def cmd_pair(NR, A, B, nimg, nebit):
    G = make_grid(NR)
    u_A = load_u(NR, A); u_B = load_u(NR, B)
    diff = (u_B - u_A); chordlen = float(diff.norm())
    e = diff / chordlen
    S_A = action_S(G, u_A); S_B = action_S(G, u_B)
    M_A = diagnostics(G, residuals(G, unpack(u_A, G), P, KAP8), KAP8)['M_MS']
    M_B = diagnostics(G, residuals(G, unpack(u_B, G), P, KAP8), KAP8)['M_MS']
    # round endpoint for gap reference (gap of each basin to round)
    try:
        u_R = load_u(NR, 'round'); S_R = action_S(G, u_R)
    except Exception:
        S_R = None
    print(f"[pair {NR} {A}<->{B}] chordlen={chordlen:.3f}  "
          f"S_{A}={S_A:.4e}(M={M_A:.4f})  S_{B}={S_B:.4e}(M={M_B:.4f})  "
          f"nimg={nimg} nebit={nebit}", flush=True)
    s_vals = np.linspace(0.0, 1.0, nimg)
    images = []
    # endpoints (fixed) carry their own S
    images.append(dict(s=0.0, S=S_A, Phi=0.0, its=0, kind='endpoint'))
    t_all = time.time()
    for s_k in s_vals[1:-1]:
        u0 = repin_bc(G, (1 - s_k) * u_A + s_k * u_B)
        S0 = action_S(G, u0)  # un-relaxed (raw interpolation) energy, for contrast
        t0 = time.time()
        ur, Phi, S, its = relax_image_transverse(G, u0, u_A, e, chordlen, s_k, nebit)
        proj = float(torch.dot(ur - u_A, e)) / chordlen
        print(f"  s={s_k:.3f}: raw S={S0:.4e} -> relaxed S={S:.4e} Phi={Phi:.1e} "
              f"its={its} proj={proj:.3f} wall={time.time()-t0:.0f}s", flush=True)
        images.append(dict(s=float(s_k), S=S, S_raw=S0, Phi=Phi, its=its,
                           proj=proj, kind='image'))
    images.append(dict(s=1.0, S=S_B, Phi=0.0, its=0, kind='endpoint'))
    # BARRIER measures (using the |S| magnitude convention -- S is negative; the
    # native action is more negative at higher-mass basins.  We report on |S| so a
    # "barrier" is a LOCAL RISE in |S| ridge... but the energy ordering used elsewhere
    # is |S| ascending = round< ...<toroidal.  To avoid sign confusion we report BOTH:
    #  (i) raw S extremum along path, (ii) |S| convention barrier.)
    Svals = np.array([im['S'] for im in images])
    absS = np.abs(Svals)
    higher_endpoint_absS = max(abs(S_A), abs(S_B))
    lower_endpoint_absS = min(abs(S_A), abs(S_B))
    # A barrier in |S|: does the interior |S| RISE above the higher endpoint, OR DIP
    # below the lower endpoint?  A TRANSITION STATE between two minima of an energy E
    # is a MAX of E.  Here the "energy" proxy is |S| (ascending order = the basin
    # ladder).  Barrier_above = max interior |S| - higher endpoint |S|  (a ridge).
    # We also report the DIP = lower endpoint |S| - min interior |S| (if the path goes
    # BELOW both, the interp passes through a lower-energy region = no separating wall).
    interior_absS = absS[1:-1] if len(absS) > 2 else absS
    barrier_above = float(interior_absS.max() - higher_endpoint_absS) if len(interior_absS) else 0.0
    dip_below = float(lower_endpoint_absS - interior_absS.min()) if len(interior_absS) else 0.0
    gap_AB = abs(abs(S_A) - abs(S_B))
    gap_A_round = abs(abs(S_A) - abs(S_R)) if S_R is not None else None
    gap_B_round = abs(abs(S_B) - abs(S_R)) if S_R is not None else None
    ratio = (barrier_above / gap_AB) if gap_AB > 1e-12 else float('inf')
    print(f"  ABS-S path: A={abs(S_A):.3e} interior=[{interior_absS.min():.3e},"
          f"{interior_absS.max():.3e}] B={abs(S_B):.3e}", flush=True)
    print(f"  BARRIER (|S| above higher endpoint) = {barrier_above:.4e} | "
          f"DIP below lower endpoint = {dip_below:.4e} | gap_AB={gap_AB:.4e} | "
          f"barrier/gap={ratio:.3f}", flush=True)
    print(f"  (gap to round: {A}={gap_A_round}  {B}={gap_B_round})", flush=True)
    print(f"  [pair {A}<->{B}] total wall={time.time()-t_all:.0f}s", flush=True)
    rec = dict(NR=NR, A=A, B=B, chordlen=chordlen, S_A=S_A, S_B=S_B, M_A=M_A, M_B=M_B,
               S_round=S_R, images=images, barrier_above=barrier_above,
               dip_below=dip_below, gap_AB=gap_AB, gap_A_round=gap_A_round,
               gap_B_round=gap_B_round, ratio=ratio, nimg=nimg, nebit=nebit)
    json.dump(rec, open(f"/tmp/p5c_barrier_{NR}_{A}__{B}.json", "w"), indent=1)


def cmd_report(NR):
    print(f"\n=== P5c-step-4 BARRIER TABLE  Nr={NR} ===", flush=True)
    print("  pair | barrier(|S| above higher) | dip below lower | gap_AB | "
          "barrier/gap | nimg | max image Phi | nebit", flush=True)
    for fp in sorted(glob.glob(f"/tmp/p5c_barrier_{NR}_*.json")):
        r = json.load(open(fp))
        maxphi = max((im.get('Phi', 0.0) for im in r['images'] if im['kind'] == 'image'),
                     default=0.0)
        print(f"  {r['A']}<->{r['B']} | {r['barrier_above']:.4e} | "
              f"{r['dip_below']:.4e} | {r['gap_AB']:.4e} | {r['ratio']:.3f} | "
              f"{r['nimg']} | {maxphi:.1e} | {r['nebit']}", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]; NR = int(sys.argv[2]); t0 = time.time()
    if mode == 'pair':
        A, B = sys.argv[3], sys.argv[4]
        nimg = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        nebit = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        cmd_pair(NR, A, B, nimg, nebit)
    elif mode == 'report':
        cmd_report(NR)
    print(f"=== DONE ({mode} {NR} {' '.join(sys.argv[3:5]) if len(sys.argv)>4 else ''}) "
          f"{time.time()-t0:.0f}s ===", flush=True)
