import json
import platform
import sympy as s

t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z)
A=1+t+x
R=1+2*x-t-t*t
eta=s.diag(-1,1,1,1)
g=A*A*eta
gi=eta/(A*A)
fgrad=[s.diff(A,c)/A for c in coords]
Gamma=[[[s.KroneckerDelta(a,b)*fgrad[c]+s.KroneckerDelta(a,c)*fgrad[b]
          -eta[b,c]*sum(eta[a,d]*fgrad[d] for d in range(4))
          for c in range(4)] for b in range(4)] for a in range(4)]
U=s.Matrix([1/A,0,0,0])
V=s.Matrix([(R+1/R)/(2*A),(R-1/R)/(2*A),0,0])
k=s.Matrix([1/A**2,1/A**2,0,0])
checks=[]
def norm(expr):return s.factor(s.cancel(expr))
def check(name,expr):
    val=norm(expr)
    if val!=0:raise AssertionError((name,val))
    checks.append(name)
def nabla_down(W):
    Wd=g*W
    return s.Matrix(4,4,lambda a,b:s.diff(Wd[b],coords[a])-
                    sum(Gamma[c][a][b]*Wd[c] for c in range(4)))
def scalar(W,D):return (W.T*D*W)[0]
def dirder(W,expr):return sum(W[a]*s.diff(expr,coords[a]) for a in range(4))

check('base_unit',scalar(U,g)+1)
check('tilted_unit',scalar(V,g)+1)
check('ray_null',scalar(k,g))
for a in range(4):
    check('ray_affine_'+str(a),dirder(k,k[a])+
          sum(Gamma[a][b][c]*k[b]*k[c] for b in range(4) for c in range(4)))
omega=-(k.T*g*U)[0]
omegat=norm(-(k.T*g*V)[0])
check('base_frequency',omega-1/A)
check('tilted_frequency',omegat-1/(A*R))
K=norm(scalar(k,nabla_down(U))/omega**2)
Kt=norm(scalar(k,nabla_down(V))/omegat**2)
# dt/dlambda=A^-2; direct affine pullback length density is omega*A².
Ldot=norm(omega*A*A)
Ltdot=norm(omegat*A*A)
b=norm(omegat/omega)
dlogb=norm((s.diff(b,t)+s.diff(b,x))/b)
check('base_generator_pullback',K*Ldot-2/A)
check('tilted_generator_pullback',Kt*Ltdot-(2/A+(s.diff(R,t)+s.diff(R,x))/R))
check('observer_change_identity',Kt*Ltdot-K*Ldot+dlogb)
check('observer_length_change',Ltdot-b*Ldot)
check('matching_initial_clock',b.subs({t:0,x:0})-1)
check('matching_final_clock',b.subs({t:1,x:1})-1)

# Full coordinate Ricci and commutation contraction (7), evaluated after
# differentiation at a rational point where all fields are regular.
point={t:s.Rational(1,2),x:s.Rational(1,2),y:0,z:0}
M=s.Matrix(4,4,lambda a,b:s.diff(V[b],coords[a])+
           sum(Gamma[b][a][c]*V[c] for c in range(4)))
theta=norm(s.trace(M))
acc=s.Matrix([norm(sum(V[a]*M[a,b] for a in range(4))) for b in range(4)])
divacc=sum(s.diff(acc[a],coords[a])+
           sum(Gamma[a][a][b]*acc[b] for b in range(4)) for a in range(4))
ric=s.Matrix(4,4,lambda b,d:sum(s.diff(Gamma[a][b][d],coords[a])-
          s.diff(Gamma[a][a][d],coords[b])+
          sum(Gamma[a][a][e]*Gamma[e][b][d]-Gamma[a][b][e]*Gamma[e][a][d]
              for e in range(4)) for a in range(4)))
RicVV=(V.T*ric*V)[0]
mm=s.trace(M*M)
check('full4d_commutator_Raychaudhuri',
      (divacc-dirder(V,theta)-mm-RicVV).subs(point))

# Two explicit sensitivities must reject wrong identities at a regular point.
wrong_sign=norm((Kt*Ltdot-K*Ldot-dlogb).subs({t:s.Rational(1,4),x:s.Rational(1,4)}))
wrong_length=norm((Kt*Ldot-K*Ldot+dlogb).subs(point))
assert wrong_sign!=0 and wrong_length!=0
checks.extend(['reject_wrong_observer_correction_sign','reject_omitted_length_jacobian'])

# Closed-null branch on (t,x) periodic with equal positive periods: at lambda
# one period, the geometric event repeats. Distinct future endpoint clocks
# are allowed comparison data but cannot be one vector field at that event.
ue=s.Matrix([1,0,0,0]);uo=s.Matrix([s.Rational(5,4),s.Rational(3,4),0,0])
kk=s.Matrix([1,1,0,0])
check('closed_branch_emitter_unit',scalar(ue,eta)+1)
check('closed_branch_receiver_unit',scalar(uo,eta)+1)
Ze=-(ue.T*eta*kk)[0];Zo=-(uo.T*eta*kk)[0]
check('closed_branch_regular_clock_ratio',Ze/Zo-2)
assert ue!=uo and Ze>0 and Zo>0
checks.append('distinct_endpoint_vectors_cannot_share_single_value')

print(json.dumps({'status':'PASS','count':len(checks),'checks':checks,
 'wrong_sign_residual':str(wrong_sign),'wrong_length_residual':str(wrong_length),
 'python':platform.python_version(),'sympy':s.__version__,
 'author_code_exposed':False,'evidence':'exact symbolic/rational controls'},indent=2))
