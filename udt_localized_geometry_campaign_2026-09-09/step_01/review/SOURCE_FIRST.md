# LG1 review — source-first stage A

Reviewer `/root/lg1_review`, fresh separate context; exact model UNKNOWN. Baseline
`78c3092b2120a80c8bbabb8024b4448d27c36a00`, branch grok, verified on disk.
Parent owns Git synchronization and full365 audit. The completed full365 status
remains NOT_PASSED at G325; no independent full365 pass is asserted here.
This file is saved before exposure to the parent's LG1 candidate, code, or output.

## Exposure and authority

Read bounded startup/current pointers, AGENTS, CLAUDE method/trigger/discipline,
no-shortcuts, completeness-map, verifier-before-record, CROSS_MODEL_VERIFY, campaign
CAMPAIGN_LOG, G310/G312 adoption records, and G303/G315/G324 exact derivations.
The task statement and intended question are exposed. NR1/NR2 proof and parent
LG1 proof/code/results are unexposed. NR1/NR2 are only UNPROMOTED motivation.
No physical premise, action, source, carrier, boundary object, or topology change
is introduced. The fixed exterior supplies Lambda=0, not UDT scalar selection.

## Independent full local adjoint calculation

In affine orthonormal coordinates on the supplied T=T0>0 slice, write

    gamma0 = I, K0 = diag(a,b,b),
    a = 1/(3 T0), b = -2/(3 T0), tau = -1/T0.

The complete constraints are H=R+tau^2-|K|^2 and M_i=D_j(K^j_i-tau delta^j_i).
Use the normalized constraint map (J,H)=(-2M,H) and background pairing
integral(Y^i J_i + N H)dV0. Overall invertible normalization changes no kernel.
For gamma-variation h and covariant K-variation q, its full flat-background formal
adjoint has q coefficient

    A_ij = 2 [partial_(i Y_j) - div(Y) delta_ij - N K0_ij
               + N tau delta_ij],

and h coefficient

    B_ij = div(Y) K0_ij - K0_li partial_j Y^l - K0_lj partial_i Y^l
           + (K0_ql partial_q Y^l) delta_ij
           - Delta(N) delta_ij + partial_i partial_j N
           + 2N (K0^2)_ij - 2N tau K0_ij.

These coefficients follow by varying all four constraints and integrating by
parts; Chrusciel--Delay equation (2.4) supplies an external algebra cross-check,
not the premise or a gluing assertion. In particular the metric terms in M
cannot be discarded.

A=0 implies div(Y)=N tau and partial_(i Y_j)=N K0_ij. Substitution into the
trace of B=0 gives Delta N=N tau^2, using |K0|^2=tau^2. Its diagonal equations
give N_ii=N tau k_i. The compatibility identity for a symmetric gradient in the
two equal-eigenvalue directions is

    partial_z^2(partial_y Y_y) + partial_y^2(partial_z Y_z)
      - partial_y partial_z(partial_y Y_z + partial_z Y_y) = 0.

Hence b(N_zz+N_yy)=2 tau b^2 N= -8 N/(9 T0^3)=0. Therefore N=0 on every open
connected chart; no periodicity, global integration, or assumed time symmetry
was used. Then Y is a Euclidean Killing field, Y=c+Omega x, Omega antisymmetric.
B=0 requires [K0,Omega]=0. Since a differs from b, only Omega_yz is free.

The complete local kernel is thus precisely four-dimensional:

    (N,Y) = (0, partial_x), (0, partial_y), (0, partial_z),
            (0, y partial_z - z partial_y).

All four candidates satisfy the full equations. Completeness follows from the
local no-lapse argument and the full Euclidean Killing equation, whose second
derivatives vanish by differentiated permutations. On the compact translation
quotient, descent requires Omega ell=0 for every lattice vector ell. A full-rank
lattice forces Omega=0. The global kernel is exactly three-dimensional.

## Localization and the linear/nonlinear distinction

For a correction supported in an embedded ball, local KIDs matter. In particular
the rotation gives an integration-by-parts identity even though it does not
descend globally: work on the containing affine chart, with the correction flat
at its outer boundary. For the collar correction problem use all local adjoint
modes on that collar. Do not substitute the three global torus modes.

If P0(h,q)=f with support in this chart, a necessary condition is
integral(Y dot f_J)=0 for each of the four Y. These are cokernel orthogonality
conditions for a linear source. They are not four extra equations on an arbitrary
already homogeneous linear solution P0(h,q)=0, and they do not prove surjectivity
or a nonlinear gluing theorem.

There is also an exact finite-amplitude identity. Define the contravariant
weight-one density pi^ij=sqrt(det gamma)(K^ij-tau gamma^ij). This is simply a
change of data variables; it imports no action. Let h=gamma-gamma0 and
p=pi-pi0. If the pair is smooth, lawful, and identical to background outside the
ball, integration of the momentum constraint against any background local Y gives

    0 = integral pi^ij (L_Y gamma)_ij d^3x
      = integral p^ij (L_Y h)_ij d^3x.

Boundary terms vanish because the difference has compact support. The first
background term vanishes since L_Y gamma0=0; the term pi0 L_Y h integrates to
zero because L_Y pi0=0. Rotation requires the full tensor Lie derivative, not
just componentwise directional differentiation. Thus four exact balances are
necessary; they are quadratic in (h,p), but nonlinear in (h,K-K0).

For a C2 one-parameter exact family through background, write h=epsilon h1+O(epsilon^2),
p=epsilon p1+O(epsilon^2). The necessary second-order condition is
integral p1 L_Y h1=0 for all four local modes. This is a tangent integrability
obstruction. A vanishing quadratic tangent charge is not proof of an exact
family, and neither these four balances nor the full linear constraints imply
the nonlinear Hamiltonian and momentum equations. Finite data must satisfy the
exact constraints, positivity, smooth collar matching, and the geometric
nontriviality requirement. A pure compact diffeomorphism or reslicing is not an
acceptable changed-spacetime witness.

For prescribed lawful interior data, split the exact charge into interior and
transition contributions. The transition must cancel the interior charge.
Nonzero interior charge alone does not force a change outside the outer ball.
No statement here establishes that a transition accomplishing this always exists.

## Method feasibility and survivor

Public primary methods inspected: Chrusciel--Delay, arXiv:gr-qc/0301073v2,
equation (2.4), Section 3 and Theorem 8.15; Chrusciel--Isenberg--Pollack,
arXiv:gr-qc/0403066, Theorem 1.1. Their absence-of-local-KIDs localization route
does not apply directly: this background has the four local KIDs above. The
connected-sum operation also does not answer a fixed-topology replacement task.
An applicable projected solve plus an actual finite-dimensional balance argument
could potentially proceed with symmetry, but those are additional mathematical
proof obligations; the kernel count alone supplies neither.

Source URLs: https://arxiv.org/pdf/gr-qc/0301073v2 and
https://arxiv.org/pdf/gr-qc/0403066 . External sources supply checked methods only.

SOURCE-FIRST ASSESSMENT: precise necessary local gates are available in the
authorized scope; automatic arbitrary-interior gluing is unsupported. The local
rotation is the likely false-pass trap. LG1 can support a reviewed obstruction
map, while exact sufficiency remains a separate construction/analysis task.

Not performed: source-package full replays, NR1/NR2 reconstruction, general
smooth constraint surjectivity proof, exact localized witness, time evolution,
stability, physical identification, or promotion. No scientific grade changes.
