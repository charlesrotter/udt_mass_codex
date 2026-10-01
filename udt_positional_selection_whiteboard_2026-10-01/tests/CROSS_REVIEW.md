# PSW1 operational-tests cross-review

**VERIFIED-WITH-CAVEATS for the conditional diagnostic, with the limits below.**
No substantive algebraic defect was found in the frozen candidate's 1:3
coefficients, trace statement or premise separation. No physical identification,
response completeness, native field law or adoption is verified by this verdict.

Reviewed `INITIAL_CANDIDATE.md`, SHA-256
`95ed91cca818cd6f1b7de819396f61ad2a24dc741f763334ed52e7bf769ad1b1`.
The candidate, two peer source-first notes, geometry check code and method-reference
file are bound in `CROSS_PRECHECK_FREEZE.json`. Own source-first note remained
unchanged at `d26c04d1bbae469a32835702b75ebea0a25c154a07f84e268b855c37985880c8`.
This is the same inherited model in an actual separate context. The initial
time-dependent control preceded peer-proposal exposure; this cross-review and
the new Kasner check follow exposure to the claimed coefficients. No different
model, blind cross-check, human review or formal proof is claimed.

## 1. General four-dimensional preparation and derivative

I checked the load-bearing argument rather than treating the symmetric controls
as a proof of the general case. Along a radial Fermi line the quadratic
contractions of g0i with n and of gij with n twice vanish by curvature
antisymmetry. The remaining quadratic radial metric term is
`g00=-(1+T(n,n)r^2)`. Parallel preparation may give a transverse initial velocity
of order L^2; radial contraction removes that term at the displayed order.
The receiver's transverse displacement during O(L) time is O(L^3), and null
deflection has the same order. Their first effect on the radial arrival time
is beyond the cubic terms used for the quadratic tick ratio. This is why a
totally geodesic two-surface is unnecessary at this order.

The rescaled variables `t=L v`, `x=L y`, `s=L u` make the small-laboratory
geodesic and incidence problem a smooth perturbation of the flat one, whose
receiver intersections are transverse. On compact direction/template sets in
a fixed smooth normal tube, Taylor remainder control can be taken in u as well
as the solution variables. A fourth-order proper-arrival remainder then has
an s derivative of order L^3. Mere pointwise O(L^4), without this smooth
rescaled/C1 statement, would not justify differentiating it. The candidate
includes that condition; it should remain adjacent to the coefficient in
integration. This gives local metric-dependent constants, not a uniform error
bound across arbitrary geometries or the existing TPS1 survey.

The return uses the relay's later event and its proper label. Explicitly,
`dt_a/dt_b=1-eL^2+O(L^3)` while
`d tau_B/dt_b=1+eL^2/2+O(L^3)`, so their ratio is
`1-3eL^2/2+O(L^3)`. This verifies the 3 factor; setting q=1/p would replace
the actual experiment with inverse-map reciprocity. Re-preparing the receiver
for each pulse would also change the derivative. Both distinctions are
correctly preserved in the candidate.

## 2. Independent controls and the false-independence boundary

Before seeing the static-lapse proposal, my source-first calculation used
`a_i=1+kappa_i t^2` and integrated the exact axial null relation. It gives
`log p=kappa_i L^2+O(L^4)` and
`log(pq)=4 kappa_i L^2+O(L^4)`, hence
`log q=3 kappa_i L^2+O(L^4)`. Its directly reconstructed
`T_ii=-2 kappa_i` agrees with the candidate. This uses a different metric and
actual time-dependent null-arrival formula, not the author's Fermi polynomial.

I inspected `geometry/check_fermi_jet.py`: its static-control arrival polynomial
and endpoint-frequency cross-check cover the outward coefficient. That script
alone does not check the future-return coefficient. The time-dependent result
above does, as does the new Kasner calculation below. Both contexts share
SymPy, standard differential geometry and R6's endpoint-frequency theorem.
That shared theoretical dependency is explicit. The separate contexts and
different metric calculations do not mean different libraries, independent
physical evidence or a separate general-data integrator.

## 3. Executed nonflat Ricci-flat control

With parent CPU-slot authorization I ran one frozen finite symbolic check:

```
python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_positional_selection_whiteboard_2026-10-01/tests/kasner_cross python3 udt_positional_selection_whiteboard_2026-10-01/tests/check_kasner_cross.py
```

`kasner_cross.json` records exit 0, 0.5387233219807968 seconds, 49,848 KiB
maximum child RSS, a 2 GiB address-space cap, no wall/CPU timeout and no signals.
`kasner_cross.stdout` records 35 exact symbolic PASS assertions; stderr is empty.
Some tensor components vanish by symmetry, so the number is bookkeeping rather
than an independence measure. The CPU slot was explicitly released. No field
evolution or ray integration was run.

The supplied Kasner metric is `-dt^2+sum t^(2 h_i) dx_i^2`, with
`h=(-1/3,2/3,2/3)`, on a small regular patch about t=1. Direct Christoffel/Riemann
reconstruction verifies every Ricci component is zero and gives the nonzero
electric tidal diagonal `(-4/9,2/9,2/9)` at t=1. This is a conditional GR
comparison geometry, not a native-admitted UDT countermodel.

For one axis with exponent h, I worked in the original synchronous coordinates,
without substituting the Fermi metric or its arrival polynomial. Parallel
preparation is essential: the spacelike exponential reaches
`t_B0=1-hL^2/2+O(L^4)`, `x_B0=L+h^2 L^3/3+O(L^5)`.
The transported unit clock has spatial conserved geodesic momentum
`C=-hL+O(L^3)`. Thus it is not a comoving coordinate clock when h is nonzero.
Spacelike-geodesic and parallel-transport equations verify those jets directly.

Conserved receiver momentum and axial null incidence give
`t_b=1+L-hL^2/2+O(L^3)` and `t_a=1+2L+O(L^3)`.
Put `a_b=t_b^h`, `a_a=t_a^h`, `w=C/a_b`, `gamma=sqrt(1+w^2)`.
Direct endpoint contractions give

```
p = a_b/(gamma-w)       = 1+h(h-1)L^2/2+O(L^3),
q = (a_a/a_b)(gamma+w)  = 1+3h(h-1)L^2/2+O(L^3).
```

The same expressions follow by implicit differentiation of the outgoing and
return null incidences while the prepared worldline and C remain fixed as
emission time varies. A proper-clock offset at preparation affects neither
derivative. The exact original-coordinate geodesic and null relations supply
this calculation; the desired Fermi coefficient is compared only afterward.

The outgoing quadratic coefficients are `(2/9,-1/9,-1/9)`; the return ones are
`(2/3,-1/3,-1/3)`. Both traces vanish, and the 1:3 ratio holds. This confirms
the preparation, signs and trace in a nonflat Ricci-flat example with nonzero
initial expansion. It remains a special analytic control, not general4D proof,
empirical evidence, a TPS1 point or a native-sign acceptance test.

## 4. Trace is not all-direction coverage

For each fixed unit U the equal-L orthonormal-triad mean has quadratic
coefficient `-Ric(U,U)/6`; this is the spherical mean of that quadratic form.
It is not a spherical average of the full finite-L data. The quadratic form
with matrix `[[0,1,0],[1,0,0],[0,0,0]]` is an adverse control: every coordinate
axis reads zero while two eigen-directions have opposite signs. Thus neither
three zero axial coefficients nor four TPS1 queries show T=0 or exclude a
negative direction. The candidate correctly requires additional quadratic-form
information for the full tensor and distinguishes trace positivity from
negative-definite T. Six directions must have rank six as quadratic-form
sampling functionals; six arbitrary directions are insufficient.

If T is nonzero and trace-free it has both eigenvalue signs. If T=0 the
quadratic diagnostic is silent about higher orders. The Kasner example supplies
an actual geometry for the first case; the isotropic time-dependent controls
show that the optional endpoint-potential criterion permits either sign.
None turns those examples into native UDT admissions or exclusions.

## 5. Numerical discriminant and a precision condition for integration

The actual quantity is a limit or a controlled estimate of a coefficient:
`lim_(L->0) mean(log p)/L^2`. A finite triad mean can be nonzero in Ric=0 from
the O(L^3) remainder. If each numerical log-ratio has absolute error at most
epsilon(L), division by L^2 also contributes at most epsilon(L)/L^2 to the
mean-coefficient error, in addition to the O(L) analytic remainder. Cancellation
across directions does not remove the need for those bounds. Errors in physical
preparation and curvature comparison need their own compatible error estimates.

**Smallest precision repair:** carry this finite-L/error qualification into the
central integration or decision brief. Do not classify one finite sample as a
nonzero Ricci coefficient or launch another vacuum survey to find a coefficient
the equation fixes to zero. A future numerical dispatch would need the frozen
physical preparation, several shrinking L values or a justified remainder
bound, interpolation/arrival/proper-time error estimates, and enough independent
curvature accuracy to resolve the proposed difference. No numerical tolerance
or such campaign is authorized or validated here. This is a use-condition, not
a correction to equations (1)–(2).

## 6. Physical join and decision value

J1 is the remaining physical issue: whether an admitted positional statement
restricts this prepared coefficient, a matched contrast, higher orders or a
different specified comparison. Ordinary tidal gravity already contributes to
the displayed coefficient. Opposite-sign controls therefore do not disprove
the founding positional interpretation, and passing the diagnostic does not
isolate it. A universal positive L^2 monopole remains UNADOPTED. It cannot be
inferred from ordinary local clocks, no preferred observer, reciprocity or the
existence of a scalar readout. Exact distance/motion preparation makes the
comparison noncircular; it does not itself choose a metric.

Nearest prior work remains DCI1/G403's directional clock-curvature relation,
G358's tides, ICN1's proper-time radar maps, SGE1's observer/geometry distinction,
CES1's physical preparation, and NCI1's endpoint-potential criterion. The
specific release-and-return 1:3 preparation is an increment relative to the
inspected sources, not a literature-wide novelty claim or a new gravity law.
The primary-method note names relevant published Fermi/clock-compass methods;
I read that note but did not independently reopen its external papers, so its
literature inspection is attributed to the parent.

The strongest survivor is a conditional, reproducible way to test a particular
physical proposal without equating amplitude with distance or choosing favorable
clocks after viewing the outcome. It narrows the next question. It does not
make another large computation informative before that proposal is stated.

## 7. Additional operational-response comparison requested by parent

After the review calculation, parent proposed stating
`C(U,U)=-6 lim_(L->0) mean(log p)/L^2=Ric(U,U)` for all future unit timelike U,
then comparing an explicitly UNADOPTED response identification
`E_response=a C+b g`, with a nonzero on the region. I inspected FE1's
`udt_field_equation_principle_design_2026-09-13/DECISION_PACKET.md` and central
R9–R10 for this comparison. This is a subsection of Route A, not a third route.

The reconstruction statement is correct at the ideal limit: equality of two
symmetric tensors on every future unit timelike U extends by quadratic
homogeneity to the open timelike cone. A quadratic polynomial vanishing on an
open cone vanishes identically, so C=Ric. One observer gives one contraction,
not all ten components; the all-U mathematical statement does not assert an
actually populated observer ensemble. Arbitrary measured scalar records do not
automatically define a tensor; the proven metric identity owns that structure.

With the stated extra constitutive identification, DDR gives
`0=TF(E_response)=a TF(Ric)`, hence `Ric=(R/4)g`. Contracted Bianchi makes R
constant on a connected regular region: `Ric=Lambda g`. The pure-trace response
term is invisible to DDR. No value/sign of Lambda or absolute scale is selected.
The premise a!=0 must apply where the equation is claimed; at a zero-normalization
sector that implication is not supplied by DDR alone.

**Strongest objection:** measurement identifies a geometric tensor, not the
response that the physical balance governs. As FE1's packet already states,
there are two unsupported choices: why this geometric quantity is that response,
and why it exhausts the relevant response up to pure trace. Clock measurements
also contain directional tidal information discarded by the trace. No principle
here excludes additional trace-free response contributions. The proposed
identification therefore remains UNADOPTED and cannot be sold as constitutive
completeness from operational reconstruction.

**Survivor/smallest repair:** retain it only as an explicitly conditional
comparison: the prepared-clock route offers an operational characterization of
the same Ricci tensor that FE1's unadopted volume-response route selects. Its
DDR consequence is the already known conditional Einstein family. It adds no
new native equation, Lambda selection, empirical prediction or proof of J1.
Credit FE1 and distinguish operational meaning from balance/completeness.

## 8. Review ceiling and omissions

No initial file was overwritten; the original candidates and precheck freezes
remain. No new full406 run, protected payload access, TPS1 raw-field/ray replay,
global/caustic extension, screen observable, empirical calibration, different
model or general-data numerical solver was used. Source selection, branch,
clock conventions, unit roles, opposite-sign retention and the J1 gap were
checked substantively. The final integrated edition still needs the designated
final reviewers and parent repository/premise checks. This cross-review neither
updates source grades nor supplies authority to adopt a physical premise.
