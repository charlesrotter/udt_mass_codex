#!/usr/bin/env python3
"""
FULL-PDE P1 solver stack.

Derived system (29/29 sympy checks, derive_system.py):
  - q := g_rtheta and w (unimodular sphere-shape) are EXACTLY ALGEBRAIC.
  - q-EL: q* = 2 r^2 W f_r f_th / (f r^2 W f_r^2 + f_th^2); exact elimination
    gives L_eff = -(c/8) sin(th) |f r^2 f_r^2 - f_th^2/W| / f.
  - w-EL has NO solution off the spherical locus (runaway theorem).
  - Class A (q=w=0, diagonal):   X_tt - X_t = +2 P_X   (elliptic in 2D)
  - Class B (q free, w=0):       X_tt - X_t = -2 P_X   (hyperbolic in 2D)
    on the radial-dominant branch Delta = f f_t^2 - (1-u^2) f_u^2 > 0,
    with Q* = e^t q* = 2 f_t v/(f f_t^2 + v^2), v = sqrt(1-u^2) f_u.
  P = (1/8) Int_{-1}^{1} (1-u^2) f_u^2 / f du,  f = sum X_l Y_l(u),
  Y_l orthonormal under du/2.  t = ln(1/y), weld at t = 0.

Discretization (choice + justification):
  * u-direction: Galerkin in orthonormal Legendre Y_l (exactly the banked
    library representation -> anchor comparability; spectral accuracy; the
    degenerate (1-u^2) operator makes the poles regular automatically, no
    axis BC rows needed).  Quadrature: Gauss-Legendre N=2000 (library
    convention).  P_X / P_XX kernels are sympy-derived (see codegen below)
    and evaluated as pure matmuls (GPU pitfall: no batched triangular
    solves; everything here is matmul + one dense LU per Newton step).
  * t-direction: DOP853 (rtol 1e-11) for radial-flow IVPs (library
    convention; the natural well-posed problem for hyperbolic Class B) and
    Chebyshev-Lobatto collocation + full Newton with analytic Jacobian
    (torch float64, CUDA) for the BVP/continuation machine (P2 hooks).
  * 2D mode (Class A, elliptic): tensor Chebyshev(t) x Gauss-Legendre(u)
    collocation, full Newton, analytic Jacobian, dense GPU solve.
"""
import numpy as np
import torch
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp

torch.set_default_dtype(torch.float64)
DEV = 'cuda' if torch.cuda.is_available() else 'cpu'

# ----------------------------------------------------------------------
# sympy-generated kernels for P, P_X, P_XX (codegen at import, verified)
# ----------------------------------------------------------------------
def _sympy_kernels():
    import sympy as sp
    f, fu, u = sp.symbols('f f_u u', real=True)
    Pint = sp.Rational(1, 8)*(1-u**2)*fu**2/f
    # variations: delta f = Y, delta f_u = Yp
    g_fu = sp.simplify(sp.diff(Pint, fu))      # coefficient of Yp in P_X
    g_f  = sp.simplify(sp.diff(Pint, f))       # coefficient of Y  in P_X
    h_fufu = sp.simplify(sp.diff(Pint, fu, 2))   # Yp Yp kernel
    h_ffu  = sp.simplify(sp.diff(Pint, f, fu))   # Y Yp + Yp Y kernel
    h_ff   = sp.simplify(sp.diff(Pint, f, 2))    # Y Y kernel
    exprs = dict(Pint=Pint, g_fu=g_fu, g_f=g_f,
                 h_fufu=h_fufu, h_ffu=h_ffu, h_ff=h_ff)
    fns = {k: sp.lambdify((f, fu, u), v, 'numpy') for k, v in exprs.items()}
    return exprs, fns

KERNEL_EXPRS, KER = _sympy_kernels()

def legendre_Y(ellmax, u):
    """Orthonormal (du/2) Legendre: Y_l = sqrt(2l+1) P_l. Returns Y, Y'."""
    u = np.asarray(u, dtype=float)
    P = np.zeros((ellmax+2, *u.shape)); Pp = np.zeros_like(P)
    P[0] = 1.0
    if ellmax+1 >= 1: P[1] = u
    for l in range(1, ellmax+1):
        P[l+1] = ((2*l+1)*u*P[l] - l*P[l-1])/(l+1)
    # derivative recursion: (1-u^2) P_l' = l (P_{l-1} - u P_l)
    for l in range(ellmax+2):
        if l == 0: Pp[l] = 0.0
        else:      Pp[l] = l*(P[l-1] - u*P[l])/(1-u**2 + 1e-300)
    norm = np.sqrt(2*np.arange(ellmax+2)+1)
    Y  = norm[:ellmax+1, None]*P[:ellmax+1]
    Yp = norm[:ellmax+1, None]*Pp[:ellmax+1]
    return Y, Yp

class AngularSector:
    """P(X), grad P, Hess P on the Gauss-Legendre grid (numpy + torch)."""
    def __init__(self, ellmax, Nquad=2000, dev=DEV):
        self.ellmax = ellmax
        un, wn = leggauss(Nquad)
        self.u, self.wq = un, wn                 # plain du weights
        self.Y, self.Yp = legendre_Y(ellmax, un)  # (L+1, N)
        self.dev = dev
        self.tu  = torch.tensor(un, device=dev)
        self.twq = torch.tensor(wn, device=dev)
        self.tY  = torch.tensor(self.Y, device=dev)
        self.tYp = torch.tensor(self.Yp, device=dev)
        # dense u-grid (incl. poles) for f_min:
        self.ud = np.linspace(-1, 1, 4001)
        self.Yd, _ = legendre_Y(ellmax, np.clip(self.ud, -1+1e-12, 1-1e-12))
        # exact pole values:
        self.Yd[:, 0]  = np.sqrt(2*np.arange(ellmax+1)+1)*(-1)**np.arange(ellmax+1)
        self.Yd[:, -1] = np.sqrt(2*np.arange(ellmax+1)+1)

    def fields(self, X):
        f  = X @ self.Y
        fu = X @ self.Yp
        return f, fu

    def P(self, X):
        f, fu = self.fields(X)
        return float(np.dot(KER['Pint'](f, fu, self.u), self.wq))

    def gradP(self, X):
        f, fu = self.fields(X)
        a = KER['g_fu'](f, fu, self.u)*self.wq
        b = KER['g_f'](f, fu, self.u)*self.wq
        return self.Yp @ a + self.Y @ b

    def hessP(self, X):
        f, fu = self.fields(X)
        hpp = KER['h_fufu'](f, fu, self.u)*self.wq
        hpf = KER['h_ffu'](f, fu, self.u)*self.wq
        hff = KER['h_ff'](f, fu, self.u)*self.wq
        H = (self.Yp*hpp) @ self.Yp.T
        H += (self.Yp*hpf) @ self.Y.T + (self.Y*hpf) @ self.Yp.T
        H += (self.Y*hff) @ self.Y.T
        return H

    # torch versions (matmul-only) for the Newton machine
    def t_gradP(self, U):
        """U: (Nt, L+1) torch -> (Nt, L+1)."""
        f  = U @ self.tY      # (Nt, N)
        fu = U @ self.tYp
        u = self.tu
        a = ((1 - u**2)*fu/(4*f))*self.twq
        b = (-(1 - u**2)*fu**2/(8*f**2))*self.twq
        return a @ self.tYp.T + b @ self.tY.T

    def t_hessP(self, U):
        """U: (Nt, L+1) -> (Nt, L+1, L+1)."""
        f  = U @ self.tY
        fu = U @ self.tYp
        u = self.tu
        hpp = ((1 - u**2)/(4*f))*self.twq
        hpf = (-(1 - u**2)*fu/(4*f**2))*self.twq
        hff = ((1 - u**2)*fu**2/(4*f**3))*self.twq
        Yp, Y = self.tYp, self.tY
        H  = torch.einsum('ln,tn,mn->tlm', Yp, hpp, Yp)
        H += torch.einsum('ln,tn,mn->tlm', Yp, hpf, Y)
        H += torch.einsum('ln,tn,mn->tlm', Y,  hpf, Yp)
        H += torch.einsum('ln,tn,mn->tlm', Y,  hff, Y)
        return H

    def fmin(self, X):
        fd = X @ self.Yd
        i = np.argmin(fd)
        return fd[i], self.ud[i]

# ----------------------------------------------------------------------
# Radial-flow IVP (library mode).  sign=+1 Class A, sign=-1 Class B.
# ----------------------------------------------------------------------
def run_flow(ang, gamma, c, sign=+1, t_max=15.0, cutoff=0.002,
             rtol=1e-11, atol=1e-13, drive=None, dense_dt=None):
    L = ang.ellmax
    X0 = np.zeros(L+1); X0[0] = 1.0
    V0 = np.zeros(L+1); V0[0] = gamma
    if drive is None:
        if L >= 1: V0[1] = -c
    else:
        V0[1:len(drive)+1] = drive
    def rhs(t, s):
        X, V = s[:L+1], s[L+1:]
        return np.concatenate([V, V + sign*2.0*ang.gradP(X)])
    # NOTE: no ride-away early exit.  The system is amplitude scale-covariant
    # (P degree-1 homogeneous => P_X degree-0), so large f_min does NOT decide
    # the fate; flows can seal long after riding through f_min >> 1.  SAT is
    # declared only by reaching t_max unsealed (classification caveat: t_max
    # horizon; threshold values quoted with their t_max).
    def ev_seal(t, s):
        return ang.fmin(s[:L+1])[0] - cutoff
    ev_seal.terminal, ev_seal.direction = True, -1
    sol = solve_ivp(rhs, (0.0, t_max), np.concatenate([X0, V0]),
                    method='DOP853', rtol=rtol, atol=atol, dense_output=True,
                    events=[ev_seal], max_step=0.05)
    res = dict(sol=sol, ang=ang, gamma=gamma, c=c, sign=sign)
    res['sealed'] = len(sol.t_events[0]) > 0
    res['t_stop'] = sol.t[-1]
    if res['sealed']:
        ts = sol.t_events[0][0]
        s = sol.sol(ts); X, V = s[:L+1], s[L+1:]
        fmin, umin = ang.fmin(X)
        dfmin = ang.fmin(V)[0] if False else None
        # linear-layer extrapolation: t_seal* = ts + f_min/|df_min/dt|
        h = 1e-6
        f2 = ang.fmin(sol.sol(ts-h)[:L+1])[0]
        slope = (fmin - f2)/h
        res['t_seal'] = ts + (fmin/(-slope) if slope < 0 else 0.0)
        res['y_seal'] = float(np.exp(-res['t_seal']))
        res['u_min'] = umin
    return res

def flow_state(res, t):
    L = res['ang'].ellmax
    s = res['sol'].sol(np.atleast_1d(t))
    return s[:L+1].T, s[L+1:].T   # X(t), V(t)

def bisect_cstar(ang, gamma, sign, lo, hi, tol=2e-6, t_max=60.0, cutoff=0.002):
    """Absolute classifier (S1 convention): TERM iff min f reaches cutoff."""
    def sealed(c):
        return run_flow(ang, gamma, c, sign=sign, t_max=t_max,
                        cutoff=cutoff, rtol=1e-10, atol=1e-12)['sealed']
    slo, shi = sealed(lo), sealed(hi)
    if slo or not shi:
        return None, (slo, shi)
    while hi - lo > tol:
        mid = 0.5*(lo+hi)
        if sealed(mid): hi = mid
        else:           lo = mid
    return 0.5*(lo+hi), (slo, shi)

# ----------------------------------------------------------------------
# Chebyshev machinery
# ----------------------------------------------------------------------
def cheb(N, T):
    """Chebyshev-Lobatto nodes (ascending, on [0,T]) + diff matrix."""
    j = np.arange(N+1)
    x = np.cos(np.pi*j/N)              # [1..-1]
    c = np.ones(N+1); c[0] = c[-1] = 2.0
    c = c*(-1.0)**j
    X = np.tile(x, (N+1, 1)).T
    dX = X - X.T + np.eye(N+1)
    D = np.outer(c, 1/c)/dX
    D -= np.diag(D.sum(axis=1))
    # map to [0,T] ascending: t = T(1-x)/2
    t = T*(1-x)/2
    D = -2.0/T*D
    idx = np.argsort(t)
    return t[idx], D[np.ix_(idx, idx)]

# ----------------------------------------------------------------------
# Newton-Chebyshev ODE-BVP (Galerkin in u) — the P2 continuation machine
# ----------------------------------------------------------------------
class NewtonBVP:
    """Solve X_tt - X_t - sign*2 P_X = 0 on [0,T] with BC rows.
       bc = ('cauchy', X0, V0)  or  ('dirichlet', X0, XT)."""
    def __init__(self, ang, T, Nt, sign=+1, dev=DEV):
        self.ang, self.T, self.Nt, self.sign, self.dev = ang, T, Nt, sign, dev
        t, D = cheb(Nt, T)
        self.t = t
        self.D  = torch.tensor(D, device=dev)
        self.D2 = self.D @ self.D
        self.L = ang.ellmax

    def residual(self, U, bc):
        D, D2, s = self.D, self.D2, self.sign
        R = D2 @ U - D @ U - s*2.0*self.ang.t_gradP(U)
        kind = bc[0]
        if kind == 'cauchy':
            X0, V0 = bc[1], bc[2]
            R[0]  = U[0] - X0
            R[-1] = (self.D @ U)[0] - V0
        else:
            X0, XT = bc[1], bc[2]
            R[0]  = U[0] - X0
            R[-1] = U[-1] - XT
        return R

    def jacobian(self, U, bc):
        Nt1, L1 = self.Nt+1, self.L+1
        A = self.D2 - self.D
        J = torch.kron(A, torch.eye(L1, device=self.dev))
        H = self.ang.t_hessP(U)            # (Nt1, L1, L1)
        for j in range(Nt1):
            J[j*L1:(j+1)*L1, j*L1:(j+1)*L1] -= self.sign*2.0*H[j]
        # BC rows overwrite rows of node 0 and node Nt:
        J[0:L1, :] = 0.0
        J[0:L1, 0:L1] = torch.eye(L1, device=self.dev)
        J[-L1:, :] = 0.0
        if bc[0] == 'cauchy':
            for m in range(L1):
                row = torch.zeros(Nt1*L1, device=self.dev)
                row[m::L1] = self.D[0]
                J[-L1+m] = row
        else:
            J[-L1:, -L1:] = torch.eye(L1, device=self.dev)
        return J

    def solve(self, U0, bc, tol=1e-12, maxit=40, verbose=False):
        U = U0.clone(); nr_prev = np.inf
        for it in range(maxit):
            R = self.residual(U, bc)
            nr = R.norm().item()
            if verbose: print(f"   Newton it {it}: |R| = {nr:.3e}")
            if nr < tol: return U, nr, it, True
            if nr > 0.7*nr_prev and nr < 1e-6:   # conditioning floor reached
                return U, nr, it, True
            nr_prev = nr
            J = self.jacobian(U, bc)
            dU = torch.linalg.solve(J, -R.reshape(-1)).reshape(U.shape)
            lam, nr0 = 1.0, nr
            for _ in range(25):
                Un = U + lam*dU
                if (Un @ self.ang.tY).min() > 1e-8:
                    nrn = self.residual(Un, bc).norm().item()
                    if nrn < nr0: break
                lam *= 0.5
            U = U + lam*dU
        R = self.residual(U, bc)
        return U, R.norm().item(), maxit, R.norm().item() < 1e-9

    # ---- pseudo-arclength continuation hook (parameter = drive c) -------
    def continuation_step(self, U, cpar, gamma, dUdc, dcds, ds, tol=1e-11):
        """One pseudo-arclength step in c. bc = cauchy with V0(c).
           Returns (U_new, c_new, tangent)."""
        L1 = self.L+1
        Upred = U + ds*dUdc*dcds  # crude predictor (tangent normalized below)
        cpred = cpar + ds*dcds
        Uk, ck = Upred.clone(), float(cpred)
        for it in range(30):
            V0 = torch.zeros(L1, device=self.dev); V0[0] = gamma; V0[1] = -ck
            X0 = torch.zeros(L1, device=self.dev); X0[0] = 1.0
            bc = ('cauchy', X0, V0)
            R = self.residual(Uk, bc).reshape(-1)
            arc = (dUdc.reshape(-1) @ (Uk-U).reshape(-1))*dcds + dcds*(ck-cpar) - ds
            Rfull = torch.cat([R, arc.reshape(1)])
            if Rfull.norm().item() < tol: break
            J = self.jacobian(Uk, bc)
            # dR/dc: only the momentum BC row of mode 1 depends on c: d(V0[1])/dc = -1 -> +1 in residual
            dRdc = torch.zeros(len(R), device=self.dev)
            dRdc[-L1+1] = 1.0
            Jfull = torch.zeros(len(R)+1, len(R)+1, device=self.dev)
            Jfull[:-1, :-1] = J; Jfull[:-1, -1] = dRdc
            Jfull[-1, :-1] = dUdc.reshape(-1)*dcds; Jfull[-1, -1] = dcds
            d = torch.linalg.solve(Jfull, -Rfull)
            Uk = Uk + d[:-1].reshape(U.shape); ck = ck + d[-1].item()
        return Uk, ck

# ----------------------------------------------------------------------
# 2D tensor-spectral Newton (Class A elliptic), full theta resolution
# ----------------------------------------------------------------------
class Newton2D:
    """Class A PDE: f_tt - f_t + d_u[(1-u^2) f_u/f] + (1-u^2) f_u^2/(2f^2) = 0
       Chebyshev(t) x Gauss-Legendre(u) collocation; Dirichlet rows in t;
       no u BCs (degenerate operator, GL interior nodes)."""
    def __init__(self, T, Nt, Nu, dev=DEV):
        self.T, self.Nt, self.Nu, self.dev = T, Nt, Nu, dev
        t, Dt = cheb(Nt, T)
        self.t = t
        un, wn = leggauss(Nu)
        self.u = un
        # barycentric differentiation matrix on GL nodes:
        x = un
        w = np.ones(Nu)
        for j in range(Nu):
            w[j] = 1.0/np.prod(x[j]-np.delete(x, j))
        Du = np.zeros((Nu, Nu))
        for i in range(Nu):
            for j in range(Nu):
                if i != j: Du[i, j] = (w[j]/w[i])/(x[i]-x[j])
            Du[i, i] = -Du[i, np.arange(Nu) != i].sum()
        self.Dt  = torch.tensor(Dt, device=dev)
        self.Dt2 = self.Dt @ self.Dt
        self.Du  = torch.tensor(Du, device=dev)
        self.one_m_u2 = torch.tensor(1-un**2, device=dev)

    def residual(self, F, f0, fT):
        Dt, Dt2, Du, m = self.Dt, self.Dt2, self.Du, self.one_m_u2
        Ft  = Dt @ F; Ftt = Dt2 @ F
        Fu  = F @ Du.T
        g   = m*Fu/F
        R = Ftt - Ft + g @ Du.T + m*Fu**2/(2*F**2)
        R[0]  = F[0]  - f0
        R[-1] = F[-1] - fT
        return R

    def jacobian(self, F):
        Nt1, Nu = self.Nt+1, self.Nu
        Dt, Dt2, Du, m = self.Dt, self.Dt2, self.Du, self.one_m_u2
        Fu = F @ Du.T
        Iu = torch.eye(Nu, device=self.dev)
        It = torch.eye(Nt1, device=self.dev)
        J = torch.kron(Dt2 - Dt, Iu)
        # d/dF of  Du(m Fu / F):  Du [ diag(m/F) Du - diag(m Fu/F^2) ]
        # d/dF of  m Fu^2/(2F^2): diag(m Fu/F^2) Du - diag(m Fu^2/F^3)
        for j in range(Nt1):
            a = (m/F[j])
            b = (m*Fu[j]/F[j]**2)
            cdiag = (m*Fu[j]**2/F[j]**3)
            Block = Du @ (a[:, None]*Du - torch.diag(b)) + b[:, None]*Du - torch.diag(cdiag)
            J[j*Nu:(j+1)*Nu, j*Nu:(j+1)*Nu] += Block
        # Dirichlet rows:
        J[0:Nu, :] = 0.0;  J[0:Nu, 0:Nu] = Iu
        J[-Nu:, :] = 0.0;  J[-Nu:, -Nu:] = Iu
        return J

    def solve(self, F0, f0, fT, tol=1e-11, maxit=40, verbose=False):
        F = F0.clone(); nr_prev = np.inf
        for it in range(maxit):
            R = self.residual(F, f0, fT)
            nr = R.norm().item()
            if verbose: print(f"   2D Newton it {it}: |R| = {nr:.3e}", flush=True)
            if nr < tol: return F, nr, it, True
            if nr > 0.7*nr_prev and nr < 1e-6:   # conditioning floor reached
                return F, nr, it, True
            nr_prev = nr
            J = self.jacobian(F)
            dF = torch.linalg.solve(J, -R.reshape(-1)).reshape(F.shape)
            lam = 1.0
            for _ in range(25):
                Fn = F + lam*dF
                if Fn.min() > 1e-8:
                    if self.residual(Fn, f0, fT).norm().item() < nr: break
                lam *= 0.5
            F = F + lam*dF
        R = self.residual(F, f0, fT)
        return F, R.norm().item(), maxit, R.norm().item() < 1e-8

# ----------------------------------------------------------------------
# diagnostics on flows
# ----------------------------------------------------------------------
def Qstar_field(ang, X, V, ugrid=None):
    """Q* = 2 f_t v/(f f_t^2 + v^2), v = sqrt(1-u^2) f_u, on a u grid."""
    if ugrid is None: ugrid = np.linspace(-1, 1, 401)
    Y, Yp = legendre_Y(ang.ellmax, np.clip(ugrid, -1+1e-12, 1-1e-12))
    f, fu, ft = X @ Y, X @ Yp, V @ Y
    v = np.sqrt(np.clip(1-ugrid**2, 0, 1))*fu
    Q = 2*ft*v/(f*ft**2 + v**2 + 1e-300)
    Delta = f*ft**2 - v**2
    return ugrid, Q, Delta, f, ft, v

def kernel_report():
    import sympy as sp
    print("sympy-generated kernels (P_X / P_XX integrands):")
    for k, v in KERNEL_EXPRS.items():
        print(f"   {k} = {v}")

if __name__ == '__main__':
    kernel_report()
