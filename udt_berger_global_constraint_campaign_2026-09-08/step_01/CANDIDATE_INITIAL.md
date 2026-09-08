# BG1 initial conditional candidate — UNREVIEWED / UNPROMOTED

Discovery began after the question/work order and startup orientation. This is
a mathematical exploration followed by candidate freeze, not a preregistered
conjecture. No reviewer reconstruction or advisory whiteboard has been read.
The current reviewed disposition, when available, belongs to REVIEWED_RESULT.md.

## Exact arena and intended conclusion

Fix a smooth compact boundary-free S3 with the supplied Berger metric
gamma=a²(sigma1²+sigma2²)+c²sigma3², a,c>0, a!=c. Positivity means a positive
definite metric, NOT necessarily positive scalar curvature. Set p=2/c,
q=2c/a², Delta=q(q-p)!=0, R=2pq-q²/2. Fix h!=0 and the single constant
Lambda=R/2+3h². Both signs of h and all such a,c are retained. Constants and
smallness neighborhoods may depend on this fixed geometry and h; no estimate
uniform toward h=0 or the round limit is asserted.

G310/G312's owner-provisional vacuum premises and G315/G330's conditional
metric-data interface control. We use the ORIGINAL constraints, with the
G315 negative-K convention dot(gamma)=-2K:

    R+(tr K)²-|K|²=2Lambda,     div(K-(tr K)gamma)=0.               (1)

Claim: near K=h gamma, every sufficiently small smooth transverse-tracefree
(TT: tr T=0, div T=0) tensor T determines an ACTUAL global smooth solution of
(1) by the construction below. Its trace is determined, not additionally
prescribed. This is a local-in-data family on the ENTIRE compact initial
manifold, not a formal jet, local spatial patch, full moduli classification,
physical selection, or stability result. No line-drift claim is made in BG1.

## 1. Exact restrictions, including an optional mean restriction

Write K=H gamma+A with tr A=0, H=(tr K)/3. Equation (1) is exactly

    H²=h²+|A|²/6,             div A=2 dH.                       (2)

On connected S3 every continuous solution has H nowhere zero and fixed sign.
For the sign component through h,

    H(A)=h sqrt(1+|A|²/(6h²)),       dH_A[B]=<A,B>/(6H).         (3)

Thus sgn(h) H>=|h| pointwise, with equality exactly where A=0.
If one additionally imposes the normalized spatial mean of H to equal h,
then integration of a continuous nonnegative quantity forces A=0 everywhere
and K=h gamma. The same holds if H=h pointwise. These are genuine obstructions
within ADDITIONALLY FIXED data classes, not obstructions to (1) with free trace.
For a general conformal Killing field X, integration of the momentum equation
gives integral H div X=0; arbitrary gradient sources need not be compatible.
We establish why that potential obstruction vanishes for this metric.

## 2. No proper conformal Killing fields on nonround Berger S3

Use the covariant three-index Cotton tensor, NOT its Hodge-dual two-index
Cotton-York representation:

    Sch=Ric-(R/4)gamma,     C_ijk=D_k Sch_ij-D_j Sch_ik.

The Berger Ricci eigenvalues are (lambda_h,lambda_h,lambda_v),
lambda_h=pq-q²/2, lambda_v=q²/2. Koszul in the orthonormal frame with brackets
[e1,e2]=q e3, [e2,e3]=p e1, [e3,e1]=p e2 gives

    D1 Sch23=D1 Sch32=-q Delta/2,
    D2 Sch13=D2 Sch31= q Delta/2,
    all other entries of D Sch are zero.

Consequently |C|²=3q²Delta² is spatially constant and strictly positive.
The three-index Cotton tensor is conformally invariant in dimension3 as a
covariant tensor (standard mathematical transformation identity; see methods).
If L_X gamma=2psi gamma, naturality under the local flow of X and conformal
invariance give L_X C=0. Contracting with three inverse metrics yields

    X(|C|²)=-6psi |C|².

The left side is zero and the norm is nonzero, so psi=0. EVERY conformal
Killing field is therefore a Killing field and has div X=0. No Cotton field
equation, gravitational action, carrier, or additional physical law was used.

## 3. Global elliptic inverse and nonlinear realization

Define the tracefree conformal Killing operator on one-forms (identified with
vectors by gamma),

    (LW)_ij=D_i W_j+D_j W_i-(2/3)(div W)gamma_ij,
    P W=div LW.

Integration by parts on this closed manifold gives

    integral <V,PW>=-(1/2) integral <LV,LW>.                    (4)

P is self-adjoint elliptic with symbol
-|zeta|² I-(1/3)zeta tensor zeta; its kernel is exactly the conformal Killing
fields, hence exactly the Killing fields by section2. Let X^{k+1,alpha} be
C^{k+1,alpha} one-forms L2-orthogonal to that finite-dimensional kernel, and
Y^{k-1,alpha} the corresponding orthogonal subspace of C^{k-1,alpha}; take
k>=3 and 0<alpha<1. Compact elliptic Fredholm theory and Schauder estimates
give a bounded isomorphism P:X->Y. Restriction is essential: P is NOT invertible
on all vector fields. No absence of isometries is assumed.

Let TT^{k,alpha} be the closed Banach subspace of symmetric C^{k,alpha} tensors
with zero trace and divergence. For T in it, set A=T+LW and define

    F(W,T)=P W-2 d[H(T+LW)] : X x TT -> Y.                     (5)

The target really is Y: PW is orthogonal to the kernel by (4), and dH is
orthogonal to every Killing field by integration by parts. The Nemytskii map
H is smooth near A=0 because h!=0; multiplication/composition and one spatial
derivative have the indicated Holder mapping properties. F is C-infinity,
F(0,0)=0, and D_W F(0,0)=P, D_T F(0,0)=0. The Banach implicit-function theorem
therefore yields neighborhoods and a smooth map W(T) in X with

    W(0)=0,    D W(0)=0,    ||W(T)||_{k+1,alpha}=O(||T||²_{k,alpha}). (6)

For smooth sufficiently small T the solution is smooth. Explicitly,

    D_W F[V]=P V-(1/3)d[<A,LV>/H].                            (7)

Its second-order principal part is a uniformly small perturbation of P when
|A|/|h| is small. Shrinking the IFT neighborhood ensures strong ellipticity
(with the negative sign convention of P). Smooth gamma,T and standard
quasilinear elliptic regularity then bootstrap W from C^{k+1,alpha} to smooth;
the square root is uniformly separated from zero. This regularity step is
part of the imported method, not a numerical convergence inference.

Finally define A(T)=T+LW(T), H(T) by (3), K(T)=H(T)gamma+A(T).
The scalar identity in (2) holds pointwise EXACTLY, and F=0 makes its momentum
identity hold globally EXACTLY. Substitution into (1) gives both original
constraints, with the SAME gamma and Lambda. For a fixed smooth TT seed T0,

    K(epsilon T0)=h gamma+epsilon T0+O(epsilon²) in C^{k,alpha}.

These are actual nonlinear data, not merely solutions of the linearized
constraints. No explicit lower bound for the allowed epsilon interval is
claimed. The TT seed is legitimate constrained initial-data freedom; it is
not asserted to parameterize all distant solutions or any physically selected
population. Pure longitudinal A alone gives only the nearby zero solution
in this chosen slice, by local uniqueness; no global no-longitudinal theorem.

## 4. Limits and meaningful alternatives

The round case loses the Cotton argument, h=0 loses this smooth square-root
basepoint, and a boundary introduces boundary/adjoint conditions. Those cases
are outside this result, not shown impossible. Fixing trace or its mean at
the baseline really removes the family; allowing its constraint-required
change does not change a physical premise or retune Lambda. Large data,
genericity, global-in-time evolution, closed-orbit persistence, topology and
physical stability remain untouched. BG2 must separately establish that some
global TT direction has nonzero FULL marked Ricci-line drift; this result
alone does not.

Analytical proof owns the existence/regularity claim. The exact finite algebra
checks can catch formula defects but cannot certify Fredholm/IFT hypotheses,
smoothness or exhaustive global behavior. Separate-context review is required
before any downstream use; imported mathematical tools do not select UDT
physical content. BI1/BI3 are context, not needed in this BG1 proof.
