# External G349 R1--R4 repair-only follow-up

Date: 2026-09-04

## Review boundary

I reviewed only the corrected sealed intake at `/intake`, first authenticated it there, and then
copied the complete tree to `/work/g349_repair_followup_intake`. All claim inspection, executable
replay, and independent reconstruction were performed from that copy. I did not access a
repository or protected package, use the web, download or install anything, edit an evidence file,
choose a physical input, change the question, or continue the research.

The only question decided here is whether the preregistered repairs R1--R4 correctly repair the
mixed transverse-screen-rank-one/ordinary-rank-two stratum while preserving the bounded G349
landing.

## 1. Intake authentication

The authentication chain and physical file set are internally exact:

| Object | SHA-256 / result |
|---|---|
| `REVIEW_SCOPE.json` | `75b6692d7154db7568ceb9ae38b8afae974d57b958f52d5b3da7b568209135b3` |
| `REVIEW_MANIFEST.tsv` | `01e40ce1a5b97f61a1edfafaa468b554304285efba94b746ffe647bb00af7417` |
| `REVIEW_MANIFEST.sha256` file | `1a07d11cb2e5b1ab81aeea2614bf4c26391b8def1c96669c011868ab0fed9727` |
| Detached manifest check | `REVIEW_MANIFEST.tsv: OK` |
| Declared payload count | 37 |
| Physical payload count | 37 |
| Total regular files | 39: 37 payloads, manifest, and detached seal |

The ordered `files` array in `REVIEW_SCOPE.json` equals the ordered manifest path column. The
physical payload paths equal that set exactly. There were no extra payloads, missing payloads, or
unexpected non-regular filesystem objects. Every one of the 37 payloads matched both its declared
byte count and SHA-256. A recursive comparison after all checks found the `/work` copy still
byte-identical to `/intake`.

This authenticates internal sealed consistency. As with the original review, the SHA-256 seal is
unkeyed and has no external trust anchor in the intake; because repository access was prohibited,
authorship and commit chronology beyond the sealed records are not independently certified. That
is an evidence boundary, not an R1--R4 defect.

## 2. Original external finding retained

`EXTERNAL_REVIEW_RESPONSE.md` is byte-exact at the required SHA-256
`aadf46778a28a074550bb039139095ea3ef16a16c3deac1ec9903384334293c1`.
The file still ends in its original caveated G349 verdict and still contains the decisive mixed
caustic/cut counterexample and the required mathematical corrections.

The finding was not erased or recast as a spurious review error. `EXTERNAL_REVIEW_ADJUDICATION.md`
expressly accepts it: null-longitudinal cut variation may restore an ordinary endpoint direction at
a quotient-screen caustic, producing ordinary rank two but a null image plane with zero metric
two-area. `REPAIR_PREREGISTRATION.md`, `REPAIR_EXECUTION_RECORD.md`, `RUN_RECORD.md`, and the
current derivation preserve the same defect and its effect.

## 3. Independent R1 reconstruction

Use signature `(-,+,+,+)` and the preregistered witness

\[
k=(1,0,0,1),\qquad J_v=0,\qquad J_w=(0,0,1,0),
\qquad d\tau(v)=1,\quad d\tau(w)=0.
\]

The endpoint differential is

\[
dF(v)=k,\qquad dF(w)=J_w.
\]

The time--`y` minor of these two columns is one, so they are linearly independent and
`r_F=2`. In the quotient `Q_k=k^\perp/\langle k\rangle`, their classes are zero and the nonzero
screen class `[J_w]`; hence `r_s=1`.

The exact Lorentzian Gram matrix is

\[
\begin{pmatrix}
g(k,k)&g(k,J_w)\\
g(J_w,k)&g(J_w,J_w)
\end{pmatrix}
=
\begin{pmatrix}0&0\\0&1\end{pmatrix},
\]

so the image plane is null-degenerate and its Lorentzian Gram determinant is zero. For an
independent Euclidean auxiliary metric the Gram matrix is `diag(2,1)`, with determinant two. Thus
the ordinary two-plane has positive auxiliary area, but

\[
J_gF=0,\qquad w_g=\sqrt{0/2}=0.
\]

I reproduced these identities with exact rational arithmetic in a package-independent scratch
check at `/work/g349_repair_followup_independent_check.py`; it imported no evidence code.

The complete rank implications also follow directly. Since `dF(TU)` lies in `k^\perp`, projection
to `Q_k` has kernel equal to its intersection with the one-dimensional null line
`span(k)`. Therefore `r_F-r_s` is either zero or one. With a two-dimensional domain:

- `r_s=2` forces `r_F=2`, and the induced plane is spacelike;
- `r_s=1` permits `r_F=1` or `2`, with the rank-two case a null plane;
- `r_s=0` forces `r_F<=1`.

Consequently the repaired definition by the nonnegative quotient-screen/Lorentzian Gram
determinant is positive exactly for `r_s=2` and zero for `r_s<2`.

## 4. Corrected area formula

The repaired derivation correctly introduces an auxiliary Riemannian metric `h` only to invoke the
ordinary area formula. At ordinary-rank-two points it uses

\[
w_g(P)=\frac{\sqrt{\det(g|_P)}}{\sqrt{\det(h|_P)}}\ge 0,
\qquad J_gF=w_gJ_hF.
\]

The weight is positive on spacelike planes and zero on null planes. This produces the valid
weighted formula

\[
\int_UJ_gF\,d\Omega_u
=\int_M\sum_{n\in F^{-1}(y),\ r_F(n)=2}
w_g(dF_nT_nU)\,d\mathcal H_h^2(y).
\]

It is then rewritten using the primary spacelike multiplicity

\[
N_s(F,U;y)=\#\{n\in U:F(n)=y,\ r_s(n)=2\}
\]

as

\[
\mathcal A_{\rm mult}
=\int_UJ_gF\,d\Omega_u
=\int_{F(U)_{\rm sp}}N_s(F,U;y)\,dA_g(y).
\]

This is the correction required by R1. The ordinary critical image `r_F<2` has zero auxiliary
two-measure, while an ordinary-rank-two, screen-critical null sheet may have positive auxiliary
two-measure but contributes zero Lorentzian metric area through `w_g=0`. No stratum is deleted from
the endpoint map. Since the source patch is compact and `J_gF` is continuous and nonnegative, the
multiplicity-weighted metric area is finite; exceptional infinite multiplicities, if any, are
handled in the usual extended-valued multiplicity function without widening the theorem.

## 5. R2 behavioral evidence and replay

The registered aggregate command was run from the copied package exactly in no-write mode:

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_package.py
```

It passed `21/21`. Its nested registered replays freshly returned:

- production: `44321/44321`;
- implementation-distinct route: `14321/14321`;
- hostile route: `22/22` mutations caught.

A digest snapshot of every copied package file before and after the aggregate was identical, and no
`__pycache__` directory appeared. A second comparison against `/intake` also remained exact.

The mixed witness is behavioral in all three repaired routes. Production constructs the specified
zero Jacobi column, nonzero screen column, nonconstant-cut null column, ordinary independence,
positive auxiliary Gram determinant, zero Lorentzian determinant, zero weight, and zero metric
Jacobian. The independent route changes the longitudinal Jacobi pieces and cut derivatives, uses
Gaussian elimination for both ranks and a Euclidean auxiliary metric, and again obtains ordinary
rank two, screen rank one, positive auxiliary area, and zero metric area. The hostile route adds the
twenty-second guard against equating ordinary rank two with positive metric area and evaluates the
explicit null witness.

Some aggregate and hostile checks are documentary token guards. I give them no mathematical
probative weight. The R1 conclusion instead rests on the direct quotient-space argument, exact Gram
calculation, corrected weighted area formula, and independent exact reconstruction above. The
executable totals are reproducibility and regression evidence only.

## 6. R3 documentary scope

`CURRENT_RESEARCH_PROGRAM.md` now uses the exact phrase “geometric endpoint image-union area”; the
former phrase “physical image-union area” is absent from that active program. Its gate keeps the
metric, geodesic, observer, patch, affine cut, and paths supplied.

The repaired analytic and audit documents consistently type the result as geometric metric area of
a supplied endpoint map. They do not derive or select an emitted or detected wave, emission,
absorption, intensity, transfer, brightness, flux, luminosity, probability, detector response,
observational distance, or a physical ray, observer, route, or label population. “Wavefront” remains
only shorthand for the supplied null endpoint map. R3 is satisfied.

## 7. R4 chronology, preservation, and replay integrity

The sealed record retains the relevant chronology rather than replacing it with a success-only
history:

1. The original preregistration is retained byte-exact at its frozen hash and records commit
   `84cb5264`.
2. The first hostile run remains recorded as `20/21`, caused by a prose-dependent cusp hook; the
   behavioral cusp correction and commit `134ecd4a` remain recorded.
3. The original external response remains exact and its mixed-rank counterexample is accepted.
4. R1--R4 were separately frozen in `REPAIR_PREREGISTRATION.md`, with repair-preregistration commit
   `c2967132`, before the recorded repair execution.
5. The repaired result JSON files retain `44321`, `14321`, and `22/22`, empty failure lists, and the
   repair-preregistration identifier. Their bytes and hashes match the sealed manifest.
6. The first repaired aggregate failure before scoring (`KeyError: preregistration_commit`) and the
   second repaired aggregate result `20/21` from a line-wrapped wording hook are both retained in
   `RUN_RECORD.md` and `REPAIR_EXECUTION_RECORD.md`; the eventual `21/21` is not presented as the
   first attempt.
7. The registered final no-write replay is byte-stable and reproduces every repaired result.

The conclusion was not widened during repair. The grade remains locally repaired and pending this
external follow-up in the sealed status documents; the repair changes only rank typing,
zero-weight treatment, multiplicity notation, behavioral coverage, and the geometric scope phrase.

## 8. Retained bounded landing

The unrepaired parts of the landing remain mathematically intact:

- Differentiating `F(n)=gamma_n(tau(n))` gives
  `dF(v)=J_v(tau)+d tau(v) k`. The source-vertex initial conditions, affine geodesicity, the Jacobi
  equation, and curvature symmetries give `g(J_v,k)=0`; with `g(k,k)=0`, all cut-gradient terms
  cancel from the induced Gram form. The cut still changes the endpoint and therefore where the
  Jacobi map is evaluated.
- The corrected multiplicity formula distinguishes sheet area from geometric union area:
  `A_union<=A_mult`, with equality exactly when `N_s=1` for metric-area-almost every spacelike
  regular image point. Isolated transverse intersections need not violate equality; positive-area
  coincident sheets do.
- Rank-one and rank-zero loci, the mixed null stratum, folds, cusps, and repeated images remain in
  the map. The cusp witness still prevents calling every rank-one point a fold.
- Signed sheet integration remains orientation-dependent and distinct from both nonnegative
  quantities. Finite source-observer covariance is restricted to the same intrinsic ray set and
  endpoint assignment, including reciprocal affine-cut renormalization. Path labels remain
  supplied and separate unless a mathematical disjoint-union census is explicitly declared.

No optics or transfer theorem, observational distance, preferred observer or route, physical
population, field equation, history, occupancy, topology selection, stability, matter/mass, scale,
`X_max`, or canon has been imported or selected. The maximum conclusion remains only a conditional
finite metric-area theorem for a supplied endpoint map, with global preimage information required
for geometric union area.

## Finding

No defect remains within R1--R4, and I found no regression in the retained bounded G349 landing.

ACCEPT_G349_R1_R4_REPAIR_FOLLOWUP
