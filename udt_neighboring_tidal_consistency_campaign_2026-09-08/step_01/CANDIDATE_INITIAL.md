# NT1 — first-neighborhood consistency beyond pointwise tidal reconstruction

CANDIDATE, UNPROMOTED; no direct-review verdict yet. Exact source snapshot
5ece4ae0. This is a necessary local compatibility result, not an inverse-metric
existence theorem, instrument interface or new physical law.

## 1. Quantifiers and supplied data

Consider any supplied smooth time-oriented4D Lorentzian Einstein development
Ric(g)=Lambda g in G310/G312's OWNER-PROVISIONAL bounded arena. Lambda is any
connected constant, not a selected value. Use G358's curvature convention and
a supplied smooth oriented orthonormal frame e0 future, with metric eta=(-+++).
At each event repeat its24 ideal Jacobi queries, with null directions e0±ei
normalized AT THAT EVENT and the specified cyclic screens. Their extension
from one event to the next is new query/comparison data, not an assertion that
these directions are one common affine ray family. No detector or light assumed.

At every event the13 G358 algebraic conditions reconstruct Q_abcd and Lambda.
Write

    Q = W + K S, K=Lambda/3,
    S_abcd=eta_bc eta_ad-eta_ac eta_bd,
    C_ij=E_ij+(Lambda/3)delta_ij,  tr C=0,
    W_i00j=C_ij,  W_i0jk=epsilon_jkl B_li,
    W_ijkl=epsilon_ijm epsilon_kln C_mn.

B is G358's uniquely reconstructed symmetric trace-free mixed curvature, not
an independent field. W is the trace-free spacetime curvature. Smooth values
and first directional variations of these records are the proposed data; no
connection, metric extension or lawful initial gamma,K is inferred from them.

## 2. The connection must not be hidden

Let omega_mu^r_a be defined by nabla_e_mu e_a=omega_mu^r_a e_r. Its metric
compatibility is eta_rr omega_mu^r_a+eta_aa omega_mu^a_r=0 (no repeated-index
sum in this expression). For the reconstructed COMPONENT functions W_abcd,

    J_mu abcd = e_mu(W_abcd)
       -omega_mu^r_a W_rbcd-omega_mu^r_b W_arcd
       -omega_mu^r_c W_abrd-omega_mu^r_d W_abcr.             (1)

J is nabla W in this frame. Formula(1) follows by differentiating the four
arguments and using metric compatibility. A frame normal at ONE event can
have omega=0 there; no parallel frame on a curved neighborhood is assumed.
If omega is unknown at a general W!=0 event, the derivative test below is
conditional on it or an existential constraint on compatible comparison data.
It is not an unqualified test of raw component derivatives. An arbitrary
solution for omega does not prove it is the Levi-Civita connection of a metric
realizing the records. Torsion, curvature and higher/PDE integrability remain.

## 3. Explicit record-derivative conditions

Define D_mu C_ij=J_mu i00j and
D_mu B_li=(1/2)epsilon_jkl J_mu i0jk. For each mu these are symmetric
trace-free matrices, since nabla preserves the algebraic Weyl identities.
This D notation includes the full spacetime slot correction in(1); it is not
just a spatial derivative with e0 or observer acceleration silently fixed.
Define

    (div C)_j=sum_i D_i C_ij,   (div B)_j=sum_i D_i B_ij,
    (curl C)_ij=(epsilon_ikl D_k C_lj+epsilon_jkl D_k C_li)/2,

and the same symmetric curl for B. Necessary equations on every such metric are

    div C=0, div B=0,
    D_0 C + curl B=0,   D_0 B - curl C=0.                  (2)

There are SIX spatial divergence conditions and TEN symmetric trace-free
time-variation conditions. These concern curvature components only; the familiar
form is not an assumed independent field equation or a carried-content law.

Proof. Differential Bianchi for Q and nabla(KS)=0 give

    J_mu abcd+J_a bmu cd+J_b mu a cd=0.                   (3)

Its contraction gives nabla^a W_abcd=0. The b=0,c=0,d=j contractions give
div C=0. The b=0,spatial cd contractions, dualized, give div B=0. The b=i,
c=0,d=j contractions give D0 C_ij+epsilon_ikl Dk B_lj=0; the spatial cd
ones, dualized, give D0 B_ij-epsilon_ikl Dk C_lj=0. The antisymmetric parts
of these curls are the respective divergence constraints; their traces vanish
by symmetry. This gives(2), including its signs in the registered Q convention.

Conversely within the FINITE vector space of Weyl-valued first-derivative
arrays, these equations recover every divergence component and the differential
Bianchi equations. This is finite algebra only: substitute the displayed C/B
representation in(3); the independent rows reduce to(2). The saved24x40
rational Bianchi matrix and its row-reduction certificate verify this explicit
substitution over the full basis, not a sample of spacetime solutions.

The ten time variables are uniquely fixed by the spatial gradients in(2).
The remaining six divergence equations on the30 spatial-gradient variables
are independent: C and B separate, and each spatial divergence map from
gradients of a symmetric trace-free matrix onto a vector is surjective. For
component j choose only D_j C_jj nonzero and compensate the trace in a
different diagonal entry at that SAME derivative index; this produces only
divergence component j. The identical construction works for B. Hence the
40-dimensional first-Weyl-derivative array has16 independent equations and a
24-dimensional kernel. With four initially arbitrary scalar derivatives there
are44 variables,20 independent equations: Bianchi also forces dLambda=0.
These dimensions are first-jet linear algebra, NOT local physical modes or a
parameter count of full Einstein developments. Constant scalar was already owned.

## 4. A genuine connection-independent incompatibility

At an event p where W(p)=0, every omega correction in(1) vanishes, for EVERY
smooth choice of orthonormal frame extension and EVERY compatible connection.
This also works at nonzero constant sectional curvature: the scalar tensor S
is parallel. Thus at p the raw directional derivatives of reconstructed C/B
are the covariant ones. Frame/connection/extrinsic-data freedom cannot repair
a violation of(2) there. This is an eventwise zero, not a flat-neighborhood
assumption, and it does not demand zero initial K or a special Cauchy slice.

Fix any Lambda0. Supply smooth G358 records generated algebraically by

    E(x)=x^1 diag(1,-1,0) -(Lambda0/3) I,    B(x)=0,       (4)

on a chart around x=0. Supply frame directions e_mu(p)=partial_mu at p,
allowing otherwise arbitrary smooth frame/metric/initial-data extensions.
Set all T_i^s from G358's displayed reconstruction; each event passes all13
algebraic conditions, including the SAME constant scalar Lambda0. At p,
W=0, D1 C=diag(1,-1,0), all other first derivatives zero. Therefore

    (div C)_1=1.                                        (5)

No smooth Lorentzian Einstein metric with a smooth orthonormal frame having
those prescribed tangent directions and those ideal records can realize(4)
on any neighborhood of p. Proof by contradiction applies(1)–(2); ANY proposed
metric's own connection drops out at p and gives0=1. It is not an arbitrary
perturbed metric being called a lawful counterexample. It is a record assignment
proved nonrealizable under the stated hypotheses. Coordinate/frame relabeling
transforms the entire derivative tensor; it cannot make its nonzero Bianchi
residual zero. Replacing the supplied directional derivatives is different data.

For clarity, the null records in(4) have zero odd part and even diagonals
H1=diag(-x1,x1), H2=diag(-x1,x1), H3=diag(2x1,-2x1), all offdiagonals zero.
This is a cross-event obstruction beyond G358, not a restatement of one-event
incompatibility or the already known constancy of Lambda.

## 5. Survival, freedom and what is NOT proved

Parallel constant-curvature records satisfy(2), but no new preservation example
is counted as a campaign result. Actual nonconstant lawful realization will be
the separate NT2 question after this review. Passing(2) alone is not a metric
existence theorem. At W!=0 with unknown comparison data, eliminating omega and
solving its metric-integrability problem remain unresolved here; this result
does NOT assert that every raw record derivative has16 directly testable constraints.

Complete initial gamma,K fields must obey G315's original constraints, but
their legitimate freedom is not replaced with a selection law. No fixed recipe,
Hopf stabilization, carrier, source, functional, observer population, scale,
physical propagation/particle law, measured detector signal or canon follows.
The identities are shared with any theory using the same Einstein arena.

## 6. Discovery, checks and review ceiling

The author derived this argument without receiving source-first reviewer findings.
The independent source-first reviewer reported readiness/seal only. An initial
CPU-limit failure, its lost buffered intermediate results and one pre-freeze
performance/progress-output correction are retained in DISCOVERY_HISTORY.md.
No result is credited to that failed run. The corrected run passed before this
freeze; the final run adds an explicit independently formulated C/B equation-map
comparison, not a scientific repair. Exact matrices and actual mutant captures
support finite algebra, not PDE existence or empirical truth.

The author deliberately reuses accepted SC3 tensor/record code: same-code replay
is regression. Raw-minus-identical-connection-action controls are also regression
and cannot independently certify the formula. Direct analytical scrutiny and
the separate-context implementation/argument must carry the load-bearing joins.
No candidate result is reviewed or banked merely by this file or a commit.
