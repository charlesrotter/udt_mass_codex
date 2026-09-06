# Step05 candidate — shared-content exclusion survives bounded weight uncertainty

CANDIDATE, UNPROMOTED; separate-context review pending.
IDs SC5-ROBUST, SC5-CLASS, SC5-THRESHOLD. No calibration accuracy is asserted.

## 1. Exact uncertainty class and its logical quantifiers

Retain reviewed SC2's nonempty measurable partition P,Q,R, common finite
nonnegative measure mu and windows W1=P union Q, W2=Q union R, W3=P union R.
Use the owner-provisional G351/G352 ideal readout and CHOSEN phase-independent
product at their existing scopes. Supply reference rates r_i>0, spacing Delta>0
and a conditional uniform relative bound 0<=e<1. Define a=1-e>0,b=1+e and

    z_i=y_i/r_i = integral_[W_i] f_i(lambda) dmu,
    a <= f_i(lambda) <= b.                              (1)

Active weights are bounded measurable; values outside the window do not
contribute. For an actual G352 query f_i=omega_i/(r_i Delta). The weight
bound is supplied query/calibration information IF supported; no observational
support for a value of e is provided here. The windows and transported label
registration are exact. Sources, registration error, record noise, finite-time
integration and device identification are not folded into e.

Necessity below holds for every fixed set of bound-valid kernels, whether
constant or varying within cells. Sufficiency means there EXISTS a set of
allowed kernels AND a measure giving the record. It is not sufficiency for
every fixed actual kernel, observer, metric development or chosen content.
The algebraic class can include measurable kernels without a chosen smooth
geometric realization; the converse uses only a constant-weight smooth
geometric subclass of SC2. This avoids claiming arbitrary kernels are metric
selected. No total measure, density regularity or probability normalization
is imposed.

## 2. SC5-ROBUST: exact uniform exclusions, without exact frequency constancy

Every record satisfies z_i>=0 and

    b(z_j+z_k) >= a z_i,     {i,j,k}={1,2,3}.           (2)

For example the certificate for i=3 is h=(b,b,-a). Its pointwise contraction
with the normalized kernels is b f1-a f3 on P, b(f1+f2) on Q, and
b f2-a f3 on R. On P and R its lower bound is ba-ab=0; on Q it is
nonnegative. Integrating against any finite nonnegative mu proves (2).
All three certificates follow by permuting windows/cells. No unknown total
mass estimate, independence of weights and content, cellwise constancy,
sampling of lambda, or fitted source profile was needed. Bounded kernels
and finite mu make every integral finite.

Thus a negative contraction excludes the JOINT assumed ideal record,
common positive measure, exact registration/windows and weight bounds.
It neither assigns blame to one assumption nor directly refutes UDT or
establishes an actual instrument-to-readout map.

## 3. SC5-CLASS: sufficiency over the declared uncertainty class

Conversely suppose z_i>=0 and (2). Seek unweighted window amounts s_i,
with

    L_i=z_i/b <= s_i <= U_i=z_i/a

and the ordinary triangle inequalities of SC2. Condition (2) is exactly
L_i<=U_j+U_k for each i.

If U obeys all triangle inequalities, choose s=U. Otherwise there is a
unique offending index i with U_i>U_j+U_k: two such strict violations would
contradict nonnegativity. Keep s_j=U_j,s_k=U_k and set s_i=U_j+U_k.
The upper/lower bounds hold because L_i<=U_j+U_k<U_i, while other entries
retain U>=L. The new triple obeys all triangle inequalities: one is equality
and the other two follow from nonnegativity. This covers zeros as well.

SC2's inverse then supplies nonnegative cell masses

    m_P=(s1+s3-s2)/2,
    m_Q=(s1+s2-s3)/2,
    m_R=(s2+s3-s1)/2.                                  (3)

Choose one point in each nonempty cell and the corresponding finite sum of
point-evaluation measures. Set f_i=z_i/s_i CONSTANT on its active window
when s_i>0. The interval bounds imply a<=f_i<=b. If s_i=0 the same bounds
force z_i=0; set f_i=1, which lies in [a,b]. Equation (1) now gives z exactly.
The measure is on label space, not a literal atomic phase/time counting law.
No converse fixes a pre-existing measure or its finer distribution.

Therefore (2) together with z>=0 is necessary and sufficient over the
uncertainty class, including zero records and boundary masses. For e=0 it
reduces exactly to SC2's triangle conditions. For e>0 it is a genuinely
weaker constraint. A record admitted by this enlarged class can still fail
for its actual fixed weights (for instance the weights identically1).

The converse is geometrically supportable without changing a metric law.
In SC2's supplied Minkowski/parallel-phase construction keep phase, spacing,
label cuts/windows and reference positive r_i. At cut i choose the constant
observer parameter d_i=Delta r_i f_i/alpha>0. The source's observer formula
gives g(U_i,U_i)=-1, U_i future, omega_i=alpha d_i and the required active
weight r_i f_i. These are legitimate chosen observer/query data on distinct
cuts, not a claim that an already fixed observer can be altered for free or
that every admitted metric supplies these values. The common product measure
still is CHOSEN; no curvature current or physical content is selected.

## 4. SC5-THRESHOLD: how much uncertainty removes an exclusion?

For a nonzero nonnegative record, put S=z1+z2+z3>0. Inequality (2) is

    S-2z_i+e S >= 0.

Hence its exact uncertainty-class feasibility threshold is

    e_* = max(0, 2 max_i z_i/S - 1).                   (4)

For 0<=e<1 the record is possible in the class iff e>=e_*.
The zero record is possible for all allowed e and is handled separately;
division by S=0 is never performed. If only one entry is positive, e_*=1,
so no e in the retained range admits it. We do not extend the proof to e=1:
the positive lower bound and the construction using U_i would then fail.

For the diagnostic z=(1,1,3), the i=3 residual is -1+5e and e_*=1/5.
It is excluded uniformly over all allowed weights when e<1/5. At e=1/5,
choose m_P=m_R=5/4, m_Q=0, f1=f2=4/5 and f3=6/5. The three ORIGINAL weighted
integrals are exactly (1,1,3). This also belongs to every larger allowed
bound e<1. The example proves sharpness of the uniform exclusion threshold,
not an empirical20-percent tolerance, typicality, or unique physical choice.
At the fixed weights f_i=1 this same record remains incompatible by SC2;
the existential class statement must not be strengthened to all kernels.

## 5. What remains supplied and what failed

Exact frequency constancy is not necessary for a shared-content constraint:
the pointwise bound suffices. But unconditional rejection of (1,1,3) fails
once the supplied uncertainty class reaches1/5. Independently positive
readouts are still not generally jointly possible for any e<1; a one-positive
record is a simple limiting control. Unknown within-cell content remains free,
and the enlarged uncertainty class generally removes SC2's unique cell-mass
identification. The result selects neither weights nor content.

For a real use, one must support the ideal readout interface, common-label
registration and the frequency bounds; naming them in this definition supplies
no such evidence. Query information is not automatically an additional law.
If an application requires a new physical measurement rule, that is a separate
authorization/evidence boundary, not an assumption hidden in this result.

## 6. Evidence and discovery ceiling

The pointwise certificates and interval/triangle construction carry the
universal/existential quantifiers. Exact rational controls test original
weighted integrals, zero/boundary cases, observer norm/frequency and threshold
sharpness; mutated formulas test implementation sensitivity only. No observed
data, source fit, numerical tolerance, metric PDE solve or reviewer finding
was used to construct the candidate. General variable-kernel necessity is
analytic, not established by a finite grid. No physical law, content identity,
instrument accuracy, accepted scientific grade or canon follows.

Author execution before freeze:16 guard groups/1262 assertions passed over
625 signed rational record controls (182 constructed,443 rejected), plus
pointwise corner, threshold, zero and original observer-contraction controls.
These counts support implementation checking only. All4 actual changed-code
paths failed: unrelaxed and wrong_sign at sharp_boundary_not_rejected;
missing_half and fixed_weights at original_weighted_integrals_reconstruct.
No unexpected author failure or repair occurred. Python3.10.12 exact Fraction
arithmetic used the declared512MiB/60s capture; all commands/streams preserved.
The independent reviewer has received the question/dependencies, not findings
from the author; candidate is now frozen before any reviewer conclusion.
