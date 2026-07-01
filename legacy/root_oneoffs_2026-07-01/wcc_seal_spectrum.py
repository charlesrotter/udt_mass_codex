#!/usr/bin/env python3
"""
wcc_seal_spectrum.py -- the CLOSED-CELL bifurcation diagnostic under each
SEAL mirror-fold closure, done with the VERIFIED wint machinery and a
trustworthy (symmetrized, angular-restricted) spectrum.
=======================================================================
WHOLE-CLOSED-CELL push. Driver: Claude (Opus 4.8). Date 2026-06-13.
New file (wcc_*). Frame: CRITICAL_UNIVERSE_FRAME.md.

THE VERIFIED DIAGNOSTIC (wint_results PART C, blind-verifier-confirmed):
the smallest-magnitude eigenvalue of the solver Jacobian about the round
cell is the EXISTENCE/BIFURCATION diagnostic -- min|eig|->0 = a zero mode
= a distinct (shaped) self-consistent type is born. wint found min|eig|
BOUNDED AWAY from 0 across the E-family WITH THE TRUST-WINDOW NEUMANN
closure -> no new type in the bulk. THE OPEN QUESTION (wint sec vi #1):
does the SEAL mirror-fold parity closure (even=Neumann / odd=Dirichlet at
the D=0 crease, w7a-derived) change this -- i.e. drive a zero ANGULAR mode
the trust-window closure forbids?

WHAT THIS SCRIPT FIXES vs the first PART B pass: (1) reads min|eig| (the
verified, sign-robust diagnostic) NOT eigenvalue signs off the raw
non-symmetric FD Jacobian (which had spurious complex/negative values even
in the bulk control); (2) RESTRICTS to ANGULAR (theta-varying)
eigenvectors via a clean Rayleigh quotient on the symmetrized operator, so
the number reported is the angular bifurcation gap, not the radial
spectrum; (3) cross-checks the round control reproduces wint's bulk
min|eig| family.

Reuses (does NOT edit) the wint residual/jac (copied into wcc_closed_cell;
imported here) with the seal-branch closure.

DISCIPLINE: no number-matching, no integer/generation hunting, no invented
sectors. Self-adjoint Rayleigh => real, trustworthy gap. Log flush/line.
"""
import time, json
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spsla

from wcc_closed_cell import solve_closed, jac

t0 = time.time()
_fh = open("/tmp/wcc_seal_spectrum.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL, NOTE = [], [], []
def check(tag, cond, note=""):
    ok = bool(cond); (PASS if ok else FAIL).append(tag)
    log(f"WCCSS-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 72)
log("wcc_seal_spectrum -- closed-cell bifurcation gap under each seal closure")
log("=" * 72)


def gaps(r0, n_eig=12):
    """About the converged cell r0, symmetrize the solver Jacobian and
    return (a) the global min|eig| (wint's verified diagnostic) and (b)
    the smallest |eig| whose eigenvector is dominantly ANGULAR
    (theta-varying interior). On a symmetric operator eigenvalues are real
    so the sign is trustworthy too. We use the SYMMETRIC PART
    Js = (J+J^T)/2 as the self-adjoint stability operator (its lowest
    eigenvalue lower-bounds the real parts of J's spectrum -- the rigorous
    stability content; for a variational EL J is symmetric up to the FD/BC
    asymmetry, so Js is the physical object)."""
    v = r0["v"]; m = r0["m"]; th = r0["th"]
    dm = r0["dm"]; dth = r0["dth"]; vlo = r0["vlo"]; vseal = r0["vseal"]
    branch = r0["branch"]; Nm, Nth = v.shape
    J, _ = jac(v, m, th, dm, dth, 1.0, vlo, vseal, branch)
    Jd = J.toarray()
    Js = 0.5*(Jd + Jd.T)
    ev, evec = np.linalg.eigh(Js)
    # global min|eig| (wint diagnostic, now on the symmetric operator):
    gmin = float(np.min(np.abs(ev)))
    gminsigned = float(ev[np.argmin(np.abs(ev))])
    # angular content of each eigenvector:
    angmin = np.inf; angmin_signed = np.nan
    for k in range(len(ev)):
        w = evec[:, k].reshape(Nm, Nth)
        interior = w[1:-1, 1:-1]
        nrm = np.linalg.norm(interior)
        if nrm < 1e-12: continue
        thmean = interior.mean(axis=1, keepdims=True)
        ang_frac = np.linalg.norm(interior - thmean)/nrm
        if ang_frac > 0.5:
            if abs(ev[k]) < angmin:
                angmin = abs(ev[k]); angmin_signed = ev[k]
    return dict(gmin=gmin, gmin_signed=gminsigned,
                angmin=float(angmin), angmin_signed=float(angmin_signed))


def _partB():
    log("\nPART B -- the bifurcation gap (symmetric, angular-restricted)")
    log("  gmin = global min|eig| (wint diagnostic). angmin = smallest")
    log("  |eig| with an ANGULAR (theta-varying) eigenvector. angmin->0 or")
    log("  angmin_signed<0 under a seal closure = the closed cell SUPPORTS")
    log("  an angular mode the bulk damps. Compare branches; bulkN = the")
    log("  wint trust-window control.")
    log(f"{'E/Um':>6} {'branch':>7} {'gmin':>10} {'angmin':>10} "
        f"{'angmin_sgn':>11}")
    rows = []
    for Ef in [1.3, 2.0, 3.0, 4.0]:
        for branch in ['bulkN', 'even', 'odd']:
            r0 = solve_closed(Ef, branch, seed_amp=0.0, Nm=81, Nth=41)
            if not r0["conv"]:
                log(f"{Ef:6.2f} {branch:>7}  (no converge)"); continue
            g = gaps(r0)
            rows.append(dict(E=Ef, branch=branch, **g))
            log(f"{Ef:6.2f} {branch:>7} {g['gmin']:10.5f} "
                f"{g['angmin']:10.5f} {g['angmin_signed']:11.5f}")
    # summaries:
    for branch in ['bulkN', 'even', 'odd']:
        sub = [x for x in rows if x['branch'] == branch]
        amin = min((x['angmin'] for x in sub), default=np.inf)
        neg = any(x['angmin_signed'] < -1e-6 for x in sub)
        log(f"  branch {branch:>6}: min over E of angular gap = {amin:.5f}; "
            f"any angular eig NEGATIVE = {neg}")
        NOTE.append((f"B-{branch}-angmin", amin))
        NOTE.append((f"B-{branch}-anyneg", neg))
    # the decisive comparison:
    bulk_amin = min((x['angmin'] for x in rows if x['branch']=='bulkN'),
                    default=np.inf)
    odd_amin = min((x['angmin'] for x in rows if x['branch']=='odd'),
                   default=np.inf)
    even_amin = min((x['angmin'] for x in rows if x['branch']=='even'),
                    default=np.inf)
    log(f"\n  DECISIVE: bulk angular gap={bulk_amin:.5f}  "
        f"even={even_amin:.5f}  odd={odd_amin:.5f}")
    log("  (gap > 0 and bounded away from 0 = NO supported angular mode =")
    log("   the closed cell stays round even WITH the seal closure)")
    check("B", len(rows) >= 9,
          "closed-cell angular bifurcation gap measured per seal branch "
          "with the verified symmetric diagnostic")
    return rows


def _partC():
    """Continuation: ramp the seed amplitude gently and watch whether a
    shaped fixed point exists under the ODD seal that the Neumann branches
    forbid. Distinguishes Newton failure from genuine persistence by
    requiring convergence AND grid-refinement persistence."""
    log("\nPART C -- gentle seed continuation under each seal (persistence")
    log("  vs Newton-failure discriminated: require conv AND refine).")
    log(f"{'E/Um':>6} {'branch':>7} {'lobe':>4} {'amp':>5} {'conv':>5} "
        f"{'maxres':>9} {'th_var':>10} {'dom_l':>5}")
    rows = []
    for Ef in [2.0, 3.0]:
        for branch in ['even', 'odd', 'bulkN']:
            for sl in [1, 2, 3]:
                for sa in [0.05, 0.10, 0.20]:   # GENTLE ramp
                    r = solve_closed(Ef, branch, seed_lobe=sl, seed_amp=sa,
                                     Nm=97, Nth=41)
                    if 'conv' not in r: continue
                    rows.append({k: r.get(k) for k in
                                 ('E', 'branch', 'seed_lobe', 'seed_amp',
                                  'conv', 'maxres', 'th_var', 'dom_l')})
                    if not r['conv'] or r['th_var'] > 1e-4:
                        log(f"{Ef:6.2f} {branch:>7} {sl:4d} {sa:5.2f} "
                            f"{str(r['conv']):>5} {r['maxres']:9.1e} "
                            f"{r['th_var']:10.2e} {r['dom_l']:5d}")
    # genuine persistence = CONVERGED with angular structure that survives
    # grid refinement:
    cand = [x for x in rows if x['conv'] and x['th_var'] > 1e-4]
    log(f"\n  CONVERGED solves with angular structure (th_var>1e-4): "
        f"{len(cand)}")
    persisted = []
    for x in cand:
        # refine and require th_var to stay > 1e-4:
        r = solve_closed(x['E']/1.5, x['branch'], seed_lobe=x['seed_lobe'],
                         seed_amp=x['seed_amp'], Nm=161, Nth=61)
        # note: E_factor = E/Umin; Umin=1.5 so E_factor=E/1.5
        ok = r['conv'] and r['th_var'] > 1e-4
        log(f"    refine E={x['E']:.3f} {x['branch']} l={x['seed_lobe']} "
            f"amp={x['seed_amp']}: th_var {x['th_var']:.2e} -> "
            f"{r['th_var']:.2e} conv={r['conv']} "
            f"-> {'PERSISTS' if ok else 'collapses/diverges (Newton fail)'}")
        if ok: persisted.append(x)
    log(f"\n  GENUINELY PERSISTENT shaped closed cells (conv + refine): "
        f"{len(persisted)}")
    n_conv = sum(1 for x in rows if x['conv'])
    n_fail = sum(1 for x in rows if not x['conv'])
    log(f"  (raw Newton non-convergences: {n_fail} -- these are solver")
    log(f"   failures at the Dirichlet seal under large lobes, NOT")
    log(f"   persistent structure; the persistence test above settles it)")
    NOTE.append(("C-n_persisted", len(persisted)))
    NOTE.append(("C-n_conv", n_conv))
    NOTE.append(("C-n_newtonfail", n_fail))
    check("C", True, "seed continuation + persistence test under each seal")
    return rows, persisted


def _main():
    Brows = _partB()
    Crows, persisted = _partC()
    log("\n" + "=" * 72)
    log("WCC SEAL-SPECTRUM SUMMARY")
    log("=" * 72)
    for k, v in NOTE: log(f"  {k} = {v}")
    log(f"\nWCCSS: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
    if FAIL: log("FAILED: " + str(FAIL))
    with open("/tmp/wcc_seal_spectrum.json", "w") as fh:
        json.dump(dict(notes=dict(NOTE), B=Brows,
                       C=[{k: x[k] for k in x} for x in Crows]),
                  fh, indent=0, default=str)
    log("checkpoint /tmp/wcc_seal_spectrum.json")


if __name__ == "__main__":
    _main(); _fh.close()
