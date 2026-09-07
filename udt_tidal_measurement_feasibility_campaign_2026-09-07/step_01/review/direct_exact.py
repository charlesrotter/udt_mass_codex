"""Independent rational direct review; no author-code import or SymPy reuse.

Question: do documented compensation accelerations reconstruct the frozen
candidate's full tidal matrix, sign, factor, scalar error and bias claims?
Method: exact rational cross products and explicit component inversion on one
nontrivial synthetic fixture; general quantifiers are examined in the prose
review, not inferred from this fixture. Also exhibit the missing-linearity
counterexample. CPU/512MiB/60s, no observational data, no GPU.
"""
from fractions import Fraction as F
import json
import platform
import pathlib

checks = {}
def guard(name, claim):
    assert claim, name
    checks[name] = True
def add(a,b): return [x+y for x,y in zip(a,b)]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def scale(a,c): return [c*x for x in a]
def cross(a,b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def mv(m,v): return [sum(x*y for x,y in zip(row,v)) for row in m]
def dot(a,b): return sum(x*y for x,y in zip(a,b))

T = [[F(2),F(3,2),F(-5,3)], [F(3,2),F(-7),F(11,5)], [F(-5,3),F(11,5),F(13)]]
w = [F(2,3),F(-3,5),F(7,11)]
alpha = [F(-2,7),F(5,13),F(11,17)]
lengths = [F(2,5),F(3,7),F(5,11)]
common = [F(17),F(-19),F(23)]
columns = []
for j,L in enumerate(lengths):
    p=[F(0)]*3
    p[j]=L/2
    m=scale(p,-1)
    def holding(r):
        return add(add(add(mv(T,r),cross(w,cross(w,r))),cross(alpha,r)),common)
    ad=scale(sub(holding(p),holding(m)),F(1,2))
    columns.append(scale(ad,2/L))
S=[[columns[j][i] for j in range(3)] for i in range(3)]
out=[[F(0)]*3 for _ in range(3)]
for i in range(3):
    out[i][i]=S[i][i]+sum(w[j]**2 for j in range(3) if j!=i)
for i,j in [(0,1),(0,2),(1,2)]:
    out[i][j]=out[j][i]=(S[i][j]+S[j][i])/2-w[i]*w[j]
guard('full_matrix_from_cross_product_force_fixture',out==T)
guard('antisymmetric_angular_acceleration',[(S[2][1]-S[1][2])/2,(S[0][2]-S[2][0])/2,(S[1][0]-S[0][1])/2]==alpha)
guard('potential_sign',[[ -v for v in row] for row in out] != T)
trace=sum(T[i][i] for i in range(3))
guard('trace_map',sum(S[i][i] for i in range(3))+2*dot(w,w)==trace)
guard('factor_two_defect_detected',sum(S[i][i]/2 for i in range(3))+2*dot(w,w)!=trace)
guard('opposite_rotation_sign_detected',sum(S[i][i] for i in range(3))-2*dot(w,w)!=trace)
delta=[F(1,19),F(-2,23),F(3,29)]
bias_trace=F(5,31)
estimated_trace=sum(S[i][i] for i in range(3))+bias_trace+2*dot(add(w,delta),add(w,delta))
error=bias_trace+4*dot(w,delta)+2*dot(delta,delta)
guard('angular_rate_and_bias_trace_error',estimated_trace-trace==error)
k,b,q=F(2,7),F(-3,11),F(13,17)
guard('scalar_bias_alias',k+b==(k+q)+(b-q))
const=[k]*4
guard('fixed_linear_contrasts_remove_constant',[const[i+1]-const[i] for i in range(3)]==[0]*3)
nonlinear=lambda values:[v*(v-1) for v in values]
guard('H_one_zero_does_not_imply_constant_blindness',nonlinear([1]*4)==[0]*4 and nonlinear([2]*4)==[2]*4)

root=pathlib.Path(__file__).resolve().parents[1]
saved=json.loads((root/'author_check.stdout').read_text())
guard('saved_author_evidence_consistency',saved['pass'] is True and saved['count']==13 and len(saved['checks'])==13)
print(json.dumps({'kind':'INDEPENDENT_RATIONAL_RECOMPUTATION_AND_ANALYTIC_COUNTEREXAMPLE',
 'python':platform.python_version(),'checks':checks,'count':len(checks),
 'T':[[str(v) for v in row] for row in T], 'recovered_T':[[str(v) for v in row] for row in out],
 'trace':str(trace),'trace_error':str(error),
 'repair_needed':'Qualify H as fixed linear, or explicitly require annihilation of all constants.'},indent=2,sort_keys=True))
