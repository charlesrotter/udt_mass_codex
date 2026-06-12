"""W5 ARM-2 VERIFIER #3 — ARC-LENGTH FOLD ATTACK (M1, full domain,
OFF branch, untruncated species).

Question: is the OFF static-existence edge at kappa ~ 0.9157 (critical
ray) a GENUINE FOLD (saddle-node: branch turns, two solutions coexist
just above the edge, Jacobian eigenvalue crosses zero) or a solver
artifact / branch endpoint?

Method: pseudo-arclength continuation of the per-ray static system
  G_i(v, kappa) = [stiffness] - w_i * (1/(8k))(1 - 2k/f_i) b_i e^{-2v_i}
(natural Neumann at the weld t=0, Dirichlet at t_b = t_stop), bordered
Newton on (v, kappa) with secant tangent and the constraint
  tau_v . (v - v_pred)/N + tau_k (kappa - kappa_pred) = 0.
dG_i/dkappa = + w_i b_i e^{-2 v_i} / (8 kappa^2)   (exact: the factor
combination lam*fac = 1/(8k) - 1/(4f) has all kappa dependence in the
1/(8k) term).

Independent of w5_arm2_lib.  Imports only the committed
w4b_verifier_lib for the member flow.  Verifier agent VB5, 2026-06-12.
"""
import sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.linalg import eigh_tridiagonal

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
from w5_arm2_verifier3_fresh import Geo, newton_ray

LOG = open("/tmp/w5_arm2_verifier3_fresh.log", "a")


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    LOG.write(msg + "\n")
    LOG.flush()


class RaySys:
    def __init__(self, geo, k):
        self.h = geo.tg[1] - geo.tg[0]
        self.p = geo.p[:, k]
        self.b = geo.b[:, k]
        self.f = geo.f[:, k]
        self.N = geo.Nt
        self.pm = 0.5 * (self.p[1:] + self.p[:-1])
        self.w = np.full(self.N, self.h)
        self.w[0] = 0.5 * self.h

    def G(self, v, kap):
        h, pm, w, b, f = self.h, self.pm, self.w, self.b, self.f
        em2 = np.exp(-2 * v)
        src = (1.0 / (8 * kap) - 1.0 / (4 * f)) * b * em2
        F = np.zeros(self.N)
        F[1:-1] = (pm[1:] * (v[2:] - v[1:-1])
                   - pm[:-1] * (v[1:-1] - v[:-2])) / h \
            - w[1:-1] * src[1:-1]
        F[0] = pm[0] * (v[1] - v[0]) / h - w[0] * src[0]
        F[-1] = v[-1]
        return F

    def Jv_diags(self, v, kap):
        """tridiagonal Jacobian dG/dv as (lo, di, up)."""
        h, pm, w, b, f = self.h, self.pm, self.w, self.b, self.f
        em2 = np.exp(-2 * v)
        src = (1.0 / (8 * kap) - 1.0 / (4 * f)) * b * em2
        di = np.zeros(self.N)
        up = np.zeros(self.N)
        lo = np.zeros(self.N)
        di[1:-1] = -(pm[1:] + pm[:-1]) / h + 2 * w[1:-1] * src[1:-1]
        up[1:-1] = pm[1:] / h
        lo[1:-1] = pm[:-1] / h
        di[0] = -pm[0] / h + 2 * w[0] * src[0]
        up[0] = pm[0] / h
        di[-1] = 1.0
        lo[-1] = 0.0
        return lo, di, up

    def Gk(self, v, kap):
        gk = self.w * self.b * np.exp(-2 * v) / (8 * kap ** 2)
        gk[-1] = 0.0
        return gk

    def lowest_jac_ev(self, v, kap):
        """lowest eigenvalue of the SYMMETRIC stability operator
        L psi = -(p psi')' + dsrc/dv psi in the lumped inner product
        (Dirichlet at t_b): sign flip at the fold."""
        lo, di, up = self.Jv_diags(v, kap)
        # G rows are scaled FEM rows; symmetrize: -J scaled by 1/w
        d = -di[:-1] / self.w[:-1]
        e = -up[:-2] / np.sqrt(self.w[:-2] * self.w[1:-1])
        Wi = 1.0 / np.sqrt(self.w[:-1])
        # exact symmetric congruence: A_ij = -J_ij / sqrt(w_i w_j)
        d = -di[:-1] * Wi ** 2
        e = -up[:-2] * Wi[:-1] * Wi[1:]
        ev = eigh_tridiagonal(d, e, select='i', select_range=(0, 0),
                              eigvals_only=True)
        return float(ev[0])


def bordered_newton(sysm, v, kap, tau_v, tau_k, v_pred, k_pred,
                    alpha, tol=1e-11, maxit=40):
    N = sysm.N
    for it in range(maxit):
        F = sysm.G(v, kap)
        cons = alpha * float(tau_v @ (v - v_pred)) + tau_k * (kap - k_pred)
        if max(np.max(np.abs(F)), abs(cons)) < tol:
            return v, kap, True
        lo, di, up = sysm.Jv_diags(v, kap)
        gk = sysm.Gk(v, kap)
        rows = []
        cols = []
        vals = []
        idx = np.arange(N)
        rows.extend(idx)
        cols.extend(idx)
        vals.extend(di)
        rows.extend(idx[:-1])
        cols.extend(idx[1:])
        vals.extend(up[:-1])
        rows.extend(idx[1:])
        cols.extend(idx[:-1])
        vals.extend(lo[1:])
        rows.extend(idx)
        cols.extend([N] * N)
        vals.extend(gk)
        rows.extend([N] * N)
        cols.extend(idx)
        vals.extend(alpha * tau_v)
        rows.append(N)
        cols.append(N)
        vals.append(tau_k)
        A = sp.csc_matrix((vals, (rows, cols)), shape=(N + 1, N + 1))
        rhs = -np.concatenate([F, [cons]])
        try:
            dz = spla.spsolve(A, rhs)
        except Exception:
            return v, kap, False
        if not np.all(np.isfinite(dz)):
            return v, kap, False
        step = np.max(np.abs(dz))
        damp = 1.0 if step < 0.5 else 0.5 / step
        v = v + damp * dz[:N]
        kap = kap + damp * dz[N]
        if v.min() < -16 or v.max() > 40 or kap <= 0:
            return v, kap, False
    return v, kap, False


def main():
    log("=" * 72)
    log("[T4] ARC-LENGTH FOLD ATTACK: M1 full domain, OFF, untruncated")
    sol = vl.flow(1.0, 0.18413678)
    geo = Geo(sol, t_b=None, Nt=4000)
    KRAY = 20          # critical ray from the main verifier run
    log(f"  critical ray {KRAY}: u={geo.u[KRAY]:+.6f}")
    sysm = RaySys(geo, KRAY)
    N = geo.Nt
    alpha = 1.0 / N    # v-norm weight in the arclength metric

    # two anchor points by plain Newton
    k0, k1 = 1.10, 1.07
    v0 = newton_ray(geo, KRAY, k0, dcell=False)
    v1 = newton_ray(geo, KRAY, k1, dcell=False, vinit=v0)
    assert v0 is not None and v1 is not None
    log(f"  anchors: kappa={k0} ||v||rms={np.linalg.norm(v0)/np.sqrt(N):.6f}"
        f" ; kappa={k1} ||v||rms={np.linalg.norm(v1)/np.sqrt(N):.6f}")

    branch = [(k0, v0), (k1, v1)]
    ds = 0.03
    kmin, vmin_at_fold = np.inf, None
    fold_ev_cross = None
    prev_ev = sysm.lowest_jac_ev(v1, k1)
    log(f"  lowest stability ev at start: {prev_ev:.6f}")
    nturn = 0
    for step in range(600):
        (ka, va), (kb, vb) = branch[-2], branch[-1]
        dv = vb - va
        dk = kb - ka
        nrm = np.sqrt(alpha * float(dv @ dv) + dk * dk)
        tau_v, tau_k = dv / nrm, dk / nrm
        ok = False
        ds_try = ds
        for _ in range(8):
            v_pred = vb + ds_try * tau_v
            k_pred = kb + ds_try * tau_k
            v2, k2, ok = bordered_newton(sysm, v_pred.copy(), k_pred,
                                         tau_v, tau_k, v_pred, k_pred,
                                         alpha)
            if ok:
                break
            ds_try *= 0.4
        if not ok:
            log(f"  step {step}: continuation stalled at kappa={kb:.6f} "
                f"ds={ds_try:.2e}")
            break
        branch.append((k2, v2))
        ds = min(ds_try * 1.5, 0.06)
        ev = sysm.lowest_jac_ev(v2, k2)
        if k2 < kmin:
            kmin, vmin_at_fold = k2, v2
        # detect tangent sign change in kappa
        if (k2 - kb) * (kb - ka) < 0 and nturn == 0:
            nturn = 1
            log(f"  >>> dkappa/ds SIGN CHANGE at step {step}: "
                f"kappa turns at ~{kb:.6f} "
                f"(||v||rms={np.linalg.norm(vb)/np.sqrt(N):.6f})")
        if prev_ev * ev < 0 and fold_ev_cross is None:
            fold_ev_cross = (kb, k2)
            log(f"  >>> lowest stability ev crosses ZERO between "
                f"kappa={kb:.6f} ({prev_ev:.3e}) and kappa={k2:.6f} "
                f"({ev:.3e})")
        prev_ev = ev
        if step % 20 == 0:
            log(f"  step {step:3d}: kappa={k2:.6f} "
                f"||v||rms={np.linalg.norm(v2)/np.sqrt(N):.6f} "
                f"vmin={v2.min():.4f} ev_low={ev:.4e}")
        # stop when well past the fold on the upper branch
        if nturn and (k2 > 1.05 or v2.min() < -10):
            log(f"  stop: upper branch reached kappa={k2:.6f} "
                f"vmin={v2.min():.4f}")
            break

    ks = np.array([k for k, _ in branch])
    log(f"\n  branch: {len(branch)} points, kappa range "
        f"[{ks.min():.6f}, {ks.max():.6f}]")
    log(f"  FOLD kappa (min over branch) = {kmin:.6f}  "
        f"(claimed member edge 0.915696)")

    # two-solutions check at kappa = 0.93 (above the fold)
    ktest = 0.93
    lower = None
    upper = None
    after_turn = False
    for i in range(1, len(branch)):
        ka, va = branch[i - 1]
        kb, vb = branch[i]
        if (kb - ka) < 0 is None:
            pass
        if not after_turn and kb < ka and kb <= kmin + 1e-9:
            pass
        # mark turn by index of kmin
    ik = int(np.argmin(ks))
    pre = [i for i in range(ik) if abs(ks[i] - ktest) ==
           min(abs(ks[j] - ktest) for j in range(ik))]
    post = [i for i in range(ik, len(ks)) if abs(ks[i] - ktest) ==
            min(abs(ks[j] - ktest) for j in range(ik, len(ks)))]
    if pre and post:
        i1, i2 = pre[0], post[0]
        vA = newton_ray(geo, KRAY, ktest, dcell=False, vinit=branch[i1][1])
        vB = newton_ray(geo, KRAY, ktest, dcell=False, vinit=branch[i2][1])
        if vA is not None and vB is not None:
            nA = np.linalg.norm(vA) / np.sqrt(N)
            nB = np.linalg.norm(vB) / np.sqrt(N)
            log(f"  TWO-SOLUTION CHECK at kappa={ktest}: lower-branch "
                f"||v||rms={nA:.6f} vmin={vA.min():.4f} ; upper-branch "
                f"||v||rms={nB:.6f} vmin={vB.min():.4f} ; "
                f"distinct={abs(nA-nB) > 1e-4}")
        else:
            log(f"  TWO-SOLUTION CHECK at kappa={ktest}: refine failed "
                f"(A={'ok' if vA is not None else 'None'}, "
                f"B={'ok' if vB is not None else 'None'})")
    else:
        log("  TWO-SOLUTION CHECK: branch did not cover kappa=0.93 on "
            "both sides of the turn")

    # grid statement: repeat fold localization at Nt=8000
    log("\n  [grid] repeating continuation fold at Nt=8000")
    geo2 = Geo(sol, t_b=None, Nt=8000)
    sysm2 = RaySys(geo2, KRAY)
    N2 = geo2.Nt
    v0b = newton_ray(geo2, KRAY, k0, dcell=False)
    v1b = newton_ray(geo2, KRAY, k1, dcell=False, vinit=None)
    branch2 = [(k0, v0b), (k1, v1b)]
    ds2 = 0.03
    kmin2 = np.inf
    al2 = 1.0 / N2
    for step in range(600):
        (ka, va), (kb, vb) = branch2[-2], branch2[-1]
        dv = vb - va
        dk = kb - ka
        nrm = np.sqrt(al2 * float(dv @ dv) + dk * dk)
        tau_v, tau_k = dv / nrm, dk / nrm
        ok = False
        ds_try = ds2
        for _ in range(8):
            v_pred = vb + ds_try * tau_v
            k_pred = kb + ds_try * tau_k
            v2, k2, ok = bordered_newton(sysm2, v_pred.copy(), k_pred,
                                         tau_v, tau_k, v_pred, k_pred,
                                         al2)
            if ok:
                break
            ds_try *= 0.4
        if not ok:
            break
        branch2.append((k2, v2))
        ds2 = min(ds_try * 1.5, 0.06)
        kmin2 = min(kmin2, k2)
        if len(branch2) > 4 and k2 > branch2[-2][0] and k2 > kmin2 + 0.05:
            break
    log(f"  [grid] Nt=8000 fold kappa = {kmin2:.6f} "
        f"(Nt=4000: {kmin:.6f}; rel dev "
        f"{abs(kmin2-kmin)/kmin:.2e})")
    log("\n[T4] DONE")


if __name__ == "__main__":
    main()
