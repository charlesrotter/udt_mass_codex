"""
RESCUE B+C (independent): breathing/fluctuation Hessian spectrum about the
ground soliton, flat phi=0, and Koide Q under three readings.

Energy E[Theta] = int [ a(r,Th) Th'^2 + b(r,Th) ] dr, a,b as derived (xi=kap=1).
Second variation about ground Th0(r):  delta^2 E = int [ P u'^2 + (2 Q u' u? ) ...]
For E = int F(r,Th,Th') dr, the second variation is
  delta^2E = int [ F_{Th'Th'} u'^2 + 2 F_{ThTh'} u u' + F_{ThTh} u^2 ] dr
Here F = a Th'^2 + b, so
  F_{Th'} = 2 a Th',   F_{Th'Th'} = 2 a
  F_{ThTh'} = 2 a_Th Th'
  F_{ThTh} = a_ThTh Th'^2 + b_ThTh
So  H operator (Sturm-Liouville): -(d/dr)(2a u') + [F_{ThTh} - d/dr(2 a_Th Th')] u = lambda W u
The 2 F_{ThTh'} u u' term integrates by parts into the potential:
  int 2 F_{ThTh'} u u' = int F_{ThTh'} (u^2)' = -int (F_{ThTh'})' u^2   (Dirichlet ends)
=> potential  V = F_{ThTh} - d/dr(F_{ThTh'}) = a_ThTh Th'^2 + b_ThTh - d/dr(2 a_Th Th')
Breathing weight W ~ e^{3phi} r^2 (time-kinetic, flat=> r^2). We test BOTH W=r^2
and the doc's e^{3phi} r^2 (flat identical) and also a plain W=1 sensitivity.
Generalized eigenproblem H u = omega^2 W u, Dirichlet u(core)=u(seal)=0.

agent: blind-verifier 2026-06-14
"""
import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import eigh
import sympy as sp

# symbolic a,b (flat phi=0): set p=0
r_s, Th_s = sp.symbols('r Th', real=True)
TWO_PI_3 = 2*sp.pi/3
S = sp.sin(Th_s)
a_sym = TWO_PI_3*(r_s**2*S**2 + 2*r_s**2 + 2*S**4 + 2*S**2)            # p=0
b_sym = TWO_PI_3*(4*S**2 + S**4/r_s**2)                                 # p=0, e^{2phi}=1
a_Th = sp.diff(a_sym, Th_s); a_ThTh = sp.diff(a_Th, Th_s)
b_ThTh = sp.diff(b_sym, Th_s, 2)
af = sp.lambdify((r_s, Th_s), a_sym, 'numpy')
bf = sp.lambdify((r_s, Th_s), b_sym, 'numpy')
aThf = sp.lambdify((r_s, Th_s), a_Th, 'numpy')
aThThf = sp.lambdify((r_s, Th_s), a_ThTh, 'numpy')
bThThf = sp.lambdify((r_s, Th_s), b_ThTh, 'numpy')
# EOM for ground state (flat): Th'' = (a_Th Th'^2 + b_Th - 2 a_Th Th'^2 ... ) see below
b_Th = sp.diff(b_sym, Th_s)
a_r = sp.diff(a_sym, r_s)
bThf = sp.lambdify((r_s, Th_s), b_Th, 'numpy')
a_rf = sp.lambdify((r_s, Th_s), a_r, 'numpy')

def ground(r_core=0.05, cellL=14.0, N=6000):
    r_int = r_core+cellL
    x = np.linspace(r_core, r_int, N)
    def rhs(r, y):
        Th, Thp = y
        a = af(r, Th); aTh = aThf(r, Th); bTh = bThf(r, Th)
        dadr = a_rf(r, Th) + aTh*Thp
        Thpp = (aTh*Thp**2 + bTh - 2*dadr*Thp)/(2*a)
        return np.vstack([Thp, Thpp])
    def bc(ya, yb): return np.array([ya[0]-np.pi, yb[0]])
    frac = (x-r_core)/cellL
    Th0 = np.pi*(1-frac)
    sol = solve_bvp(rhs, bc, x, np.vstack([Th0, np.gradient(Th0, x)]), tol=1e-9, max_nodes=200000)
    return sol, r_int

def hessian_spectrum(sol, r_int, Nfd=3000, Wkind='r2'):
    r_core = sol.x[0]
    x = np.linspace(r_core, r_int, Nfd)
    dx = x[1]-x[0]
    Th = sol.sol(x)[0]; Thp = sol.sol(x)[1]
    P = 2*af(x, Th)                                  # coefficient of u'^2
    # potential V = a_ThTh Th'^2 + b_ThTh - d/dr(2 a_Th Th')
    FThTh_prime = np.gradient(2*aThf(x, Th)*Thp, x)
    V = aThThf(x, Th)*Thp**2 + bThThf(x, Th) - FThTh_prime
    if Wkind == 'r2':
        W = x**2
    elif Wkind == 'one':
        W = np.ones_like(x)
    elif Wkind == 'r2e3phi':   # flat phi -> same as r2
        W = x**2
    # interior nodes (Dirichlet): indices 1..Nfd-2
    n = Nfd-2
    # build H (symmetric) for -(d/dr)(P u') + V u  with FD, and W diagonal
    main = np.zeros(n); lower = np.zeros(n-1)
    Phalf = 0.5*(P[:-1]+P[1:])   # P at half points, length Nfd-1; Phalf[i] between x[i],x[i+1]
    for i in range(n):
        gi = i+1   # grid index
        main[i] = (Phalf[gi-1]+Phalf[gi])/dx**2 + V[gi]
    for i in range(n-1):
        gi = i+1
        lower[i] = -Phalf[gi]/dx**2
    H = np.diag(main) + np.diag(lower, 1) + np.diag(lower, -1)
    Wd = W[1:-1]
    # generalized symmetric: H u = omega^2 W u  -> scale by 1/sqrt(W)
    sW = 1.0/np.sqrt(Wd)
    Hn = (H * sW[:, None]) * sW[None, :]
    w = np.linalg.eigvalsh(Hn)
    return np.sort(w)

def koide(E):
    E = np.array(E[:3], float)
    return (E.sum())/(np.sqrt(E).sum())**2

if __name__ == '__main__':
    sol, r_int = ground()
    print("ground converged:", sol.success, " E0-check width:",
          "(rms resid %.1e)" % np.sqrt(np.mean(sol.rms_residuals**2)))
    for Wkind in ['r2', 'one']:
        w = hessian_spectrum(sol, r_int, Wkind=Wkind)
        omega2 = w[:6]
        print(f"\nW={Wkind}: omega^2 (lowest 6) =", np.round(omega2, 5))
        print("           omega         =", np.round(np.sqrt(np.abs(omega2)), 5))
        n_neg = np.sum(omega2 < -1e-8)
        print("           negative modes:", n_neg, "(0 => stable)")
        # spacing: linear fit omega2 vs n, and exp fit log(omega) vs n
        n = np.arange(len(omega2))
        clin = np.polyfit(n, omega2, 1)
        cexp = np.polyfit(n, np.log(np.sqrt(np.abs(omega2))), 1)
        print(f"           linear fit omega2 ~ {clin[1]:.3f} + {clin[0]:.3f} n ; "
              f"exp-fit slope c={cexp[0]:.3f} (e^c={np.exp(cexp[0]):.3f}/level)")
        # Koide three readings using lowest 3
        om = np.sqrt(np.abs(omega2))
        Esol = 45.607
        QA = koide([Esol+om[0], Esol+om[1], Esol+om[2]])
        QB = koide([omega2[0], omega2[1], omega2[2]])
        QC = koide([om[0], om[1], om[2]])
        print(f"           Koide  A(soliton+omega)={QA:.5f}  B(omega^2)={QB:.5f}  C(omega)={QC:.5f}")
        print(f"           R1,R2  A:{(Esol+om[1])/(Esol+om[0]):.4f},{(Esol+om[2])/(Esol+om[0]):.4f}"
              f"  B:{omega2[1]/omega2[0]:.4f},{omega2[2]/omega2[0]:.4f}"
              f"  C:{om[1]/om[0]:.4f},{om[2]/om[0]:.4f}")
