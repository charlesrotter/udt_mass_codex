# G319 preregistration — ratio-free non-CMC constraint descent

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_OUTCOME_SCRIPTS_OR_RESULTS`

## Registered frame

Use the G318 seed

\[
\bar\gamma_{ij}=\delta_{ij},\qquad \psi=\psi(x)>0,
\]

\[
\bar A_{TT}^{ij}=\operatorname{diag}(\alpha,-\alpha/2+d,-\alpha/2-d),
\qquad W=w(x)\partial_x,
\]

and

\[
\bar A_{TT}+\bar LW
=\operatorname{diag}(2v/3,-v/3+d,-v/3-d).
\]

Require smooth periodic nonconstant `psi` and sign-definite periodic `tau`, but impose no constant
or functional ratio between `v`, `psi`, and `tau`.

## Candidate ratio-free reduction

Define

\[
\lambda=v\psi^{-6},\qquad A=\tau+\lambda,\qquad B=\tau-\lambda,
\qquad H=\psi'/\psi.
\]

Preregister that the vector and scalar constraints must independently reduce to

\[
\boxed{B'=3H(A-B)},
\]

\[
\boxed{AB=F[\psi]},
\qquad
F[\psi]=12\psi''\psi^{-5}+3d^2\psi^{-12}+3\Lambda.
\]

Without dividing by `B`, these imply

\[
(B^2)'=6H(F-B^2).
\]

Preregister the exact conserved quantity

\[
\boxed{
J_0=\psi^6B^2-36(\psi')^2+3d^2\psi^{-6}-3\Lambda\psi^6,
}
\]

and falsify it if direct differentiation does not vanish under both constraints.

## Regular-stratum reconstruction

On every connected region where `B` is nowhere zero, preregister

\[
B=\epsilon\psi^{-3}
\sqrt{36(\psi')^2-3d^2\psi^{-6}+3\Lambda\psi^6+J_0},
\qquad \epsilon=\pm1,
\]

\[
A=F/B,qquad
\tau=(A+B)/2,qquad
\lambda=(A-B)/2,qquad
v=\psi^6\lambda.
\]

Periodicity must then fix

\[
\alpha=\frac23\langle v\rangle,
\qquad
w'=\frac12(v-\langle v\rangle)
\]

modulo the additive translation kernel. Production and independent direct-physical calculations
must verify both constraints after reconstruction.

## Zero/crossing stratum

The global first integral is not permitted to divide by `B`. At every zero of `B`, the scalar
constraint requires `F=0`. The vector equation retains `B'=3HA`. Production must classify these as
compatibility/gluing points rather than silently deleting them. No claim of a full explicit
parameterization of this exceptional stratum is allowed unless its smoothness data are proved.

## Arbitrary-profile discriminator

For any fixed smooth positive periodic `psi`, fixed real `d,Lambda`, and sufficiently large `J_0`,
the radicand and `B^2+F` should both be strictly positive on the compact period. Then the regular
reconstruction gives positive `tau` for `epsilon=+1` and negative `tau` for `epsilon=-1`.

Preregister the following possible landings:

1. `RATIO_FREE_CONSTRAINTS_SELECT_A_SMALLER_PROFILE_FAMILY` if a further nonidentity residual
   survives after direct replay;
2. `EXACT_QUADRATURE_LEAVES_ARBITRARY_POSITIVE_PERIODIC_PSI` if the reconstruction works for every
   such profile with sufficiently large free `J_0`;
3. `ONLY_PARTIAL_REGULAR_STRATUM_CLASSIFIED` if the nowhere-zero result holds but a claimed global
   statement improperly crosses `B=0`;
4. `REGISTERED_FRAME_INCONSISTENT` if conformal and direct constraints disagree.

## G318 regression test

For

\[
\tau=C\psi^n,qquad \lambda=\frac{n}{n+6}\tau,
\]

verify that the G318 scalar ODE makes `J_0` constant and that its power-law family embeds as a
strict subfamily. If ratio-free examples have nonconstant `lambda/tau`, G318's exponent and
`n<=-3` obstruction must remain explicitly ansatz-scoped rather than being promoted or erased.

## Certification and falsification contract

- Exact production identities use standard-library rational arithmetic where algebraic.
- An implementation-distinct verifier reconstructs Christoffels and physical Hamiltonian/momentum
  constraints without importing production functions or reading production output.
- Periodic explicit controls include constant-ratio regression and genuinely variable-ratio
  profiles.
- Hostile checks must catch wrong factors `3,6,12,36`, wrong `psi` powers, division through a `B=0`
  point, loss of mean subtraction, a fake arbitrary-profile theorem without compact positivity,
  promotion of `J_0` to a measured scale, and any selected history/kernel/observation claim.
- The full repository purity harness and exact premise registry must pass.
- Fresh external adversarial review is required before external acceptance.

Maximum conclusion: a classification of the registered ratio-free initial-constraint tile. No
physical data, history, topology, population, scalar, scale, source, matter/mass law, observation,
fit, physical `X_max`, metric change, or reciprocal-kernel change may be claimed.
