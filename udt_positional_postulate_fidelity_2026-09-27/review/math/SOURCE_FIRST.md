# Source-first mathematics and GR comparison

Status: source-first assessment frozen before exposure to this investigation's
candidate. No scientific promotion or native equation is asserted. Baseline:
`grok` `97af29a72322fa686dd0158a33947a91ac27d678`. Assigned scope: F1-F4/W4-W6,
complete metric versus completed pair/scalar, and external static spherical GR
diagnostic. Source versions/scopes are in `SOURCE_PINS.json`; check plan and exact
outputs are retained beside this file.

## Finding

The reciprocal construction represents a definite part of the founding positional
dilation postulate: in its declared primary chart, a clock calibration factor and
a radial ruler factor are inverse, the factors compose exponentially in additive
depth, and the complete metric supplies clock, length, angular and causal geometry.
This is more than a scalar renaming. It is not a complete mathematical translation
of every possible meaning of "observed c arises from positional dilation."

The accepted owner postulate does not need a derivation of its own physical why.
The remaining fidelity question is whether an intended measurable implication is
absent from the representation, or whether the intended interpretation is already
fully represented by the clock/ruler metric. No universal distance law, signal
mechanism, rate/duration inversion, or equation for the valued geometry can be
silently inserted to answer that question. Numerical derivation of c_E is also
not required by this work order; c_E remains its observed calibration.

## F1-F4: each mathematical step performs visible work

F1 supplies the two conversion directions L=c_E T and T=L/c_E and their physical
interpretation. The bare invertible conversion alone does not imply reciprocal
positional transformations. F2 adds preservation of K=[[0,1],[1,0]] by a positive
diagonal P=diag(u,v). Direct multiplication gives P^T K P=uv K, hence uv=1.
Ordinary commuting covariance of the conversion would instead give u=v. This is
an alternative interpretation/control, not evidence against the owner postulate.

F3 adds continuity/measurability, positivity and composition on an additive depth
coordinate. log(u) is additive, so regularity gives log(u)=a Delta. Nontriviality
and a sign/unit convention give diag(exp(-delta),exp(delta)). The group coordinate
is not automatically areal radius, proper/radar distance, or elapsed physical time.
F4 adds a local Lorentzian quadratic readout and the static spherical areal sector.
Together these yield

    ds²=-f(r)c_E²dt²+dr²/f(r)+r²dOmega², f=exp(-2phi)>0.

The positive diagonal comparison, local quadratic signature, spherical areal
sector, and static reduction must remain visible. The source derivation is valid
with them; it is not a theorem that c_E alone forces this four-dimensional ansatz.
The foundational 2026-07-15 source itself makes these dependencies explicit.

F2 preserves its conversion pairing K, not the fixed Lorentz matrix eta in those
same clock/ruler channels: D^T eta D=diag(-exp(-2delta),exp(2delta)). FSR1 already
records the exact change of basis to a Lorentz-boost representation and why it
does not identify a metric deformation with transported unit-frame comparison.
This distinction is recovered source content, not new discovery.

## Three different levels must survive compression

1. The primary four-metric contains a restricted clock/radial block and the areal
   sphere. Its curvature depends on f and its derivatives. The angular sector
   cannot be reconstructed from one terminal clock scalar alone.
2. A supplied germ J pulls back the complete metric: h=J^T g J. All angular,
   screen, shift and mixing terms enter before W1's reciprocal completion.
3. The terminal Phi=-log(T/T_star), followed by chi=tanh(Phi) in the matched
   source typing, is a scalar readout. It is not the full completed relation,
   a metric field, a dynamical response operator, or an event/path assignment.

For h=-T²(dy0+beta d_sigma)²+L²d_sigma², W1 fixes the positive density m=TL.
In the coframe (dy0,m d_sigma), det(h_n)=-1 and the completed radial factor is
1/T. But the full record includes m and shift. If J_m=diag(1,m), then
h=J_m^T h_n J_m. This exact reconstruction, established by G213, is lost if m
is discarded. Complete marked rank-sufficient networks can reconstruct supplied
metrics; one scalar generally cannot. The mathematical ability to normalize a
regular pair is broader than the physical admission of that pair as a UDT query.

W1's spatial element need not be a coordinate differential: m d_sigma can be
anholonomic. The current `founding.md` correction controls regional use over
G176's older coordinate shorthand. Exactness cannot be inferred from positivity.

W4 provisionally supplies a single local metric for clocks, rulers, free fall and
null propagation with calibrated local c_E. It does not choose that metric's field
equation or identify finite-pair c_eff as a second local speed. W5 gives physical
meaning to the screen-retaining projective relation on supplied completed data;
its vector does not replace full path/frame carry and is not a dimensional distance.
W6 separates nonpropagating relational membership from controllable metric-causal
response; it supplies neither a response operator nor a realized global network.
These are actual working postulates with their source scope, not optional omissions.

## Primary reciprocity is not merely W1 normalization

Use the broader diagnostic family, without admitting it as native UDT,

    ds²=-A(r)c_E²dt²+B(r)dr²+r²dOmega²,

on a connected regular interval r>0 with A,B positive and C². Set x0=c_E t.
Direct Christoffel-to-Ricci calculation in the retained code gives

    G^t_t=(1/B-1)/r²-B'/(r B²),
    G^r_r=(1/B-1)/r²+A'/(r A B),
    G^r_r-G^t_t=(A'/A+B'/B)/(r B)=(AB)'/(r A B²).

Thus equal mixed time/radial Einstein entries are equivalent to AB=constant on
that connected interval. The primary reciprocal choice AB=1 is an actual
restriction of this fixed-areal-radius family. If AB is a positive constant,
a specified constant rescaling of static time can put it at one; this is a
normalization freedom, not permission to alter a fixed operational calibration.
For nonconstant AB, reparameterizing radius to normalize the two-metric changes
the angular term to r(s)²dOmega². It does not yield the primary form with s as
areal radius. The statement is tied to the static spherical structure and a
normalized static clock/Killing direction, not a universal coordinate component
condition on arbitrary metrics.

At the same time every regular radial pullback diag(-A,B) can be W1-normalized
using m=sqrt(AB), producing diag(-A,1/A) in the completed coframe. The original
AB information remains in m and the angular-radius relation. For a dimensionless
radial coordinate measured in a freely chosen reference length, the exact control
A=1+r², B=1 has positive AB and G^r_r-G^t_t=2/(1+r²), while its pair still
normalizes exactly. This control separates the two operations; it is neither
a new physical geometry nor an all-postulates countermodel.

This answers a possible overstatement in either direction. "Reciprocity is only
normalization and adds no geometric content" is too strong for the primary
areal chart. "Pair normalization forces every ambient metric into the primary
ansatz" is also false. A stronger equation/value restriction has not followed.

## Exact full-metric external GR diagnostic

For A=f, B=1/f the independently reconstructed tensor is

    G^t_t=G^r_r=E0/r²,    G^theta_theta=G^az_az=E1/r²,
    E0=rf'+f-1,           E1=rf'+r²f''/2,
    r E0'=2 E1.

The source angular amplitudes satisfy

    A_parallel=(r²f''-rf')/2,
    A_perp=1-f+rf'/2,
    A_parallel+A_perp=E1-E0,
    A_parallel=r A_perp'.

These identities hold for every smooth positive f in this arena. Imposing the
external vacuum equation G=0 further selects f=1+C/r. Imposing only angular
trace balance leaves f=1+a r²+b/r, with G=3a I. The latter is the already known
G260 result, and the neighboring angular identity is already PJC1. They are
not new field equations. Isolating the two-dimensional clock/radial metric gives
identically zero Einstein tensor; that is a vacuous substitute for the full
comparison. The sphere's contribution is essential.

If, additionally and only for an external GR interpretation, one imposed
G_ab+Lambda g_ab=kappa T_ab with constant nonzero kappa, the primary AB=1
restriction would require T^r_r=T^t_t. For a diagonal static stress with
T^t_t=-energy_density and T^r_r=p_r, this reads p_r=-energy_density. This
restricts possible GR source interpretations of the ansatz; it neither derives
matter nor says ordinary UDT matter has that equation of state. Computing a
tensor from a supplied f and naming it an effective T is bookkeeping, not a
constitutive source law or native UDT derivation. No such source was selected.

## What "adding positional dilation to GR" could mean

GR's metric already gives position-dependent clock rates. For static observers
in the diagnostic chart, d_tau=sqrt(A)dt and d_ell=sqrt(B)dr. Radial null curves
obey |dr/dt|=c_E sqrt(A/B), while the local ratio |d_ell/d_tau|=c_E. On the
primary reciprocal branch these become d_tau=sqrt(f)dt and |dr/dt|=c_E f.
The lapse, its square and a finite-pair ratio must not be conflated. The local
ratio uses both clock and ruler calibration, not a clock factor by itself.

For static endpoint clocks and a conserved Killing-frequency signal comparison,
nu_received/nu_emitted=sqrt(A_emitted/A_received). This is a metric-plus-query
calculation; it does not require reintroducing a separate dilation factor in the
Einstein tensor. Extra factors that merely repeat this lapse would count the
same metric effect again or change W4's clock coupling. Carroll's original
lecture notes distinguish metric clock/redshift effects from field equations;
see the primary references below. This comparison does not adjudicate the
founding postulate's physical origin or adopt GR dynamics.

A mathematically substantive modification would need an explicit new restriction
on the valued complete metric/response, with its quantified domain and units.
For example, a schematic change of field law would require specifying an actual
covariant symmetric tensor functional, its derivative/order and regularity scope,
its consistency/conservation identities, its data, and the comparison regime.
No tensor functional is chosen here. In an equation written schematically as
G+C=kappa T with fixed couplings, the geometric Bianchi identity demands the
corresponding divergence balance; writing an unidentified C does not satisfy
or explain it. An altered physical clock law is a separate possible change and
would require explicit authority to change W4. An ontological interpretation
of the existing metric relation need not modify the equations at all.

The precise prerequisite for a useful next investigation is therefore to name
which operational or geometric condition is required by the owner's positional
postulate beyond the encoded inverse factors and single-metric readout, and
show its type before choosing a field equation. This is a fidelity specification,
not another undirected local-versus-finite search. If no extra implication is
intended, the remaining unknown equation is not evidence that the postulate was
poorly encoded. If an extra implication is intended, it must first be made
testable against the representation. Its independent authority/derivation must
then be preserved; a conditional label alone does not authorize a fitted tensor.

## Current G312 and previous-stop boundary

Current G312 authority is GR FILTER ONLY. The historical stronger principal-
response overlap does not regain current authority through this comparison.
Local Metric Sufficiency and Universal Reciprocity/DDR remain owner-provisional.
DDR gives TF(E)=0 for the specified all-pair symmetric response but does not
identify E[g]. Within the full G301 class E=a Ric+b Rg, a nonzero a gives
TF(E)=a(Ric-Rg/4), hence conditional Einstein-space mathematics. The current
independent class-membership join is unclosed. The generic A,B curvature identity
above does not close it, select a response class, or turn Einstein into native E.

FSR1 already separates full finite frame arrows, endpoint scalar cycles and
event-moving neighborhood isometries. PJC1 already separates angular-output
compatibility from a restriction on f. Those arguments must not be recycled as
new discoveries or broadened into a no-go against all possible native closure.
This report recovers them only to prevent that regression.

## Evidence and limitations

The exact script passed 20 checks in 1.086 seconds, Python 3.10.12 / SymPy 1.13.1.
It constructs Christoffels and Ricci from the metric matrix, then checks every
mixed Einstein component, rather than merely substituting the source residual
formulas into themselves. Matrix normalization/reconstruction is checked directly.
All source-derived target formulas were exposed before implementation; this is
independent implementation with source-first reconstruction, not a blind proof.
The logical implications in the report require their displayed hypotheses in
addition to symbolic agreement. The deliberately missing-sphere calculation is
a retained corruption control; it returns residual one on the vacuum family.

No full source-package test suites, external historic reviews, global existence,
time-live/nonspherical extension, physical signal attachment, or empirical data
were independently re-audited. The parent startup and earlier 406-row PASS are
attributed only. Local HEAD/status were independently read; no protected payload
was opened and no git mutation was performed. The target packet is the only
write scope, restricted further to this review/math directory.

Independence: fresh separate context; inherited model, exact variant unavailable
and different-model axis UNTESTED; no scientific implementation reused; prior
source arguments exposed; no current candidate exposed at this freeze. Parent's
additional A,B / mixed-Einstein-difference question was exposed and is recorded
in CHECK_PLAN.md. No human specialist review is represented as complete.

Primary external references consulted 2026-09-27: Sean Carroll, *Lecture Notes on
General Relativity*, 1997, hosted by Caltech/NED:

- [Chapter 4, Gravitation](https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll4.html),
  especially gravitational redshift, the geometric conservation identity, and
  the distinction between assigning an effective stress and restricting sources.
- [Chapter 7, Schwarzschild solution](https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll7.html),
  especially static clock/redshift discussion, equations 7.58-7.61. The diagnostic
  curvature formulas above were independently reconstructed, not imported from
  a secondary summary. Attempts to retrieve Tong chapters 4 and 6 failed and
  supply no evidence here.

Return: source-first stage complete; await separately pinned current candidate
for direct adversarial review. This is not a candidate-review verdict.
