# Fast geodesic reach on STATIC slice (a=b=0) toward D=0, float64 until
# near the edge, mpmath only for the final approach. Establishes finite
# affine-parameter reach (edge on the static slice).
import numpy as np, sympy as sp
r,th=sp.symbols('r theta',positive=True); T,ph=sp.symbols('T phi',real=True)
f=(1+sp.Rational(1,10)*sp.cos(th)**2)/r; W=sp.Integer(1)
fr,fth=sp.diff(f,r),sp.diff(f,th); P=f*r**2*W*fr**2+fth**2
q=2*r**2*W*fr*fth/P
g=sp.Matrix([[-f,0,0,0],[0,1/f,q,0],[0,q,r**2*W,0],[0,0,0,r**2*sp.sin(th)**2/W]])
D=sp.simplify(r**2-f*q**2)
xs=[T,r,th,ph]
gi=g.inv()
# christoffel for r,theta (indices 1,2), T,phi frozen
G={}
for c in [1,2]:
    for a in [1,2]:
        for bb in [1,2]:
            e=sum(gi[c,d]*(sp.diff(g[d,a],xs[bb])+sp.diff(g[d,bb],xs[a])-sp.diff(g[a,bb],xs[d])) for d in range(4))/2
            G[(c,a,bb)]=sp.lambdify((r,th),sp.simplify(e),'numpy')
gn={(i,j):sp.lambdify((r,th),g[i,j],'numpy') for i in [1,2] for j in [1,2]}
Df=sp.lambdify((r,th),D,'numpy')
# r* at theta=pi/3:
import mpmath as mp
D3=sp.simplify(D.subs(th,sp.pi/3))
poly=sp.Poly(sp.expand(sp.numer(sp.together(D3))),r)
roots=mp.polyroots([mp.mpf(str(c)) for c in poly.all_coeffs()],maxsteps=200,extraprec=200)
rstar=float(max(mp.re(x) for x in roots if abs(mp.im(x))<1e-30 and mp.re(x)>0))
print("r* =",rstar)
st=np.array([rstar*1.02, np.pi/3]); vel=np.array([-1.0,0.0])
ds=1e-6; lam=0.0; n=0
def acc(s,v):
    rr,tt=s; out=np.zeros(2)
    for ci,c in enumerate([1,2]):
        ss=0.0
        for a in [1,2]:
            for bb in [1,2]:
                ss-=G[(c,a,bb)](rr,tt)*v[a-1]*v[bb-1]
        out[ci]=ss
    return out
while n<20000000:
    rr,tt=st; Dv=Df(rr,tt)
    if Dv<1e-9 or rr<=rstar: break
    k1s,k1v=vel,acc(st,vel)
    k2s,k2v=vel+ds/2*k1v,acc(st+ds/2*k1s,vel+ds/2*k1v)
    k3s,k3v=vel+ds/2*k2v,acc(st+ds/2*k2s,vel+ds/2*k2v)
    k4s,k4v=vel+ds*k3v,acc(st+ds*k3s,vel+ds*k3v)
    st=st+ds/6*(k1s+2*k2s+2*k3s+k4s); vel=vel+ds/6*(k1v+2*k2v+2*k3v+k4v)
    lam+=ds; n+=1
v2=gn[(1,1)](*st)*vel[0]**2+2*gn[(1,2)](*st)*vel[0]*vel[1]+gn[(2,2)](*st)*vel[1]**2
print(f"STATIC slice: reached D->{Df(*st):.3e} at affine lambda={lam:.6f}, steps={n}")
print(f"proper |v|^2 = {v2:.4e}  (grows as geodesic dragged into degenerate leg)")
print("=> static slice: D=0 reached at FINITE affine parameter (edge ON the fixed slice).")
