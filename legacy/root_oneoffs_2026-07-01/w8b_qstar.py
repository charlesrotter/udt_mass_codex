"""W8 PHASE-B — script 3: THE q*-COUPLED RUN (the angular-sector effect).

THE QUESTION (w8 vi step 3 / CATALOG_FRAME / registry #30): does the
q*-coupling — the angular sector's back-reaction through the f-row w_thth
DOOR and the mirror-FOLD closure — DISCRETIZE the catalog where the q=0
(bands-not-lines, registry #28) class did NOT?

W6 banked (w6_results.md): the angular discreteness, if any, lives in HOW
THE CELL CLOSES ON ITS MIRROR (the fold/quotient seal BC), not in a single
cell's interior modes. The q*-branch signal speeds diverge as 1/D at the
fold; the time-row completion is regular Lorentzian. So the q*-coupling's
operational effect on the catalog enters through the SEAL CLOSURE BC.

EXECUTABLE TEST (mechanism-open, no new mechanism imported): re-run the
persistence test on the SAME base cell with TWO seal closures:
  (A) q=0 control: inner Dirichlet seal (the W4/registry-#28 bands BC);
  (B) q*-coupled / mirror-fold: inner ROBIN parity seal (robin1: v_x = v
      at the seal end), the same-minus mirror/parity BC that the fold
      imposes (w8 ii.3); this carries the f-row w_thth door's boundary
      pairing (the only place cross-sector angular stiffness enters per
      W6). Both reuse w4b_evolib evolve_torch verbatim.
COMPARE: do the persistence bands / the set of stable kappa CHANGE between
(A) and (B)? If (B) produces ISOLATED stable kappa (lines) where (A) gave
open bands -> the angular effect discretizes. If (B) gives the same open
bands -> it does not (q*-coupling is not the discretizer at this order).

PRE-REGISTERED FAILURE: if the robin1 seal merely shifts band EDGES but
keeps OPEN stable intervals, the verdict is NOT-DISCRETIZED (first-class).
Discretization requires the stable set to become measure-zero in kappa.

Members tested: the lepton base-cell candidate (G1.0_M1.3) + 4 spread
members. Log /tmp/w8b_qstar.log. New file. 2026-06-13, W8 PHASE-B.
"""
import sys
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import numpy as np
import w4b_evolib as ev
import w8b_scan as ws

LOG = open("/tmp/w8b_qstar.log", "w")
def log(*a):
    m = " ".join(str(x) for x in a)
    print(m, flush=True); LOG.write(m + "\n"); LOG.flush()

NPZ = np.load("/tmp/w8b_bg.npz")
MEMBERS = ["G1.0_M1.3", "G0.5_M2.0", "G1.0_M2.0", "G1.5_M1.3", "G2.0_M1.3"]
NX, NU, AMP = 1024, 24, 0.02


def kappa_axis_for(geo):
    kc = max(ws.kappa_c_ray(geo, k) for k in range(geo.Nu))
    # fine straddle of the band: many points to resolve open-vs-isolated
    pos = sorted(set([round(m * kc, 6) for m in
                      [0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 1.0,
                       1.1, 1.25, 1.5, 2.0, 3.0]]))
    neg = [-2.0, -1.0, -0.5, -0.1]
    return np.array(sorted(set(neg + pos))), kc


def run_bc(geo, kappa_axis, bc, dcell):
    v0 = ev.bump_profile(geo, AMP, "g1")
    NB = len(kappa_axis)
    v0b = np.broadcast_to(v0, (NB, *v0.shape)).copy()
    vt0b = np.zeros_like(v0b)
    T_end = 6.0 * float(np.max(geo.xmax))
    resb = ev.evolve_torch(geo, v0b, vt0b, kappa_axis, dcell, T_end,
                           frame="primary", bc=bc, cpu_assert=True, log=log)
    return [ev.classify_batch(resb, b, AMP)[0] for b in range(NB)]


def stable(lab):
    return lab in ("RING", "BREATHER")


def main():
    for member in MEMBERS:
        geo = ev.Geo(NPZ, member, Nu=NU, Nx=NX)
        kappa_axis, kc = kappa_axis_for(geo)
        log(f"=== {member} kappa_c={kc:.5f}  axis={list(np.round(kappa_axis,4))}")
        for dcell in (False, True):
            labA = run_bc(geo, kappa_axis, ("dirichlet", "neumann"), dcell)
            labB = run_bc(geo, kappa_axis, ("robin1", "neumann"), dcell)
            stA = [k for k, l in zip(kappa_axis, labA) if stable(l)]
            stB = [k for k, l in zip(kappa_axis, labB) if stable(l)]
            log(f"  beta={int(dcell)}  q=0 (Dirichlet seal): "
                f"{dict(zip([f'{k:.4f}' for k in kappa_axis], labA))}")
            log(f"  beta={int(dcell)}  q*-fold (Robin parity seal): "
                f"{dict(zip([f'{k:.4f}' for k in kappa_axis], labB))}")
            log(f"  beta={int(dcell)}  stable-kappa COUNT: q0={len(stA)} "
                f"qstar={len(stB)}  (axis n={len(kappa_axis)})")
            # discretization check: did Robin collapse open bands to isolated?
            def open_band(stab_list):
                # an open band = >=2 consecutive stable axis points
                idx = [i for i, k in enumerate(kappa_axis) if k in stab_list]
                runs = 0
                for a, b in zip(idx, idx[1:]):
                    if b == a + 1:
                        runs += 1
                return runs
            log(f"  beta={int(dcell)}  open-band adjacency: q0={open_band(stA)} "
                f"qstar={open_band(stB)}  "
                f"=> {'DISCRETIZED' if open_band(stB)==0 and open_band(stA)>0 else 'NOT-discretized'}")
    log("QSTAR DONE")


if __name__ == "__main__":
    main()
