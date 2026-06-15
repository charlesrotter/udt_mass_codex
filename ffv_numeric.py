"""
FULLY INDEPENDENT numeric finite-difference Einstein tensor.
Different code path from sympy: build g(x) numerically, finite-difference
the metric to get Christoffel, Riemann, Ricci, G. float64.
Agent: verifier-2026-06-14.

Tests:
  - static arm => G_tr, G_ttheta ~ 0
  - stationary nonzero arm => G_tr, G_ttheta nonzero
  - time-dependent arm + STATIC phi => nonzero, shifted
  - time-dependent arm + TIME-DEPENDENT phi => does forcing SURVIVE? (P4 attack)
  - can a time-dependent EVEN phi alone (arm=0) produce G_tr? (must be 0 by parity)
"""
import numpy as np

c = 1.3  # arbitrary nonzero speed

def make_metric(phi_f, A_f, B_f):
    def g(x):
        t, r, th, ph = x
        phi = phi_f(t, r, th)
        A = A_f(t, r, th)
        B = B_f(t, r, th)
        m = np.zeros((4, 4))
        m[0, 0] = -np.exp(-2*phi)*c**2
        m[1, 1] = np.exp(2*phi)
        m[2, 2] = r**2
        m[3, 3] = r**2*np.sin(th)**2
        m[0, 1] = m[1, 0] = A
        m[0, 2] = m[2, 0] = B
        return m
    return g

def einstein_lower(g, x, h=1e-4):
    n = 4
    G0 = g(x)
    Ginv = np.linalg.inv(G0)
    # first derivatives of metric: dg[k][i][j] = d_k g_ij
    dg = np.zeros((n, n, n))
    for k in range(n):
        xp = np.array(x, float); xp[k] += h
        xm = np.array(x, float); xm[k] -= h
        dg[k] = (g(xp) - g(xm))/(2*h)
    # second derivatives ddg[k][l][i][j] = d_k d_l g_ij
    ddg = np.zeros((n, n, n, n))
    for k in range(n):
        for l in range(n):
            xpp = np.array(x, float); xpp[k] += h; xpp[l] += h
            xpm = np.array(x, float); xpm[k] += h; xpm[l] -= h
            xmp = np.array(x, float); xmp[k] -= h; xmp[l] += h
            xmm = np.array(x, float); xmm[k] -= h; xmm[l] -= h
            ddg[k, l] = (g(xpp) - g(xpm) - g(xmp) + g(xmm))/(4*h*h)
    # Christoffel Gamma^l_{ij}
    Gamma = np.zeros((n, n, n))
    for l in range(n):
        for i in range(n):
            for j in range(n):
                s = 0.0
                for m in range(n):
                    s += Ginv[l, m]*(dg[i][m][j] + dg[j][m][i] - dg[m][i][j])
                Gamma[l, i, j] = 0.5*s
    # dGamma^l_{ij} / dx^k  via finite difference of Christoffel
    def gamma_at(xx):
        Gx = g(xx); Gix = np.linalg.inv(Gx)
        dgx = np.zeros((n, n, n))
        for k in range(n):
            xp = np.array(xx, float); xp[k] += h
            xm = np.array(xx, float); xm[k] -= h
            dgx[k] = (g(xp) - g(xm))/(2*h)
        Gam = np.zeros((n, n, n))
        for l in range(n):
            for i in range(n):
                for j in range(n):
                    s = 0.0
                    for m in range(n):
                        s += Gix[l, m]*(dgx[i][m][j] + dgx[j][m][i] - dgx[m][i][j])
                    Gam[l, i, j] = 0.5*s
        return Gam
    dGamma = np.zeros((n, n, n, n))  # dGamma[k][l][i][j] = d_k Gamma^l_{ij}
    for k in range(n):
        xp = np.array(x, float); xp[k] += h
        xm = np.array(x, float); xm[k] -= h
        dGamma[k] = (gamma_at(xp) - gamma_at(xm))/(2*h)
    # Ricci R_{ij} = d_l Gamma^l_{ij} - d_j Gamma^l_{il} + Gamma^l_{lm}Gamma^m_{ij} - Gamma^l_{jm}Gamma^m_{il}
    Ric = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            term = 0.0
            for l in range(n):
                term += dGamma[l][l][i][j]
                term -= dGamma[j][l][i][l]
                for m in range(n):
                    term += Gamma[l][l][m]*Gamma[m][i][j]
                    term -= Gamma[l][j][m]*Gamma[m][i][l]
            Ric[i, j] = term
    Rs = 0.0
    for i in range(n):
        for j in range(n):
            Rs += Ginv[i, j]*Ric[i, j]
    Glow = Ric - 0.5*G0*Rs
    return Glow

X = (0.4, 1.4, 0.6, 0.25)

def run(name, phi_f, A_f, B_f):
    g = make_metric(phi_f, A_f, B_f)
    Glow = einstein_lower(g, X)
    print(f"{name:42s}  G_tr={Glow[0,1]: .6e}  G_ttheta={Glow[0,2]: .6e}")
    return Glow

# static even dilation shape
phi_static = lambda t, r, th: 0.3*np.cos(th)*r
phi_td_even = lambda t, r, th: 0.3*np.cos(th)*r*(1 + 0.4*np.cos(1.7*t))  # EVEN in t (cos)
zero = lambda t, r, th: 0.0

# arms: ODD in t means A(-t)=-A(t). sin(omega t) is odd. We use generic functions for the
# *value* test (need not be exactly odd to test G nonzero), and odd ones for parity tests.
A_stat = lambda t, r, th: 0.12*np.sin(r)*np.cos(th)         # stationary (no t) arm
B_stat = lambda t, r, th: -0.20*np.cos(r)*np.sin(th)
A_td = lambda t, r, th: 0.12*np.sin(r)*np.cos(th)*np.sin(1.1*t)  # ODD in t
B_td = lambda t, r, th: -0.20*np.cos(r)*np.sin(th)*np.sin(0.9*t)

print("=== INDEPENDENT NUMERIC EINSTEIN (finite-diff, c=%.2f) at x=%s ===" % (c, X))
run("STATIC (arm=0, phi static)", phi_static, zero, zero)
run("STATIONARY nonzero arm, phi static", phi_static, A_stat, B_stat)
run("TIME-DEP arm (odd), phi static", phi_static, A_td, B_td)
print("--- P4 ATTACK: TIME-DEPENDENT EVEN phi ---")
run("STATIC arm(=0), phi TIME-DEP even", phi_td_even, zero, zero)
run("STATIONARY arm, phi TIME-DEP even", phi_td_even, A_stat, B_stat)
run("TIME-DEP arm (odd), phi TIME-DEP even", phi_td_even, A_td, B_td)
print("--- extra: does time-dep even phi with arm=0 give ANY G_tr? (should be 0 by parity at t=0; here t=0.4) ---")
# evaluate at t=0 (the seal/fixed surface) where even phi has phi_t=0
X0 = (0.0, 1.4, 0.6, 0.25)
g = make_metric(phi_td_even, zero, zero)
G0 = einstein_lower(g, X0)
print(f"  at SEAL t=0, arm=0, phi td-even:  G_tr={G0[0,1]: .3e}  G_ttheta={G0[0,2]: .3e}")
