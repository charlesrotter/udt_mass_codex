# IEC1 exposed mathematical review — candidate snapshot

Context `/root/iec_math`, same inherited model/SymPy, fresh before source-first
seal. Parent candidate exposure occurred only after SOURCE_FIRST_SEAL.json.
This report reviews INITIAL_CANDIDATE.md SHA256
43d1e16e32f3805ffe595afc951d8b910b37c96256bed21b68f33ff5ed0eec84,
derive_universal.py 5f5ede29d331547d2f381ea236af11c91075df8e13a697c7d07ed56dcc03d088,
and UNIVERSAL_FORMAL_RESULT.json
fe8d68c2f155ae9fcff7be74dc0d2815ae7e8bb0f0bae486949671e39fe6e2d5.
Parent's CANDIDATE_FREEZE.json provides exact captured construction bindings.

Disposition at this stage: **no mathematical defect found in the inspected
coefficient contractions or protocol; universal acceptance pending two named
checks**. They are the exact associative-log reconstruction and the complete
local metric/transvection justification below. No theorem is inferred from
my finite sphere-product controls.

## Argument and sign audit

The half-log formula is appropriate to the local coset problem. If
G=exp(Z)h with h in the isotropy group, the involution obeys sigma(h)=h and
sigma(exp Z)=exp(-Z), so G sigma(G)^-1=exp(2Z). The relative product
exp(-sU)exp(Ln)exp(bU) maps the first clock event to the origin and the second
to its proper relative position, provided exp(Ln) is the preparation
transvection with parallel differential. No future-clock exchange is assumed.
The later root is F(a,b)=0 and q=-F_b/F_a; these match PSW.

I checked the script's curvature pairings directly. With C=R(n,U),
[u,n]=C and [[u,n],u]=A, [[u,n],n]=B. Every further pair of left brackets
maps X to -R(X,z)w. For an endpoint e in {U,n},

    <e,-R(X,z)w>=sgn(w,e)<X,Cz>,

where R(w,e)=sgn(w,e)C. Applying pair symmetry and skew-adjointness again
gives exactly the degree7 pairing coded with Kij. For a degree3 vector Y,
<Y,-R(X,z)w>=R(X,z,Y,w). These verify all branches of pairing(),
including the signs in the indefinite inner product and the mixed K terms.
The displayed Z3 gives F4=-T(x²+xy+y²)/3 directly.

Parallel curvature implies curvature acts as a derivation of R. Applying C
to R(n,U)=C gives

    0=[C,C]=R(Cn,U)+R(n,CU)=R(B,U)-R(A,n).

Thus the index1=index2 simplification is valid on the stated class and is not
an identity for an arbitrary algebraic curvature tensor. The script applies
the substitutions simultaneously and does not discard a remaining K component
by numerical fitting.

For V=0 the candidate's K00=-T³, K01=K11=K13=0,
K03=-T bb=T³-T|W|² are correct. The cubic T terms cancel and the remaining
coefficient is T|W|²/3. No converse, total-geodesy theorem or sign condition
follows from the vanishing of d4 or d6; the candidate states those limits.

## Independent exact witness contraction

My source-first derivation used a direct sphere embedding, its parallel
transport and two original null-incidence roots. It did not use the candidate
Lie expansion. Its tilted control u=3/4,gamma=5/4,a=3/5,b=4/5 has

    T=9/25, aa=ab=81/400, bb=4329/10000,
    K00=K01=K11=-729/6400,
    K03=K13=-38961/160000.

These values follow from R(X,Y,Z,W)=-det(Xs,Ys)det(Zs,Ws) on the unit
sphere's tangent plane. In particular det(A,U)=det(A,n)=-27/80 and
det(B,n)=-1443/2000. Exact substitution into the candidate gives

    d4=3483/10000, d6=-1371951/16000000,

matching my pre-exposure coefficients. Reversing a reverses ab,K01,K13,
while leaving T,aa,bb,K00,K03,K11 unchanged; it matches the independently
computed negative quartic coefficient and changed sixth coefficient. Aligned
and zero-boost controls also match. These are independent original-incidence
tests of contractions in one metric family; they do not cover the full tensor
space or replace the universal algebra argument.

## Local signature and remainder gate

The indefinite signature is not itself an obstruction. A direct route is to
derive the exponential-chart metric from radial Jacobi fields. For
J_X(V)=R(V,X)X, the pullback differential is parallel transport times

    S_X V=sum_{k>=0}(-1)^k J_X^k V/(2k+1)!.

Consequently the normal-chart metric is <S_X V,S_X W>, analytic and
nondegenerate near0, including null X. No division by g(X,X), curvature
eigenvalue, diagonalizability or positive metric is required. Since
J_-X=J_X, X→-X is a local isometry. Compose the two point symmetries on the
preparation geodesic to obtain a transvection. Its differential is parallel
transport: an isometry preserves parallel transport, and the midpoint symmetry
has differential -I at its center; composing with -I at o removes the sign.

The candidate should write this local argument explicitly or bind inspected
primary mathematics proving the same indefinite local statement. A global
Riemannian Cartan decomposition or classification is neither needed nor a valid
substitute. The local isotropy/transvection bracket identification must also be
bound to the curvature convention. A restriction to an explicitly realized
symmetric-pair metric class is the smallest fallback if that connection is not
completed. No current counterexample defeats the proposed local connection.

Given this connection, the palindrome's inverse is obtained by L→-L; its log
is odd and F/L² is analytic in L². Its two limit-root derivatives are nonzero.
Analytic implicit dependence then supplies the arrival and emission-derivative
remainders and O(L8) in D for fixed geometry/frame, on the regular small branch.
This does not assert a uniform bound or extend through a caustic. The positive
proper-clock ratios and 2-p²>0 follow locally by continuity from1.

## Remaining validation

The Dynkin left-bracket projection should be checked by expanding every saved
Z word back into the associative algebra and comparing all coefficients of
the original log. That provides exact finite algebraic correspondence without
requiring uninspected attribution of the projection theorem. It also catches
word-order/sign and degree errors that comparing the final D alone could miss.
Parent has already named this gate and separate original metric controls.

This review did not rerun the parent's construction as purported independent
verification; it inspected the derivation and independently contracted a
pre-exposure exact source. The existing source-first script/outputs are left
unchanged. No protected payload, scientific registry, CANON or central prose
was edited. Final acceptance awaits the exact gates and final artifact binding.
