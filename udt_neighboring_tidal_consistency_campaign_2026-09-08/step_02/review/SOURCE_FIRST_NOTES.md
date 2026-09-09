# NT2 source-first independent reconstruction — before author exposure

Reviewer `/root/nt2_review`, fresh separate context, 2026-09-09 UTC.
Baseline `5ece4ae086cc9b0f93a5635867600ad92324d150`, branch grok,
independently checked. Instructions describe Codex/GPT-6, but exact deployed
model ID is unavailable; same/different-model relation UNKNOWN. Different
model, human specialist and formal-proof axes UNTESTED.

Read the bounded startup and shared triggered protocols/CROSS_MODEL_VERIFY,
the new WORK_ORDER and NT2 QUESTION, the entire NT1 candidate, reviewed result
and four controlling reviews. Read G310/G312 owner-adoption records and G312
equation audit; G315 whole exact derivation/audit; G358 original candidate,
whole direct review and banking scope; G348 curvature/Jacobi definitions.
Historical source verdicts, and NT1's conditional verdict/history, are exposed
as required dependency provenance. No author NT2 proof, code, output or result
has been opened. No NT2 findings have been communicated to the author.

Parent owns the shared synchronization and full premise audit; reviewer verified
HEAD/dirt and inspected actual startup_363 PASS receipt (363 rows, exit0,
402.585933seconds), without duplicate full audit or Git mutation as dispatched.
Root tracking changes and protected untracked packages remain untouched. This
does not independently assert present remote freshness or source-suite replay.

## Question, data and bounds

Use only the owner-provisional smooth four-dimensional Lorentzian bounded
vacuum equation Ric=Lambda g with connected constant Lambda, and the stated
Q_abcd=g(R(e_a,e_b)e_c,e_d) convention. At W(p)=0, consider the targeted
nonzero real tensor J=nabla W=nu tensor P, with nu nonzero and P a nonzero
algebraic Weyl tensor. Rank-one factorization is a restriction on supplied
data, not a physical law or general curvature-variation ansatz. Normalization,
coordinates, frame and witness profile are free-and-explored query/data
choices. Signature, regularity, curvature symmetries and original equations
are pinned-by-THEORY relative to the cited adopted/conditional arena.

The question is which causal types/shapes satisfy the FULL finite NT1 Bianchi
conditions, and what actual local metric realizations can be constructed.
Neither a finite passing jet nor a count of free amplitudes proves general
Einstein existence or counts physical modes. No source, carrier, light,
stability, scale, selected universe or physical identification is admitted.

Checks below: exact symbolic/rational CPU calculations, one library thread,
512MiB address space and60seconds CPU/wall per run through the unchanged
shared run_capture.py, absolute owned output stems, unbuffered progress.
No GPU/grid, numerical approximation, production PDE solve, full old suite,
protected/archival input or source mutation. Combined review budget75minutes
from dispatch, and original campaign hard stop03:44UTC; one same-premise
repair/review cycle at most. Preserve failures and do not credit lost output.

## Independent finite argument

The full differential Bianchi condition is nu wedge P=0 in the first
three indices: nu_m P_abcd+nu_a P_bmcd+nu_b P_macd=0. Contracting the
trace-free Weyl identities gives nu^a P_abcd=0. Contract the uncontracted
identity with nu^m; the other terms vanish by that contraction and skewness,
leaving g^-1(nu,nu) P_abcd=0. Since P is nonzero, nu must be null.
This excludes BOTH timelike and spacelike factors without freezing a connection
or any extrinsic datum. W(p)=0 makes the raw/covariant first derivative agree
in any smooth registered frame, but the algebraic argument itself is tensorial.

For null nu choose null coordinates at the tangent space with nu=du and
g=-2du dv+dx^2+dy^2. Rescaling coordinates here is supplied factor/frame
freedom, not metric-selected normalization. The wedge condition implies
every nonzero first skew pair contains u. Pair interchange implies the same
for the second pair. The contraction nu^a P_abcd=0 removes every v index.
Thus only P_uA uB remain, A,B=x,y. Pair symmetry makes this a symmetric
two-by-two screen matrix H; Weyl trace freedom makes tr H=0. Conversely
each real STF H satisfies all algebraic Weyl and differential Bianchi
identities. There are two real entries, with H=0 excluded. This is the
complete restricted finite-factor classification, not a physical polarization law.

Equivalently, P_abcd=nu_a nu_c H_bd-nu_b nu_c H_ad
-nu_a nu_d H_bc+nu_b nu_d H_ac, where H represents an STF form on the
positive two-dimensional null quotient screen. The representation depends
on a screen lift; the resulting tensor has only the displayed null-screen
components and is independent of changes of the lift modulo nu.

## Exact local realization route to check

In the Lambda=0 sector alone, consider the ACTUAL smooth metric

    g=-2du dv+dx^2+dy^2+F du^2,
    F=u [a(x^2-y^2)+2bxy], (a,b)!=(0,0).

The complete inverse has g^uv=-1, g^vv=-F, g^uu=0 and screen identity;
its determinant is -1 and it is Lorentzian. Direct Christoffel calculation
should give Q_uA uB=(1/2)F_AB=u H_AB, H=[[a,b],[b,-a]], and
Ric_uu=-(1/2)(F_xx+F_yy)=0, with all other Ricci entries zero. Thus the
original equation holds on a neighborhood, not merely at p or to first
order. At the origin Q=W=0; since connection action on Q vanishes there,
nabla Q=du tensor P_H. Nonzero H makes curvature nonconstant. Arbitrary
real STF screen amplitudes occur in this construction; no claim for nonzero
Lambda or arbitrary nonfactorized jets is inferred.

For a lawful spacelike seed, introduce t=(u+v)/sqrt2 and
z=(v-u)/sqrt2. Write f=F/2, A=1+f, so

    g=-dt^2+dz^2+dx^2+dy^2+f(dt-dz)^2.

On t=0 restrict to an open neighborhood with A>0. Then gamma=diag(A,1,1)
in (z,x,y), lapse N=A^-1/2, covariant shift beta_z=-f, and future normal
n=(partial_t-beta^z partial_z)/N. Here f_t=-f_z. The original G315 sign
K=-(1/2)L_n gamma gives

    K_zz=-f_z/(2sqrt A), K_zA=-f_A/(2sqrt A), K_AB=0.

These data are induced from the actual metric, not independently guessed
arbitrary seeds. Independently calculate all constraints. Expected identities
for general smooth f(z,x,y) with this K are

    R3+Ktrace^2-|K|^2=-(f_xx+f_yy)/A,
    D_j(K^j_z-delta^j_z Ktrace)=-(f_xx+f_yy)/(2sqrt A),
    D_j(K^j_A-delta^j_A Ktrace)=0.

The chosen f is transverse harmonic, so all four vanish throughout this
local slice. Positivity is open near p because A(p)=1. No boundary or global
completion is imposed; arbitrary small local slices suffice. Exact explicit
metrics avoid reliance on an unproved general smooth PDE existence theorem
for this witness. Any inference to other scalar sectors remains OPEN.

## Planned independent implementation and adversarial phase

Construct a generic symmetric six-by-six bivector form, impose all algebraic
Bianchi/trace-free contractions, then impose nu wedge P for timelike,
spacelike and null representative covectors. This starts from the complete
finite tensor space rather than importing author E/B code. Calculate the full
metric Christoffel/Riemann/Ricci tensors and first derivative at the origin;
separately calculate intrinsic three-metric curvature and all constraints.
Analytic covariance/classification owns arbitrary real covectors/polarizations;
finite exact matrices and symbolic parameters support, not replace, that proof.

Seal source-first notes, script, results, source hashes and real captures
before author exposure. Then examine the whole frozen candidate, signs,
all tensor slots, quotient/lift choices, normal orientation/K convention,
nonzero/positivity domains, actual-neighborhood equations, scope and quantifiers.
Independently recompute saved load-bearing artifacts and execute actual
false-pass corruptions. Same-code reruns are regression only. Return readiness
and seal first; no premature candidate verdict.
