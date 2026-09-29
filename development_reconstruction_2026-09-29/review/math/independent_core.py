"""Original reviewer implementation. No source-package scientific code imported."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

out = Path(__file__).resolve().parent
checks = {}
values = {}

def ck(name, proposition):
    result = bool(proposition)
    checks[name] = result
    if not result:
        raise AssertionError(name)

def zero(m):
    return all(s.simplify(v) == 0 for v in m)

Q = s.Rational
eta = s.diag(-1, 1, 1, 1)
e = [s.eye(4)[:, i] for i in range(4)]

# Direct positive reciprocal character/readout identities.
p, q = s.symbols('p q', positive=True)
P = s.diag(p, 1/p)
K = s.Matrix([[0, 1], [1, 0]])
ck('dual_pairing', P.T*K*P == K)
ck('dual_nonreciprocal_covariance_separator', s.diag(2,2).T*K*s.diag(2,2) != K)
def chi(q): return (1-q)/(1+q)
ck('mobius_from_multiplicative_ratio', s.cancel(chi(p*q)-(chi(p)+chi(q))/(1+chi(p)*chi(q))) == 0)
ck('ratio_inverse_reversal', s.cancel(chi(1/p)+chi(p)) == 0)

# Shift retained: use positive T,L and arbitrary beta, derive via metric entries.
T, L, beta, om = s.symbols('T L beta om', positive=True)
h = s.Matrix([[-T*T,-T*T*beta],[-T*T*beta,L*L-T*T*beta*beta]])
m2 = -h.det()
ck('completed_density', s.expand(m2-T*T*L*L) == 0)
ck('schur_ruler', s.simplify(h[1,1]-h[0,1]**2/h[0,0]-L*L) == 0)
hs = s.diag(1,1/(T*L))*h*s.diag(1,1/(T*L))
ck('completed_determinant', s.simplify(hs.det()) == -1)
ck('completed_shift', s.simplify(hs[0,1]/hs[0,0]-beta/(T*L)) == 0)
ck('completed_ratio', s.simplify((-hs[0,0])**2-T**4) == 0)
ck('common_scale_density', s.simplify(-(om**2*h).det()-om**4*m2) == 0)
ck('arbitrary_control_scale_blind', s.simplify((-(om**2*h).det())/(om**2*h[0,0])**2-m2/h[0,0]**2) == 0)
ck('completed_clock_scale_sensitive', (om**2*h)[0,0] != h[0,0])
ck('angular_turn_positive', Q(1,4)*3**2*Q(4,9) == 1)
ck('zero_tangent_excluded', Q(0)**2+Q(1,4)*3**2*Q(0) == 0)

# Fully independent exact coframe multiplication; no block formula used first.
B = s.Matrix([[2,-2],[2,1]])
Qs = s.Matrix([[1,2],[2,3]])
S = s.Matrix([[-1,1],[-1,-1]])
E = B.row_join(s.zeros(2)).col_join((Qs*S).row_join(Qs))
Y = s.Matrix([[3,2],[-3,1]])
Z = s.Matrix([[1,-2],[2,-3]])
J = Y.col_join(Z)
hh = J.T*(E.T*eta*E)*J
ck('G179_full_witness', hh == s.Matrix([[-118,102],[102,822]]))
ck('G179_density_squared', -hh.det() == 107400)
ck('G179_block_formula', hh == Y.T*B.T*s.diag(-1,1)*B*Y+(S*Y+Z).T*Qs.T*Qs*(S*Y+Z))
Ysing = s.Matrix([[-8,0],[2,0]])
Zsing = s.Matrix([[-6,3],[-6,-6]])
Jsing = Ysing.col_join(Zsing)
hhsing = Jsing.T*E.T*eta*E*Jsing
ck('singular_base_regular_pair', Ysing.det() == 0 and Jsing.rank() == 2 and hhsing[0,0] < 0 and hhsing.det() < 0)
ck('G179_singular_base_witness', hhsing == s.Matrix([[-124,-132],[-132,225]]))

# General smooth-family change of ruler parameter, evaluated symbolically.
k = s.symbols('k', positive=True)
hk = s.diag(1,k)*h*s.diag(1,k)
ck('auxiliary_density_weight', s.simplify(-hk.det()-k**2*m2) == 0)
ck('auxiliary_clock_unchanged', hk[0,0] == h[0,0])

# Rational noncollinear boosts and an exact rotation.
def boost(i,c,sh):
    M=s.eye(4);M[0,0]=M[i,i]=c;M[0,i]=M[i,0]=sh
    return M
A=boost(1,Q(13,5),Q(12,5))
Bb=boost(2,Q(17,15),Q(8,15))
Rot=s.Matrix([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]])
n=s.Matrix([Q(3,5),Q(4,5),0])
ell=s.Matrix([1,*n])
def carried(M,n):
    v=M*s.Matrix([1,*n]);return v[0],v[1:4,0]/v[0]
for name,M in [('A',A),('B',Bb),('R',Rot),('BA',Bb*A)]:
    ck('Lorentz_'+name,M.T*eta*M==eta and M.det()==1 and M[0,0]>=1)
f1,n1=carried(A,n);f2,n2=carried(Bb,n1);ft,nt=carried(Bb*A,n)
ck('null_direction_composition',ft==f1*f2 and nt==n2)
ck('dropping_intermediate_direction_fails',carried(Bb,n)[0]*f1 != ft)
fi,ni=carried((Bb*A).inv(),nt)
ck('same_comparison_inverse', fi*ft == 1 and ni == n)
c=(Bb*A)*e[0]
ck('directional_clock_column_formula',s.simplify(c[0]-(c[1:4,0].T*nt)[0]) == 1/ft)
values['noncollinear_null_frequency_factor']=str(ft)
values['wrong_no_direction_carry_factor']=str(carried(Bb,n)[0]*f1)
def proj(M):
    v=M*e[0];return v[1:4,0]/v[0]
ck('projective_inputs_equal',proj(Bb)==proj(Bb*Rot))
ck('projective_compositions_different',proj(Bb*A)!=proj(Bb*Rot*A))

w=s.symbols('w',positive=True)
cc=s.Matrix([1+w*w/2,w*w/2,w,0])
ck('saturation_future_clock',s.expand((cc.T*eta*cc)[0]) == -1)
ck('saturation_clock_ratio_one',cc[0]-cc[1] == 1)
ck('saturation_projective_norm',s.limit(sum((cc[i]/cc[0])**2 for i in range(1,4)),w,s.oo) == 1)
rr,ww=s.symbols('rr ww',positive=True)
Gamma=(rr+1/rr+rr*ww*ww)/2
aa=Gamma-1/rr
ck('screen_interlock_timelike',s.expand(-Gamma*Gamma+aa*aa+ww*ww) == -1)
ck('screen_interlock_frequency',s.simplify(Gamma-aa) == 1/rr)
ck('screen_strict_example', (1/Gamma).subs({rr:2,ww:1})==Q(4,9))

# Construct actual covariant H matrices from orthonormal pairs, then derive rank.
def H(u,n):
    ck('pair_'+str(len(checks)),(u.T*eta*u)[0]==-1 and (n.T*eta*n)[0]==1 and (u.T*eta*n)[0]==0)
    uf,nf=eta*u,eta*n
    return 2*(uf*uf.T+nf*nf.T)
Hs=[H(e[0],e[i]) for i in range(1,4)]
for i,j in [(1,2),(1,3),(2,3)]: Hs.append(H(e[0],Q(3,5)*e[i]+Q(4,5)*e[j]))
C,Sh=Q(13,5),Q(12,5)
for i in range(1,4): Hs.append(H(C*e[0]+Sh*e[i],Sh*e[0]+C*e[i]))
components=[(i,j) for i in range(4) for j in range(i,4)]
rows=s.Matrix([[hh[i,j] for i,j in components] for hh in Hs])
ck('DDR_span_nine',rows.rank()==9)
ck('DDR_all_traceless',all(s.trace(eta*hh)==0 for hh in Hs))
pairrows=s.Matrix([[hh[i,j]*eta[i,i]*eta[j,j]*(1 if i==j else 2) for i,j in components] for hh in Hs])
ns=pairrows.nullspace()
ck('DDR_annihilator_metric',len(ns)==1 and zero(s.Matrix(ns[0])-s.Matrix([eta[i,j] for i,j in components])))
uf,nf=eta*e[0],eta*e[1]
cross=Hs[6]/2-(C*C+Sh*Sh)*Hs[0]/2
ck('G310_covector_cross_positive_sign',cross == 2*C*Sh*(uf*nf.T+nf*uf.T))
ck('G310_printed_covector_negative_sign_fails',cross != -2*C*Sh*(uf*nf.T+nf*uf.T))
ck('G310_coordinate_cross_negative',cross[0,1] == -2*C*Sh)
ck('DDR_one_plane_leaves_eight',pairrows[:1,:].rank()==1)

a,b=s.symbols('a b')
Ric=s.Matrix([[-3,2,1,4],[2,5,6,7],[1,6,-2,8],[4,7,8,9]])
R=s.trace(eta*Ric)
EE=a*Ric+b*R*eta
TF=lambda x:x-s.trace(eta*x)*eta/4
ck('conditional_Ricci_TF_identity',zero(TF(EE)-a*TF(Ric)))
ck('scalar_response_DDR_vacuous',zero(TF(EE.subs(a,0))))
values['DDR_rank']=rows.rank()
values['DDR_annihilator']=[str(x) for x in ns[0]]

record={'implementation':'fresh reviewer symbolic/exact implementation; no production imports',
        'python':platform.python_version(),'sympy':s.__version__,
        'checks':checks,'values':values,'passed':sum(checks.values()),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (out/'core_results.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'passed':record['passed'],'values':values},sort_keys=True))
