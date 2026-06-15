#!/usr/bin/env python3
"""
fermion_forcing2.py  (OBSERVE; lean Einstein-tensor for the nonstationary cell)

Regime under test (the genuinely nonstationary cell):
  - DERIVED static dilation shape: phi = phi(r, theta)   [the cell's settled shape]
  - sigma-ODD TIME ROW switched on: g_tr = A(t,r,theta), g_ttheta = B(t,r,theta)
    [CHOSE: these ARE the nonstationary arm; their t-dependence is what "nonstationary"
     means; A,B declared sigma-ODD per the seal involution]
We compute G_{mu nu} WITHOUT global simplify (too heavy); we simplify ONLY the
time-row components G_tr, G_ttheta and read off their structure and parity.

We then run:
  - FORCING TEST: are G_tr, G_ttheta nonzero when A,B time-dependent? do they vanish
    when A=B=0 (static limit)?
  - which derivatives appear (A_t, B_t, A_r, ...): does the time-row Einstein sector
    carry genuinely time-odd content (terms odd under t->-t with A,B odd)?
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
c = sp.symbols('c', positive=True)
X = [t, r, th, ph]

phi = sp.Function('phi')(r, th)           # DERIVED static shape
A   = sp.Function('A')(t, r, th)          # g_tr  (sigma-ODD time row)
B   = sp.Function('B')(t, r, th)          # g_ttheta (sigma-ODD time row)

e_m = sp.exp(-2*phi); e_p = sp.exp(2*phi)
g = sp.Matrix([
    [-e_m*c**2, A,   B,   0],
    [ A,        e_p, 0,   0],
    [ B,        0,   r**2,0],
    [ 0,        0,   0,   r**2*sp.sin(th)**2],
])
ginv = g.inv()           # exact inverse (kept symbolic)
n = 4
def d(e,i): return sp.diff(e, X[i])

# Christoffel (no simplify; just cancel to keep size sane)
print("Christoffel...", flush=True)
Gam = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for ccc in range(b,n):
            s = sp.S(0)
            for dd in range(n):
                s += ginv[a,dd]*(d(g[dd,b],ccc)+d(g[dd,ccc],b)-d(g[b,ccc],dd))
            s = sp.cancel(sp.together(s/2))
            Gam[a][b][ccc] = s
            Gam[a][ccc][b] = s

def ricci(b, dd):
    s = sp.S(0)
    for a in range(n):
        s += d(Gam[a][b][dd], a) - d(Gam[a][b][a], dd)
        for e in range(n):
            s += Gam[a][a][e]*Gam[e][b][dd] - Gam[a][dd][e]*Gam[e][b][a]
    return sp.cancel(sp.together(s))

# We only need the time-row Einstein components G_tr, G_ttheta.
# G_{mu nu} = Ric_{mu nu} - 1/2 g_{mu nu} R. For off-diagonal (t r),(t theta),
# g_{tr}=A, g_{ttheta}=B are nonzero, so we DO need R there. Compute Ricci fully.
print("Ricci (needed components)...", flush=True)
Ric = sp.zeros(n)
for b in range(n):
    for dd in range(b,n):
        Ric[b,dd] = ricci(b,dd); Ric[dd,b]=Ric[b,dd]

# Ricci scalar
Rs = sp.S(0)
for a in range(n):
    for b in range(n):
        Rs += ginv[a,b]*Ric[a,b]
Rs = sp.cancel(sp.together(Rs))

def Glow(mu,nu):
    return sp.cancel(sp.together(Ric[mu,nu] - sp.Rational(1,2)*g[mu,nu]*Rs))

print("\n=== TIME-ROW EINSTEIN COMPONENTS (nonstationary) ===", flush=True)
Gtr  = Glow(0,1)
Gtth = Glow(0,2)
Gtr_s  = sp.simplify(Gtr)
Gtth_s = sp.simplify(Gtth)
print("G_tr  =", Gtr_s)
print()
print("G_ttheta =", Gtth_s)

# Derivative-content test
At=sp.diff(A,t); Bt=sp.diff(B,t); Att=sp.diff(A,t,2); Btt=sp.diff(B,t,2)
Ar=sp.diff(A,r); Bth=sp.diff(B,th)
for nm,e in [("G_tr",Gtr_s),("G_ttheta",Gtth_s)]:
    print(f"\n{nm}:  has A_t={e.has(At)} B_t={e.has(Bt)} A_tt={e.has(Att)} B_tt={e.has(Btt)}",
          f"A_r={e.has(Ar)} B_th={e.has(Bth)}")

# save srepr text (picklable-safe)
with open('/home/udt-admin/udt_mass_codex/fermion_forcing2_dump.txt','w') as fh:
    fh.write("Gtr = "+sp.srepr(Gtr_s)+"\n\nGtth = "+sp.srepr(Gtth_s)+"\n")
print("dumped srepr.", flush=True)

# STATIC LIMIT: A=B=0 (atom-based, robust)
print("\n=== STATIC LIMIT A=B=0 (all derivs) ===", flush=True)
def kill_all(expr):
    reps = {a: sp.S(0) for a in expr.atoms(sp.Derivative) if a.expr in (A,B)}
    reps[A]=sp.S(0); reps[B]=sp.S(0)
    return sp.simplify(expr.subs(reps))
print("G_tr  (A=B=0) =", kill_all(Gtr_s))
print("G_ttheta (A=B=0) =", kill_all(Gtth_s))

# STATIONARY ARM (A_t=B_t=0, arm nonzero) — atom-based
print("\n=== STATIONARY ARM (all t-derivs of A,B = 0, arm nonzero) ===", flush=True)
def kill_tderiv(expr):
    reps={}
    for a in expr.atoms(sp.Derivative):
        if a.expr in (A,B) and t in [v for (v,_) in a.variable_count]:
            reps[a]=sp.S(0)
    return sp.simplify(expr.subs(reps))
gtr_stat=kill_tderiv(Gtr_s); gtth_stat=kill_tderiv(Gtth_s)
print("G_tr   (A_t=B_t=0):", "ZERO" if gtr_stat==0 else "NONZERO -> stationary arm already sources")
print("G_ttheta (A_t=B_t=0):", "ZERO" if gtth_stat==0 else "NONZERO -> stationary arm already sources")

# LEADING (LINEAR-IN-ARM) PIECE [hypothesis-development linearization, principle 2:
# short-lived, to READ the leading source structure; NOT a stated result]
print("\n=== LEADING LINEAR-IN-ARM PIECE [hypothesis-development only] ===", flush=True)
eps=sp.symbols('eps', positive=True)
def lin(expr):
    e=expr.subs({A:eps*A, B:eps*B})
    return sp.simplify(sp.series(e, eps, 0, 2).removeO().coeff(eps,1))
Ltr=lin(Gtr_s); Ltth=lin(Gtth_s)
print("G_tr  (linear) =", Ltr)
print()
print("G_ttheta (linear) =", Ltth)
for nm,e in [("G_tr lin",Ltr),("G_ttheta lin",Ltth)]:
    td=sorted([str(a) for a in e.atoms(sp.Derivative)
               if a.expr in (A,B) and t in [v for (v,_) in a.variable_count]])
    print(f"{nm}: surviving time-deriv terms:", td)
with open('/home/udt-admin/udt_mass_codex/fermion_forcing2_lin.txt','w') as fh:
    fh.write("Ltr = "+sp.srepr(Ltr)+"\n\nLtth = "+sp.srepr(Ltth)+"\n")
print("\nDONE2")
