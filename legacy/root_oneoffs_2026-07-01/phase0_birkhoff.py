#!/usr/bin/env python3
"""
phase0_birkhoff.py -- Phase-0 (A): BANK BIRKHOFF for the held UDT round/diagonal
time-dependent metric, source-free (vacuum, T_munu=0).

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A.
Frame: time_live_bare_solve_DESIGN.md (RED-TEAM-REVISIONS #1, PHASE-0 (a)).

Metric (round, diagonal, TIME-DEPENDENT dilation; C-2026-06-18-1 held form):
  ds^2 = -e^{-2 phi(t,r)} c^2 dt^2 + e^{2 phi(t,r)} dr^2 + r^2 dOmega^2.

Goal:
 (A.i) compute Einstein tensor exactly (sympy), report the OFF-DIAGONAL G_{tr}
       (mixed and lowered) and confirm it is proportional to d_t(phi):
       vacuum G_tr=0 => d_t phi = 0 => STATIC (Birkhoff).
 (A.ii) confirm the UDT tie g_tt g_rr = -c^2 is IDENTICAL to Schwarzschild AB=1.
 Cross-check G_tr a second way (independent metric functions A,B with A*B=c^2).
"""
import sympy as sp

t, r, th, ph, c = sp.symbols('t r theta phi_ang c', positive=True)
phi = sp.Function('phi')(t, r)

# ---------------------------------------------------------------------------
# Build the held UDT round/diagonal time-dependent metric.
# ---------------------------------------------------------------------------
gtt = -sp.exp(-2*phi) * c**2
grr =  sp.exp(2*phi)
gthth = r**2
gpp = r**2 * sp.sin(th)**2

X = [t, r, th, ph]
g = sp.diag(gtt, grr, gthth, gpp)
ginv = g.inv()


def einstein_tensor(g, ginv, X):
    n = len(X)
    # Christoffel Gamma^a_{bc}
    Gamma = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cidx in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, cidx], X[b])
                                     + sp.diff(g[d, b], X[cidx])
                                     - sp.diff(g[b, cidx], X[d]))
                Gamma[a][b][cidx] = sp.simplify(sp.Rational(1, 2)*s)
    # Ricci R_{bd} = d_a G^a_{bd} - d_d G^a_{ba} + G^a_{ae}G^e_{bd} - G^a_{de}G^e_{ba}
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], X[a]) - sp.diff(Gamma[a][b][a], X[d])
                for e in range(n):
                    s += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
            Ric[b, d] = sp.simplify(s)
    Rscal = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n)))
    G = sp.zeros(n, n)
    for mu in range(n):
        for nu in range(n):
            G[mu, nu] = sp.simplify(Ric[mu, nu] - sp.Rational(1, 2)*g[mu, nu]*Rscal)
    return G, Ric, Rscal


print("=== (A) Birkhoff for held UDT round/diagonal TIME-DEPENDENT metric ===")
G, Ric, Rscal = einstein_tensor(g, ginv, X)

Gtr = sp.simplify(G[0, 1])         # lowered G_{t r}
print("\nG_{t r} (lowered) =", Gtr)

# mixed G^t_r = g^{tt} G_{t r}
Gt_r = sp.simplify(ginv[0, 0]*G[0, 1])
print("G^t_r (mixed)     =", Gt_r)

dtphi = sp.diff(phi, t)
ratio = sp.simplify(Gtr / dtphi)
print("\nG_{t r} / d_t(phi) =", ratio, "   <-- proportionality to d_t phi")

# Red-team expected G_tr = 2 d_t phi / r  -- check the MIXED/either form matches.
target = 2*dtphi/r
print("\nDoes G_{t r}     == 2 d_t phi / r ? ",
      sp.simplify(Gtr - target) == 0)
print("Does G^t_r       == 2 d_t phi / r ? ",
      sp.simplify(Gt_r - target) == 0)
print("Does -G^t_r      == 2 d_t phi / r ? ",
      sp.simplify(-Gt_r - target) == 0)

# GATE (i) cross-check: independent metric functions A(t,r), B(t,r), tie A*B=c^2.
print("\n--- Cross-check #2: independent A(t,r),B(t,r), generic (tie imposed after) ---")
A = sp.Function('A')(t, r)   # plays role of -g_tt / c^2 -> here use g_tt=-A, g_rr=B
B = sp.Function('B')(t, r)
g2 = sp.diag(-A, B, r**2, r**2*sp.sin(th)**2)
ginv2 = g2.inv()
G2, _, _ = einstein_tensor(g2, ginv2, X)
Gtr2 = sp.simplify(G2[0, 1])
print("Generic G_{t r}(A,B) =", Gtr2)
# This is the standard Schwarzschild-derivation result: G_{t r} = - d_t B /(r B) (form).
# Now impose the UDT/Schwarzschild tie A*B = c^2  i.e. B = c^2 / A:
Gtr2_tie = sp.simplify(Gtr2.subs(B, c**2/A).doit())
Gtr2_tie = sp.simplify(Gtr2_tie)
print("Under tie A*B=c^2, G_{t r} =", Gtr2_tie)
# express via phi: A = e^{-2phi} c^2  => B = e^{2phi}; check equals 2 d_t phi/r
Gtr2_phi = sp.simplify(Gtr2.subs({A: sp.exp(-2*phi)*c**2, B: sp.exp(2*phi)}).doit())
print("With A=e^{-2phi}c^2, B=e^{2phi}: G_{t r} =", sp.simplify(Gtr2_phi))
print("  == 2 d_t phi / r ? ", sp.simplify(Gtr2_phi - target) == 0)

# GATE (ii): UDT tie == Schwarzschild AB=1.
print("\n=== (A.ii) UDT tie  g_tt g_rr = -c^2  ==  Schwarzschild AB=1 ===")
tie = sp.simplify(gtt*grr)
print("g_tt * g_rr =", tie, "   (== -c^2 exactly:",
      sp.simplify(tie + c**2) == 0, ")")
print("In A,B language (g_tt=-A, g_rr=B): A*B =", sp.simplify(A*B),
      " and the tie sets A*B = c^2  -> with c=1 this is Schwarzschild's A*B=1.")
print("So NO extra DOF: the tie removes exactly the freedom Schwarzschild's AB=1 removes.")

# Show vacuum forces static.
print("\n=== Birkhoff conclusion ===")
print("Vacuum: G_{t r}=0.  G_{t r}=2 d_t phi / r = 0  for r>0  =>  d_t phi = 0.")
print("=> the round + diagonal + vacuum UDT cell is STATIC BY THEOREM (Birkhoff).")
print("Independent of cell size / seal: it is a pointwise momentum-constraint result.")
