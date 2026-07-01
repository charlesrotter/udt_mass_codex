"""
BLIND ADVERSARIAL VERIFIER — independent Einstein tensor of the
nonstationary UDT cell. Written from scratch; does NOT import or run the
authored scripts. Agent: verifier-2026-06-14.

Metric (lower):
  g = [ -e^{-2phi}c^2   A            B          0          ]
      [  A              e^{2phi}     0          0          ]
      [  B              0            r^2        0          ]
      [  0              0            0    r^2 sin^2(theta) ]
with phi = phi(t,r,theta) GENERAL (we will specialize), A=g_tr(t,r,theta),
B=g_ttheta(t,r,theta).

We compute the FULL lower Einstein tensor G_{mu nu} exactly via
Christoffel -> Riemann -> Ricci -> R -> G = Ric - 1/2 g R.
"""
import sympy as sp

t, r, th, ph, c = sp.symbols('t r theta phi_coord c', real=True)
coords = [t, r, th, ph]

def build_and_report(phi_func_kind):
    # phi, A, B as functions
    if phi_func_kind == 'static':
        phi = sp.Function('phi')(r, th)
    elif phi_func_kind == 'timedep':
        phi = sp.Function('phi')(t, r, th)
    A = sp.Function('A')(t, r, th)
    B = sp.Function('B')(t, r, th)

    g = sp.Matrix([
        [-sp.exp(-2*phi)*c**2, A, B, 0],
        [A, sp.exp(2*phi), 0, 0],
        [B, 0, r**2, 0],
        [0, 0, 0, r**2*sp.sin(th)**2],
    ])
    ginv = g.inv()
    n = 4

    # Christoffel symbols of the second kind
    Gamma = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    dg = [[[sp.diff(g[a, b], coords[cc]) for cc in range(n)] for b in range(n)] for a in range(n)]
    for l in range(n):
        for i in range(n):
            for j in range(n):
                s = sp.S(0)
                for m in range(n):
                    s += ginv[l, m]*(dg[m][i][j] + dg[m][j][i] - dg[i][j][m])
                Gamma[l][i][j] = sp.simplify(s/2)

    # Ricci tensor R_{ij} = d_l Gamma^l_{ij} - d_j Gamma^l_{il}
    #                       + Gamma^l_{lm}Gamma^m_{ij} - Gamma^l_{jm}Gamma^m_{il}
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

    Rscalar = sp.S(0)
    for i in range(n):
        for j in range(n):
            Rscalar += ginv[i, j]*Ric[i, j]

    G = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            G[i, j] = Ric[i, j] - sp.Rational(1, 2)*g[i, j]*Rscalar

    return phi, A, B, g, ginv, Gamma, Ric, Rscalar, G

if __name__ == '__main__':
    import sys
    kind = sys.argv[1] if len(sys.argv) > 1 else 'static'
    phi, A, B, g, ginv, Gamma, Ric, Rscalar, G = build_and_report(kind)
    print("=== phi kind:", kind, "===")
    # G_tr = G[0,1], G_ttheta = G[0,2]
    G_tr = G[0, 1]
    G_tth = G[0, 2]

    # --- Static limit: arm A=B=0 and all derivatives ---
    subs_static = {}
    # substitute A,B and ALL their derivatives by zero: easiest via replacing functions by 0
    G_tr_static = G_tr.subs({A: 0, B: 0})
    G_tth_static = G_tth.subs({A: 0, B: 0})
    # also kill derivatives explicitly
    def kill_arm(expr):
        e = expr
        for f in (A, B):
            for d in e.atoms(sp.Derivative):
                if d.expr == f:
                    e = e.subs(d, 0)
            e = e.subs(f, 0)
        return sp.simplify(e)
    G_tr_static = kill_arm(G_tr)
    G_tth_static = kill_arm(G_tth)
    print("STATIC LIMIT (arm=0):")
    print("  G_tr     =", G_tr_static)
    print("  G_ttheta =", G_tth_static)

    # --- Derivative content of full G_tr, G_tth ---
    def has_deriv(expr, f, varlist):
        for d in expr.atoms(sp.Derivative):
            if d.expr == f:
                dvars = [v for v, _ in d.variable_count]
                if set(dvars) == set(varlist):
                    return True
        return False
    print("DERIV CONTENT (full):")
    print("  G_tr  has A_t:", has_deriv(G_tr, A, [t]), " B_t:", has_deriv(G_tr, B, [t]),
          " A_tt:", has_deriv(G_tr, A, [t, t]), " B_tt:", has_deriv(G_tr, B, [t, t]))
    print("  G_tth has A_t:", has_deriv(G_tth, A, [t]), " B_t:", has_deriv(G_tth, B, [t]),
          " A_tt:", has_deriv(G_tth, A, [t, t]), " B_tt:", has_deriv(G_tth, B, [t, t]))

    # whether nonzero generically: substitute a concrete nonzero arm
    print("Nonzero-generic check done in numeric script.")
