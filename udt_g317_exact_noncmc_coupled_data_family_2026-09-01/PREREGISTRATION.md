# G317 preregistration — exact coupled non-CMC data family

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_OUTCOME_SCRIPTS_OR_RESULTS`

## Whole bounded question

For the G316 conformal equations

\[
-8\bar\Delta\psi+\bar R\psi
-|\bar A_{TT}+\bar L W|^2\psi^{-7}
+\left(\frac23\tau^2-2\Lambda\right)\psi^5=0,
\]

\[
\bar D_j(\bar L W)^{ij}=\frac23\psi^6\bar D^i\tau,
\]

classify all solutions in the registered constant-`psi`, flat-torus, diagonal-TT,
one-coordinate non-CMC ansatz. Reconstruct the physical data and determine whether the admitted
family has zero or nonzero initial Weyl tide. Do not select a member or widen the ansatz.

## Registered ansatz and ownership

On a marked flat `T^3` with dimensionless `2 pi` periodic coordinates `(x,y,z)`, choose

\[
\bar\gamma_{ij}=\delta_{ij},\qquad \psi=p>0,
\]

\[
\tau=\tau(x),\qquad \tau(x+2\pi)=\tau(x),\qquad \tau'\not\equiv0,
\]

\[
\bar A_{TT}^{ij}=\operatorname{diag}(\alpha,\beta,\gamma),
\qquad \alpha+\beta+\gamma=0,
\]

\[
W=w(x)\,\partial_x.
\]

This entire ansatz is a chosen mathematical diagnostic slice. `tau` is free and explored through
arbitrary finite Fourier data and exact abstract mean/value identities. `p` and the surviving
transverse constant are free parameters. None is observed, fitted, or UDT-selected.

For this vector field,

\[
(\bar L W)^{ij}
=\operatorname{diag}\left(\frac43w',-\frac23w',-\frac23w'\right),
\qquad
\bar D_j(\bar L W)^{xj}=\frac43w''.
\]

Let

\[
\mu=\frac1{2\pi}\int_0^{2\pi}\tau(x)\,dx,
\qquad
d=\frac{\beta-\gamma}{2}.
\]

## Preregistered vector classification

The vector equation is to be tested as

\[
2w''=p^6\tau'.
\]

Periodicity preregisters the candidate integrated family

\[
w'=\frac{p^6}{2}(\tau-\mu),
\]

with `w` unique only modulo an additive translation/conformal-Killing constant. The zero-mean
condition on `tau-mu` is the periodic integrability condition, not a physical normalization.

## Preregistered scalar classification

Substitute the vector solution into the scalar equation. Before imposing any result, the
preregistered reduced residual divided by `p^5` is

\[
\mathcal F(x)=
\left(\frac43\mu-2\alpha p^{-6}\right)\tau(x)
-\frac23\mu^2+2\alpha p^{-6}\mu
-\left(\alpha^2+\beta^2+\gamma^2\right)p^{-12}
-2\Lambda.
\]

Because `tau` is nonconstant, test whether pointwise vanishing is equivalent to

\[
\alpha=\frac23p^6\mu,
\qquad
\Lambda=-d^2p^{-12}.
\]

Define the candidate physical transverse constant

\[
q=d\,p^{-6}.
\]

The classification must report necessity and sufficiency only inside the registered ansatz. The
`q=0` and `q\ne0` branches must both remain visible. A negative `Lambda` relation in this family
must not be promoted beyond it or confused with G304's separately bounded static positive branch.

## Preregistered direct physical reconstruction

If the candidate conditions hold, reconstruct and independently test

\[
\gamma_{ij}=p^4\delta_{ij},
\qquad
K^i{}_j=\operatorname{diag}(\tau(x),q,-q),
\qquad
\Lambda=-q^2.
\]

The direct physical constraints are

\[
{}^{(3)}R+K^2-K_{ij}K^{ij}=2\Lambda,
\qquad
D_j(K^{ij}-\gamma^{ij}K)=0.
\]

Their exact satisfaction is required independently of conformal-form cancellation. Nonconstant
`tau` must make the vector source and longitudinal correction nonzero for at least one registered
profile; otherwise the “coupled” claim fails.

## Preregistered tide diagnostic

For an Einstein development, compute the initial electric Weyl tensor from

\[
E^i{}_j={}^{(3)}R^i{}_j+K K^i{}_j-K^i{}_kK^k{}_j
-\frac23\Lambda\delta^i{}_j.
\]

Test the candidate eigenvalues

\[
E^i{}_j=operatorname{diag}
\left(\frac23q^2,\ \tau q-\frac13q^2,\ -\tau q-\frac13q^2\right).
\]

Also test the magnetic Weyl curl from the registered one-coordinate diagonal data. The result must
distinguish:

- `q=0`, where the initial Weyl data may vanish and local flatness is at most conditional on the
  already-caveated uniqueness theorem;
- `q!=0`, where the nonzero `E_x^x` supplies an invariant tidal witness.

This diagnostic characterizes geometry. It does not assign matter, mass, population, or
observational meaning.

## Solution-space and nonpromotion audit

The result must retain:

- arbitrary smooth periodic nonconstant `tau(x)` within the ansatz;
- the free marked-slice size parameter `p`;
- the continuous `q` family, with `q` and `-q` tested under the `y<->z` axis relabelling;
- additive conformal-Killing freedom in `w`;
- separate zero-tide and tidal subclasses;
- omitted nonconstant-`psi`, nonflat, nondiagonal, boundary, and global-completion sectors.

No acceptance test may prefer smooth shape, a sign, a scale, a topology, or a desired physical
interpretation. Smoothness and periodicity define the bounded function space; Fourier examples are
coverage witnesses, not fitted profiles.

## Certification and falsification contract

Production must derive the vector integration, reduced scalar residual, necessary/sufficient
coefficient conditions, physical reconstruction, direct constraints, and Weyl classification. An
implementation-distinct standard-library verifier must rebuild the load-bearing algebra without
importing production functions or reading production results. Hostile checks must catch at least:

- wrong `4/3`, `2/3`, or `p^6` vector factors;
- omission of the mean subtraction required by periodic `w`;
- wrong TT trace or norm;
- wrong `alpha=(2/3)p^6 mu` condition;
- wrong sign or power in `Lambda=-d^2p^-12`;
- a scalar-only false pass that violates momentum;
- a conformal-only false pass that violates the direct physical constraints;
- omission of the `-2Lambda/3` electric-Weyl term;
- calling the `q=0` branch tidal or the `q!=0` branch zero-tide;
- treating `q` sign as selected when axis relabelling interchanges it;
- promoting the torus, ansatz, `p`, `q`, `Lambda`, or `tau` profile into UDT canon;
- selecting a universe/history or changing metric/kernel/angular/observational interfaces.

Run the current premise verifier and full repository suite before banking. Fresh external
adversarial review is required before an externally accepted grade.

## Preregistered landing classes

Exactly one maximum landing may be used:

1. `EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_WITH_ZERO_TIDE_AND_TIDAL_SUBBRANCHES__CONSTANT_PSI_CLASSIFICATION_FORCES_LAMBDA_MINUS_Q_SQUARED__NO_PHYSICAL_DATA_SELECTION`
2. `EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_BUT_ALL_REGISTERED_MEMBERS_ARE_ZERO_TIDE__NO_PHYSICAL_DATA_SELECTION`
3. `REGISTERED_NONCMC_COUPLED_ANSATZ_HAS_NO_LAWFUL_DATA`
4. `CLASSIFICATION_INCONCLUSIVE_WITHIN_REGISTERED_SCOPE`

No landing changes the metric, reciprocal kernel, angular cancellation, observational interface,
or premise grades.
