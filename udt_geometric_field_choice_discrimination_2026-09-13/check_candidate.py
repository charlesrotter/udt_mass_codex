"""NR2 exact original-equation and map checks; symbolic regression, not independent proof."""
from pathlib import Path
import sympy as s,json,sys,hashlib,platform
p=Path(__file__).resolve().parent
source=Path('udt_current_native_radiation_feasibility_2026-09-13/check_candidate.py');txt=source.read_text()
# Reuse only frozen utility definitions, never execute NR1's old experiment.
part=txt[txt.index('def conn_ric'):txt.index("u,v,x,y=s.symbols")];ns={'s':s};exec(compile(part,str(source),'exec'),ns)
checks=[]
def flat(x):
 if isinstance(x,s.MatrixBase):return list(x)
 if isinstance(x,(tuple,list)):return [v for y in x for v in flat(y)]
 return [x]
def eq(name,a,b=0):
 aa,bb=flat(a),flat(b)
 if len(bb)==1 and bb[0]==0:bb=[0]*len(aa)
 assert len(aa)==len(bb),(name,len(aa),len(bb))
 rr=[s.simplify(x-y) for x,y in zip(aa,bb)]
 checks.append({'name':name,'pass':all(r==0 for r in rr),'shape':[len(aa),len(bb)],'residuals':list(map(str,rr))})
def nz(name,x):
 r=s.simplify(x);checks.append({'name':name,'pass':r!=0,'expression':str(r),'meaning':'not the identically zero symbolic expression or a declared exact nonzero witness, not universal nonvanishing'})
u,v,x,y=s.symbols('u v x y',real=True);c=(u,v,x,y);H=s.Function('H')(u,x,y)
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
C,R=ns['conn_ric'](g,c);expected=s.zeros(4);expected[0,0]=-(s.diff(H,x,2)+s.diff(H,y,2))/2
eq('general_full_Ricci',R,expected);eq('general_det',g.det(),-1)
ax=s.Function('a_x')(u);ay=s.Function('a_y')(u);F=s.zeros(4);F[0,2]=ax;F[2,0]=-ax;F[0,3]=ay;F[3,0]=-ay
Fu=g.inv()*F*g.inv();eq('arbitrary_profile_closed',ns['closed'](F,c));eq('arbitrary_profile_original_divergence',ns['densdiv'](g,F,c,s.Integer(1)))
eq('arbitrary_profile_null',sum(F[i,j]*Fu[i,j] for i in range(4) for j in range(4)))
eq('arbitrary_profile_wedge_square',F[0,1]*F[2,3]-F[0,2]*F[1,3]+F[0,3]*F[1,2])
q=s.Function('q')(u);r=s.Function('r')(u);K=s.Matrix([0,s.diff(q,u)*x+s.diff(r,u)*y,q,r]);FK=ns['exterior'](g*K,c)
eq('lowering_retains_full_metric_Kflat',g*K,s.Matrix([-s.diff(q,u)*x-s.diff(r,u)*y,0,q,r]));eq('full_F_from_K',FK,F.subs({ax:2*s.diff(q,u),ay:2*s.diff(r,u)}))
L=ns['lie'](g,K,c);Le=s.zeros(4);Le[0,0]=q*s.diff(H,x)+r*s.diff(H,y)-2*x*s.diff(q,u,2)-2*y*s.diff(r,u,2);eq('general_K_Lie',L,Le)
A=2/u**2;H0=A*(x*x-y*y);eps=s.symbols('epsilon',real=True);cub=x**3-3*x*y*y;He=H0+eps*cub
subsH={H:He}
Re=R.subs(subsH).doit();eq('cubic_full_Ricci',Re)
LeActual=L.subs(subsH).doit().subs({s.diff(q,u,2):A*q,s.diff(r,u,2):-A*r});LeTarget=s.zeros(4);LeTarget[0,0]=eps*(3*q*(x*x-y*y)-6*r*x*y);eq('cubic_actual_Lie_residual',LeActual,LeTarget)
nz('cubic_K_failure_exact_witness',LeActual[0,0].subs({u:1,x:1,y:0,eps:1,q:1,r:1}))
eq('base_Killing',LeActual.subs(eps,0));eq('central_Killing_survives',ns['lie'](g,s.Matrix([0,1,0,0]),c))
# Full curvature from connection, not assumed pp-wave expression.
def Rlow(a,b,d,e):
 return s.simplify(sum(g[a,z]*(s.diff(C[z][e][b],c[d])-s.diff(C[z][d][b],c[e])+sum(C[z][d][k]*C[k][e][b]-C[z][e][k]*C[k][d][b] for k in range(4))) for z in range(4)))
tide=s.Matrix(2,2,lambda i,j:Rlow(0,i+2,0,j+2));eq('general_screen_Riemann',tide,s.Matrix(2,2,lambda i,j:-s.diff(H,(x,y)[i],(x,y)[j])/2))
delta=tide.subs(H,He).doit()-tide.subs(H,H0).doit();eq('cubic_off_axis_tide',delta,-3*eps*s.Matrix([[x,-y],[-y,-x]]));eq('central_tide_unchanged',delta.subs({x:0,y:0}));eq('central_transverse_tidal_gradient',s.diff(delta[0,0],x).subs({x:0,y:0}),-3*eps)
jet=[eps*cub]+[s.diff(eps*cub,z) for z in c]+[s.diff(eps*cub,z,w) for z in c for w in c];eq('all_central_metric_two_jet_differences',[e.subs({x:0,y:0}) for e in jet]);nz('catch_central_equality_promoted_to_all_points',delta[0,0].subs({x:1,y:0,eps:s.Rational(1,8)}))
# A nonharmonic control remains allowed geometry, but must fail a Ricci-flat claim.
nh=(R.subs(H,H0+eps*(x*x+y*y)).doit())[0,0];eq('nonharmonic_Ricci_control',nh,-2*eps);nz('catch_unchecked_harmonicity',nh.subs(eps,1))
# Observer normalization and parallel frame/connection on central sheet.
g0=g.subs(H,H0);U=s.Matrix([1/s.sqrt(2),1/s.sqrt(2),0,0]);eq('central_U_norm',(U.T*g0*U)[0].subs({x:0,y:0}),-1)
C0=[[[e.subs(H,H0).doit().subs({x:0,y:0}) for e in row] for row in plane] for plane in C];eq('central_connection_zero',C0)
record=s.Matrix([(U.T*FK*s.eye(4)[:,i])[0] for i in (2,3)]);eq('signed_projection_normalization',record,s.sqrt(2)*s.Matrix([s.diff(q,u),s.diff(r,u)]))
# Explicit finite ODE family and inversion, with positive u for powers/logs.
t=s.symbols('t',positive=True);q0,p0,r0,s0=s.symbols('q0 p0 r0 s0',real=True);nu=s.sqrt(7)/2
qq=(q0+p0)*t*t/3+(2*q0-p0)/(3*t);rr=s.sqrt(t)*(r0*s.cos(nu*s.log(t))+(s0-r0/2)*s.sin(nu*s.log(t))/nu)
eq('q_original_ODE',s.diff(qq,t,2)-2*qq/t**2);eq('r_original_ODE',s.diff(rr,t,2)+2*rr/t**2);eq('all_four_initial_data',[qq.subs(t,1),s.diff(qq,t).subs(t,1),rr.subs(t,1),s.diff(rr,t).subs(t,1)],[q0,p0,r0,s0])
e=s.sqrt(2)*s.Matrix([s.diff(qq,t),s.diff(rr,t)]);ep=s.diff(e,t);eq('local_signed_inverse',[ep[0]*t*t/(2*s.sqrt(2)),e[0]/s.sqrt(2),-ep[1]*t*t/(2*s.sqrt(2)),e[1]/s.sqrt(2)],[qq,s.diff(qq,t),rr,s.diff(rr,t)])
z=s.Matrix([q0,p0,r0,s0]);jetmap=e.col_join(ep).subs(t,1).jacobian(z);eq('signed_jet_full_rank_det',jetmap.det(),16)
qx=s.diff(e[0]/s.sqrt(2),q0);rx=s.diff(e[1]/s.sqrt(2),r0);eq('two_sample_x_coefficient',qx,s.Rational(2,3)*(t-t**-2));eq('two_sample_y_coefficient',rx,-2/(nu*s.sqrt(t))*s.sin(nu*s.log(t)))
M=e.subs(t,1).col_join(e).jacobian(z);eq('two_sample_det_factor',M.det(),-4*qx*rx)
blind=s.exp(s.pi/nu);eq('exact_y_blind_return',rx.subs(t,blind));nz('x_still_visible_at_blind_return',qx.subs(t,blind));eq('coincident_samples_rank_loss',M.det().subs(t,1))
# The analytic b=2 claim is supported by inequalities in the proof; finite evaluation is descriptive only.
vals={'two_sample_det_at2':str(s.N(M.det().subs(t,2),50)),'first_nonzero_blind_b':str(s.N(blind,50))}
# Pure readout algebra including the zero case, with nonzero norm stated in candidate.
ex,ey,dx,dy=s.symbols('ex ey dx dy',real=True);ev=s.Matrix([ex,ey]);dv=s.Matrix([dx,dy]);Q=ev*ev.T;I=ex*ex+ey*ey;Qp=dv*ev.T+ev*dv.T
inverse=(Qp*ev-ev*(ev.T*Qp*ev)[0]/(2*I))/I;eq('quadratic_first_jet_inverse',inverse,dv)
eq('quadratic_sign_ambiguity',(-ev)*(-ev).T,Q)
a=s.symbols('scale',nonzero=True,real=True);eq('normalized_line_scale_ambiguity',(a*ev)*(a*ev).T/(a*a*I),Q/I)
eq('quadratic_zero_first_jet',[Q.subs({ex:0,ey:0}),Qp.subs({ex:0,ey:0})]);nz('zero_record_can_have_nonzero_second_jet',(2*dv*dv.T)[0,0].subs({dx:1,dy:0}))
eref=e.subs({q0:1,p0:1,r0:1,s0:1});eother=e.subs({q0:-1,p0:-1,r0:1,s0:1});eq('all_history_scalar_I_reflection',(eref.T*eref)[0],(eother.T*eother)[0]);eq('orientation_cross_term_plus',(eref*eref.T)[0,1].subs(t,1),2);eq('orientation_cross_term_minus',(eother*eother.T)[0,1].subs(t,1),-2)
# Same-form phase factorization and a richer aligned-family record counterexample.
f=s.Function('f')(u);theta_grad=s.Matrix([s.diff(f,u),0,0,0]);atheta=s.Matrix([0,0,ax/s.diff(f,u),ay/s.diff(f,u)]);eq('same_F_phase_factorization',theta_grad*atheta.T-atheta*theta_grad.T,F)
# Distinct phases -u/-u² have different gradients, same compensated F.
eq('phase_example_compensated_F',F[0,2]/(-2*u)*(-2*u),F[0,2]);nz('different_phase_gradients',(-2*u)-(-1))
extra=(t-1)**3;eq('larger_family_same_signed_first_jet',[extra.subs(t,1),s.diff(extra,t).subs(t,1)]);nz('larger_family_different_field_at2',extra.subs(t,2))
# Concrete failure of dropping a hypothesis: transverse dependence can spoil divergence.
Fb=F.copy();Fb[0,2]=x;Fb[2,0]=-x
nz('catch_unrestricted_transverse_profile',ns['densdiv'](g,Fb,c,s.Integer(1))[1])
result={'kind':'original-equation symbolic regression, exact map checks and labeled finite descriptions; not independent proof','python':platform.python_version(),'sympy':s.__version__,'utility_source':str(source),'utility_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'checks':checks,'count':len(checks),'passed':sum(x['pass'] for x in checks),'all_pass':all(x['pass'] for x in checks),'finite_descriptions_50_digits':vals,'evidence_limit':'Generic nonzero expressions are not universal nonzero claims; all-function classification rests on analytic proof; no floating tolerance or operating-domain certification.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('count','passed','all_pass','finite_descriptions_50_digits')}));sys.exit(0 if result['all_pass'] else 1)
