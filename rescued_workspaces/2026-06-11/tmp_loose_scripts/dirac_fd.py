import numpy as np
import scipy.linalg as sla

def phi_metric(r): return 0.5*np.log(r/(2.0+r))
m=1.0

def build_H(kappa, sign, rmax, N):
    # Discretize the first-order Dirac system as a generalized problem.
    # System: y' = M(r,E) y with M = A0 + E*B  where
    #  G' = (PHI'-k/r)G + (E e^{2PHI}+m e^{PHI})F
    #  F' = (PHI'+k/r)F - (E e^{2PHI}-m e^{PHI})G
    # Rearrange to eigenproblem in E? E appears with e^{2PHI} factor -> generalized.
    # Write as  E * S y = K y  where collect E-terms.
    # G': E e^{2PHI} F  ;  F': -E e^{2PHI} G
    # Non-E parts: G' - (PHI'-k/r)G - m e^{PHI}F =0 ; F' -(PHI'+k/r)F + m e^{PHI}G=0
    # Hard to make symmetric. Use a cleaner standard form via 2nd-order? 
    # Instead: solve det(M-match) approach is the robust one. For a quick independent box check,
    # transform to canonical Dirac form. Let g = e^{-PHI} G? Try u=G, v=F and absorb PHI'.
    # Substituting G=e^{PHI} g, F=e^{PHI} f kills the PHI' diagonal:
    #  G'=e^{PHI}(PHI' g + g'),  plug:  e^{PHI}(PHI'g+g')=(PHI'-k/r)e^{PHI}g+(E e^{2PHI}+m e^{PHI})e^{PHI}f
    #  => g' = -(k/r) g + (E e^{2PHI}+m e^{PHI}) e^{PHI} f
    # similarly f' = (k/r) f - (E e^{2PHI}-m e^{PHI}) e^{PHI} g
    # Now standard Dirac form: g'=-(k/r)g + W+ f ; f'=(k/r)f - W- g
    #   W+ = E e^{3PHI}+m e^{2PHI} ; W- = E e^{3PHI}-m e^{2PHI}
    # Generalized eigenproblem: E (e^{3PHI}) couples. Build matrices.
    r=np.linspace(rmax/N, rmax, N)  # avoid r=0
    dr=r[1]-r[0]
    PHI=sign*phi_metric(r)
    e3=np.exp(3*PHI); e2=np.exp(2*PHI)
    # unknowns g_i, f_i. central diff with Dirichlet BC (g,f ->0 at ends)
    n=N
    A=np.zeros((2*n,2*n))  # K matrix (E-independent)
    Bm=np.zeros((2*n,2*n)) # multiplies E
    def gi(i): return i
    def fi(i): return n+i
    for i in range(n):
        # g' equation: g'_i + (k/r)g_i - m e^{2PHI} f_i = E e^{3PHI} f_i
        # derivative central
        ip=min(i+1,n-1); im=max(i-1,0)
        # build A (LHS, =E*B form): move E-term to B
        # g'_i:
        A[gi(i),gi(ip)] += 1/(2*dr); A[gi(i),gi(im)] += -1/(2*dr)
        A[gi(i),gi(i)]  += kappa/r[i]
        A[gi(i),fi(i)]  += -m*e2[i]
        Bm[gi(i),fi(i)] += e3[i]
        # f' equation: f'_i - (k/r)f_i + m e^{2PHI} g_i = E e^{3PHI} g_i
        A[fi(i),fi(ip)] += 1/(2*dr); A[fi(i),fi(im)] += -1/(2*dr)
        A[fi(i),fi(i)]  += -kappa/r[i]
        A[fi(i),gi(i)]  += m*e2[i]
        Bm[fi(i),gi(i)] += e3[i]
    return A,Bm,r

def levels(kappa,sign,rmax,N):
    A,Bm,r=build_H(kappa,sign,rmax,N)
    w=sla.eig(A,Bm,right=False)
    w=w[np.isfinite(w)]
    real=w[np.abs(w.imag)<1e-6].real
    bound=np.sort(real[(real>0)&(real<0.999999)])
    return bound

for rmax,N in [(40,1200)]:
    print(f"rmax={rmax} N={N}")
    for kappa in [-1,-2,-3]:
        b=levels(kappa,1,rmax,N)
        print(f"  BARE sign+1 kappa={kappa}: {len(b)} in (0,1): {np.round(b[:8],4)}")
    for kappa in [-1,-2,-3]:
        b=levels(kappa,-1,rmax,N)
        print(f"  INV  sign-1 kappa={kappa}: {len(b)} in (0,1): {np.round(b[:12],4)}")
