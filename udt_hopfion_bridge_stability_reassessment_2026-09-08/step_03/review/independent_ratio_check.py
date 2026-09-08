"""G331 metric inversion -> HB2 jet -> angular quotient; no author imports."""
import json
import platform
import sys
import sympy as s

x, p, q = s.symbols('x p q', positive=True)
gap, root, norm = s.symbols('gap root norm', nonzero=True)
F = p*x+q*(1-x)
eta = s.Matrix([x/F, (1-x)/F])
zeta = s.Matrix([q/F, -p/F])
H = x*(1-x)/F*zeta*zeta.T+eta*eta.T
Hinv = H.inv().applyfunc(s.factor)
R = 24*p*q/F-8*(p+q)-2
xi = s.Matrix([p, q])
JgradR = (Hinv*eta.diff(x)*2*x*(1-x)*F*s.diff(R,x)).applyfunc(s.factor)
Y = JgradR*5/(2*gap*root)
Vdot = Y+norm*xi
ratio_jet = s.factor((Vdot[0]*q-p*Vdot[1])/q**2)
expected = -120*p*(p-q)/(q*gap*root)
assert s.factor(ratio_jet-expected) == 0
assert s.diff(ratio_jet,norm) == 0
assert (H*xi-eta).applyfunc(s.factor) == s.zeros(2,1)
assert (JgradR-2*F*s.diff(R,x)*s.Matrix([1-x,-x])).applyfunc(s.factor) == s.zeros(2,1)
u,d = s.symbols('u d', real=True)
denominator_square = s.expand((6-u)**2*(u+d)/2)
assert s.Poly(denominator_square,u).nth(3) == s.Rational(1,2)

records=[]
for pp,qq,xx in [(s.Rational(1,4),s.Rational(1,2),s.Rational(2,5)),
                 (s.Rational(1,2),s.Rational(1,4),s.Rational(3,5)),
                 (s.Rational(3),s.Rational(4),s.Rational(1,3)),
                 (s.Rational(1,2),s.Rational(1,2),s.Rational(2,3))]:
  rr=s.factor(R.subs({p:pp,q:qq,x:xx})); gg=(6-rr)/2
  ends=[s.factor(R.subs({p:pp,q:qq,x:z})) for z in [0,1]]
  assert (6-ends[0])*(6-ends[1])>0
  for cc in [-3,3]:
    for dd in [-16,16]:
      ll=rr/2+cc**2-s.Rational(dd**2,4)
      assert min([2*(r+2*cc**2-2*ll) for r in ends])>0
      sub={p:pp,q:qq,x:xx,gap:gg,root:dd,norm:s.Rational(dd,2)}
      val=s.factor(ratio_jet.subs(sub))
      wrong=s.factor(val*s.Rational(3,5))
      if pp!=qq:
        assert val!=0 and val!=-val and val!=wrong
      else:
        assert val==0
      records.append(dict(weights=[str(pp),str(qq)],x=str(xx),C=str(cc),
        root=str(dd),Lambda=str(ll),R=str(rr),gap=str(gg),
        Y=[str(s.factor(v.subs(sub))) for v in Y],ratio_derivative=str(val),
        wrong_coefficient_residual=str(val-wrong),global_gap=True,global_root=True))
print(json.dumps(dict(kind='exact metric-inversion and quotient algebra; finite anchors',
  ratio_derivative=str(ratio_jet),denominator_square=str(denominator_square),
  records=records,versions=dict(python=sys.version,sympy=s.__version__,
  platform=platform.platform())),indent=2))
