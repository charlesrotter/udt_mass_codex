"""
Symbolic reduced functional of the genuinely-UNIT hedgehog nhat = normalize(A),
then EOM, solved numerically -> self-consistent stationary profile. This makes
translation an EXACT zero mode and the Hessian clean.
"""
import sympy as sp
r, th, ph = sp.symbols('r theta phi', positive=True)
F = sp.Function('Theta')(r)
phd = sp.Function('phidil')(r)

nA = sp.Matrix([sp.sin(F)*sp.sin(th)*sp.cos(ph),
                sp.sin(F)*sp.sin(th)*sp.sin(ph),
                sp.cos(F)])
norm = sp.sqrt(sp.simplify(nA.dot(nA)))
nhat = nA/norm

def cross(a,b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

dnr=sp.Matrix([sp.diff(c,r) for c in nhat])
dnt=sp.Matrix([sp.diff(c,th) for c in nhat])
dnp=sp.Matrix([sp.diff(c,ph) for c in nhat])
grr=sp.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*sp.sin(th)**2)
grad2=grr*dnr.dot(dnr)+gtt*dnt.dot(dnt)+gpp*dnp.dot(dnp)
e2=sp.Rational(1,2)*grad2
Srt=cross(dnr,dnt); Srp=cross(dnr,dnp); Stp=cross(dnt,dnp)
L4s=2*(grr*gtt*Srt.dot(Srt)+grr*gpp*Srp.dot(Srp)+gtt*gpp*Stp.dot(Stp))
e4=sp.Rational(1,4)*L4s
sqrtg=sp.exp(phd)*r**2*sp.sin(th)
dens=(e2+e4)*sqrtg

# integrate over ph (0,2pi) then th. phi integration:
print("integrating over phi...")
dens_ph=sp.integrate(dens,(ph,0,2*sp.pi))
dens_ph=sp.simplify(dens_ph)
print("phi done. integrating theta (numeric fallback if symbolic stalls)...")
# Try symbolic theta integral; if it stalls we'll do numeric.
import pickle
with open('unit_dens_ph.pkl','wb') as fh:
    pickle.dump(sp.srepr(dens_ph),fh)
print("DENS_PH saved. Expr (head):")
print(str(dens_ph)[:400])
