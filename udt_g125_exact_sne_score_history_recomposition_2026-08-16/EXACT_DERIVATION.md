# G125 exact derivation — SNe total-score/history recomposition

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_REPAIRS__EXACT_CONDITIONAL_SNE_TOTAL_SCORE_DERIVED`

## 1. Result first

G120's conditional outgoing P1 curve is

\[
R(Z)=R_\infty\left(1-Z^{-2/n}\right),
\qquad R_\infty=nX_{\rm eff},
\qquad Z>1.
\tag{1}
\]

It is monotone and therefore invertible on the declared open branch:

\[
Z(R)=\left(1-\frac{R}{R_\infty}\right)^{-n/2},
\qquad 0<R<R_\infty.
\tag{2}
\]

The observer vertex `R=0,Z=1` is the continuous boundary closure, not a member of the `Z>1` open
inversion domain. Hence the operational frequency depth of this frozen functional curve is exactly

\[
\boxed{
\zeta_{\rm P1}(R)=\log Z(R)
=-\frac n2\log\left(1-\frac{R}{R_\infty}\right)
}.
\tag{3}
\]

G124 gives, on the same supplied normalized radial-null central-spherical query,

\[
\zeta=\phi_{\rm pair}-\kappa_{\rm pair}+\chi_s,
\qquad
\kappa_{\rm pair}=-\frac12\log|K(R)|.
\tag{4}
\]

Combining (3) and (4) yields the exact conditional SNe score constraint

\[
\boxed{
\phi_{\rm pair}(R)
+\frac12\log|K(R)|
+\chi_s(R)
=-\frac n2\log\left(1-\frac{R}{R_\infty}\right)
}.
\tag{5}
\]

Over the evaluated SNe range, this is the strongest current conditional SNe statement about a
history already assumed to realize the same G119 query, G120 imported transfer, processed-release
frequency slot, and frozen P1 curve. Outside the evaluated range it is only formal continuation of
that functional family. It is one scalar constraint on three correctly typed channels, not a
measurement of terminal `phi_pair` alone or independent evidence for G124.

## 2. Why no likelihood replay is warranted

G120's imported temporary transfer law is

\[
d_L=Z^2R.
\tag{6}
\]

Neither (4) nor (5) changes the supplied operational variables `Z` and `R`. Substitution of (1)
into (6) therefore reproduces identically

\[
d_L(Z)=R_\infty Z^2(1-Z^{-2/n}).
\tag{7}
\]

The Pantheon+ and DES predictions and likelihoods are unchanged algebraically. Re-running them
would be regression evidence only and would violate the preregistered anti-loop stop rule.

## 3. Exact surviving freedom

Equation (5) does not select its component histories. For arbitrary real functions
`phi_pair(R)` and `chi_s(R)`, it admits

\[
|K(R)|=exp\left(2[\zeta_{\rm P1}(R)-\phi_{\rm pair}(R)-\chi_s(R)]\right)>0.
\tag{8}
\]

Equivalently, for arbitrary positive `|K(R)|` and arbitrary `phi_pair(R)`, it fixes only

\[
\chi_s(R)=\zeta_{\rm P1}(R)-\phi_{\rm pair}(R)-\frac12\log|K(R)|.
\tag{9}
\]

A simple two-parameter algebraic witness family is

\[
\phi_{\rm pair}=a\zeta_{\rm P1},
\qquad
\chi_s=b\zeta_{\rm P1},
\qquad
|K(R)|=e^{2(1-a-b)\zeta_{\rm P1}}.
\tag{10}
\]

It contains distinct terminal allocations: all score assigned algebraically to `phi_pair` at
`(a,b)=(1,0)`, to screen rate at `(0,0)`, or to the source-clock term at `(0,1)`. These are exact
terminal-data decompositions, not stationary, screen-dominated, or source-dominated realized
histories. Global integrability requires additional complete-history and source-clock consistency.

The oriented affine-to-areal rate is `K(R)=sigma |K(R)|`. Orientation remains in `sigma`, the
branch label, and G124's `beta_pair`; it is not carried by the total score.

## 4. Endpoint and formal limit

At the normalized observer vertex, `R=0`, equations (2)--(3) give `Z=1` and `zeta=0`. With the full
G124 vertex normalization one obtains the corresponding zeroed initial components. Equation (5)
by itself, however, only fixes their sum.

As `R` approaches the formal extrapolated family limit `R_inf` from below, `zeta_P1` diverges.
This region lies outside the evaluated SNe range. Equation (5)
requires at least one component combination to carry that divergence, but it does not decide
whether it lies in reciprocal depth, affine/areal screen rate, source-clock relation, or a mixture.
`R_inf` remains an extrapolated P1 family parameter, not a measured or derived `X_max`.

## 5. Bounded landing

```text
EXACT_CONDITIONAL_SNE_SCORE_RECOMPOSITION
__G120_NUMERICAL_INTERFACE_UNCHANGED
__P1_IDENTIFIES_ONLY_ZETA_OF_R_EQUALS_MINUS_N_OVER_TWO_LOG_ONE_MINUS_R_OVER_RINF
__G124_RETYPES_THIS_AS_PHI_PLUS_HALF_LOG_ABS_K_PLUS_CHI
__TERMINAL_SCREEN_SOURCE_DECOMPOSITION_AND_COMPLETE_HISTORY_NOT_SELECTED
__NO_LIKELIHOOD_REPLAY_JUSTIFIED
```

No physical history, query owner, source clock, native transfer, branch population, `X_max`, CMB,
BAO, action, bootstrap, matter, mass, or signalling conclusion follows.
