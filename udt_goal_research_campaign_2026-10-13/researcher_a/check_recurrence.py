"""GRC1-A1: exact supplied metric recurrence check, not a physical law."""
import json, platform
import sympy as s
u,v,x,y,k,b=s.symbols('u v x y k b', real=True)
z=[u,v,x,y]; H=k*v*v+b*x*x
G=s.Matrix([[H,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
Gi=G.inv(); n=4
Gamma=[[[s.simplify(sum(Gi[a,d]*(s.diff(G[d,c],z[j])+s.diff(G[d,j],z[c])-s.diff(G[j,c],z[d])) for d in range(n))/2) for c in range(n)] for j in range(n)] for a in range(n)]
# R^a_bij corresponds to R(partial_i,partial_j) partial_b.
R=[[[[s.simplify(s.diff(Gamma[a][j][c],z[i])-s.diff(Gamma[a][i][c],z[j])+sum(Gamma[a][i][d]*Gamma[d][j][c]-Gamma[a][j][d]*Gamma[d][i][c] for d in range(n))) for j in range(n)] for i in range(n)] for c in range(n)] for a in range(n)]
w=[k*v,0,0,0]
checks={}
checks['det_minus_one']=s.simplify(G.det()+1)==0
checks['recurrence_all16']=all(s.simplify(Gamma[a][i][1]-(w[i] if a==1 else 0))==0 for a in range(n) for i in range(n))
checks['curvature_line_all64']=all(s.simplify(R[a][1][i][j]-((s.diff(w[j],z[i])-s.diff(w[i],z[j])) if a==1 else 0))==0 for a in range(n) for i in range(n) for j in range(n))
checks['affine_null_line']=all(Gamma[a][1][1]==0 for a in range(n))
checks['screen_optical_zero']=all(Gamma[a][i][1]==0 for a in [2,3] for i in [2,3])
checks['nontrivial_curvature_coefficient']=s.simplify(R[1][1][1][0]-k)==0
# If R(e0,e1), R(e0,e2) are nonzero pure boosts, no common null line.
# First boost's real null eigenlines e0 +/- e1 fail the second boost.
eta=s.diag(-1,1,1,1)
B=[]
for i in [1,2]:
    m=s.zeros(4); m[0,i]=1; m[i,0]=1; B.append(m)
checks['boosts_lorentz_skew']=all(m.T*eta+eta*m==s.zeros(4) for m in B)
checks['first_boost_null_eigenlines']=all(B[0]*s.Matrix([1,t,0,0])==t*s.Matrix([1,t,0,0]) for t in [-1,1])
checks['second_boost_breaks_both']=all((B[1]*s.Matrix([1,t,0,0]))==s.Matrix([0,0,1,0]) for t in [-1,1])
# First boost eigenvalue0 kernel is span(e2,e3), so contains no nonzero real null.
checks['zero_eigenspace_spacelike']=B[0].nullspace()==[s.Matrix([0,0,1,0]),s.Matrix([0,0,0,1])]
result={'python':platform.python_version(),'sympy':s.__version__,'equations':'g=2du dv+dx²+dy²+(k v²+b x²)du²; R=[nabla,nabla]','checks':checks,'passed':all(checks.values()),'recurrence_form':[str(q) for q in w], 'line_curvature_Rv_vvu':str(R[1][1][1][0]),'meaning':'Exact symbolic witness and linear algebra; no empirical or UDT admission claim'}
print(json.dumps(result,indent=2))
assert all(checks.values()),result
