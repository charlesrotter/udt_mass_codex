"""verify_embedded_closure.py -- CAS check of the EMBEDDED-cell seal closure H_cell=H_amb.

Derives (and checks) that a UDT cell sharing a movable seal with the ambient universe interior
obeys, from the shared-interface (Weierstrass-Erdmann) corner condition:
    (C1) momentum continuity  pi_cell = pi_amb            [JC1/JC2]
    (C2) Hamiltonian continuity  H_cell = H_amb           [the embedded closure -- the scale pin]
Both fall out of ONE interface variation as the coefficients of the two INDEPENDENT variations
(Dq = continuous field value at the seal; drs = seal-position shift). The closed cell is the
vacuum special case L_amb=0 -> H_amb=0 -> H_cell=0 (Step-0 V5, already blind-verified).

E1  single-endpoint transversality formula   d/deps INT_a^{s(eps)} L dr = INT EL*eta + pi*Dq + (L-q'pi)*drs
E2  two-domain interface variation -> corner conditions C1, C2 (sign-correct assembly)
E3  identify (L - q'pi) = -H, so C2 is H_cell = H_amb ; and confirm for the UDT reduced L-bar
    that the Step-0/solver Hamiltonian H_of_r EQUALS sum_q q' pi_q - L-bar (H is the corner quantity).
No wall numbers. No solving.
"""
import sympy as sp

# =========================================================================================
# E1: single variable-endpoint transversality formula, verified for a CONCRETE L (polynomials so
#     the integrals evaluate; the content is the IBP that turns d/deps INT into EL-form + boundary).
#     L = A(r) q'^2/2 - U(q,r).  Family q(r,eps)=q0(r)+eps*eta(r), moving end s(eps)=s0+eps*sig.
# =========================================================================================
r, eps, s0, sig = sp.symbols('r epsilon s0 sigma', real=True)
a = sp.Integer(0)                                       # fixed left end at 0 (eta(a)=0 below)
Afun = 1 + r**2                                         # concrete A(r)
q0e = r**2                                              # concrete q0(r)
etae = r                                                # concrete eta(r), eta(0)=0  (left end fixed)
Ufun = lambda qq: qq**3/6                               # concrete U(q); dU/dq = q^2/2
q = q0e + eps*etae
qp = sp.diff(q, r)
L = Afun*qp**2/2 - Ufun(q)

# LHS = d/deps INT_a^{s(eps)} L dr |_{eps=0}   (Leibniz: L|_s * s'(eps) + INT dL/deps)
s = s0 + eps*sig
dL_deps = sp.diff(L, eps)
LHS = (L.subs(eps, 0).subs(r, s0))*sig + sp.integrate(dL_deps.subs(eps, 0), (r, a, s0))

# RHS target = INT EL*eta dr + pi(s0)*Dq + (L - q' pi)|_{s0} * sig ,  Dq = eta(s0)+q0'(s0) sig
L0 = L.subs(eps, 0)
piL = Afun*sp.diff(q0e, r)                              # pi = dL/dq' = A q0'
# EL = dL0/dq0 - d/dr(dL0/dq0') = -dU/dq - d/dr(A q0') = -(q0^2/2) - (A q0')'
ELq = -(q0e**2/2) - sp.diff(piL, r)
Dq = etae.subs(r, s0) + sp.diff(q0e, r).subs(r, s0)*sig
transversality = (L0 - sp.diff(q0e, r)*piL).subs(r, s0)
RHS = (sp.integrate(ELq*etae, (r, a, s0))
       + piL.subs(r, s0)*Dq
       + transversality*sig)
E1 = sp.simplify(LHS - RHS) == 0

# E1b: LOWER-limit endpoint (the ambient side). d/deps INT_{s(eps)}^{b} L dr = INT EL eta
#      - pi*Dq - (L-q'pi)*drs  (opposite sign to E1 -- this is the ambient sign flip that E2 uses).
b = sp.Integer(3)                                       # concrete right end; eta(b)=0 for the ambient
etae_b = (r - b)                                        # eta(b)=0 (right end of ambient fixed)
q_b = q0e + eps*etae_b
L_b = Afun*sp.diff(q_b, r)**2/2 - Ufun(q_b)
LHS_b = -(L_b.subs(eps, 0).subs(r, s0))*sig + sp.integrate(sp.diff(L_b, eps).subs(eps, 0), (r, s0, b))
ELq_b = -(q0e**2/2) - sp.diff(piL, r)
Dq_b = etae_b.subs(r, s0) + sp.diff(q0e, r).subs(r, s0)*sig
RHS_b = (sp.integrate(ELq_b*etae_b, (r, s0, b))
         - piL.subs(r, s0)*Dq_b - transversality*sig)
E1b = sp.simplify(LHS_b - RHS_b) == 0

# =========================================================================================
# E2: two-domain interface variation. Generic symbols for each side at the seal.
#     Boundary functional B = [pi*eta(s) + (L-q'pi)*sig]_cell - [pi*eta(s)+(L-q'pi)*sig]_amb
#     (ambient integral has s as LOWER limit -> overall minus). eta(s) = Dq - q' sig (continuous Dq).
# =========================================================================================
Dqs, drs = sp.symbols('Dq drs', real=True)
pi_c, pi_a, qp_c, qp_a, L_c, L_a = sp.symbols('pi_c pi_a qp_c qp_a L_c L_a', real=True)
# transversality boundary term per side: pi*Dq + (L - q'pi)*drs, with Dq the TOTAL endpoint
# variation (single-valued at the seal). Ambient integral has the seal as LOWER limit -> minus.
B_cell = pi_c*Dqs + (L_c - qp_c*pi_c)*drs
B_amb  = pi_a*Dqs + (L_a - qp_a*pi_a)*drs
B = sp.expand(B_cell - B_amb)
coeff_Dq  = sp.simplify(B.coeff(Dqs))                   # -> C1
coeff_drs = sp.simplify(B.coeff(drs))                   # -> C2

# Define H = q' pi - L on each side; C2 should be H_amb - H_cell.
H_c = qp_c*pi_c - L_c
H_a = qp_a*pi_a - L_a
E2_C1 = sp.simplify(coeff_Dq - (pi_c - pi_a)) == 0                 # momentum continuity
E2_C2 = sp.simplify(coeff_drs - (H_a - H_c)) == 0                  # Hamiltonian continuity

# =========================================================================================
# E3: (L - q' pi) = -H identity, and for the UDT reduced L-bar confirm H_of_r = sum q' pi - L-bar.
#     Use the theta-DENSITY (pointwise in theta; avoids generic-f theta integration).
# =========================================================================================
th = sp.symbols('theta', positive=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r); f = sp.Function('f')(r, th)
sth = sp.sin(th)
Dg = (sth/2)*((Z/2)*rho**2*sp.diff(phi, r)**2 + 2 - 2*sp.exp(-2*phi)*sp.diff(rho, r)**2)
Dm = sp.Rational(1, 2)*((xi/2)*(rho**2*sp.diff(f, r)**2*sth + sp.diff(f, th)**2*sth + N**2*sp.sin(f)**2/sth)
      + (kap*N**2/2)*(sp.sin(f)**2/sth*sp.diff(f, r)**2 + sp.sin(f)**2/(sth*rho**2)*sp.diff(f, th)**2))
D = Dg - Dm                                             # total theta-density of L-bar

# radial momenta (density level) and the density Hamiltonian T = sum_q q' dD/dq' - D
# (so (L-bar - sum q'pi) = -T by definition; the corner condition C2 is thus H_cell=H_amb with H=T).
Tdens = (sp.diff(phi, r)*sp.diff(D, sp.diff(phi, r))
         + sp.diff(rho, r)*sp.diff(D, sp.diff(rho, r))
         + sp.diff(f, r)*sp.diff(D, sp.diff(f, r)) - D)

# GENERAL-f DENSITY-LEVEL check (stronger than rigid-only): build the H_of_r theta-DENSITY from the
# moment integrands and confirm it equals Tdens for GENERIC f (exercises the f_r-kinetic moments Ir,
# I4r that vanish at rigid f=theta). moment densities: Ir=(1/2)sin f_r^2, Ith=(1/2)sin f_th^2,
# Is=(1/2)sin^2f/sin, I4r=(1/2)sin^2f/sin f_r^2, I4th=(1/2)sin^2f/sin f_th^2.
fr_, fth_ = sp.diff(f, r), sp.diff(f, th)
Ir_d = sp.Rational(1, 2)*sth*fr_**2
Ith_d = sp.Rational(1, 2)*sth*fth_**2
Is_d = sp.Rational(1, 2)*sp.sin(f)**2/sth
I4r_d = sp.Rational(1, 2)*sp.sin(f)**2/sth*fr_**2
I4th_d = sp.Rational(1, 2)*sp.sin(f)**2/sth*fth_**2
Hdens_target = ((sth/2)*((Z/2)*rho**2*sp.diff(phi, r)**2 - 2*sp.exp(-2*phi)*sp.diff(rho, r)**2 - 2)
                - (xi/2)*rho**2*Ir_d + (xi/2)*(Ith_d + N**2*Is_d)
                - (kap*N**2/2)*I4r_d + (kap*N**2/2)*I4th_d/rho**2)
E3_solverH = sp.simplify(Tdens - Hdens_target) == 0     # GENERAL f (not restricted to rigid)

print("E1  transversality formula (UPPER limit / cell side)  = INT EL eta + pi Dq + (L-q'pi) drs :", E1)
print("E1b transversality formula (LOWER limit / ambient side, the sign flip E2 relies on)       :", E1b)
print("E2 corner condition C1 (coeff of Dq)  =  pi_cell - pi_amb         [momentum continuity]:", E2_C1)
print("E2 corner condition C2 (coeff of drs) =  H_amb - H_cell           [H_cell = H_amb]      :", E2_C2)
print("    -> C2 vanishes  <=>  H_cell = H_amb  (vacuum ambient L_amb=0 => H_amb=0 => closed-cell H=0).")
print("E3 GENERAL-f: solver H_of_r density EQUALS corner quantity (sum q'pi - L-bar) density     :", E3_solverH)
print("\nRESULT: the embedded closure H_cell = H_amb is the drs-coefficient of the shared-interface")
print("variation; it holds ALONGSIDE momentum continuity; it reduces to the verified closed-cell")
print("H=0 when the ambient is vacuum. H_amb (the ambient universe's radial Hamiltonian at the seal)")
print("supplies the cell's scale -- the pin the closed cell lacked.")
