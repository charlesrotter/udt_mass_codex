# G190 preregistration — completed-pair time-live frequency/screen join

Date: 2026-08-20

Status: `PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION`

## Whole question

Starting only from:

1. one supplied smooth Lorentzian complete metric `g=E^T eta E`;
2. one supplied regular completed observer-pair family, with the G179--G180 completed-pair
   normalization applied after the full metric pullback;
3. one marked observer event, time orientation, and ruler orientation; and
4. one regular affine null branch generated from the resulting pair plane and meeting the declared
   endpoint observer clock,

determine whether the same metric/query data uniquely produce both:

- the endpoint frequency ratio `Z=omega_s/omega_o`; and
- the finite quotient-screen Jacobi map `D`, hence `d_A^2=|det D|`.

The main target is a finite parametric metric response

```text
lambda -> (Z(lambda), D(lambda), d_A(lambda))
```

and, only on a regular monotone-frequency/noncaustic interval, the descended relation

```text
Z -> d_A(Z).
```

This must be derived without a separately chosen `phi(R)`, P1 chord, `R(Z)`, `X_max`, fitted
coefficient, post-readout orchestra term, or G116 local coefficient decomposition.

## Mode and bounded arena

Mode: `METRIC_LED`, observing rather than targeting.

Let the completed pair metric be

\[
h_s=-T^2(d\tau+B\,ds)^2+T^{-2}ds^2,
\qquad T>0.
\]

At the marked event let `X_0=F_* partial_tau` and `X_s=F_* partial_s`. The derivation must prove or
reject that

\[
U=T^{-1}X_0,
\qquad
N=T(X_s-BX_0)
\]

are an orthonormal clock/ruler pair, and that

\[
\ell_\pm=U\pm N
\]

are the two normalized null directions in the completed pair plane. The ruler orientation chooses
which sign is called outgoing; it may not introduce a continuous path coefficient.

The metric geodesic initial-value problem is then followed on one regular branch. A target clock
must be supplied by the same typed observer-family query at a regular intersection event. If a
smooth clock carry `U(lambda)` along the branch is additionally supplied by that query, derive the
finite frequency evolution law; endpoint frequency requires only the two endpoint clocks.

G188's full matrix quotient-screen Jacobi system is retained without diagonalization.

## Premise and choice ledger

| Item | Tag | Role |
|---|---|---|
| observed `c_E` clock/ruler calibration | `OBSERVED` / `pinned-by-THEORY` | dimension-matched pair coordinates |
| complete metric `g=E^T eta E` | `free-and-explored` supplied history | all base, screen, mixing, and time-live jets remain live |
| completed-pair Dual Reciprocity after full pullback | `WORKING_FOUNDATIONAL_CLARIFICATION` | G176--G180 normalization |
| pair family/germ and marked endpoint clocks | `free-and-explored` supplied typed query | no universal observer population claimed |
| future and ruler orientations | `CHOSE_QUERY` | select one of two null directions and reversal convention |
| affine normalization `-g(U_o,k_o)=1` | `CHOSE_QUERY_CALIBRATION` | fixes null scale and Jacobi vertex units |
| Levi-Civita geodesic, curvature, quotient screen, Jacobi equation | `DERIVED_CONDITIONAL` geometry | evaluators, not dynamics |
| transparent carrier bridge | `OMITTED_FROM_CORE`; optional imported corollary only | may be restated as conditional `d_L=Z^2 d_A` but not derived |
| G116 coefficient decomposition | `SEALED_FROM_DERIVATION` | post-result local regression check only |
| G189 static formula | `SEALED_FROM_DERIVATION` | post-result specialization check only |

No value is `pinned-by-HABIT`.

## Required derivation

1. Prove the completed-pair orthonormality identities
   `g(U,U)=-1`, `g(N,N)=1`, and `g(U,N)=0`.
2. Prove `ell_+` and `ell_-` are null, normalized by `-g(U,ell)=1`, and exhaust the null lines in
   the Lorentzian pair plane.
3. Prove local uniqueness of the affine null geodesic from either normalized initial direction,
   with ruler reversal exchanging the two directions.
4. Derive the endpoint scalar
   \[
   Z=\frac{-g(k_s,U_s)}{-g(k_o,U_o)}
   \]
   and prove invariance under affine rescaling of an already common ray normalization.
5. When a smooth completed clock field is supplied along the ray, derive directly
   \[
   \frac{d\omega}{d\lambda}=-k^ak^b\nabla_aU_b,
   \qquad \omega=-g(U,k),
   \]
   without a G116 decomposition.
6. Join this to the unmodified G188 system
   \[
   \mathcal D''+\mathcal T\mathcal D=0,
   \quad \mathcal D(0)=0,
   \quad \mathcal D'(0)=I,
   \quad d_A^2=|\det\mathcal D|.
   \]
7. Prove that the joint parametric response is fixed on the supplied branch. Prove that an
   ordinary single-valued `d_A(Z)` exists only where `Z` is locally one-to-one and the position
   block is in the declared noncaustic stratum; otherwise retain the branch-parametric object.
8. Recover G189's static result and G116's local result only after the general theorem is frozen.
9. Supply one exact time-live mathematical control in which completed pair clocks, frequency, and
   Jacobi area are all independently reconstructed from the same metric. It is not a proposed
   cosmology.
10. Prove that no P1 screen chord, static `phi(R)`, `X_max`, fitted transfer exponent, or
    post-readout angular correction enters the core system.

## Omitted sectors and limits

Excluded: physical history or observer-population selection; failure or multiplicity of endpoint
intersection; cut/focal/caustic aggregation; source emission and standardized luminosity; native
electromagnetic/radiative transfer; absorption/scattering; observations; global completion;
numerical `X_max`; action; source dynamics; matter; mass; bootstrap; and signalling.

The abstract metric may be fully time dependent and nonspherical. Those sectors are not frozen.

## Certification and falsification contract

- exact symbolic verification of the completed orthonormal/null-frame construction;
- direct coordinate verification of the frequency derivative from the geodesic equation;
- implementation-distinct reconstruction of the exact time-live control;
- exact recovery of the static G189 specialization;
- mutation catches for shift deletion, common-scale deletion, frequency sign reversal, nonaffine
  contamination, Jacobi curvature sign flip, scalarization of the screen matrix, P1 insertion,
  `X_max` insertion, and post-readout angular correction;
- package replay, premise verifier, repository tests, source hashes, and `git diff --check`;
- fresh adversarial review before any high-strength banking.

The candidate is falsified if the pair plane does not determine the stated normalized null lines,
if the frequency law needs a new coefficient, if the screen requires nonmetric carry, if the
static limit fails, or if a single-valued `d_A(Z)` is asserted across a frequency turn or caustic.

## Preregistered landings

One of:

- `COMPLETED_PAIR_TIMELIVE_FREQUENCY_SCREEN_JOINT_EVALUATOR_DERIVED_CONDITIONALLY`;
- `PAIR_NULL_GERM_DERIVED__FREQUENCY_AND_SCREEN_REMAIN_SEPARATELY_QUERY_TYPED`;
- `JOINT_PARAMETRIC_EVALUATOR_DERIVED__DESCENT_TO_DA_OF_Z_REQUIRES_EXTRA_RESTRICTION`;
- `COMPLETED_PAIR_TO_NULL_BRANCH_TYPE_FAILURE`;
- `DERIVATION_OR_CERTIFICATION_FAILURE`.

Compatible qualifications may coexist.

## Maximum conclusion

At most G190 can derive one finite metric-native, completed-pair-conditioned joint evaluator for
frequency and screen area on a supplied regular branch, and show exactly when it descends to a
single-valued frequency-area relation. It cannot select a physical metric history or observer
population, derive radiative transfer, fit SNe/BAO/CMB, determine `X_max`, or establish dynamics,
matter, mass, bootstrap, or signalling.
