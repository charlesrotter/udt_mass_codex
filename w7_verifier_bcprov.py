#!/usr/bin/env python3
"""INDEPENDENT VERIFIER — attack B: is the mirror BC DERIVED or CHOSEN,
and does it QUANTIZE or only LABEL? Re-derive sigma's action from scratch.

NO shared machinery. Own sympy. Tests:
  B-1  sigma:(a,b)->(-a,-b) involution + det g4 invariant + (f,q,w,r,th)
       block untouched (re-derive the W6 determinant myself).
  B-2  crease residual rho=(b-fqa) is ODD under sigma (the normal datum).
  B-3  on the same-minus stationary row (a*=alpha f_T, b*=(f_th/f_r)a*),
       sigma IS f_T->-f_T (time reversal). DERIVED.
  B-4  THE DECISIVE LOGIC AUDIT: the parity (even->Neumann, odd->Dirichlet
       AT THE CREASE z=0) is a CREASE condition. A crease condition on a
       symmetric operator only SPLITS the spectrum into parity towers; it
       imposes NO discreteness by itself (an operator on a HALF-LINE
       [0,inf) with one BC at 0 has a CONTINUOUS spectrum). Confirm: the
       crease BC alone (no outer wall) => continuous spectrum. Hence the
       mirror BC does NOT quantize; the outer wall does. (This is the
       smuggled-quantizer check: if the arm claimed the crease quantizes,
       that would be the failure. It does NOT claim that -- it concedes
       the outer wall quantizes. So B is HONEST but the headline overclaims
       'native'.)
"""
import sys, time
import sympy as sp
import mpmath as mp

t0 = time.time()
PASS, FAIL = [], []


def check(tag, cond, note=""):
    (PASS if cond else FAIL).append(tag)
    print(f"BP-{tag}: {'PASS' if cond else 'FAIL'}  {note}", flush=True)


r, th = sp.symbols('r theta', positive=True)
f, q, w = sp.symbols('f q w', positive=True)
a, b = sp.symbols('a b', real=True)
W = (1+w)**2
sin = sp.sin(th)
g4 = sp.Matrix([[-f, a, b, 0],
                [a, 1/f, q, 0],
                [b, q, r**2*W, 0],
                [0, 0, 0, r**2*sin**2/W]])
D = r**2*W - f*q**2
# re-derive det g4 from scratch (no import of the W6 form):
det4 = sp.cancel(sp.together(g4.det()))
det_target = -(r**2*sin**2)/(f*W)*(f*D*(1+a**2) + (b-f*q*a)**2)
check("B1det", sp.simplify(det4 - det_target) == 0,
      "det g4 = -(r sin)^2/[f(1+w)^2][f D(1+a^2)+(b-fqa)^2] re-derived "
      "from scratch (independent of the W6 record)")

sig = {a: -a, b: -b}
g4s = g4.subs(sig, simultaneous=True)
g4ss = g4s.subs(sig, simultaneous=True)
inv = sp.simplify(g4ss - g4) == sp.zeros(4, 4)
detinv = sp.simplify(g4s.det() - g4.det()) == 0
block = all(sp.simplify(g4s[i, j]-g4[i, j]) == 0 for (i, j) in
            [(0, 0), (1, 1), (2, 2), (3, 3), (1, 2), (2, 1)])
check("B1", inv and detinv and block,
      "sigma^2=id, det INVARIANT, (f,q,w) diag + (r,th) sector untouched "
      "=> sigma is a genuine class-preserving involution (mirror real)")

rho = b - f*q*a
check("B2", sp.simplify(rho.subs(sig, simultaneous=True) + rho) == 0,
      "crease residual rho=(b-fqa) is ODD under sigma (det~rho^2 even => "
      "fold regular, but rho the normal datum flips): parity DERIVED")

fT = sp.Symbol('f_T', real=True)
al, fr_, fh = sp.symbols('alpha f_r f_theta', real=True)
a_star = al*fT
b_star = (fh/fr_)*a_star
check("B3", sp.simplify(a_star.subs(fT, -fT)+a_star) == 0
      and sp.simplify(b_star.subs(fT, -fT)+b_star) == 0,
      "on same-minus stationary row sigma:(a,b)->(-a,-b) IS f_T->-f_T "
      "(time reversal). DERIVED, not chosen.")

# B-4: the DECISIVE LOGIC AUDIT. A single BC at the crease (z=0) on a
# self-adjoint operator extended to the HALF-LINE [0, infinity) gives a
# CONTINUOUS spectrum (scattering). Quantization requires the OUTER wall.
# Demonstrate numerically: PT on [0, Lbig] with crease-Dirichlet at 0 and
# NO outer wall (free/radiation at Lbig) -> dense levels (continuum).
mp.mp.dps = 30
theta = mp.mpf(1)
print("   crease-Dirichlet at 0, push the outer edge Lbig: level spacing")
prev = None
shrinks = True
sp_first = None
sp_last = None
for Lbig in [4, 8, 16, 32, 64, 128]:
    s = theta*mp.mpf(Lbig)
    stt = s*mp.tanh(s)
    Fodd = lambda x: stt*mp.cos(x) + x*mp.sin(x)
    # first two roots in kL:
    out, x, step = [], mp.mpf('1e-4'), mp.mpf('0.01')
    pr = Fodd(x); x += step
    while len(out) < 2 and x < 100:
        cu = Fodd(x)
        if (pr < 0) != (cu < 0):
            out.append(mp.findroot(Fodd, x-step/2))
        pr = cu; x += step
    dk = (out[1]-out[0])/mp.mpf(Lbig)  # k-spacing
    if sp_first is None:
        sp_first = dk
    sp_last = dk
    print(f"     Lbig={Lbig:>5}: k-spacing={mp.nstr(dk,6)}")
check("B4", sp_last < sp_first/4,
      f"CREASE BC ALONE DOES NOT QUANTIZE: with only the crease "
      f"condition (Dirichlet at z=0) and the outer edge pushed away, the "
      f"k-spacing collapses {mp.nstr(sp_first,4)}->{mp.nstr(sp_last,4)} "
      "(->0): a CONTINUUM. The mirror/crease provides PARITY only; "
      "discreteness is SUPPLIED BY THE OUTER FINITE-CELL WALL. The "
      "arm's own scripts concede this ('crease BC quantizes nothing "
      "alone; SELECTS the tower'). So B is HONEST but the 'mirror "
      "yields discreteness' framing is the outer box doing the work.")

print(f"\nBC-PROVENANCE VERIFIER: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
