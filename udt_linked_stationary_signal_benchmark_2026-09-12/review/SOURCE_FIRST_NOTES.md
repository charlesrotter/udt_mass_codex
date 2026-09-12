# LSB1 fresh source-first adversarial notes

Written 2026-09-12 23:25 UTC before opening any LSB1 parent candidate or numerical contract.
Reviewer context: /root/lsb1_stationary_review; separate context, inherited source/question/task
exposure. Configured parent gpt-6-astra/xhigh is attribution only; actual runtime model/version
UNATTESTED. Different-model independence UNTESTED. No subagents. Allocation maximum 40 elapsed
minutes including repair and final fidelity, hard stop 2026-09-13 00:03 UTC. Parent startup is
attributed: grok synchronized at c12db2562da1a5098f65a97ae0c924dec149ca4c, initial tracked clean,
46 collapsed untracked entries/51 expanded files. Reviewer independently read branch/status and
HEAD at 23:23 UTC: grok...origin/grok, that HEAD, no tracked modifications; LSB1 is additional
untracked work. Reviewer did not fetch or independently attest remote freshness. Parent current
398-row verifier was pending at dispatch; old source audit results are historical.

Exposure: AGENTS.md; WORK_ORDER.md; SOURCE_PINS.json; CLAUDE.md required sections; no-shortcuts,
completeness-map and verifier-before-record protocols; exact G220/G395/G397 rows; ND1 candidate;
QC1 candidate; G220 audit and exact derivation sections 1–4; current GR authority; bounded banking
record search; both unchanged existing capture utility implementations. Initial lookup of
SOURCE_PINS.tsv failed (actual pin file is .json). No LSB1 candidate/proof/numerical outcome seen.
No protected payload, runtime config, archive or disk inspection. Status names are not payload reads.

## Source scope and unclosed join

G395 reuses G260's complete one-function static spherical family; it neither selects a,b nor
adopts a physical response. G397 gives conditional ideal static clock ratios with supplied
areal-radius/time/frame matching; it supplies no light transfer law. G220 gives dτ_B/dτ_A =
(k_A·U_A)/(k_B·U_B) on one supplied regular null branch and explicitly does not adopt a signalling
protocol. The work order's null probes, static observers and local frames therefore are explicit
unadopted benchmark apparatus. G312 GR remains FILTER ONLY; no native response membership,
source/mass identification, scale or physical signal law follows.

## Independent analytic derivation

Use the supplied full metric L²[-f dT²+f^-1 dr²+r²dΩ²], f=1+a r²+b/r, f>0 on a
bounded positive-radius window. Static observers obey dτ=(L/c_E)√f dT. Stationarity shifts a
fixed spatial ray and its endpoints by a common ΔT. Thus time-tag slopes are
R_i=dτ_i/dτ_0=√(f_i/f_0), independent of flight-time offsets; conditional Killing contraction
in G220 gives the same arrow. Frequency-ratio interpretation is optional and not needed.

Let q_i=R_i² for i=1,2 at three independently supplied distinct positive radii r_0,r_1,r_2.
The exact two equations are

    (r_i²-q_i r_0²)a + (1/r_i-q_i/r_0)b = q_i-1.

At admitted exact data the determinant is

    D=(r_1-r_0)(r_2-r_0)(r_2-r_1)(r_0+r_1+r_2)/(r_0 r_1 r_2 f_0).

Reason: subtract q_i times row 0 from rows i of the three-by-three basis matrix
[1,r_i²,1/r_i]; its first column becomes [1,1-q_1,1-q_2], and expanding after replacing
that column by f gives f_0 D. Multiply the original rows by r_i and use the generalized
Vandermonde determinant for [r_i,r_i³,1]. Direct polynomial expansion is an alternative.
Hence D is nonzero for distinct positive radii and finite positive f_0. One ratio alone leaves
a one-parameter ambiguity; three clocks give two independent slope statistics, not one scalar
calibration. No universal noise stability follows: radii can coalesce and f_0 can grow, while
noisy arbitrary q can make D vanish or recovered f fail positivity. L/radii/layout must be
supplied independently; these clock ratios do not select an absolute scale.

Restrict a ray to an equatorial plane by spherical symmetry. With affine tangent define
E=f Tdot>0, J=r² phidot and j=J/E. Nullity gives

    rdot²=E²(1-j² f/r²).

For nonradial J≠0 write u=1/r and h=j^-2-a. Then

    u_phi²=h-u²-bu³,       u_phiphi+u=-(3/2)b u².

For a fixed regular chosen endpoint ray branch, shape depends on b and h; a cancels, while
j=(h+a)^-1/2 changes with a. Existence, branch choice and positive metric are essential and
are not supplied by this cancellation. For static local frames with signed radial direction,

    sin²(alpha) = j² f/r² = (a+u²+bu³)/(a+h),
    cos(alpha) = sign(rdot) sqrt[(h-u²-bu³)/(a+h)].

On a nonturning endpoint, derivative of sin²(alpha) with respect to a at fixed path is
(h-u²-bu³)/(a+h)²>0. A turning endpoint has alpha=π/2 and is blind; a radial ray is a separate
j=0 case and does not have angular sensitivity. Incoming sky direction is opposite to photon
propagation; this sign convention must be disclosed before calling an angle apparent direction.

For increasing phi,

    T_AB = sqrt(h+a) integral_A^B dphi/(a+u²+bu³).

The coordinate duration depends on a even when shape does not. Since u_phi²>=0 implies
u²+bu³<=h, its integrand derivative is strictly negative for a positive length permitted
fixed path (the lapse denominator stays positive). Static proper duration adds a lapse factor,
so no unproved universal monotonicity claim should be inferred. With explicitly instantaneous
direction-reversing relay and static apparatus, the return ray reverses the spatial path and
has the same coordinate duration; source round-trip time is

    τ_round = 2(L/c_E) sqrt(f_A) T_AB.

This is not a generic time-dependent return inverse. Matched flat-layout angle or duration
subtraction is a benchmark comparison, not a native prediction or an asymptotic scattering
angle. Delays at the relay must be zero or independently supplied and accounted for.

## Proposed review attacks and finite check freeze

Attack source/observable orientation, determinant and fit-input counting, radial/turning and
multi-branch restrictions, proper versus coordinate angles/time, absolute scale dependence,
flat matched-layout definition, noisy-data conditioning and stochastic-independence language.
No physical inference, global classification, uniqueness beyond chosen regular branch, horizons,
caustics, flux/EM/matter, nonstationarity or native assembly is covered.

Before parent candidate exposure: independently code exact SymPy determinant/null/tetrad algebra.
Numerical readout independent replay will be frozen after candidate exposure because exact layout
is not yet supplied; it will use a separate method/code and preserve failed checks. CPU one thread,
one scientific subprocess in this reviewer context, FLOAT64 and exact rational algebra; ordinary
capture <=180 seconds/2048 MiB, PYTHONDONTWRITEBYTECODE=1; capture utility is reused unchanged.
No empirical or statistically independent validation follows from synthetic unused observables.
