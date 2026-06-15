"""
BOSONIC INSUFFICIENCY (independent): stress of the unit-3-vector winding
field n (hedgehog), minimal S^2 sigma model L2.
  T_{mu nu} = Lambda [ d_mu n . d_nu n  -  1/2 g_{mu nu} (d n)^2 ]
n = (sinTheta cosPhi, sinTheta sinPhi, cosTheta), Theta=Theta(...), Phi=phi_coord(...).
Cases:
 (a) STATIC hedgehog Theta=Theta(r,th), Phi=ph  -> T_tr, T_ttheta = ?
 (b) TIME-DEP EVEN Theta=Theta(t,r,th) even in t -> T_tr at seal t=0?
Agent: verifier-2026-06-14.
"""
import sympy as sp
t, r, th, ph, c = sp.symbols('t r theta phi_coord c', real=True)
coords = [t, r, th, ph]
Lam = sp.symbols('Lambda', positive=True)

def winding_T(Theta, Phi, phi):
    g = sp.Matrix([
        [-sp.exp(-2*phi)*c**2, 0, 0, 0],
        [0, sp.exp(2*phi), 0, 0],
        [0, 0, r**2, 0],
        [0, 0, 0, r**2*sp.sin(th)**2],
    ])
    ginv = g.inv()
    nvec = sp.Matrix([sp.sin(Theta)*sp.cos(Phi),
                      sp.sin(Theta)*sp.sin(Phi),
                      sp.cos(Theta)])
    # d_mu n
    dn = [sp.Matrix([sp.diff(nvec[k], coords[m]) for k in range(3)]) for m in range(4)]
    # (d n)^2 = g^{ab} d_a n . d_b n
    dnsq = sp.S(0)
    for a in range(4):
        for b in range(4):
            dnsq += ginv[a, b]*(dn[a].dot(dn[b]))
    T = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            T[mu, nu] = Lam*(dn[mu].dot(dn[nu]) - sp.Rational(1, 2)*g[mu, nu]*dnsq)
    return T

print("=== (a) STATIC hedgehog ===")
phi = sp.Function('phi')(r, th)
Theta = sp.Function('Theta')(r, th)
T = winding_T(Theta, ph, phi)
print("T_tr     =", sp.simplify(T[0, 1]))
print("T_ttheta =", sp.simplify(T[0, 2]))
print("T_tt     =", sp.simplify(T[0, 0]))
print("T_rr     =", sp.simplify(T[1, 1]))

print("\n=== (b) TIME-DEP winding Theta=Theta(t,r,th) ===")
phi2 = sp.Function('phi')(t, r, th)
Theta2 = sp.Function('Theta')(t, r, th)
T2 = winding_T(Theta2, ph, phi2)
Ttr = sp.simplify(T2[0, 1]); Ttth = sp.simplify(T2[0, 2])
print("T_tr     =", Ttr)
print("T_ttheta =", Ttth)
# at the seal: Theta even in t => Theta_t=0 at t=0
ThT = sp.Derivative(Theta2, t)
print("At seal (Theta_t=0):  T_tr =", sp.simplify(Ttr.subs(ThT, 0)),
      "  T_ttheta =", sp.simplify(Ttth.subs(ThT, 0)))
# Could an ODD-in-t winding (Theta odd) carry T_tr at seal? Theta odd => Theta(0)=0,
# Theta_t(0)!=0, but Theta_r(0)=0. T_tr ~ Theta_t*Theta_r => 0 at seal too.
print("\nIf Theta ODD in t: at seal Theta(0)=0=>Theta_r(0)=0, so T_tr~Theta_t*Theta_r=0 at seal.")
