# G240 exact derivation — metric null-image cluster census

Date: 2026-08-23

Status: `LOCALLY_VERIFIED_PENDING_FRESH_EXTERNAL_REVIEW`

## 1. Bounded landing

```text
ALL_REGULAR_NULL_IMAGE_QUERY_REMOVES_ARBITRARY_BRANCH_WEIGHTS_CONDITIONALLY
__METRIC_RELATION_INDUCES_IMAGE_INTENSITY_AND_SIBLING_PAIR_MEASURE_ON_A_SUPPLIED_HISTORY
__PHYSICAL_HISTORY_SOURCE_MEASURE_TRANSFER_CRITICAL_STRATA_AND_OBSERVATIONAL_ANCHOR_OPEN
```

This is a regular-stratum measure theorem. No observational outcome, profile, feature, scale,
coefficient, P1, `X_max`, or protected work enters.

## 2. Typed geometric input

Supply:

1. a smooth time-oriented Lorentzian history `(M,g)`;
2. one observer event `o` and calibrated observer sky `O`;
3. a measurable parent/source-event space `X` with intensity measure `mu` and incidence map into
   spacetime;
4. the query: enumerate **every regular past-null branch** satisfying the source/observer incidence.

For each parent `x`, let `B_x` be the finite fiber of regular null **branch objects**. A branch has an
observed sky coordinate

\[
\psi_x:B_x\longrightarrow O.
\]

Distinct branches remain distinct even if their observed coordinates coincide. Define the image
counting measure

\[
C_x=\sum_{b\in B_x}\delta_{\psi_x(b)}.
\]

No numerical branch weight has been supplied. Unit multiplicity follows from the chosen instruction
to count each regular image once. The branch set and sky map are metric-derived only **after** the
history, incidence, and query are supplied.

## 3. Point-process theorem

Let the parent events form a Poisson random measure `Pi` on `X` with intensity `mu`. The observed
image counting measure is the deterministic-cluster pushforward

\[
Y=\sum_{x\in\Pi} C_x.
\]

For a measurable sky set `A`, Campbell's identity gives

\[
\boxed{
\nu_1(A)=\mathbb E[Y(A)]
=\int_X C_x(A)\,\mu(dx).
}
\]

For measurable `A,B`, the ordered-distinct factorial pair count is

\[
Y^{[2]}(A\times B)
=\sum_{(x,b)\ne(x',c)}
1_A(\psi_x(b))1_B(\psi_{x'}(c)).
\]

Split this sum into `x != x'` and `x=x', b != c`. Poisson factorization of **distinct parents** gives

\[
\mathbb E\!\left[
\sum_{x\ne x'}C_x(A)C_{x'}(B)
\right]
=\nu_1(A)\nu_1(B).
\]

The same-parent term is

\[
\Sigma_{\rm sib}(A\times B)
=\int_X
\sum_{\substack{b,c\in B_x\\b\ne c}}
1_A(\psi_x(b))1_B(\psi_x(c))\,\mu(dx).
\]

Therefore

\[
\boxed{
\nu_2=\nu_1\otimes\nu_1+\Sigma_{\rm sib}.
}
\]

This is the exact bridge from the supplied metric relation to G239. It proves neither a Poisson
source law nor a physical all-image detection protocol.

## 4. Multiplicity and the zero/nonzero boundary

Let `m(x)=|B_x|`. The total ordered sibling mass is

\[
\boxed{
S=\Sigma_{\rm sib}(O\times O)
=\int_X m(x)[m(x)-1]\,\mu(dx).
}
\]

Hence:

- if `m(x)<=1` almost everywhere, then `Sigma_sib=0`;
- if `m(x)>=2` on a set of positive `mu` measure, then `S>0`.

The second statement is about total sibling mass. A particular angular bin can still receive zero
sibling contribution.

The metric has not “chosen weights.” It has determined a finite branch fiber. Counting every branch
once converts that fiber into a canonical counting measure for this query.

## 5. Exact G239 normalization

Let

\[
N=\nu_1(O),\qquad P=\nu_1/N.
\]

The total ordered pair mass is `N^2+S`, so

\[
\bar\nu_2=\frac{\nu_1\otimes\nu_1+\Sigma_{\rm sib}}{N^2+S}.
\]

Subtracting `P tensor P` gives

\[
\boxed{
\Gamma_{\rm sib}
=\frac{\Sigma_{\rm sib}}{N^2+S}
-\frac{S}{N^2+S}P\otimes P.
}
\]

The compensating second term is required by normalization. The exact one-parent/two-image control
reproduces

\[
\Gamma=\begin{pmatrix}
-1/12&1/12\\
1/12&-1/12
\end{pmatrix}.
\]

## 6. Coordinate and label behavior

Branch relabeling changes no sum. A measurable source reparameterization pushes `mu`, incidence,
and the branch family together and leaves the resulting measure unchanged. A sky-coordinate change
pushes `C_x`, `nu_1`, `Sigma_sib`, and `Gamma` covariantly. Thus the construction is not tied to the
finite cell labels used for exact verification.

Where a regular branch map is locally invertible, the density form contains its Jacobian. This is
not an added image weight: it is the coordinate density of the invariant pushforward measure.

## 7. Critical and global strata

The theorem assumes a measurable, locally finite, proper regular-image relation. It does not erase
the difficult strata:

- at a caustic, a density formula using an inverse Jacobian can fail even when the pushforward
  measure remains defined;
- branch merger requires a multiplicity convention beyond the regular census;
- a symmetric ring or nonproper relation can have non-discrete fibers;
- infinitely many images require local finiteness/integrability;
- coherent wave interference is not a point-image counting problem.

These cases are `OPEN`, not classified as failures.

## 8. What freedom was removed—and what was not

Removed conditionally:

- arbitrary numerical branch weights in G239, for the all-regular-image query;
- a separate sibling-pair ansatz: `Sigma_sib` is induced by metric branch multiplicity;
- a preferred-branch selector: all regular branches are retained.

Still supplied or open:

- which complete metric history is physical;
- the observer/source incidence domain;
- the physical source intensity and correlations;
- whether all images are detected or weighted by transfer;
- caustic, infinite-image, and wave-optical completion;
- any observational anchor and all BOSS outcomes.

Thus G240 narrows the population gap without pretending to close the history or source-law gap.

## 9. Completeness/anti-imposition ledger

This is one regular query tile:

| Criterion | Covered | Dropped/open |
|---|---|---|
| fields/history | supplied complete metric evaluated | no history equation/selection |
| action/equations | none imported | action/dynamics open |
| domain | full locally finite regular branch fiber for declared incidence | other incidence domains open |
| boundary/critical set | regular stratum characterized | caustics/nonproper fibers open |
| topology/branches | every regular branch counted | infinite/continuous fibers open |
| dynamics | time-dependent history allowed if supplied | no physical evolution law |
| population | Poisson parent control evaluated | physical source law open |
| regime | point-image factorial moments | transfer/coherence/detection open |

No acceptance criterion filters images for producing a desired shape. The only branch restriction is
the preregistered mathematical regularity/local-finiteness scope.
