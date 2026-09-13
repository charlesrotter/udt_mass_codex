"""Exact coefficient-space check of the full retained-class leading jet."""
import json, platform
import sympy as sp

x=sp.Matrix(sp.symbols('x y z'))
pairs=[(i,j) for i in range(3) for j in range(i,3)]
monomials=[x[i]*x[j] for i,j in pairs]
coeff=sp.symbols('b0:36')
B=sp.zeros(3)
for row,(i,j) in enumerate(pairs):
 B[i,j]=B[j,i]=sum(coeff[6*row+k]*monomials[k] for k in range(6))
equations=[]
for entry in B*x: equations.extend(sp.Poly(entry,*x).coeffs())
constraint,_=sp.linear_eq_to_matrix(equations,coeff)
rank=constraint.rank(); kernel=constraint.nullspace()
assert constraint.shape==(30,36)
assert rank==30 and len(kernel)==6
s=sp.symbols('s0:6'); S=sp.zeros(3)
for v,(i,j) in zip(s,pairs): S[i,j]=S[j,i]=v
C=sp.Matrix([[0,-x[2],x[1]],[x[2],0,-x[0]],[-x[1],x[0],0]])
D=sp.expand(C.T*S*C)
encoded=sp.Matrix([sp.Poly(D[i,j],*x).coeff_monomial(m) for i,j in pairs for m in monomials])
image=encoded.jacobian(s)
assert image.shape==(36,6) and image.rank()==6
assert constraint*image==sp.zeros(30,6)
# Rank/nullity plus injective six-column image proves exact equality of spaces.
H={(i,j,k,l):sp.diff(D[i,j],x[k],x[l]) for i in range(3) for j in range(3) for k in range(3) for l in range(3)}
R={(i,j,k,l):sp.expand((H[i,l,j,k]+H[j,k,i,l]-H[i,k,j,l]-H[j,l,i,k])/2)
   for i in range(3) for j in range(3) for k in range(3) for l in range(3)}
recover_B=sp.Matrix(3,3,lambda i,j:-sum(R[i,k,j,l]*x[k]*x[l] for k in range(3) for l in range(3))/3)
assert all(sp.expand(v)==0 for v in recover_B-D)
recover_S=sp.Matrix(3,3,lambda p,q:-sum(sp.LeviCivita(p,i,j)*sp.LeviCivita(q,k,l)*R[i,j,k,l]
                      for i in range(3) for j in range(3) for k in range(3) for l in range(3))/12)
assert recover_S==S
# At |n|=1, average of quadratic polynomial is one third of the trace.
area_coefficient=sp.expand(sum(sp.trace(D).coeff(xi,2) for xi in x)/6)
assert sp.expand(area_coefficient-sp.trace(S)/3)==0
area_row=sp.Matrix([area_coefficient]).jacobian(s)
assert area_row.rank()==1 and len(area_row.nullspace())==5
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':sp.__version__,
 'coefficient_pairs':pairs,'monomials':[str(v) for v in monomials],
 'constraint_shape':constraint.shape,'constraint_rank':rank,'kernel_dimension':len(kernel),
 'image_rank':image.rank(),'area_constraint_rank':area_row.rank(),'tracefree_dimension':5,
 'inverse_B_identity':True,'inverse_S_identity':True,'area_coefficient':str(area_coefficient),
 'constraint_matrix':[[int(v) for v in row] for row in constraint.tolist()],
 'image_matrix':[[int(v) for v in row] for row in image.tolist()],
 'scope':'marked leading second jet in stated geometric class; analytical exact-realization proof separate; no native admission'},indent=2))
