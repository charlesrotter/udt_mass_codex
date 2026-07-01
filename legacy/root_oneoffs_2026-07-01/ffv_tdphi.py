"""
P4 ATTACK (exact sympy): time-dependent phi.
1. Compute G_tr, G_ttheta for arm=0 but phi=phi(t,r,theta). Are they zero?
2. Compute them for arm!=0 + phi(t,r,theta). Does the arm-forcing survive?
3. Parity analysis: is phi(t,r,theta) even or odd in t under the seal involution,
   and what does that imply at the seal t=0?
Agent: verifier-2026-06-14.
"""
import sympy as sp

t, r, th, ph, c = sp.symbols('t r theta phi_coord c', real=True)
coords = [t, r, th, ph]

def einstein_lower(phi, A, B):
    g = sp.Matrix([
        [-sp.exp(-2*phi)*c**2, A, B, 0],
        [A, sp.exp(2*phi), 0, 0],
        [B, 0, r**2, 0],
        [0, 0, 0, r**2*sp.sin(th)**2],
    ])
    ginv = g.inv()
    n = 4
    dg = [[[sp.diff(g[a, b], coords[cc]) for cc in range(n)] for b in range(n)] for a in range(n)]
    Gamma = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for i in range(n):
            for j in range(n):
                s = sp.S(0)
                for m in range(n):
                    s += ginv[l, m]*(dg[m][i][j] + dg[m][j][i] - dg[i][j][m])
                Gamma[l][i][j] = s/2
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            term = sp.S(0)
            for l in range(n):
                term += sp.diff(Gamma[l][i][j], coords[l])
                term -= sp.diff(Gamma[l][i][l], coords[j])
                for m in range(n):
                    term += Gamma[l][l][m]*Gamma[m][i][j]
                    term -= Gamma[l][j][m]*Gamma[m][i][l]
            Ric[i, j] = term
    Rs = sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))
    G = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            G[i, j] = Ric[i, j] - sp.Rational(1, 2)*g[i, j]*Rs
    return G

# CASE 1: arm = 0, phi = phi(t,r,theta)
print("=== CASE 1: arm=0, phi=phi(t,r,theta) ===")
phi = sp.Function('phi')(t, r, th)
G = einstein_lower(phi, sp.S(0), sp.S(0))
Gtr = sp.simplify(G[0, 1])
Gtth = sp.simplify(G[0, 2])
print("G_tr     (arm=0, phi td) =", Gtr)
print("G_ttheta (arm=0, phi td) =", Gtth)

# Evaluate G_tr structure: which derivatives of phi?
print("\nG_tr atoms (derivatives):")
for d in sorted(Gtr.atoms(sp.Derivative), key=str):
    print("   ", d)

# CASE 1b: at the SEAL t=0 with phi EVEN in t => phi_t(0)=0. Substitute phi_t->0.
phit = sp.Derivative(phi, t)
print("\n=== CASE 1b: set phi_t=0 (even phi at seal t=0) ===")
Gtr_seal = sp.simplify(Gtr.subs(phit, 0))
Gtth_seal = sp.simplify(Gtth.subs(phit, 0))
# also kill mixed phi_tr, phi_tth? An even-in-t phi at t=0 has odd t-derivatives vanish:
phitr = sp.Derivative(phi, t, r); phitth = sp.Derivative(phi, t, th)
phittt = sp.Derivative(phi, t, t, t)
Gtr_seal = sp.simplify(Gtr_seal.subs({phitr: 0, phitth: 0, phittt: 0}))
Gtth_seal = sp.simplify(Gtth_seal.subs({phitr: 0, phitth: 0, phittt: 0}))
print("G_tr     at seal (phi_t,phi_tr,phi_tth=0) =", Gtr_seal)
print("G_ttheta at seal (phi_t,phi_tr,phi_tth=0) =", Gtth_seal)
