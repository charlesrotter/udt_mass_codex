"""CO1 symbolic geometry and finite algebra checks; no observational arrays."""
import json
import platform
import sympy as s

u,v,x,y=s.symbols('u v x y', real=True)
coords=(u,v,x,y)
A,B=s.Function('A')(u),s.Function('B')(u)
H=A*(x*x-y*y)+2*B*x*y
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi=g.inv()
Gamma=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,b],coords[c])+s.diff(g[d,c],coords[b])-s.diff(g[b,c],coords[d])) for d in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
def R(a,b,c,d):
    return s.simplify(s.diff(Gamma[a][d][b],coords[c])-s.diff(Gamma[a][c][b],coords[d])+sum(Gamma[a][c][e]*Gamma[e][d][b]-Gamma[a][d][e]*Gamma[e][c][b] for e in range(4)))
ric=s.Matrix(4,4,lambda b,d:s.simplify(sum(R(a,b,a,d) for a in range(4))))
tidal=s.Matrix(2,2,lambda i,j:s.simplify(sum(g[0,a]*R(a,i+2,0,j+2) for a in range(4))))
assert g.det()==-1 and ric==s.zeros(4)
assert tidal==s.Matrix([[-A,-B],[-B,A]])

# Generic three-channel/two-waveform algebra; independent of any event geometry.
f=s.Matrix(3,2,s.symbols('a:f'))
n=f[:,0].cross(f[:,1])
assert s.simplify(n.T*f)==s.zeros(1,2)
F=s.Matrix([[1,0],[0,1],[2,3]])
N=F[:,0].cross(F[:,1])
assert F.rank()==2 and N==s.Matrix([-2,-3,1])
h=s.Matrix(s.symbols('hp hx'))
assert (N.T*F*h)[0]==0
# The original noise need not be independent between calibration and null views.
noise_crosscov=(F.T*N)
assert noise_crosscov==s.zeros(2,1)  # only this equal independent-noise comparator
C=s.diag(1,2,3)
assert F.T*C*N!=s.zeros(2,1)
rank1=s.Matrix([[1,2],[2,4],[3,6]])
assert rank1.rank()==1 and len(rank1.T.nullspace())==2

# R1: a coefficient row and its adjoint column must not be interchanged.
bc=s.Matrix([[-s.I,0,1]])
Cc=s.Matrix([[1,0,s.I/2],[0,1,0],[-s.I/2,0,1]])
assert Cc==Cc.H and all(Cc[:k,:k].det()>0 for k in (1,2,3))
complex_variance=(bc*Cc*bc.H)[0]
wrong_column=bc.T
wrong_variance=(wrong_column.H*Cc*wrong_column)[0]
assert complex_variance==3 and wrong_variance==1

# Declared finite perturbation controls, not an exhaustive detector verifier.
guard_rejections=[]
def require(condition,label):
    if not condition: raise AssertionError(label)
for label,condition in [
    ('wrong_tidal_sign', -tidal==s.Matrix([[-A,-B],[-B,A]])),
    ('lost_cross_polarization', tidal.subs(B,0)==s.Matrix([[-A,-B],[-B,A]])),
    ('false_null_vector', s.Matrix([[1,1,1]])*F==s.zeros(1,2)),
    ('two_detector_unused_channel', 2-F[:2,:].rank()>0),
    ('rank_deficient_still_two_reconstructible', rank1.rank()==2),
    ('arbitrary_covariance_independence', F.T*C*N==s.zeros(2,1)),
    ('R1_missing_complex_conjugation', wrong_variance==complex_variance),
]:
    try: require(condition,label)
    except AssertionError: guard_rejections.append(label)
    else: raise AssertionError('false pass '+label)

print(json.dumps({'status':'PASS_SYMBOLIC_GEOMETRY_AND_FINITE_ALGEBRA',
 'python':platform.python_version(),'sympy':s.__version__,
 'coordinate_order':['u','v','x','y'],'metric_determinant':str(g.det()),
 'Ricci':str(ric),'R_uiuj':str(tidal),'generic_null_vector':str(n),
 'generic_null_identity':str(s.simplify(n.T*f)),
 'finite_F':str(F),'finite_null':str(N),
 'nonwhite_signal_null_noise_covariance':str(F.T*C*N),
 'rank_deficient_null_dimension':len(rank1.T.nullspace()),
 'complex_covariance_R1':{'coefficient_row':str(bc),'positive_definite_covariance':str(Cc),'correct_variance':str(complex_variance),'wrong_unconjugated_column_variance':str(wrong_variance)},
 'finite_defects_rejected':guard_rejections,
 'scope':'Exact pp-wave Ricci/tides and polynomial null identity; finite controls are not proof of all metrology or statistical independence',
 'no_data_fit':True,'physical_identification':False},indent=2))
