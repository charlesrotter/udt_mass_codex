"""NFCA1 exact original-pullback witnesses; regression of an exposed audit argument."""
from pathlib import Path
import sympy as s,json,hashlib,platform,sys
u,v,x,y,eps=s.symbols('u v x y epsilon',real=True)
c=(u,v,x,y);H=2*(x*x-y*y)/u**2+eps*(x**3-3*x*y*y)
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
J=s.Matrix([[1,0],[s.Rational(3,2),0],[0,1],[0,0]])
checks=[];records=[]
def eq(name,a,b):
 aa=list(a) if isinstance(a,s.MatrixBase) else [a]
 bb=list(b) if isinstance(b,s.MatrixBase) else [b]
 if len(aa)!=len(bb):raise ValueError((name,len(aa),len(bb)))
 rr=[s.simplify(s.sympify(a-b).rewrite(s.exp)) for a,b in zip(aa,bb)]
 checks.append({'name':name,'pass':all(r==0 for r in rr),'shape':[len(aa),len(bb)],'residuals':list(map(str,rr))})
def gate(name,predicate):checks.append({'name':name,'pass':bool(predicate)})
gate('python_integer_zero_supported',s.simplify(s.sympify(2-2).rewrite(s.exp))==0)
gate('python_integer_nonzero_retained',s.simplify(s.sympify(2-3).rewrite(s.exp))!=0)
try:
 eq('deliberate_shape_mismatch',s.Matrix([1,2]),s.Matrix([1]))
except ValueError:
 gate('shape_mismatch_rejected',True)
else:
 gate('shape_mismatch_rejected',False)
eq('full_metric_determinant',g.det(),-1);eq('supplied_pair_rank',J.rank(),2)
h=J.T*g*J;eq('full_original_pullback',h,s.diag(H-3,1))
K=s.Matrix([0,2*u*x,u*u,0]);a=g*K
F=s.Matrix(4,4,lambda i,j:s.diff(a[j],c[i])-s.diff(a[i],c[j]))
target=s.zeros(4);target[0,2]=4*u;target[2,0]=-4*u
eq('full_lowering',a,s.Matrix([-2*u*x,0,u*u,0]));eq('original_exterior_field',F,target)
eq('same_field_under_cubic_change',s.diff(F,eps),s.zeros(4))
a2=g*(2*K);F2=s.Matrix(4,4,lambda i,j:s.diff(a2[j],c[i])-s.diff(a2[i],c[j]))
eq('generator_rescaling_changes_field',F2,2*F);gate('nonzero_field_rescaling_at_u1',F2.subs(u,1)!=F.subs(u,1))
for e,want in [(s.Rational(0),s.Rational(0)),(s.Rational(1,8),s.Rational(1,15))]:
 p={u:1,v:0,x:1,y:0,eps:e};hp=h.subs(p);m=s.sqrt(-hp.det());D=s.diag(1,m);hs=D.inv().T*hp*D.inv()
 phi=-s.log(-hp[0,0])/2;chi=s.simplify(s.tanh(phi).rewrite(s.exp))
 tag='epsilon_'+str(e).replace('/','_')
 gate(tag+'_regular_pair',hp[0,0]<0 and hp.det()<0)
 eq(tag+'_completed_determinant',hs.det(),-1)
 eq(tag+'_reconstruct_original_pullback',D.T*hs*D,hp)
 eq(tag+'_kernel_from_log_tanh',chi,want)
 eq(tag+'_full_field_unchanged',F.subs(p),target.subs(p))
 # Unit normalization separately changes J and the query; it is not the fixed-J comparison.
 Junit=J*s.diag(1/s.sqrt(-hp[0,0]),1);hu=Junit.T*g.subs(p)*Junit
 eq(tag+'_different_unit_clock_query',hu[0,0],-1)
 records.append({'epsilon':str(e),'h':str(hp),'m':str(m),'h_s':str(hs),'Phi':str(phi),'chi':str(chi),'F':str(F.subs(p)),'unit_normalized_query_chi':'0, different J/protocol'})
hc=h.subs({x:0,y:0});eq('central_full_pullback_for_all_epsilon',hc,s.diag(-3,1))
eq('central_kernel_for_all_epsilon',s.tanh(-s.log(3)/2),s.Rational(-1,2))
# Existing G213 information-loss control, distinct from the field issue.
h1=s.diag(-1,1);h2=s.diag(-1,4);D1=s.diag(1,1);D2=s.diag(1,2)
eq('density_deleted_completed_records_equal',D1.inv()*h1*D1.inv(),D2.inv()*h2*D2.inv())
gate('original_pullbacks_different_despite_normalized_equality',h1!=h2)
gate('dropping_density_breaks_reconstruction',D2.inv()*h2*D2.inv()!=h2)
out={'kind':'exact original-pullback and exterior-derivative witnesses, plus existing density-loss control; not new general proof','python':platform.python_version(),'sympy':s.__version__,'checks':checks,'count':len(checks),'passed':sum(z['pass'] for z in checks),'all_pass':all(z['pass'] for z in checks),'records':records,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'same auxiliary J and calibration marking; T is not a unit observer; all-pair fixed-g independence is an analytic dependency statement; no physical field/shift or UDT admission claimed'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['count','passed','all_pass']}));sys.exit(0 if out['all_pass'] else 1)
