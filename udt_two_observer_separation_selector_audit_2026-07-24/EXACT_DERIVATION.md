# Exact derivation and obstruction

## 1. The strongest native construction

Let

\[
\alpha=d\phi,\qquad s=g^{-1}(\alpha,\alpha).
\]

On a connected region where \(s<0\), `dphi` is timelike.  With a time
orientation chosen consistently, \(\phi\) is a temporal function: for every
future-timelike tangent \(w\), \(\alpha(w)\) has one strict sign.  Therefore
\(\phi\) is strictly monotone along every future-timelike observer history.

For any two such histories whose \(\phi\)-ranges overlap, the rule

\[
\phi(A)=\phi(B)=\lambda
\]

pairs at most one event on each history at every common \(\lambda\).  This
does not select one preferred observer congruence.  It treats every
future-timelike history in the branch by the same rule.

Define the Common-Scale-Neutral metric

\[
h_0=|s|\,g.
\]

Under \(g\mapsto\Omega^2g\),
\(s\mapsto\Omega^{-2}s\), so \(h_0\) is invariant.  Set

\[
n=\sharp_{h_0}\alpha .
\]

Then

\[
h_0(n,n)=-1,\qquad \alpha(n)=-1.
\]

The rank-three tensor

\[
q_0=h_0+\alpha\otimes\alpha
\]

vanishes on \(n\) and is positive definite on
\(\ker\alpha=T\Sigma_\lambda\), where
\(\Sigma_\lambda=\{\phi=\lambda\}\).  Its pullback includes every base,
angular, and shift contribution of the complete metric; it is not a
radial or block-diagonal truncation.

On each connected level set define

\[
d_{0,\lambda}(p,q)
=\inf_{\gamma:p\to q}
\int_\gamma \sqrt{q_0(\dot\gamma,\dot\gamma)}\,du .
\]

This is a chart/coframe-invariant Riemannian distance on that supplied
slice.  It is nonnegative, symmetric, zero only at coincident slice points,
and includes path and angular geometry through the intrinsic infimum.

Thus the complete registered \((g,\phi)\) data contain an exact conditional
two-observer separation construction:

```text
globally temporal phi branch
  -> all future-timelike observer histories
  -> equal-phi event pairing
  -> intrinsic q0 slice distance.
```

No preferred observer is introduced.  The condition is on the complete
solution branch.

## 2. Why this is not yet the universal physical distance

The construction has four unresolved ownership gates.

### Causal-domain gate

It requires \(d\phi\) timelike and nonzero:

- spacelike `dphi` makes \(\ker d\phi\) Lorentzian, not a positive
  three-space;
- null `dphi` makes \(h_0\) degenerate;
- zero `dphi` selects no line or foliation;
- causal-type change crosses a null or zero stratum and requires an
  unsupplied interface rule.

The static WR-L branch has positional/spacelike `dphi`, so this construction
does not retrospectively derive its observer separation.

### Global branch gate

The twelve registered finite-cell completions contain zero complete on-shell
\((g,\phi)\) solutions.  Several compact static completions force a critical
point of a real static \(\phi\); their time-live alternatives remain open.
No current premise forces a complete everywhere-temporal \(\phi\), common
range for all observer histories, connected/complete level sets, or
compatible global gluing.

### Physical-representative gate

The CSN-invariant \(h_0\) is the unique member of its conformal orbit making
\(|d\phi|=1\), so \(d_{0,\lambda}\) is a genuine canonical pre-scale
construction.  But current UDT does not say that unit-gradient normalization
is the physical ruler.

The already registered family

\[
h_f=e^{2f(\phi)}h_0
\]

is also constructed invariantly from \(([g],\phi)\).  On
\(\Sigma_\lambda\),

\[
d_{f,\lambda}=e^{f(\lambda)}d_{0,\lambda}.
\]

At one fixed slice this common factor cancels from a distance/diameter ratio,
but it changes comparisons among different \(\phi\)-slices and can change a
whole-solution supremum.  The family is sufficient to block an unconditional
physical-ruler claim.  It is not claimed to exhaust every higher-jet
construction.

### Physical-observer gate

Future-timelike histories are a metric-defined kinematic class, but no
native matter law says which histories are physically realized.  This does
not spoil the geometric conditional result; it blocks promotion to a
complete material-observer theorem.

## 3. Exact controls excluding the other shortcuts

In Minkowski signature \((-+++)\):

- a nonzero null displacement \((1,1,0,0)\) has interval zero, so taking the
  absolute interval fails identity of indiscernibles;
- \(\phi=t\) gives timelike `dphi` and positive `t=constant` level metrics;
- \(\phi=x\) gives spacelike `dphi` and Lorentzian `x=constant` levels;
- \(\phi=t-x\) gives null `dphi`;
- constant \(\phi\) gives no distinguished direction.

Event pairing is load-bearing.  For two parallel worldlines separated by
\(L\), a lab slice gives separation \(L\).  A tilted slice
\(t=\beta x\) pairs different events and has induced separation

\[
L\sqrt{1-\beta^2}.
\]

At \(\beta=3/5\), this is \(4L/5\).  The metric has not contradicted itself;
the pairing changed.

Path selection is also load-bearing.  Between opposite corners of a unit
square, straight and broken paths have lengths \(\sqrt2\) and \(2\).
Intrinsic Riemannian distance resolves this by an infimum only after a
positive spatial slice has been selected.

Finally, \(|\phi(p)-\phi(q)|\) and projective radial depth cannot be complete
distance: distinct points on one level set have zero scalar difference,
while points at equal radius but different angle have nonzero spatial
separation.

## 4. Ruling

One exact conditional separation family is present, but no candidate passes
the universal gate across all registered causal and completion classes.

```text
TEMPORAL-PHI SLICE SEPARATION:
    DERIVED_CONDITIONAL GEOMETRY

UNIVERSAL PHYSICAL TWO-OBSERVER D_g:
    OPEN_SELECTOR
```

Because the universal gate fails, this audit does not compute a global
diameter and does not test \(X_{\mathrm{WRL}}=X_{\max}\).
