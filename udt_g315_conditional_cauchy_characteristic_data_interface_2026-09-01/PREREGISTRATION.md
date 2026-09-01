# G315 preregistration — conditional Cauchy and characteristic data interface

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_DERIVATION_OR_OUTCOME_FILES`

## Whole bounded question

For the active bounded equation

\[
R_{ab}=\Lambda g_{ab},\qquad d\Lambda=0,
\]

classify:

1. the exact constraints on regular spacelike initial data;
2. the distinction between physical data and lapse/shift/coordinate gauge;
3. the local functional freedom left after constraints and diffeomorphism;
4. the exact metric variables propagated by the equation;
5. the universal null constraint visible on a regular characteristic hypersurface;
6. what is freely supplied versus transported in an intersecting-null presentation;
7. whether `Lambda` is visible in same-null focusing or only in non-null/mixed projections;
8. whether the reciprocal pair evaluator adds an independent initial-data or evolution residual.

This is a conditional-data interface map, not a unique-universe, cosmology, or observational fit.

## Preregistered spacelike identities

With induced metric `gamma_ij`, unit normal `n`, second fundamental form `K_ij`, spatial derivative
`D`, and the convention `K_ij=-(1/2)L_n gamma_ij`, test

\[
\mathcal H={}^{(3)}R+K^2-K_{ij}K^{ij}=2\Lambda,
\]

\[
\mathcal M^i=D_j(K^{ij}-\gamma^{ij}K)=0.
\]

For `K_ij=A_ij+(tau/3)gamma_ij`, `A^i_i=0`, test the equivalent split

\[
{}^{(3)}R+\frac23\tau^2-A_{ij}A^{ij}=2\Lambda,
\qquad
D_jA^{ij}-\frac23D^i\tau=0.
\]

Test the full metric evolution presentation

\[
(\partial_t-\mathcal L_\beta)\gamma_{ij}=-2N K_{ij},
\]

\[
(\partial_t-\mathcal L_\beta)K_{ij}
=-D_iD_jN+N\left({}^{(3)}R_{ij}+K K_{ij}-2K_i{}^kK_{kj}-\Lambda\gamma_{ij}\right).
\]

`N` and `beta` are preregistered as free gauge presentation, not selected physics. The generic local
count `12 - 4 constraints - 4 coordinate freedoms = 4 phase-space functions` may be reported only
as a principal/generic count, not a global parameterization theorem.

## Preregistered characteristic identities

On a twist-free null hypersurface with affinely parametrized generator `ell`, screen metric `q_AB`,
null second fundamental form `chi_AB=(1/2)L_ell q_AB`, expansion `theta=q^AB chi_AB`, and shear
`sigma_AB=chi_AB-(theta/2)q_AB`, test

\[
\mathcal L_\ell\theta=-\frac12\theta^2-\sigma_{AB}\sigma^{AB},
\]

because

\[
R_{ab}\ell^a\ell^b=\Lambda g_{ab}\ell^a\ell^b=0.
\]

For cross-normalized null normals `g(ell,k)=-1`, also test

\[
R_{ab}\ell^a k^b=-\Lambda.
\]

The maximum characteristic conclusion is typed: conformal screen/shear data and compatible corner
data may be supplied, while expansion and remaining connection variables obey a transport/constraint
hierarchy. No claim of a formalism-independent minimal list or global caustic-free development is
permitted.

## Registered exact witnesses

The spacelike constraints and evolution signs must be checked against at least:

- the round positive bounce: `R3=6/X^2`, `K_ij=0`, `Lambda=3/X^2`;
- the flat positive slicing: `R3=0`, `K_ij=-H gamma_ij`, `Lambda=3H^2`;
- the time-symmetric positive product slice: `R3=2Lambda`, `K_ij=0`;
- the G313 Berger-`S3` data: `R3=7/2`, `K_ij=h gamma_ij`, `h^2=5/12`, `Lambda=3`.

These are equation and sign controls, not a physical population or exhaustive data census.

## Certification and falsification contract

Production must derive the registered identities without importing a field equation beyond the
active bounded G312/G313 result. An implementation-distinct standard-library verifier must rebuild
the algebra and witness checks without importing production functions or result files. Hostile
mutations must catch at least:

- wrong sign of `Lambda` in the Hamiltonian or evolution equation;
- treating lapse or shift as physical data selected by UDT;
- erasing the momentum constraint;
- calling four phase-space functions four configuration degrees of freedom;
- claiming all seed data solve the constraints;
- inserting `Lambda` into same-null Raychaudhuri focusing;
- declaring a single null sheet a complete characteristic data set;
- turning local conditional propagation into global completeness or one selected history;
- calling the pair kernel an independent evolution equation;
- importing a source, matter, action, observation, scale, physical `X_max`, or protected work.

Run the full premise verifier and repository tests before banking. A fresh external adversarial
review is required before any externally accepted grade.

## Preregistered landing classes

Exactly one maximum landing may be used:

1. `ACTIVE_EQUATION_HAS_A_LAWFUL_CONDITIONAL_DATA_INTERFACE__CAUCHY_AND_CHARACTERISTIC_DATA_REMAIN_FREELY_SUPPLIED_WITH_DERIVED_CONSTRAINTS`
2. `ACTIVE_EQUATION_SELECTS_A_UNIQUE_LAWFUL_INITIAL_DATA_CLASS`
3. `ACTIVE_EQUATION_FAILS_LOCAL_CONSTRAINT_PROPAGATION`
4. `CLASSIFICATION_INCONCLUSIVE_WITHIN_REGISTERED_LOCAL_SCOPE`

No landing changes the metric, reciprocal kernel, angular cancellation, observational interface,
or premise grades.
