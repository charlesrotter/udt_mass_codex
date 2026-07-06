"""
Blind symbolic derivation of the coupling constant lambda that reconciles the
base solver's reduced matter Lagrangian with (a) its rho-EOM matter force and
(b) its Hamiltonian matter integrand.  Independent of any numeric expectation.
"""
import sympy as sp

r = sp.symbols('r', real=True)
Z, XI, KAP, N, lam = sp.symbols('Z xi kappa N lambda', real=True)

# --- dynamical 1D fields ---
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)

# --- theta-moments: functions of r that DO NOT depend on rho(r) ---
# (I_r, I_4r depend on f_r; I_th, I_s, I_4th on f; none depend on rho.  So for the
#  rho-EL they are treated as rho-independent given profiles.)
Ir  = sp.Function('I_r')(r)
Ith = sp.Function('I_th')(r)
Is  = sp.Function('I_s')(r)
I4r = sp.Function('I_4r')(r)
I4th= sp.Function('I_4th')(r)

phip = sp.diff(phi, r)
rhop = sp.diff(rho, r)

# ------------------------------------------------------------------
# reduced Lagrangians
# ------------------------------------------------------------------
# geometric part chosen so its EL reproduces the base VACUUM rho/phi EOMs (given)
L_geo = sp.Rational(1,2)*Z*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 + 2

# standard reduced Faddeev-Skyrme matter density (theta-integrated)
L_m_red = XI*(rho**2*Ir + Ith + N**2*Is) + KAP*N**2*(I4r + I4th/rho**2)

L = L_geo + lam*L_m_red

# ==================================================================
# PART 1 : rho-EOM
# ==================================================================
# Euler-Lagrange for rho:  d/dr(dL/drho') - dL/drho = 0, solve rho''
EL_rho = sp.diff(sp.diff(L, rhop), r) - sp.diff(L, rho)
rhopp = sp.symbols('rhopp')
EL_rho_sub = EL_rho.subs(sp.diff(rho, (r,2)), rhopp)
rho_pp_sol = sp.solve(EL_rho_sub, rhopp)[0]
rho_pp_sol = sp.expand(sp.simplify(rho_pp_sol))

# base rho-EOM  (line 245-246 of cell_solver_f2d.py):
rho_pp_base = (2*phip*rhop - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*phip**2
               + sp.Rational(1,4)*sp.exp(2*phi)*(XI*rho*Ir - KAP*N**2*I4th/rho**3))

# The vacuum (Z, kinetic) parts must already match; the difference is the matter force.
diff_rho = sp.expand(rho_pp_sol - rho_pp_base)
# collect coefficient of the matter-force group (e^{2phi}) : solve for lambda making diff=0
lam_rho = sp.solve(sp.Eq(rho_pp_sol, rho_pp_base), lam)
print("=== PART 1 : rho-EOM ===")
print("EL-derived rho'' =", rho_pp_sol)
print("base      rho'' =", rho_pp_base)
print("lambda (rho-EOM) =", lam_rho)

# ==================================================================
# PART 2 : Hamiltonian
# ==================================================================
# Beltrami matter-Hamiltonian of lam*L_m_red.  The f_r-kinetic moments I_r, I_4r
# carry the q d/dq -> factor 2 (given by prompt):
H_m = lam*(2*(XI*rho**2*Ir + KAP*N**2*I4r) - L_m_red)
H_m = sp.expand(H_m)

# base H matter integrand (the I-terms in H, line 305-307):
H_matter_base = (-(XI/2)*rho**2*Ir + (XI/2)*(Ith + N**2*Is)
                 - (KAP*N**2/2)*I4r + (KAP*N**2/2)*I4th/rho**2)
H_matter_base = sp.expand(H_matter_base)

lam_H = sp.solve(sp.Eq(H_m, H_matter_base), lam)
print("\n=== PART 2 : Hamiltonian ===")
print("H_m(lambda) =", H_m)
print("base H_matter =", H_matter_base)
print("lambda (H)   =", lam_H)

# ==================================================================
# PART 3 : agreement
# ==================================================================
print("\n=== PART 3 : agreement ===")
agree = (set(lam_rho) == set(lam_H)) and len(lam_rho) == 1
print("lambda_rho =", lam_rho, " lambda_H =", lam_H)
print("AGREE (single consistent lambda)?", agree)

# ==================================================================
# PART 4 : corrected shear source coefficient
# ==================================================================
print("\n=== PART 4 : shear source ===")
if agree:
    lval = lam_rho[0]
    coeff = sp.nsimplify(lval*sp.Rational(1,2))   # Tshear = lambda*(rho^2/2)*T_s
    print("lambda =", lval)
    print("Tshear = lambda*(rho^2/2)*T_s = (%s)*rho^2*T_s" % coeff)
else:
    print("lambdas differ -> internal base inconsistency; no single shear coefficient")
