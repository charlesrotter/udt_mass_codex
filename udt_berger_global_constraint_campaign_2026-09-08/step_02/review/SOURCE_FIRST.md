# BG2 independent source-first reconstruction — conditional, not promoted

Written before any BG2 author candidate, code, output, campaign log or advisory
material exposure. Only the dispatched original sources, full BI1 review and
completed BG1 reviewed family were used. BG1's reviewer auxiliary construction
was not read. Mathematical exploration preceded this proof freeze.

## 1. Fixed objects and full drift

Fix a,c>0 with a!=c, gamma=a²(sigma1²+sigma2²)+c²sigma3² on the entire
smooth compact boundary-free S3; p=2/c,q=2c/a², delta=q(q-p)!=0.
Let V=e3 be either oriented unit representative of the initially simple Ricci
line; lambda_v=q²/2, lambda_h=pq-q²/2. Fix signed h!=0 and
Lambda=R/2+3h² once. No positivity of R or Lambda is assumed.

G310/G312 remain owner-adopted provisional premises. G315 supplies the
conditional original constraints and gamma-dot=-2K convention; G330 supplies
the metric and gap. G337's full uncommuted Ricci variation and reviewed BI1
supply the following linear differential operator on arbitrary smooth K:

    S(K)_ij=-D^r D_i K_rj-D^r D_j K_ri+D^r D_r K_ij+D_i D_j tr K,
    D(K)=Pi_h [S(K)^sharp V+2 lambda_v K^sharp V]/delta.          (A)

Here Pi_h=I-V tensor V-flat. D(K) is the horizontal marked normal velocity
of the image line; neither the connection terms nor inverse-metric term is
removed. For constant K=h gamma, S(K)=0 and D(K)=0. This is not the same as
the full orthogonal-projector derivative. With k=Pi_h K^sharp V,

    P-dot=D(K) tensor V-flat+V tensor [D(K)-2k]-flat.             (B)

Thus Y=D(K)!=0 proves image drift, and consequently also nonzero projector
drift. A vanishing Y alone would not show a stationary full projector.

## 2. Actual global TT fields, including the kernel

Let E=S²_0 T* S3 be tracefree symmetric tensors, L the conformal Killing
operator and P=div L on one-forms. Let G be the L2-orthogonal generalized
inverse of P, zero on its finite-dimensional kernel. Then P G=I-Q, where Q
projects onto conformal Killing fields. In BG1 these are exactly Killing
fields. The existence and smoothness of G follow from compact elliptic
Fredholm theory; no inverse on the full vector space is asserted.

For ANY smooth tracefree q, integration by parts gives

    <div q,X>_L2=-1/2 <q,LX>_L2=0    whenever LX=0.

Therefore Q div q=0 exactly, and

    T(q)=q-LG div q                                                (C)

is smooth on the ENTIRE S3, tracefree and exactly divergence-free. Nonlocal
projection may spread the field beyond its original support; compact support
of the resulting TT field is not claimed. Equation (C), not an approximate
local tensor, is the input to BG1.

The additional imported mathematical fact used here is that the orthogonal
generalized inverse of a smooth elliptic operator on a compact manifold is
a pseudodifferential operator of opposite order, with finite-rank smoothing
kernel corrections. Consequently G has order -2 and T has order0. The
calculus and principal symbols apply to vector bundles. Hypotheses match:
smooth compact boundary-free S3, smooth bundles/density/coefficients, elliptic
self-adjoint P, and the exact kernel complement. These are analytic methods,
not a field equation or physical premise. See Melrose, Chapter6, Theorem6.2,
equations(6.48)--(6.49),(6.58), and Theorem6.3:
https://math.mit.edu/~rbm/iml/Chapter6.pdf .

## 3. Principal symbol and a smooth global seed with nonzero exact drift

At a point o in an orthonormal coordinate frame, use Fourier convention
partial_j -> i zeta_j. On tracefree q the principal symbols are

    sigma(P)=-[|zeta|² I+(1/3)zeta tensor zeta]=-M,
    sigma(T)q=q-l_zeta M^-1(q zeta),
    l_zeta w=zeta tensor w+w tensor zeta-(2/3)<zeta,w>I.

This projection has zero trace and zeta-contraction and acts identically
when q zeta=0. Directly from the FULL (A), its second-order numerator is

    sigma(S)q=zeta tensor(q zeta)+(q zeta) tensor zeta
                 -|zeta|²q-(tr q)zeta tensor zeta.

It therefore equals -|zeta|²q on TT polarizations. Lower-order terms still
remain in (A). At any prescribed o choose orthonormal e1,e2,V, set
zeta=e2-flat, q_o=e1-flat tensor V-flat+V-flat tensor e1-flat. Then

    tr q_o=0, q_o zeta=0,
    sigma_2(D T)(o,zeta)q_o=-e1/delta !=0.                        (D)

This nonzero symbol can be realized as a nonzero value on a smooth global
TT field. Choose coordinates x with x(o)=0, dx2(o)=zeta and a smooth compactly
supported tracefree tensor q(x) in that coordinate patch with q(o)=q_o.
It exists by taking a bump times a local tensor and subtracting its gamma
trace. Extend it by zero; set f_N=q cos(N x2), T_N=T(f_N).

The classical symbol expansion at o gives

    D(T_N)(o)=-N² e1/delta+O(N),    N -> +infinity.               (E)

This is an asymptotic for the FULL operator D composed with the exact global
projection. To see why: locally the Fourier formula for an order2 symbol a
applied to q exp(iN x2) is the integral of
a(o,N zeta+eta) q-hat(eta); its leading term is N² a2(o,zeta)q(o).
Symbol remainder/first expansion terms give O(N); the rapid decay of q-hat
controls the tail. Kernel terms away from o are smoothing and integration
by parts in x2 makes their contributions rapidly decaying. The same leading
term holds at -zeta, so taking the real part gives (E). The construction uses
a fixed smooth cutoff, not a discontinuous or asymptotically shrinking one.
Local quantization/symbol estimates are standard analytic methods; see
Melrose, sections2--3 of
https://math.mit.edu/~rbm/18-155-F15/PseudodifferentialOperators.pdf .

For sufficiently large but FINITE N, (E) forces D(T_N)(o)!=0. Fix ONE such
N once and for all, defining the actual smooth global TT tensor T0=T_N.
No explicit threshold, global TT-array solve or pointwise numerical value
is claimed. This proves existence for every fixed declared background and
every marked o. Neither uniform N nor uniform constants toward roundness,
h=0 or degenerating radii are asserted. A principal symbol on its own would
not be a global datum; (C) and (E) are the missing global realization link.

## 4. From the fixed seed to exact nonlinear constraints and actual drift

The entire completed BG1 candidate/review, PROVISIONAL and UNPROMOTED, gives
for sufficiently small epsilon in C^(k,alpha), k>=3,

    A_e=epsilon T0+L W(epsilon T0),
    H_e=h sqrt(1+|A_e|²/(6h²)),
    K_e=H_e gamma+A_e=h gamma+epsilon T0+O(epsilon²),
    W(0)=0, DW(0)=0,
    div A_e=2dH_e, H_e²=h²+|A_e|²/6.                           (F)

These are global smooth tensors. The ORIGINAL Hamiltonian identity is
R+(3H_e)²-[3H_e²+|A_e|²]=R+6h²=2Lambda and the ORIGINAL momentum
is div(K_e-3H_e gamma)=div A_e-2dH_e=0 on all S3. Trace is allowed to
change as the constraints require; no pointwise or spatial-mean trace fixing
is hidden. Both signs of h retain the square-root branch through h.

D:C^(k,alpha)->C^(k-2,alpha) is bounded and linear at fixed gamma.
Applying it to (F), with fixed N and T0, gives

    Y_e(o)=epsilon D(T0)(o)+O(epsilon²).

The nonzero first coefficient implies Y_e(o)!=0 for every sufficiently small
nonzero epsilon. K_e approaches h gamma in the stated norm, so data are
arbitrarily small. ALL nonlinear correction and curvature terms remain; they
cannot cancel the nonzero linear coefficient for all sufficiently small
epsilon. The frequency limit was used only to select a single seed before
the small-data limit. There is no exchanged limit and no physical wavelength
or amplitude selected by this argument.

Conditionally on the imported smooth marked Einstein-Cauchy method used in
the source arena, each fixed datum has a local normal development. The
initial nonzero simple gap persists for a sufficiently short interval; a
nonzero initial line derivative entails line departure at o for sufficiently
small nonzero normal time t. Epsilon and t are distinct. No global-in-time
conclusion, orbit closure change, fibration loss, topology change, genericity,
particle stability, physical size, scale, carrier, action or canon follows.

## 5. Checks and adversarial limits

The corrected independently written SymPy3x3 code gives17 exact checks and
FIVE executed mutations caught. It verifies the full TT projection symbol,
the TT Ricci principal symbol, the mixed polarization, direct invariant-frame
Koszul curvature differentiated before using any Ricci-variation formula,
agreement of all9 entries with the full uncommuted formula, and moving-metric
projector algebra. For arbitrary constant K13=c0, its lower-order anchors are
S13=-(2pq+q²)c0 and B-dot13=-2pq c0, explicitly detecting the raising term.
This constant off-constraint tensor is an ALGEBRA control, not the global
lawful drift witness. The global existence conclusion is owned by (C)--(F).

The initial reviewer assembly-order failure and corrected result are preserved
in source_first_check.*, source_first_check_corrected.* and PRESEAL_FAILURE.md.
The correction adds a separate loop so the whole connection tensor exists
before its derivative is assembled. No author scientific repair was consumed.
Exact arithmetic is not PDE/numerical certification. BG1/BI1's inherited
review caveats, shared SymPy and source-method overlap remain. No author
program was imported; independent implementation is not a different symbolic
engine, different model or formal proof. Earlier full suites and startup
audit were not replayed. No unresolved obstruction was found in this
source-first reconstruction; actual author comparison remains pending.
