"""Independent RC3 source-first reconstruction; exact CPU, no author imports."""
import itertools
import json
import platform
import sympy as s

u, v, x, y = s.symbols('u v x y', real=True)
coords = (u, v, x, y)
H = s.Function('H')(u, x, y)
g = s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
inv = g.inv()
idx = range(4)
sim = lambda z: s.factor(s.simplify(z))
checks = []
def check(name, values):
    vals = list(values)
    residuals = [sim(z) for z in vals]
    assert all(z == 0 for z in residuals), (name, residuals)
    checks.append(name)
def connection(metric, variables):
    n = len(variables)
    mi = metric.inv()
    return [[[sim(sum(mi[a,d]*(s.diff(metric[d,c],variables[b])+
              s.diff(metric[d,b],variables[c])-s.diff(metric[b,c],variables[d]))
              for d in range(n))/2) for c in range(n)]
              for b in range(n)] for a in range(n)]
C = connection(g, coords)
# R^d_{c a b} applied to the vector in slot c; Q_abcd = g(R(a,b)c,d).
R = {(a,b,c,d):sim(s.diff(C[d][b][c],coords[a])-s.diff(C[d][a][c],coords[b])+
     sum(C[d][a][e]*C[e][b][c]-C[d][b][e]*C[e][a][c] for e in idx))
     for a,b,c,d in itertools.product(idx,repeat=4)}
Q = {(a,b,c,d):sim(sum(g[d,e]*R[a,b,c,e] for e in idx))
     for a,b,c,d in itertools.product(idx,repeat=4)}
Ric = s.Matrix(4,4,lambda b,c:sim(sum(R[a,b,c,a] for a in idx)))
expected_ric = s.zeros(4); expected_ric[0,0] = -s.diff(H,x,2)/2-s.diff(H,y,2)/2
check('original_general_H_Ricci', list(Ric-expected_ric))
check('parallel_V_all_slots', (C[a][b][1] for a,b in itertools.product(idx,repeat=2)))
# On the admitted harmonic sector W=Q. Keep every component and FIRST dual.
harmonic = {s.diff(H,y,2):-s.diff(H,x,2)}
W = {key:sim(value.subs(harmonic)) for key,value in Q.items()}
dual = {}
for a,b,c,d in itertools.product(idx,repeat=4):
    dual[a,b,c,d] = sim(sum(s.LeviCivita(a,b,m,n)*inv[m,p]*inv[n,q]*W[p,q,c,d]/2
        for m,n,p,q in itertools.product(idx,repeat=4)
        if s.LeviCivita(a,b,m,n) and inv[m,p] and inv[n,q] and W[p,q,c,d]))
B = {}
for a,b,c,d in itertools.product(idx,repeat=4):
    B[a,b,c,d] = sim(sum(inv[e,f]*inv[h,i]*(W[a,e,c,h]*W[b,f,d,i]+
       dual[a,e,c,h]*dual[b,f,d,i]) for e,f,h,i in itertools.product(idx,repeat=4)
       if inv[e,f] and inv[h,i] and
       (W[a,e,c,h]*W[b,f,d,i] or dual[a,e,c,h]*dual[b,f,d,i])))
N = s.diff(H,x,2)**2+s.diff(H,x,y)**2
check('full_256_Weyl_FIRST_dual_B', (value-(N if key==(0,0,0,0) else 0)
      for key,value in B.items()))
Knull = s.Matrix([1,H/2,0,0]); V = s.Matrix([0,1,0,0])
screen = [s.eye(4)[:,2],s.eye(4)[:,3]]
check('full_null_pair_screen', [ (Knull.T*g*Knull)[0], (V.T*g*V)[0],
      (V.T*g*Knull)[0]+1]+[(E.T*g*Knull)[0] for E in screen]+
      [(E.T*g*V)[0] for E in screen])
T = s.Matrix(2,2,lambda i,j:sim(sum(Q[i+2,b,c,j+2]*Knull[b]*Knull[c]
    for b,c in itertools.product(idx,repeat=2))))
check('ideal_tide_full_contraction', list(T+s.hessian(H,(x,y))/2))
# Full spacelike graph, with original intrinsic constraints independently assembled.
L=H+4
embed=s.Matrix([[1,0,0],[-2,0,0],[0,1,0],[0,0,1]])
gamma=sim(embed.T*g*embed)
n=-inv*s.Matrix([2,1,0,0])/s.sqrt(L)
K=s.Matrix(3,3,lambda i,j:sim(-sum(embed[a,i]*embed[b,j]*(2*C[0][a][b]+C[1][a][b])
                   for a,b in itertools.product(idx,repeat=2))/s.sqrt(L)))
check('full_graph_normal',[(n.T*g*n)[0]+1]+list(embed.T*g*n))
X=(u,x,y); ci=connection(gamma,X); gi=gamma.inv(); rr=range(3)
ric3=s.Matrix(3,3,lambda i,j:sim(sum(s.diff(ci[k][i][j],X[k])-s.diff(ci[k][i][k],X[j])+
      sum(ci[k][k][m]*ci[m][i][j]-ci[k][j][m]*ci[m][i][k] for m in rr) for k in rr)))
R3=sim(s.trace(gi*ric3)); trK=sim(s.trace(gi*K))
ham=sim(R3+trK**2-s.trace(gi*K*gi*K))
mixed=sim(gi*K-s.eye(3)*trK)
mom=[sim(sum(s.diff(mixed[j,i],X[j])+sum(ci[j][j][k]*mixed[k,i]-ci[k][j][i]*mixed[j,k]
              for k in rr) for j in rr)) for i in rr]
lap=s.diff(H,x,2)+s.diff(H,y,2)
check('original_intrinsic_constraints_general_H',[ham+lap/L,mom[0]-lap/(2*s.sqrt(L)),mom[1],mom[2]])
P=x**3-3*x*y**2+x**4-6*x**2*y**2+y**4
Qpoly=3*x*x*y-y**3+4*x**3*y-4*x*y**3
check('harmonic_conjugates',[s.diff(P,x,2)+s.diff(P,y,2),s.diff(Qpoly,x,2)+s.diff(Qpoly,y,2),
       s.diff(P,x)-s.diff(Qpoly,y),s.diff(P,y)+s.diff(Qpoly,x)])
c0,s0=s.symbols('c0 s0',real=True)
profile=c0*P+s0*Qpoly
NN=s.factor(s.diff(profile,x,2)**2+s.diff(profile,x,y)**2)
N0=s.factor(s.diff(P,x,2)**2+s.diff(P,x,y)**2)
check('rotating_Hessian_norm',[NN-(c0*c0+s0*s0)*N0])
q0=sim((s.diff(N0,x)**2+s.diff(N0,y)**2)/(16*N0**2))
point={x:1,y:0}
bpoint=s.root(N0.subs(point),4); qpoint=sim(q0.subs(point))
check('positive_anchor_values',[N0.subs(point)-324,qpoint-s.Rational(25,36),bpoint-3*s.sqrt(2)])
tidepoint=sim((-s.hessian(profile,(x,y))/2).subs(point))
theta=s.Function('theta')(u)
Hs=s.cos(theta)*P+s.sin(theta)*Qpoly
hu_point=sim(s.diff(Hs,u).subs(point))
check('angle_derivative_full_data',[hu_point+2*s.sin(theta)*s.diff(theta,u)])
# Full phase, root recurrence and geometric quotient are direct inverse/volume identities.
kappa=s.symbols('kappa',positive=True)
b=s.Function('b')(x,y); alpha=s.Matrix([0,0,s.diff(b,x)/b,s.diff(b,y)/b])
beta=s.Matrix([-b,0,0,0]); k=s.Matrix([-kappa,0,0,0])
check('recurrence_all_16',(s.diff(beta[a],coords[d])-sum(C[e][d][a]*beta[e] for e in idx)-alpha[d]*beta[a]
      for a,d in itertools.product(idx,repeat=2)))
check('phase_null_future_direction',list(inv*k-kappa*V)+[(k.T*inv*k)[0]])
q=sim((alpha.T*inv*alpha)[0]); w=s.symbols('w',positive=True)
check('full_graph_flux_density',[sim(-(w*V).dot(g*n)*s.sqrt(gamma.det()))-w])
# Fixed positive measure density sigma=Delta*w/kappa0 makes changed phase factor kappa/kappa0.
ka,k0,Delta=s.symbols('ka k0 Delta',positive=True)
product_residual=sim(ka*(Delta*w/k0)/Delta-w)
check('changed_phase_residual',[product_residual-w*(ka/k0-1)])
print(json.dumps({'runtime':{'python':platform.python_version(),'sympy':s.__version__},
 'checks':checks,'general_Ricci':str(Ric),'full_B_nonzero':{str(z):str(a) for z,a in B.items() if a!=0},
 'general_tide':str(T),'gamma':str(gamma),'K':str(K),'R3':str(R3),'Hamiltonian':str(ham),'momentum':list(map(str,mom)),
 'P':str(P),'Qpoly':str(Qpoly),'N0':str(N0),'q0':str(q0),'positive_anchor':{'N':324,'b':str(bpoint),'q':str(qpoint),'w':str(sim(bpoint*qpoint))},
 'registered_tide_anchor':str(tidepoint),'Hu_anchor':str(hu_point),'changed_phase_density_residual':str(product_residual)},indent=2))
