# PSC1 source-first mathematical challenge

**VERIFIED-WITH-CAVEATS as conditional mathematics.** Proposal S's stated weak
near-flat response scale does not select the full R² equation even inside the
restricted metric-f(R) class. The permitted cubic completion supplies a full-
tensor local counterexample to that selection inference. A stronger constant-
background-pole requirement can select a quadratic f on an interval under
additional hypotheses. Proposal H supplies f once its entropy function is
specified; it does not independently choose that function.

This is a fixed review artifact, not the maintained scientific development or
physical adoption. SOURCE_FIRST_PLAN and SOURCE_PINS own the question freeze,
source versions and exposure. Separate-context `/root/psc_math`, same inherited
model and shared libraries; exact model/runtime identifier unavailable. No new
parent or peer proof/code/results were read before this report/seal. Parent's
stronger-pole question arrived before check code and is explicitly recorded.

## 1. The weak response scale fixes a linear jet, not a nonlinear completion

Use the unadopted response and convention of the work order,

    E_f = F Ric - f g/2 + (g Box - Hess)F, F=f'(R),
    E_f + Lambda g = 0,
    f(R)=R+alpha R²+beta R³.

In Lorentz4, tr(E_f) = FR-2f+3 Box F. Around Minkowski, Lambda=0,
g=eta+epsilon h, and R=epsilon R1+O(epsilon²), the original tensor variation is

    E1 = G1 + 2alpha(eta Box - partial partial)R1,
    (Box - m²)R1=0, m²=1/(6alpha).

The beta term drops out of every tensor component at this order. The scalar
trace is necessary, but a generic metric satisfying that scalar equation need
not solve E1=0. Sufficiency for an actual scalar metric mode is demonstrated by
h=-2alpha R1 eta. Its computed curvature is6alpha Box R1=R1 on that equation,
and its G1 cancels the derivative term component by component. Subtracting this
scalar metric from any linear solution leaves the usual linear Einstein vacuum
equation; its propagating tensor plane-wave sector is massless. This local linear
decomposition is not a nonlinear stability or unrestricted PDE theorem.

For alpha>0, the scalar dispersion in calibrated c_E=1 coordinates is
omega²=|k|²+1/(6alpha); a spatially homogeneous mode oscillates with angular
frequency1/sqrt(6alpha). In a static exterior the scalar admits both
exp(-r/sqrt(6alpha))/r and exp(+r/sqrt(6alpha))/r branches. Choosing the decaying
branch is supplied boundary information. The existing ERC1 two-potential metric
Psi=-mu/r-alpha R1, Phi=-mu/r+alpha R1 solves every original static linear
component for every beta; the independently checked radial and transverse
components both cancel. The domain is a fixed regular compact exterior annulus,
not a source model or infinity assertion. In ordinary time units, a matched
temporal angular frequency and length obey omega0*ell=c_E. alpha<0 instead has
the known growing homogeneous linear scalar mode and no analogous real Yukawa
decay length; alpha=0 has no nondegenerate flat scalar pole in this formula.

Thus a independently observed weak spatial/temporal scale could motivate and
calibrate alpha within this comparison, subject to the specified metric/clock
reconstruction and filters. It does not constrain beta. Nor does it identify
response normalization, pure trace, an action, source coupling or a native UDT
law. A universal equation can already have circumstance-dependent behavior;
the owner's universal-law meaning does not require this particular response
scale or a background-independent pole.

## 2. Full homogeneous equations and the quartic/quintic clock discriminator

For g=-dt²+a(t)² delta_ij dx^i dx^j, define H=adot/a,
R=6(Hdot+2H²), P=Rdot and S=f''=2alpha+6beta R. The original00 and spatial
residuals (spatial divided by a²) are

    C = 3F H² -(FR-f)/2 +3H Fdot -Lambda,
    D = F(Hdot+3H²)-f/2-Fddot-2H Fdot+Lambda.

These expressions were reconstructed directly from Christoffel/Ricci/Hessian
tensors, not inferred from the scalar trace. The trace and curvature definition
give the smooth local system, where S!=0,

    Hdot=R/6-2H², Rdot=P, adot=aH,
    Pdot=(-R+beta R³+4Lambda-18beta P²)/(6alpha+18beta R)-3HP.

The original tensor identity is Cdot=-3H(C+D). On this trace system, -C+3D=0
and Cdot=-4HC. Therefore C initially zero remains zero, and D=0 as well.
This proves local full-tensor solutions through initially vanishing H without
dividing by H or F. It does not assert trace sufficiency for arbitrary metrics.

Supply a0=1,H0=R0=Lambda=0,P0!=0 with alpha!=0. Both R² and the completion
have C0=0 and full Riemann curvature zero initially; their common metric jet
through order3 is the same. Since S0=2alpha, analytic local ODE existence gives
a>0 and S!=0 on a sufficiently small neighborhood. Differentiating yields

    a(t)=1+(P0/36)t³-[beta P0²/(48alpha)]t⁴
         +[-P0/(4320alpha)+3beta² P0³/(80alpha²)]t⁵+O(t⁶).

In particular Pdot0=-3beta P0²/alpha, and
Pddot0=-P0/(6alpha)+27beta²P0³/alpha². The beta effect is not postponed to
sixth order: the Hessian of R² already contributes at the initially flat event.

Use the RCD1 protocol: supplied comoving proper clocks, first emission0, a0=1,
independently calibrated initial proper separation L, and regular first arrival
L=integral_0^t du/a(u). The differential received/emitted proper-period ratio is
p(L)=a(t(L)). Because t(L)=L+O(L⁴), the first three nonzero coefficients of
log p equal those of a(t):

    log p=b3 L³+b4 L⁴+b5 L⁵+O(L⁶),
    b3=P0/36,
    b4=-beta P0²/(48alpha),
    b5=-P0/(4320alpha)+3beta² P0³/(80alpha²).

Equivalently, for b3!=0,

    b4=-27(beta/alpha)b3²,
    b5=-b3/(120alpha)+(12/5)b4²/b3.

R² predicts b4=0 and the RCD1 fifth-order relation. A nonzero beta at the same
informative initial preparation predicts b4!=0; the full local metric solutions
therefore differ despite their identical weak linear scale. If this polynomial
class and preparation were independently justified, the corrected relations
would recover alpha=-b3/[120(b5-(12/5)b4²/b3)] and beta=-alpha b4/(27b3²).
Those are conditional identifiability formulas, not an observational fit or
confirmation. Independent preparation/calibration and higher-order residual
checks remain necessary; no noise model or achievable precision is supplied.
P0=0 is an uninformative flat preparation and is excluded from these divisions.

Echoes satisfy log q=log p(2L)-log p(L), so their cubic, quartic and quintic
coefficients acquire factors7,15,31. These are kinematic in this protocol.
Echoes calculated from p cannot independently confirm the equation.

An independent stdlib-Fraction calculation solves the original spatial metric
equation for a(t), without using the trace ODE, for alpha=2,beta=1/3,P0=3/5.
It independently integrates1/a, reverts arrival time, and obtains

    (b3,b4,b5)=(1/60,-1/800,7/45000).

It recovers alpha=2,beta=1/3 from the corrected law. Incorrectly applying the R²
only ratio would give alpha=-25/28. This supplied exact example illustrates the
completion sensitivity, not physical calibration. Its first10 supported00 and
first9 supported spatial coefficients vanish exactly. Removing the quartic
term gives original D0=-18/25; retaining it while using the R²-only quintic gives
D1=81/125. These nonzero controls ensure those errors are detected.

## 3. Stronger Proposal S: a constant pole across curvature backgrounds

This is an additional physical hypothesis, not a consequence of weak near-flat
agreement. Consider an open interval I of constant-curvature Einstein backgrounds
R=r, with smooth f and F(r)!=0,f''(r)!=0 on the intended regular branch. The
background equation is rF(r)-2f(r)+4Lambda=0. The scalar curvature variation obeys

    [Box-m²(r)]delta R=0,
    m²(r)=[F(r)-r f''(r)]/[3f''(r)].

This is a covariant scalar-pole coefficient, not a globally defined temporal
Fourier frequency on every curved spacetime. It is represented in the full
linearized tensor equation: for a scalar satisfying the displayed equation,
h=-(f''(r)/F(r))delta R g has its computed delta R equal to the supplied scalar,
and the complete original tensor variation vanishes. The f'' and F exclusions
state the nondegenerate branch, not a classification of their zeros.

Requiring the SAME positive m0² for all r in I gives

    F=(r+3m0²)F',
    F=A(r+3m0²),
    f=(A/2)r²+3A m0² r+B.

On a connected regular interval this elementary first-order ODE proves the
restricted selection. If0 belongs to I and one normalizes F(0)=1 and f(0)=0,
then f=R+R²/(6m0²). F normalization and the additive constant are separate
choices; entropy/clock reconstruction does not silently supply them. More
generally the quadratic form holds on I only; smooth extensions outside I are
not fixed. The point r=-3m0² would have F=0 and lies outside the stated regular
spin-two branch. Nothing here classifies general curvature invariants or
non-f(R) equations, or selects unique response representatives under RCD1.

There is an essential quantifier cost. If one FIXES Lambda and demands that an
open interval of r be vacuum solutions of that single equation, differentiating
rF-2f+4Lambda=0 gives r f''-F=0 and hence m²=0. An open family with a positive
constant pole is therefore impossible with fixed Lambda and the stated
nondegeneracy. R² at fixed Lambda itself has only R=4Lambda. Under conditional
DDR the integration constant may instead vary between solution sectors; each
constant-curvature background can then have its own Lambda(r). The proposed
all-background principle would compare those sectors explicitly. Introducing
source-supported backgrounds is a different question and is not done here.

The polynomial control has m²(r)=[1-3beta r²]/[6alpha+18beta r], generally
background-dependent. An ideal comparison across independently known constant-
curvature preparations could discriminate this strengthened proposal, but this
work does not establish physical access to varying integration sectors or an
independent UDT reason for imposing the same pole. The stronger condition is a
defensible explicit premise for discussion within its class, not an observed
fact, native consequence or adoption recommendation.

## 4. Proposal H: the algebra reveals the entropy choice

The literature assumptions are substantive: local horizons for all null
directions, a heat-flux identification, quantum temperature, an entropy law and
conserved source flux; curvature-dependent entropy adds a non-equilibrium
production term. Eling–Guedens–Jacobson's equations10,19,21 show why merely
reusing equilibrium area balance does not yield the varying-density equation.
Their entropy function is prescribed, not selected by the construction.
Primary sources inspected: [Jacobson v2](https://arxiv.org/abs/gr-qc/9504004v2)
and [Eling–Guedens–Jacobson v1](https://arxiv.org/html/gr-qc/0602001v1).

Independently of accepting that physical construction, its relevant tensor
algebra is short. For an algebraic density F(R), suppose a conditional horizon
relation gives F Ric-Hess F+Psi g with a divergence-free right side. Contracted
Bianchi and the Hessian commutator give

    div(F Ric-Hess F)= (F/2)dR-d(Box F).

Writing f'=F integrates conservation to Psi=Box F-f/2+C, giving E_f+Cg. Thus
an exact F=1+2alpha R yields f=R+alpha R²+B; a density
F=1+2alpha R+3beta R² yields the allowed completion instead. A constant density
yields the Einstein response with its constants. Specifying only the weak
entropy slope leaves higher nonlinear coefficients free, just as in Proposal S.

The additive f constant/integration constant and multiplicative entropy/source
normalization remain distinct. Deriving the functional shape of F from an
independent physical source would be new evidence; writing the target F into
the entropy premise does not do that. This algebra neither identifies UDT heat
or matter nor adopts a microscopic entropy or a new source coupling.

## 5. Checks, failure history and remaining review

The new symbolic implementation reconstructs full homogeneous metric tensors,
checks the local constraint implication,16 flat linear components, independent
static radial/transverse components, the curved scalar realization, and the
clock jet. Its56 exact-zero checks are overlapping diagnostics, not56 scientific
results. The initial Fourier-shell substitution did not reduce odd powers of
k0; it failed at component01 with a residual proportional to the shell equation.
The initial source/stdout/stderr/receipt are preserved. Polynomial remainder
reduction repaired this checking error; no equation, jet, hypothesis or tolerance
changed. The repaired run passed in0.580s at50,552KiB maxrss.

The independent stdlib-Fraction run passed in0.098s at11,328KiB maxrss. It imports
neither symbolic code nor saved output, derives the metric from the original
spatial equation, checks original00, and independently builds the null-clock
series. Finite exact series checks support the analytic local argument; they
are not numerical convergence, empirical evidence or a global remainder bound.
The reference to shared SymPy libraries concerns the first implementation;
the second check supplies a separate arithmetic library/implementation axis.
Different-model, human, formal and full PDE review are UNTESTED.

I have not replayed ERC1's old numerical histories, audited physical experiments,
re-proved all source theorems, classified degenerate f''/F strata, or inspected
protected work. No parent candidate or central integration is yet reviewed.
Those actual-exposure reviews remain required before the final checkpoint is
called reviewed. The strongest survivor is an informative conditional
discriminator plus explicit premise costs; no complete-UDT insufficiency,
required-new-postulate or native selection conclusion follows.
