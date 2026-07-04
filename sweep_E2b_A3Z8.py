"""sweep_E2b_A3Z8.py -- E2b BRACKET 3 SWEEP (A3, Z=8) of the approved E2 contract
(microphysics_E2_battle_plan.md, APPROVED AS WRITTEN). OBSERVE mode: the deliverable is what the
coupled system DOES, including "nothing converges". No merit gating; data-blind (no masses).

ADAPTED (not rewritten) from sweep_E2b_A1Z1.py per the E2b brief + the accumulated bracket-1/2
conditioning notes (microphysics_E2b_A1Z8_results.md sec. 8 + microphysics_E2b_A1Z1_results.md
sec. 8): full matrix without triage; 0.10*r_s boundary caps; ONE wide-guard run to measure THIS
bracket's dilation exponent (so far -1.31 A1Z8, -0.99 A1Z1); H_cell read on EVERY end state
(Phi alone misleads -- falling Phi with H_cell O(1) = false floor); EXTEND-FLOOR any parked
state ~4000 iters before calling it finite-size; read rho_p and U(rho_p) on wall end states --
the STATION-LOCK cross-family question (A1 Z=1 locked at U(rho_p)=2.000003 exactly; is it
FAMILY-universal?); don't read CPU/GPU mismatch on e^{2phi}-overflow end states as machinery
bugs; don't donate continuation seeds from guard-parked states (flag if used).

FIRST A3-FAMILY BRACKET: the ambient slice family switches from A1 (U = 2 rho^m e^{-a(rho^2-1)})
to A3 (U = 2 rho^2 (1+b)/(1+b rho^4)) via the same cascade_stageA_lib ports the composite solver
already exposes (make_slice dispatches on bracket['family']; a* = banked b). The E1 audit found
the N=2 inversion present in this bracket (present 3 of 4, absent only A1 Z8): the N=2 kap~1
wall-admissible cells here are GENUINE articles, as in bracket 2. A3 U=2 stations: rho=1 (core
fold) and rho = b^{-1/2} = 1.012095 (the wall station; E1 rho_at_rstar = 1.012092).

Machinery: cell_solver_composite.py UNCHANGED (imported; same state as brackets 1-2, clean git
tree). The only local addition is the same FREE-BOUNDARY TRUST-CAPPED LM variant (lm_qr_capped)
as brackets 1-2 -- Category-A conditioning; the banked lm_qr is NOT edited.

PREMISE LEDGER OF THIS RUN (all CHOSE unless cited; carried into the results doc):
  P-E2b3-1 window cells (from microphysics_E1_probe_results.json necessary_map, A3 Z=8):
           W1 (N=1,xi=0.5,kap=0.1)   moderate-xi plateau cell (admfrac 1.0 here); kept identical
                                     to brackets 1-2 -> continuation start + cross-bracket
                                     comparability                               (CHOSE, map-guided)
           W2 (N=1,xi=0.2,kap=0.1)   moderate-xi plateau neighbor (admfrac 1.0) (CHOSE, map-guided)
           W3 (N=1,xi=1.0,kap=0.1)   moderate-xi plateau neighbor -- NOTE: in THIS bracket
                                     admfrac 0.905, plateau_admissible=True but outer_seal_
                                     admissible=False (brackets 1-2 had admfrac 1.0 here);
                                     kept for cross-bracket comparability, FLAGGED (CHOSE, map-guided)
           W4 (N=1,xi=0.5,kap=1.0)   kappa-continuation neighbor (admfrac 1.0)  (CHOSE, map-guided)
           W5 (N=2,xi=0.05,kap=1.0)  WALL-ADMISSIBLE N=2 kap=1 cell (admfrac 0.122,
                                     outer_seal_admissible=True) -- E1-inversion bracket,
                                     genuine article                             (CHOSE, map-guided)
           W6 (N=2,xi=0.1,kap=1.0)   2nd WALL-ADMISSIBLE N=2 kap=1 cell (admfrac 0.114,
                                     outer_seal_admissible=True)                 (CHOSE, map-guided)
           C1 (N=1,xi=0.05,kap=0.01) fully-admissible small-coupling control (admfrac 1.0)
           C2 (N=2,xi=0.05,kap=0.01) 2nd fully-admissible control (admfrac 1.0 -- genuine, no
                                     substitute flag needed)                     (CHOSE, map-guided)
  P-E2b3-2 slices: plateau-target r_p0 = 100.0 (deep interior, r_p0/r_s ~ .139; same absolute
           value as brackets 1-2 for comparability); wall-target r_p0 = 0.95*r_s ~ 684.9 (near
           the U=2 station r* = .95228 r_s ~ 686.6). Seeds only; r_p is a FREE unknown. (CHOSE)
  P-E2b3-3 seed amplitudes amp in {0.3, 0.8, 1.5} (moderate -> far-from-rigid; banked N=1
           undersampling lesson; bulge theorem: solutions are non-perturbative in theta) (CHOSE)
  P-E2b3-4 grids: cell Nr=12, Nth=8; ambient Na=192, kmap=2.5 (brackets-1/2 choice, unchanged);
           confirm grids Nr=16/24, Nth=12 for candidates only.        (Category-A conditioning)
  P-E2b3-5 LM: maxit=150, per-solve wall 75 s, lam0=1e-6; free-boundary per-iteration step caps
           |d r_p|, |d r_sU| <= 0.10*r_s; domain-validity guard r_p in (1e-6*r_s, r_sU*(1-1e-9)),
           r_sU in (r_p, 5*r_s) (reject step, not a constraint row).  (Category-A trust handling)
  P-E2b3-6 convergence (pre-committed, plan instrument 1): max|F|_inf <= 1e-8 (rows are O(1) at
           seed; absolute ~ relative); everything below that = non-convergence DATA.
  P-E2b3-7 continuation: after each (cell x slice) primary seeds, one extra seed from the
           best-Phi end state of W1 (same slice), re-solved under the new cell's couplings
           ("continuation in (xi,kap) from the best-conditioned window cell", plan sec. Method).
           Per the bracket-2 conditioning note: if the W1 donor is guard-parked, the opposite-
           slice continuation rows are expected to 1-iteration-stall (poisoned donor) -- observed
           both brackets; donor provenance REPORTED per continuation row.
  P-E2b3-8 anchor: a* HELD at the banked bracket value (A3 Z=8 a_banked = 0.9762462704, the T3
           slice parameter b); Delta-phi FLOATS, reported as dphi_float / dphi_anchor_gap.
                                                                          (THEORY: E1 #5)
  P-E2b3-9 total compute budget ~90 min => internal hard budget 70 min for the matrix; coverage
           order = every (cell x slice) gets amp=0.8 FIRST, then amp depth, then continuation;
           un-run remainder reported THROUGHPUT-LIMITED. (Brackets 1-2 used ~10-12 min total;
           bracket-1 conditioning note: run the FULL matrix without triage.)       (anti-hang)
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys
import json
import math
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

REPO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO)
import cell_solver_composite as C
import cell_solver_f2d as F2D

LAB = "A3 Z=8"
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5
MAXIT, SOLVE_WALL = 150, 75.0
MATRIX_BUDGET = 70 * 60.0          # hard budget for the sweep matrix (s)
CONV_MAXF = 1e-8                   # pre-committed convergence floor (P-E2b3-6)
INTERESTING_PHI = 1e-6             # save fields below this (recompute-on-saved)
OUT_JSON = os.path.join(REPO, "microphysics_E2b_A3Z8_results.json")
LOG = os.path.join(REPO, "sweep_E2b_A3Z8.log")

br = C.load_bracket(LAB)
RS = br["r_s"]

CELLS = [  # (name, N, xi, kap, provenance-note)
    ("W1", 1, 0.5,  0.1,  "moderate-xi plateau (admfrac 1.0); brackets-1/2 W1 kept -> continuation start"),
    ("W2", 1, 0.2,  0.1,  "moderate-xi plateau neighbor (admfrac 1.0)"),
    ("W3", 1, 1.0,  0.1,  "moderate-xi plateau neighbor (admfrac 0.905 THIS bracket, outer_seal_admissible=False -- FLAGGED, kept for comparability)"),
    ("W4", 1, 0.5,  1.0,  "kappa-continuation neighbor (admfrac 1.0)"),
    ("W5", 2, 0.05, 1.0,  "WALL-ADMISSIBLE N=2 kap=1 (admfrac .122, outer_seal_admissible) -- E1-inversion bracket, genuine"),
    ("W6", 2, 0.1,  1.0,  "2nd WALL-ADMISSIBLE N=2 kap=1 (admfrac .114, outer_seal_admissible)"),
    ("C1", 1, 0.05, 0.01, "fully-admissible small-coupling control (admfrac 1.0)"),
    ("C2", 2, 0.05, 0.01, "2nd fully-admissible small-coupling control (admfrac 1.0; genuine, no flag)"),
]
SLICES = [("plateau", 100.0), ("wall", 0.95 * RS)]
AMPS = [0.8, 0.3, 1.5]     # coverage order: moderate first (P-E2b3-9), then depth

logfh = open(LOG, "a")
def log(msg):
    print(msg, flush=True)
    logfh.write(msg + "\n"); logfh.flush()


# ---------- row blocks (residual-mass reporting; layout = residual_comp row order) ----------
def make_row_blocks(Nr, Nth, Na):
    return [("cell phi-ODE", Nr - 2), ("cell rho-ODE", Nr - 2), ("f-PDE", (Nr - 2) * Nth),
            ("core phi'", 1), ("core rho'", 1), ("core f_r", Nth), ("C1c f_r(seal)", Nth),
            ("amb phi-ODE", Na - 2), ("amb rho-ODE", Na - 2),
            ("seal [phi]", 1), ("seal [rho]", 1), ("C1a", 1), ("C1b", 1), ("C2", 1),
            ("fold phi", 1), ("fold rho'", 1), ("fold H_amb", 1)]


def block_norms(F, blocks):
    out = []; i = 0
    for name, k in blocks:
        seg = F[i:i + k]; i += k
        out.append((name, float(np.sqrt((seg * seg).sum())), float(np.abs(seg).max())))
    return out


# ---------- trust-capped LM (Category-A; banked lm_qr + boundary caps + validity guard) -------
def lm_qr_capped(resfn_t, w0, r_s, maxit=150, lam0=1e-6, tol=1e-20, time_budget=75.0,
                 device="cpu", cap_frac=0.10, verbose=False):
    """Identical algorithm to cell_solver_composite.lm_qr (float64 residual path) PLUS:
    (a) per-iteration cap |dx| on the two free-boundary components <= cap_frac*r_s (whole-step
        rescale, direction preserved); (b) domain-validity guard (reject step -> lam up) if
        r_p or r_sU leaves (1e-6*r_s, ...) ordering/positivity bounds. Both Category-A."""
    from torch.func import jacrev
    t0 = time.time()
    w = np.asarray(w0, dtype=np.longdouble).copy()
    n = w.size
    cap = cap_frac * r_s

    def valid(ww):
        rp, rsU = float(ww[-2]), float(ww[-1])
        return (rp > 1e-6 * r_s) and (rsU > rp * (1 + 1e-9)) and (rsU < 5 * r_s)

    def evalF(ww):
        if not valid(ww):
            return None
        F = resfn_t(torch.as_tensor(ww.astype(float), device=device)
                    ).detach().cpu().numpy().astype(np.longdouble)
        if not np.isfinite(F.astype(float)).all():
            return None
        return F

    F = evalF(w)
    assert F is not None, "seed invalid"
    Phi = float((F * F).sum())
    lam = lam0; hist = [Phi]; nacc = 0; ncap = 0
    rp_traj = [float(w[-2])]; rsU_traj = [float(w[-1])]
    stall = False
    for it in range(maxit):
        if Phi < tol or (time.time() - t0) > time_budget:
            break
        wt = torch.as_tensor(w.astype(float), device=device)
        J = jacrev(resfn_t)(wt).detach()
        colscale = J.abs().amax(dim=0).clamp(min=1e-30)
        Js = J / colscale
        Ft = torch.as_tensor(F.astype(float), device=device)
        eye = torch.eye(n, dtype=torch.float64, device=device)
        zer = torch.zeros(n, dtype=torch.float64, device=device)
        accepted = False
        for _try in range(40):
            Aug = torch.cat([Js, math.sqrt(lam) * eye], 0)
            rhs = torch.cat([-Ft, zer])
            dxs = torch.linalg.lstsq(Aug, rhs.unsqueeze(1)).solution.squeeze(1)
            dx = (dxs / colscale).cpu().numpy().astype(np.longdouble)
            bmax = max(abs(float(dx[-2])), abs(float(dx[-1])))
            if bmax > cap:                       # free-boundary trust cap (whole-step rescale)
                dx = dx * np.longdouble(cap / bmax); ncap += 1
            wn = w + dx
            Fn = evalF(wn)
            Pn = float((Fn * Fn).sum()) if Fn is not None else float("inf")
            if math.isfinite(Pn) and Pn < Phi:
                w = wn; F = Fn; Phi = Pn
                lam = max(lam / 3.0, 1e-18); accepted = True; nacc += 1
                break
            lam = min(lam * 2.0, 1e10)
        hist.append(Phi)
        rp_traj.append(float(w[-2])); rsU_traj.append(float(w[-1]))
        if verbose:
            log(f"    it={it:3d} Phi={Phi:.4e} lam={lam:.1e} rp={float(w[-2]):.2f} "
                f"rsU={float(w[-1]):.2f} {'acc' if accepted else 'STALL'}")
        if not accepted:
            stall = True
            break
    return w, dict(Phi=Phi, iters=len(hist) - 1, accepted=nacc, ncap=ncap, stalled=stall,
                   hist=[float(h) for h in hist], rp_traj=rp_traj, rsU_traj=rsU_traj,
                   wall=time.time() - t0)


def json_safe(x):
    if isinstance(x, dict):
        return {k: json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [json_safe(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, float) and not math.isfinite(x):
        return str(x)
    return x


# ---------- A3 station-lock diagnostic (bracket-2 conditioning note; one line of arithmetic) ---
A3_B = br["a_star"]                      # banked b = 0.9762462704
RHO_STATION = A3_B ** (-0.5)             # nontrivial U=2 root: b rho^4 - (1+b) rho^2 + 1 = 0
U_of, _Up_of = C.make_slice(br["family"], A3_B, np)


def run_one(ctx, prm, v0, tag):
    """One bounded solve + full observation record (converged OR not -- non-convergence is DATA)."""
    resfn = lambda vv: C.residual_comp(vv, ctx, prm, br)
    F0 = resfn(v0)
    Phi0 = float((F0 * F0).sum())
    w, info = lm_qr_capped(resfn, v0.detach().cpu().numpy().astype(np.longdouble), RS,
                           maxit=MAXIT, time_budget=SOLVE_WALL, device=DEV)
    vf = torch.as_tensor(w.astype(float), device=DEV)
    Ff = resfn(vf)
    maxF = float(Ff.abs().max())
    blocks = block_norms(Ff.detach().cpu().numpy(), make_row_blocks(ctx["Nr"], ctx["Nth"], ctx["Na"]))
    top3 = sorted(blocks, key=lambda b: -b[2])[:3]
    phi_c, rho_c, uf, phi_a, rho_a, rp, rsU = C.unpack_comp(vf, ctx)
    g = C.gates_comp(vf, ctx, prm, br)
    rho_p = float(rho_a[0])                              # seal-side ambient rho
    status = ("CONVERGED" if maxF <= CONV_MAXF else
              ("stalled" if info["stalled"] else
               ("iter/wall-capped" if info["iters"] >= MAXIT or info["wall"] >= SOLVE_WALL
                else "flatlined")))
    rec = dict(tag=tag, status=status, Phi0=Phi0, Phi_end=info["Phi"], maxF_end=maxF,
               iters=info["iters"], accepted=info["accepted"], ncap=info["ncap"],
               stalled=info["stalled"], wall=round(info["wall"], 1),
               rp_seed=float(v0[-2]), rp_end=float(rp), rsU_seed=float(v0[-1]),
               rsU_end=float(rsU),
               rp_traj_every10=[round(x, 3) for x in info["rp_traj"][::10]] + [round(info["rp_traj"][-1], 3)],
               rsU_traj_every10=[round(x, 3) for x in info["rsU_traj"][::10]] + [round(info["rsU_traj"][-1], 3)],
               phi_core=float(phi_c[0]), rho_core=float(rho_c[0]),
               max_u=float(uf.abs().max()),
               rho_p=rho_p, U_rho_p=float(U_of(rho_p)),   # station-lock diagnostic (every end state)
               rho_station=float(RHO_STATION),
               phi_hist_decades=[float(h) for h in info["hist"][:3]] + [float(info["hist"][-1])],
               top_residual_blocks=[(n_, l2, mx) for n_, l2, mx in top3],
               gates=json_safe(g))
    return rec, vf, w


# ------------------------------- MAIN SWEEP -------------------------------
def main():
    t_start = time.time()
    results = dict(stage="E2b bracket sweep", bracket=LAB, date="2026-07-03",
                   config=dict(Nr=Nr, Nth=Nth, Na=Na, kmap=KMAP, maxit=MAXIT,
                               solve_wall=SOLVE_WALL, conv_maxF=CONV_MAXF,
                               amps=AMPS, slices={s: r for s, r in SLICES},
                               cap_frac=0.10, device=DEV,
                               a_star_held=br["a_star"], rho_station=float(RHO_STATION),
                               cells={c[0]: dict(N=c[1], xi=c[2], kap=c[3], note=c[4])
                                      for c in CELLS}),
                   runs=[], candidates=[], throughput_limited=[], notes=[])

    def save():
        with open(OUT_JSON, "w") as fh:
            json.dump(json_safe(results), fh, indent=1)

    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)

    # GPU-vs-CPU spot check at the first seed (banked GPU discipline)
    prm0 = (br["Z"], CELLS[0][2], CELLS[0][3], CELLS[0][1])
    v0 = C.seed_comp(ctx, br, rp0=SLICES[0][1], amp=AMPS[0], device=DEV)
    if DEV == "cuda":
        ctx_c = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device="cpu")
        Fg = C.residual_comp(v0, ctx, prm0, br).cpu()
        Fc = C.residual_comp(v0.cpu(), ctx_c, prm0, br)
        spot = float((Fg - Fc).abs().max()) / max(1.0, float(Fc.abs().max()))
        log(f"GPU-vs-CPU residual spot-check (seed): rel maxdiff = {spot:.2e}")
        results["notes"].append(f"GPU-vs-CPU seed residual spot-check rel maxdiff {spot:.2e}")

    best_W1 = {}          # slice -> (Phi, w, guard_parked) for continuation seeds (P-E2b3-7)
    queue = []            # (priority, cell, slice, seedkind, amp)
    # coverage order (P-E2b3-9): pass1 = amp .8 every (cell x slice); pass2 = amps .3/1.5;
    # pass3 = continuation seeds for cells != W1
    for a_i, amp in enumerate(AMPS):
        for cname, N, xi, kap, note in CELLS:
            for sname, rp0 in SLICES:
                queue.append((a_i, cname, N, xi, kap, sname, rp0, "bulge", amp))
    for cname, N, xi, kap, note in CELLS[1:]:
        for sname, rp0 in SLICES:
            queue.append((3, cname, N, xi, kap, sname, rp0, "cont-W1", None))

    for item in queue:
        prio, cname, N, xi, kap, sname, rp0, seedkind, amp = item
        tag = f"{cname}/{sname}/{seedkind}" + (f"-amp{amp}" if amp is not None else "")
        elapsed = time.time() - t_start
        if elapsed > MATRIX_BUDGET:
            results["throughput_limited"].append(tag)
            continue
        prm = (br["Z"], xi, kap, N)
        if seedkind == "bulge":
            v0 = C.seed_comp(ctx, br, rp0=rp0, amp=amp, device=DEV)
        else:  # continuation from best W1 end state, same slice (P-E2b3-7)
            if sname not in best_W1:
                results["notes"].append(f"{tag}: no W1 end state available, skipped")
                continue
            v0 = torch.as_tensor(best_W1[sname][1].astype(float), device=DEV)
        log(f"[{elapsed/60:5.1f}m] SOLVE {tag}  (N={N} xi={xi} kap={kap} rp0={float(v0[-2]):.1f})")
        try:
            rec, vf, w = run_one(ctx, prm, v0, tag)
        except Exception as e:
            log(f"  EXCEPTION: {e}")
            results["runs"].append(dict(tag=tag, status="EXCEPTION", error=str(e)))
            save(); continue
        if seedkind == "cont-W1":
            rec["donor_guard_parked"] = bool(best_W1[sname][2])   # bracket-2 poisoned-donor flag
        log(f"  -> {rec['status']}  Phi {rec['Phi0']:.2e}->{rec['Phi_end']:.2e} "
            f"maxF={rec['maxF_end']:.2e} iters={rec['iters']} acc={rec['accepted']} "
            f"ncap={rec['ncap']} rp {rec['rp_seed']:.1f}->{rec['rp_end']:.2f} "
            f"rsU {rec['rsU_seed']:.1f}->{rec['rsU_end']:.2f} wall={rec['wall']}s "
            f"H_cell_max={rec['gates']['H_cell_max']:.2e} U(rho_p)={rec['U_rho_p']:.6f}")
        log(f"     top residual blocks: {rec['top_residual_blocks']}")
        results["runs"].append(rec)
        if cname == "W1" and seedkind == "bulge":
            if sname not in best_W1 or rec["Phi_end"] < best_W1[sname][0]:
                parked = rec["rsU_end"] > 4.5 * RS
                best_W1[sname] = (rec["Phi_end"], w, parked)
        if rec["Phi_end"] < INTERESTING_PHI or rec["status"] == "CONVERGED":
            pt = os.path.join(REPO, f"E2b_A3Z8_{tag.replace('/', '_')}.pt")
            torch.save(dict(w=torch.as_tensor(w.astype(float)), prm=prm, Nr=Nr, Nth=Nth,
                            Na=Na, kmap=KMAP, tag=tag), pt)
            rec["saved_pt"] = os.path.basename(pt)
            log(f"     saved fields -> {pt}")
        if rec["status"] == "CONVERGED":
            results["candidates"].append(tag)
        save()

    log(f"\nmatrix done at {(time.time()-t_start)/60:.1f} min; "
        f"candidates={results['candidates']}; "
        f"throughput-limited remainder n={len(results['throughput_limited'])}")
    save()
    return results


if __name__ == "__main__":
    main()
