import numpy as np
Jz = np.diag([1,0,-1]).astype(complex)
Jp = np.array([[0,np.sqrt(2),0],[0,0,np.sqrt(2)],[0,0,0]],dtype=complex)
Jm = Jp.conj().T
Jx=(Jp+Jm)/2; Jy=(Jp-Jm)/(2j)
def sym(A,B): return (A@B+B@A)/2
J2=Jx@Jx+Jy@Jy+Jz@Jz
Q0=3*Jz@Jz-J2; Q1=sym(Jx,Jz); Q2=sym(Jy,Jz); Q3=Jx@Jx-Jy@Jy; Q4=sym(Jx,Jy)
ops=[Jx,Jy,Jz,Q0,Q1,Q2,Q3,Q4]

# 1) SPAN: do these 8 span the 8-dim space of traceless Hermitian 3x3?
# vectorize each as real 8-vector in basis of Gell-Mann. Just check rank of the 8x9 (flattened) matrix.
M=np.array([O.flatten() for O in ops])
rank=np.linalg.matrix_rank(M,tol=1e-9)
print("Rank of 8 ops in 9-dim matrix space (max meaningful=8 traceless):", rank)

# 2) CLOSURE under commutators: is [A,B] always a real-linear combo of the 8 ops?
#    su(3) is closed under commutator. Build basis from the 8 ops (as 9-vectors), test each commutator.
basis=M.T  # 9 x 8
def in_span(v):
    # least squares residual
    coef,res,rk,sv=np.linalg.lstsq(basis,v,rcond=None)
    recon=basis@coef
    return np.max(np.abs(recon-v))
maxres=0
for i in range(8):
    for j in range(8):
        C=ops[i]@ops[j]-ops[j]@ops[i]
        r=in_span(C.flatten())
        maxres=max(maxres,r)
print("Max commutator-closure residual:", maxres)

# 3) CASIMIR: with a proper su(3) NORMALIZATION the quadratic Casimir of the fundamental is 4/3.
#    The claim is C_2 = (4/3) I_3. But Casimir value depends ENTIRELY on normalization of generators.
#    Check: sum of squares of the 8 ops (unnormalized) = ? proportional to I?
S=sum(O@O for O in ops)
print("sum O^2 (unnormalized):")
print(np.round(S.real,4))
print("Is it proportional to I_3?", np.allclose(S, S[0,0]*np.eye(3)))
print("proportionality const:", S[0,0])
