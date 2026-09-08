# BG2 initial conditional candidate — UNREVIEWED / UNPROMOTED

Question recorded after BG1 review closed and before BG2 computation. Parent
has not read the BG2 reviewer's reconstruction, code or outputs. Mathematical
discovery, then freeze; no numerical outcome-blind preregistration claim.
The BG1 reviewer's auxiliary explicit family was seen but is NOT used here.

## Arena and quantifiers

For EVERY fixed smooth supplied positive definite nonround Berger S3,
gamma=a²(sigma1²+sigma2²)+c²sigma3², a,c>0, a!=c, EVERY signed h!=0 and EVERY
marked point o, fix Lambda=R/2+3h². Claim: arbitrarily close to h gamma in any
fixed C^{k,alpha} data norm, k>=3, 0<alpha<1, there are actual smooth GLOBAL
solutions K of ALL original constraints whose full marked Ricci-line IMAGE
drift Y(o) is nonzero. The metric and Lambda are unchanged. The data need not
match BI3's prescribed pointwise K/DK or its local seed. No symmetry, fixed
trace/mean, carrier/action or physical content is additionally imposed.

This is a reviewed-BG1-dependent CONDITIONAL candidate in the G310/G312
owner-provisional vacuum arena, with G315's negative-K convention and G330's
supplied geometric branch. Not all such data drift; homogeneous/pure-trace
preserving data remain valid. No genericity or complete zero-locus claim.

## 1. FULL drift operator retained

Use xi=e3, eta=xi-flat, P0=xi tensor eta, Pi=I-P0,
B=gamma^{-1}Ric3 with eigenvalues lambda_h=pq-q²/2 and lambda_v=q²/2,
p=2/c,q=2c/a², Delta=lambda_v-lambda_h=q(q-p)!=0.
For EVERY smooth symmetric K, BI1/G337 give

    S(K)_ij=-D^r D_i K_rj-D^r D_j K_ri
             +D^r D_r K_ij+D_i D_j tr K,
    dot B(K)=gamma^{-1}S(K)+2K-sharp B,
    Rline(K)=Pi[(gamma^{-1}S(K))xi+2lambda_v K-sharp xi]/Delta.  (8)

Rline is a real linear differential operator of order2 on the FIXED initial
geometry; the covariant derivatives are NOT commuted using momentum. This is
the exact full image drift Y, not just its principal part. With
kappa=Pi K-sharp xi the full orthogonal projector derivative is

    dot P0=Y tensor eta+xi tensor(Y-flat-2kappa-flat).           (9)

The line is fixed iff Y=0, while the full projector is fixed iff also kappa=0.
The metric-inverse term is indispensable to dot B; it is order0, not absent.
For K=h gamma, S=0 and dot B=2h B, so Rline(h gamma)=0.

## 2. Actual global smooth TT projection

Let delta A=div A on symmetric tracefree tensors and let L and P=delta L be
BG1's conformal Killing operator and self-adjoint elliptic vector operator.
Let G be its generalized inverse, zero on the Killing kernel, inverse on the
orthogonal complement. It is a real classical pseudodifferential operator of
order-2 on the compact manifold; PG=GP=I-proj_kernel. This is a standard
elliptic method with the hypotheses established in BG1, not a new law.

For any smooth global symmetric tracefree tensor F,

    Q F=F-L G delta F.                                      (10)

Pairing delta F with a kernel field X gives
integral <delta F,X>=-(1/2)integral <F,LX>=0. Therefore delta QF=0 exactly;
trace QF=0 exactly; Q preserves every TT tensor. It is a real order0 projection
onto global smooth TT tensors. The projection may introduce nonlocal tails;
compact support or preservation of specified local jets is NOT asserted.

At a nonzero covector zeta, write (temporarily suppressing i factors)

    d_zeta F=F(zeta-sharp, .),
    l_zeta w=zeta tensor w+w tensor zeta-(2/3)<zeta,w>gamma,
    M_zeta=d_zeta l_zeta=|zeta|² I+(1/3)zeta tensor zeta.

M_zeta is positive invertible. Since symbols of delta,L are i d,i l and
that of G is -M^{-1}, the leading symbol of Q is

    pi_zeta=I-l_zeta M_zeta^{-1}d_zeta.                       (11)

It is the projection onto tracefree tensors transverse to zeta. In particular
it fixes each tracefree E with E(zeta-sharp,.)=0. This symbol statement does
NOT replace (10)'s exact global divergence equation.

## 3. The full line operator cannot annihilate all global TT seeds

The principal symbol of S from (8) is

    s_zeta(E)_ij=zeta_i zeta^r E_rj+zeta_j zeta^r E_ri
                 -|zeta|² E_ij-zeta_i zeta_j tr E.            (12)

For tracefree transverse E it reduces to -|zeta|²E. At the chosen point o,
take zeta=e1-flat and E=e2-flat tensor e3-flat+e3-flat tensor e2-flat.
Then pi_zeta E=E and the composite Aop=Rline Q has

    sigma2(Aop)(o,zeta)E=-e2/Delta !=0.                       (13)

This includes the leading symbol of the FULL operator (8); omitted lower-order
terms are not being declared zero in the actual drift. They cannot cancel
(13) for all smooth inputs.

For an explicit existence argument behind that statement, choose a small
coordinate patch around o, a real smooth phase f with f(o)=0, df(o)=zeta and
df nowhere zero on the support of a real cutoff chi, chi=1 near o. Choose a
smooth real tracefree extension E(x) of the stated polarization. Extend

    F_N=chi cos(Nf) E(x)

by zero to the compact manifold. The standard local oscillatory formula for
the order2 operator Aop gives

    Aop F_N(o)=-(N²/Delta)e2+O(N),              N -> infinity. (14)

All coefficients/patch/cutoff/geometry are fixed. Off-diagonal smooth-kernel
contributions decay by integration by parts; the subprincipal terms contribute
at most O(N). Equivalently one may use complex exp(iNf) then take real parts,
since Aop is real and f(o)=0. Thus for SOME sufficiently large FINITE integer
N, T0=Q F_N is a real smooth global TT tensor with Rline(T0)(o)!=0.
No numerical cutoff, limiting field, or selected physical wavelength is used.
This works at every o and every fixed nonround geometry; the frequency bound
may depend on them. No explicit numerical bound is supplied.

## 4. Lift the fixed seed to exact nonlinear data before evolution

FREEZE the one smooth T0 just obtained. Apply BG1 to epsilon T0, for epsilon
sufficiently small of either sign. BG1 gives actual global smooth data

    K_epsilon=h gamma+epsilon T0+O(epsilon²) in C^{k,alpha},
    R+(tr K_epsilon)²-|K_epsilon|²=2Lambda,
    div(K_epsilon-(tr K_epsilon)gamma)=0                      (15)

on the entire initial S3. Its trace adjusts by the original scalar constraint;
mean trace is not silently fixed. The linear differential operator (8) is
continuous C^{k,alpha}->C^{k-2,alpha}, so

    Y_epsilon(o)=epsilon Rline(T0)(o)+O(epsilon²) !=0          (16)

for every sufficiently small nonzero epsilon. This yields arbitrarily small
GLOBAL lawful data with nonzero FULL image drift, not just a formal spatial
jet or a point-sampled constraint residual. The finite N is chosen BEFORE
epsilon tends to zero; there is no interchanged or uniform high-frequency/
nonlinear limit. Smallness constants, lifetime and drift magnitude are not
uniform toward h=0, roundness, degenerating geometry or growing N.

## 5. Exact meaning of normal-time departure and exclusions

Conditionally on the already imported smooth marked Einstein-Cauchy method,
each datum (15) has a local development. Use unit-lapse normal-flow comparison
near the initial slice; normal time t is different from epsilon. The initial
simple Ricci eigengap is nonzero; smoothness/compactness preserve the branch
for a sufficiently short interval. Its unit eigenvector V has horizontal
normal derivative Y_epsilon(o)!=0. Hence under that fixed marking its image
line differs from the original at o for sufficiently small nonzero t. This is
NOT a coordinate-invariant comparison of unrelated slicings, long-time control,
energetic or nonlinear physical instability, topology change, or proof that
the perturbed spatial curves cease to close. A moving line could still belong
to a deformed Hopf fibration. No carrier/action/occupancy/content/scale is selected.

The mathematical counterexample rejects global constraint-forced first-normal
rigidity at the stated data basepoints, not UDT or every preservation result.
Homogeneous preservation and special zero-drift seeds survive. The exact
constraints, global projection, nonzero symbol and nonlinear lift are all
load-bearing. Finite symbol checks alone cannot certify them or catch dropped
lower-order terms; inherit BI1's ENTIRE false-pass/full-tensor review and add
the stated relevant full-tensor anchor. BG1's hard-coded conformal-weight check
remains bookkeeping only. Fresh separate-context review is required before use.
