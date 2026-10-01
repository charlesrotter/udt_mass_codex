# PCC1 supplement mathematical review

Verdict: **VERIFIED-WITH-CAVEATS** for the two explicit controls and their stated
limits. No substantive objection or required scientific repair was found.
Reviewer `/root/pcc_math` saw the parent's SUPPLEMENT, fidelity/SOURCE_FIRST,
the fidelity check implementation and its actual saved output after freezing
and running the independent mathematical reconstruction. No peer verdict was
seen. The variable-kappa construction originated in this math context; this
review checks the parent's transcription, not a claim of independence from
one's own discovery. The cubic control is source-exposed from the separate
fidelity context and was checked here by a separate analytic calculation.

For the first control, a0=exp(t^2/2), a=exp(t^2/2+ct), H0=t and H=t+c.
The sectional difference is 2ct+c^2 in all six planes. The parent's displayed
connection, reference Ricci transfer and target-connection divergence agree
with the direct original-connection outputs and the subsequent PCC-c check.
The dimensional b variant is consistent: H0=bt and H=bt+c gives 2bct+c^2.
Selecting b=1 by units for b>0 is a supplied comparison choice, not a selected
physical scale. The metrics are smooth and nondegenerate, so this is an actual
varying regional contrast, not merely a formally unsolved Bianchi condition.

For the second control, a=1+b t^3 is positive on a sufficiently small open
neighborhood of t=0 for each fixed finite b. At t=0, a'=0 makes the spatial
preparation line a spacetime geodesic and makes parallel transport of the
initial U trivial along it. The comoving receiver and emitter subsequently
follow geodesics. Thus the preparation meets PSW1, with proper separation L
because a(0)=1. a''(0)=0 and a'(0)=0 set the complete curvature tensor at that
event to zero, for every initial frame by tensoriality.

Hold these same comoving worldlines fixed while varying the emission time s.
Their exact conformal incidences give

    eta(tb)-eta(s)=L,  eta(ta)-eta(tb)=L,
    p=a(tb)/a(s),     q=a(ta)/a(tb).

At s=0, eta(t)=t-bt^4/4+O(t^7), whose local analytic inverse exists because
eta'(0)=1. Hence tb=L+bL^4/4+O(L^7) and ta=2L+4bL^4+O(L^7). Substitution into
the exact arrival derivatives gives

    log p=bL^3+O(L^6),  log q=7bL^3+O(L^6).

This independently checks the fidelity code's series operations and the
parent's coefficients/remainders without applying PSW1 to manufacture cubic
terms. With b nonzero, sufficiently small positive L produces nonzero shifts
despite zero quadratic terms. Both flights and neighboring emissions must stay
in the a>0 regular neighborhood; the supplement explicitly supplies that
restriction. No finite-L numerical error constant or global sign is inferred.

The point-only limitation is essential and correctly stated. This pair does
not satisfy zero curvature contrast in an entire neighborhood, so it cannot
refute any regional all-frame requirement. Nor does 1:7 at cubic order
contradict the 1:3 relation for PSW1's quadratic coefficients, both of which
vanish here. It supplies no positional attribution or native physical input.

No additional scientific process was run for the cubic review: the analytic
incidence and inversion argument above is the independent check. The fidelity
saved output was inspected for its cubic checks and PASS, but was not rerun;
shared SymPy, model family and sources are not new independence axes. The
variable-kappa controls were run by this context as recorded separately.
This scoped review neither re-proves all of PSW1 nor certifies finite-clock
accuracy, general region construction, empirical behavior or UDT selection.
