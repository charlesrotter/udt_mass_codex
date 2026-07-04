"""sweep_E2b_A3Z1.py -- E2b BRACKET 4 SWEEP (A3, Z=1) -- the FINAL bracket of the approved E2
contract (microphysics_E2_battle_plan.md, APPROVED AS WRITTEN). OBSERVE mode: the deliverable is
what the coupled system DOES, including "nothing converges". No merit gating; data-blind.

ADAPTED (not rewritten) from sweep_E2b_A3Z8.py per the E2b brief + the ACCUMULATED bracket-1/2/3
conditioning notes (microphysics_E2b_A1Z8_results.md sec.8 + ..._A1Z1_... sec.8 + ..._A3Z8_...
sec.8): full matrix without triage; 0.10*r_s boundary caps; ONE wide-guard run to measure THIS
bracket's dilation exponent (so far -1.31 A1Z8, -0.99 A1Z1, -1.00 A3Z8 -- this bracket
DISCRIMINATES the U_seal/wall-admissible correlate: prediction ~ -1.0 if it holds); H_cell read
on EVERY end state; EXTEND-FLOOR any parked state ~4000 iters; expect a WIDE parked basin if
small-coupling cells can nearly pay E_ang(seal)~2 (check amp-1.5 lock survival); underflow-
direction CPU/GPU matches are expected clean (bracket-3: 18/18); no guard-parked continuation
donors without flags.

THE BRACKET-3 REGRADE, APPLIED UP FRONT (the sharpest new instrument): compute BOTH the seed
shell height rho_seed(0.95*r_s) AND the exact station root rho = b^{-1/2} BEFORE any solve, and
read rho_p against BOTH on every wall end state. "Station lock" = SEED-HEIGHT PRESERVATION under
rigid translation (brackets 2-3 retro-checked), NOT solver-tuning to the station. THIS bracket
separates the two readings cleanly because r* = 0.94801*r_s < 0.95*r_s -- the wall seed sits
OUTSIDE the station for the first time, so
    preserved  => rho_p ~ 1.0037706012 (seed height), U(rho_p) ~ 1.9999977  (BELOW 2)
    tuned      => rho_p ~ 1.0036152090 (station),     U(rho_p) =  2.0000000 (exactly)
(the two differ at the 4th decimal; the lock reads to 5-7 digits -- fully discriminating).

BRACKET FACTS (banked E0 + E1): a* = b = 0.9928086030 = the E0 FRESH-CONVERGED value a_reshot
(A3 Z=1 was Stage-A budget-cut, a_banked=None; load_bracket falls back to a_reshot -- the brief's
banked number). r_s = 784.4148, rho_s = 1.352957, q = 1.0717828 (an OUTPUT), rho_c = 1.
U_seal = U(rho_s) = 1.68623 -- the HIGHEST of the four brackets (0.052, 1.409, 0.671, 1.686);
E1 xiN wall bound = 1.68623 (vs plateau 2.0). E1: the N=2 inversion IS present and this bracket
has THREE N=2 kap=1 wall-admissible cells (the most of any bracket) -> W7 added (bracket novelty,
per the E2b brief "E1 found 3 here").

Machinery: cell_solver_composite.py UNCHANGED (imported; same state as brackets 1-3, clean git
tree). Local addition = the same FREE-BOUNDARY TRUST-CAPPED LM (lm_qr_capped) as brackets 1-3 --
Category-A conditioning; the banked lm_qr is NOT edited.

PREMISE LEDGER OF THIS RUN (all CHOSE unless cited; carried into the results doc):
  P-E2b4-1 window cells (from microphysics_E1_probe_results.json necessary_map, A3 Z=1):
           W1 (N=1,xi=0.5,kap=0.1)   moderate-xi plateau (admfrac 1.0); identical to brackets
                                     1-3 -> continuation start + comparability (CHOSE, map-guided)
           W2 (N=1,xi=0.2,kap=0.1)   moderate-xi plateau neighbor (admfrac 1.0) (CHOSE, map-guided)
           W3 (N=1,xi=1.0,kap=0.1)   moderate-xi plateau neighbor (admfrac 1.0 in THIS bracket --
                                     bracket 3's flag does NOT apply here; no flag) (CHOSE, map-guided)
           W4 (N=1,xi=0.5,kap=1.0)   kappa-continuation neighbor (admfrac 1.0)  (CHOSE, map-guided)
           W5 (N=2,xi=0.05,kap=1.0)  WALL-ADMISSIBLE N=2 kap=1 (admfrac 0.110,
                                     outer_seal_admissible=True) -- inversion cell (CHOSE, map-guided)
           W6 (N=2,xi=0.1,kap=1.0)   2nd WALL-ADMISSIBLE N=2 kap=1 (admfrac 0.102,
                                     outer_seal_admissible=True)                 (CHOSE, map-guided)
           W7 (N=2,xi=0.2,kap=1.0)   3rd WALL-ADMISSIBLE N=2 kap=1 (admfrac 0.094,
                                     outer_seal_admissible=True) -- BRACKET NOVELTY: E1 found 3
                                     inversion cells here, the most of any bracket; all included
                                     per the brief                               (CHOSE, map-guided)
           C1 (N=1,xi=0.05,kap=0.01) fully-admissible small-coupling control (admfrac 1.0)
           C2 (N=2,xi=0.05,kap=0.01) 2nd fully-admissible control (admfrac 1.0 -- genuine,
                                     no substitute flag needed)                  (CHOSE, map-guided)
  P-E2b4-2 slices: plateau-target r_p0 = 100.0 (deep interior, r_p0/r_s ~ .127; same absolute
           value as brackets 1-3 for comparability); wall-target r_p0 = 0.95*r_s ~ 745.2 (near
           the U=2 station r* = .94801*r_s ~ 743.6 -- seed OUTSIDE the station, first bracket
           where that happens). Seeds only; r_p is a FREE unknown.  (CHOSE)
  P-E2b4-3 seed amplitudes amp in {0.3, 0.8, 1.5} (moderate -> far-from-rigid; banked N=1
           undersampling lesson; bulge theorem: solutions are non-perturbative in theta) (CHOSE)
  P-E2b4-4 grids: cell Nr=12, Nth=8; ambient Na=192, kmap=2.5 (brackets-1/2/3 choice, unchanged);
           confirm grids Nr=16/24, Nth=12 for candidates only.        (Category-A conditioning)
  P-E2b4-5 LM: maxit=150, per-solve wall 75 s, lam0=1e-6; free-boundary per-iteration step caps
           |d r_p|, |d r_sU| <= 0.10*r_s; domain-validity guard r_p in (1e-6*r_s, r_sU*(1-1e-9)),
           r_sU in (r_p, 5*r_s) (reject step, not a constraint row).  (Category-A trust handling)
  P-E2b4-6 convergence (pre-committed, plan instrument 1): max|F|_inf <= 1e-8 (rows are O(1) at
           seed; absolute ~ relative); everything below that = non-convergence DATA.
  P-E2b4-7 continuation: after each (cell x slice) primary seeds, one extra seed from the
           best-Phi end state of W1 (same slice), re-solved under the new cell's couplings.
           Poisoned-donor protocol unchanged (brackets 1-3): if the W1 donor is guard-parked the
           rows are flagged donor_guard_parked; provenance REPORTED per continuation row.
  P-E2b4-8 anchor: a* HELD at the banked bracket value (A3 Z=1 a* = a_reshot = 0.9928086030 --
           the E0 fresh-converged, blind-verified number; a_banked is None for this budget-cut
           bracket and load_bracket's documented fallback IS the banked discipline);
           Delta-phi FLOATS, reported.                                     (THEORY: E1 #5)
  P-E2b4-9 total compute budget ~90 min => internal hard budget 70 min for the matrix; coverage
           order = every (cell x slice) gets amp=0.8 FIRST, then amp depth, then continuation;
           un-run remainder reported THROUGHPUT-LIMITED. (Brackets 1-3 used ~10-15 min total;
           this bracket has 9 cells -> 70 phase-1 solves.)                       (anti-hang)
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

LAB = "A3 Z=1"
DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5
MAXIT, SOLVE_WALL = 150, 75.0
MATRIX_BUDGET = 70 * 60.0          # hard budget for the sweep matrix (s)
CONV_MAXF = 1e-8                   # pre-committed convergence floor (P-E2b4-6)
INTERESTING_PHI = 1e-6             # save fields below this (recompute-on-saved)
OUT_JSON = os.path.join(REPO, "microphysics_E2b_A3Z1_results.json")
LOG = os.path.join(REPO, "sweep_E2b_A3Z1.log")

br = C.load_bracket(LAB)
RS = br["r_s"]

CELLS = [  # (name, N, xi, kap, provenance-note)
    ("W1", 1, 0.5,  0.1,  "moderate-xi plateau (admfrac 1.0); brackets-1/2/3 W1 kept -> continuation start"),
    ("W2", 1, 0.2,  0.1,  "moderate-xi plateau neighbor (admfrac 1.0)"),
    ("W3", 1, 1.0,  0.1,  "moderate-xi plateau neighbor (admfrac 1.0 THIS bracket -- bracket-3 flag not applicable)"),
    ("W4", 1, 0.5,  1.0,  "kappa-continuation neighbor (admfrac 1.0)"),
    ("W5", 2, 0.05, 1.0,  "WALL-ADMISSIBLE N=2 kap=1 (admfrac .110, outer_seal_admissible) -- inversion cell, genuine"),
    ("W6", 2, 0.1,  1.0,  "2nd WALL-ADMISSIBLE N=2 kap=1 (admfrac .102, outer_seal_admissible)"),
    ("W7", 2, 0.2,  1.0,  "3rd WALL-ADMISSIBLE N=2 kap=1 (admfrac .094, outer_seal_admissible) -- BRACKET NOVELTY (E1: 3 inversion cells here, most of any bracket)"),
    ("C1", 1, 0.05, 0.01, "fully-admissible small-coupling control (admfrac 1.0)"),
    ("C2", 2, 0.05, 0.01, "2nd fully-admissible small-coupling control (admfrac 1.0; genuine, no flag)"),
]
SLICES = [("plateau", 100.0), ("wall", 0.95 * RS)]
AMPS = [0.8, 0.3, 1.5]     # coverage order: moderate first (P-E2b4-9), then depth

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


# ---------- station-lock diagnostics, computed UP FRONT (the bracket-3 regrade instrument) ----
A3_B = br["a_star"]                      # banked a* = a_reshot = 0.9928086030 (fresh-converged)
RHO_STATION = A3_B ** (-0.5)             # exact station root: b rho^4 - (1+b) rho^2 + 1 = 0
RHO_SEED_HEIGHT = float(np.interp(0.95 * RS, br["prof_r"], br["prof_rho"]))  # seed shell height
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
               rho_seed_height=float(RHO_SEED_HEIGHT),    # bracket-3 regrade: read against BOTH
               dev_from_seed_height=rho_p - float(RHO_SEED_HEIGHT),
               dev_from_station=rho_p - float(RHO_STATION),
               phi_hist_decades=[float(h) for h in info["hist"][:3]] + [float(info["hist"][-1])],
               top_residual_blocks=[(n_, l2, mx) for n_, l2, mx in top3],
               gates=json_safe(g))
    return rec, vf, w


# ------------------------------- MAIN SWEEP -------------------------------
def main():
    t_start = time.time()
    results = dict(stage="E2b bracket sweep", bracket=LAB, date="2026-07-04",
                   config=dict(Nr=Nr, Nth=Nth, Na=Na, kmap=KMAP, maxit=MAXIT,
                               solve_wall=SOLVE_WALL, conv_maxF=CONV_MAXF,
                               amps=AMPS, slices={s: r for s, r in SLICES},
                               cap_frac=0.10, device=DEV,
                               a_star_held=br["a_star"], rho_station=float(RHO_STATION),
                               rho_seed_height_at_095rs=float(RHO_SEED_HEIGHT),
                               U_at_seed_height=float(U_of(RHO_SEED_HEIGHT)),
                               U_seal=float(U_of(br["rho_s"])),
                               r_star_over_rs=0.9480063504430243,   # E1 (seed OUTSIDE station)
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

    log(f"UP-FRONT station-lock discriminators (bracket-3 regrade): "
        f"rho_station={RHO_STATION:.10f} (U=2 exactly), "
        f"rho_seed_height(0.95*r_s)={RHO_SEED_HEIGHT:.10f} (U={U_of(RHO_SEED_HEIGHT):.7f}); "
        f"separation {RHO_SEED_HEIGHT-RHO_STATION:+.3e}; seed OUTSIDE station (r*=0.948*r_s)")

    best_W1 = {}          # slice -> (Phi, w, guard_parked) for continuation seeds (P-E2b4-7)
    queue = []            # (priority, cell, slice, seedkind, amp)
    # coverage order (P-E2b4-9): pass1 = amp .8 every (cell x slice); pass2 = amps .3/1.5;
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
        else:  # continuation from best W1 end state, same slice (P-E2b4-7)
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
            rec["donor_guard_parked"] = bool(best_W1[sname][2])   # poisoned-donor flag
        log(f"  -> {rec['status']}  Phi {rec['Phi0']:.2e}->{rec['Phi_end']:.2e} "
            f"maxF={rec['maxF_end']:.2e} iters={rec['iters']} acc={rec['accepted']} "
            f"ncap={rec['ncap']} rp {rec['rp_seed']:.1f}->{rec['rp_end']:.2f} "
            f"rsU {rec['rsU_seed']:.1f}->{rec['rsU_end']:.2f} wall={rec['wall']}s "
            f"H_cell_max={rec['gates']['H_cell_max']:.2e} U(rho_p)={rec['U_rho_p']:.6f} "
            f"dev(seed)={rec['dev_from_seed_height']:+.2e} dev(stn)={rec['dev_from_station']:+.2e}")
        log(f"     top residual blocks: {rec['top_residual_blocks']}")
        results["runs"].append(rec)
        if cname == "W1" and seedkind == "bulge":
            if sname not in best_W1 or rec["Phi_end"] < best_W1[sname][0]:
                parked = rec["rsU_end"] > 4.5 * RS
                best_W1[sname] = (rec["Phi_end"], w, parked)
        if rec["Phi_end"] < INTERESTING_PHI or rec["status"] == "CONVERGED":
            pt = os.path.join(REPO, f"E2b_A3Z1_{tag.replace('/', '_')}.pt")
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
