# ERC1 mathematical source-first argument and frozen check plan

Reviewer: fresh separate-context Codex mathematical subagent, inherited model;
the exact backend runtime/model identifier is not exposed. No different-model,
different-library, human or formal-proof claim. Parent startup is attributed to
the dispatch (including its prior full406 audit); reviewer independently observed
branch grok and HEAD b01ba4e0b41ed6b525f10c3db44dc7ffd8777781, no tracked dirt at
that inspection, and the preserved untracked names without reading their payloads.
This is a scoped review, not a replay of top-level startup.

Exposure before this freeze: AGENTS.md, ERC1 WORK_ORDER.md, CLAUDE.md required
sections and triggered no-shortcuts/completeness-map/verifier-before-record
protocols; central D1/R9/R10/R17, GCA1 REVIEWED_RESULT.md, and ULC1
OWNER_CLARIFICATION.md. Parent supplied the two authorized definitions and broad
review remit. No parent ERC1 derivation, implementation, plan or outcomes read.
TPS1 capture.py was inspected solely as an existing resource/capture utility.
The scientific code here is independently written. A failed read of the guessed
capture_check.py filename was administrative only; the actual capture.py was then
located and read. External comparison checked in De Felice and Tsujikawa,
[f(R) Theories](https://link.springer.com/article/10.12942/lrr-2010-3), equations
2.4, 2.7 and 3.2/3.8. Those known metric-f(R) results are attribution and a sign
cross-check, not native UDT premises. The PMC copy presented a browser challenge;
the publisher text was accessible.

## Analytic argument frozen before computation

Conventions are signature (-+++), Box=grad^a grad_a and curvature convention with
R=6(Hdot+2H^2) on spatially flat FLRW. Smoothness sufficient for the displayed
derivatives is required. One connected regular patch is the local domain.
Both response identifications remain UNADOPTED counterfactuals; DDR contributes
TF(E)=0 only, and ordinary proper clocks evaluate supplied geometry only.

For A, write F=1+2 alpha R. TF(E_A)=F(Ric-Rg/4). Wherever F is nonzero, DDR is
equivalent to Ric=Rg/4; contracted Bianchi gives dR=0. Thus a nonconstant scalar
prefactor does not enlarge this regular solution set or select an Einstein
curvature value. Its off-shell divergence is G_ab grad^a F, generally nonzero.
For alpha nonzero the F=0 interior has R=-1/(2 alpha); E_A then vanishes on any
metric of that constant scalar curvature, not only Einstein metrics. This
degenerate stratum is outside the regular comparison. No classification of
smooth transitions between strata is claimed.

For B, trace(E_B)=-R+6 alpha Box R, and

    TF(E_B)=F(Ric-Rg/4)-2 alpha(Hess R-g Box R/4).

The divergence of 2R Ric-R^2 g/2 is 2 Ric(grad R,.); the scalar-Hessian
commutator cancels it in the derivative term. Hence div E_B=0 identically.
DDR gives E_B=lambda g with constant lambda on the connected patch. Defining
Lambda=-lambda yields E_B+Lambda g=0 and

    6 alpha Box R-R+4 Lambda=0.

For alpha nonzero, scalar perturbations about constant R=4 Lambda have
mass-squared 1/(6 alpha); in Minkowski, omega^2=|k|^2+1/(6 alpha).
Positive alpha removes the scalar tachyon in this linear flat test only.
Negative alpha admits growing long-wavelength scalar solutions. Neither statement
certifies full nonlinear stability, causal well-posedness or a GR recovery filter.
No independent physical scalar is inserted: R remains metric curvature, although
its extra higher-derivative initial data must be supplied and constrained.
F=0 cannot be divided out. At constant R=-1/(2 alpha), every constant-scalar
metric has E_B=g/(8 alpha), including non-Einstein metrics, with
Lambda=-1/(8 alpha). Sign/principal and stability questions there are separate.
For alpha=0, DDR returns the ordinary Einstein-shape branch with an unfixed
connected Lambda. For constant R with F nonzero, B returns that shape too.

Weak static diagnostic: ds^2=-(1+2 epsilon Phi)dt^2+
(1-2 epsilon Psi)(dr^2+r^2 dOmega^2), a compact interval 1<=r<=3 in selected
dimensionless units and epsilon small. Both potentials are retained. Linearized
vacuum E_B=0 is a declared Lambda=0 subcase of DDR. In Cartesian spatial
components R00=Delta Phi, Rij=partial_i partial_j(Psi-Phi)+delta_ij Delta Psi,
R1=2 Delta(2 Psi-Phi), so a sufficient family is

    Phi=U-alpha R1, Psi=U+alpha R1,
    Delta U=0, (Delta-1/(6 alpha))R1=0.

The positive-alpha radial scalar is (c_- exp(-m r)+c_+ exp(m r))/r. On the
finite interval neither coefficient is removed by a silently imposed asymptotic
condition. The check uses the declared decaying member only, U=-1/(10r),
R1=exp(-r)/r, alpha=1/6, not a source-derived amplitude. Negative-alpha radial
members replace the exponentials by sine/cosine. At fixed static clock radii
r_e,r_o, received/emitted infinitesimal proper period ratio is
sqrt[(1+2 epsilon Phi_o)/(1+2 epsilon Phi_e)], with first variation
Phi_o-Phi_e. Coordinate light travel sees Psi+Phi=2U to first order; the pure
scalar pieces cancel there, while endpoint proper-clock factors still change.
The linearized solution is not thereby an exact finite-amplitude solution. Its
smooth compact-domain metric residual is O(epsilon^2) under bounded derivatives;
the exact first-order coefficient is checked below. No mass amplitude, interior,
source law, global extension, empirical fit, or universal preferred center enters.

Evolving diagnostic: ds^2=-dt^2+a(t)^2 dx^2, a>0, H=adot/a, P=Rdot. This
symmetry and chart are pinned-by-HABIT for tractability; alpha and initial data
are free-and-explored. The tensor equations are equivalent on this slice to

    adot=aH, Hdot=R/6-2H^2, Rdot=P,
    Pdot=-3HP-(R-4Lambda)/(6alpha),
    C=3(1+2alpha R)H^2-alpha R^2/2+6alpha HP-Lambda=0.

The original 00 residual is C. The spatial diagonal residual divided by a^2 is
D=F(Hdot+3H^2)-(R+alpha R^2)/2-2alpha(Pdot+2HP)+Lambda.
The trace evolution gives 3D=C and the equations give Cdot=-4HC. Thus satisfying
the evolution equations alone with arbitrary initial data is insufficient; a
constraint defect persists. The check independently derives the metric Ricci
components, the tensor expressions, and this propagation identity. Initial data
for the one short numerical witness are a=1, H=1/10, R=1/10, P=-31/600,
alpha=1, Lambda=0, with C exactly zero. No H division occurs during evolution.

Supplied comoving clocks have proper time t. Let eta(t)=integral dt/a(t).
For coordinate separation L, a regular outgoing arrival satisfies
eta(t_a)-eta(s)=L, and immediate reflection gives eta(t_b)-eta(s)=2L.
Differentiation gives dt_a/ds=a(t_a)/a(s) and dt_b/ds=a(t_b)/a(s).
For finite emission interval delta the received/echo period ratios are the
corresponding differences in t_a/t_b divided by delta, not exactly the endpoint
scale-factor ratios. These clocks are not claimed PSW1 parallel-prepared.

## Frozen numerical controls and evidence ceiling

Run source_first_check.py through the existing TPS1 capture.py: CPU symbolic
SymPy and float64 SciPy, one BLAS thread, 2 GiB virtual memory, no elapsed/CPU
timeout, manual interruption available, no GPU. One evolving case only, t in
[0,2], 101 audit times, solve_ivp Radau at rtol=1e-8/1e-10/1e-12 with
atol=rtol/100. The initial actual workload is the same short single case.
Null calculations use L=0.2, emissions s=0.1 and s+delta=0.12. Independent
quadrature of 1/a and scalar root solving reconstruct the arrival/echo events;
eta is also evolved and compared. Stop before accepting nonfinite values,
a<=0, F<=0, solver failure or absent brackets. Fixed absolute acceptance:
max original tensor residual <=1e-7, two tightest endpoint states/clock intervals
agree within 1e-7, quadrature-versus-eta arrival differences <=1e-8. No asymptotic
rate is inferred from these three tolerances. A deliberately perturbed initial
P is checked algebraically to expose the nonvacuous constraint gate; the false
static equal-potential omission is also checked algebraically.

This file and code are frozen before numerical outcomes and before parent
candidate exposure. Exact symbolic identities support only the displayed
restricted statements; floating agreement supports one supplied finite example,
not physical adoption, source selection, empirical recovery, nonlinear/global
stability, full PDE well-posedness or a complete response classification.
