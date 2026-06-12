import numpy as np
# The DEEP fact being tested: ANY 8 linearly-independent traceless Hermitian 3x3 matrices
# automatically span su(3) and automatically close under commutator -- because the set of
# traceless Hermitian 3x3 matrices IS the Lie algebra su(3) (it's a vector space closed under [,]/i).
# So "closure to 1e-16" and "span = Gell-Mann space" are GUARANTEED for ANY 8 indep traceless
# Hermitian 3x3 ops. It tests linear independence, NOT a special property of rank-1+rank-2.

# Demonstrate: take 8 RANDOM traceless Hermitian 3x3 matrices. They will also "close as su(3)".
np.random.seed(0)
def rand_herm_traceless():
    A=np.random.randn(3,3)+1j*np.random.randn(3,3)
    H=(A+A.conj().T)/2
    H=H-np.trace(H)/3*np.eye(3)
    return H
ops=[rand_herm_traceless() for _ in range(8)]
M=np.array([O.flatten() for O in ops])
print("Random 8 traceless-Hermitian: rank =",np.linalg.matrix_rank(M,tol=1e-9))
basis=M.T
def in_span(v):
    coef,_,_,_=np.linalg.lstsq(basis,v,rcond=None)
    return np.max(np.abs(basis@coef-v))
mr=max(in_span((ops[i]@ops[j]-ops[j]@ops[i]).flatten()) for i in range(8) for j in range(8))
print("Random ops commutator-closure residual:",mr)
print(">>> Random unrelated ops ALSO 'close as su(3)' to machine precision.")

# Casimir 4/3: comes from RESCALING generators to the standard su(3) normalization Tr(T_a T_b)=1/2 delta_ab.
# For ANY orthonormal (in trace) basis of su(3) fundamental, sum T_a^2 = C_2(fund) I = 4/3 I. Identity-true.
# Build Gell-Mann, normalize T=lambda/2, sum squares:
l1=np.array([[0,1,0],[1,0,0],[0,0,0]]);l2=np.array([[0,-1j,0],[1j,0,0],[0,0,0]])
l3=np.array([[1,0,0],[0,-1,0],[0,0,0]]);l4=np.array([[0,0,1],[0,0,0],[1,0,0]])
l5=np.array([[0,0,-1j],[0,0,0],[1j,0,0]]);l6=np.array([[0,0,0],[0,0,1],[0,1,0]])
l7=np.array([[0,0,0],[0,0,-1j],[0,1j,0]]);l8=np.array([[1,0,0],[0,1,0],[0,0,-2]])/np.sqrt(3)
T=[x/2 for x in [l1,l2,l3,l4,l5,l6,l7,l8]]
print("Sum (lambda_a/2)^2 =",np.round(sum(t@t for t in T).real,4)[0,0],"* I  -> the 4/3 is a normalization identity for ANY su(3) fund basis")
