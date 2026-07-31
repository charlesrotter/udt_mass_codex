#!/usr/bin/env python3
# BLIND VERIFIER independent check -- P4 doorway study. Built incrementally.
# Independent re-derivations; NOT a copy of derive_doorway_study.py.
import sys, os
import sympy as sp
from sympy import symbols, sin, cos, exp, I, pi, S, Matrix, integrate, simplify, eye, zeros

FAIL = []
def chk(name, ok):
    print(("VPASS " if ok else "VFAIL ") + name)
    if not ok: FAIL.append(name)

th, ph, psi = symbols('theta phi psi', real=True)
# --- G1: C1 Hopf. My own route: full left-invariant forms on S3 (Euler angles),
# sigma3 = dpsi + cos(th) dphi. Chern via Stokes on two charts, NOT just the naive integral.
sig3 = {'th': S(0), 'ph': cos(th), 'ps': S(1)}
d_thph = sp.diff(sig3['ph'], th)          # d(sigma3) two-form coefficient (th^ph)
chk("G1_dsigma3", simplify(d_thph + sin(th)) == 0)
# potentials in the two trivializations psi_N = psi + phi, psi_S = psi - phi (my own):
# sigma3 = d(psi_N) + (cos th - 1) dphi = d(psi_S) + (cos th + 1) dphi  -- verify exactly
lhsN = sp.diff(psi + ph, psi) - 1        # trivial sanity of construction
aN, aS = cos(th) - 1, cos(th) + 1
chk("G1_potentials", simplify(sp.diff(aN, th) + sin(th)) == 0
    and simplify(sp.diff(aS, th) + sin(th)) == 0
    and aN.subs(th, 0) == 0 and aS.subs(th, pi) == 0)
# Chern by Stokes: int_{S2} d(sigma3) = loop-int over equator of (aN - aS) dphi
stokes = integrate(aN - aS, (ph, 0, 2*pi))
direct = integrate(integrate(-sin(th), (th, 0, pi)), (ph, 0, 2*pi))
chk("G1_chern_minus4pi_two_routes", simplify(stokes + 4*pi) == 0 and simplify(direct + 4*pi) == 0)
# transition datum psi_N - psi_S = 2*phi: winding around fiber circle (period 4pi) = 4pi/4pi = 1
chk("G1_transition_winding_one", simplify(integrate(sp.diff(2*ph, ph), (ph, 0, 2*pi)) - 4*pi) == 0)
# no global F (even circle-valued) with dF = sigma3: dF closed but d sigma3 != 0 -- exact
chk("G1_no_global_phase", simplify(d_thph) != 0)

# --- G2: cap census recomputed MYSELF from the banked TSV (independent parse)
tsv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "udt_higher_isometry_plane_ownership_audit_2026-07-28",
                   "TORIC_CAP_ENUMERATION.tsv")
lines = [l.rstrip("\n").split("\t") for l in open(tsv) if l.strip()]
hdr, data = lines[0], lines[1:]
dets = []
for r in data:
    a, b = [sp.Integer(v) for v in r[1].split(",")], [sp.Integer(v) for v in r[2].split(",")]
    dets.append(a[0]*b[1] - a[1]*b[0])
chk("G2_census_104_rows", len(data) == 104)
chk("G2_all_dets_unit", all(abs(d) == 1 for d in dets))
chk("G2_banked_column_match", all(d == sp.Integer(r[3]) for d, r in zip(dets, data)))
# pi1 = Z/|det| per pair; |det|=1 => trivial; Hom(trivial, Z) = 0 => no winding home.

# --- G3: C2 toric angle. Winding 1 on cap-axis loop; continuous extension over the cap
# point would force, on a sufficiently small loop, image inside an open arc; a loop in an
# arc lifts with |increment| < 2pi, and increment in 2piZ => increment 0 => winding 0.
n = symbols('n', integer=True)
chk("G3_only_small_multiple_is_zero",
    sp.solveset(sp.Eq(2*pi*n, 0), n, S.Integers) == sp.FiniteSet(0)
    and not bool(sp.Abs(2*pi) < 2*pi))
# contradiction with winding 1 (homotopy invariance = named Category-A) => C2 FAILS. AGREE.

print("PART1 fails:", FAIL)

# --- G4: C3 screen SO(2) + K4. MY OWN route: use Route B's banked K4 explicitly.
t = symbols('t', real=True)
Rt = Matrix([[cos(t), -sin(t)], [sin(t), cos(t)]])
chk("G4_circle_genuine", simplify(Rt.subs(t, 2*pi) - eye(2)) == zeros(2,2)
    and simplify(Rt.subs(t, pi) + eye(2)) == zeros(2,2))
# banked K4 (Route B): {I, diag(1,1,-1,-1), diag(1,-1,-1,1), diag(1,-1,1,-1)} in SO+(1,3).
K4 = [sp.diag(1,1,1,1), sp.diag(1,1,-1,-1), sp.diag(1,-1,-1,1), sp.diag(1,-1,1,-1)]
screens = [M[2:4, 2:4] for M in K4]     # screen block = slots (2,3)
in_SO2 = [sp.det(Sb) == 1 and (Sb[0,0]-Sb[1,1]) == 0 and (Sb[0,1]+Sb[1,0]) == 0 for Sb in screens]
chk("G4_K4_screen_blocks", screens[0] == eye(2) and screens[1] == -eye(2)
    and screens[2] == sp.diag(-1,1) and screens[3] == sp.diag(1,-1))
chk("G4_only_two_K4_screens_in_SO2", in_SO2 == [True, True, False, False])
# so the OWNED-CIRCLE members among K4 screen shadows are exactly {I,-I} = 2-torsion of SO(2);
# the other two K4 elements have det=-1 screen blocks (NOT circle members) -- caveat recorded.
# SO(2) intersect signed-diagonals = {I,-I}: my own certificate
sd = [sp.diag(e1, e2) for e1 in (1,-1) for e2 in (1,-1)]
inter = [D for D in sd if simplify(sp.det(D)) == 1 and D[0,0] == D[1,1]]
chk("G4_SO2_cap_signed_diag", sorted([str(D) for D in inter]) ==
    sorted([str(eye(2)), str(-eye(2))]))
chk("G4_real_points_U1", sp.solveset(sp.Eq(symbols('z')**2, 1), symbols('z'), S.Reals)
    == sp.FiniteSet(-1, 1))
# triangular chart block group owns no compact one-parameter subgroup: my route via eigenvalues
a_, b_ = symbols('a_ b_', real=True, nonzero=True)
Xl = Matrix([[a_, 0], [b_, -a_]])       # generic traceless lower-triangular generator
ev = list(Xl.eigenvals().keys())
chk("G4_triangular_gen_real_spectrum", all(sp.simplify(sp.im(e)) == 0 for e in ev))
# nilpotent case a_=0: exp(TX) = I + T X, unbounded unless zero
Tn = symbols('Tn', real=True)
chk("G4_nilpotent_noncompact", (eye(2) + Tn*Xl.subs(a_, 0)) != eye(2))
# anchored dressing: my own dsolve
kf = sp.Function('k'); f = sp.Function('thd'); x = symbols('x', real=True)
solD = sp.dsolve(sp.Eq(f(x).diff(x) + 2*kf(x)*f(x), 0), f(x), ics={f(0): 0})
chk("G4_dressing_zero", solD.rhs == 0)

# --- G5: C4 E07/E08. My own: E08 group = R semidirect R, check n-th roots directly.
p_, u_ = symbols('p_ u_', real=True)
def mulE(A, B):  # A then B composed as in banked law u12 = u1 + e^{-p1} u2
    return (A[0] + B[0], A[1] + exp(-A[0])*B[1])
# associativity on symbols:
q1, q2, q3, v1, v2, v3 = symbols('q1 q2 q3 v1 v2 v3', real=True)
A1, A2, A3 = (q1, v1), (q2, v2), (q3, v3)
l_ = mulE(mulE(A1, A2), A3); r_ = mulE(A1, mulE(A2, A3))
chk("G5_E08_assoc", all(simplify(l_[i] - r_[i]) == 0 for i in (0, 1)))
sq = mulE((p_, u_), (p_, u_))
chk("G5_E08_no_2torsion", simplify(sq[0]) == 2*p_ and
    sp.solveset(sp.Eq(2*p_, 0), p_, S.Reals) == sp.FiniteSet(0)
    and simplify(sq[1].subs(p_, 0)) == 2*u_)
kk = symbols('kk', real=True, nonzero=True)
chk("G5_E07_point_kernel",
    sp.solveset(sp.Eq(exp(Tn*kk), 1), Tn, S.Reals).subs(kk, 3) == sp.FiniteSet(0))
print("PART2 fails:", FAIL)

# --- G6: C5 legality chain (my own instances)
tv = symbols('tv', real=True)
chk("G6_bare_theta_not_target_function", simplify((tv + 2*pi) - tv) != 0)
chk("G6_periodic_entries_legal", all(simplify(F.subs(tv, tv + 2*pi) - F) == 0
    for F in (cos(tv), sin(tv), exp(I*tv), cos(2*tv) + 3*sin(tv))))
Fg = sp.Function('lift')
chk("G6_jets_lift_independent",
    simplify(sp.diff(Fg(x) + 2*pi, x) - sp.diff(Fg(x), x)) == 0)
# co-translation rule (Route D R3 form), MY witness lift = x^3:
s_ = symbols('s_', real=True); w3 = x**3; uu = symbols('uu', real=True)
tm = integrate(sp.diff(w3.subs(x, uu + s_), uu), (uu, 0, x))     # anchored entry of shifted member
nv = w3.subs(x, x + s_) - w3.subs(x, 0)                          # co-translated original entry
chk("G6_nonlocal_anchor_defect", simplify(tm - nv) == -s_**3 and simplify(tm - nv) != 0)
# also reproduce their -s^2 witness independently:
w2 = x**2
tm2 = integrate(sp.diff(w2.subs(x, uu + s_), uu), (uu, 0, x)); nv2 = w2.subs(x, x+s_) - w2.subs(x, 0)
chk("G6_their_witness_minus_s2", simplify(tm2 - nv2) == -s_**2)

# --- G7: two-sided twisted law + central U(1) (my own generic blocks, incl. base assoc)
def two(Bt, At):  # (rho, Q, L, u), segment At then Bt
    return (Bt[0]*At[0], Bt[1]*At[1], Bt[1]*At[2] + Bt[2]*At[0], Bt[3]*At[3])
Ms = [Matrix(2, 2, sp.symbols(f'm{k}_:4')) for k in range(9)]
pa, pb, pc = symbols('pa pb pc', real=True)
TA = (Ms[0], Ms[1], Ms[2], exp(I*pa)); TB = (Ms[3], Ms[4], Ms[5], exp(I*pb)); TC = (Ms[6], Ms[7], Ms[8], exp(I*pc))
L1 = two(two(TC, TB), TA); R1 = two(TC, two(TB, TA))
chk("G7_assoc_with_U1", all(sp.expand(L1[i] - R1[i]) == zeros(2,2) for i in (0,1,2))
    and simplify(L1[3] - R1[3]) == 0)
# adjunction is DIRECT-PRODUCT (u never enters blocks; blocks never enter u): structural note
chk("G7_blocks_untouched", all((two(TB, TA)[i] - two((Ms[3],Ms[4],Ms[5],S(1)), (Ms[0],Ms[1],Ms[2],S(1)))[i])
    == zeros(2,2) for i in (0,1,2)))
chk("G7_unitary", simplify(exp(I*pa)*sp.conjugate(exp(I*pa))) == 1)

# --- G8: K4/parity crease + J05 IBP (my own witnesses) + F-D5
# theta == -theta on R/2piZ  <=>  2 theta in 2piZ  <=>  theta in {0, pi} mod 2pi:
fund = [k*pi/6 for k in range(12)]                    # sweep the fundamental domain at pi/6 grid
fixed = [v for v in fund if simplify(sp.Mod(2*v, 2*pi)) == 0]
chk("G8_crease_two_torsion", fixed == [0, pi]
    and simplify(sp.Mod(2*(pi/2), 2*pi)) == pi and simplify(sp.Mod(2*(pi/3), 2*pi)) != 0)
Lw = symbols('Lw', positive=True)
Dw, Ew, Vw = sin(x), cos(2*x), x**2 + 3*x   # MY witnesses, non-polynomial mix
lhsI = integrate(Dw*Vw + Ew*sp.diff(Vw, x), (x, 0, Lw))
rhsI = integrate((Dw - sp.diff(Ew, x))*Vw, (x, 0, Lw)) + (Ew*Vw).subs(x, Lw) - (Ew*Vw).subs(x, 0)
chk("G8_J05_IBP_trig_witness", simplify(lhsI - rhsI) == 0)
chk("G8_FD5_real_vs_circle",
    sp.solveset(sp.Eq(exp(t), 1), t, S.Reals) == sp.FiniteSet(0)
    and simplify(exp(2*pi*I)) == 1 and simplify(exp(4*pi*I)) == 1
    and simplify(exp(pi*I)) == -1 and 2*pi != 0)
print("PART3 fails:", FAIL)

# --- G9: TD-3. My own N=2 telescoping derivation of the winding condition.
c1_, c2_, L1_, L2_, J1_, J2_, b1_ = symbols('c1_ c2_ L1_ L2_ J1_ J2_ b1_', real=True)
nw = symbols('nw', integer=True)
# lifts: cell1 theta = c1 x + b1 on [0, L1]; seam jump J1; cell2 theta = c2 x + b2 on [0, L2]
b2_ = c1_*L1_ + b1_ + J1_          # start of cell 2 = end of cell 1 + jump
end2 = c2_*L2_ + b2_               # end of cell 2
back = end2 + J2_                  # after closing seam jump J2, must return to b1 mod 2pi
increment = simplify(back - b1_)
chk("G9_increment_telescopes", sp.expand(increment - (c1_*L1_ + c2_*L2_ + J1_ + J2_)) == 0)
# single-valuedness of the CIRCLE-valued field: e^{i increment} = 1 <=> increment in 2piZ.
# The 2pi is the registered target period -- from exp(I*2pi*n)=1 exactly, and NOT from any
# real-target condition (real target would force increment == 0):
chk("G9_2pi_from_target", simplify(exp(I*(2*pi*nw)).rewrite(cos).subs(nw, 5)) == 1
    and simplify(exp(I*pi)) == -1)
chk("G9_real_target_contrast", sp.solve(sp.Eq(increment, 0), c1_) ==
    [-(c2_*L2_ + J1_ + J2_)/L1_])   # single hyperplane (n forced 0) -- banked real-target form
solL = sp.solve(sp.Eq(c1_*L1_ + c2_*L2_ + J1_ + J2_, 2*pi*nw), L1_)
chk("G9_Z_indexed_family", solL == [(2*pi*nw - c2_*L2_ - J1_ - J2_)/c1_])
# fixed-slope conditional lattice (c=1, J=0, one cell): L = 2 pi n -- and freedom check:
# at ANY given (L1_, L2_, n) there is a slope solving it => no unconditional cut of lengths:
solc = sp.solve(sp.Eq(c1_*L1_ + c2_*L2_ + J1_ + J2_, 2*pi*nw), c1_)
chk("G9_slopes_absorb", len(solc) == 1)
# Hom(D-infinity, Z) = 0: generators of order 2
hz = symbols('hz', integer=True)
chk("G9_homDinfZ_zero", sp.solveset(sp.Eq(2*hz, 0), hz, S.Integers) == sp.FiniteSet(0))
# torsion revival: real target 2P=0 => P=0; U(1) target hol^2=1 => {+-1} (TWO points)
PP = symbols('PP', real=True); zz = symbols('zz')
chk("G9_real_vacuity_reproduced", sp.solveset(sp.Eq(2*PP, 0), PP, S.Reals) == sp.FiniteSet(0))
chk("G9_U1_two_torsion_live", sp.solveset(sp.Eq(zz**2, 1), zz, S.Complexes) == sp.FiniteSet(-1, 1))

# --- G10: TD-4. pi2(S1) = 0 route + Hopf base metric identity (my own forms).
# S2 -> S1 lift exists (pi1(S2)=0, monodromy hom trivial): Hom(0,Z)=0 trivially; then
# straight-line homotopy in R: H(s,p) = s*lift(p), H(0)=0, H(1)=lift -- endpoints:
sB = symbols('sB', real=True); lf = sp.Function('lf')(symbols('pB'))
chk("G10_null_homotopy_endpoints", (sB*lf).subs(sB, 0) == 0 and (sB*lf).subs(sB, 1) == lf)
# left-invariant forms (Euler angles): sigma1 = cos(psi) dth + sin(psi) sin(th) dph,
# sigma2 = -sin(psi) dth + cos(psi) sin(th) dph. Sum of squares:
s1th, s1ph = cos(psi), sin(psi)*sin(th)
s2th, s2ph = -sin(psi), cos(psi)*sin(th)
chk("G10_hopf_base_round_S2",
    simplify(s1th**2 + s2th**2 - 1) == 0
    and simplify(s1ph**2 + s2ph**2 - sin(th)**2) == 0
    and simplify(s1th*s1ph + s2th*s2ph) == 0)
# psi-independence (basic w.r.t. the fiber) -- coefficients of the quadratic form:
chk("G10_psi_independent", all(sp.diff(e, psi) == 0 for e in
    (simplify(s1th**2 + s2th**2), simplify(s1ph**2 + s2ph**2), simplify(s1th*s1ph + s2th*s2ph))))
chk("G10_equatorial_unit", simplify(cos(tv)**2 + sin(tv)**2 - 1) == 0)
print("PART4 fails:", FAIL)
print("TOTAL VFAILS:", len(FAIL))
sys.exit(0 if not FAIL else 1)
