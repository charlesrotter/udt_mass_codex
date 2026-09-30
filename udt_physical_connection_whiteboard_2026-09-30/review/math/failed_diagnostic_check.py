"""Direct reviewer reconstruction; no proposal imports or author-code imports."""
import json
import platform
import sympy as s

e, v, b, te = s.symbols('epsilon v b te', real=True)
# Light coordinate speed c=e^-2epsilon; receiver interception is an affine map.
c = s.exp(-2*e)
arrival = (b+c*te)/(c-v)
emitter_rate = s.exp(-e)
receiver_rate = s.sqrt(s.exp(-2*e)-s.exp(2*e)*v**2)
Z = receiver_rate*s.diff(arrival,te)/emitter_rate
dD = s.simplify(s.diff(Z,e)/Z).subs(e,0)
assert s.simplify(dD-2*v/(1-v**2)) == 0
z0 = s.simplify(Z.subs(e,0))
assert s.simplify(z0**2-(1+v)/(1-v)) == 0
# W on +/- epsilon is reconstructed from I=48 epsilon^2, J=0.
p = s.symbols('p', positive=True)
W = (48**2*p**4)**s.Rational(1,4)
assert s.simplify(W/p-4*s.sqrt(3)) == 0

# Full Schwarzschild connection; derivative at a regular orbit point precedes
# contractions. R^a_bcd convention: d_c Gamma^a_db-d_d Gamma^a_cb+Gamma Gamma.
t, r, theta, phi = coords = s.symbols('t r theta phi', real=True)
f = 1-2/r
g = s.diag(-f,1/f,r**2,r**2*s.sin(theta)**2)
gi = g.inv()
Gamma = [[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c0],coords[b0])
    +s.diff(g[d,b0],coords[c0])-s.diff(g[b0,c0],coords[d]))
    for d in range(4))/2) for c0 in range(4)] for b0 in range(4)] for a in range(4)]
point = {r:s.Integer(3),theta:s.pi/2}
Gp = [[[Gamma[a][b0][c0].subs(point) for c0 in range(4)]
       for b0 in range(4)] for a in range(4)]
R = [[[[s.simplify(s.diff(Gamma[a][d][b0],coords[c0]).subs(point)
    -s.diff(Gamma[a][c0][b0],coords[d]).subs(point)
    +sum(Gp[a][c0][l]*Gp[l][d][b0]-Gp[a][d][l]*Gp[l][c0][b0]
    for l in range(4))) for d in range(4)] for c0 in range(4)]
    for b0 in range(4)] for a in range(4)]
Ric = s.Matrix(4,4,lambda a,b0:s.simplify(sum(R[l][a][l][b0] for l in range(4))))
assert Ric == s.zeros(4), str(Ric)
gp=g.subs(point)
k=s.Matrix([3,0,0,1/s.sqrt(3)])
screens=[s.Matrix([0,1/s.sqrt(3),0,0]),s.Matrix([0,0,s.Rational(1,3),0])]
assert (k.T*gp*k)[0] == 0
assert s.simplify(sum(Gp[1][a][b0]*k[a]*k[b0] for a in range(4) for b0 in range(4))) == 0
for i in range(2):
    assert (screens[i].T*gp*k)[0] == 0
    for j in range(2):
        assert (screens[i].T*gp*screens[j])[0] == (1 if i==j else 0)
def tidal(i,j):
    return s.simplify(sum(gp[a,a]*R[a][b0][c0][d]*k[a]*screens[i][b0]*k[c0]*screens[j][d]
        for a in range(4) for b0 in range(4) for c0 in range(4) for d in range(4)))
screen=s.Matrix(2,2,tidal)
assert screen == s.diag(-s.Rational(1,3),s.Rational(1,3))
bracket=13*(k.T*Ric*k)[0]*s.eye(2)-4*screen
assert bracket == s.diag(s.Rational(4,3),-s.Rational(4,3))
# General screen trace is basis invariant and requires no off-diagonal choice.
Rkk, shear = s.symbols('Rkk shear')
eigenvalues=[Rkk/2+shear,Rkk/2-shear]
assert s.expand(sum(13*Rkk-4*l for l in eigenvalues)) == 22*Rkk

print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'kind':'distinct reviewer reconstruction, exact symbolic comparison; not QFT',
 'shapes':{'metric':[4,4],'Riemann':[4,4,4,4],'screen':[2,2]},
 'flat_protocol_dD':str(dD),'flat_protocol_Z_squared':str(s.simplify(z0**2)),
 'W_right_slope':str(W/p),'W_left_slope':str(-W/p),
 'Schwarzschild_orbit':{'M':1,'r':3,'theta':'pi/2','affine_E':1,
 'Ricci':str(Ric),'screen':str(screen),'optical_bracket':str(bracket)},
 'omissions':['QFT loop calculation','physical state/ensemble selection','empirical tests',
 'native solution admission','full covariance/global causality proof']},indent=2))
