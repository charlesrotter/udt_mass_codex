"""Independent NR2 geometry: no candidate imports, upper-half-plane chart.

All constants/coordinates below are FREE mathematical test parameters or
SOURCED background quantities. No physical equation is introduced; H/M are
the G303 constraints in the admitted conditional vacuum sector.
"""
import json
import platform
import sympy as s

x = s.symbols('x', real=True)
a, b = s.symbols('a b', positive=True)
p, c, q, ell, u, v = [s.Function(z)(x) for z in ('p','c','q','ell','u','v')]
G = s.Matrix([[s.exp(2*p), 2*c*s.exp(2*p)],
              [2*c*s.exp(2*p), s.exp(-2*p)+4*c*c*s.exp(2*p)]])
Gi = s.simplify(G.inv())
Cp = Gi*G.diff(p)
Cc = Gi*G.diff(c)
B = s.simplify((Gi*G.diff(x))/2)
S = s.simplify((Cp*u+Cc*v)/2)
gamma = s.diag(a*a, 1, 1)
gamma[1:3,1:3] = b*b*G
inv = s.simplify(gamma.inv())
Kmix = s.diag(ell, q, q)
Kmix[1:3,1:3] += S
K = s.simplify(gamma*Kmix)
tau = s.trace(Kmix)

def D(z,i):
    return s.diff(z,x) if i==0 else s.S.Zero

Gamma = [[[s.simplify(sum(inv[i,l]*(D(gamma[l,k],j)+D(gamma[l,j],k)
               -D(gamma[j,k],l)) for l in range(3))/2)
          for k in range(3)] for j in range(3)] for i in range(3)]
Ric = s.Matrix(3,3,lambda i,j: s.simplify(sum(
    D(Gamma[k][i][j],k)-D(Gamma[k][i][k],j)+sum(
        Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k]
        for l in range(3)) for k in range(3))))
R = s.simplify(sum(inv[i,j]*Ric[i,j] for i in range(3) for j in range(3)))
M = [s.simplify(sum(D(Kmix[j,i],j)+sum(
    Gamma[j][j][l]*Kmix[l,i]-Gamma[l][j][i]*Kmix[j,l]
    for l in range(3)) for j in range(3))-D(tau,i)) for i in range(3)]
H = s.simplify(R+tau*tau-s.trace(Kmix*Kmix))
checks = []
def check(name, predicate):
    ok = bool(predicate)
    checks.append({'name':name,'pass':ok})
    assert ok, name

def zero(expr):
    return s.simplify(expr)==0

check('determinant_one', zero(G.det()-1))
check('K_symmetric', all(zero(z) for z in K-K.T))
check('shape_tracefree', zero(s.trace(S)))
check('full_coordinate_scalar', zero(R+2*(p.diff(x)**2+s.exp(4*p)*c.diff(x)**2)/a**2))
check('full_coordinate_all_momenta', all(zero(z) for z in s.Matrix(M)-s.Matrix([
    -2*q.diff(x)-2*(p.diff(x)*u+s.exp(4*p)*c.diff(x)*v),0,0])))
check('full_coordinate_Hamiltonian', zero(H-(R+4*ell*q+2*q*q-2*(u*u+s.exp(4*p)*v*v))))
check('B_shape_pairing', zero(s.trace(B*S)-2*(p.diff(x)*u+s.exp(4*p)*c.diff(x)*v)))

eps,T = s.symbols('eps T', real=True, nonzero=True)
fp,fc,vp,vc = [s.Function(z)(x) for z in ('fp','fc','vp','vc')]
# The cotangent map compensates the target metric, exactly at all eps.
cotangent = {p:eps*fp,c:eps*fc,u:-eps*vp,v:-eps*s.exp(-4*eps*fp)*vc}
pair = s.simplify(s.trace(B*S).subs(cotangent).doit())
target_pair=-2*eps**2*(fp.diff(x)*vp+fc.diff(x)*vc)
check('exact_not_quadratic_cotangent_pairing', zero(pair-target_pair))
completed_qx=eps**2*(fp.diff(x)*vp+fc.diff(x)*vc)
check('full_exact_axial_momentum_completion', zero(M[0].subs(cotangent).doit().subs(q.diff(x),completed_qx)))
Lam=s.symbols('Lambda')
ell_completion=(2*Lam-R-2*q*q+s.trace(S*S))/(4*q)
check('full_exact_hamiltonian_completion_all_Lambda', zero(H.subs(ell,ell_completion)-2*Lam))

# A directly parameterized full datum gives the inherited gamma/K tangent.
q0=-s.Rational(2,3)/T
q2=s.Function('q2')(x)
subdata={**cotangent,q:q0+eps**2*q2}
gdata=gamma.subs(subdata).doit()
ldata=s.simplify(ell_completion.subs(Lam,0).subs(subdata).doit())
kdata=K.subs(subdata).subs(ell,ldata).doit()
expected_h=s.zeros(3)
expected_h[1:3,1:3]=2*b*b*s.Matrix([[fp,fc],[fc,-fp]])
expected_k=s.zeros(3)
expected_k[1:3,1:3]=b*b*(2*q0*s.Matrix([[fp,fc],[fc,-fp]])-s.Matrix([[vp,vc],[vc,-vp]]))
check('full_metric_tangent', all(zero(z) for z in gdata.diff(eps).subs(eps,0)-expected_h))
check('full_K_tangent_including_longitudinal', all(zero(z) for z in kdata.diff(eps).subs(eps,0)-expected_k))
check('background_longitudinal_K', zero(ldata.subs(eps,0)-1/(3*T)))

# Fourier means are integrated directly, including both polarizations.
ac,bc,ad,bd,vc0,vs0,vd,ve=s.symbols('ac bc ad bd vc vs vd ve', real=True)
Fs=s.Matrix([ac*s.cos(x)+bc*s.sin(x),ad*s.cos(x)+bd*s.sin(x)])
Vs=s.Matrix([vc0*s.cos(x)+vs0*s.sin(x),vd*s.cos(x)+ve*s.sin(x)])
forcing=s.expand((Fs.diff(x).T*Vs)[0])
period_integral=s.integrate(forcing,(x,0,2*s.pi))
Q=vc0*bc-vs0*ac+vd*bd-ve*ad
check('direct_whole_period_integral', zero(period_integral-s.pi*Q))
cancellation={ac:1,bc:0,ad:0,bd:1,vc0:0,vs0:1,vd:1,ve:0}
check('nontrivial_cross_polarization_cancellation', Q.subs(cancellation)==0 and (vc0*bc-vs0*ac).subs(cancellation)!=0)

# Actual false-pass attacks, each evaluated against independently derived data.
mutants=[]
def reject(name,expr):
    rejected=not zero(expr)
    mutants.append({'name':name,'rejected':rejected})
    assert rejected,name
reject('remove_cotangent_weight', s.trace(B*S).subs({p:eps*fp,c:eps*fc,u:-eps*vp,v:-eps*vc}).doit()-target_pair)
reject('reverse_periodic_primitive_sign',M[0].subs(cotangent).doit().subs(q.diff(x),-completed_qx))
reject('omit_connection_pairing',M[0]+2*q.diff(x))
reject('omit_spatial_curvature_in_H',H.subs(ell,(2*Lam-2*q*q+s.trace(S*S))/(4*q))-2*Lam)
reject('omit_cross_polarization_from_mean',period_integral-s.pi*(vc0*bc-vs0*ac))
reject('wrong_full_K_tangent',kdata.diff(eps).subs(eps,0)[1,2]+b*b*vc)

print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
    'chart':'upper-half-plane G=[[exp(2p),2c exp(2p)],[2c exp(2p),exp(-2p)+4c² exp(2p)]]',
    'coordinate_scalar':str(R),'coordinate_momenta':[str(z) for z in M],
    'coordinate_hamiltonian':str(H),'exact_pairing':str(pair),
    'period_integral':str(period_integral),'checks':checks,'mutants':mutants},indent=2))
