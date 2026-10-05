# PIA1 exposed mathematical and interface review

Actual reviewer: the same separate context `/root/pia_math` as
SOURCE_FIRST_REVIEW.md, now exposed to parent INITIAL_CANDIDATE.md and
SOURCES.md. Source-first findings had already been sent to parent and written;
parent candidate/control code had not been read for that phase. Exact exposed
inputs are hashed in EXPOSED_INPUTS.json. Parent implementation still unread.
Shared model is disclosed; no cross-model or independent experimental
verification is claimed.

Verdict on this initial candidate: **VERIFIED-WITH-CAVEATS** as conditional
mathematical/interface synthesis, with the two small clarifications below.
It does not admit any actual physical experiment or regrade FRI1.

1. P1 independently matches the source-first exact rational check and the
   positive-factor algebra. The conservative threshold >54180 is sound and
   is not falsely advertised as the exact minimum. Its interpretation as a
   total paired-clock Z, rather than a new factor appended to a reduced
   astronomical proxy, is essential and correctly retained. Necessary does
   not mean sufficient; P1 does not certify all of D.
2. P2 follows direct substitution into A, mu and y. It correctly preserves
   areal radius versus physical distance and leaves H unidentified. Small
   clarification: label C=1, C=.008 and K*delta=.0005 as the **base-H**
   synthetic control. On the same schedule the homothetic H/2 history has
   half these dimensionless values. The initial wording can be read as
   describing the reference control, but explicit labeling prevents a
   mistaken all-history monitoring claim.
3. The source-clock drift conversion is the correct chain rule in proper
   seconds. It requires an independently supported emitter-time derivative
   bound across the actual mapped interval and source/receiver calibration.
   The source-amplitude example epsilon*sin(omega*tau_e) correctly refutes
   amplitude-alone derivative control. The arbitrary-drift ambiguity is also
   valid: composing the positive proposed nu_e2(t) with its own monotone
   emission map supplies a source-time function; this is not silently a
   physical source model admitted under a bounded q.
4. P3 is sound. For X=-Y, g''(t)=Var_t(X) under the normalized exponential
   tilt. The tilted support is unchanged, and variance is at most L^2/4
   because its mean minimizes squared deviations while the interval midpoint
   is within L/2 of every value. Thus
   `g(1)-g(0)-g'(0)=integral_0^1 (1-t)g''(t)dt<=L^2/8`.
   Smooth FRI1 Y and positive finite windows meet differentiability and
   boundedness hypotheses. Its base-long value is
   `(.005*(1+.0005)+.000005)^2*.1^2/8=3.13438203125e-8`, below 3.14e-8.
   Parent correctly avoids using an estimated H as an independently known
   error bound and retains candidate-by-candidate compatibility as an option.
   The correction is not source/instrument validation. The separate
   source-first numerical counterexample already showed that estimator bias
   need not cancel between windows.
5. The fractional-frequency-to-log bound is correct for 0<=r<1. The angular
   tolerance conversion is about 10.313 mas and does not itself admit the
   physical radial frame. Free frame rotation can conceal the equatorial
   signed-angle drift. Timestamp error does not automatically cover an
   unknown multiplicative receiver clock scale; the text explicitly retains
   clock-rate uncertainty in the budget, consistent with the independently
   checked K_hat=K/(1+kappa) relation.
6. The proposed probability transfer needs one wording clarification. For
   each fixed admitted history/parameter, under its declared observation
   model, let E be the JOINT event that every required finite-window and
   hull-level assumption/bound holds. If P(E)>=1-p, FRI1's deterministic
   implication gives at least that coverage for the resulting H interval.
   Separate valid failure bounds combine by the union bound without
   independence. But a high **unconditional** P(E) does not automatically
   retain the same coverage after conditioning on a selected geometry/source
   class. For example, all failures can occupy a class of probability .01:
   unconditional coverage .99 coexists with zero coverage conditional on
   that class. Specify 'for each admitted fixed history' or explicitly
   condition the joint probability on the class. Parent was notified; no
   new physical premise or expanded calculation is needed for this repair.

I read the parent's five-source paraphrase ledger for semantic consistency.
I did not independently download/read those external papers, and therefore
do not attest their factual transcription. Another review must own that
primary-source check. The scoped conclusion 'none of these three documented
protocols supplies all required FRI1 interfaces' is logically appropriate
if the ledger's checked source limitations hold. It does not become a theorem
that no atomic-clock, pulsar, maser or other experiment can ever work.

The next-question text is a proposed new work order, not executed authority.
The current tail's eta cannot be reused for a different observed-ratio domain.
No Hubble parameter, material mass, X_max or new matched-GR difference is
introduced by the initial candidate. No additional controls or physical
source fit were run during this exposed pass; source-first controls remain
12/12. Final integrated text and resolution of the two clarification points
remain to be inspected before final attestation.
