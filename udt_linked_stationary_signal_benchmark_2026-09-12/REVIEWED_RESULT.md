# LSB1 — linked stationary signal readouts

**REVIEWED CONDITIONAL, VERIFIED-WITH-CAVEATS, UNPROMOTED.**
The ENTIRE INITIAL_CANDIDATE.md equations (1)–(12), its hypotheses and
CANDIDATE_CLARIFICATIONS.md control this result. The initial candidate is
preserved; its UNREVIEWED header is historical under this review overlay.
review/ADVERSARIAL_REVIEW.md and the final fidelity seal own review scope and omissions.
This is a mathematical benchmark, not observed evidence or physical adoption.

## Result and reusable contract

For the supplied complete stationary spherical family

    ds²=L²[-f dT²+f^-1 dr²+r²dOmega²], f=1+a r²+b/r,

on a bounded regular positive-radius window with positive lapse margin, two
proper-clock slope ratios at three known distinct radii determine BOTH a and b.
This is exact at every consistent positive family member: the determinant in
initial equation (4) is strictly positive for ordered radii. One clock ratio
alone leaves a coefficient freedom locally on the fixed positive compact window.
Scale L, areal radii, family form, observer support and protocol remain supplied.

The same coefficients then specify another clock ratio, a finite-endpoint local
sky angle and a single-clock round-trip time. The signal branch is a regular
one-periapse null geodesic, with explicit simple-turn/no-barrier conditions and
a supplied branch choice. Round-trip timing includes an ideal instantaneous
direction-reversing relay. No remote clock synchronization is smuggled into a
one-way duration. Known layout, scale and relay response may not be fitted from
the purported unused timing/angle targets.

Thus the benchmark can test the joint metric/protocol/calibration contract
without a separate coefficient fit for each output. “Unused” means unused for
calibration, not statistical independence. Real applications must propagate
shared covariance and apparatus errors; this virtual benchmark supplies none.

## A concrete information distinction

At fixed turning radius and finite endpoints, the coordinate orbit is exactly
independent of a. Its equation in u=1/r is

    u''+u=-(3b/2)u².

For the same selected endpoint branch, a remains visible in the observer's sky:

    sin²(psi_B)=(a+V_B)/(a+V_p), V_r=1/r²+b/r³,
    partial_a sin²(psi_B)=(V_p-V_B)/(a+V_p)²>0.

Strict positivity follows from the nonturning endpoint branch condition. Holding
the impact ratio instead of the turning point is a different comparison. This
is not an arbitrary-metric degeneracy or a general rejection of linearization.
It is an exact reason to retain local clock/angle/timing readouts alongside the
coordinate ray. The complete metric, both coefficients and finite endpoints
were used throughout; no weak-field or frozen-profile replacement was needed.

The b=0 controls illustrate the distinction particularly plainly. All three
coordinate paths have turning radius 3.68944124604339, within numerical precision,
for r_A=6, r_B=8 and angular separation2. Yet the local angles and round trips differ:

| Supplied a | Receiver angle, radians | Round-trip time, in L/c_E |
|---|---:|---:|
| -0.002 | 0.451859204 | 23.766015886 |
| 0 | 0.479324782 | 23.660101125 |
| +0.002 | 0.504389512 | 23.585190473 |

These are chosen diagnostic geometries with synthetic ideal clock calibration,
not measured physical systems. The complete nine-case table is BENCHMARK_TABLE.tsv.
The flat reference uses the same areal layout and scale, not identical proper
spatial distances. Timing contrasts can have either sign; no general positive
delay theorem is claimed.

## Kernel connection and source scope

G220's supplied regular clock correspondence gives

    R_AB=sqrt(f_B/f_A), delta_AB=-log R_AB,
    chi_clock=tanh(delta_AB)=(f_A-f_B)/(f_A+f_B).

The last expression is the compatible completed clock leg under G176's
WORKING_FOUNDATIONAL_CLARIFICATION. It does not reconstruct the remaining pair
germ or close native event/path/assembly. Clock comparison and ray geometry
are linked at the stated supplied protocol, with no second fitted kernel law.

G260/G395 own the family; G397 already owns scoped static clock/readout
bounds. This campaign adds their linked finite signal/calibration contract,
not a rediscovery of those sources or a claim of novelty in known mathematics.
G312 remains GR FILTER ONLY, native response membership unclosed. Universal
Reciprocity/DDR remains owner-provisional; the chosen observers do not become
preferred physical frames. Other observers use the covariant k·U/tetrad readouts.

## Verification and limits

The actual new full398 premise audit passed in404.188 seconds, exit0 and empty
stderr. It completed before parent numerical execution. Exact symbolic/rational
calibration and transformation checks passed. All nine frozen FLOAT64 examples
and tighter repeats passed; maximum scaled tighter change was4.12e-14.

One fresh context independently reconstructed the main relationships before
candidate exposure, then attacked the whole candidate. Its separate affine
geodesic implementation evaluated18 case/control combinations (nine geometries,
two controls), with affine ODE integrations inside each root search, checking the
original null constraint and boundary residues. The raw IVP call count was not
instrumented;18 is the number of saved final case/control records. Against the parent
quadrature, maximum absolute differences were6.67e-15 in turning radius,
1.17e-15 radians in angle and3.20e-14 in dimensionless round-trip time.
Agreement is floating-point support, not interval certification. Shared source
metric and libraries remain shared; different runtime model and human review
are UNTESTED. Three parent defect variants failed and the reviewer independently
replayed all three; its own exact algebra checks included distinct defect injections.

Three scope clarifications were accepted; no equation, sample or tolerance repair
was needed. The later credited review/REGULAR_ROOT_NOTE.md independently checks
endpoint-root regularity/uniqueness on the diagnostic bracket [2,5.5] for the
chosen endpoints and b range. It distinguishes that condition from a simple
radial turn; it is not a general-family branch theorem. Numerical root locations
and signs remain floating-point evidence. At the chosen angle2 in (pi/2,pi),
the flat comparison chord has its perpendicular foot between the endpoints. Preservation, actual resource/review intervals, navigation checks and
publication have separate closeout receipts. Historical source checks not repeated
are not counted as current passes.

Conditional faux-light means distinguishable probes following supplied null
geodesics, with proper-clock tags and local sky readout, neglecting backreaction.
No photons, EM/Maxwell, energy transport, brightness, interference, polarization,
physical source/relay/clock realization or native light law is derived. The
parameters are not identified with a Sun, mass, charge or selected cosmological
content. No dataset, fit, physical size, X_max, source/action/carrier law or canon
is supplied. Multiple paths, caustics, nonspherical/evolving metrics and general
branch existence/uniqueness remain outside this result.

If another theory supplies the same metric and signal rules, it predicts the
same records. This supplies a conditional consistency test and a useful virtual
measurement baseline; it does not by itself distinguish UDT from GR.
