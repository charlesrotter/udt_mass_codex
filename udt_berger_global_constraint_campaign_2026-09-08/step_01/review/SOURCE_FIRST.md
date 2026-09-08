# BG1 independent source-first reconstruction

Reviewer: actual separate context `/root/bg1_review`, created with no author
conversation fork. Inherited Codex runtime/model; a distinct backend/model is
UNTESTED. Written 2026-09-08 before reading the author candidate, checker,
outputs, method notes, campaign log, previous whiteboard or other reviews.
Only the work order, question, precise dispatch, required method instructions,
parent startup receipt, four specified registry rows, G315/G330 source proofs
and reports, and G310/G312 current adoption records were read from the project.
Parent informed me that its candidate was frozen at 19:28 UTC; I have not opened
that freeze or candidate. Source identities are sealed separately.

The parent startup receipt reports successful synchronization at
8784f168bf08473b202fc9485eedefcfff920859 and a full 358-row verifier pass.
Reusing that receipt is not an independent startup replay. Review writes are
confined to this directory. No protected payload or old carrier computation.

## Question and premises

On the supplied complete connected compact boundary-free Berger S3,
gamma=a²(sigma1²+sigma2²)+c²sigma3² with a,c>0 and a!=c, fix any signed h!=0
and Lambda=R/2+3h². Positive refers to the metric; the argument requires
neither positive scalar curvature nor positive Lambda. What genuinely smooth
global K solve all G315 constraints? The conditional vacuum equation rests on
the owner-provisional G310/G312 premises, not derived postulates or canon.
G315's sign is K=-L_n gamma/2. No evolution or BG2 line-drift result is claimed.

The geometry, equation and sign are pinned-by-THEORY only within that admitted
conditional arena. The complete initial K and family parameters are freely
supplied data. The exact constructions below are declared restricted families,
not a data-selection law. Mathematical Fredholm/implicit-function tools and
the Cotton conformal identity are imported methods, not physical premises.
All exact computation is CPU, one library thread, 512 MiB address space and
60 CPU/wall seconds per command; no PDE production or GPU. Maximum outcome is
a conditional mathematical family plus precise restrictions, with no promotion.

## 1. Exact scalar and global restrictions

Put K=A+(tau/3)gamma, tr A=0. The original equations are exactly

    (2/3) tau² - |A|² = 6h²,
    div A = (2/3) d tau.

Consequently tau never vanishes, its sign is constant on connected S3, and
|tau|>=3|h|. On the branch containing h gamma,

    tau(A)=3h sqrt(1+|A|²/(6h²)).

Integrating gives

    integral |A|² = (2/3) integral tau² - 6h² Vol.

If one additionally fixes mean(tau)=3h on this branch, the pointwise one-sided
bound forces tau=3h and A=0 everywhere. That is an obstruction only under the
EXTRA mean restriction. Keeping gamma and Lambda fixed does not keep the mean
of tau fixed. In particular, a second-order shift of tau is necessary for a
nonzero infinitesimal tracefree perturbation; insisting on exactly tau=3h
would manufacture a false obstruction.

For every conformal Killing field Y, integrating momentum gives the necessary
compatibility integral tau div(Y)=0. This follows from tr A=0 and
integral <div A,Y>=-integral A:sym(DY)=0. Killing fields cause no obstruction
because div Y=0. This integral test alone is not nonlinear existence.

## 2. The conformal-Killing issue can be resolved on this Berger metric

Use the fully covariant Cotton tensor
C_ijk=D_k(Ric_ij-R gamma_ij/4)-D_j(Ric_ik-R gamma_ik/4).
The invariant-frame Koszul recomputation in independent_check.py gives

    delta=lambda_v-lambda_h=4(c²-a²)/a⁴,
    C_132=(c/a²) delta,
    |C|²=12(c/a²)² delta²
         =192 c²(a²-c²)²/a¹².

Thus |C|² is a positive spatial constant for EVERY positive nonround Berger
metric, including metrics with R<=0. It vanishes at the excluded round point.

The only imported identity used here is conformal invariance of the covariant
Cotton form in dimension three, cott(e^(2f)g)=cott(g). See Sergiu Moroianu,
"The Cotton tensor and Chern-Simons invariants in dimension 3: an introduction",
Proposition 15, page 10, https://arxiv.org/pdf/1509.05156, consulted through the
browser 2026-09-08. This is a mathematical identity on an oriented smooth
Riemannian 3-manifold; S3 meets these hypotheses. No field equation from that
paper is used.

If L_Y gamma=2psi gamma, naturality and that identity give L_Y C=0. Differentiating
its squared norm gives Y(|C|²)=-6psi |C|². The left side is zero and |C|²>0,
so psi=0. Therefore every conformal Killing field is Killing. This uses the
three-covariant Cotton form, not the differently weighted Cotton-York tensor.
It supplies the missing kernel condition without a scalar-spectrum guess.

## 3. Actual small nonlinear families from any small smooth TT seed

Define the conformal Killing operator

    (LW)_ij=D_i W_j+D_j W_i-(2/3)(div W) gamma_ij,
    D W=div LW.

On this smooth compact manifold D is elliptic and formally self-adjoint,
integral <W,DW>=-(1/2) integral |LW|², so its kernel consists precisely of
conformal Killing fields, hence Killing fields by Section 2. Its principal
symbol is -|xi|² I-(1/3)xi tensor xi. Standard compact elliptic Fredholm theory
therefore makes it an isomorphism between the L2-orthogonal complements of
that finite-dimensional kernel in C^(k+1,alpha) and C^(k-1,alpha), k>=2,
0<alpha<1. The same theory gives the usual smooth York decomposition; no
boundary conditions are missing because the manifold has no boundary.

Let sigma range over tracefree divergence-free C^(k,alpha) tensors, a closed
Banach subspace. For W in the indicated complement define

    F(W,sigma)=div LW-(2/3)d[tau(sigma+LW)].

For every W,sigma this takes values in the target complement: both divergences
of tracefree symmetric tensors and gradients are orthogonal to Killing
fields. F is smooth between these Hölder spaces, F(0,0)=0, and D_W F(0,0)=D
because d tau/dA vanishes at A=0. The Banach implicit function theorem gives
an actual unique small W(sigma) for all sufficiently small sigma. Hence

    A=sigma+LW(sigma),
    K=A+(tau(A)/3)gamma

satisfy BOTH original constraints globally, with the original fixed Lambda.
This is a nonlinear existence argument, not only a formal jet. The smallness
radius depends on the supplied gamma,h,k,alpha; no uniform radius near h=0,
roundness or degenerating Berger radii is claimed. W=O(||sigma||²), while
tau=3h+|A|²/(4h)+O(|A|⁴). Both signs of h are retained.

For smooth sigma, W is smooth. More explicitly, the principal symbol of the
negative W-linearization is

    |xi|² I+(1/3)xi tensor xi-(2/tau)xi tensor (A xi).

For |A|/|tau|<1/4 its quadratic form is bounded below by
(1/2)|xi|²|w|². Shrinking the IFT neighborhood achieves this uniformly.
Quasilinear elliptic Schauder bootstrapping then applies to the smooth seed
and metric. This states the actual regularity and ellipticity hypotheses
instead of calling an arbitrary formal correction smooth.

This local family leaves the full global constraint classification open. It
does not prove that any chosen local seed extends with its exact local jets.

## 4. A second, finite-dimensional exact construction avoiding elliptic PDE

There is also an explicit global inhomogeneous family. Choose a nonzero
right-invariant vector field X on SU(2)=S3. It generates left translations,
so it is Killing for the supplied left-invariant Berger metric and is nowhere
zero. Normalize its Lie-algebra value to Euclidean unit length solely as a
parameter convention. If x=gamma(X,X) and m=min(a²,c²), then

    m<=x<=max(a²,c²),
    X(x)=0, div X=0, D_X X=-(1/2) grad x.

The bounds follow by left trivialization: Ad(g^-1)X_e rotates a Euclidean unit
vector. For a!=c its orbit makes x nonconstant. This is supplied isometry data,
not an additional physical object.

For any |epsilon|<1/8 define u(x) as the unique root in (-1/4,1/4) of

    u sqrt(1-u)=epsilon (m/x)^(3/2).

The left side has positive derivative (1-3u/2)/sqrt(1-u) on that interval;
its endpoint values -sqrt(5)/8 and sqrt(3)/8 bracket [-1/8,1/8]. Thus the root
exists uniquely and smoothly for every x in the entire compact metric range,
with no chart singularity or hidden boundary matching. Set

    alpha=h/sqrt(1-u),
    beta=-3 alpha u/(2x),
    K=alpha gamma+beta X-flat tensor X-flat.

The eigenvalues relative to the X direction are alpha, alpha, alpha+beta x.
Direct substitution into the ORIGINAL constraints gives

    (tr K)²-|K|²=6alpha²+4alpha beta x=6h²,
    div K-d(tr K)=(-2alpha'-x beta'-(3/2)beta)dx=0.

The second identity follows from

    u'=-3u(1-u)/(x(2-3u)).

Both scalar identities are checked exactly by a separately written symbolic
implementation. Global smoothness, the Killing properties and the derivative
identity prove all points; the argument is not numerical point sampling.
At epsilon=0, K=h gamma. For epsilon!=0 the tracefree part is

    A=(alpha u/2)(gamma-3 X-flat tensor X-flat/x),
    |A|²=(3/2)alpha²u²,
    tau=3alpha(1-u/2).

The exact ratio (tau/(3h))²=1+u²/[4(1-u)] confirms the necessary trace shift.
The construction works for positive or negative h at the same fixed Lambda.
It is a restricted supplied-data family, with no preferred Killing generator
or amplitude selected. No nonzero Ricci-line drift has been computed here.

Its derivative at epsilon=0 provides a nonconstant smooth TT tensor

    (h/2)(m/x)^(3/2)(gamma-3 X-flat tensor X-flat/x),

which also proves that the TT-seed space in Section 3 contains useful
inhomogeneous data. This observation is not needed to prove the exact family.

## 5. Adversarial controls and limits

The invariant-frame momentum calculation gives

    (div K)_1=(2c/a²-2/c) K_23,
    (div K)_2=(2/c-2c/a²) K_13,
    (div K)_3=0

for a left-invariant symmetric K. On the nonround Berger metric this optional
homogeneous ansatz forces K_13=K_23=0. Therefore a search confined to that ansatz
could miss useful inhomogeneous data; its failure is not a global obstruction.

independent_check.py imports no parent code or outputs. It recomputes the
Ricci tensor from brackets, the Cotton component and norm, the invariant
momentum equation, the full scalar split with all symmetric entries, and
the exact rank-one family's original constraints. Actual hostile algebra
changes executed: beta's 3/2 replaced by 1; wrong Killing acceleration sign;
omitted beta derivative; nonround Cotton declared zero. All yield nonzero
symbolic residuals. These are exact algebra diagnostics, not a proof of the
Fredholm or implicit-function theorem and not a certification of BG2 drift.

No author checker was replayed before this seal. No source package's prior
complete test suite, Git ancestry, external review or full startup audit was
independently repeated. Those retain their original authority and caveats.
The new argument's strongest current status is independent source-first
mathematical reconstruction pending direct review of the frozen candidate.
