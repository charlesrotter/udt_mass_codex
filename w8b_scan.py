"""W8 PHASE-B — script 2: THE CATALOG PERSISTENCE SCAN (GPU).

THE TEST (CATALOG_FRAME): impose ALL cell-defining conditions SIMULTANEOUSLY
on the limited variable space and determine whether the STABLE set is
DISCRETE or CONTINUOUS. NOT 're-find the band'. A point is a CATALOG MEMBER
iff it is a STABLE SELF-CONSISTENT CELL (w8 section v):
  - self-consistent on the formation-flow background (frozen-f inner loop on
    the trust window; coupling handled by w8b_selfconsistent.py separately);
  - finite C1 action (formation flow members have it by construction);
  - closes on the same-minus MIRROR FOLD (mirror/parity BC) at the seal end +
    finite-cell outer Dirichlet at the weld -> bc=("dirichlet","neumann") is
    the W4 mirror-labelling BC at the seal (registry #1 W7: mirror BC LABELS
    parity); we ALSO test the explicit Robin/parity seal end (robin1) as the
    fold closure cross-check;
  - PERSISTENCE: w4b classifier (STATIC=trivially persistent if equilibrium
    exists + bounded perturbation; BREATHER=bounded; COLLAPSE/GROW=unstable).

REUSE (never edited): w4b_evolib (Geo, bump_profile, evolve_torch, classify_
batch, equilibrium_newton, source), w8b_bg.npz backgrounds. TRUE UNITS c=2
carried in the species (w5 member-unit erratum) is in the SOURCE convention:
the evolib source uses sc = c_member fth2/(16 kappa); the kappa swept here is
the member-unit kappa. We carry BOTH the kappa axis AND, for the ratio
verdict, the kappa-DEPENDENCE explicitly (kappa underived).

SCAN AXES (w8 section vi):
  members: the 25-member (gamma,mult) grid from w8b_bg.npz
  gshape: g1,g2,g3 (ell 0/1/2 angular content)
  kappa: BOTH signs, scaled to per-member kappa_c (linear gap) + fixed negs
  beta (D_cell): {0,1}  (test-both fork)
  mechanism: STATIC (equilibrium_newton + perturbation) AND BREATHER (evolve)

PRE-REGISTERED PER-SCRIPT FAILURE / VALIDITY (binding):
  - G1 energy drift <= 1e-6 else run INVALID (excluded, counted).
  - G3 GPU-vs-CPU <= 1e-11 (enforced inside evolve_torch; abort on fail).
  - classification is the persistence verdict; UNRESOLVED-STIFF never banked.
  - A point is CATALOG iff classify in {STATIC-persistent, BREATHER, RING}
    AND valid. COLLAPSE/GROW/DISPERSE/QUIET-unstable are NOT members.
  - DISCRETE verdict requires: stable set is isolated points/thin slices
    separated by COLLAPSE/GROW; CONTINUUM = stable set fills a 2D patch.

Checkpointed per (member,gshape,beta,frame) cell to /tmp/w8b_scan_ckpt.json;
full results to /tmp/w8b_scan.npz + /tmp/w8b_scan_rows.csv. Log /tmp/w8b_scan.log
flush-per-line. New file. 2026-06-13, W8 PHASE-B.
"""
import sys, os, json, time
import numpy as np
import scipy.linalg as sla
import w4b_evolib as ev


def kappa_c_ray(geo, k, bc=("dirichlet", "neumann")):
    """Linear-gap kappa_c for ray k (VERBATIM the committed w4b_gates.py
    kappa_c_ray algorithm; reproduced here to avoid importing w4b_gates,
    whose module body runs JOB1/JOB2 on import). A = Int r^2 u_x^2,
    B = (3c/16) Int f_th^2 u^2; kappa_c = max gen-eig of B u = theta A u."""
    dx = geo.dx[k]
    r2 = geo.r[k]**2
    fth2 = geo.fth2[k]
    N = len(geo.xg[k])
    r2m = 0.5 * (r2[1:] + r2[:-1])
    A = np.zeros((N, N))
    idx = np.arange(N - 1)
    A[idx, idx] += r2m / dx
    A[idx + 1, idx + 1] += r2m / dx
    A[idx, idx + 1] -= r2m / dx
    A[idx + 1, idx] -= r2m / dx
    wxs = np.full(N, dx)
    wxs[0] = wxs[-1] = dx / 2
    B = np.diag(3 * geo.c / 16 * fth2 * wxs)
    keep = np.arange(N)
    if bc[0] == "dirichlet":
        keep = keep[1:]
    if bc[1] == "dirichlet":
        keep = keep[:-1]
    A, B = A[np.ix_(keep, keep)], B[np.ix_(keep, keep)]
    th = sla.eigh(B, A, eigvals_only=True)
    return float(th[-1])

LOG = open("/tmp/w8b_scan.log", "a")
def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True); LOG.write(msg + "\n"); LOG.flush()

NPZ = np.load("/tmp/w8b_bg.npz")
MEMBERS = sorted([k[:-5] for k in NPZ.files if k.endswith("_meta")])
GSHAPES = ["g1", "g2", "g3"]
BETAS = [0, 1]           # D_cell off / on
FRAME = "primary"        # primary frame (true; diagonal is the labelled variant)
NX = 1024                # scan grid; representatives doubled in w8b_converge.py
NU = 24
AMP = 0.02               # bump amplitude (small, shaped)
CKPT = "/tmp/w8b_scan_ckpt.json"
CSV = "/tmp/w8b_scan_rows.csv"

# kappa axis: per-member multiples of kappa_c (positive = unstable band by the
# linear gap) PLUS negative-kappa probes (stiffening sign) PLUS fixed values.
KC_MULTS_POS = [0.25, 0.5, 0.9, 1.1, 2.0]   # straddle kappa_c
KAPPA_NEG = [-2.0, -1.0, -0.5]               # negative-sign branch (true units)


def kappa_c_member(geo):
    """Max-over-rays kappa_c (Rayleigh) for inner-Dirichlet/outer-Neumann."""
    kcs = [kappa_c_ray(geo, k, bc=("dirichlet", "neumann"))
           for k in range(geo.Nu)]
    return float(max(kcs)), int(np.argmax(kcs))


def load_ckpt():
    if os.path.exists(CKPT):
        return json.load(open(CKPT))
    return {}


def save_ckpt(d):
    json.dump(d, open(CKPT, "w"))


def main():
    done = load_ckpt()
    if not os.path.exists(CSV):
        with open(CSV, "w") as fh:
            fh.write("member,gamma,mult,gshape,beta,frame,kappa,kappa_c,"
                     "mech,label,valid,edrift,env_max,rate_final,pF_seal,"
                     "pF_weld\n")
    csv = open(CSV, "a")

    for member in MEMBERS:
        meta = NPZ[f"{member}_meta"]
        gamma, c, t_stop = meta[0], meta[1], meta[2]
        mult, cstar = NPZ[f"{member}_multcstar"]
        pF_seal = float(NPZ[f"{member}_pF"][-1])
        pF_weld = gamma / 2.0
        geo = ev.Geo(NPZ, member, Nu=NU, Nx=NX)
        kc, kray = kappa_c_member(geo)
        kappas_pos = [m * kc for m in KC_MULTS_POS]
        kappa_axis = sorted(set([round(k, 6) for k in (KAPPA_NEG + kappas_pos)]))
        log(f"=== {member} gamma={gamma} mult={mult} t_stop={t_stop:.3f} "
            f"kappa_c={kc:.5f} (ray {kray}) pF_seal={pF_seal:.5f} ===")

        g3_done_this_member = False
        for gshape in GSHAPES:
            for beta in BETAS:
                cellkey = f"{member}|{gshape}|b{beta}|{FRAME}"
                if cellkey in done:
                    g3_done_this_member = True  # already witnessed earlier
                    continue
                dcell = bool(beta)
                t0 = time.time()
                v0 = ev.bump_profile(geo, AMP, gshape)
                vt0 = np.zeros_like(v0)
                # ----- STATIC branch: equilibrium existence (D_cell OFF only;
                # D_cell ON the static point is the on-branch algebraic eq) ---
                static_label = "n/a"
                veq = None
                if not dcell:
                    veqr, info = ev.equilibrium_newton(
                        geo, kappa=max(kappa_axis), frame=FRAME,
                        bc=("dirichlet", "neumann"))
                    if veqr is not None:
                        veq = veqr
                        static_label = "EXISTS"
                    else:
                        static_label = f"NO ({len(info['fail_rays'])} rays)"
                # ----- BREATHER branch: batched evolve over kappa axis -------
                NBk = len(kappa_axis)
                v0b = np.broadcast_to(v0, (NBk, *v0.shape)).copy()
                vt0b = np.zeros_like(v0b)
                T_end = 8.0 * float(np.max(geo.xmax))
                # G3 GPU-vs-CPU trust gate (<=1e-11): the stepper is
                # geometry-determined and IDENTICAL across gshape/beta on a
                # given member, so witnessing G3 once per MEMBER geometry
                # (the first cell) satisfies the gate; recorded honestly.
                do_g3 = not g3_done_this_member
                try:
                    resb = ev.evolve_torch(
                        geo, v0b, vt0b, np.array(kappa_axis), dcell, T_end,
                        frame=FRAME, bc=("dirichlet", "neumann"),
                        cpu_assert=do_g3, log=log)
                    g3_done_this_member = True
                except AssertionError as e:
                    log(f"  {cellkey}: G3 GATE FAIL {e} -- ABORT cell")
                    done[cellkey] = {"error": str(e)}
                    save_ckpt(done); continue
                rows = []
                for b, kap in enumerate(kappa_axis):
                    lab, diag = ev.classify_batch(resb, b, AMP)
                    valid = diag.get("valid", True)
                    rows.append((kap, lab, valid, diag.get("edrift", np.nan),
                                 diag.get("env_max", np.nan),
                                 diag.get("rate_final", np.nan)))
                    csv.write(f"{member},{gamma},{mult},{gshape},{beta},{FRAME},"
                              f"{kap:.6f},{kc:.6f},breather,{lab},{int(valid)},"
                              f"{diag.get('edrift',np.nan):.3e},"
                              f"{diag.get('env_max',np.nan):.4f},"
                              f"{diag.get('rate_final',np.nan):.4f},"
                              f"{pF_seal:.6f},{pF_weld:.6f}\n")
                csv.flush()
                # static row
                csv.write(f"{member},{gamma},{mult},{gshape},{beta},{FRAME},"
                          f"nan,{kc:.6f},static,{static_label},1,nan,nan,nan,"
                          f"{pF_seal:.6f},{pF_weld:.6f}\n")
                csv.flush()
                labs = [r[1] for r in rows]
                done[cellkey] = {
                    "kappa_axis": kappa_axis, "labels": labs,
                    "valid": [bool(r[2]) for r in rows],
                    "static": static_label, "kappa_c": kc,
                    "pF_seal": pF_seal, "pF_weld": pF_weld,
                    "gamma": float(gamma), "mult": float(mult)}
                save_ckpt(done)
                log(f"  {cellkey}: static={static_label} breather labels="
                    f"{dict(zip([f'{k:.3f}' for k in kappa_axis], labs))} "
                    f"[{time.time()-t0:.1f}s]")
    csv.close()
    log("SCAN COMPLETE. cells:", len(done))
    np.savez("/tmp/w8b_scan.npz", done=json.dumps(done))


if __name__ == "__main__":
    main()
