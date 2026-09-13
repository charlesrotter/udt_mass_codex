"""GFC1 exact original-connection checks; source utility reuse is regression, not independence."""
from pathlib import Path
import ast,json,sys,platform,hashlib
import sympy as s
out=Path(sys.argv[1]); source=Path('udt_current_native_radiation_feasibility_2026-09-13/check_candidate.py')
tree=ast.parse(source.read_text()); names={'conn_ric','exterior','closed','densdiv','lie'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(source),'exec'))
checks=[]
def simp(e):return s.simplify(s.sympify(e))
def equal(a,b):
 if isinstance(a,s.MatrixBase) or isinstance(b,s.MatrixBase):
  if not isinstance(a,s.MatrixBase) or not isinstance(b,s.MatrixBase) or a.shape!=b.shape:return False,['SHAPE_MISMATCH']
  vals=list(a-b)
 elif isinstance(a,(list,tuple)) or isinstance(b,(list,tuple)):
  if not isinstance(a,(list,tuple)) or not isinstance(b,(list,tuple)) or len(a)!=len(b):return False,['SHAPE_MISMATCH']
  vals=[x-y for x,y in zip(a,b)]
 else:vals=[s.sympify(a)-s.sympify(b)]
 residuals=[simp(x) for x in vals];return all(x==0 for x in residuals),[str(x) for x in residuals if x!=0]
def check(name,a,b=0):
 ok,res=equal(a,b);checks.append({'name':name,'pass':ok,'nonzero_residuals':res});print(name,ok,flush=True);return ok
def caught(name,a,b):
 ok,res=equal(a,b);checks.append({'name':name,'pass':not ok,'control':'computed defect must fail the same equality comparator','observed_defect':res});print(name,not ok,flush=True)
u=s.symbols('u',positive=True);v,x,y=s.symbols('v x y',real=True);coords=(u,v,x,y);root=s.sqrt(2)
H=2*(x*x-y*y)/u**2;g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]]);gi=g.inv();C,Ric=conn_ric(g,coords)
k=s.Matrix([0,1,0,0]);ell=s.Matrix([1,H/2,0,0]);T=(k+ell)/root;N=(ell-k)/root;ex=s.eye(4)[:,2];ey=s.eye(4)[:,3]
base=s.Matrix.hstack(T,N,ex,ey);check('base_Gram_all16',base.T*g*base,s.diag(-1,1,1,1));check('metric_det',g.det(),-1);check('full_Ricci_all16',Ric,s.zeros(4));check('parallel_k_all16',s.Matrix(4,4,lambda a,b:C[a][b][1]),s.zeros(4))
def cov(X,a):return X.diff(coords[a])+s.Matrix([sum(C[i][a][j]*X[j] for j in range(4)) for i in range(4)])
def Afrom(E1,E2):return s.Matrix([simp((E1.T*g*cov(E2,a))[0]) for a in range(4)])
f=s.Function('w1',real=True)(u);h=s.Function('w2',real=True)(u);w=s.Matrix([f,h]);c=s.sqrt(1+f*f+h*h);S=s.eye(2)+w*w.T/(c+1)
Tw=c*T+f*ex+h*ey;E1=f*T+S[0,0]*ex+S[0,1]*ey;E2=h*T+S[1,0]*ex+S[1,1]*ey;frame=s.Matrix.hstack(Tw,N,E1,E2)
check('boost_Gram_all16',frame.T*g*frame,s.diag(-1,1,1,1));check('screen_k_pairing_all2',(k.T*g*s.Matrix.hstack(E1,E2)).T,-w/root)
Aactual=Afrom(E1,E2);B=(h*s.diff(f,u)-f*s.diff(h,u))/(c+1);Aexpected=s.Matrix([B-root*(h*x+f*y)/u**2,0,0,0]);check('original_A_all4',Aactual,Aexpected)
Factual=exterior(Aactual,coords);Fexpected=s.zeros(4);Fexpected[0,2]=root*h/u**2;Fexpected[0,3]=root*f/u**2;Fexpected[2,0]=-Fexpected[0,2];Fexpected[3,0]=-Fexpected[0,3]
check('original_dA_all16',Factual,Fexpected)
omega_off=[simp((frame[:,i].T*g*cov(frame[:,j],a))[0]) for i in range(4) for j in range(4) for a in [1,2,3]];check('full_frame_connection_off_du_all48',omega_off,[s.Integer(0)]*48)
R=[[[[simp(s.diff(C[a][d][b],coords[cc])-s.diff(C[a][cc][b],coords[d])+sum(C[a][cc][e]*C[e][d][b]-C[a][d][e]*C[e][cc][b] for e in range(4))) for d in range(4)] for cc in range(4)] for b in range(4)] for a in range(4)]
projection=s.Matrix(4,4,lambda a,b:simp(sum((E1.T*g)[j]*R[j][d][a][b]*E2[d] for j in range(4) for d in range(4))))
check('ambient_R_projection_all16',projection,Fexpected);check('nonflat_tidal_x',sum(g[0,j]*R[j][2][0][2] for j in range(4)),-2/u**2);check('nonflat_tidal_y',sum(g[0,j]*R[j][3][0][3] for j in range(4)),2/u**2)
check('original_exterior_closure',closed(Factual,coords),[s.Integer(0)]*4);check('original_density_divergence',densdiv(g,Factual,coords,s.Integer(1)),s.zeros(4,1));Fu=gi*Factual*gi;check('null_scalar',sum(Factual[a,b]*Fu[a,b] for a in range(4) for b in range(4)));check('wedge_square',Factual[0,1]*Factual[2,3]-Factual[0,2]*Factual[1,3]+Factual[0,3]*Factual[1,2])
# Whole compatible-screen local class: arbitrary rotation and null lift functions.
angle=s.Function('lambda',real=True)(*coords);b1=s.Function('b1',real=True)(*coords);b2=s.Function('b2',real=True)(*coords)
P1=s.cos(angle)*ex-s.sin(angle)*ey+b1*k;P2=s.sin(angle)*ex+s.cos(angle)*ey+b2*k;Ag=Afrom(P1,P2)
check('compatible_screen_Gram',s.Matrix.hstack(P1,P2).T*g*s.Matrix.hstack(P1,P2),s.eye(2));check('compatible_connection_dlambda',Ag,s.Matrix([s.diff(angle,z) for z in coords]));check('compatible_curvature_zero_all16',exterior(Ag,coords),s.zeros(4))
# Inverse profiles include zeros without polar coordinates.
ax=s.Function('a_x',real=True)(u);ay=s.Function('a_y',real=True)(u);inverse={f:u**2*ay/root,h:u**2*ax/root};Fa=s.zeros(4);Fa[0,2]=ax;Fa[0,3]=ay;Fa[2,0]=-ax;Fa[3,0]=-ay
check('arbitrary_profile_inverse_all16',Fexpected.subs(inverse),Fa);check('zero_profile_frame',frame.subs({f:0,h:0}).doit(),base);check('zero_profile_curvature',Fexpected.subs({f:0,h:0}),s.zeros(4))
node={f:u**2*(u-1)**2/root,h:u**2*(u-1)/root};check('nodal_frame_regular',frame.subs(node).subs(u,1).doit(),base);check('nodal_F_zero',Fexpected.subs(node).subs(u,1),s.zeros(4));check('nodal_F_derivative_survives',s.diff(Fexpected.subs(node)[0,2],u).subs(u,1),1)
K=s.Matrix([0,2*u*x,u**2,0]);FK=exterior(g*K,coords);target={f:s.Integer(0),h:2*root*u**3};Aone=Aactual.subs(target).doit();Fone=Factual.subs(target).doit()
check('existing_K_Killing',lie(g,K,coords),s.zeros(4));check('existing_K_screen_field_match',Fone,FK);check('existing_K_potential_exact_difference',Aone-g*K,-s.Matrix([s.diff(u**2*x,z) for z in coords]));caught('compatible_zero_is_not_K_field',s.zeros(4),FK)
# Finite controls catch defects that exterior curvature alone would miss.
control={f:u,h:u**2};Acontrol=Aactual.subs(control).doit();Bcontrol=B.subs(control).doit();Aomit=Acontrol-s.Matrix([Bcontrol,0,0,0]);caught('catch_omitted_moving_boost_connection',Acontrol.subs({u:1,x:1,y:0}),Aomit.subs({u:1,x:1,y:0}));check('omitted_B_curvature_blindness_disclosed',exterior(Acontrol,coords),exterior(Aomit,coords))
E1one=E1.subs(target).doit();E2one=E2.subs(target).doit();Apartial=s.Matrix([simp((E1one.T*g*E2one.diff(z))[0]) for z in coords]);caught('catch_omitted_Christoffel',Apartial.subs({u:1,x:1,y:0}),Aone.subs({u:1,x:1,y:0}))
bad1=f*T+ex;bad2=h*T+ey;badgram=s.Matrix.hstack(bad1,bad2).T*g*s.Matrix.hstack(bad1,bad2);caught('catch_omitted_spatial_boost_correction',badgram.subs({f:1,h:0}),s.eye(2));caught('catch_wrong_field_sign',-Fone.subs(u,1),FK.subs(u,1));caught('catch_comparator_unequal_shapes',s.zeros(2,2),s.zeros(4,1));caught('catch_comparator_nonzero_integer',1,0);check('comparator_zero_integer',0,0)
result={'kind':'exact original-connection symbolic checks; shared NR1 metric utilities are regression, not independent proof','python':platform.python_version(),'sympy':s.__version__,'source_utility':str(source),'source_utility_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'AST_functions_only':sorted(names),'equations':{'A_original':[str(z) for z in Aactual],'F_original':str(Factual),'screen_R_projection':str(projection)},'checks':checks,'count':len(checks),'passed':sum(r['pass'] for r in checks),'all_pass':all(r['pass'] for r in checks)}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'count':result['count'],'passed':result['passed'],'all_pass':result['all_pass']}));sys.exit(0 if result['all_pass'] else 1)
