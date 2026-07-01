"""
INDEPENDENT blind verifier for em_forcing_results.md.
Re-derives Maxwell/Proca stress on the UDT background from first principles.
Does NOT read or run em_forcing.py / em_forcing2.py.

UDT metric: ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
sigma = (t -> -t).  A_t even ; A_r, A_theta odd.
"""
import sympy as sp

t, r, th, ph, c = sp.symbols('t r theta phi_ang c', real=True)
phi = sp.Function('phi')(t, r, th)   # general phi(t,r,theta) so nothing is smuggled
m = sp.symbols('m', real=True)       # Proca mass

# coords order: t, r, theta, phi
x = [t, r, th, ph]

# metric (lower)
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
detg = sp.simplify(g.det())
sqrtmg = sp.sqrt(-detg)

print("=== metric check ===")
print("g^tt g^rr =", sp.simplify(ginv[0,0]*ginv[1,1]))   # expect -1/c^2  (with c). Their claim: -1 in c=1 units
print("sqrt(-g) =", sp.simplify(sqrtmg))

# Vector potential (covariant), axisymmetric: A_phi = 0, depend on (t,r,theta)
At = sp.Function('A_t')(t, r, th)
Ar = sp.Function('A_r')(t, r, th)
Ath = sp.Function('A_th')(t, r, th)
A = [At, Ar, Ath, sp.Integer(0)]

# Field strength F_{mu nu} = d_mu A_nu - d_nu A_mu
F = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        F[mu, nu] = sp.diff(A[nu], x[mu]) - sp.diff(A[mu], x[nu])

# Raise both indices: F^{ab} = g^{a mu} g^{b nu} F_{mu nu}
Fup = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        s = 0
        for mu in range(4):
            for nu in range(4):
                s += ginv[a, mu]*ginv[b, nu]*F[mu, nu]
        Fup[a, b] = sp.simplify(s)

# F_{mu}^{ alpha} = g^{alpha beta} F_{mu beta}  (one index up)
Fmixed = sp.zeros(4, 4)
for mu in range(4):
    for al in range(4):
        s = 0
        for be in range(4):
            s += ginv[al, be]*F[mu, be]
        Fmixed[mu, al] = s

# F^2 = F_{ab} F^{ab}
F2 = 0
for a in range(4):
    for b in range(4):
        F2 += F[a, b]*Fup[a, b]
F2 = sp.simplify(F2)

# Maxwell stress (lower indices):
# T_{mu nu} = F_{mu alpha} F_nu^{ alpha} - 1/4 g_{mu nu} F^2
# (with L = -1/4 F^2 convention; sign of overall T is convention but ratios/zeros invariant)
def maxwell_T(mu, nu):
    s = 0
    for al in range(4):
        s += Fmixed[mu, al]*F[nu, al]
    return sp.simplify(s - sp.Rational(1, 4)*g[mu, nu]*F2)

print("\n=== MAXWELL time-row stress (general A, general phi) ===")
T_tr = maxwell_T(0, 1)
T_tth = maxwell_T(0, 2)
print("T_tr     =", sp.simplify(T_tr))
print("T_ttheta =", sp.simplify(T_tth))
