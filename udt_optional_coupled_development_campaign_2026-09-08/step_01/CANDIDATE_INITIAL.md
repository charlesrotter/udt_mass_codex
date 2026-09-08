# CD1 initial candidate — independently seeded local constraint family

2026-09-08. Explored then frozen for separate-context review. CONDITIONAL
CANDIDATE, not banked or physically adopted. Prior scope: ../CD1_QUESTION.md.
This is a spacelike-data result, NOT a coupled spacetime-existence theorem.

## 1. Optional model and exact data class

Retain the OPTIONAL comparison Ric=Lambda_* g+beta n dphi tensor dphi,
with supplied constants Lambda_* real and beta!=0, n>0 and nonzero exact
future-null phase. No physical identification, sign or units are selected.
Reuse SM3/G369's necessary constraints with K=-L_N gamma/2:

    R3+(tr K)^2-K_ij K^ij=2Lambda_*+2beta n E^2,
    D_j(K^j_i-delta^j_i tr K)=beta n E^2 v_i.                 (1)

Consider a local slice I x V with coordinates(x,y,z), V a bounded label
rectangle. Work near an interior x0. INDEPENDENTLY SUPPLY smooth profiles
rho(x)>0 and Phi(x) with Phi'(x)>0, plus s0>0, B0!=0 and the constants above.
Profiles need only satisfy these open inequalities after restricting I.
The cross-phase labels(y,z), measure mu=s0|dy dz| and normalized initial
phase phi_0=Phi(x) are supplied and thereafter fixed. This is the regular
positive AC product class, not atoms, singular measures or a selected scale.

Translation symmetry and transverse isotropy are EXPLICIT choices of a
construction class, not a classification of all possible data or a UDT law.
Choose

    gamma=dx^2+a(x)^2(dy^2+dz^2),
    K^i_j=diag(A(x),B(x),B(x)),
    n_0=rho(x),       a(x)=sqrt(s0/rho(x)).                    (2)

Thus n_0 is a seed, not a spacetime Ricci residual. The area part of gamma
is solved from the chosen product, not supplied as a completed metric.
K_ij=diag(A,a^2 B,a^2 B) is symmetric. Set

    E=Phi'(x)>0,       v=partial_x,       N(phi)=-E.           (3)

This fixes the future-null covector on the slice from its spatial restriction:
in Gaussian normal initial gauge q=(-E,E,0,0), q-sharp=E(N+partial_x).
No ambient phase extension is claimed yet.

## 2. Actual cut/product match

Because Phi'>0, each fixed-phi cut of the spacelike slice is x=constant,
with label metric a^2(dy^2+dz^2). Its sheet-area density is J_0=a^2.
Consequently

    n_0 J_0=rho a^2=s0                                             (4)

for every initial phase and retained label, not only one isolated cut.
Equivalently initial current flux on Sigma is rho E a^2 dx dy dz
=s0 dPhi dy dz, with consistent orientation. This fixes the FULL initial
three-form/product including the phase factor E; sheet density is not the
three-dimensional volume density. Mu is finite on V. Transport/preservation
off Sigma remains a CD2 question, not inferred from this match alone.

## 3. Constraint solution as an ordinary differential equation

Write h=a'/a and T=beta rho (Phi')^2. Direct intrinsic geometry gives

    R3=-4a''/a-2h^2,
    (tr K)^2-K_ij K^ij=4AB+2B^2,
    M_x=-2B'+2h(A-B),       M_y=M_z=0.                      (5)

The Hamiltonian constraint determines, wherever B!=0,

    A(x,B)=[2Lambda_*+2T-R3-2B^2]/(4B).                    (6)

The only nontrivial momentum constraint is then the first-order equation

    B'=h[A(x,B)-B]-T/2,         B(x0)=B0.                  (7)

For EVERY seed choice of section1 and every B0!=0, the right side is smooth
in x and B on a neighborhood of(x0,B0); its B derivative is bounded on a
smaller compact rectangle avoiding B=0. The local Picard--Lindelof theorem
therefore gives a unique smooth B on some interval about x0 with B!=0.
The interval may depend on the seeds; there is no common lifespan claim.
Equation(6) then gives smooth A. Substitution in (5) proves ALL FOUR
constraints(1), not just a trace or a necessary zero-momentum condition.
This is local ODE uniqueness at fixed seeds and B0 within this ansatz, not
uniqueness of initial data in the unrestricted class or of a spacetime.

For analytic seed profiles the right side is analytic in(x,B) around B0,
so the same local solution is analytic by the analytic ODE theorem. This
is a method/data subcase useful for a possible analytic development test;
smooth CD1 existence does not require analyticity.

This constructs an entire varying family from phase and density profiles
supplied BEFORE solving K. It is not an exact completed-metric example,
nor an inference that a Ricci-defined current is independently supplied.
No relation between the two profiles beyond the stated inequalities has
been imposed: the fixed product instead determines a. Legitimate data may
be jointly constrained without every component remaining arbitrary.

## 4. What is free, constrained, omitted and not proved

Free-and-explored: rho(x)>0, monotone Phi(x), s0>0, B0!=0, the slice chart,
bounded labels, and chosen symmetry sector. Lambda_* and beta!=0 are supplied
constants of the OPTIONAL law, not results. Dependent: a=sqrt(s0/rho),
E=Phi', future normal phase rate, B from(7), A from(6), and K_ij from(2).
No imposed physical equation of state or profile-selection law occurs.

The nonzero-B restriction makes this particular solution chart regular.
It is SUFFICIENT here, not proved necessary for constrained data: at B=0
the divided formula cannot be used, and the undivided scalar equation has
a separate compatibility condition. This campaign does not classify that
sector, crossings, general three-variable/nondiagonal data, boundaries,
global topology or quotient equivalence of seeds. Phi'>0 fixes this local
orientation/data chart; it is not a physical direction selector.

The constant transverse label density and product force rho to correlate
with area a^2; arbitrary independently fixed gamma,rho,mu would generally
fail(4). This is a compatibility restriction of the CHOSEN product and
ansatz, not proof that all UDT content must have these shapes. Changes of
coordinate description may relate some seeds; no physical-moduli count
or inequivalence theorem is asserted.

Positive outcome at this scope: genuine independently seeded constrained
data exist locally and vary functionally. Ambient exact/null phase,
current transport, coupled PDE existence, gauge constraint propagation,
uniqueness modulo spacetime gauge, continuous dependence, stability and
global completion are NOT proved in CD1. In particular G315's vacuum method
is not a sourced-development theorem. Failure outside this construction
would not be a failure of admitted UDT.

## 5. Verification boundary

The general geometry plus local ODE argument owns the quantifiers. Author
checks differentiate the full intrinsic3D metric and covariant K tensor,
then test the reduced expressions, product/phase signs and deliberately
wrong substitutions. Finite rational anchors are diagnostics, not an ODE
existence proof. Initial candidate/checker/output will be hashed before
direct fresh review. No downstream CD2 use before a reviewed survivor.
