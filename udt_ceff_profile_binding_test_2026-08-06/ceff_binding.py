"""Exact symbolic test: is c_eff intertwined with the depth PROFILE at the
BARE RADIAL (reciprocal-subgroup) level, or does the binding REQUIRE the
angular/screen sector?  OBSERVE mode; float-free sympy; no production imports.

Grounds on udt_complete_pair_phi_orchestra_audit_2026-08-05:
  C_A = A^dagger A,  A^dagger = g_p^-1 A^T g_q  (frame-covariant strain)
  delta_t(A) = -(1/2) log(lambda_timelike of C_A)   (signed depth extractor)
  delta_a(p,q) = log[N(p)/N(q)] + a log[R(q)/R(p)]   (screen family, a free)
"""
import sympy as sp

phi_p, phi_q, cE = sp.symbols('phi_p phi_q c_E', real=True, positive=True)
Rp, Rq          = sp.symbols('R_p R_q', real=True, positive=True)
phi, a          = sp.symbols('phi a', real=True)

results = {}

# ---------------------------------------------------------------------------
# PART 0.  Reciprocal-lock metric, coordinate light speed, single-eigenvalue id
# ---------------------------------------------------------------------------
# ds^2 = -e^{-2phi} c_E^2 dt^2 + e^{2phi} dx^2   (radial 2-slot, reciprocal lock)
g_tt = -sp.exp(-2*phi)*cE**2
g_xx =  sp.exp( 2*phi)
c_eff = sp.sqrt(-g_tt/g_xx)                 # coordinate cone ratio (GAUGE quantity)
c_eff = sp.simplify(c_eff)
results['c_eff_symbolic'] = str(c_eff)      # expect c_E * e^{-2 phi}
results['c_eff_equals_cE_exp_m2phi'] = sp.simplify(c_eff - cE*sp.exp(-2*phi)) == 0

# reciprocal-subgroup strain at a founded point of depth phi=delta (r=e^phi):
# D_r = diag(r^-1, r, 1, 1),  C_D = D_r^dagger D_r on eta = diag(-1,1,1,1).
r = sp.exp(phi)
eta = sp.diag(-1, 1, 1, 1)
D_r = sp.diag(1/r, r, 1, 1)
C_D = eta.inv() * D_r.T * eta * D_r
C_D = sp.simplify(C_D)
results['C_D_diag'] = str([sp.simplify(C_D[i,i]) for i in range(4)])
# timelike eigenline = slot 0 (the eta=-1 direction)
lam_t = sp.simplify(C_D[0,0])               # expect e^{-2 phi}
results['lambda_timelike'] = str(lam_t)
# delta_t extractor recovers founded depth:
delta_t = sp.simplify(-sp.Rational(1,2)*sp.log(lam_t))
results['delta_t_equals_phi'] = sp.simplify(delta_t - phi) == 0

# THE IDENTITY:  c_eff = c_E * lambda_timelike   and   phi = -(1/2) log(c_eff/c_E)
results['ID_ceff_eq_cE_lambda_t'] = sp.simplify(c_eff - cE*lam_t) == 0
phi_from_ceff = sp.simplify(-sp.Rational(1,2)*sp.log(c_eff/cE))
results['ID_phi_eq_m_half_log_ceff_over_cE'] = sp.simplify(phi_from_ceff - phi) == 0
# => lambda_timelike = c_eff/c_E = e^{-2phi}; phi = delta_t. ONE eigenvalue, two reads.

for k, v in results.items():
    print(f"{k}: {v}")

# ---------------------------------------------------------------------------
# PART 1.  OPTION B -- radial-complete: profile of delta_t as q moves (p fixed),
#          bound to c_eff, using ONLY the reciprocal (radial) subgroup.
# ---------------------------------------------------------------------------
print("\n=== PART 1: radial profile binding (Option B) ===")
b = {}
# Natural chart comparison arrow p->q is A = Identity reading g_p vs g_q.
# Radial 2-slot metrics (reciprocal lock, c=c_E):
gp2 = sp.diag(-sp.exp(-2*phi_p)*cE**2, sp.exp(2*phi_p))
gq2 = sp.diag(-sp.exp(-2*phi_q)*cE**2, sp.exp(2*phi_q))
A2  = sp.eye(2)
eta2 = sp.diag(-1, 1)
Adag2 = gp2.inv() * A2.T * gq2                 # A^dagger = g_p^-1 A^T g_q
C2 = sp.simplify(Adag2 * A2)
b['C2_diag'] = str([sp.simplify(C2[i,i]) for i in range(2)])
lam_t_pq = sp.simplify(C2[0,0])                # timelike slot
b['lambda_t_pq'] = str(lam_t_pq)               # expect e^{-2(phi_q-phi_p)}
# c_eff profile ratio q/p:
ceff_p = cE*sp.exp(-2*phi_p); ceff_q = cE*sp.exp(-2*phi_q)
b['ceff_ratio_eq_lambda_t'] = sp.simplify(ceff_q/ceff_p - lam_t_pq) == 0
# depth profile from extractor:
delta_t_pq = sp.simplify(-sp.Rational(1,2)*sp.log(lam_t_pq))
b['delta_t_pq'] = str(delta_t_pq)              # expect phi_q - phi_p
# MUTUAL FIXING: given radial comparison alone, c_eff(q) <-> phi(q) invertible.
# c_eff(q) determines phi(q):  phi_q = -(1/2) log(ceff_q/cE)
b['phi_q_recovered'] = sp.simplify(-sp.Rational(1,2)*sp.log(ceff_q/cE) - phi_q) == 0
# and phi(q) determines c_eff(q):  ceff_q = cE e^{-2phi_q}  (already by construction)
b['ceff_q_from_phi'] = sp.simplify(ceff_q - cE*sp.exp(-2*phi_q)) == 0
for k, v in b.items(): print(f"{k}: {v}")

# ---------------------------------------------------------------------------
# PART 2.  OPTION A -- turn on the screen/angular sector.  Does `a` enter the
#          TIMELIKE eigenvalue (hence c_eff)?
# ---------------------------------------------------------------------------
print("\n=== PART 2: screen sector on -- does a enter the timelike eigenvalue? ===")
s = {}
# Full 4-slot metrics: [t (timelike), x (radial), screen1, screen2], screen = R^2.
gp4 = sp.diag(-sp.exp(-2*phi_p)*cE**2, sp.exp(2*phi_p), Rp**2, Rp**2)
gq4 = sp.diag(-sp.exp(-2*phi_q)*cE**2, sp.exp(2*phi_q), Rq**2, Rq**2)
A4  = sp.eye(4)                                 # split-preserving natural chart arrow
C4  = sp.simplify(gp4.inv()*A4.T*gq4*A4)
diag4 = [sp.simplify(C4[i,i]) for i in range(4)]
s['C4_diag'] = str(diag4)
lam_t4 = diag4[0]                               # timelike slot
s['lambda_timelike_4slot'] = str(lam_t4)        # expect e^{-2(phi_q-phi_p)}, NO R
# does R (hence a) appear in the timelike eigenvalue?
s['R_in_timelike_eig'] = bool(lam_t4.free_symbols & {Rp, Rq})
s['timelike_eig_unchanged_by_screen'] = sp.simplify(lam_t4 - lam_t_pq) == 0
# screen eigenvalues carry R:
s['screen_eigs'] = str([diag4[2], diag4[3]])
s['R_in_screen_eig'] = bool((diag4[2].free_symbols) & {Rp, Rq})
# c_eff (radial cone) uses only g_tt,g_xx -> unchanged by R:
ceff4 = sp.simplify(sp.sqrt(-gq4[0,0]/gq4[1,1]))
s['ceff_4slot'] = str(ceff4)
s['ceff_no_R'] = not bool(ceff4.free_symbols & {Rp, Rq})

# delta_a family and where `a` lives:
# delta_a(p,q) = log[N(p)/N(q)] + a log[R(q)/R(p)],  N = sqrt(-g_tt) = c_E e^{-phi}
N_p = cE*sp.exp(-phi_p); N_q = cE*sp.exp(-phi_q)
delta_a = sp.log(N_p/N_q) + a*sp.log(Rq/Rp)
delta_a = sp.simplify(delta_a)
s['delta_a'] = str(delta_a)                     # expect (phi_q-phi_p) + a log(Rq/Rp)
# the a-dependent piece:
da_da = sp.simplify(sp.diff(delta_a, a))
s['d(delta_a)/da'] = str(da_da)                 # = log(Rq/Rp): pure screen, no timelike
# timelike-strain depth delta_t is the a=0 part; a modulates ONLY screen:
s['delta_a_at_a0_eq_delta_t'] = sp.simplify(delta_a.subs(a,0) - delta_t_pq) == 0
s['a_touches_timelike'] = bool(da_da.free_symbols & {phi_p, phi_q})  # expect False
for k, v in s.items(): print(f"{k}: {v}")

# ---------------------------------------------------------------------------
# PART 3.  F-STEER honesty probe: the OFF-DIAGONAL clock-screen MIXING witness
#          (EXACT_DERIVATION.md sec.4).  This is a DIFFERENT angular operation
#          -- unipotent mixing, NOT the diagonal screen-area coefficient `a`.
#          Does it touch the timelike eigenvalue?  (If yes -> that channel is A;
#          but it is not what `a` in delta_a parameterizes.)
# ---------------------------------------------------------------------------
print("\n=== PART 3: off-diagonal clock->screen mixing witness (not a) ===")
m = {}
A = sp.Matrix([[sp.Rational(1,2),0,0,0],
               [0,2,0,0],
               [sp.Rational(1,4),0,1,0],
               [0,0,0,1]])                       # sec.4 registered arrow
CA = sp.simplify(eta.inv()*A.T*eta*A)            # endpoints founded (g=eta)
# clock-screen 2x2 block (rows/cols 0,2):
blk = CA.extract([0,2],[0,2])
cp = sp.simplify(blk.charpoly(sp.Symbol('L')).as_expr())
m['clockscreen_charpoly'] = str(cp)              # expect L^2 -(19/16)L +1/4
eigs = sp.solve(sp.Eq(cp,0), sp.Symbol('L'))
m['clockscreen_eigs'] = str([sp.nsimplify(e) for e in eigs])
lam_minus = min(eigs, key=lambda e: sp.N(e))     # timelike eigenline
delta_t_mix = sp.simplify(-sp.Rational(1,2)*sp.log(lam_minus))
m['delta_t_mix_vs_log2'] = str(sp.simplify(delta_t_mix - sp.log(2)))  # nonzero
m['mixing_changes_timelike'] = sp.simplify(delta_t_mix - sp.log(2)) != 0
# KEY: this mixing is NOT diag screen-area; it does NOT appear as `a` in delta_a.
# delta_a (sec.7 character) = delta_quotient + a*log det Q ; unipotent mixing
# "does not enter this ordinary character" (EXACT_DERIVATION sec.7).
m['note'] = "mixing != a: a is diagonal screen-area; mixing is unipotent off-diagonal"
for k, v in m.items(): print(f"{k}: {v}")
