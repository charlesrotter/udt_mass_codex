"""
RECHECK L4 off-diagonals carefully. The first pass showed nonzero M4[01],M4[02].
Investigate: are these real (L4 breaks diagonality) or an integration/azimuthal
error? The hedgehog is axisymmetric about target-3 -> the inertia tensor MUST be
invariant under simultaneous rotation about axis-3 in BOTH target and space.
That forces diag(X,X,Y) with X for (1,2). So genuine off-diagonals would be a
RED FLAG. Check term by term.
"""
import sympy as sp
th, ph, Th, Thp, r, P = sp.symbols('theta phi Theta Theta_p r P', real=True)
# P = metric potential (renamed, NOT pi)
sT,cT=sp.sin(Th),sp.cos(Th)
n=sp.Matrix([sT*sp.sin(th)*sp.cos(ph), sT*sp.sin(th)*sp.sin(ph), cT])
e=[sp.Matrix([1,0,0]),sp.Matrix([0,1,0]),sp.Matrix([0,0,1])]
v=[ea.cross(n) for ea in e]
dn_dTh=sp.Matrix([cT*sp.sin(th)*sp.cos(ph), cT*sp.sin(th)*sp.sin(ph), -sT])
dn={'r':Thp*dn_dTh,'th':sp.Matrix([sp.diff(c,th) for c in n]),'ph':sp.Matrix([sp.diff(c,ph) for c in n])}
ginv={'r':sp.exp(-2*P),'th':1/r**2,'ph':1/(r**2*sp.sin(th)**2)}
def dot(a,b): return sp.expand_trig((a.T*b)[0])
def L4d(a,b):
    s=0
    for i in ['r','th','ph']:
        s+=ginv[i]*(dot(v[a],v[b])*dot(dn[i],dn[i])-dot(v[a],dn[i])*dot(dn[i],v[b]))
    return s
dW=sp.sin(th)
def ang(expr):
    inner=sp.integrate(sp.expand(expr*dW),(ph,0,2*sp.pi))
    return sp.simplify(sp.integrate(inner,(th,0,sp.pi)))
print("L4 off-diagonal M4[02] (raw angular integral):")
m02=ang(L4d(0,2)); print("  =",sp.simplify(m02))
print("L4 off-diagonal M4[01]:")
m01=ang(L4d(0,1)); print("  =",sp.simplify(m01))
print("\nNumeric eval at Theta=1.0 rad, Thp=0.5, r=1.0, P=0 (flat):")
sub={Th:1.0,Thp:0.5,r:1.0,P:0.0}
print("  M4[01] =",float(m01.subs(sub)))
print("  M4[02] =",float(m02.subs(sub)))
print("  M4[00] =",float(ang(L4d(0,0)).subs(sub)))
print("  M4[22] =",float(ang(L4d(2,2)).subs(sub)))
print("\nDIAGNOSIS: if M4[01],M4[02] nonzero, the L4 t-t reduction as I wrote it")
print("is NOT diagonal -> either (i) my reduction formula differs from the doc's,")
print("or (ii) genuine non-diagonality the doc missed. Check vs eigenvalues.")
# Build full 3x3 angular-integrated tensor and get eigenvalues at the sub point
M4=sp.zeros(3,3)
for a in range(3):
    for b in range(3):
        M4[a,b]=ang(L4d(a,b))
M4n=M4.subs(sub)
M4n=sp.Matrix(3,3,lambda i,j: float(M4n[i,j]))
print("\nFull L4 angular tensor at the point:")
sp.pprint(M4n)
print("eigenvalues:", [sp.re(e).evalf() for e in M4n.eigenvals()])
