<a id="r16pia"></a>

#### Physical clock/source admission — PIA1

The independent interface audit finds no admitted physical realization of
FRI1 among the three reviewed protocols. The obstacle is more specific than
instrument precision: FRI1's supplied tail requires an extreme TOTAL clock
ratio, a particular source/receiver geometry and independently justified error
conditions. This does not refute FRI1's conditional inversion, UDT, or all
possible finite experiments. It blocks presenting the1.902% synthetic width
as an experimental accuracy forecast.

From the existing class, h<=.85, B<=.0001, w<9 and alpha<=1.000000006 give

    Z>54180, HR>=50000, R/a>=500000, R/m>=5000000.       (PIA1-1)

The first inequality follows from Z=(1-wB)/(sqrt(h)alpha y) and the exact
lower bound .9991/[sqrt(.85)*1.000000006*.00002]>54180. Also f(R)<0;
the receiver is outside the supplied static region. These are implications
of the conditional metric/query, not measurements, an extra redshift factor,
or native UDT predictions. An independently valid upper bound on the actual
paired-clock total Z below54180 would reject THIS class. An unknown source
normalization or a reduced systemic spectral proxy cannot supply it directly.
Large Z alone does not establish the class. Exact principal B_*=0 preparation
and entire-support-hull admission remain unverified by finite angular samples.

Writing K=c_E H and C=K T_seconds gives a/c_E=A T/C and R/c_E>=50000 T/C.
For the BASE synthetic history the long control has C=1, short C=.008 and
K delta=.0005. Its homothetic companion has half those values at the same
calibrated times. Changing H to shorten the observing period also changes
the required geometry. No time in years is established; R remains areal
radius, not an observed distance, travel time or X_max. G has no new mass
interface and H has not been identified with an observed Hubble rate.

**Source and instrument interfaces.** Ordinary proper-clock kinematics give
nu_o=nu_e/Z, so FRI1's Y is -log(nu_o/nu_ref). An independently supported
emitter-time drift bound Q_e transfers to receiver seconds as q_seconds<=Q_e/Zmin,
only once the needed Z lower bound is independently admitted over the interval.
Source calibration, reference stability, finite pulse/cycle resolution and
visibility are additional physical interfaces. Bounded frequency amplitude or
sampled stability does not by itself bound the derivative through all gaps.
Allowing arbitrary source drift defeats timing identification: replacing
nu_e1 by nu_e2=nu_e1 Z2/Z1 along each history gives identical nu_o.
This is an ambiguity outside FRI1's q restriction, not a new source law.

A uniform phase-window counter measures mean frequency, whereas FRI1 uses
mean log-frequency. If |Y'|<=M on a window of width delta, then

    0<=mean Y + log(mean exp(-Y)) <= M² delta²/8.         (PIA1-2)

The proof bounds the variance of Y under exponential reweighting by one
quarter of its squared range and integrates twice. The base long-control
values bound the bias by3.13438203125e-8. It can be budgeted or corrected;
this does not certify any real counter. An independent M or an H-dependent
compatibility calculation is needed, not substitution of the desired H.
Actual weighting, gating, dead time, clock rate and width calibration need
their own reductions. Timestamp-center error does not automatically cover them.

The nominal epsilon_z=.003 allows at most about.29955% uniform fractional
frequency error if this were the sole error. The angular tolerance5e-8rad is
about10.313mas in the declared parallel radial frame. Physical budgets must
include transfer/reference/estimator errors and angular-frame registration,
motion and feature stability. Relative position precision alone does not fix
the frame; an unknown rotation can mimic the angular drift.

**Three reviewed protocol classes.** [Primary-source audit](udt_physical_clock_interface_audit_2026-10-05/SOURCES.md)
links the methods and qualifications, with published outcomes exposed.
Engineered atomic-clock links support precise calibrated frequency transfer
in their tested local setup, but do not realize this extreme-tail geometry.
The reviewed pulsar protocol fits unknown spin/spin-down; residual precision
does not independently bound the secular source rate needed here. Megamaser
monitoring supplies spectral and angular records, but feature/disk reductions
are not FRI1's means/frame. The existing near-unity systemic proxies do not
certify the extreme paired-clock regime; no new likelihood exclusion is made.

Published statistical uncertainty is not a deterministic all-time bound.
This does not require unattainable absolute empirical certainty: for each
fixed admitted history, a measurement model giving the JOINT required-bound
event probability>=1-p transfers that coverage to the deterministic H enclosure.
Conditional component failure probabilities can be combined by a union bound,
without independence. No such instrument model or coverage certificate is
supplied here; pointwise errors alone do not certify a whole observing hull.

The [initial argument](udt_physical_clock_interface_audit_2026-10-05/INITIAL_CANDIDATE.md),
[review clarifications](udt_physical_clock_interface_audit_2026-10-05/REVIEW_REPAIR.md)
and [descendant review](udt_physical_clock_interface_audit_2026-10-05/DESCENDANT_REVIEW.md)
preserve positive and negative scope. The supported return is an explicit
missing physical interface. FRI1 remains a tool; native geometry selection,
physical mass/X_max and an additional effect beyond matched GR remain open.
The [decision brief](udt_physical_clock_interface_audit_2026-10-05/DECISION_BRIEF.md)
proposes testing a specified moderate-regime protocol before any empirical fit.
