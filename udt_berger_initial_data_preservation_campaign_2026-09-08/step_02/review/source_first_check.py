"""Pre-BI2-candidate exact Koszul/Lie/ADM reconstruction; no author imports."""
import json
import platform
import sys
import sympy as s

checks = []


def zero(name, value):
    entries = list(value) if isinstance(value, s.MatrixBase) else [value]
    residuals = [s.factor(v) for v in entries]
    assert all(v == 0 for v in residuals), (name, residuals)
    checks.append(name)


def nonzero(name, value):
    assert s.factor(value) != 0, (name, value)
    checks.append(name)


x, y, z = s.symbols('x y z', positive=True)
g = s.diag(x, y, z)
gi = g.inv()
C = [[[2*s.LeviCivita(i, j, k) for k in range(3)]
      for j in range(3)] for i in range(3)]
# A_i columns are nabla_Xi Xj, from Koszul with the fixed, nonorthonormal Xi.
A = [s.Matrix(3, 3, lambda k, j: s.cancel(
    (C[i][j][k]*g[k,k]-C[j][k][i]*g[i,i]+C[k][i][j]*g[j,j])/(2*g[k,k])))
    for i in range(3)]
for i in range(3):
    zero('metric_compatibility_'+str(i), A[i].T*g+g*A[i])
    for j in range(3):
        zero('torsion_'+str((i,j)), A[i][:,j]-A[j][:,i]-s.Matrix(C[i][j]))
curvature = [[A[i]*A[j]-A[j]*A[i]-sum(
    (C[i][j][k]*A[k] for k in range(3)), s.zeros(3))
    for j in range(3)] for i in range(3)]
Ric = s.Matrix(3, 3, lambda b,j: s.factor(sum(curvature[i][j][i,b] for i in range(3))))
B = (gi*Ric).applyfunc(s.factor)
rho = [2*(x*x-(y-z)**2)/(x*y*z),
       2*(y*y-(z-x)**2)/(x*y*z),
       2*(z*z-(x-y)**2)/(x*y*z)]
zero('full_Ricci_endomorphism', B-s.diag(*rho))
gap31 = s.factor(B[2,2]-B[0,0])
gap32 = s.factor(B[2,2]-B[1,1])
zero('gap31_all_factors', gap31-4*(z-x)*(z+x-y)/(x*y*z))
zero('gap32_all_factors', gap32-4*(z-y)*(z+y-x)/(x*y*z))
zero('round_Ricci', B.subs({y:x,z:x})-s.eye(3)*2/x)
zero('Berger_Ricci', B.subs(y,x)-s.diag(4/x-2*z/x**2,4/x-2*z/x**2,2*z/x**2))
P = ((B-B[0,0]*s.eye(3))*(B-B[1,1]*s.eye(3))/(gap31*gap32)).applyfunc(s.factor)
zero('full_spectral_projector',P-s.diag(0,0,1))
zero('projector_idempotent',P*P-P)
zero('projector_selfadjoint_with_moving_metric',P.T*g-g*P)
zero('projector_commutes',B*P-P*B)

u,v,w,Lambda = s.symbols('u v w Lambda',real=True)
K = s.diag(u,v,w)
tau = s.trace(gi*K)
rhs_gamma = -2*K
rhs_K = Ric+tau*K-2*K*gi*K-Lambda*g
for i in range(3):
    for j in range(3):
        if i != j:
            zero('original_ADM_offdiag_'+str((i,j)),rhs_K[i,j])
for n, signs in enumerate(((1,-1,-1),(-1,1,-1),(-1,-1,1))):
    D=s.diag(*signs)
    zero('complete_data_metric_symmetry_'+str(n),D.T*g*D-g)
    zero('complete_data_K_symmetry_'+str(n),D.T*K*D-K)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                zero('automorphism_'+str((n,i,j,k)),
                     (signs[i]*signs[j]-signs[k])*C[i][j][k])

# Direct definition of tensor Lie derivative, with no coframe formula imported.
ad3=s.Matrix(3,3,lambda k,i:C[2][i][k])
q=s.diag(x,y,0)
Lq=-(ad3.T*q+q*ad3)
zero('unaveraged_horizontal_Lie_derivative',Lq-s.Matrix([[0,2*(x-y),0],[2*(x-y),0,0],[0,0,0]]))
zero('horizontal_annihilation',q[:,2])
h1,h2,h12=s.symbols('h1 h2 h12',real=True)
horizontal=s.Matrix([[h1,h12,0],[h12,h2,0],[0,0,0]])
Lhorizontal=-(ad3.T*horizontal+horizontal*ad3)
zero('unrotated_shear_basicness',Lhorizontal-s.Matrix([[-4*h12,2*(h1-h2),0],[2*(h1-h2),4*h12,0],[0,0,0]]))
zero('continuous_axial_ADM_invariance',
     (rhs_K[0,0]-rhs_K[1,1]).subs({y:x,v:u},simultaneous=True))
zero('normal_first_difference',rhs_gamma[0,0]-rhs_gamma[1,1]+2*(u-v))
zero('normalized_Hopf_integral',s.Rational(1,4)*(-2)*2-(-1))

fixture = {x:1,y:1,z:s.Rational(9,4),u:1,v:2,w:-s.Rational(9,16),Lambda:3}
ham=s.trace(B)+tau**2-s.trace(gi*K*gi*K)-2*Lambda
zero('lawful_anisotropic_Hamiltonian',ham.subs(fixture))
momentum=[]
for j in range(3):
    # div of constant covariant K; trace is spatially constant.
    momentum.append(s.factor(sum(gi[i,i]*(-sum(
        A[i][m,i]*K[m,j]+A[i][m,j]*K[i,m] for m in range(3)))
        for i in range(3))))
zero('all_original_diagonal_momenta',s.Matrix(momentum))
zero('lawful_witness_departure',
     (rhs_gamma[0,0]-rhs_gamma[1,1]).subs(fixture)-2)
nonzero('lawful_witness_K_not_axially_invariant',
        (-(ad3.T*K+K*ad3))[0,1].subs(fixture))

controls=[]
for vals in ((1,3,2),(3,1,2),(1,2,4),(1,s.Rational(6,5),s.Rational(9,4))):
    sub=dict(zip((x,y,z),vals))
    rr=[s.factor(B[i,i].subs(sub)) for i in range(3)]
    controls.append(dict(metric=list(map(str,vals)),Ricci=list(map(str,rr)),
                         gap31=str(s.factor(gap31.subs(sub))),gap32=str(s.factor(gap32.subs(sub)))))
zero('positive_triaxial_extra_gap31_zero',gap31.subs({x:1,y:3,z:2}))
nonzero('other_gap_at_extra_gap31_zero',gap32.subs({x:1,y:3,z:2}))
zero('positive_triaxial_extra_gap32_zero',gap32.subs({x:3,y:1,z:2}))
nonzero('other_gap_at_extra_gap32_zero',gap31.subs({x:3,y:1,z:2}))
for i,j in ((0,1),(0,2),(1,2)):
    nonzero('three_simple_eigenvalues_'+str((i,j)),
            (B[i,i]-B[j,j]).subs({x:1,y:2,z:4}))

# Nonzero diagnostic contrasts are not represented as end-to-end mutation catches.
discriminators={
    'omit_extra_gap_factor':s.factor(gap31-4*(z-x)/(x*y)),
    'reuse_two_eigenvalue_linear_projector':s.factor(((B-B[0,0]*s.eye(3))/gap31)[1,1]),
    'claim_all_diagonal_metrics_have_basic_q':str(Lq[0,1]),
    'claim_Berger_metric_alone_gives_axial_data_symmetry':str((-(ad3.T*K+K*ad3))[0,1])}
for name,val in discriminators.items():nonzero('contrast_'+name,s.sympify(val))

result=dict(status='PASS',python=sys.version,sympy=s.__version__,platform=platform.platform(),
            evidence_type='exact symbolic algebra; analytic argument owns evolution quantifiers',
            checks=checks,check_count=len(checks),Ricci_covariant=str(Ric),
            Ricci_endomorphism=str(B),gaps=[str(gap31),str(gap32)],projector=str(P),
            ADM_K=str(rhs_K.applyfunc(s.factor)),Hamiltonian=str(s.factor(ham)),
            momenta=list(map(str,momentum)),horizontal_Lie=str(Lq),
            unrotated_shear_Lie=str(Lhorizontal),controls=controls,
            nonzero_discriminators={k:str(v) for k,v in discriminators.items()})
print(json.dumps(result,indent=2,sort_keys=True))
