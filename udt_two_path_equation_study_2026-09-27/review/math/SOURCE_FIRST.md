# Source-first mathematical record — quadratic metric response

Status: **UNADOPTED CONDITIONAL MATHEMATICS; source-first freeze before candidate exposure.**
Reviewer: separate `quadratic_review` agent context, same inherited model as parent;
no different-model or human independence claimed. Date: 2026-09-27.

## Authority, exposure, and scope

I independently inspected local branch/status and HEAD:
`grok`, `6553f5e90e5e7a51030fb9f8205528f8420b0b0f`. Unrelated untracked
work was visible in status and preserved; its payload was not opened. Parent
successful fetch/pull and full 406-row premise PASS are attributed, not rerun here.
The parent retains the before-banking premise-audit gate.

Read on disk: AGENTS.md; CLAUDE.md required method/review sections; triggered
no-shortcuts, completeness-map, verifier-before-record skills; WORK_ORDER.md;
current GR-filter authority; G311 audit and exact DDR shape theorem; G201
primary metric audit/scope. An initially broad registry text search displayed
other matching rows; only G311/G312/G201 are used below. No protected package
payload, parent candidate, parent implementation, or parent output was read.
The task disclosed that the parent had preliminary speculative algebra, but
not its equations or conclusions. Discovery was targeted, not outcome-blind.

This is the one chosen counterfactual `sqrt(-g)(R+alpha R^2)`, with the action,
EH term, quadratic term, and identification of its tensor with DDR response
all **CHOSEN / UNADOPTED**. `alpha` is real, free-and-explored, dimension L^2.
Its sign and magnitude are not selected. No independent field, source,
boundary law, X_max use, physical mass, charge, or scale adoption occurs.
Local Metric Sufficiency and current GR FILTER ONLY do not derive this action.
DDR remains the separately owned provisional postulate; the tensor supplied
to it is the extra choice. G311 gives `TF(E)=0`, not `E=0`.

Question: classify **every** smooth solution of that chosen full tensor DDR
equation on the specified primary metric, on a connected open interval
`I subset (0,infinity)` with `f>0`. Staticity, spherical symmetry, areal radius,
and reciprocal radial block are scope restrictions inherited from the work order,
not consequences of the new action or a whole-theory classification. `x0=c_E t`
uses the allowed observed calibration, with no new transfer-speed premise.

Method: exact differential geometry and polynomial identities, no approximation
in the static calculation. CPU-only single small SymPy process, no GPU/grid/data,
120-second wall timeout, modest symbolic expressions, no production solve.
Outputs are confined to this review directory. Maximum claim is conditional
local classification plus a necessary linearized trace diagnostic. Global
completion, horizons/f=0, r=0, sources, asymptotics, physical realization,
generic well-posedness, stability, and empirical discrimination are excluded.

## Primary external formula and variational prescription

Primary derivation consulted: Guarnizo, Castañeda, Tejeiro,
*Boundary Term in Metric f(R) Gravity: Field Equations in the Metric Formalism*,
[arXiv:1002.0617v4](https://arxiv.org/html/1002.0617v4), equations (3.8),
(3.14), and (3.25), accessed 2026-09-27. Its boundary discussion following
(3.23) is not silently replaced by metric Dirichlet data alone. A review-paper
search result was initially seen but is not used as a scientific source.

Use compactly supported metric variations in the open region, so no physical
boundary completion is introduced. With inverse-metric variation,
`delta sqrt(-g)=-sqrt(-g)g_ab delta g^ab/2` and
`delta R=Ric_ab delta g^ab + g_ab box(delta g^ab)
         - nabla_a nabla_b(delta g^ab)`.
Two integrations by parts give, writing `q=R+alpha R^2` and `F=q_R=1+2alpha R`,

`delta S = integral sqrt(-g) E_ab delta g^ab`,

`E_ab = F Ric_ab - (q/2)g_ab + (g_ab box - nabla_a nabla_b)F`.       (1)

The bulk tensor agrees with the cited primary formula; the branch analysis
below is independently derived here. Curvature sign is the convention in
the reference's (2.2): de Sitter has positive scalar curvature in signature
`(-,+,+,+)`.

Crucial distinction: unrestricted stationarity of this action would impose
`E=0`, a different field equation. Here full variation **computes the response**;
DDR then imposes `TF(E)=0`. Equivalently one may describe stationarity only
against arbitrary pointwise trace-free compactly supported variations, but
that variational restriction is itself a chosen prescription. No unrestricted
Euler-Lagrange equation is being relabeled DDR.

Equation (1) is a natural symmetric covariant metric tensor with generally
fourth metric derivatives. It satisfies an off-shell divergence identity.
Indeed the differentiated curvature term leaves `Ric_ab nabla^a F`, since
`nabla^a Ric_ab=(1/2)nabla_b R` and `nabla_b q=F nabla_b R` cancel their
remaining terms. The divergence of `g_ab box F - nabla_a nabla_b F` is
`-Ric_ab nabla^a F`, by the scalar Hessian commutator. Thus `nabla^a E_ab=0`.

Writing `S_ab=Ric_ab-R g_ab/4`, the full DDR equation is

`F S_ab - 2alpha [nabla_a nabla_b R - (box R)g_ab/4] = 0`.          (2)

DDR implies `E_ab=lambda(x)g_ab`; (1)'s divergence then makes lambda one
constant on a connected region. Its trace retains the equation

`-R + 6alpha box R = 4lambda`.                                  (3)

Neither lambda nor R is set to zero. Constancy of lambda uses the chosen
response identity, not DDR alone.

## Complete primary metric equations

For `g=-f(dx0)^2+dr^2/f+r^2(dtheta^2+sin(theta)^2 dphi^2)`, direct
four-dimensional connection reconstruction, including all angular terms, gives

`A := Ric^0_0 = Ric^r_r = -f''/2 - f'/r`,
`B := Ric^theta_theta = Ric^phi_phi = (1-f-r f')/r^2`,
`R = 2A+2B = -f''-4f'/r+2(1-f)/r^2`.                            (4)

For any radial scalar R, the mixed Hessian is diagonal:

`H^0_0=(f'/2)R'`,
`H^r_r=f R''+(f'/2)R'`,
`H^theta_theta=H^phi_phi=(f/r)R'`,
`box R=f R''+(f'+2f/r)R'`.                                     (5)

Each full component of (1) is therefore

`E^0_0 = F A-q/2+2alpha[box R-(f'/2)R']`,
`E^r_r = F A-q/2+2alpha[box R-f R''-(f'/2)R']`,
`E^theta_theta = E^phi_phi = F B-q/2+2alpha[box R-(f/r)R']`.       (6)

All off-diagonal components vanish by this direct reconstruction. Equalizing
the three distinct diagonal entries is equivalent to the full TF equation.
In particular,

`E^0_0-E^r_r=2alpha f R''`,
`E^0_0-E^theta_theta=F(A-B)-2alpha(f'/2-f/r)R'`.                  (7)

Equations (4)-(7), with (3) as their conserved trace consequence, retain the
angular equation; a radial-only equality is insufficient.

## Necessity, degenerate locus, and sufficiency

For `alpha=0`, (2) is `S=0`. Bianchi gives constant `R=b`, and direct
integration gives `f=1+c/r-b r^2/12`. All such profiles solve the full
equation on any connected positive-f interval; `lambda=-b/4`.

For `alpha!=0`, positivity of f makes the first equation in (7) imply `R''=0`
throughout I, **without dividing by F**. Hence `R=a r+b`. Integrating (4)
without guessing a target profile gives the full general solution of this
linear curvature equation:

`f=1-b r^2/12-a r^3/20+c/r+d/r^2`.                             (8)

The two homogeneous modes are r^-1 and r^-2; this follows from the Euler
operator `f''+4f'/r+2f/r^2`, not from a finite search. For (8), (3) becomes

`-a r-b+6alpha a(2/r-b r/3-a r^2/4+c/r^2)=4lambda`.              (9)

Multiplication by r^2 is valid on I. The r^4 coefficient in the resulting
polynomial identity is `-3alpha a^2/2`. A polynomial vanishing on an open
interval has every coefficient zero; since alpha is nonzero, `a=0`.
This proves constant scalar curvature in this slice, including possible
zero or changing-sign F loci. No finite sample or analyticity assumption
for the original smooth f is needed.

Then `F=1+2alpha b` is a connected constant and (2) reduces to `F S=0`.
For constant-R (8),

`S^a_b = (d/r^4) diag(-1,-1,1,1)`.                             (10)

Consequently the complete classification is:

1. **Generic branch:** `1+2alpha b != 0`, `d=0`,
   `f=1+c/r-b r^2/12`, `R=b`, `E=-(b/4)g`.
2. **Degenerate branch:** `alpha!=0`, `b=-1/(2alpha)`, arbitrary c,d,
   `f=1+c/r+d/r^2+r^2/(24alpha)`, `R=-1/(2alpha)`,
   `E=g/(8alpha)`. The d=0 subset is also Einstein; d!=0 is non-Einstein.

All constants are real mathematical integration data, restricted only by
existence of the declared positive-f interval. The coefficient c is not
identified with physical mass and d is not identified with charge or a
source. The degenerate branch is nonempty: alpha=1,c=0,d=1 makes f>0 for
all r>0, although no regular-center or global-completeness claim follows.
No positivity of F, Einstein-frame transform, or division by F was assumed.
If a later physical viability gate required F>0, that would be a further
declared gate, not a reason to delete this mathematical solution now.

Sufficiency is direct substitution in every component (6), saved as exact
checks. Necessity uses full component equality, the divergence identity,
the general integral (8), and an interval polynomial identity. These provide
an actual bounded classification argument, not checklist-based completeness.
The critical branch is not a zero-response branch: E is nonzero at finite
nonzero alpha. More generally every metric with that constant critical R
satisfies TF(E)=0, but only the explicitly derived primary subset is classified.

## Limit and optional trace diagnostic

At fixed smooth metric jets, `alpha -> 0` gives `E -> G` and `TF(E) -> S`.
The generic primary branch is the same Einstein profile family for every
noncritical alpha, without selecting b,c. The critical branch has
`R=-1/(2alpha)` and therefore no bounded-curvature alpha->0 limit.
This is a singular branch limit, not a contradiction of the operator limit.

For alpha!=0, linearize (3) about any fixed background solution with constant
R0 and fixed connected lambda0=-R0/4. Since `delta(box)R0=0`,

`(box_background-1/(6alpha)) delta R = 0`                       (11)

for variations within the same lambda sector. If the sector varies,
`(6alpha box_background-1)delta R=4 delta lambda`, where delta lambda is
connected constant. This is a necessary first variation of the trace only;
delta R must still arise from metric perturbations satisfying the remaining
linearized tensor equations. It does not certify arbitrary scalar data,
global stability, causality, or well-posedness. The coefficient `1/(6alpha)`
is a chosen-model scalar mass-squared parameter in this operator: its sign
changes with alpha, but a positive sign alone is not a stability certificate.
No independent scalar has been supplied as a physical premise, yet the fourth
derivative metric content is real and must not be hidden. The static reciprocal
classification does not remove this content in wider geometries.

## Verification, independence, and limits

`independent_static_check.py` imports only Python libraries/SymPy, no existing
UDT or parent code/artifacts. It constructs the four-dimensional Christoffels,
Ricci tensor, scalar Hessian, response, and all four mixed divergences directly.
Run command: `timeout 120s python3
udt_two_path_equation_study_2026-09-27/review/math/independent_static_check.py`.
Actual Python 3.10.12 / SymPy 1.13.1 run completed with exit 0, **49 exact
symbolic zero checks**, plus three nonzero refuting controls. Stdout, stderr,
and machine-readable CHECK_RESULT.json are saved. The controls expose deletion
of the non-Einstein critical branch, replacement of DDR by E=0, and omission
of the angular equation. They are concrete algebraic counterexamples, not an
independent physical validation or a general mutation-testing certification.

The hand proof above was worked out before implementing these checks. Thus
there is a separate-context source-first argument and an independent tensor
implementation relative to parent code; shared standard mathematics and SymPy
are disclosed. This is same-model, not different-model independence. Source
theorems' original reviews were not replayed. No empirical/GPU/global numerical
tests, full PDE degree-of-freedom count, boundary action completion, or dynamical
stability proof was attempted. Fresh candidate review occurs after this freeze.

**Source-first landing:** the chosen action gives a coherent conditional DDR
response equation with a conserved trace datum. On the entire declared primary
slice it forces constant scalar curvature and is Einstein generically, while
its critical response factor admits the additional d/r^2 family. Thus it supplies
no generic new primary profile in this slice; it does supply a distinct,
degenerate mathematical stratum. None of this establishes native emergence,
physical viability, response ownership, a source law, or adoption.
