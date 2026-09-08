"""Post-exposure recomputation from sealed reviewer machinery; no author imports."""
import contextlib,io,json,pathlib,runpy
import sympy as s
pdir=pathlib.Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    own=runpy.run_path(str(pdir/'source_first_check.py'))
checks=[]
def eq(name, actual,expected=0):
    vals=list(actual-expected) if isinstance(actual,s.MatrixBase) else [actual-expected]
    assert all(s.factor(e)==0 for e in vals),(name,actual,expected)
    checks.append(name)
x,y,z,u,v,w,E,pp,q,h,eps=(own[n] for n in ['x','y','z','u','v','w','E','p','q','h','epsilon'])
m,r=s.symbols('m r',real=True)
za=(E-m*m+r*r+w*w)/(2*m)
KA=s.Matrix([[m,0,r],[0,m,w],[r,w,za]])
UA=(m,r,w)
D=s.Matrix(3,3,lambda a,b:s.Symbol(f'J{a}{b}'))
dsubs={own['d'][a,i,j]:sum(s.diff(KA[i,j],UA[l])*D[a,l] for l in range(3))
       for a in range(3) for i in range(3) for j in range(3)}
M=own['mom'].subs(dsubs,simultaneous=True).subs({x:m,y:m,z:za,u:0,v:r},simultaneous=True)
F=m+za
e=lambda a,f:sum(s.diff(f,UA[l])*D[a,l] for l in range(3))
eq('author_subfamily_exact_Hamiltonian',s.trace(KA)**2-s.trace(KA*KA)-2*E)
eq('all_author_momenta_from_sealed_general_Koszul',M,s.Matrix([-e(0,F)+D[2,1]+(q-pp)*w,
      -e(1,F)+D[2,2]+(pp-q)*r,D[0,1]+D[1,2]-2*D[2,0]]))
b1,b2=s.symbols('b1 b2',real=True)
normal=s.Matrix(s.symbols('Nm Nr Nw'))
tangent=s.Matrix(2,3,lambda a,b:s.Symbol(f'T{a}{b}'))
mix={D[a,l]:tangent[a,l]+[b1,b2][a]*normal[l] for a in [0,1] for l in range(3)}
mix.update({D[2,l]:normal[l] for l in range(3)})
system=s.Matrix([-M[2]/2,M[0],M[1]]).subs(mix)
A=system.jacobian(normal)
base={m:h,r:0,w:0,E:3*h*h}
eq('author_CK_nondegenerate_at_marked_point',A.subs({b1:0,b2:0}),s.eye(3))
eq('author_F_partial_at_base',s.diff(F,m).subs(base),-1)

# Independently solve the author's nine missing Hessians in component order.
J={};vars=[]
for name in ['m','r','w']:
    J[name]=s.zeros(3)
    if name=='w': J[name][0,0]=eps
    for a in range(3):
        var=s.Symbol(f'{name}normal{a}');vars.append(var)
        J[name][a,2]=J[name][2,a]=var
eqs=[]
for b in range(3):
    eqs.extend([2*J['m'][2,b]-J['r'][0,b]-J['w'][1,b],
                J['r'][2,b]+J['m'][0,b],J['w'][2,b]+J['m'][1,b]])
solutions=s.solve(eqs,vars,dict=True)
assert len(solutions)==1
for var in vars:eq('actual_CK_Hessian_'+str(var),solutions[0][var])
H={key:s.S.Zero for key in own['H']}
H[0,0,1,2]=H[0,0,2,1]=eps
S=own['ricci_variation'](h*s.eye(3),own['zero1'],H)
# Independent direct connection variation with all nine Ricci entries.
DC={(a,k,i,j):-H[a,i,j,k]-H[a,j,i,k]+H[a,k,i,j] for a,k,i,j in H}
direct=s.Matrix(3,3,lambda i,j:sum(DC[k,k,i,j]-DC[j,k,i,k] for k in range(3)))
eq('author_jet_full_covariant_and_direct_Ricci',S,direct)
B=own['B'];gap=own['gap'];Bdot=S+2*h*B
PD=s.zeros(3)
for i in [0,1]:PD[i,2]=Bdot[i,2]/gap;PD[2,i]=Bdot[2,i]/gap
P=s.diag(0,0,1)
eq('full_raised_derivative_eigenprojector_relation',Bdot*P+B*PD-PD*B-P*Bdot,s.zeros(3))
saved=json.loads((pdir/'candidate_snapshots/author_check_01.stdout').read_text())
loc=dict(Matrix=s.Matrix,m=m,r=r,w=w,E=E,p=pp,q=q,h=h,epsilon=eps,b1=b1,b2=b2)
parse=lambda value:s.sympify(value,locals=loc)
eq('saved_normal_matrix_all_entries',A,parse(saved['noncharacteristic_matrix']))
eq('saved_normal_determinant',A.det(),parse(saved['normal_determinant']))
eq('saved_Ricci_tensor_all_entries',S,parse(saved['Ricci_dot_difference']))
eq('saved_projector_all_entries',PD,parse(saved['Pdot']))
fixture_values=[]
for index,f in enumerate(saved['fixtures']):
    a,c,hh,ee=map(s.Rational,[f['a'],f['c'],f['h'],f['epsilon']])
    Delta=4*(c*c-a*a)/a**4
    R=8/a**2-2*c*c/a**4
    eq(f'fixture_{index}_same_Lambda',R/2+3*hh**2,s.Rational(f['Lambda']))
    eq(f'fixture_{index}_drift',PD[1,2].subs({pp:2/c,q:2*c/a**2,h:hh,eps:ee}),s.Rational(f['Y2']))
    fixture_values.append(dict(index=index,Delta=str(Delta),Y2=str(ee/Delta)))
# A finite polynomial still fails the exact scalar equation at fourth order.
t=s.symbols('t',real=True)
naive=h*s.eye(3);naive[1,2]=naive[2,1]=eps*t*t/2
badH=s.expand(s.trace(naive)**2-s.trace(naive*naive)-6*h*h)
eq('formal_jet_is_not_an_exact_nonlinear_datum',badH,-eps**2*t**4/2)
print(json.dumps(dict(status='PASS',check_count=len(checks),checks=checks,
    full_Ricci=str(S),full_Bdot=str(Bdot),full_Pdot=str(PD),fixtures=fixture_values,
    independence='No author code imported; generic sealed Koszul/covariant machinery reused and separately contracted connection variation. Author subfamily/seed comparison is post-exposure.',
    scope='Algebra and saved-output comparison only; analytic existence remains the independently reviewed noncharacteristic CK proof.'),indent=2))
