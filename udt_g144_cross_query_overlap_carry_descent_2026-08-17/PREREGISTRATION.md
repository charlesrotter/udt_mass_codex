# G144 preregistration — cross-query overlap carry descent

Date: 2026-08-17

## Whole bounded question

Determine exactly when two supplied calibrated pair queries own a cross-query carry without a new
physical mechanism. Test the hypothesis that the carry is derived when the query realizations are
two charts of the same regular immersed relation on an open overlap, while common observers or
endpoint incidence alone are insufficient.

Let `F_alpha:Sigma_alpha->M` and `F_beta:Sigma_beta->M` be supplied regular calibrated pair
realizations. On open subsets, suppose a calibration-compatible diffeomorphism
`psi_ba:U_alpha->U_beta` obeys `F_beta o psi_ba=F_alpha`. Test whether

```text
J_ba=d psi_ba,
h_alpha=psi_ba^* h_beta,
C_ba=R_beta J_ba R_alpha^-1
```

is the exact cross-query overlap transition, and whether it is metric-isometric rather than a new
positional dilation at the same ambient event.

## Frame and premise ledger

- Method: exact metric/type algebra and explicit immersion countermodel; no fit, dynamics, action,
  path selector, source, or new coefficient.
- `DERIVED_CONDITIONALLY`: pullback naturality, terminal factors, G142 total comparison, G143
  same-query covariance.
- `SUPPLIED/CONDITIONAL`: both pair realizations, regular open overlap, branch choice, embeddings or
  locally invertible immersions, overlap diffeomorphism, and calibration compatibility.
- `OPEN/OMITTED`: selection of either query, proof that arbitrary sheets are one relation, physical
  branch population, nonoverlap transport, self-intersection ambiguity, generic singular/null/cut
  strata, history, `X_max`, proper length, observations, light/EM, action, source, bootstrap, matter,
  mass, and dynamics.

## Preregistered theorem and countermodel tests

1. `F_beta o psi_ba=F_alpha` implies `h_alpha=psi_ba^*h_beta` and `J_ba` supplies the tangent carry.
2. On triple overlaps the differentials satisfy the exact carry cocycle.
3. `C_ba=R_beta J_ba R_alpha^-1` preserves the model Lorentz form.
4. In positive-diagonal upper-triangular `B^+(2)`, Lorentz preservation forces `C_ba=I`; hence a
   genuine same-event overlap transition creates no reciprocal depth.
5. Construct two exact regular timelike strip immersions with the same two observer boundaries but
   different interiors. Prove they have no open image overlap and no induced differential carry.
6. Distinguish embeddings, branch-resolved immersions, and self-intersecting cases.

## Certification and falsification

Production will use exact SymPy algebra for pullback, Lorentz intersection, and the strip witness.
An independent stdlib/Fraction replay must reconstruct the finite claims without production imports.
Falsify or narrow if overlap transitions are nonisometric, `O(1,1) intersect B^+(2)` contains a
nonidentity positive-triangular element, or the endpoint-only witness actually has an open overlap.

Maximum possible conclusion:

```text
GENUINE_OPEN_OVERLAP_OF_TWO_BRANCH_RESOLVED_PAIR_REALIZATIONS_OWNS_CARRY_BY_DPSI__
THE_OVERLAP_TOTAL_TRANSITION_IS_LORENTZ_ISOMETRIC__
IN_POSITIVE_TRIANGULAR_GAUGE_IT_IS_IDENTITY_AND_ADDS_NO_POSITIONAL_DEPTH__
COMMON_OBSERVERS_OR_ENDPOINT_INCIDENCE_ALONE_DO_NOT_OWN_CROSS_QUERY_CARRY__
NONOVERLAP_BRANCH_POPULATION_HISTORY_AND_XMAX_REMAIN_OPEN
```
