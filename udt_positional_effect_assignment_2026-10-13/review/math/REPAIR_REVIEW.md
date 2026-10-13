# PEA1 mathematics review of precision repair

Verdict: **repair accepted; VERIFIED-WITH-CAVEATS conditional mathematical
conclusion survives.** Reviewed REPAIR.md SHA256
`a0341edc8e32fe4e369c9975adf15e4308dc0636a3ecce2f99a644520ff45665`.

Exposure chronology matters. This reviewer's DIRECT_REVIEW.md was already
saved at SHA256 `17db05c6064eebd50763dfc42215e6f31426c028353a2b3d88ffe4fca96a2250`
when the parent relayed the fidelity reviewer's finding. The direct review and
independent check had both used the half-squared world function, but this
reviewer did not flag the frozen researcher's inconsistent words. I therefore
claim no independent discovery of that wording defect. DIRECT_REVIEW remains
unchanged; this exposed follow-up records the correction and its effect.

For the fixed static flat histories A(s)=(s,0,0,0) and B(T)=(T,L,0,0),

    D(s,T)=-(T-s)^2+L^2,
    sigma(s,T)=D(s,T)/2.

At s=0,T=L, partial_T D=-2L and partial_T sigma=-L. Both defining functions
vanish on the same outgoing branch. Implicit differentiation gives

    dT/ds = -D_s/D_T = -sigma_s/sigma_T = 1.

This is direct differentiation, with no rounding or new computational run.
The already saved CHECK_RESULT/check_independent.py use sigma and verify its
actual branch and derivative. Neither the mathematical inference nor that
independent check depended on naming D as sigma.

On the candidate's common sufficiently short convex normal tube, define sigma
by one-half the metric norm squared of the inverse-exponential separation.
Smooth metric/geodesic-ODE dependence, followed by the implicit-function theorem
at the nonzero reception derivative, yields the same smoothly varying reception
map. Ordinary proper-clock rates also vary smoothly. Thus both physical net
Z limits remain1 while the assigned limits remain1 and1+2aL. Multiplying a
defining function by2 changes neither its null zero set nor derivative ratio.

The defect was an interval-normalization/name mismatch, not a failure of the
regular root, an incidence change, or a new physical assumption. The smallest
repair is exactly the supplied definition/wording correction. Existence,
rank-based uniqueness, strict all-null sign, reference nonextension and the
separate echo/tide identity need no scientific repair. All original domain,
query, same-history, differential-tick and UNADOPTED qualifications remain.

This is the first included precision repair/re-review, not a rerun of every
source test. Central integrated descendants have not yet been exposed here;
their exact final versions still require the promised separate attestation.
No candidate, maintained source, registry grade or CANON was edited by this
reviewer. Same model/context and exposed-review limitations remain as recorded
in DIRECT_REVIEW.
