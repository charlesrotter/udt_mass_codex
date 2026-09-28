"""Peer checks after candidate exposure; FREE supplied diagnostic metrics."""
import json
import platform
import sympy as s

t,x,y,z = coords=s.symbols('t x y z', real=True)
f=1+t+x*y
w=s.Matrix([1,z,x,0])
h=s.diag(0,1+x*x,1+y*y,1+z*z)
g=f*f*(h-w*w.T)
U=s.Matrix([1/f,0,0,0])
Uc=g*U
dg=[g.diff(q) for q in coords]
dUc=s.Matrix(4,4,lambda a,b:s.diff(Uc[b],coords[a]))
checks={};values={}
def zero(name,exprs):
    residual=[s.factor(s.simplify(v)) for v in exprs]
    if any(v!=0 for v in residual):raise AssertionError((name,residual))
    checks[name]='EXACT_ZERO'

for n,point in enumerate([{t:0,x:0,y:0,z:0},
                         {t:s.Rational(1,5),x:s.Rational(1,3),y:s.Rational(1,7),z:s.Rational(-1,4)}]):
    G=g.subs(point);I=G.inv();v=U.subs(point);vc=Uc.subs(point)
    D=[a.subs(point) for a in dg]
    Gam=[[[sum(I[a,d]*(D[b][d,c]+D[c][d,b]-D[d][b,c]) for d in range(4))/2
           for c in range(4)] for b in range(4)] for a in range(4)]
    Nab=dUc.subs(point)-s.Matrix(4,4,lambda a,b:sum(Gam[c][a][b]*vc[c] for c in range(4)))
    Hv=sum(I[a,b]*Nab[a,b] for a in range(4) for b in range(4))/3
    ac=s.Matrix([sum(v[a]*Nab[a,b] for a in range(4)) for b in range(4)])
    proj=s.eye(4)+vc*v.T
    rest=G+vc*vc.T
    Sig=proj*(Nab+Nab.T)*proj.T/2-Hv*rest
    vort=proj*(Nab-Nab.T)*proj.T/2
    alpha=ac-Hv*vc
    grad=s.Matrix([s.diff(f,q)/f for q in coords]).subs(point)
    zero(f'nontrivial_normal_form_unit_{n}',[(v.T*G*v)[0]+1])
    zero(f'nontrivial_normal_form_shear_{n}',list(Sig))
    zero(f'nontrivial_normal_form_alpha_{n}',list(alpha-grad))
    zero(f'nontrivial_normal_form_expansion_{n}',[Hv-(s.diff(f,t)/f**2).subs(point)])
    W=s.factor(sum(I[a,c]*I[b,d]*vort[a,b]*vort[c,d]
           for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
    assert W>0
    values[f'twist_squared_event_{n}']=str(W)

S=s.symbols('S',real=True)
ft=s.exp(t);m=ft**2
old=s.diag(-ft**2,ft**2)
# Exact coordinate S=exp(2t)*sigma. Carry old partial_t rather than reselecting it.
J=s.Matrix([[1,0],[-2*S/m,1/m]])
new=J.T*old*J
K=s.Matrix([1,2*S])
zero('actual_coordinate_clock_vector_retained',[(K.T*new*K)[0]+ft**2])
zero('actual_coordinate_determinant', [new.det()+1])
zero('coframe_density_reciprocity',[(s.diag(1,1/m).T*old*s.diag(1,1/m)).det()+1])
zero('actual_coordinate_extra_time_coefficient',[new[0,0]+ft**2-4*S*S/ft**2])
values['coframe_nonclosure_coefficient']=str(s.diff(m,t))
assert s.diff(m,t)!=0

k,L,to=s.symbols('kappa L to',positive=True)
log_received=k*(to**2-(to-L)**2)
zero('quadratic_emission_zero_redshift',[log_received.subs(to,L)-k*L**2])
zero('quadratic_reception_zero_blueshift',[log_received.subs(to,0)+k*L**2])
values['quadratic_received_at_zero_log_ratio']=str(log_received.subs(to,0))

print(json.dumps({'kind':'PEER_CHECK_AFTER_CANDIDATE_EXPOSURE','python':platform.python_version(),
   'sympy':s.__version__,'checks':checks,'values':values,
   'independence':'New small pointwise metric-jet contraction code; candidate and its code read first; no blind-method claim'},indent=2))
