# Correction preregistration — full-metric relative-scale gate

Date: 2026-07-23
Correction base: `12d296a86a3492eb4e6c576a525d290e54033392`
Status: preregistered before correcting generated branch results

## Error found

The original preregistration proposed using only

```text
J = H-(trace(H)/2)I
```

for the reciprocal-pattern decision. That object correctly measures the
angular conformal shape strain, but it is not by itself the complete-metric
angular generator required by the preceding intertwiner theorem.

Common-Scale Neutrality removes a conformal rescaling shared by the entire
metric. It does not remove angular common expansion relative to the
reciprocal clock/ruler block. Treating the angular trace as pure calibration
would silently erase the already registered open relative angular
normalization.

The original preregistration and premise ledger remain historical evidence;
this correction layer supersedes their test predicate.

## Corrected invariant comparison

Let

```text
H_rec
```

be the reciprocal coframe strain generator and `H_ang` the angular strain
generator, both measured along the same `T` with `T(phi)=1`.

Under a full common conformal rescaling, both acquire the same scalar
multiple of the identity. The invariant relative mean rate is therefore

```text
a_rel = trace(H_ang)/2 - trace(H_rec)/2.
```

In the registered reciprocal gauge,

```text
H_rec=diag(-1,+1),
trace(H_rec)=0,
```

so `a_rel=w_p` for

```text
q=exp(2w) R(theta)^T diag(exp(-2u),exp(2u)) R(theta).
```

The angular traceless strain still obeys

```text
J^2=sigma^2 I,
sigma^2=u_p^2+theta_p^2 sinh(2u)^2.
```

The full symmetric angular generator has eigenvalues

```text
w_p-sigma, w_p+sigma.
```

It matches the reciprocal `{-1,+1}` spectrum iff

```text
w_p=0
and
sigma^2=1.
```

The angular metric alone still does not supply its skew frame-rotation
generator. Constant eigendirections or a supplied compatible transport
remain a separate persistence gate.

## Consequence to be tested, not forced

For the registered FC12 profile

```text
q=Omega(phi)^2 diag(exp(-2phi),exp(2phi)),
```

the traceless shape is reciprocal for every positive `Omega`, but the full
angular generator matches `{-1,+1}` only when

```text
d log(Omega)/dphi=0
```

relative to the reciprocal block. Because FC12 explicitly permits arbitrary
positive `Omega`, the complete FC12 family must not be called forced
reciprocal. Its constant-relative-scale subfamily may remain an exact
conditional witness.

## Corrected maximum conclusion

```text
THE_FULL_METRIC_ANGULAR_STRAIN_MATCHES_THE_RECIPROCAL_MINUS1_PLUS1_
SPECTRUM_IFF_ITS_RELATIVE_MEAN_SCALE_RATE_VANISHES_AND_ITS_CSN_SHAPE_
SPEED_HAS_UNIT_MAGNITUDE__THE_REGISTERED_FC12_PROFILE_SUPPLIES_AN_EXACT_
CONSTANT_RELATIVE_SCALE_SUBFAMILY_BUT_ARBITRARY_OMEGA_TOPOLOGY_SEAL_
MONODROMY_AND_CURRENT_BOOTSTRAP_DO_NOT_FORCE_OR_SELECT_IT
```

No generated table or report predating this correction may be used as
evidence. Production and independent verification must be rerun from the
corrected predicate.

