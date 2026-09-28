# FSL1 source-first adversarial reconstruction

Sealed 2026-09-28 before exposure to an FSL1 candidate, code, outputs or verdict.
Reviewer: `/root/fsl1_review`, separate fresh scoped context, inherited Codex runtime;
exact model identifier unavailable. Different-model independence is UNKNOWN, not
claimed. Independent argument and dependency-free exact-rational implementation
are present; no claim of formal proof assistant, human, or observational review.

## Scope, startup and exposure

Parent startup attributed, not replayed: synchronization succeeded on `grok`,
HEAD and origin/grok `f79094c07d7260877ba80005e857294bfebdc670`, tracked clean,
52 unrelated/protected untracked paths preserved, bounded startup chain read and
orientation given. I independently read AGENTS and relevant CLAUDE sections,
verifier-before-record, CROSS_MODEL_VERIFY, no-shortcuts and completeness-map;
verified current branch, HEAD and origin/grok; and checked every LAUNCH source
hash. I did not inspect protected payloads or mutate git. All written artifacts
are confined to this review directory.

Read WORK_ORDER and LAUNCH; founding W4/W5 and sections 6--7; current program
lines 1--88; G274 and G176 audit reports; CRD1 reviewed result and source sections
1,3. Parent then identified earlier transport sources: I read G274 source
manifest and G269/G272/G273 exact derivations before sealing. Historical adoption
wording there is overlaid by current W5. I have not read their code, raw arrays,
external review texts, or complete historical packages. Entire files were hashed
where needed without reading unassigned content into context. Source hashes are
in `source_first_result_corrected.json`.

Question: for any supplied smooth time-oriented Lorentz metric, regular affine
null branch and proper-time endpoint clocks, which clock factors and composition
follow, and what does projective pair position determine? Metric/path/observers/
frame choices are free-and-explored query data; local metric coupling inherits
W4 WORKING/POSIT. Signature (-+++) and c_E=1 are conventions. Ideal null tick
correspondence is conditional. No field equation or microscopic light theory is
assumed, and no physical W5 arrow is automatically identified with transport.

Checks use one CPU process, exact Fraction arithmetic, no grids/GPU/numerical
approximation, <=60 seconds and 512 MiB per run, existing capture helper and
absolute output prefixes. Maximum conclusion is conditional geometry/matching,
not native physical query selection, cosmological law or canon. Stop before any
unsupported physical join. Analytic reasoning is general evidence; finite exact
checks test examples and named wrong formulas, not completeness.

## Independent general argument

Let E_A,E_B be future orthonormal tetrads with timelike legs the endpoint clocks,
and let P be metric parallel transport along the supplied affine null ray. Define
L=E_B^{-1} P E_A. This is a proper orthochronous Lorentz map for compatible oriented
frames. For a future source direction n with |n|=1, write k_A=omega_A E_A(1,n).
Then

    a(L,n)=(L(1,n))^0 > 0,
    omega_B/omega_A=a(L,n),
    n_B=spatial(L(1,n))/a(L,n),
    r_AB=d tau_B/d tau_A=1/a(L,n),
    delta_AB=log a(L,n)=-log r_AB.

The received tick relation follows from a regular null family, not from the
Lorentz matrix alone. If J varies the null geodesic family, [k,J]=0 and affine
geodesicity give d[g(k,J)]/d lambda = (1/2)J[g(k,k)]=0. At the endpoints J is the
proper clock tangent times the endpoint proper-time variation, modulo a multiple
of k for moving affine limits, which does not change the contraction. Therefore
omega_A d tau_A=omega_B d tau_B. This is the differential inter-tick limit at
finite separation. A finite emitted interval instead obeys
Delta tau_B=integral r_AB(tau_A) d tau_A; one sample r need not equal its average.

For two subdivisions of the SAME ray,

    a(L2 L1,n)=a(L2,n_B) a(L1,n),
    r_AC=r_AB r_BC,   delta_AC=delta_AB+delta_BC,

where the middle observer and its normalized ray are the same in both factors.
This is a cocycle on carried rays, not an endpoint scalar law from arbitrary
independent experiments. Re-emission can introduce a different ray/frequency
normalization. Algebraic reversal uses the inverse map and corresponding reverse
query; a later causal return is a different experiment. Path independence and
trivial holonomy are extra restrictions. Composition implies none of them.

These are standard Lorentz/transport/first-variation identities, and much of this
clock construction is already owned by G220/G269. FSL1 must not call their
recovery a new native physical law.

## What projective position determines

For c=L e0=(gamma,gamma chi), gamma=(1-|chi|^2)^(-1/2). The source-direction
frequency factor uses the TIME ROW of L. A clock COLUMN is not that row: L and
L R for a spatial source-frame rotation R share c but need not share a(L,n).
Thus chi alone, or chi plus an uncarried fixed source direction, cannot determine
the received factor in a fixed chart. This is consistent with G274's full-carry
requirement. A passive gauge rotation also transforms n and leaves the physical
answer unchanged; changing L while holding n fixed here is the separator.

There is an equivalent receiver-direction formula. Metricity gives
-g(c,L(1,n))=1, so with the ACTUAL received n_B,

    r_AB=gamma (1-chi dot n_B).

Thus chi plus the appropriate measured/carried target direction does determine
this supplied-query factor. This does not infer that direction, complete frame
carry, a physical branch, or a distance law from chi. It also uses the explicitly
defined arrow convention; the transported-source-frame convention in G269/G273
has the opposite clock/arrow ordering.

A one-dimensional boost of signed parameter d gives a=e^d for the plus null
ray, a=e^-d for the minus ray. Accordingly the matching reciprocal depth is
respectively delta=d or delta=-d. For a generic supplied G176 terminal pair,
its coefficient Phi=-log T is not automatically this integrated clock depth
(CRD1 section 3). A matching claim requires the same physical comparison,
orientation and calibration, with delta_pair=log a; algebraically defining a
new number by that equality is not construction of the pair. G269/G272 already
own the sharp screen-planarity condition for equality of rapidity magnitude
and |delta|. They must retain priority.

## Explicit boundary implication available for an FSL1 return

For fixed chi magnitude rho=tanh eta, the allowed interval ratios over target
ray directions satisfy e^-eta <= r <= e^eta. Thus rho->1 opens an ever wider
range; it does NOT require received slowing or r->infinity. A continuous exact
G269-family specialization in flat space is

    U_A=(1,0,0,0), k=(1,1,0,0),
    U_B=(1+w^2/2,w^2/2,w,0), w>=0.

It is future unit timelike; omega_A=omega_B=1; r=1 for every w; and transported
rapidity gamma=1+w^2/2 diverges so rho^2=1-gamma^-2 ->1. This directly realizes
the asymptotic consequence latent in G269's fixed-r screen family. It is not a
new physical countermodel admitted by UDT dynamics; it proves that the supplied
geometric premises plus projective boundedness alone do not yield the owner's
universal slowing asymptote. A native result requires actual population/ray/
geometry conditions which exclude or control this freedom. A planar match can
recover the intended asymptote conditionally, with orientation/sign retained.

## Actual checks, repairs and omissions

`source_first_check.py` imports only the Python standard library. Its 53 exact
assertions include four Lorentz-metric checks, same-ray composition, rejection
of a fixed-uncarried-direction multiplication, a same-column/different-row
separator, 16 receiver-direction identities, opposite planar ray factors,
three exact unit-clock/no-redshift boundary examples, all 20 LAUNCH hashes and
three G274 historical source hash matches. These are transparent finite exact
checks, not a general algebra proof or source-grade upgrade.

Concrete outcomes: carried composition frequency factor 17/6; using the original
direction again gives 10/3 and is rejected. Two arrows with identical clock
columns yield source-ray frequency factors 3 and 5/3. Planar opposite-ray factors
are 3 and 1/3. At w=1,10,100, rho^2 is respectively 5/9,2600/2601,
25010000/25010001 while r remains exactly 1.

Capture records: `source_first.json` and `source_first_corrected.json`, each exit
0, about 0.03 seconds, <17 MiB maximum RSS, under declared limits. The first
run's summary recorder accidentally reused the final loop ray when printing
`wrong_direction`; its assertions used the correct ray and passed. I preserved
the initial script as `source_first_check_initial.py`, initial JSON/stdout/stderr,
corrected only the recorder to retain ray_y, and reran all checks. The corrected
result and capture are controlling; this is a packaging repair, not science.

Not performed: full source-package replay, full premise verifier (assigned to
parent closure), candidate review (not yet exposed), observational test, numerical
transport integration, field-equation construction, independent model or human
review. The two explicit wrong-rule separators are analytic/exact counterchecks,
not a newly installed regression harness with a general mutation score.

## Source-first verdict

The general finite-separation null-clock readout and carried-ray cocycle are
mathematically sound conditional constructions. W5 alone does not supply missing
ray/transport/population/history data. Previously established G269/G272 planarity
and screen distinctions survive. The explicit nonradial boundary implication
must constrain any claim of a universal positional-redshift asymptote. No verdict
on an unseen FSL1 candidate is issued. Source-first stage is complete and sealed;
direct candidate review may now begin.
