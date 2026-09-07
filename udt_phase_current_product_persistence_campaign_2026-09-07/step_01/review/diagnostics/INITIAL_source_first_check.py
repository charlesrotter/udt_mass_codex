"""Independent PC1 algebra/complete-data controls; stdout only, no author imports."""
import hashlib
import itertools
import json
import pathlib
import platform
import sympy as s

root = pathlib.Path(__file__).resolve().parents[3]
eta = [-1, 1, 1, 1]
inds = range(4)
pairs = list(itertools.combinations(inds, 2))
var = s.symbols('z:21')
lam = s.symbols('Lambda')
mat = s.zeros(6)
k = 0
for i in range(6):
    for j in range(i, 6):
        mat[i, j] = mat[j, i] = var[k]
        k += 1

def Q(a, b, c, d):
    if a == b or c == d:
        return s.S.Zero
    sig = (1 if a < b else -1) * (1 if c < d else -1)
    return sig * mat[pairs.index(tuple(sorted((a, b)))),
                     pairs.index(tuple(sorted((c, d))))]

eq = [Q(a,b,c,d)+Q(b,c,a,d)+Q(c,a,b,d)
      for a,b,c,d in itertools.product(inds, repeat=4)]
eq += [sum(eta[a]*Q(a,b,c,a) for a in inds)
       - (lam*eta[b] if b == c else 0) for b,c in itertools.product(inds, repeat=2)]
eq += [Q(i,j,0,d)+Q(i,j,3,d)
       for i,j in itertools.combinations(range(1,4), 2) for d in inds]
coeff, rhs = s.linear_eq_to_matrix(eq, (*var, lam))
solution = next(iter(s.linsolve((coeff, rhs), (*var,lam))))
subs = dict(zip((*var,lam), solution))
qs = {(a,b,c,d):s.expand(Q(a,b,c,d).subs(subs))
      for a,b,c,d in itertools.product(inds, repeat=4)}
free = sorted(set().union(*(v.free_symbols for v in solution)), key=str)
assert len(free) == 3, (free, solution)
Ein = s.Matrix(3,3,lambda i,j:qs[i+1,0,0,j+1])
Lambda = s.expand(lam.subs(subs))
assert Lambda != 0
full_annihilation = sorted({s.expand(qs[a,b,0,d]+qs[a,b,3,d])
                           for a,b,d in itertools.product(inds,repeat=3)}-{s.S.Zero}, key=str)
flat_scalar_sub = s.solve(Lambda, free, dict=True)[0]
assert all(s.expand(v.subs(flat_scalar_sub)) == 0 for v in full_annihilation)

# First-pair dual and all 256 entries of the unchanged quadratic recipe.
def metric(a,b):
    return eta[a] if a == b else 0
weyl = {(a,b,c,d):s.expand(qs[a,b,c,d] - Lambda/s.Integer(3)*
         (metric(b,c)*metric(a,d)-metric(a,c)*metric(b,d)))
         for a,b,c,d in itertools.product(inds,repeat=4)}
dual = {(a,b,c,d):s.expand(sum(s.LeviCivita(a,b,e,f)*eta[e]*eta[f]*weyl[e,f,c,d]
         for e,f in itertools.product(inds,repeat=2))/2)
        for a,b,c,d in itertools.product(inds,repeat=4)}
B = {(a,b,c,d):s.expand(sum(eta[e]*eta[h]*(weyl[a,e,c,h]*weyl[b,e,d,h]
         +dual[a,e,c,h]*dual[b,e,d,h])
         for e,h in itertools.product(inds,repeat=2)))
     for a,b,c,d in itertools.product(inds,repeat=4)}
B0 = {idx:s.factor(v.subs(flat_scalar_sub)) for idx,v in B.items()}
rho = B0[0,0,0,0]
ell_flat = [-1,0,0,1]
assert all(s.expand(v-rho*s.prod(ell_flat[a] for a in idx)) == 0
           for idx,v in B0.items())
# Necessary rank-one minor for any real covector fourth power, null or otherwise.
minor = s.factor(B[0,0,0,0]*B[1,1,1,1]-B[0,0,1,1]**2)

# Complete spacelike graph in the admitted cubic harmonic metric.
u,x,y = s.symbols('u x y', real=True)
H = x**3-3*x*y**2
c = s.S.One  # supplied graph v=-c*u, not physical selection
L = H+2*c
coord = [u,x,y]
gamma = s.diag(L,1,1)
inverse = gamma.inv()
Gamma = [[[s.simplify(sum(inverse[a,d]*(s.diff(gamma[d,b],coord[j])+
          s.diff(gamma[d,j],coord[b])-s.diff(gamma[b,j],coord[d]))
          for d in range(3))/2) for j in range(3)] for b in range(3)] for a in range(3)]
Ric3 = s.Matrix(3,3,lambda i,j:s.simplify(sum(
       s.diff(Gamma[k][i][j],coord[k])-s.diff(Gamma[k][i][k],coord[j])+
       sum(Gamma[k][k][m]*Gamma[m][i][j]-Gamma[k][j][m]*Gamma[m][i][k]
           for m in range(3)) for k in range(3))))
K = s.Matrix(3,3,lambda i,j: (s.diff(H,coord[j])/(2*s.sqrt(L)) if i==0 else
           s.diff(H,coord[i])/(2*s.sqrt(L)) if j==0 else 0))
trK = s.trace(inverse*K)
Ksq = s.trace(inverse*K*inverse*K)
R3 = s.simplify(s.trace(inverse*Ric3))
ham = s.simplify(R3+trK**2-Ksq)
assert ham == 0
T = K*inverse-trK*s.eye(3)
momentum = [s.simplify(sum(s.diff(T[i,j],coord[j])+
            sum(Gamma[j][j][k]*T[i,k]-Gamma[k][j][i]*T[k,j]
                for k in range(3)) for j in range(3))) for i in range(3)]
assert momentum == [0,0,0]
f = 1/s.sqrt(L)
Y = s.Matrix([-1/L,0,0])
norm = s.simplify((Y.T*gamma*Y)[0]-f*f)
normal_seed = [s.simplify(s.diff(f,coord[i])-(K*Y)[i]) for i in range(3)]
spatial_seed = [[s.simplify(s.diff(Y[j],coord[i])+
                sum(Gamma[j][i][k]*Y[k] for k in range(3))-
                f*(inverse*K)[j,i]) for j in range(3)] for i in range(3)]
assert norm == 0 and normal_seed == [0,0,0]
assert spatial_seed == [[0,0,0],[0,0,0],[0,0,0]]
point = {u:0,x:1,y:0}
assert L.subs(point) == 3
N = s.diff(H,x,2)**2+s.diff(H,x,y)**2
assert s.expand(N) == 36*(x*x+y*y)

sources = [
 'AGENTS.md','CLAUDE.md','CROSS_MODEL_VERIFY.md',
 '.claude/skills/verifier-before-record/SKILL.md',
 '.claude/skills/no-shortcuts/SKILL.md',
 '.claude/skills/solution-space-not-imposition/SKILL.md',
 '.claude/skills/completeness-map/SKILL.md',
 'CURRENT_SCIENTIFIC_PREMISES.tsv',
 'startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md',
 'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/EXACT_DERIVATION.md',
 'udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/EXACT_DERIVATION.md',
 'udt_g335_local_pair_response_persistence_2026-09-03/EXACT_DERIVATION.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_03/CANDIDATE_ARGUMENT.md',
 'udt_g313_curvature_phase_current_candidate_2026-09-06/CANDIDATE_ARGUMENT.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_03/CANDIDATE_ARGUMENT.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_04/CANDIDATE_ARGUMENT.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_03/REVIEW_RECORD.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_04/REVIEW_RECORD.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_03/review/STAGE_B_ADVERSARIAL_REVIEW.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_04/review/STAGE_B_ADVERSARIAL_REVIEW.md',
 'udt_g353_g356_conditional_banking_2026-09-06/BANKING_RECORD.md',
 'udt_g357_g360_conditional_banking_2026-09-07/BANKING_RECORD.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
 'udt_phase_current_product_persistence_campaign_2026-09-07/WORK_ORDER.md',
 'udt_phase_current_product_persistence_campaign_2026-09-07/step_01/QUESTION.md']
record = dict(status='PASS', python=platform.python_version(),sympy=s.__version__,
  exact=True,author_imports=False,curvature_variables=22,constraint_rank=coeff.rank(),
  remaining_parameters=list(map(str,free)),Lambda=str(Lambda),
  electric_matrix=str(Ein),full_annihilation_defect=list(map(str,full_annihilation)),
  Weyl_quartic_minor=str(minor),B0000=str(B[0,0,0,0]),B1111=str(B[1,1,1,1]),
  B0011=str(B[0,0,1,1]),Lambda0_fourth_coefficient=str(rho),
  complete_graph=dict(H=str(H),L=str(L),gamma=str(gamma),K=str(K),f=str(f),Y=str(Y),
     R3=str(R3),Hamiltonian=str(ham),momentum=momentum,
     seed_normal=normal_seed,seed_tangent=spatial_seed,null_norm=str(norm)),
  sources={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sources})
print(json.dumps(record,indent=2,sort_keys=True))

