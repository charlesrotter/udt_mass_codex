# Exact dependency and counterfamily derivation

## 1. Founded reciprocal character

For additive signed depth `delta`, the founded pair representation is

```text
D(delta)=diag(exp(-delta),exp(+delta)).
```

It obeys

```text
D(delta_2)D(delta_1)=D(delta_1+delta_2),
D(-delta)=D(delta)^(-1).
```

These identities determine the two-channel character after `delta` is supplied. They do not
define the physical comparison arrows or calculate `delta` from the complete metric.

Indeed, for every scalar `f` on the event domain,

```text
delta_f(p,q)=f(q)-f(p)
```

has identity, reversal, and exact three-point composition. Composition therefore admits an
infinite family and cannot be the missing depth selector.

## 2. Complete full-frame extension retains a modulus

Once an ordered clock/ruler pair and an isotropic screen reduction are supplied, the diagonal
extension family is

```text
X_lambda=diag(-1,+1,lambda,lambda),
E_lambda(phi)=exp(phi X_lambda)
             =diag(exp(-phi),exp(+phi),exp(lambda phi),exp(lambda phi)).
```

Every real `lambda` preserves the founded inverse action on the first two slots and composes as a
one-parameter representation. Distinct `lambda` values give distinct transverse responses. The
seven-dimensional affine response audit also shows that an unchanged spectator screen is not the
general complete response. Hence covariance, trace assumptions not in force, and pair composition
do not select the full lift.

## 3. Stationary metric supplies a bounded depth

Let a complete stationary metric possess an intrinsic timelike Killing line `K`, and put

```text
Q=sqrt(-g(K,K)).
```

Constant rescaling of a representative of the line cancels in the endpoint ratio, so

```text
delta_K(p,q)=log[Q(p)/Q(q)],
alpha_K=-d log Q
```

is metric-native on this domain. In the founded stationary readout

```text
Q=c_E exp(-phi),
```

the observed anchor cancels and

```text
delta_K(p,q)=phi(q)-phi(p),
integral_gamma alpha_K=delta_K(p,q).
```

This is a genuine positive result. It is bounded to stationary observers on a branch with an
intrinsic timelike Killing line. It neither selects that branch as realized nor supplies arbitrary
observer/nonstationary depth.

## 4. Metric transport and reciprocal dilation are different types

The Levi-Civita connection is metric-skew:

```text
omega^T eta + eta omega=0.
```

The founded reciprocal generator is metric-self-adjoint:

```text
H^T eta-eta H=0,
H=diag(-1,+1,0,0).
```

Their invariant trace pairing vanishes:

```text
tr(H omega)=0.
```

Thus ordinary metric transport cannot secretly generate the reciprocal dilation. It does,
however, give exact coframe transport `U_gamma` on a supplied path.

The type-correct stationary hybrid is therefore the ordered pair

```text
C_gamma=(D(delta_K(p,q)),U_gamma).
```

For composable paths, both components compose exactly. This yields an exact reducible comparison
family. It is not an irreducible four-dimensional reciprocal lift and does not select the path,
`lambda`, mixing response, section, completion, or causal continuation.

## 5. Complete counterfamily

On a supplied `R x S3` domain with global Maurer-Cartan forms, consider

```text
theta_0=exp(-phi)(c_E dt+a sigma_3),
theta_1=R exp(+phi) sigma_3,
theta_2=R exp(lambda phi) sigma_1,
theta_3=R exp(lambda phi) sigma_2.
```

The determinant is

```text
det E=R^3 exp(2 lambda phi),
det g=-R^6 exp(4 lambda phi).
```

It is nonzero for positive `R`, finite smooth `phi`, and every real `lambda`. Subject to the
separately stated spacelike-slice inequality, this is a coherent complete non-ultrastatic
configuration family. It simultaneously proves:

- complete geometry does not select `lambda`;
- complete geometry alone does not select a realized `phi` profile;
- a configuration witness is not an equation of motion.

The twist-off member retains stationary norm depth while losing the twist-selected ruler line,
separating depth from ruler selection on one family.

## 6. Global data do not follow from the local law

The registered atlases classify multiple caps, seams, quotients, holonomy patterns, causal strata,
and interface choices. Local tensorial covariance supplies chart transformation behavior for a
given construction. It does not choose the transition cocycle, global section, completion class,
or continuation/exclusion theorem at a type-changing surface.

Likewise, bootstrap and co-presence are registered working interpretations without an executable
map from a complete configuration back to the comparison, lift, and global data. An action cannot
be imported downstream to fill a kinematic domain that remains open.

## 7. Exact dependency boundary

The registered chain is

```text
founded pair -> reciprocal character
stationary complete metric + intrinsic K -> bounded signed depth
complete metric + supplied path -> coframe transport
bounded depth + transport -> conditional exact reducible hybrid
ordered pair + real lambda -> conditional finite reciprocal lift family
supplied global data -> conditional global constructions
```

There is no registered arrow from the common complete input to all of:

```text
physical comparison/depth;
selected finite full-frame reciprocal response;
selected global completion/interface.
```

The runnable algebra is `run_algebra.py`; the independent non-importing replay is
`verify_audit.py`.
