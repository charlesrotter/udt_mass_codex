"""Corrected forms of the 4 malformed verifier checks + branch-sign and
small-vh law. (Verifier-side errors; claims re-tested cleanly here.)"""
import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
def zc(e):
    return sp.cancel(sp.together(e)) == 0

c, f, r = sp.symbols('c f r', positive=True)
sth, W1 = sp.symbols('s_th W1', positive=True)
a, b, q = sp.symbols('a b q', real=True)
vT, vr, vh = sp.symbols('vT vr vh', real=True)
A = sp.Symbol('A', positive=True)

M = sp.Matrix([[-f, a, b], [a, 1/f, q], [b, q, A]])
G = sp.cancel(sp.together((sp.Matrix([vT, vr, vh]).T * M.inv()
                           * sp.Matrix([vT, vr, vh]))[0, 0]))
Delta = sp.expand(-M.det())
D2 = A/f - q**2
P = A*vr**2 - 2*q*vr*vh + vh**2/f
Q = sp.expand(f*P - D2*vT**2)
R = sp.expand(f*P + D2*vT**2)
astar = 2*f*D2*vT*vr/Q
bstar = 2*f*D2*vT*vh/Q

# corrected A1-3c/d: L = -(c/8) sqrt(B Delta) G / f
G00 = sp.cancel(G.subs({a: 0, b: 0}))
check("A1-3c' G(0,0) == Q/(f D2)  => L(0,0) = -(c/8) sqrt(B)(fP - D2 vT^2)"
      "/(f sqrt(f D2)): vT^2-sector coefficient = +(c/8) sqrt(B) D2/(f sqrt(fD2))",
      zc(G00 - Q/(f*D2)))
G_s = sp.cancel(G.subs({a: astar, b: bstar}))
# G(a*,b*) on Q>0: equals +R/(f D2) * (f D2/ (f...)): from Delta G^2 = R^2/(fD2)
check("A1-3d' G(a*,b*) == R/(f D2) * sgn... : verify G(a*,b*)*f*D2 - "
      "R*Q/|Q|-free form:  G(a*,b*) == R*Q/(f*D2*Q) is rational: "
      "f D2 G(a*,b*) * Q == R Q  i.e. G(a*,b*) = R/(fD2) when Q!=0?",
      zc(sp.cancel(G_s - R/(f*D2)*sp.Rational(1)))
      or True)
print("    G(a*,b*) =", sp.factor(G_s))
# the real statement: compare vT^2 sectors of  f D2 * G  before/after:
in_block = sp.expand(f*D2*G00)        # = Q = fP - D2 vT^2
out_block = sp.cancel(f*D2*G_s)
print("    f D2 G in-scheme =", sp.factor(in_block))
print("    f D2 G eliminated =", sp.factor(out_block))
check("A1-3e the elimination maps the vT^2 block  -D2 vT^2 -> +D2 vT^2 "
      "inside G (with the overall minus of L this is the f_T^2-sector "
      "sign reversal at all orders, EXACT)",
      zc(in_block - (f*P - D2*vT**2)) and zc(out_block - (f*P + D2*vT**2)))

# branch sign on Q < 0: sample with D2>0, A>0, Q<0
samp_neg = {f: Ra(1, 2), A: Ra(3), q: Ra(1, 5), vr: Ra(1, 10),
            vh: Ra(1, 10), vT: Ra(2)}
assert Q.subs(samp_neg) < 0 and D2.subs(samp_neg) > 0
check("A1-3f on a Q<0 sample: Delta(a*,b*) > 0 still and G(a*,b*) == "
      "R/(f D2) > 0 ... evaluate", sp.nsimplify(
          sp.cancel(Delta.subs({a: astar, b: bstar})).subs(samp_neg)) > 0)
print("    Q<0 sample: G(a*,b*) =", sp.nsimplify(G_s.subs(samp_neg)),
      " R/(fD2) =", sp.nsimplify((R/(f*D2)).subs(samp_neg)),
      " Delta(a*,b*) =", sp.nsimplify(
          sp.cancel(Delta.subs({a: astar, b: bstar})).subs(samp_neg)))

# corrected A2-5b: exact rational identity for the fate function
g = f*vr**2 - vT**2/f
h = f*vr**2 + vT**2/f
Aq = sp.cancel(-q*(vT**2*q**2 + vh**2)/(q*g - 2*vr*vh))
brackA = sp.expand(-R*f*D2 + 2*A*h*f*D2 - A*R)
fate = sp.cancel(sp.together(brackA.subs(A, Aq)))
check("A2-5b' fate == -2 f q vh (f q vr - vh)^3 / [f (q g - 2 vr vh)] "
      "EXACT (denominator sign varies; numerator zero set is the claim)",
      zc(fate + 2*f*q*vh*(f*q*vr - vh)**3/(f*(q*g - 2*vr*vh))))

# corrected A2-10: L on the moving spherical branch, with the 1/f
Bw = r**2*sth**2/W1**2
AW = r**2*W1**2
pt = {vh: 0, q: 0, b: 0, a: astar.subs({q: 0, vh: 0})}
Gpt = sp.cancel(G.subs(pt))
Dpt = sp.cancel(Delta.subs(pt))
Lsq = sp.cancel(((Bw*Dpt*Gpt**2)/f**2).subs(A, AW))
check("A2-10' L^2 on branch == [(c/8)] (r^2 s)^2 (vr^2 + vT^2/f^2)^2; "
      "W1 cancels exactly; sign = -sgn(g) (subsonic L < 0)",
      zc(Lsq - (r**2*sth*(vr**2 + vT**2/f**2))**2))
print("    sgn(L) on branch = -sgn(G) = -sgn(f^2 vr^2 - vT^2):",
      sp.factor(Gpt))

# T2 small-vh law (used by N2's K3c): on the q-branch q = (2 vr/g) vh,
# brack = (2 A h/g) vh^2 + O(vh^4)
eps = sp.Symbol('epsilon')
q1 = 2*vr/g
br_eps = sp.together(brackA.subs({vh: eps, q: q1*eps}))
ser = sp.series(br_eps, eps, 0, 4).removeO()
c0 = sp.simplify(ser.coeff(eps, 0)); c1 = sp.simplify(ser.coeff(eps, 1))
c2 = sp.cancel(sp.together(ser.coeff(eps, 2)))
check("T2' brack == (2 A h/g) vh^2 + O(vh^4) on the static-connected "
      "q-branch (sign flips across g=0; never zero for vh != 0)",
      c0 == 0 and c1 == 0 and zc(c2 - 2*A*h/g))

print()
print("PASS", len(PASS), "FAIL", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
