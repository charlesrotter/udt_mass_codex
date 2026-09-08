# VS1 initial candidate — finite local scale data from the admitted vacuum law

EXPLORATORY CANDIDATE, NOT REVIEWED, NOT_BANKED.2026-09-08.
Baseline4ffd6a4d; WORK_ORDER.md and QUESTION.md control. Initial argument is
frozen before direct reviewer exposure. No previous scientific source changes.

## 1. Premises, type and provenance

Let U be a connected smooth regular time-oriented4D Lorentzian region with
signature(-+++). Supply g with Ric(g)=Lambda g, Lambda constant, and put
k=Lambda/3. The admitted equation is S(g)=Ric(g)-(R(g)/4)g=0, through the
OWNER_ADOPTED_PROVISIONAL G310/G312 premises and registered response gates;
G313 supplies its Einstein arena. This is not CD1/CD2's optional source law.
The base metric, event identifications and query embeddings are supplied
data, not inferred values or new physics. No non-null-gradient, Weyl rank,
symmetry, analyticity, global completion or physical population assumption.

Compare g_hat=Omega^2 g with Omega>0 smooth. Define u=Omega^(-1), a change of
mathematical unknown, not a new physical field. Both metrics live at the same
identified events. Conclusions constrain THIS conformal comparison of a
supplied geometry, not the full space of UDT histories or physical moduli.

This is an application/reconstruction of established conformal-Einstein
mathematics, NOT a claim of a novel theorem in differential geometry. Gover,
arXiv:math/0412393, Section2 equations(2.1)--(2.3), gives general prolongation
for arbitrary conformal geometry. Kuehnel--Rademacher, Conformal Transformations
of Pseudo-Riemannian manifolds, Section5 Lemma5.2/Corollary5.3, gives the exact
conformal Ricci/Hessian relation. Their methods are checked below directly
in the admitted Einstein specialization. No conventional physical field law
is imported. G165/G255 historical censuses are reused, not rerun or exported
past G312 adoption. No equivalent completed UDT connection was found in the
bounded AUDIT_REPORT-name/text screen; that is not a corpus-wide novelty proof.

## 2. Full nonlinear compatibility

Use R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb
+Gamma^a_ce Gamma^e_db-Gamma^a_de Gamma^e_cb, Ric_bd=R^a_bad.
Thus [nabla_c,nabla_d]v^a=R^a_bcd v^b. All contractions below use g;
Box u=g^ab nabla_a nabla_b u, q=g^ab (partial_a u)(partial_b u).

Directly from Levi-Civita's formula, the connection difference is

    C^a_bc=Gamma_hat^a_bc-Gamma^a_bc
          =-u^(-1)(delta^a_b u_c+delta^a_c u_b-g_bc u^a).

Insert this into the ORIGINAL Ricci difference

    Ric_hat_bd-Ric_bd = nabla_a C^a_db-nabla_d C^a_ab
                        +C^a_ae C^e_db-C^a_de C^e_ab.

Contraction in dimension4 gives the exact, not linearized, identity

    Ric_hat=Ric+2u^(-1) Hess(u)
                 +[u^(-1) Box(u)-3u^(-2)q]g.                 (1)

Trace-free parts of a covariant rank2 tensor are the same with respect to
g and u^(-2)g: the inverse-metric trace factor cancels the metric factor.
Since S(g)=0, (1) implies

    S(g_hat)=0 iff Hess(u)=f g,    f=Box(u)/4,    u>0.       (2)

This is necessary AND sufficient as an equation throughout a neighborhood.
A scalar-curvature condition alone is weaker and is not substituted for(2).

## 3. Integrability and closed first-order system

The scalar-gradient commutator gives

    nabla^a Hess(u)_ab = partial_b Box(u)+Ric_ba u^a.

Substitute Hess(u)=f g and Ric=3k g: df=4df+3k du, hence

    df=-k du,       c:=f+ku is a connected constant.

Thus (2) is equivalent to the smooth linear system in six components

    du=mu,
    nabla_a mu_b=(c-ku)g_ab,
    dc=0,                                                    (3)

with u>0. Conversely(3) gives mu=du, the Hessian condition, and by(1) the
full original Einstein equation for g_hat. The six components are u, four
covector components mu, and c, not six physical degrees of freedom.

Taking an uncontracted commutator in(3) yields

    W^d_bac mu_d=0                                           (4)

for every index triple, where
R^d_bac=W^d_bac+k(delta^d_a g_bc-delta^d_c g_ba).
This Weyl-kernel condition is necessary THROUGHOUT U. Its value only at one
event is not asserted sufficient; differentiating it yields further conditions
involving nabla W and (c-ku). Finite point jets are not neighborhood solutions.

Equivalently define on E=R direct-sum T*U direct-sum R the connection

    D_a(u,mu_b,c)=(partial_a u-mu_a,
                  nabla_a mu_b+(ku-c)g_ab, partial_a c).       (5)

Direct commutation gives curvature D^2=(0,-W^d_bac mu_d,0).
The scalar slots vanish, and the constant-curvature part cancels exactly.
These are integrability conditions of the admitted equation, not a new law.

## 4. Actual local realization and finite-data ceiling

On a fixed small connected coordinate neighborhood B with base point p,
let H_p(B) consist of data v in E_p fixed by D-parallel transport around
EVERY piecewise smooth loop based at p in B. This is a vector subspace of
the six-dimensional fiber. Smooth connection coefficients give unique linear
ODE transport along each finite smooth path. A parallel solution restricts to
data in H_p(B). Conversely, for v in H_p(B), transport v from p to x along
any path. Two paths differ by a based loop, so the resulting section is
path-independent. Smoothly varying local paths give a smooth section; path
concatenation and ODE uniqueness give D-parallelness. This constructs an
ACTUAL solution, not a formal Taylor series. If its u(p)>0, shrinking B about
p keeps u>0, yielding a lawful conformal metric there.

For a solution on all of a prescribed B, additionally require u>0 everywhere
on B. Positivity at p guarantees only some smaller neighborhood. For solution
germs the exact requirement is that such a B exists. No analytic regularity,
complete null geodesic, simply-connected physical universe or global boundary
is needed. The loop criterion is exact but is NOT a finite pointwise algorithm
or a claim that curvature at p alone decides existence on every smooth g.

Evaluation of a solution of(3) at p is injective: zero initial data give zero
along every path by linear ODE uniqueness. Hence the vector space of real u
solutions of Hess(u)=(c-ku)g on connected B has dimension at most SIX.
Positive u constitute its restricted positive domain, not a vector space;
Omega=1/u is a nonlinear parametrization. The same bound applies to germs:
any finite collection has a common smaller B, and uniqueness proves their
evaluation map injective. There is no arbitrary-function rescaling freedom
at a fixed supplied base g once the full vacuum equation is required.
Compatible initial data need not be uniquely selected. Some may be related
by isometries/diffeomorphisms; this is not a quotient-moduli count.

As a simple sufficient rigidity sector, if the Weyl map in(4) is injective
on a nonempty open subset, mu=0 there and(3) forces c=ku there. A constant
solution with that value has identical six data at a point of the subset;
ODE uniqueness makes u constant throughout connected B. No claim of genericity
or necessity of that rank condition; the sharper Lorentzian boundary is VS2.

## 5. Connected scalar and a null-path consequence

The quantity

    Q=q+k u^2-2c u                                           (6)

is constant along any solution: dq=2(c-ku)du and dc=dk=0.
Substituting into(1) yields ALL original components

    Ric(g_hat)=Lambda_hat g_hat,       Lambda_hat=-3Q.         (7)

For free target scalar, Q is simply the conserved value of compatible data.
If Lambda_hat is independently prescribed, it imposes the additional algebraic
condition Q(p)=-Lambda_hat/3 on those data; it may not be silently retuned.
For constant u=a>0, Lambda_hat=a^2 Lambda, recovering known homothety.
If a SAME NONZERO Lambda is independently fixed for both metrics this control
forces a=1; for Lambda=0 it does not fix a. This is conditional data bookkeeping,
not scale selection by the source-free equation.

Along every supplied affinely parametrized g-null geodesic gamma(s) contained
in the positive regular domain, equation(2) implies

    d^2[u(gamma(s))]/ds^2 = Hess(u)(gamma',gamma')=0.          (8)

Thus the inverse common scale is affine along each such segment. Affine
normalization and the chosen geometric path are ordinary query data; these
are null geodesics, not physically identified light or instrument trajectories.
No complete-geodesic/global rigidity theorem is imported into this local task.

## 6. Sharp finite bound and checks, not a second campaign step

For flat eta in a small Cartesian chart, EVERY solution is

    u(x)=a+b_i x^i+(c/2)eta_ij x^i x^j.                       (9)

Indeed Hess(u)=c eta follows from(3) at k=0, and integration gives(9);
conversely differentiating(9) verifies it. a>0 supplies local positivity near
the origin for arbitrary real b_i,c. All six initial values occur, so the
universal six-dimensional ceiling is sharp. Here Q=eta^ij b_i b_j-2ca,
and target Lambda_hat=3(2ca-b^2). This standard flat control checks the general
data count and scalar formula, not a new family of physically chosen histories.
It does not answer the nonflat rigidity/null-sector question reserved for VS2.

Planned finite checks recompute(1) by connection contraction at a general
normal-coordinate jet, then independently obtain coordinate Ricci for declared
positive flat/conformally-flat anchors and a failed profile. They also check
conserved scalar, null-path affine behavior, the six-data reconstruction and
actual guard rejection. These are exact finite/symbolic checks supporting
implementation, not proof of universal quantifiers or holonomy realization.

## 7. Completed-pair consequence and honest ceiling

G176/G180's WORKING_FOUNDATIONAL_CLARIFICATION gives, on the SAME supplied
regular auxiliary pair embeddings,

    m_hat=u^(-2)m,     Phi_hat=Phi+log u,
    delta_hat_12=delta_12+log(u_2/u_1).                        (10)

These existing kinematic formulas are now evaluated only on profiles satisfying
the admitted vacuum compatibility, not arbitrary profiles. G131 reduced-control
values stay unchanged under the comparison; full completed data do not.
This is a concrete restriction on scale-dependent geometric readouts, not a
detector law, physical carried content or empirically distinguishing UDT test.

No full geometry is inferred from six numbers: g and its conformal geometry
were supplied throughout. No scalar magnitude/sign, initial data, population,
history, boundary, physical matter/light/source, scale, X_max or canon is selected.
The local positive domain may shrink; smooth existence here is only for this
linear overdetermined scale system, not a UDT nonlinear well-posedness/stability
claim. No optional source model is developed. Review and banking remain pending.
