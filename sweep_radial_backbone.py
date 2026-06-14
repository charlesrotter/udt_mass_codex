"""
Robust radial-backbone BVP solver for the UDT metric field equation.

ODE (radial sector of the UDT metric field equation), Phi=1 fixed:
    phi'' + (2/r) phi' - 2 phi'^2 = Phi*(1 - e^{3 phi})
BCs:
    phi(r_in=1) = D    (core depth = matter content)
    phi(r*)     = 0    (outer interface)

We discretize on a uniform grid r in [1, r*] with N interior unknowns
(the two endpoints are Dirichlet). Second-order central differences.
Dense Newton with analytic Jacobian. Natural + pseudo-arclength
continuation in D. float64 everywhere.

DO NOT edit other repo files. Helper file only.
"""
import numpy as np
import json

R_IN = 1.0
PHI = 1.0


def make_grid(rstar, N):
    """N total grid points incl endpoints, uniform in r. Returns r, h."""
    r = np.linspace(R_IN, rstar, N)
    h = r[1] - r[0]
    return r, h


def residual_full(phi, r, h, D):
    """
    Residual of the discretized ODE at interior nodes.
    phi: full array length N (with endpoints). Returns F length N-2.
    Endpoints enforced separately: phi[0]=D, phi[-1]=0.
    F_i = (phi_{i+1}-2phi_i+phi_{i-1})/h^2
          + (2/r_i)*(phi_{i+1}-phi_{i-1})/(2h)
          - 2*((phi_{i+1}-phi_{i-1})/(2h))^2
          - PHI*(1 - exp(3 phi_i))
    """
    pm = phi[:-2]
    p0 = phi[1:-1]
    pp = phi[2:]
    ri = r[1:-1]
    d2 = (pp - 2.0 * p0 + pm) / h**2
    d1 = (pp - pm) / (2.0 * h)
    F = d2 + (2.0 / ri) * d1 - 2.0 * d1**2 - PHI * (1.0 - np.exp(3.0 * p0))
    return F


def jacobian_interior(phi, r, h, D):
    """
    Jacobian of F (length M=N-2) wrt interior unknowns phi[1:-1] (length M).
    Tridiagonal. Returns dense MxM (1D problem, dense is fine for N<=2000;
    for large N we build banded). Columns correspond to interior nodes.
    """
    M = len(phi) - 2
    ri = r[1:-1]
    d1 = (phi[2:] - phi[:-2]) / (2.0 * h)
    # dF_i/dphi_i
    diag = -2.0 / h**2 + PHI * 3.0 * np.exp(3.0 * phi[1:-1])
    # dF_i/dphi_{i+1}: from d2 (1/h^2), from d1 ((2/ri)/(2h)), from -2 d1^2 (-4 d1 * (1/(2h)))
    upper = 1.0 / h**2 + (2.0 / ri) / (2.0 * h) - 2.0 * 2.0 * d1 / (2.0 * h)
    # dF_i/dphi_{i-1}
    lower = 1.0 / h**2 - (2.0 / ri) / (2.0 * h) + 2.0 * 2.0 * d1 / (2.0 * h)
    J = np.zeros((M, M))
    idx = np.arange(M)
    J[idx, idx] = diag
    J[idx[:-1], idx[:-1] + 1] = upper[:-1]
    J[idx[1:], idx[1:] - 1] = lower[1:]
    # Note: at i=0 (first interior), phi_{i-1}=phi[0]=D (fixed) -> not an unknown.
    # at i=M-1 (last interior), phi_{i+1}=phi[-1]=0 (fixed) -> not an unknown.
    return J, upper, lower  # upper[0], lower[-1] couple to BCs (for arclength)


def dF_dD(phi, r, h):
    """dF/dD: only F_0 depends on D through phi_{i-1}=D at first interior node.
    F_0 has term (D)/h^2 + ... and d1 = (phi_2 - D)/(2h).
    dF_0/dD = 1/h^2 - (2/r_1)/(2h) + 2*2*d1_0/(2h)."""
    M = len(phi) - 2
    v = np.zeros(M)
    ri1 = r[1]
    d1_0 = (phi[2] - phi[0]) / (2.0 * h)
    v[0] = 1.0 / h**2 - (2.0 / ri1) / (2.0 * h) + 2.0 * 2.0 * d1_0 / (2.0 * h)
    return v


def newton_solve(phi0, r, h, D, tol=1e-11, maxit=200, verbose=False):
    """Damped Newton with line search. phi0 full array (endpoints set)."""
    phi = phi0.copy()
    phi[0] = D
    phi[-1] = 0.0
    F = residual_full(phi, r, h, D)
    rn = np.max(np.abs(F))
    for it in range(maxit):
        if rn < tol:
            return phi, rn, it, True
        J, _, _ = jacobian_interior(phi, r, h, D)
        try:
            dx = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            return phi, rn, it, False
        # line search
        lam = 1.0
        ok = False
        for _ in range(40):
            trial = phi.copy()
            trial[1:-1] = phi[1:-1] + lam * dx
            Ft = residual_full(trial, r, h, D)
            rnt = np.max(np.abs(Ft))
            if np.isfinite(rnt) and rnt < (1.0 - 1e-4 * lam) * rn:
                phi = trial
                F = Ft
                rn = rnt
                ok = True
                break
            lam *= 0.5
        if not ok:
            # accept tiny step if it reduces at all
            trial = phi.copy()
            trial[1:-1] = phi[1:-1] + lam * dx
            Ft = residual_full(trial, r, h, D)
            rnt = np.max(np.abs(Ft))
            if np.isfinite(rnt) and rnt < rn:
                phi, F, rn = trial, Ft, rnt
            else:
                return phi, rn, it, False
    return phi, rn, maxit, rn < tol


def linear_seed(r, h, D, rstar):
    """Linear interpolation seed phi = D*(rstar - r)/(rstar - r_in)."""
    return D * (rstar - r) / (rstar - R_IN)


# ---------------------------------------------------------------------------
# Natural continuation in D with warm start
# ---------------------------------------------------------------------------
def natural_continuation(rstar, N, D_target, dD0=0.01, tol=1e-11):
    """March D from 0 up toward D_target, warm-starting. Returns dict of
    converged solutions keyed by D. Stops if it cannot converge (fold/seal)."""
    r, h = make_grid(rstar, N)
    phi = np.zeros(N)
    results = {}
    D = 0.0
    dD = dD0
    # D=0 trivial solution is phi=0 (check: 1-e^0=0, ok). Start there.
    phi, rn, it, ok = newton_solve(phi, r, h, 0.0, tol=tol)
    results[0.0] = (phi.copy(), rn)
    last_phi = phi.copy()
    while D < D_target - 1e-12:
        step = min(dD, D_target - D)
        Dn = D + step
        seed = last_phi.copy()
        seed[0] = Dn
        phi, rn, it, ok = newton_solve(seed, r, h, Dn, tol=tol)
        if ok and rn < 1e-9:
            results[Dn] = (phi.copy(), rn)
            last_phi = phi.copy()
            D = Dn
            if it < 6:
                dD = min(dD * 1.3, dD0 * 5)
        else:
            dD *= 0.4
            if dD < 1e-6:
                break
    return r, h, results, D


# ---------------------------------------------------------------------------
# Pseudo-arclength continuation (traverses folds)
# Unknowns: u = phi_interior (length M), and parameter D.
# Augmented system:
#   F(u, D) = 0                                  (M eqs)
#   N(u,D,s) = dot(du/ds, (u-u0)) + (dD/ds)(D-D0) - ds = 0  (1 eq)
# Predictor: tangent (du, dD); corrector: Newton on augmented (M+1)x(M+1).
# ---------------------------------------------------------------------------
def arclength_continuation(rstar, N, ds0=0.02, max_steps=4000, tol=1e-11,
                           D_cap=50.0, fcore_floor=1e-6):
    r, h = make_grid(rstar, N)
    M = N - 2
    # start from D=0 trivial
    phi = np.zeros(N)
    phi, rn, it, ok = newton_solve(phi, r, h, 0.0, tol=tol)
    u = phi[1:-1].copy()
    D = 0.0
    # initial tangent: increase D. Solve J du = -dF/dD.
    def assemble(u, D):
        ph = np.empty(N)
        ph[0] = D; ph[-1] = 0.0; ph[1:-1] = u
        F = residual_full(ph, r, h, D)
        J, _, _ = jacobian_interior(ph, r, h, D)
        Fd = dF_dD(ph, r, h)
        return ph, F, J, Fd

    ph, F, J, Fd = assemble(u, D)
    du = np.linalg.solve(J, -Fd)
    dD = 1.0
    nrm = np.sqrt(du @ du + dD**2)
    du /= nrm; dD /= nrm
    if dD < 0:
        du = -du; dD = -dD  # start by increasing D

    branch = []
    ds = ds0
    prev_tan = (du.copy(), dD)
    fold_info = None
    for stp in range(max_steps):
        ph_cur, _, _, _ = assemble(u, D)
        fcore = np.exp(-2.0 * D)
        maxphi = np.max(ph_cur)
        comp = 1.0 - np.exp(-2.0 * maxphi)
        d1 = (ph_cur[2:] - ph_cur[:-2]) / (2.0 * h)
        maxdphi = np.max(np.abs(d1))
        branch.append(dict(D=D, comp=comp, fcore=fcore, maxphi=maxphi,
                           maxdphi=maxdphi, ds=ds, dDds=dD))
        if D > D_cap or fcore < fcore_floor:
            break
        # Predictor
        du_p, dD_p = prev_tan
        u_pred = u + ds * du_p
        D_pred = D + ds * dD_p
        # Corrector: Newton on augmented system
        u_c = u_pred.copy(); D_c = D_pred
        conv = False
        for nit in range(60):
            ph, F, J, Fd = assemble(u_c, D_c)
            # arclength constraint: tangent dot (state - predicted-from-base)
            n_val = du_p @ (u_c - u) + dD_p * (D_c - D) - ds
            rn = max(np.max(np.abs(F)), abs(n_val))
            if rn < 1e-9:
                conv = True
                break
            # Augmented Jacobian [[J, Fd],[du_p^T, dD_p]]
            A = np.zeros((M + 1, M + 1))
            A[:M, :M] = J
            A[:M, M] = Fd
            A[M, :M] = du_p
            A[M, M] = dD_p
            rhs = np.concatenate([F, [n_val]])
            try:
                dz = np.linalg.solve(A, -rhs)
            except np.linalg.LinAlgError:
                break
            # damping
            lam = 1.0
            for _ in range(30):
                u_t = u_c + lam * dz[:M]
                D_t = D_c + lam * dz[M]
                ph2 = np.empty(N); ph2[0]=D_t; ph2[-1]=0.0; ph2[1:-1]=u_t
                F2 = residual_full(ph2, r, h, D_t)
                n2 = du_p @ (u_t - u) + dD_p * (D_t - D) - ds
                rn2 = max(np.max(np.abs(F2)), abs(n2))
                if np.isfinite(rn2) and rn2 < (1 - 1e-4*lam) * rn:
                    u_c, D_c = u_t, D_t
                    break
                lam *= 0.5
            else:
                break
        if not conv:
            ds *= 0.5
            if ds < 1e-7:
                break
            continue
        # New tangent: solve [[J,Fd],[du_p,dD_p]] t = [0...0,1]
        ph, F, J, Fd = assemble(u_c, D_c)
        A = np.zeros((M + 1, M + 1))
        A[:M, :M] = J; A[:M, M] = Fd
        A[M, :M] = du_p; A[M, M] = dD_p
        e = np.zeros(M + 1); e[M] = 1.0
        try:
            t = np.linalg.solve(A, e)
        except np.linalg.LinAlgError:
            break
        tn = np.sqrt(t @ t)
        t /= tn
        du_new = t[:M]; dD_new = t[M]
        # keep direction consistent
        if du_new @ du_p + dD_new * dD_p < 0:
            du_new = -du_new; dD_new = -dD_new
        # detect fold: sign change in dD/ds
        if dD_p > 0 and dD_new <= 0 and fold_info is None:
            fold_info = dict(D=D_c, comp=1.0 - np.exp(-2*np.max(
                np.r_[D_c, u_c, 0.0])), fcore=np.exp(-2*D_c))
        u, D = u_c, D_c
        prev_tan = (du_new, dD_new)
        # grow step if converged fast
        if nit < 4:
            ds = min(ds * 1.2, ds0 * 4)
    return r, h, branch, fold_info


def find_fold(branch):
    """Locate max D along branch (the fold/turning point in D)."""
    if not branch:
        return None
    Ds = np.array([b['D'] for b in branch])
    i = int(np.argmax(Ds))
    return branch[i], i, Ds[i]
