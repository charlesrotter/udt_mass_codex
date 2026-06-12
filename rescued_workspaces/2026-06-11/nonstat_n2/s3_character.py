"""NONSTATIONARY SECTOR N2 — script 3: the evolution system and its character.

Inputs (s1, s2 all PASS): the unique nondegenerate reduction is
  L*_ab = -sgn(Q) (c/8) sqrt(B) [f P + D2 vT^2] / (f sqrt(f D2)),
and the complete solution set of the algebraic sector is the spherical
branch {vh = 0, q = 0, w arbitrary} (plus degenerate corners).

This script:
  C1: the exact spherical-branch reduced Lagrangian and EOM; w-decoupling;
      the banked algebraic-weld anchor a* -> H1 = -4 d_t(dphi)/f0'.
  C2: principal symbol / character on the exact branch: ELLIPTIC in (T,r).
  C3: constrained-class characters (diagonal-evolution; Class-B evolution):
      Hessian signatures, sonic/degeneracy loci.
  C4: well-posedness statements (recorded as printed rulings + checks).
"""
import numpy as np
import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label)

def zero_cancel(e):
    return sp.cancel(sp.together(e)) == 0

c, f, r = sp.symbols('c f r', positive=True)
sth = sp.Symbol('s_th', positive=True)
W1 = sp.Symbol('W1', positive=True)          # 1 + w
q = sp.Symbol('q', real=True)
vT, vr, vh = sp.symbols('v_T v_r v_theta', real=True)
A = r**2 * W1**2
B = r**2 * sth**2 / W1**2
D2 = A / f - q**2
P = A * vr**2 - 2 * q * vr * vh + vh**2 / f
Rn = f * P + D2 * vT**2
Lab = -Ra(1, 8) * c * sp.sqrt(B) * Rn / (f * sp.sqrt(f * D2))   # Q>0 branch

# ===================================================================== C1
Lsph = sp.simplify(Lab.subs({vh: 0, q: 0}))
Lsph_expected = -Ra(1, 8) * c * r**2 * sth * (vr**2 + vT**2 / f**2)
check("C1a: spherical-branch L_red = -(c/8) r^2 sin(th) [f_r^2 + f_T^2/f^2] "
      "— w cancels EXACTLY (flat direction invisible in the action)",
      sp.simplify(Lsph - Lsph_expected) == 0)

# EOM in f and in phi = -(1/2) ln f; equivalence.
T, rr = sp.symbols('T r_c', positive=True)
ff = sp.Function('f', positive=True)(T, rr)
Lf = (-Ra(1, 8) * c * rr**2 * (sp.diff(ff, rr)**2 + sp.diff(ff, T)**2 / ff**2))
ELf = (sp.diff(sp.diff(Lf, sp.diff(ff, T)), T)
       + sp.diff(sp.diff(Lf, sp.diff(ff, rr)), rr)
       - sp.diff(Lf, ff))
phi = sp.Function('phi', real=True)(T, rr)
fphi = sp.exp(-2 * phi)
ELf_phi = ELf.subs(ff, fphi).doit()
target = rr**2 * sp.diff(phi, T, 2) + sp.diff(rr**2 * fphi**2 * sp.diff(phi, rr), rr) \
    + 2 * rr**2 * fphi**2 * sp.diff(phi, rr)**2
ratio = sp.simplify(sp.cancel(sp.together(ELf_phi / target)))
print("    EL(f-form)/[phi-form target] =", ratio)
check("C1b: EL(f-form) = (c/2) e^{2 phi} * [r^2 phi_TT + (r^2 f^2 phi_r)' "
      "+ 2 r^2 f^2 phi_r^2]  — positive multiple: EOMs equivalent",
      sp.simplify(ratio - c * sp.exp(2 * phi) / 2) == 0)
# static limit: (r^2 f')' = 0  => banked vacuum f = C + a/r
fst = sp.Function('f0', positive=True)(rr)
ELst = ELf.subs(ff, fst).doit()
Cc, aa = sp.symbols('C a_v', positive=True)
check("C1c: static limit EOM = (r^2 f')' = 0; banked vacuum f = C + a/r solves it",
      sp.simplify(ELst.subs(fst, Cc + aa / rr).doit()) == 0)

# the banked algebraic weld: a* linearized = H1 = -4 d_t(dphi)/f0'
a_star = 2 * f * vT * vr / (f**2 * vr**2 - vT**2)   # spherical branch (q=0,vh=0)
eps = sp.Symbol('epsilon')
f0s, f0p, dfT = sp.symbols('f0 f0p df_T', real=True)
a_lin = sp.series(a_star.subs({f: f0s, vT: eps * dfT, vr: f0p}), eps, 0, 2).removeO().coeff(eps, 1)
# dphi_T = -df_T/(2 f0)  =>  -4 dphi_T/f0' = 2 df_T/(f0 f0p)
check("C1d: linearized a* = 2 df_T/(f0 f0') = -4 d_t(dphi)/f0'  "
      "[the BANKED ALGEBRAIC WELD H1 — exact anchor]",
      zero_cancel(a_lin - 2 * dfT / (f0s * f0p)))

# ===================================================================== C2
# principal symbol on the exact branch: Hess_v of L_red ~ -(c/4) r^2 diag(1/f^2, 1)
H_TT = sp.diff(Lsph_expected, vT, 2)
H_rr = sp.diff(Lsph_expected, vr, 2)
H_Tr = sp.diff(sp.diff(Lsph_expected, vT), vr)
check("C2a: exact-branch principal symbol  -(c/4) r^2 s_th (tau^2/f^2 + rho^2) "
      "— NEGATIVE DEFINITE: ELLIPTIC in (T, r), no real characteristics",
      sp.simplify(H_TT + Ra(1, 4) * c * r**2 * sth / f**2) == 0 and
      sp.simplify(H_rr + Ra(1, 4) * c * r**2 * sth) == 0 and H_Tr == 0)
print("    degeneracy loci of the exact branch: f -> 0 (seal), r -> 0 (core),")
print("    and the elimination boundary Q = (A/f) g = 0, g = f vr^2 - vT^2/f")
print("    (a* = 2 f vT vr / (f g) blows up at g = 0: |f_T| = f |f_r|).")

# ===================================================================== C3
# constrained classes (NOT exact solutions; the banked library's homes).
# (i) diagonal-evolution class: a,b eliminated; q = 0, w frozen:
Hd = sp.hessian(Lab.subs(q, 0), (vT, vr, vh))
Hd_diag = [sp.simplify(Hd[i, i]) for i in range(3)]
check("C3a: diagonal-evolution Hessian = -(c/4) sqrt(B) sqrt(A)/f * "
      "diag(1/f^2, f, 1/(A...)) — NEGATIVE DEFINITE: ELLIPTIC in (T,r,theta)",
      all(sp.simplify(d).is_negative for d in Hd_diag) and
      all(sp.simplify(Hd[i, j]) == 0 for i in range(3) for j in range(3) if i != j))
print("    diagonal-class diag:", [sp.simplify(d) for d in Hd_diag])

# (ii) Class-B evolution: q eliminated at the static-connected cubic root,
# w frozen. Hessian signature scanned numerically over the admissible
# domain (q from the real cubic root continuously connected to q*_static).
import numpy.polynomial.polynomial as npoly
def qcubic_root(fv, Av, vrv, vhv, vTv):
    # vT^2 q^3 + (f A vr^2 + vh^2 - (A/f) vT^2) q - 2 A vr vh = 0
    c3, c1, c0 = vTv**2, fv * Av * vrv**2 + vhv**2 - (Av / fv) * vTv**2, -2 * Av * vrv * vhv
    if abs(c3) < 1e-300:
        return -c0 / c1 if c1 != 0 else None
    roots = np.roots([c3, 0.0, c1, c0])
    rts = [z.real for z in roots if abs(z.imag) < 1e-9 * max(1, abs(z))]
    if not rts:
        return None
    qstat = 2 * Av * vrv * vhv / (fv * Av * vrv**2 + vhv**2)
    return min(rts, key=lambda z: abs(z - qstat))

fL, AL, qL = sp.symbols('fL AL qL', positive=True, real=True)
qS = sp.Symbol('qS', real=True)
D2L = AL / fL - qS**2
PL = AL * vr**2 - 2 * qS * vr * vh + vh**2 / fL
RL = fL * PL + D2L * vT**2
LB = -RL / sp.sqrt(fL * D2L)      # measure prefactor (c/8)sqrt(B)/f > 0 dropped
LB_f = sp.lambdify((vT, vr, vh, qS, fL, AL), LB, 'numpy')
hess_syms = sp.hessian(LB, (vT, vr, vh))
hess_f = sp.lambdify((vT, vr, vh, qS, fL, AL), hess_syms, 'numpy')
dLdq_f = sp.lambdify((vT, vr, vh, qS, fL, AL), sp.diff(LB, qS), 'numpy')
gradv_f = sp.lambdify((vT, vr, vh, qS, fL, AL),
                      [sp.diff(LB, vT), sp.diff(LB, vr), sp.diff(LB, vh)], 'numpy')

rng = np.random.default_rng(7)
Q_f = sp.lambdify((vT, vr, vh, qS, fL, AL),
                  fL * PL - D2L * vT**2, 'numpy')
sigs = {}
n_match = 0
n_tot = 0
for _ in range(20000):
    fv = float(np.exp(rng.uniform(np.log(0.05), np.log(20.0))))
    Av = float(np.exp(rng.uniform(np.log(0.05), np.log(20.0))))
    vrv, vhv, vTv = rng.normal(size=3) * 10**rng.uniform(-1, 1, size=3)
    qv = qcubic_root(fv, Av, vrv, vhv, vTv)
    if qv is None:
        continue
    if Av / fv - qv**2 <= 1e-10:
        continue
    dq = 1e-6 * max(1.0, abs(qv))
    if Av / fv - (abs(qv) + dq)**2 <= 0:
        continue
    Hvv = np.array(hess_f(vTv, vrv, vhv, qv, fv, Av), float)
    Hvq = (np.array(gradv_f(vTv, vrv, vhv, qv + dq, fv, Av), float)
           - np.array(gradv_f(vTv, vrv, vhv, qv - dq, fv, Av), float)) / (2 * dq)
    Lq = lambda qx: LB_f(vTv, vrv, vhv, qx, fv, Av)
    Hqq = (Lq(qv + dq) - 2 * Lq(qv) + Lq(qv - dq)) / dq**2
    if abs(Hqq) < 1e-8 or not np.isfinite(Hqq):
        continue
    Heff = Hvv - np.outer(Hvq, Hvq) / Hqq
    if not np.all(np.isfinite(Heff)):
        continue
    ev = np.linalg.eigvalsh(Heff)
    sig = tuple(int(np.sign(e)) for e in ev)
    sigs[sig] = sigs.get(sig, 0) + 1
    n_tot += 1
    Qv = Q_f(vTv, vrv, vhv, qv, fv, Av)
    # branch bookkeeping: on Q<0 the eliminated L carries the opposite
    # overall sign, so the (-,-,-) computed here is (+,+,+) physically —
    # DEFINITE either way: ELLIPTIC.
    if (Qv > 0 and sig == (-1, -1, 1)) or (Qv < 0 and sig == (-1, -1, -1)):
        n_match += 1
print("    Class-B evolution Hessian signatures over admissible scan:", sigs)
print(f"    sign(Q) classification: {n_match}/{n_tot} exact")
check("C3b: Class-B evolution is MIXED TYPE with type boundary EXACTLY at "
      "the time-row sonic surface Q = fP - D2 vT^2 = 0: Q>0 Lorentzian "
      "(-,-,+) [theta timelike], Q<0 definite [elliptic]",
      n_tot > 5000 and n_match == n_tot)

# static-slice exact confirmation of the (-,-,+) signature:
LBstat = LB.subs(qS, 2 * AL * vr * vh / (fL * AL * vr**2 + vh**2))
# at vT=0 the q* root is exact; Hessian there:
Hs = sp.hessian(LBstat, (vT, vr, vh))
pt = {vT: 0, vr: Ra(1), vh: Ra(1, 3), fL: Ra(2), AL: Ra(3)}
Hs_num = np.array(sp.Matrix(Hs).subs(pt).evalf(), float)
evs = np.linalg.eigvalsh(Hs_num)
check("C3c: exact static-slice Class-B Hessian signature (-,-,+) "
      "(sample, exact q*)", (evs[0] < 0) and (evs[1] < 0) and (evs[2] > 0))
print("    static-slice eigenvalues:", evs)

# ===================================================================== C4
print()
print("CHARACTER / WELL-POSEDNESS RULING:")
print("  (1) EXACT BRANCH (the only solutions): quasilinear ELLIPTIC in")
print("      (T, r): r^2 phi_TT + (r^2 f^2 phi_r)' + 2 r^2 f^2 phi_r^2 = 0.")
print("      The T-Cauchy IVP is ILL-POSED (Hadamard); the natural problems")
print("      are 4D BOUNDARY-VALUE problems. Cells do not 'evolve'; they")
print("      EQUILIBRATE in spacetime. (Consistent with the banked weld")
print("      'elliptic on-shell' reading and the S2 relaxation ladder.)")
print("  (2) DIAGONAL-EVOLUTION CLASS (banked library home): elliptic in")
print("      ALL of (T, r, theta) — no IVP at all; pure BVP/relaxation.")
print("  (3) CLASS-B EVOLUTION (q eliminated, w frozen): MIXED TYPE,")
print("      partitioned EXACTLY by the time-row sonic surface Q = 0:")
print("      Q > 0 (subsonic): Lorentzian (-,-,+) with THETA timelike —")
print("      the well-posed Cauchy march is ANGULAR (P1's exterior-data-")
print("      propagates-inward, with T joining r as a second elliptic")
print("      direction); Q < 0 (supersonic): definite/elliptic. T-IVP is")
print("      ill-posed everywhere. NO sector of C1 alone propagates")
print("      hyperbolically in T.")
print("  Degeneracy/sonic loci: f = 0 (seal), r = 0 (core), g = f vr^2 -")
print("  vT^2/f = 0 (time-row elimination boundary, a* singular), D2 = 0")
print("  (P1 corner), plus the Class-B cubic-discriminant fold where the")
print("  static-connected q-root merges with a spurious branch.")

print()
print("PASS:", len(PASS), " FAIL:", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
    raise SystemExit(1)
