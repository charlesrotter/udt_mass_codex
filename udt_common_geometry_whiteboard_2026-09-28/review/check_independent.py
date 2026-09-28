"""CGW1 reviewer calculation from original metrics; no author imports."""
import json
import sys
import sympy as s

records = []
def norm(v):
    return s.factor(s.simplify(s.expand_trig(v)))
def zero(label, values):
    vals = list(values) if isinstance(values, (list, tuple, s.MatrixBase)) else [values]
    residuals = [norm(v) for v in vals]
    bad = [str(v) for v in residuals if v != 0]
    records.append(dict(label=label, components=len(vals), residuals=bad or ['EXACT_ZERO']))
    if bad:
        raise RuntimeError((label, bad))
def reject(label, expression, point):
    value = norm(expression.subs(point))
    records.append(dict(label=label, rejected_residual=str(value), point={str(k):str(v) for k,v in point.items()}))
    if value == 0:
        raise RuntimeError(('FALSE_PASS', label))
def geometry(g, coords):
    n=len(coords); inv=g.inv()
    C=[[[norm(sum(inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(n))/2) for c in range(n)] for b in range(n)] for a in range(n)]
    R=[[[[norm(s.diff(C[a][d][b],coords[c])-s.diff(C[a][c][b],coords[d])+sum(C[a][c][e]*C[e][d][b]-C[a][d][e]*C[e][c][b] for e in range(n))) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Ric=s.Matrix(n,n,lambda b,d: norm(sum(R[a][b][a][d] for a in range(n))))
    return C,R,Ric,norm(s.trace(inv*Ric))
def acceleration(C, vec, coords):
    n=len(coords)
    return s.Matrix([norm(sum(vec[b]*s.diff(vec[a],coords[b]) for b in range(n))+sum(C[a][b][c]*vec[b]*vec[c] for b in range(n) for c in range(n))) for a in range(n)])

t,x,y,z,k=s.symbols('t x y z k',real=True)
L,ell,E,a,b=s.symbols('L ell E a b',positive=True)
coords=[t,x,y,z]; eta=s.diag(-1,1,1,1)
u=1+k*(-t*t+x*x+y*y+z*z)/2
g=eta/u**2
C,R,Ric,scalar=geometry(g,coords)
zero('C1_original_Ricci', Ric-6*k*g)
zero('C1_original_scalar', scalar-24*k)
zero('C1_all_constant_curvature_components', [R[i][j][m][n]-2*k*((1 if i==m else 0)*g[j,n]-(1 if i==n else 0)*g[j,m]) for i in range(4) for j in range(4) for m in range(4) for n in range(4)])
U=s.Matrix([u,0,0,0]); K=u**2*s.Matrix([1,-1,0,0]); freq=norm(-(U.T*g*K)[0])
zero('C1_unit_observer', (U.T*g*U)[0]+1)
zero('C1_null_affine_original', [(K.T*g*K)[0],*acceleration(C,K,coords)])
cone={t:-ell,x:ell,y:0,z:0}
zero('C1_cone_frequency_and_factor', [u.subs(cone)-1,freq.subs(cone)-1])
zero('C1_cone_screen_tide', [sum(R[i][j][m][i]*K[j]*K[m] for j in range(4) for m in range(4)).subs(cone) for i in [2,3]])
uo=u.subs({x:0,y:0,z:0});ue=u.subs({t:t-L,x:L,y:0,z:0})
ratio=norm(ue/uo);width=L/ue
zero('C1_neighbor_arrival_drift',[(uo*s.diff(ratio,t)).subs(t,0)-k*L,(uo*s.diff(width,t)).subs(t,0)+k*L**2,(uo*s.diff(ratio*width,t)).subs(t,0)])
emit=u.subs({t:0,x:0,y:0,z:0});relay=u.subs({t:L,x:L,y:0,z:0});receive=u.subs({t:2*L,x:0,y:0,z:0})
zero('C1_actual_future_relay',[emit/relay-1,relay/receive-1/(1-2*k*L**2)])
reject('catch_reversed_clock_ratio', (uo*s.diff(1/ratio,t)).subs(t,0)-k*L,{k:s.Rational(1,10),L:1})
reject('catch_future_return_is_inverse', relay/receive-relay/emit,{k:s.Rational(1,10),L:1})
reject('catch_wrong_curvature_coefficient',scalar-12*k,{k:s.Rational(1,10)})
zero('C1_affine_reparameterization',s.diff(ell/(a*(a+b*ell)),ell)-1/(a+b*ell)**2)

f=s.exp(k*t*t); gg=f**2*eta
CC,RR,_,_=geometry(gg,coords)
te=s.symbols('te',real=True);Ce=s.exp(k*te*te)
KK=Ce/f**2*s.Matrix([1,1,0,0]); UU=s.Matrix([1/f,0,0,0])
zero('C2_original_null_affine',[(KK.T*gg*KK)[0],*acceleration(CC,KK,coords)])
omega=norm(-(UU.T*gg*KK)[0])
zero('C2_normalized_clock_slope',-s.diff(s.log(omega),t)*KK[0]/omega-s.diff(f,t)/f**2)
tide=norm(sum(RR[2][j][2][n]*KK[j]*KK[n] for j in range(4) for n in range(4)))
zero('C2_original_screen_tide',tide-Ce**2*(2*s.diff(f,t)**2-f*s.diff(f,t,2))/f**6)
D=f*(t-te); Dp=KK[0]*s.diff(D,t);Dpp=KK[0]*s.diff(Dp,t)
zero('C2_original_Jacobi_residual_and_vertex',[Dpp+tide*D,D.subs(t,te),Dp.subs(t,te)-1])
reject('catch_unnormalized_clock_slope',-s.diff(s.log(omega),t)*KK[0]-s.diff(f,t)/f**2,{k:1,t:1,te:0})
reject('catch_wrong_screen_frequency', (Dp/Ce).subs(t,te)-1,{k:1,te:1})
L1,L2=s.symbols('L1 L2',positive=True)
logratio=lambda T,l:k*((T+l)**2-T**2)
zero('C2_carried_composition',logratio(t,L1+L2)-logratio(t,L1)-logratio(t+L1,L2))
reject('catch_uncarried_composition',logratio(t,L1+L2)-logratio(t,L1)-logratio(t,L2),{k:1,L1:1,L2:2})
zero('C2_emission_reception_and_return',[logratio(0,L)-k*L**2,logratio(-L,L)+k*L**2,logratio(L,L)-3*k*L**2])

q=s.symbols('q',real=True);N=s.Function('N')(q);g2=s.diag(-N**2,1)
C2,R2,Ric2,Sc2=geometry(g2,[t,q]);ray=s.Matrix([E/N**2,E/N])
zero('H_original_curvature',Sc2+2*s.diff(N,q,2)/N)
zero('H_original_null_affine',[(ray.T*g2*ray)[0],*acceleration(C2,ray,[t,q])])
v,ss,h=s.symbols('v ss h',real=True)
ext=s.Matrix([[-(1-h*ss)**2,1],[1,0]])
CE,RE,RicE,ScE=geometry(ext,[v,ss])
zero('H_regular_extension',[ext.det()+1,ScE+2*h**2,*acceleration(CE,s.Matrix([0,-E]),[v,ss])])
beta=s.symbols('beta',positive=True);gam=1/s.sqrt(1-beta**2)
received=1/((1-beta)*gam)
zero('SR_actual_forward_return',received-gam*(1+beta))
reject('catch_Doppler_equals_gamma',received-gam,{beta:s.Rational(3,5)})
print(json.dumps({'python':sys.version,'sympy':s.__version__,'metric_shapes':['4x4','4x4','2x2','2x2'],'Riemann_shape':'4x4x4x4','method':'original-coordinate metric differentiation; no author scientific routine','groups':records,'checks':len(records)},indent=2))
