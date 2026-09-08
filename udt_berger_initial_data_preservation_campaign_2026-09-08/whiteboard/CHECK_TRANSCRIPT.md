# Exact whiteboard checks — source and actual captured output

These are the complete three mathematical computations run in the delegated
whiteboard context. They were executed read-only by `python3` from
`/home/udt-admin/udt_mass_codex`. No project modules or production result files
were imported. All three returned exit code 0 and no reported stderr. SymPy
reported version 1.13.1 in the first run. The Python interpreter version was
not separately queried; do not infer one. No further computations were run
after the parent's stop instruction.

These small exact symbolic checks support and check algebra in
WHITEBOARD_ARGUMENT.md. They are author checks in the same exposed context,
not independent adversarial review. The saved transcript was reconstructed
verbatim from tool responses; stdout and stderr were not separately captured
to on-disk files during execution.

## Check 1 — all six components and original constraint algebra

Exact command:

```bash
python3 - <<'PY'
import sympy as s
p,q=s.symbols('p q', real=True)
u,v,w,z,r,t=s.symbols('u v w z r t', real=True)
K=s.Matrix([[u,z,r],[z,v,t],[r,t,w]])
bs=[p,p,q]
C=lambda i,j,k:s.LeviCivita(i,j,k)*bs[k]
G=lambda i,j,k:(C(i,j,k)-C(j,k,i)+C(k,i,j))/2
M=[s.simplify(sum(-G(j,i,l)*K[l,j]-G(j,j,l)*K[i,l] for j in range(3) for l in range(3))) for i in range(3)]
print('Sympy:',s.__version__)
print('Momentum lower components:',M)
print('tau2 - norm2:',s.expand(s.trace(K)**2-s.trace(K*K)))
PY
```

Actual output, exit 0:

```text
Sympy: 1.13.1
Momentum lower components: [t*(-p + q), r*(p - q), 0]
tau2 - norm2: -2*r**2 - 2*t**2 + 2*u*v + 2*u*w + 2*v*w - 2*z**2
```

Reported elapsed tool wall time: 0.115928404 seconds.

## Check 2 — gap factorization, concrete witness, and exceptional branch

Exact command:

```bash
python3 - <<'PY'
import sympy as s
x,y,z=s.symbols('x y z',positive=True)
r=[2*(x*x-(y-z)**2)/(x*y*z),2*(y*y-(z-x)**2)/(x*y*z),2*(z*z-(x-y)**2)/(x*y*z)]
print('vertical-horizontal gap factors:',s.factor(r[2]-r[0]),s.factor(r[2]-r[1]))
R=s.Rational(7,2);Lam=s.Integer(3);K=s.diag(1,2,-s.Rational(1,4))
print('example original Hamiltonian residual:',R+s.trace(K)**2-s.trace(K*K)-2*Lam)
print('example tensor eigenvalues:',list(K.diagonal()))
print('zero-trace horizontal exceptional stratum: det([[d,z],[z,-d]])=',s.det(s.Matrix([[s.Symbol('d'),s.Symbol('z')],[s.Symbol('z'),-s.Symbol('d')]])))
PY
```

Actual output, exit 0:

```text
vertical-horizontal gap factors: -4*(x - z)*(x - y + z)/(x*y*z) 4*(y - z)*(x - y - z)/(x*y*z)
example original Hamiltonian residual: 0
example tensor eigenvalues: [1, 2, -1/4]
zero-trace horizontal exceptional stratum: det([[d,z],[z,-d]])= -d**2 - z**2
```

Reported elapsed tool wall time: 0.029595428 seconds.

This run used the proposed triaxial Ricci expression as input; it did not
independently derive that expression. Check 3 subsequently derives it directly
from the Lie bracket and Koszul coefficients.

## Check 3 — direct general diagonal-frame Koszul curvature reconstruction

Exact command:

```bash
python3 - <<'PY'
import sympy as s
b=s.symbols('b1:4', real=True)
C=lambda i,j,k:s.LeviCivita(i,j,k)*b[k]
G=lambda i,j,k:(C(i,j,k)-C(j,k,i)+C(k,i,j))/2
Ric=s.Matrix(3,3,lambda j,k:s.factor(sum(G(j,k,l)*G(i,l,i)-G(i,k,l)*G(j,l,i)-C(i,j,l)*G(l,k,i) for i in range(3) for l in range(3))))
print('general diagonal-frame Ricci from Koszul:',Ric)
A,B,F=s.symbols('A B F', positive=True)
subs={b[0]:2*A/(B*F),b[1]:2*B/(F*A),b[2]:2*F/(A*B)}
print('metric squared coefficients A² B² F² Ricci:',[s.factor(Ric[i,i].subs(subs)) for i in range(3)])
print('vertical gap factors:',[s.factor((Ric[2,2]-Ric[i,i]).subs(subs)) for i in range(2)])
PY
```

Actual output, exit 0:

```text
general diagonal-frame Ricci from Koszul: Matrix([[(b1 - b2 + b3)*(b1 + b2 - b3)/2, 0, 0], [0, -(b1 - b2 - b3)*(b1 + b2 - b3)/2, 0], [0, 0, -(b1 - b2 - b3)*(b1 - b2 + b3)/2]])
metric squared coefficients A² B² F² Ricci: [2*(A**2 - B**2 + F**2)*(A**2 + B**2 - F**2)/(A**2*B**2*F**2), -2*(A**2 - B**2 - F**2)*(A**2 + B**2 - F**2)/(A**2*B**2*F**2), -2*(A**2 - B**2 - F**2)*(A**2 - B**2 + F**2)/(A**2*B**2*F**2)]
vertical gap factors: [-4*(A - F)*(A + F)*(A**2 - B**2 + F**2)/(A**2*B**2*F**2), 4*(B - F)*(B + F)*(A**2 - B**2 - F**2)/(A**2*B**2*F**2)]
```

Reported elapsed tool wall time: 0.074464921 seconds.

In this check, x=A^2, y=B^2, zeta=F^2. The exact polynomial signs agree with
the two gap formulas in WHITEBOARD_ARGUMENT.md. This is a separate direct
curvature reconstruction from the proposed formula in Check 2, but shares
the author context and the general Koszul method used in Check 1.
