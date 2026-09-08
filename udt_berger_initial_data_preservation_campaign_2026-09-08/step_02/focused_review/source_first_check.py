"""Independent BI2 source-first exact check; no package imports or data reads."""
import json
import platform
import sympy as S

q = S.symbols('A B C3', positive=True)
v = S.symbols('u1 u2 u3', real=True)
acc = S.symbols('w1 w2 w3', real=True)
k = S.symbols('k1 k2 k3', real=True)
lam = S.Symbol('Lambda', real=True)
g = [-S.Integer(1), *q]
indices = range(4)
def bracket(i,j,l):
    return 2*S.LeviCivita(i,j,l) if i*j*l else S.Integer(0)
def derivative(i,expr):
    if i:
        return S.Integer(0)
    return sum(S.diff(expr,q[j])*v[j]+S.diff(expr,v[j])*acc[j] for j in range(3))
def dg(i,j,l):
    return derivative(i,g[j]) if j==l else S.Integer(0)
# G[i,j,l] is the X_l component of nabla_(X_i) X_j in a fixed frame.
G = {(i,j,l): S.cancel((dg(i,j,l)+dg(j,i,l)-dg(l,i,j)
       +bracket(i,j,l)*g[l]-bracket(j,l,i)*g[i]
       +bracket(l,i,j)*g[j])/(2*g[l]))
     for i in indices for j in indices for l in indices}
Ric = S.Matrix(4,4,lambda j,l:S.factor(sum(
    derivative(i,G[j,l,i])-derivative(j,G[i,l,i])
    +sum(G[j,l,m]*G[i,m,i]-G[i,l,m]*G[j,m,i]
         -bracket(i,j,m)*G[m,l,i] for m in indices) for i in indices)))
checks = []
def zero(name,expr):
    vals=list(expr) if isinstance(expr,S.MatrixBase) else [expr]
    residuals=[S.factor(x) for x in vals]
    checks.append(dict(name=name,passed=all(x==0 for x in residuals),
                       residuals=list(map(str,residuals))))
static=Ric.subs(dict.fromkeys([*v,*acc],0))
r=[]
for i in range(3):
    j,l=(i+1)%3,(i+2)%3
    r.append(S.factor(2*(q[i]**2-(q[j]-q[l])**2)/S.prod(q)))
    zero(f'spatial Ricci {i+1}',static[i+1,i+1]/q[i]-r[i])
gaps={}
for i,j in [(0,1),(2,0),(2,1)]:
    l=3-i-j
    expected=4*(q[i]-q[j])*(q[i]+q[j]-q[l])/S.prod(q)
    zero(f'gap {i+1}-{j+1}',r[i]-r[j]-expected)
    gaps[f'{i+1}-{j+1}']=str(S.factor(r[i]-r[j]))
tau=sum(k)
qd=[-2*q[i]*k[i] for i in range(3)]
kd=[r[i]+tau*k[i]-lam for i in range(3)]
qdd=[4*q[i]*k[i]**2-2*q[i]*kd[i] for i in range(3)]
evolved=Ric.subs(dict(zip([*v,*acc],[*qd,*qdd])),simultaneous=True)-lam*S.diag(*g)
H=sum(r)+tau**2-sum(x*x for x in k)-2*lam
target=S.zeros(4); target[0,0]=H
zero('ALL 16 original vacuum components equal Hamiltonian-only residual',evolved-target)
Hd=sum(S.diff(H,q[i])*qd[i]+S.diff(H,k[i])*kd[i] for i in range(3))
zero('Hamiltonian propagation',Hd-2*tau*H)
A,B,C3=q
lh=4/A-2*C3/A**2
lv=2*C3/A**2
zero('Berger eigenvalues including round control',S.Matrix(r).subs(B,A)-S.Matrix([lh,lh,lv]))
zero('initial vertical gap', (r[2]-r[0]).subs(B,A)-4*(C3-A)/A**2)
# Lie derivative of a covariant tensor uses both bracket slots.
h=S.diag(A,B,0)
Lie=S.Matrix(3,3,lambda i,j:-sum(bracket(3,i+1,l+1)*h[l,j]
                    +bracket(3,j+1,l+1)*h[i,l] for l in range(3)))
zero('direct quotient descent Lie derivative',Lie-S.Matrix([[0,2*(A-B),0],[2*(A-B),0,0],[0,0,0]]))
zero('horizontal departure derivative', (qd[0]-qd[1]).subs(B,A)+2*A*(k[0]-k[1]))
# Check every sign automorphism algebraically, not by an assumed symmetry label.
for signs in [(1,-1,-1),(-1,1,-1),(-1,-1,1)]:
    zero('complete sign bracket invariance '+str(signs),S.Matrix([
        (signs[l]-signs[i]*signs[j])*bracket(i+1,j+1,l+1)
        for i in range(3) for j in range(3) for l in range(3)]))
out=dict(python=platform.python_version(),sympy=S.__version__,method='fixed-frame 4D Koszul and full Ricci contraction',
         exact=True,spatial_eigenvalues=list(map(str,r)),all_gaps=gaps,
         original_Ricci=str(Ric),vacuum_residual_after_evolution=str(S.simplify(evolved)),
         Hamiltonian=str(S.factor(H)),horizontal_Lie_derivative=str(Lie),
         checks=checks,count=len(checks),all_pass=all(c['passed'] for c in checks),
         limits='symbolic identities; no PDE theorem proof or numerical time evolution')
print(json.dumps(out,indent=2))
raise SystemExit(0 if out['all_pass'] else 1)
