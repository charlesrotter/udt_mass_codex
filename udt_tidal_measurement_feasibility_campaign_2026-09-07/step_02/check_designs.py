#!/usr/bin/env python3
"""Exact author finite-design controls; examples do not supply general proof."""
import json
import platform
import sympy as s

checks=[]
records={}
def guard(name,condition):
    assert condition,name
    checks.append(name)
def serial(matrix):
    return [[str(x) for x in row] for row in matrix.tolist()]
def design(name,P,N):
    n=P.cols
    p=P*s.ones(n,1)
    Q=P*N
    M=p.row_join(Q)
    left=M.T.nullspace()
    C=s.Matrix.vstack(*[v.T for v in left]) if left else s.zeros(0,P.rows)
    ranks={'P':P.rank(),'M':M.rank(),'Q':Q.rank(),'C':C.rank(),'CP':(C*P).rank()}
    guard(name+':left-annihilator',C*M==s.zeros(C.rows,M.cols))
    guard(name+':signal-rank',ranks['CP']==ranks['P']-ranks['M'])
    identifiable=M.rank()>Q.rank()
    records[name]={'P':serial(P),'N':serial(N),'M':serial(M),'C':serial(C),
                   'ranks':ranks,'absolute_kappa_identifiable':identifiable}
    return M,C,identifiable

n=4
one=s.ones(n,1)
t=s.Matrix(range(n))
I=s.eye(n)
M,C,absolute=design('identity_no_nuisance',I,s.zeros(n,0))
guard('absolute_scalar_and_three_tests',absolute and C.rows==3)
M,C,absolute=design('unknown_constant_offset',I,one)
guard('absolute_alias_but_three_tests',not absolute and (C*I).rank()==3)
M,C,absolute=design('unknown_affine_drift',I,one.row_join(t))
K=s.Matrix([[-1,2],[-2,3]])
CA=(-K).row_join(s.eye(2))
MA=M[:2,:]
MB=M[2:,:]
guard('training_predicts_without_unique_parameters',K*MA==MB and MA.rank()<M.cols)
guard('two_genuine_signal_contrasts',CA*M==s.zeros(2,M.cols) and CA.rank()==2)
quadratic=t.applyfunc(lambda x:x*x)
guard('quadratic_departure_retained',CA*quadratic==s.Matrix([2,6]))
guard('affine_departure_hidden',CA*(3*one+2*t)==s.zeros(2,1))
bad_kernel=s.Matrix([0,0,1])
guard('one_training_epoch_insufficient',M[:1,:]*bad_kernel==s.zeros(1,1) and M[1:,:]*bad_kernel!=s.zeros(3,1))
u=s.symbols('u',positive=True)
bounds=s.Matrix([sum(abs(x)*u for x in row) for row in CA.tolist()])
guard('worst_case_bounds',bounds==s.Matrix([4*u,6*u]))
Sigma=s.eye(4)+one*one.T/3
cov=CA*Sigma*CA.T
guard('shared_constant_noise_cancels_without_independence',cov==CA*CA.T)
guard('independent_A_B_noise_not_assumed',Sigma[0,2]!=0)
records['prospective_affine']={'K':serial(K),'C_AB':serial(CA),'quadratic_response':serial(CA*quadratic),
    'ambiguity_vector':serial(bad_kernel),'bounds':serial(bounds),'correlated_covariance':serial(Sigma),
    'residual_covariance':serial(cov)}
M,C,absolute=design('arbitrary_offsets',I,I)
guard('arbitrary_offsets_kill_tests',C.rows==0 and not absolute)
P=I-one*one.T/n
M,C,absolute=design('centering',P,one)
guard('lost_DC_retains_three_signal_tests',not absolute and (C*P).rank()==3 and C.rows==4)
P=one*one.T/n
M,C,absolute=design('only_mean',P,s.zeros(n,0))
guard('mean_no_unused_signal_test',absolute and (C*P).rank()==0)
M,C,absolute=design('scalar_erasure',s.zeros(n),s.zeros(n,0))
guard('scalar_erasure_no_information',not absolute and (C*s.zeros(n)).rank()==0)
P=s.Matrix([[1,0],[1,0]])
M,C,absolute=design('duplicated_single_input',P,s.zeros(2,0))
guard('nonzero_residual_can_be_vacuous_for_signal',C.rows==1 and C!=s.zeros(1,2) and C*P==s.zeros(1,2))
guard('duplicated_B_not_new_query',P.row(0)==P.row(1))
print(json.dumps({'kind':'AUTHOR_EXACT_DESIGN_CONTROLS_NOT_GENERAL_PROOF',
    'python':platform.python_version(),'sympy':s.__version__,'checks':checks,
    'count':len(checks),'pass':True,'designs':records},indent=2))
