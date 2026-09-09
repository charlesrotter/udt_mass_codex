"""Independent exact full-coordinate Ricci jet and Bianchi interface checks.

Generic rational SPD point data are mathematical test fixtures, not physics.
No parent/NR1/NR2 implementation is imported. This finite check corroborates,
but does not replace, the general Gaussian-coordinate calculation in the review.
"""
import json
import platform
import sympy as s

gamma=s.Matrix([[3,1,0],[1,2,1],[0,1,2]])
assert all(gamma[:k,:k].det()>0 for k in (1,2,3))
gi=gamma.inv()
K=s.Matrix([[2,-1,3],[-1,4,2],[3,2,-2]])/7
C=[s.Matrix(3,3,lambda i,j:s.Rational((i+1)*(j+1)+2*k+1,11+k)) for k in range(3)]
dK=[s.Matrix(3,3,lambda i,j:s.Rational((i+j+1)*(k+2)-3,13+k)) for k in range(3)]
D=[[s.Matrix(3,3,lambda i,j:s.Rational((i+j+1)*(k+l+2)+k*l,17+k+l)) for l in range(3)] for k in range(3)]

def tensor(metric, dmetric, ddmetric):
    n=metric.rows
    inv=metric.inv()
    dinv=[-inv*dmetric[k]*inv for k in range(n)]
    Gamma=[[[sum(inv[a,d]*(dmetric[b][d,c]+dmetric[c][d,b]-dmetric[d][b,c]) for d in range(n))/2
              for c in range(n)]for b in range(n)]for a in range(n)]
    dGamma=[[[[sum(dinv[e][a,d]*(dmetric[b][d,c]+dmetric[c][d,b]-dmetric[d][b,c])+
                     inv[a,d]*(ddmetric[e][b][d,c]+ddmetric[e][c][d,b]-ddmetric[e][d][b,c])
                     for d in range(n))/2 for c in range(n)]for b in range(n)]for a in range(n)]for e in range(n)]
    Ric=s.Matrix(n,n,lambda b,c:s.simplify(sum(dGamma[a][a][b][c]-dGamma[c][a][b][a]+
                    sum(Gamma[a][a][d]*Gamma[d][b][c]-Gamma[a][c][d]*Gamma[d][b][a] for d in range(n))
                    for a in range(n))))
    return Ric,Gamma

R3,Gamma3=tensor(gamma,C,D)
tau=s.trace(gi*K)
Ktime=R3+tau*K-2*K*gi*K
H=s.trace(gi*R3)+tau*tau-s.trace(gi*K*gi*K)
kmix=gi*K
dkmix=[-gi*C[k]*gi*K+gi*dK[k] for k in range(3)]
dtau=[s.trace(z) for z in dkmix]
M=s.Matrix([s.simplify(sum(dkmix[j][j,i]+sum(Gamma3[j][j][l]*kmix[l,i]-Gamma3[l][j][i]*kmix[j,l]
    for l in range(3))for j in range(3))-dtau[i])for i in range(3)])

def fourmetric(gtt):
    g=s.diag(-1,1,1,1)
    g[1:4,1:4]=gamma
    dg=[s.zeros(4) for _ in range(4)]
    dg[0][1:4,1:4]=-2*K
    for k in range(3): dg[k+1][1:4,1:4]=C[k]
    ddg=[[s.zeros(4) for _ in range(4)]for _ in range(4)]
    ddg[0][0][1:4,1:4]=gtt
    for k in range(3):
        ddg[0][k+1][1:4,1:4]=-2*dK[k]
        ddg[k+1][0][1:4,1:4]=-2*dK[k]
        for l in range(3):ddg[k+1][l+1][1:4,1:4]=D[k][l]
    return g,dg,ddg

g,dg,ddg=fourmetric(-2*Ktime)
R4,Gamma4=tensor(g,dg,ddg)
checks=[]
def check(name,ok):
    passed=bool(ok);checks.append({'name':name,'pass':passed});assert passed,name
def zero(z):return s.simplify(z)==0
check('full_spatial_Ricci_evolution',all(zero(z)for z in R4[1:4,1:4]))
check('full_time_Ricci_equals_H_after_spatial_evolution',zero(R4[0,0]-H))
check('full_mixed_Ricci_equals_negative_M',all(zero(R4[0,i+1]+M[i])for i in range(3)))
check('constraint_fixture_nonzero_and_nonvacuous',H!=0 and all(z!=0 for z in M))
# Every one of the six independent gamma_tt directions, including off diagonal.
for i in range(3):
    for j in range(i,3):
        perturb=s.zeros(3);perturb[i,j]=perturb[j,i]=1
        gm,dm,ddm=fourmetric(-2*Ktime+perturb)
        RR,_=tensor(gm,dm,ddm)
        check(f'normal_principal_direction_{i}{j}',all(zero(z)for z in RR[1:4,1:4]-perturb/2))

# Direct covariant divergence for the residual Einstein tensor implied by Rij=0.
A,At=s.symbols('A At')
Ai=s.symbols('Ax Ay Az')
B=s.Matrix(s.symbols('Bx By Bz'))
Bt=s.Matrix(s.symbols('Btx Bty Btz'))
Bd=[s.Matrix(s.symbols(f'B{k}x B{k}y B{k}z'))for k in range(3)]
E=s.zeros(4);E[0,0]=A/2
for i in range(3):E[0,i+1]=E[i+1,0]=B[i]
E[1:4,1:4]=A*gamma/2
dE=[s.zeros(4)for _ in range(4)]
dE[0][0,0]=At/2
for k in range(3):dE[k+1][0,0]=Ai[k]/2
for i in range(3):
    dE[0][0,i+1]=dE[0][i+1,0]=Bt[i]
    for k in range(3):dE[k+1][0,i+1]=dE[k+1][i+1,0]=Bd[k][i]
dE[0][1:4,1:4]=At*gamma/2-A*K
for k in range(3):dE[k+1][1:4,1:4]=Ai[k]*gamma/2+A*C[k]/2
ginv=g.inv()
div=s.Matrix([s.simplify(sum(ginv[a,c]*(dE[c][a,b]-sum(Gamma4[d][c][a]*E[d,b]+Gamma4[d][c][b]*E[a,d]
     for d in range(4)))for a in range(4)for c in range(4)))for b in range(4)])
DivB=s.simplify(sum(gi[i,j]*(Bd[i][j]-sum(Gamma3[k][i][j]*B[k]for k in range(3)))for i in range(3)for j in range(3)))
expected=s.Matrix([-At/2+DivB+tau*A]+[-Bt[i]+Ai[i]/2+tau*B[i]for i in range(3)])
check('full_covariant_Bianchi_propagation_including_lower_terms',all(zero(z)for z in div-expected))
mutants=[]
def reject(name, expr):
    caught=not zero(expr);mutants.append({'name':name,'rejected':caught});assert caught,name
reject('wrong_H_to_Ric00_factor',R4[0,0]-H/2)
reject('wrong_Codazzi_sign',R4[0,1]-M[0])
reject('omit_Bianchi_tau_A',div[0]-(-At/2+DivB))
reject('omit_Bianchi_tau_B',div[1]-(-Bt[0]+Ai[0]/2))
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
    'H':str(H),'M':[str(z)for z in M],'Ric00':str(R4[0,0]),
    'propagation':'A_t=2 D_i B^i+2 tau A; B_i,t=(1/2)partial_i A+tau B_i',
    'checks':checks,'mutants':mutants},indent=2))
