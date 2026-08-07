# O1 asymptote checks — exact sympy, CPU, float-free. No production imports.
# Ground (cited, not imported): udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md
#   (C_A = A^dag A, A^dag = g^-1 A^T g; conjugacy invariance; delta_t = -(1/2)log lambda_timelike;
#    reversal delta_t(A^-1) = -delta_t(A); arrows TYPED INVERTIBLE),
# udt_ceff_profile_binding_test_2026-08-06/DERIVATION_NOTES.md (lambda_t = e^{-2 dphi} reciprocal),
# udt_mixing_channel_lane_2026-08-06/DERIVATION_NOTES.md (mu defect; lam_t*lam_r=1 iff mu=0, s!=r).
import sympy as sp

L, s, r, p, q, w, m = sp.symbols('L s r p q w m', positive=True)
out = []
def bank(k, v):
    out.append((k, v)); print(k, '=', v)

# ================= Q1 : mu=0 stratum, strain diag(L, 1/L, s^2, s^2), L = lambda_t -> 0+
ev = [L, 1/L, s**2, s**2]
e1 = sum(ev)
e2 = sum(ev[i]*ev[j] for i in range(4) for j in range(i+1, 4))
e3 = sum(ev[i]*ev[j]*ev[k] for i in range(4) for j in range(i+1, 4) for k in range(j+1, 4))
e4 = ev[0]*ev[1]*ev[2]*ev[3]
for nm, ex in [('e1', e1), ('e2', e2), ('e3', e3), ('e4', e4)]:
    bank('Q1_limit_' + nm, sp.limit(sp.together(ex), L, 0, '+'))

# arrow along the reciprocal path: D_r = diag(1/r, r, 1, 1); det and strain det
eta4 = sp.diag(-1, 1, 1, 1)
Dr = sp.diag(1/r, r, 1, 1)
bank('Q1_detA_along_path', sp.det(Dr))                      # stays 1: never singular
CDr = sp.simplify(eta4 * Dr.T * eta4 * Dr)                  # A^dag A (g=eta both ends)
bank('Q1_detC_along_path', sp.det(CDr))                     # stays 1
# entrywise limit of the ARROW as r->oo (lambda_t = 1/r^2 -> 0): the r-entry diverges
bank('Q1_arrow_entry_r_limit', sp.limit(Dr[1, 1], r, sp.oo))
# projectivized strain C/e1 as r->oo: rank-1 on the radial partner line, timelike line in kernel
e1r = 1/r**2 + r**2 + 2
Pproj = sp.Matrix(4, 4, lambda i, j: sp.limit((CDr / e1r)[i, j], r, sp.oo))
bank('Q1_projective_limit_strain', Pproj)
bank('Q1_projective_limit_rank', Pproj.rank())
bank('Q1_timelike_e0_in_kernel_of_limit', Pproj * sp.Matrix([1, 0, 0, 0]) == sp.zeros(4, 1))
# eigenline survival: e0 is an eigenvector of C for EVERY r (diagonal), causal char eta(e0,e0)=-1
bank('Q1_e0_eigvec_all_r', sp.simplify(CDr * sp.Matrix([1, 0, 0, 0]) - (1/r**2) * sp.Matrix([1, 0, 0, 0])) == sp.zeros(4, 1))
# reversal (banked law): strain of D_r^{-1} has timelike eigenvalue r^2 = 1/lambda_t
CDri = sp.simplify(eta4 * (Dr.inv()).T * eta4 * Dr.inv())
bank('Q1_reversal_lambda_t', CDri[0, 0])

# ================= Q2a : exact additivity scope
# (i) collinear reciprocal subgroup: D_{r1} D_{r2} = D_{r1 r2}
r1, r2 = sp.symbols('r1 r2', positive=True)
A1 = sp.diag(1/r1, r1, 1, 1); A2 = sp.diag(1/r2, r2, 1, 1)
bank('Q2a_collinear_group_law', sp.simplify(A2 * A1 - sp.diag(1/(r1*r2), r1*r2, 1, 1)) == sp.zeros(4, 4))
# depth additivity: lambda_t(comp) = 1/(r1 r2)^2 -> delta = log r1 + log r2 exactly
Ccomp = sp.simplify(eta4 * (A2 * A1).T * eta4 * (A2 * A1))
bank('Q2a_collinear_additive', sp.simplify(Ccomp[0, 0] - 1/(r1*r2)**2) == 0)
# (ii) DIFFERENT SPATIAL AXES, both diagonal (squeeze 0-1 then squeeze 0-2): STILL exactly additive
eta3 = sp.diag(-1, 1, 1)
B1 = sp.diag(sp.exp(-p), sp.exp(p), 1)      # reciprocal squeeze along x
B2 = sp.diag(sp.exp(-q), 1, sp.exp(q))      # reciprocal squeeze along y
M12 = B2 * B1
C12 = sp.simplify(eta3 * M12.T * eta3 * M12)
bank('Q2a_multiaxis_strain', C12)
bank('Q2a_multiaxis_additive_lambda_t', sp.simplify(C12[0, 0] - sp.exp(-2*(p+q))) == 0)
# (iii) SPATIAL-ROTATION twist of leg B's squeeze axis: e0 stays a shared eigenvector -> additive
th = sp.symbols('theta', real=True)
Rth = sp.Matrix([[1, 0, 0], [0, sp.cos(th), -sp.sin(th)], [0, sp.sin(th), sp.cos(th)]])
Brot = Rth * sp.diag(sp.exp(-q), sp.exp(q), 1) * Rth.T
Mrot = Brot * B1
Crot = sp.simplify(eta3 * Mrot.T * eta3 * Mrot)
v0 = sp.Matrix([1, 0, 0])
bank('Q2a_rotation_twist_e0_eigvec', sp.simplify(Crot * v0 - sp.exp(-2*(p+q)) * v0) == sp.zeros(3, 1))
# leg B depth under rotation twist is still q (spectrum check)
CBrot = sp.simplify(eta3 * Brot.T * eta3 * Brot)
bank('Q2a_rotB_spectrum', {sp.simplify(k) for k in CBrot.eigenvals().keys()})

# ================= Q2b : BOOST-twisted composition (the substantive leg) — 2x2 Lorentzian block
eta2 = sp.diag(-1, 1)
def dag2(A): return eta2 * A.T * eta2
P1 = sp.diag(sp.exp(-p), sp.exp(p))                          # leg A, depth p
Lw = sp.Matrix([[sp.cosh(w), sp.sinh(w)], [sp.sinh(w), sp.cosh(w)]])
D2 = sp.diag(sp.exp(-q), sp.exp(q))
Lwi = sp.Matrix([[sp.cosh(w), -sp.sinh(w)], [-sp.sinh(w), sp.cosh(w)]])  # explicit inverse
bank('Q2b_Lw_inv_exact', sp.simplify(sp.expand_trig(Lw * Lwi - sp.eye(2))) == sp.zeros(2, 2))
B = Lw * D2 * Lwi                                            # leg B, boost-twisted, depth q
CB = dag2(B) * B
bank('Q2b_legB_selfadj', (dag2(CB) - CB).applyfunc(lambda x: sp.simplify(sp.expand(x.rewrite(sp.exp)))) == sp.zeros(2, 2))
bank('Q2b_legB_charpoly_no_w', sp.simplify(sp.expand((CB.charpoly().as_expr()
     - (sp.Symbol('lambda')**2 - 2*sp.cosh(2*q)*sp.Symbol('lambda') + 1)).rewrite(sp.exp))) == 0)
M = B * P1                                                   # composite arrow (A then B)
CM = dag2(M) * M
half_tr = sp.trace(CM) / 2
law = sp.cosh(2*(p+q)) + 2*sp.sinh(w)**2 * sp.sinh(2*p) * sp.sinh(2*q)
bank('Q2b_TRACE_LAW_cosh2delta', sp.simplify(sp.expand((half_tr - law).rewrite(sp.exp))) == 0)
bank('Q2b_det_CM', sp.simplify(sp.expand(CM.det().rewrite(sp.exp))))
# => cosh(2 delta_comp) = cosh(2(p+q)) + 2 sinh^2(w) sinh(2p) sinh(2q):
#    same-sign p,q: SUPER-additive, equality iff w=0 (or a leg depth is 0). Unbounded in w.
corr = 2*sp.sinh(w)**2*sp.sinh(2*p)*sp.sinh(2*q)
bank('Q2b_correction_positive_offcollinear', corr.is_positive)   # w,p,q > 0
bank('Q2b_correction_zero_at_w0', corr.subs(w, 0))
bank('Q2b_limit_w_inf_same_sign', sp.limit(law, w, sp.oo))
# opposite-sign legs: cosh(2 delta) = cosh(2(p-q)) - 2 sinh^2 w sinh 2p sinh 2q (can exit stratum)
Bm = Lw * sp.diag(sp.exp(q), sp.exp(-q)) * Lwi               # depth -q leg
CMm = dag2(Bm * P1) * (Bm * P1)
lawm = sp.cosh(2*(p - q)) - 2*sp.sinh(w)**2*sp.sinh(2*p)*sp.sinh(2*q)
bank('Q2b_TRACE_LAW_opposite_sign', sp.simplify(sp.expand((sp.trace(CMm)/2 - lawm).rewrite(sp.exp))) == 0)

# exact RATIONAL witness of super-additivity: e^p = e^q = 2, cosh w = 5/4, sinh w = 3/4
P1n = sp.diag(sp.Rational(1, 2), 2)
Ln = sp.Matrix([[sp.Rational(5, 4), sp.Rational(3, 4)], [sp.Rational(3, 4), sp.Rational(5, 4)]])
Bn = Ln * sp.diag(sp.Rational(1, 2), 2) * Ln.inv()
Mn = Bn * P1n
CMn = dag2(Mn) * Mn
evs = list(CMn.eigenvals().keys())
lam_min = sp.Min(*[sp.nsimplify(e) for e in evs])
bank('Q2b_witness_half_trace', sp.nsimplify(sp.trace(CMn) / 2))       # expect 6137/512 > 257/32
bank('Q2b_witness_super_additive', sp.simplify(lam_min - sp.Rational(1, 16)).is_negative)  # lam_t < e^{-2(p+q)}
# causal label of the small-eigenvalue eigenline at the witness point: eta-norm sign
lam0 = [e for e in evs if sp.simplify(e - 1) .is_negative][0]
vec = (CMn - lam0 * sp.eye(2)).nullspace()[0]
bank('Q2b_witness_small_eig_timelike', sp.simplify((vec.T * eta2 * vec)[0, 0]).is_negative)

# ================= Q2b-3D : out-of-plane boost twist (0-2 plane boost on 0-1 squeezes), exact rational
def dag3(A): return eta3 * A.T * eta3
L02 = sp.Matrix([[sp.Rational(5, 4), 0, sp.Rational(3, 4)], [0, 1, 0], [sp.Rational(3, 4), 0, sp.Rational(5, 4)]])
D3 = sp.diag(sp.Rational(1, 2), 2, 1)
B3 = L02 * D3 * L02.inv()
CB3 = dag3(B3) * B3
bank('Q2b3_legB_spectrum', sorted(CB3.eigenvals().keys()))            # expect {1/4, 4, 1}: depth log 2
M3 = B3 * D3                                                          # composite of two depth-log2 legs
CM3 = dag3(M3) * M3
cp = CM3.charpoly()
roots = sp.real_roots(cp)
bank('Q2b3_all_roots_real_positive', all((rt.is_real and (rt > 0) == True) for rt in roots))
lam_min3 = min(roots)
bank('Q2b3_lambda_min_below_additive_1_16', (lam_min3 < sp.Rational(1, 16)) == True)
# timelike label of the min root: eta-norm of its eigenvector (exact algebraic sign)
try:
    lam0r = lam_min3
    N3 = CM3 - lam0r * sp.eye(3)
    v3 = N3.adjugate()[:, 0]
    nrm = sp.simplify((v3.T * eta3 * v3)[0, 0])
    bank('Q2b3_min_root_timelike', nrm.is_negative)
except Exception as ex:
    bank('Q2b3_min_root_timelike', 'UNDECIDED: ' + str(ex))


# ================= Q2d : ESCAPE HUNT (F-STEER discharge)
# (1) sub-additive POCKET hunt: mixed rotation+boost twists, both legs depth log 2.
Rr = sp.Matrix([[1,0,0],[0,sp.Rational(4,5),-sp.Rational(3,5)],[0,sp.Rational(3,5),sp.Rational(4,5)]])
L01 = sp.Matrix([[sp.Rational(5,4),sp.Rational(3,4),0],[sp.Rational(3,4),sp.Rational(5,4),0],[0,0,1]])
twists = {'rot_only': Rr, 'boost01': L01, 'boost02': L02,
          'rot_boost01': Rr*L01, 'boost02_rot': L02*Rr, 'boost01_boost02': L01*L02}
for nm, T in twists.items():
    Bt = T * D3 * T.inv()
    Ct = dag3(Bt * D3) * (Bt * D3)
    rts = sp.real_roots(Ct.charpoly())
    if len(rts) < 3:
        bank('POCKET_' + nm, 'NONREAL_SPECTRUM (left regular stratum)')
        continue
    lm = min(rts)
    cmp_add = 'EQUAL(additive)' if (lm == sp.Rational(1,16)) else ('SUPER(lam<1/16)' if (lm < sp.Rational(1,16)) == True else 'SUB(lam>1/16)')
    bank('POCKET_' + nm, cmp_add)

# (2) singular arrow attains lambda_t = 0 at FINITE entries — but is NOT a comparison arrow
A0 = sp.diag(0, 2, 1)
C0 = dag3(A0) * A0
bank('ESC_singular_strain', sp.diag(*sorted(C0.eigenvals().keys())))
bank('ESC_singular_det', sp.det(A0))   # 0 -> no inverse -> excluded by the banked typed-invertible arrow set

# (3) mu-direction (unipotent mixing leg) CANNOT reach the wall at fixed (r,s):
# clock-screen block of C_A (mixing lane, machine-confirmed): trace T = 1/r^2 + s^2 - m^2,
# det d = s^2/r^2 (verification-corrected constant term). Real spectrum: T^2 >= 4d and T>0.
T_ = 1/r**2 + s**2 - m**2
d_ = s**2 / r**2
lam_lo = (T_ - sp.sqrt(T_**2 - 4*d_)) / 2
lam_hi = (T_ + sp.sqrt(T_**2 - 4*d_)) / 2
bank('ESC_mu_block_sum_prod', (sp.simplify(lam_lo + lam_hi - T_) == 0, sp.simplify(lam_lo * lam_hi - d_) == 0))
# floor: lam_min = d/lam_max >= d/T >= d/(1/r^2+s^2) = s^2/(1+r^2 s^2) > 0 (m only LOWERS T)
bank('ESC_mu_floor_identity', sp.simplify(d_ / (1/r**2 + s**2) - s**2/(1 + r**2 * s**2)) == 0)
# machine check of the floor on the real-spectrum window at a rational grid (exact):
flr_ok = True
for rv, sv, mv in [(2, 1, sp.Rational(1,4)), (3, sp.Rational(1,2), sp.Rational(1,10)),
                   (sp.Rational(1,2), 2, sp.Rational(1,5)), (5, 1, sp.Rational(1,2))]:
    Tv = sp.Rational(1)/rv**2 + sv**2 - mv**2; dv = sv**2/rv**2
    if (Tv**2 - 4*dv) < 0: continue
    lmv = (Tv - sp.sqrt(Tv**2 - 4*dv))/2
    if not ((lmv >= dv/(sp.Rational(1)/rv**2 + sv**2)) == True): flr_ok = False
bank('ESC_mu_floor_holds_on_samples', flr_ok)

# (4) exits from the regular stratum by opposite-sign composition (2x2): never lambda_t = 0
# tr/2 = cosh(2(p+q)) - 2 sinh^2 w sinh(2p) sinh(2|q|) with q -> -q.
# elliptic exit sample: e^p=2, e^-q=2 wait q=-log2; sinh w = 1/4 -> tr/2 in (-1,1)
chq = sp.Rational(5,4); shq = sp.Rational(3,4)
def tr_half(shw):
    return 1 - 2*shw**2 * sp.Rational(15,8) * sp.Rational(15,8)
bank('ESC_elliptic_exit_tr_half', tr_half(sp.Rational(1,4)))     # in (-1,1): complex pair, |eig|=1 (det 1)
bank('ESC_negative_exit_tr_half', tr_half(sp.Rational(3,4)))     # < -1: both eigenvalues negative real
# in both exits det C = 1 != 0: lambda = 0 is never crossed; the extractor DOMAIN is left instead.

# ================= summary
print('---- ALL BANKED:', len(out), 'checks')
