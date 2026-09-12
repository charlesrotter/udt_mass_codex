# OB1 source-first reconstruction, before candidate exposure

Reviewer context: `/root/ob1_optics_review`. First observed UTC clock:
2026-09-12 13:52:39. Parent's completed startup is attributed to STARTUP_RECORD.json
and the actual startup_premise397 capture/streams: exit 0, 404.541622 seconds.
Independently checked grok=origin/grok=4c56085101da045b8d00732528bb6f99ed0fd8e2
and the original 46 untracked status-name entries' SHA-256
55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2.
Protected filenames were seen in status; no protected payload was opened or hashed.

This reconstruction is sealed before opening OB1 INITIAL_CANDIDATE,
FRAME_AND_DISCOVERY, scientific code, outputs, CHECK_HISTORY, or prior OB1 verdict.
Exposure already includes the parent task, SOURCE_FIRST_REVIEW_TASK, WORK_ORDER,
SOURCE_PINS, selected G405/G407/G176/G166 rows, the full accepted G405 candidate
and review, G166/G176 reports, banking record, source README, and selected source
text. The permitted source README already contained the parent's interpretation
of source scope and a warning about the extracted Eq.12 sign. Thus this is a
source-first argument stage, not a wholly blind proposal or independent discovery.
The first attempted startup metadata filename was absent; the actual capture
provenance, JSON, stderr and stdout were subsequently read. No scientific run failed.

Runtime model/version is UNATTESTED. Parent configured gpt-6-astra/xhigh is attributed,
not runtime evidence. Context is fresh; different-model and human/formal review
are UNTESTED. I will write my own scientific check without importing author functions.

## Source-first mathematical reconstruction

Question/quantifier: for the supplied smooth stationary G405 threading geometry,
what can an ideal reciprocal, coherent two-direction loop delay interface measure?
This is metric-led mathematics plus explicitly imported conventional optics.
The metric, observer U=N^-1 partial_t, marked loop, detector/source at P, units,
and ideal transfer are supplied class/design choices (free-and-explored), not
native solution selection. G166 native assembly remains OPEN; G176 is WORKING.
The primary scalar kernel cannot supply a light law, apparatus, path or population.

Write g=-N^2(dt+beta)^2+gamma, with N>0 and gamma SPD. For a path tangent v,
future null transport obeys dt=-beta(v) ds+sqrt(gamma(v,v)) ds/N.
Define L=integral_C sqrt(gamma(v,v))/N ds and B=integral_C beta(v) ds.
If the same spatial path is followed in both directions in a stationary apparatus,
coordinate transit times are t_plus=L-B and t_minus=L+B, hence

    d := proper_delay_plus-minus = -2 N(P) B.

This follows directly by the two null roots and orientation reversal; Ruggiero
and Tartaglia Sec.II/Eqs.2-11 supply the matching conventional equal-local-speed
argument. Their Eq.12 extraction has sqrt(g00) despite g00<0; derive the detector
conversion directly from g|P=-N(P)^2 dt^2 instead of copying it.
For a reciprocal speed u(x) other than unity the common L changes to integral
sqrt(gamma)/(N u), but the difference still cancels under the explicit equal-speed
condition. That is not automatically an optical PHASE-delay theorem in a medium.

There is a causality/domain gate: G405 alone does not require t-slices spacelike.
A sufficient clean loop condition is |beta(v)|<sqrt(gamma(v,v))/N along the path,
so both coordinate roots progress forward. At minimum the two delay transfers must
have positive transit durations and a causal, stationary implementation. This is
an added supplied apparatus/domain restriction, not a theorem from N>0 and SPD alone.

Vacuum geometric optics follows null geodesics at short wavelength (Dolan Intro
and Sec.3.1/3.2); an arbitrary common spatial loop in stationary geometry need not
be two counterpropagating geodesics. A stationary reciprocal guide, prescribed
mirror system, or equivalent constrained transfer must be assumed and justified
as an interface. A null curve is not by itself a derived realizable optical guide.
Likewise, phase velocity and group/transit delay cannot be identified in a general
dispersive apparatus. An ideal coherent pure delay is sufficient and explicit:

    E_plus(tau)=a_plus E_s(tau-T_plus) exp(i kappa_plus),
    E_minus(tau)=a_minus E_s(tau-T_minus) exp(i kappa_minus),
    E_s(tau)=exp(-i omega tau), a_plus,a_minus>0.

At ONE common reception event, arg(E_plus conjugate(E_minus)) is
omega d+kappa_plus-kappa_minus modulo 2pi. The opposite source phasor convention
or opposite arm order reverses the displayed sign. Equal-emission pulses arriving
at different events do not directly define an interference phase. A continuous
coherent source compares different emission phases at their common reception.
Stationarity and pure delay make the common-event phase linear in omega; guide,
polarization, reflection, coherent detection and finite-wave errors are additional
interface hypotheses, not products of the metric calculation.

The sufficient augmented G405 record data are common marking plus T=N,
m_i=N sqrt(gamma_ii), B_i=beta_i/m_i along the loop; beta_i=m_i B_i and N(P)
give d. Full six-direction records reconstruct the rest geometry to check the
admitted class and delay durations. First derivatives are unnecessary for a line
integral if the actual fields along the whole loop are supplied. Phi=-log N alone
loses beta. Even normalized H_i/B_i fields lose m_i: the G405 control
g_lambda=-(dt+lambda x dy)^2+lambda^2 delta has identical T and B_v but different
beta and loop delay. Thus it is full retained, marked data, not the scalar alone.
Under t'=t+f(x), beta'=beta-df and a closed integral is unchanged; under t'=a t,
N'=N/a and beta'=a beta, so N(P)B is unchanged. A loop integral is not pointwise
W or a full metric inverse measurement; many beta perturbations have zero integral.

## Calibration and wrapped-phase conclusions before author exposure

Use three nominal proper angular frequencies omega_j=omega_0+j Delta, Delta!=0,
and noiseless phase phasors z_j=exp(i(a+omega_j d)), j=0,1,2.

With independent geometric delay d_g, only a is fitted from z_0. Frequencies 1 and
2 are unused phase predictions. Residuals are z_j conjugate(z_0)
exp(-i j Delta d_g); both equal 1 under the ideal model. A delay departure alias
2pi k/Delta is invisible after a absorbs omega_0 times that alias. This does not
identify d absolutely. Supplied geometry must be independently supplied, not
reconstructed from these same optical values and relabeled a prediction.

Without independent d, z_0 and z_1 fit the two parameters modulo aliases.
d_k=(arg(z_1 conjugate(z_0))+2pi k)/Delta and a_k=arg(z_0)-omega_0 d_k.
Despite infinitely many slopes, the unused third prediction is unique:
z_2=z_1^2 conjugate(z_0). Equivalently closure z_0 z_2 conjugate(z_1)^2=1.
The blind set is exactly delta_0-2delta_1+delta_2 in 2pi Z, not merely real-affine
unwrapped departures. This is a finite affine-phase consistency test, not a test
of one independently specified geometry or a native UDT signal.

An unknown instrumental delay b enters the same column as d, so only d+b is
observable; knowing d_g does not recover a geometry-specific constraint unless b
is independently controlled/bounded. More frequencies cannot split identical
columns. Arbitrary unknown phase at each frequency absorbs all finite phase data.
A frequency-independent differential phase offset is a substantive apparatus
assumption; it is not justified simply by calling one datum calibration.

Circular error distance obeys the triangle inequality without statistical
independence. If per-frequency circular error bounds are u_j, the closure null
bound is u_0+2u_1+u_2, supplemented by declared transfer errors and frequency
errors |d|(|delta omega_0|+2|delta omega_1|+|delta omega_2|).
That last estimate requires an independent finite bound on the TOTAL delay when
it is inferred only modulo aliases. Unknown unbounded aliases cannot support a
finite frequency-error budget. Known geometric delay uncertainty u_d gives
pairwise bounds u_j+u_0+|j Delta|u_d+(|d_g|+u_d)(v_j+v_0), where v bounds angular
frequency errors. Any instrumental/model contributions must also be retained.
Bounds >=pi are vacuous for rejection. A circular signal separation >2E gives
guaranteed rejection under a valid null bound E, when such separation is possible.
No detector errors or experimental power are currently supplied.

## Frozen direct-review and independent-check plan

Audit candidate hypotheses, original failures and repairs, record density,
future-root and common-event signs, clock factor, guide/phase distinction,
wrapped alias proof, nuisance blind spaces, and frequency/geometry errors.
Independently implement direct pullback quadratic roots and a concrete nonconstant
lapse/nonzero-shift loop witness; use a flat rotating-frame source/detector arrival
calculation as an alternate physical sign/factor anchor where feasible. Check
record sufficiency/omission, clock/gauge invariance, exact rational phase turns
modulo integers, three-frequency heldout prediction and instrumental-delay
confounding. Use explicit negative examples that fail meaningful guards; do not
count tautological restatements as independent certification. Inspect and replay
author code only after the independent scientific implementation is fixed.

CPU exact algebra, no grids/GPU/data/experiment: one scientific subprocess in this
context, one thread, <=180s/2GiB using the inspected existing capture wrapper.
Stop by parent hard return15:31:25UTC, target substantive review before14:55UTC,
or on new-premise/protected/source-conflict/resource blocker. Preserve any failed
checks; bounded same-premise repair/re-review is authorized, promotion is not.
Maximum result: VERIFIED-WITH-CAVEATS at exact supplied-metric plus ideal-optical
scope, a narrowed finding, or an unresolved objection. No apparatus qualification,
empirical validation, unique UDT signature, native light derivation, or canon.
