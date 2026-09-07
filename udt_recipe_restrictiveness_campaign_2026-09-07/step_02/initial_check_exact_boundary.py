"""RC2 full exact family and algebraic recipe boundary checks; CPU symbolic."""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tensor_geometry import geometry,quadratic
import sympy as s
I=range(4); J=range(3); slots=list(itertools.product(I,repeat=4))
mode=sys.argv[1] if len(sys.argv)>1 else 'none'; checks={}
def check(name,truth):
    checks[name]=bool(truth)
    if not truth:
        print(json.dumps({'status':'FAIL','mode':mode,'checks':checks,'failed':name},indent=2));sys.exit(1)
u,v,x,y,e=s.symbols('u v x y epsilon',real=True)
c=s.S.Zero if mode=='omit_quadratic_completion' else s.Rational(2,3)
H=x**3-3*x*y**2-2*e*v*y+c*e**2*x**4
g=s.Matrix([[H,-1,0,e*x**2],[-1,0,0,0],[0,0,1,0],[e*x**2,0,0,1]])
gi,G,R,Ric=geometry(g,(u,v,x,y))
check('original_exact_Ricci',Ric==s.zeros(4))
check('Lorentzian_nonzero_determinant',g.det()==-1)
B,_=quadratic(g,R)
minors={(i,j):s.factor(B[0,0,0,0]*B[0,0,i,j]-B[0,0,0,i]*B[0,0,0,j]) for i,j in itertools.product(I,repeat=2)}
minor_point={str(k):str(z.subs({u:0,v:0,x:1,y:0})) for k,z in minors.items() if z.subs({u:0,v:0,x:1,y:0})!=0}
check('any_fourth_root_obstructed',any(z.subs({u:0,v:0,x:1,y:0})!=0 for z in minors.values()))
# The coordinate null line is recurrent, not parallel; this alone is not recipe recurrence.
omega=s.Matrix([e*y,0,0,0])
check('coordinate_null_line_recurrent',all(s.simplify(G[a][b][1]-s.KroneckerDelta(a,1)*omega[b])==0 for a,b in itertools.product(I,repeat=2)))
check('line_recurrence_not_closed',s.diff(omega[0],y)==e)
dt=s.Matrix([2,1,0,0]); S=s.factor(-(dt.T*gi*dt)[0]); n=-gi*dt/s.sqrt(S)
X=s.Matrix([[1,0,0],[-2,0,0],[0,1,0],[0,0,1]])
gamma=(X.T*g*X).subs(v,-2*u)
check('spacelike_common_patch',S.subs({u:0,v:0,x:1,y:0})==5-e**2/3)
check('original_constraint_projections',s.simplify((n.T*Ric*n)[0])==0 and X.T*Ric*n==s.zeros(3,1))

# General ten-parameter algebraic Ricci-flat curvature in G358 slot convention.
a,b,cE,d,f, m,nM,p,q,t=s.symbols('a b cE d f m nM p q t',real=True)
E=s.Matrix([[a,b,cE],[b,d,f],[cE,f,-a-d]])
M=s.Matrix([[m,nM,p],[nM,q,t],[p,t,-m-q]])
Q={k:s.S.Zero for k in slots}
def put(i,j,k,l,z):
    for key,sgn in [((i,j,k,l),1),((j,i,k,l),-1),((i,j,l,k),-1),((j,i,l,k),1),((k,l,i,j),1),((l,k,i,j),-1),((k,l,j,i),-1),((l,k,j,i),1)]:Q[key]=s.expand(sgn*z)
for i,j in itertools.product(J,repeat=2):put(i+1,0,0,j+1,E[i,j])
for i,j,k in itertools.product(J,repeat=3):
    if j<k:put(i+1,0,j+1,k+1,sum(s.LeviCivita(j,k,l)*M[l,i] for l in J))
for i,j,k,l in itertools.product(J,repeat=4):
    if i<j and k<l:put(i+1,j+1,k+1,l+1,sum(s.LeviCivita(i,j,h)*s.LeviCivita(k,l,z)*E[h,z] for h,z in itertools.product(J,repeat=2)))
eta=s.diag(-1,1,1,1)
check('general_algebraic_Ricci_zero',all(s.expand(sum(eta[h,h]*Q[h,i,j,h] for h in I))==0 for i,j in itertools.product(I,repeat=2)))
check('general_first_Bianchi',all(s.expand(Q[i,j,k,l]+Q[j,k,i,l]+Q[k,i,j,l])==0 for i,j,k,l in slots))
BB,DD=quadratic(eta,Q)
if mode=='drop_FIRST_dual':
    BB={key:s.expand(sum(eta[ee,ee]*eta[hh,hh]*Q[key[0],ee,key[2],hh]*Q[key[1],ee,key[3],hh] for ee,hh in itertools.product(I,repeat=2))) for key in slots}
energy=sum(E[i,j]**2+M[i,j]**2 for i,j in itertools.product(J,repeat=2))
sos=sum((E[i,0]+M[i,1])**2+(E[i,1]-M[i,0])**2+E[i,2]**2+M[i,2]**2 for i in J)
check('full_energy_and_null_saturation',s.expand(BB[0,0,0,0]-energy)==0 and s.expand(BB[0,0,0,0]+BB[0,0,0,3]-sos)==0)
zero_squares=[z for i in J for z in (E[i,0]+M[i,1],E[i,1]-M[i,0],E[i,2],M[i,2])]
variables=(a,b,cE,d,f,m,nM,p,q,t)
solution=s.linsolve(zero_squares,variables)
expected=(a,b,0,-a,0,b,-a,0,-b,0)
check('saturation_complete_two_parameter_class',solution==s.FiniteSet(expected))
sub=dict(zip(variables,expected));ell=s.Matrix([1,0,0,1]);lf=eta*ell
check('all64_full_curvature_annihilation',all(s.expand(sum(Q[i,j,k,l].subs(sub)*ell[k] for k in I))==0 for i,j,l in itertools.product(I,repeat=3)))
check('all256_converse_root',all(s.expand(BB[key].subs(sub)-4*(a*a+b*b)*s.prod(lf[j] for j in key))==0 for key in slots))
print(json.dumps({'status':'PASS','mode':mode,'checks':checks,'sympy':s.__version__,'exact_metric':str(g),'Ricci':str(Ric),'S':str(S),'gamma':str(gamma),'B_exact_nonzero':{str(k):str(s.factor(z)) for k,z in B.items() if z!=0},'rank_one_minors_at_point':minor_point,'line_recurrence':str(omega),'algebraic_B0000':str(s.factor(BB[0,0,0,0])),'algebraic_B0003':str(s.factor(BB[0,0,0,3])),'sum_of_squares':str(sos),'saturation_solution':str(solution),'scope':'EXACT_LOCAL_FAMILY_AND_FINITE_DIMENSIONAL_ALGEBRA_NOT_GENERIC_PDE_OR_PHYSICS'},indent=2))
