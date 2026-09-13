"""NR1 exact symbolic checks of ORIGINAL tensors; not an independent proof."""
import sympy as s
import json,sys,platform
from pathlib import Path
out=Path(sys.argv[1])
checks=[]
def zero(name,expr):
    vals=list(expr) if isinstance(expr,(list,tuple,s.MatrixBase)) else [expr]
    rem=[s.simplify(v) for v in vals]
    ok=all(v==0 for v in rem)
    checks.append({'name':name,'pass':ok,'residuals':[str(v) for v in rem]})
    return ok
def nonzero(name,expr):
    e=s.simplify(expr); checks.append({'name':name,'pass':e!=0,'residual':str(e)})
def conn_ric(g,c):
    n=len(c); gi=g.inv()
    C=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,b],c[e])+s.diff(g[d,e],c[b])-s.diff(g[b,e],c[d])) for d in range(n))/2) for e in range(n)] for b in range(n)] for a in range(n)]
    R=s.Matrix(n,n,lambda b,d:s.simplify(sum(s.diff(C[a][b][d],c[a])-s.diff(C[a][b][a],c[d])+sum(C[a][a][e]*C[e][b][d]-C[a][d][e]*C[e][b][a] for e in range(n)) for a in range(n))))
    return C,R
def exterior(a,c): return s.Matrix(len(c),len(c),lambda i,j:s.diff(a[j],c[i])-s.diff(a[i],c[j]))
def closed(F,c): return [s.diff(F[j,k],c[i])+s.diff(F[k,i],c[j])+s.diff(F[i,j],c[k]) for i in range(4) for j in range(i+1,4) for k in range(j+1,4)]
def densdiv(g,F,c,rho):
    Fu=g.inv()*F*g.inv(); return s.Matrix([s.simplify(sum(s.diff(rho*Fu[a,b],c[a]) for a in range(4))/rho) for b in range(4)])
def lie(g,K,c):return s.Matrix(4,4,lambda a,b:s.simplify(sum(K[d]*s.diff(g[a,b],c[d])+g[d,b]*s.diff(K[d],c[a])+g[a,d]*s.diff(K[d],c[b]) for d in range(4))))
u,v,x,y=s.symbols('u v x y',real=True); q=s.Function('q',positive=True)(u); A=s.diff(q,u,2)/q
c=(u,v,x,y); H=A*(x*x-y*y)
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
K=s.Matrix([0,s.diff(q,u)*x,q,0]); F=exterior(g*K,c); gi=g.inv(); Fu=gi*F*gi
C,R=conn_ric(g,c)
zero('pp_full_Ricci_all16',R);zero('pp_Killing_all16',lie(g,K,c));zero('pp_det',g.det()+1)
expected=s.zeros(4);expected[0,2]=2*s.diff(q,u);expected[2,0]=-expected[0,2]
zero('pp_F_lower_then_d',F-expected);zero('pp_exterior_closure',closed(F,c));zero('pp_original_divergence',densdiv(g,F,c,s.Integer(1)))
zero('pp_null_scalar',sum(F[a,b]*Fu[a,b] for a in range(4) for b in range(4)))
zero('pp_wedge_self',F[0,1]*F[2,3]-F[0,2]*F[1,3]+F[0,3]*F[1,2])
zero('pp_parallel_du',[-C[0][a][b] for a in range(4) for b in range(4)])
T=F*gi*F.T-g*sum(F[a,b]*Fu[a,b] for a in range(4) for b in range(4))/4
Te=s.zeros(4);Te[0,0]=4*s.diff(q,u)**2;zero('pp_quadratic_comparison',T-Te)
root=s.sqrt(2);E=s.Matrix([[(1-H/2)/root,1/root,0,0],[(-1-H/2)/root,1/root,0,0],[0,0,1,0],[0,0,0,1]])
zero('pp_complete_coframe',E.T*s.diag(-1,1,1,1)*E-g);nonzero('pp_invertible_coframe',E.det())
qex=1+s.exp(-u*u)/4; nonzero('explicit_pulse_nonzero_at_u1',2*s.diff(qex,u).subs(u,1));zero('explicit_pulse_zero_at_center',s.diff(qex,u).subs(u,0))
# Catches are computed equation defects, never token matches.
Kb=s.Matrix([0,-s.diff(q,u)*x,q,0]);nonzero('catch_wrong_Kv_sign',lie(g,Kb,c)[0,2]);nonzero('catch_F_factor_one',F[0,2]-s.diff(q,u))
gbad=g.copy();gbad[0,0]=A*(x*x+y*y);_,Rb=conn_ric(gbad,c);nonzero('catch_wrong_transverse_trace',Rb[0,0])
# Curved non-vacuum checks certify the sign and necessity of Ric(K)=0.
t,X,Y,Z=s.symbols('t X Y Z',positive=True);d=(t,X,Y,Z);gd=s.diag(-1,1,1,1)/t**2;Kd=s.Matrix([0,1,0,0]);Fd=exterior(gd*Kd,d);_,Rd=conn_ric(gd,d);jd=densdiv(gd,Fd,d,t**-4)
zero('deSitter_Ric_3g',Rd-3*gd);zero('deSitter_Killing',lie(gd,Kd,d));zero('Killing_Ricci_sign',jd+2*gd.inv()*Rd*Kd);nonzero('catch_omit_Ricci_condition',jd[1])
flat=s.diag(-1,1,1,1);badA=s.Matrix([0,t*t,0,0]);Fb=exterior(badA,d);zero('G95_closed_arbitrary_A',closed(Fb,d));nonzero('G95_nonzero_divergence',densdiv(flat,Fb,d,s.Integer(1))[1])
# Flat null waves are not all Killing-generated (analytic affine argument in candidate).
gflat=g.copy();gflat[0,0]=0;f=s.Function('f')(u);Fw=s.zeros(4);Fw[0,2]=f;Fw[2,0]=-f
zero('flat_nonconstant_null_wave_closed',closed(Fw,c));zero('flat_nonconstant_null_wave_divergence',densdiv(gflat,Fw,c,s.Integer(1)));nonzero('flat_wave_can_vary',s.diff(Fw[0,2],u))
# BE1 direct full metric density calculation with N retained as independent positive function.
xi=s.symbols('xi',real=True);cc=(t,xi,Y,Z);P=s.Function('P')(t,xi);N=s.Function('N',positive=True)(t,xi);gg=s.diag(-N*N,N*N,t*s.exp(P),t*s.exp(-P));rho=N*N*t
be=[]
for axis,sign in [(2,1),(3,-1)]:
    Kv=s.eye(4)[:,axis];FF=exterior(gg*Kv,cc);jj=densdiv(gg,FF,cc,rho)
    target=s.zeros(4,1);target[axis]=-sign*(s.diff(P,t)+t*s.diff(P,t,2)-t*s.diff(P,xi,2))/rho
    zero('BE1_density_identity_'+str(axis),jj-target);zero('BE1_exterior_'+str(axis),closed(FF,cc));zero('BE1_Killing_'+str(axis),lie(gg,Kv,cc))
    # exact wave-operator substitution, no numerical residual fitted to tolerance
    zero('BE1_on_equation_'+str(axis),[e.subs(s.diff(P,t,2),s.diff(P,xi,2)-s.diff(P,t)/t).doit() for e in jj])
    be.append(str(jj[axis]))
g0=s.diag(-N*N,N*N,t,t);F0=exterior(g0*s.eye(4)[:,2],cc);F0u=g0.inv()*F0*g0.inv()
zero('BE1_background_nonnull_value',sum(F0[a,b]*F0u[a,b] for a in range(4) for b in range(4))+2/(N*N*t));nonzero('BE1_background_nonnull',-2/(N*N*t))
record={'kind':'exact symbolic regression and equation checks, not independent proof','python':platform.python_version(),'sympy':s.__version__,'checks':checks,'count':len(checks),'passed':sum(r['pass'] for r in checks),'BE1_original_divergences':be,'all_pass':all(r['pass'] for r in checks)}
out.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'count':record['count'],'passed':record['passed'],'all_pass':record['all_pass']}));sys.exit(0 if record['all_pass'] else 1)
