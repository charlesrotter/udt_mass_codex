#!/usr/bin/env python3
"""
em_forcing.py  (OBSERVE; gated)

QUESTION: is the FORCED sigma-ODD matter source (G_tr, G_ttheta of a sealed
nonstationary UDT cell, from fermion_forcing #46) the native GAUGE/EM sector?
I.e. does a vector field A_mu (Maxwell, then Proca) on the UDT background
SUPPLY the forced sigma-ODD time-row source, and does its static limit give
UDT_REBUILD's Coulomb A_t = c0 + Q/r?

We compute, on the SAME nonstationary UDT background used in #46:
  ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dOmega^2  (+ time row arm; for the
  stress-tensor probe we use the DIAGONAL background -- the matter stress on the
  diagonal cell is what must SUPPLY the off-diagonal G; the arm is the geometric
  response, the matter need not itself carry the arm. We test both.)

  1. Maxwell  L = -1/4 F_mn F^mn,  F = dA.
  2. Proca    L = -1/4 F_mn F^mn + 1/2 m^2 A_mu A^mu.
Extract sigma-ODD time-row stress T_tr, T_ttheta.
MATCH against the forced G_tr, G_ttheta structure.
Static limit -> Coulomb check.

DISCIPLINE: do NOT assert Maxwell native; TEST whether the forced structure
selects a closed 2-form F (dF=0) gauge field vs a generic sigma-odd source.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
c, mA = sp.symbols('c m_A', positive=True)  # mA = Proca mass
X = [t, r, th, ph]
n = 4

phi = sp.Function('phi')(r, th)
e_m = sp.exp(-2*phi); e_p = sp.exp(2*phi)

# DIAGONAL UDT background (the cell's settled metric). g^tt g^rr = -1 holds.
g = sp.diag(-e_m*c**2, e_p, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
sqrtmg = sp.sqrt(-g.det())   # = c * r^2 sin(theta)  (phi CANCELS: e^{-phi}*e^{phi}=1)
sqrtmg = sp.simplify(sqrtmg)
print("sqrt(-g) =", sqrtmg, "  (phi-cancellation check)")

def d(e,i): return sp.diff(e, X[i])

# ---- Vector potential A_mu : general sigma-ODD-capable config ----
# A_t even, A_r/A_theta odd under t->-t. Allow t,r,theta dependence (axisymmetric).
At = sp.Function('A_t')(t, r, th)
Ar = sp.Function('A_r')(t, r, th)
Ath = sp.Function('A_th')(t, r, th)
Aph = sp.S(0)                       # axisymmetric, no phi-component for this probe
Alow = [At, Ar, Ath, Aph]

# Field strength F_{mu nu} = d_mu A_nu - d_nu A_mu  (closed 2-form, dF=0 identically)
F = sp.zeros(n)
for mu in range(n):
    for nu in range(n):
        F[mu,nu] = d(Alow[nu], mu) - d(Alow[mu], nu)

# Raise: F^{mu nu} = g^{mu a} g^{nu b} F_{a b}
Fup = sp.zeros(n)
for mu in range(n):
    for nu in range(n):
        s = sp.S(0)
        for a in range(n):
            for b in range(n):
                s += ginv[mu,a]*ginv[nu,b]*F[a,b]
        Fup[mu,nu] = sp.simplify(s)

# F^2 = F_{ab} F^{ab}
F2 = sp.simplify(sum(F[a,b]*Fup[a,b] for a in range(n) for b in range(n)))

# A^2 = A_mu A^mu  (for Proca)
A2 = sp.simplify(sum(ginv[a,b]*Alow[a]*Alow[b] for a in range(n) for b in range(n)))

def Tmaxwell(mu,nu):
    # T_{mu nu} = F_{mu a} F_nu^{ a} - 1/4 g_{mu nu} F^2
    s = sp.S(0)
    for a in range(n):
        for b in range(n):
            s += F[mu,a]*ginv[a,b]*F[nu,b]
    return sp.simplify(s - sp.Rational(1,4)*g[mu,nu]*F2)

def Tproca(mu,nu):
    # add massive piece: + m^2 ( A_mu A_nu - 1/2 g_{mu nu} A^2 )
    extra = mA**2*(Alow[mu]*Alow[nu] - sp.Rational(1,2)*g[mu,nu]*A2)
    return sp.simplify(Tmaxwell(mu,nu) + extra)

print("\n=== MAXWELL stress-tensor TIME-ROW components ===", flush=True)
Ttr_M  = Tmaxwell(0,1)
Ttth_M = Tmaxwell(0,2)
print("T_tr (Maxwell)     =", Ttr_M)
print()
print("T_ttheta (Maxwell) =", Ttth_M)

print("\n=== PROCA stress-tensor TIME-ROW components ===", flush=True)
Ttr_P  = Tproca(0,1)
Ttth_P = Tproca(0,2)
print("T_tr (Proca)     =", Ttr_P)
print()
print("T_ttheta (Proca) =", Ttth_P)

# ---- sigma-parity of the time-row stress ----
# sigma: t->-t. At even; Ar,Ath odd. F_{tr}=d_t A_r - d_r A_t: (odd-thing)_t even?
#  d_t(Ar=odd)=even ; d_r(At=even)=even  -> F_tr is sigma-EVEN.
#  F_{rtheta}=d_r Ath - d_th Ar : odd - odd = sigma-ODD (magnetic-type, time-row partner).
# T_tr ~ F_{t a} F_r^{a}.  Report which terms survive when Ar=Ath=0 (pure electric, A_t only)
# vs when At=0 (pure magnetic/odd potential).
print("\n=== sigma-ODD content test: which potentials feed T_tr, T_ttheta ===", flush=True)

def restrict(expr, keep):
    """keep in {'electric'(At only),'magnetic'(Ar,Ath only)} -> zero the others"""
    reps = {}
    if keep == 'electric':
        for fn in (Ar, Ath):
            for a in expr.atoms(sp.Derivative):
                if a.expr == fn: reps[a]=sp.S(0)
            reps[fn]=sp.S(0)
    elif keep == 'magnetic':
        for a in expr.atoms(sp.Derivative):
            if a.expr == At: reps[a]=sp.S(0)
        reps[At]=sp.S(0)
    return sp.simplify(expr.subs(reps))

for nm, e in [("T_tr Maxwell", Ttr_M), ("T_ttheta Maxwell", Ttth_M)]:
    el = restrict(e, 'electric')
    mg = restrict(e, 'magnetic')
    print(f"{nm}: electric-only(A_t)={el!='0' and el!=0} ; magnetic-only(A_r,A_th)={mg!='0' and mg!=0}")
    print("   electric-only piece :", el)
    print("   magnetic-only piece :", mg)

# ---- STATIC COULOMB LIMIT ----
print("\n=== STATIC limit: pure electric, A_t=f(r) only, source-free Maxwell ===", flush=True)
fr = sp.Function('f')(r)
subs_static = {}
for fn in (Ar, Ath):
    for a in [sp.Derivative(fn, v) for v in X]:
        subs_static[a] = sp.S(0)
    subs_static[fn] = sp.S(0)
# At -> f(r)
At_static = At.subs({}).subs(At, fr) if False else None
# Build F with At=f(r), Ar=Ath=0 directly:
Alow_s = [fr, sp.S(0), sp.S(0), sp.S(0)]
Fs = sp.zeros(n)
for mu in range(n):
    for nu in range(n):
        Fs[mu,nu] = d(Alow_s[nu], mu) - d(Alow_s[mu], nu)
# Source-free Maxwell: D_mu F^{mu nu} = (1/sqrt-g) d_mu( sqrt-g F^{mu nu} ) = 0
Fsup = sp.zeros(n)
for mu in range(n):
    for nu in range(n):
        s = sp.S(0)
        for a in range(n):
            for b in range(n):
                s += ginv[mu,a]*ginv[nu,b]*Fs[a,b]
        Fsup[mu,nu] = sp.simplify(s)
# the t-component eqn (nu=0):
divF0 = sp.simplify( sum(d(sqrtmg*Fsup[mu,0], mu) for mu in range(n)) / sqrtmg )
print("sqrt(-g) F^{r t} =", sp.simplify(sqrtmg*Fsup[1,0]), "  <- phi-cancellation: should be r^2-form, phi GONE")
print("Maxwell eqn (nu=t):  (1/sqrt-g) d_r( sqrt-g F^{r t} ) = 0  =>")
print("   ", sp.Eq(divF0, 0))
sol = sp.dsolve(sp.Eq(divF0, 0), fr)
print("   static A_t solution:", sol)

print("\nDONE_EM")
