# TM1 source-first reconstruction — sealed before candidate exposure

Reviewer /root/tidal_tm1_review. Baseline 508eb238d1321a3bdce9a45eb47a97b63fb1b541,
grok, checked directly. This is a source-first assessment, not a direct verdict
on the still-withheld TM1 author candidate. Exact model UNKNOWN; fresh context
YES; different model, human specialist and formal verification UNTESTED.

AGENTS.md startup authority, current bounded status chain, triggered
no-shortcuts/completeness-map/verifier-before-record skills and
CROSS_MODEL_VERIFY.md read. Parent reported the current full 349-row audit
passed, exit 0, 399.178 seconds, after which the exact G261/G313/G358 registry
rows were queried. I did not rerun that audit or mutate git/shared sources.

## Independent geometric reconstruction

W4 remains WORKING/POSIT_NOT_CANON. G261 combines it with supplied
Lorentz-metric/Levi-Civita geometry to interpret ideal clocks, rulers and free
fall. This supplies no electrostatic force/voltage response, rigid metrology,
instrument self-gravity removal, or finite-baseline error theorem.

G313 uses contracted Bianchi in the adopted bounded smooth vacuum arena:
div(Ric-Rg/4)=dR/4, hence Ric=Lambda g and dLambda=0 on a connected region.
Neither scalar value nor Weyl tensor is selected. With G358's explicit slots
Q_abcd=g(R(e_a,e_b)e_c,e_d), E_ij=Q_i00j, Ric_00=sum_i E_ii=-Lambda.
Thus the negative freefall relative acceleration in calibrated SI units is
T=c_E^2 E, with trace(T)=-c_E^2 Lambda. It is not automatically zero.

At a single event any symmetric E is algebraically allowed when Lambda is
free; its trace calibrates one scalar instead of testing an additional
equation. Across a connected admitted vacuum region, trace constancy is a
necessary restriction, subject to registration, calibration and nuisance
control. A single observer's timelike E leaves G358's five mixed-curvature
components open. Any null-screen tide is blind to constant sectional
curvature. These statements are geometry, not instrument eligibility.

## Independent local kinematic argument

Define the instrument output sign as applied holding/compensation acceleration
on a sensor fixed at body-frame r, and define Wv=omega cross v. In an inertial
frame, x=O(t)r has acceleration O(dot W+W^2)r. Freefall acceleration differences
are -T r. Consequently the holding-force acceleration gradient is

    D=T+W^2+dot W,
    T=sym(D)-W^2,
    trace(T)=trace(D)+2|omega|^2.

If a positive arm has length L and the telemetry convention is half difference
a_d=(a_plus-a_minus)/2, then its D column is 2 a_d/L. The conventional potential
Hessian V has freefall relative acceleration +V r, hence V=-T. One must not
identify the released V with T by name. Reversing the sensor sign/orientation
requires the corresponding complete sign translation. Retaining relative proof
mass motion adds Coriolis/relative acceleration terms; the above fixed-sensor
idealization must carry those omissions as error terms.

stage_a_exact.py independently starts from a rotation Taylor jet and computes
holding forces for two arms, then forms nine differences. Twelve exact
symbolic/synthetic checks passed, including opposite rotation-sign,
potential/tide-sign and factor-two counterexamples. This uses SymPy 1.13.1,
Python 3.10.12; 0.498 seconds, 46,328 KiB maximum RSS, under the shared
512 MiB/60 second limits. General reasoning supplies quantifiers; checks do
not calibrate hardware or prove small omitted errors.

## Source qualification and lost directions

The 2006 L1b handbook is an accessible official source with internal editorial
inconsistencies: its Eq.4 has -V but its displayed Gamma and Eq.5 have +V;
Eq.11's yy entry displays the pair-25 X component. Eq.4 and the remaining
Eq.11 signs agree with the independent holding-force derivation above, with
the yy component read geometrically as its Y component. These defects must
be disclosed; they cannot establish which modern processor is implemented.

The versioned primary documents establish a chain requiring calibration and
attitude reconstruction, with model-assisted routes at later processing
stages. Their summaries and exact locations are in PRIMARY_SOURCES.tsv.
They do not prove every L1b trace is constrained to zero, nor that an unused
raw trace never exists. In particular, the L1b Eq.11 diagonal expressions
can carry a nonzero sum. Target-based validation criteria are not identical
to deterministic projection of the target out of every released value.

Independently of implementation, if the measured gradient is T+B with an
unconstrained additive matrix bias B, (T,B)->(T+qI,B-qI) leaves all records
unchanged. Spatial rotation cannot modulate qI away from a scalar bias. A
filter or fitted constant removal that annihilates constants removes the
absolute connected-scalar channel; centering illustrates this exactly. If
only time-independent bias is unknown, varying trace may still be testable;
unknown drift creates further aliases. No empirical error bound is inferred.

External model calibration does not mathematically erase every discrepancy,
but a target entering calibration, rejection, replacement or model fitting
cannot simultaneously be counted as an unused test without a dependency and
identifiability audit. The documented EGG_TRF_2_ replacement of low frequencies
and two off-diagonal directions provides a specific version-bounded reason
not to treat all its components as original independent measurements.

Source-first disposition: a conditional ideal map is reconstructable;
absolute/held-out eligibility of a particular released scalar channel is not
established by the inspected documents. A useful next question is the exact
surviving subspace after a fully declared calibration/processing map, including
bias and drift, rather than presuming a positive or negative universal result.
No new premise is necessary merely to state that question.

## Exposure, limitations and direct-review boundary

Read: work order, TM1 plan, registered G261/G313/G358 controlling definitions
and their authority reports/banking record; W4; primary technical documents
and metadata listed separately. No TM1 author argument/code/output/verdict.
The old G358 scientific candidate is an admitted source, not the new TM1
candidate. Its historical status wording is controlled by later banking.

Primary-document searches incidentally returned unrelated bibliographic and
qualitative mission/performance snippets, including a statement about trace
reduction. Those papers were not opened for outcomes, no quantitative
flight-data outcomes or residual arrays were inspected, and no observational
payload was downloaded or used. Primary processing descriptions are exposure
to methods, not confirmation outcomes. Old handbook assumptions/requirements
are not flight validation. Later official handbook access was unsuccessful;
the pinned revisions do not certify current released-product behavior.

Not done: physical calibration, noise estimation, flight-data validation,
full underlying UDT package replay, modern processor/source-code audit,
finite-baseline/relativistic error bound, complete Einstein test, human review,
or scientific promotion. Local PDFs stay temporary and are not redistributed.

Await the author's frozen TM1 candidate for direct adversarial comparison.
