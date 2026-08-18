# G154 cold external review adjudication

Date: 2026-08-18
Status: `EXTERNALLY_REVIEWED_WITH_CAVEATS__INDEPENDENT_LOCAL_REPLAY_PASS`

## Primary landing

```text
CONFORMAL_NETWORK_NONSELECTION__CURRENT_IDENTITIES_ONLY_EVALUATE_SUPPLIED_HISTORY
```

The cold review validly strengthens G154. It does not retract the original four-class result. It
shows why the freedom survives the complete relation network: positive common rescaling changes
the complete metric history and its normalized response while preserving the reciprocal-position
subnetwork and every currently active compatibility identity.

## Exact distinction

The two load-bearing scales have different types:

\[
X_* = \text{scale parameter of the dimensionful position group},
\qquad
e^\kappa = \text{common clock/ruler scale in the pair metric}.
\]

For

\[
h=-T^2(d\tau+\beta\,d\sigma)^2+L^2d\sigma^2,
\qquad
T=e^{\kappa-\phi},\quad L=e^{\kappa+\phi},
\]

the working fixed-scale position is \(\rho=X_*\tanh\phi\), whereas the normalized ruler is

\[
n=e^{-\kappa-\phi}(\partial_\sigma-\beta\partial_\tau).
\]

Thus the position law contains \(X_*\) and \(\phi\), while the normalized approach rate also
contains \(\kappa\). No active identity relates them.

## Common-scale theorem

For every positive smooth conformal factor,

\[
\widehat h=e^{2\omega}h,
\]

the terminal readouts obey

\[
\widehat\phi_{\rm pair}=\phi_{\rm pair},\qquad
\widehat\beta=\beta,\qquad
\widehat\kappa=\kappa+\omega.
\]

Consequently \(\widehat\rho=\rho\), but every normalized pair-frame derivative scales as

\[
\widehat V(\rho)=e^{-\omega}V(\rho),\qquad V=u,n.
\]

This deformation remains inside the complete coframe chart: if

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},
\]

then \(\widehat E=e^\Omega E\) has \(\widehat B=e^\Omega B\),
\(\widehat Q=e^\Omega Q\), and \(\widehat S=S\). Every supplied pair pullback and every
reparameterization/overlap identity remains lawful.

The exact global counterfamily in the cold review realizes quiet, finite, divergent, and
nonconvergent normalized responses with the same \(\phi\), \(\rho\), \(X_*\), topology, causal
cones, query atlas, and overlap structure. A smooth cutoff can leave an entire finite calibration
neighborhood unchanged while retaining any chosen asymptotic class.

## Network conclusion

The complete network of all labelled two-plane pullbacks is faithful to a supplied metric: it can
reconstruct that metric pointwise. This is a reconstruction theorem, not a selection theorem.
Every regular metric generates a coherent pullback network. Common rescaling therefore produces a
**different complete network**, not a gauge copy of the same one; nevertheless each network is
equally coherent, and its reciprocal-position subnetwork is unchanged.

Metricity, Cartan and Bianchi identities, causal cones, transport composition, endpoint-rank
closure, and pullback descent all evaluate or organize each supplied history. Without a prescribed
invariant target value or another nonidentity condition, none chooses one member of the conformal
family.

## What the anchors do not yet own

- `c_E` calibrates clock and ruler units and fixes their relative dimensional conversion. A common
  rescaling of both channels leaves that role unchanged; `c_E` does not determine `kappa`.
- `G_obs` is a valid observed anchor, but no active source-, mass-, or density-valued law supplies
  it with a typed argument that restricts `kappa` or the complete history.

This does not prove that an additional dimensional constant is mandatory. A coefficient-free
covariant restriction could exist. What is missing is a nonidentity law, not necessarily a new
constant.

## Smallest missing object

The result types the next joint as a diffeomorphism-natural nonidentity common-scale/history
admissibility law. It must distinguish at least two regular common-scale twins that agree on the
reciprocal position and all calibration neighborhoods, and it must do so for a reason stated
independently of the desired response class.

Its architecture remains `OPEN`: local or global, dynamical or nondynamical, source-dependent or
purely relational. The current evidence does not authorize choosing one.

## Independent verification

The supplied SymPy script reran with stdout byte-identical to the supplied successful log. A new
Python-standard-library implementation was then written without importing SymPy, the supplied
script, or G154 production functions.

Its first frozen tail grid returned `FAIL`: the deliberately slow \(q^{-1/12}\) divergent witness
had grown by only 3.75 orders, short of the preregistered four-order gate. That failure is preserved
in `EXTERNAL_REVIEW_INDEPENDENT_FIRST_RUN.json`. Extending the identical grid from \(q=10^{-48}\)
to \(q=10^{-60}\), without changing formulas or tolerances, produced `12/12 PASS` in
`EXTERNAL_REVIEW_INDEPENDENT_RESULT.json`.

## Mandatory caveats

1. Common scale is retained physical/history freedom, not declared gauge.
2. Conformal twins have different complete pair networks; only the reciprocal-position subnetwork
   is invariant.
3. Endpoint-cocycle algebra for `kappa` is permissive bookkeeping, not a proof that physical
   `kappa` universally descends to endpoints.
4. The theorem is bounded to the active smooth regular configuration arena and current identities.
   It does not prove that no future metric-native law exists.

## Final grade

```text
ACCEPT_CONFORMAL_NETWORK_NONSELECTION_WITH_CAVEATS
```

