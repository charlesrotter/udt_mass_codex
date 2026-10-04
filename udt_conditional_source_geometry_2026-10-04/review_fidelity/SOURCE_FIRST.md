# CGE1 source-first fidelity review

Reviewer: `/root/cge_fidelity`, actual separate context, 2026-10-04.
Model/runtime: Codex agent; exact model identifier is not exposed in this context.
No different-model or human review is claimed. Parent attribution: continuing
session startup synchronized at `cdc94b5d1703d99230afaee632f47376645f5585`,
ACP1 full406 and current normal premise checks reported by parent, not replayed
here. I independently checked local branch `grok`, HEAD and `origin/grok` equal
that hash, and inspected status: no tracked changes when read; existing
untracked paths plus this package. No protected payload was opened or hashed.
Remote fetch/pull is parent-attributed, not independently repeated.

## Exposure and axes

Before this record/checker: task dispatch, AGENTS, WORK_ORDER, BASELINE, bounded
central R2/R6/R8ACP/R9/R10/R13 and relevant owner definitions, current exact
G01/G02/G05/G06/G220/G301/G310/G312/G348 rows, cited FSL1/ACP1 repairs and the
sources in SOURCE_HASHES.json. No parent CGE1 candidate, proof, code, results,
reviewer verdict, or other new reviewer output has been read. Repository method
files were read as methods, not premises. Complete source files are hashed for
version binding even where reading was bounded to the named sections.

Fresh context: yes. Source-first argument: yes. Independent implementation:
coordinate-Christoffel/Ricci construction and exact symbolic endpoint checks,
without parent imports. Different model: unknown/unclaimed. Premise independence:
no; this uses the same declared conditional sources. Full historical source
replay, physical confirmation, full registry replay and human review: not done.

## Classification and owner fidelity

The work order is correctly framed as exploration inside the retained R10
conditional branch. GR FILTER ONLY does not itself impose Ric=Lambda g.
DDR and Local Metric Sufficiency remain owner-provisional, not absent premises;
their full G301 class-membership join remains unclosed. R10's entire response
class and nonzero Ricci coefficient are needed before the Einstein implication.
Neither covariance alone, quiet GR overlap, a retained action, nor an exact
solution of the resulting equation supplies that native join.

R2 supplies the reciprocal static areal form only after symmetry and chart are
declared. It does not choose phi(r), a cosmic center, or a source. Solving the
conditional exterior equation in that form legitimately gives

    ds²=-f dt²+dr²/f+r²dOmega²,
    f=1-2m/r-Lambda r²/3,  c_E=1 in length-time units.

The integration constant m has length dimension. Its identification with
G_obs M/c_E² is a conventional external-model/source input, not matter emergence
or a native mass law. The source interior and its matching remain excluded.
The MASS_BRANCH_AUTHORITY_MAP supplies no alternative source ownership here.

The full metric is required for source and null motion; deleting the sphere
would discard the circular clock and angular records. Work only on a connected
regular static region f>0, r>0 and regular sphere charts. r=0 is not a clock
location for m!=0. f=0 is the limit of this presentation, not physical X_max.
A regular exterior does not prove a globally regular source interior.

Owner clarification retains ordinary local proper clocks, actual received ticks,
one geometry, and an additional positional requirement with no prescribed
factorization. A standard conditional Einstein exterior does not establish that
additional native effect, select Lambda, or prove all UDT premises insufficient.
Free query data are legitimate; they are not themselves a missing-law theorem.

## Independent reconstruction before exposure

For an equatorial circular geodesic at r=a, let

    Omega²=m/a³-Lambda/3, U^t=(1-3m/a)^(-1/2),
    U^phi=Omega U^t.

Require f(a)>0, 1-3m/a>0 and Omega²>0 for a genuinely orbiting future timelike
clock. Omega²=0 is a stationary degeneracy requiring separate wording. These
conditions show regularity and geodesicity, not orbital stability. The sign of
Omega is a supplied orientation. Source cadence/readout remains conditional.

At radial free reception R, write u=(e/f_R,v,0,0), e>0, e²-v²=f_R>0.
For a photon with E>0, impact b=L/E and radial sign epsilon, put
q=sqrt(1-f b²/r²)>0. Direct contraction gives

    omega_e=E U^t(1-b Omega),
    omega_o=E(e-epsilon v q_R)/f_R,
    Z=f_R U^t(1-b Omega)/(e-epsilon v q_R).

All factors must belong to one actual regular incidence, not independently chosen
endpoint labels. For outward b=0 this reduces to Z=U^t(e+v). It also follows
independently from actual arrival variation: at a radial base ray,
T_b=0, T_R=1/f_R, and Phi_b=integral_a^R dr/r²=1/a-1/R. The angular equation
chooses the neighboring b to compensate the circular source's changing phase;
the time equation gives (e-v)Z/f_R=U^t. Thus the differential interpretation
does not freeze b=0 for every neighboring emission from an orbiting clock.

For every target Z*>0 and any supplied static exterior with such a source and
R>a on the same f>0 component, set s=Z*/U^t and

    e=(s+f_R/s)/2, v=(s-f_R/s)/2.

Then e>0, e²-v²=f_R and Z=Z*. Smooth geodesic existence realizes this timelike
receiver initial state locally; the radial ray is assigned its reception event
and source phase. This establishes one-shift nonidentifiability with free
receiver preparation. It does not fix all records, prove broad observational
degeneracy, select this physical receiver, or exclude inference with extra data.

An outward orthonormal radial receiver axis is E_r=(v/f_R,e,0,0).
On the equator use E_phi=(0,0,0,1/R). The *sky* direction is minus propagation:

    n_sky^r=(v-epsilon e q_R)/(e-epsilon v q_R),
    n_sky^phi=-f_R b/[R(e-epsilon v q_R)].

The squared sum is one; radial outward reception has n_sky^r=-1. This is a
finite direction readout, not a proof that the full angular map is a scalar
distance. ACP1's complete-map/similarity gate, affine normalization and screen
sign conventions remain required for comparison to actual spot geometry.

Static observers at distinct fixed radii would instead measure lapse ratios
whose reverse products are one. This stationary-clock limitation survives but
does not apply to freely moving receiver histories by substitution. Circular
timelike clocks and their neighboring connecting rays remove no native gap.

## Frozen independent check scope

Before executing `source_checks.py`, freeze this text, script and source hashes.
Question: do the above exact conditional identities satisfy the full original
coordinate equations and permit the declared one-shift degeneracy? Frame:
metric-led *within the supplied conditional class*. Symmetry, m, Lambda, orbit,
receiver state and source/ray incidence are free-and-explored restrictions;
the geometry and clock contractions follow from the stated conditional metric
interface. No physical value is pinned-by-HABIT or claimed native.

CPU only, one process, one BLAS thread, 2 GiB address-space hard limit, no GPU,
grid, optimization, empirical fit or timeout. Exact SymPy arithmetic; no floating
precision levels required. At most twelve finite cases: six radial cases with
m=1,a=10,R=30, Lambda in {-1/100000,0,1/100000}, target Z in {3/4,4/3}; six
nonradial endpoint checks with b=+/-2, the same three Lambda, v=1/5, E=1.
Symbolic identities supplement this finite inventory. Failures stop the checker
and must be preserved; no tolerance loosening. No stability, source interior,
global completeness, Jacobi-map integration, full source estimator replay or
full candidate-implementation certification is attempted here. Maximum result:
source-fidelity boundaries and checked conditional algebra, pending exposed
candidate and final integration review.
