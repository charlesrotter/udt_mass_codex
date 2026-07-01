"""
Does the ARM forcing of G_tr,G_ttheta SURVIVE with time-dependent phi?
And the parity bookkeeping at the seal.

Strategy: compute G_tr, G_ttheta with phi=phi(t,r,th) AND arm A,B present.
Then specialize to the SEAL t=0 under the seal involution sigma:t->-t with
  phi EVEN  (phi(-t)=phi(t))  => odd t-derivs vanish at t=0: phi_t, phi_tr, phi_tth, phi_ttt = 0
  A,B ODD   (A(-t)=-A(t))     => even t-derivs vanish at t=0: A, A_tt, A_r? no:
     A odd in t: A(0)=0, A_tt(0)=0, but A_t(0)!=0, A_r(0)=d_r A(0)=0 (since A(0)=0 for all r => A_r(0)=0!).
   Careful: A(t,r,th) odd in t => A(0,r,th)=0 for ALL r,th => A_r(0)=0, A_th(0)=0, A_rr(0)=0...
            A_t(0)!=0 (generic), A_ttt(0)!=0.
We substitute these seal conditions and see what survives in G_tr, G_ttheta AT THE SEAL.
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
                s = sum(ginv[l, m]*(dg[m][i][j] + dg[m][j][i] - dg[i][j][m]) for m in range(n))
                Gamma[l][i][j] = s/2
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            term = sp.S(0)
            for l in range(n):
                term += sp.diff(Gamma[l][i][j], coords[l]) - sp.diff(Gamma[l][i][l], coords[j])
                for m in range(n):
                    term += Gamma[l][l][m]*Gamma[m][i][j] - Gamma[l][j][m]*Gamma[m][i][l]
            Ric[i, j] = term
    Rs = sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))
    G = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            G[i, j] = Ric[i, j] - sp.Rational(1, 2)*g[i, j]*Rs
    return G

phi = sp.Function('phi')(t, r, th)
A = sp.Function('A')(t, r, th)
B = sp.Function('B')(t, r, th)
print("Computing full G with phi(t,r,th), A,B(t,r,th) ... (may take a bit)")
G = einstein_lower(phi, A, B)
Gtr = G[0, 1]
Gtth = G[0, 2]

# Seal substitutions: t=0, phi even, A,B odd.
def D(f, *vs): return sp.Derivative(f, *vs)

# All ODD-in-t derivatives of phi (even fn) vanish at t=0:
even_kill = {D(phi, t): 0, D(phi, t, r): 0, D(phi, t, th): 0,
             D(phi, t, t, t): 0, D(phi, t, r, r): 0, D(phi, t, th, th): 0,
             D(phi, t, r, th): 0}
# A,B odd in t => A(0)=0 for all (r,th): A and all its PURELY-SPATIAL and EVEN-t derivs vanish at t=0:
odd_kill = {}
for f in (A, B):
    odd_kill[f] = 0
    odd_kill[D(f, r)] = 0
    odd_kill[D(f, th)] = 0
    odd_kill[D(f, r, r)] = 0
    odd_kill[D(f, th, th)] = 0
    odd_kill[D(f, r, th)] = 0
    odd_kill[D(f, t, t)] = 0          # even # of t derivs of odd fn -> odd -> 0 at t=0
    odd_kill[D(f, t, t, r)] = 0
    odd_kill[D(f, t, t, th)] = 0
    # SURVIVES at seal: D(f,t), D(f,t,r), D(f,t,th), D(f,t,t,t) (odd # t-derivs)

seal = {**even_kill, **odd_kill}
Gtr_seal = sp.simplify(Gtr.subs(seal))
Gtth_seal = sp.simplify(Gtth.subs(seal))
print("\n=== AT THE SEAL t=0 (phi even, arm odd) ===")
print("G_tr     |seal =", Gtr_seal)
print("G_ttheta |seal =", Gtth_seal)

# Now: at the seal, is G_tr driven by the ARM's velocity A_t, B_t (the surviving odd-t derivs)?
print("\nSurviving derivative atoms in G_tr|seal:")
for d in sorted(Gtr_seal.atoms(sp.Derivative), key=str):
    print("   ", d)
print("Surviving derivative atoms in G_ttheta|seal:")
for d in sorted(Gtth_seal.atoms(sp.Derivative), key=str):
    print("   ", d)

# Is G_tr|seal nonzero when A_t,B_t != 0?  set A_t,B_t to nonzero symbols
At, Bt = sp.symbols('At Bt', real=True)
test = Gtr_seal.subs({D(A, t): At, D(B, t): Bt})
print("\nG_tr|seal as fn of A_t,B_t (subset):", sp.simplify(test))
