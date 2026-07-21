# UDT metric-native clock/ruler soldering selector audit

Date: 2026-07-20

## Result first

This derivation found a real partial closure hiding in the finite-cell mirror:

> Within the conditional mixed Lorentzian readout and a supplied reciprocal base, the spatial seal
> uniquely selects the local clock and radial eigendirections at its fixed surface, up to discrete
> signs.

The seal also selects the spatial-reflection **sign branch** of the mixed family. It does **not**
select the invariant magnitude `mu`, the complete angular/normal/time-on lift, or a path-consistent
global continuation.

Accordingly, the previous “soldering absent” wording is refined rather than overturned: a
seal-local base soldering is derived conditionally, while a complete selected global soldering
remains absent from the current ledger.

## Exact seal-local construction

Write the spatial-reflection branch as

```text
H = [[A,-k A b],[-k A b,A b^2]],       A>0, b>0, k>1,
F_b = [[0,b],[1/b,0]].
```

The fixed and reversed seal vectors are

```text
v_plus=(b,1),       F_b v_plus=+v_plus,
v_minus=(-b,1),     F_b v_minus=-v_minus.
```

Their metric products are

```text
H(v_plus,v_plus)=2 A b^2(1-k)<0,
H(v_minus,v_minus)=2 A b^2(1+k)>0,
H(v_plus,v_minus)=0.
```

Thus a spatial seal fixes the timelike line and reverses the radial spacelike line. The opposite
mixed-family sign would exchange those causal roles and realize a temporal-like rather than spatial
reflection in this convention.

Normalize these two vectors by their metric norms. Then

```text
S0^T H S0 = diag(-1,1),
S0^-1 F_b S0 = diag(1,-1),
S0^-1 (-F_b) S0 = diag(-1,1).
```

All orthonormalizers of `H` differ by an `O(1,1)` transformation, but requiring the seal to retain
the standard spatial-reflection form removes the continuous boost: its commutator is proportional
to `sinh(chi)`, whose only real zero is `chi=0`. Only discrete sign/time-orientation choices remain.

This is a conditional local soldering theorem at the seal. It uses no SR/GR observer mechanics.

## What remains in the reciprocal operator

In the normalized seal frame the reciprocal generator is

```text
L_seal = [[0,sqrt((k-1)/(k+1))],
          [sqrt((k+1)/(k-1)),0]].
```

The seal has selected the sign branch, but `k` remains. Since `mu=k^2`, the invariant magnitude is
still open.

## Complete metric and nonzero angular coupling

To avoid relying on a product spectator, the audit used

```text
H4 = [[H,C],[C^T,I2]],
C  = [[u,v],[u,-v]],
R4 = diag(F_1, diag(1,-1)).
```

The nonzero cross block is the complete solution of the tested parity form

```text
F_1^T C A = C.
```

It obeys the exact full seal isometry and reciprocal inversion. Two witnesses with the identical
angular block, angular reflection, `u=v=1/10`, `c` convention, orientation, and Lorentz signature
survive:

| `mu` | determinant | full-pair invariant |
|---:|---:|---:|
| 4 | `-7599/2500` | `-8300/2533` |
| 9 | `-20099/2500` | `-49900/20099` |

Their different full-pair invariants prove that the angular coupling has not made them equivalent.

In the conditional direct transverse-identity reciprocal extension,
`L4=diag(-1,1,0,0)` selects the reciprocal plane `im(L4)`. The metric then supplies its unique
orthogonal complement through the projector

```text
Pi = U (U^T H4 U)^-1 U^T H4.
```

`Pi` is idempotent, metric-self-adjoint, and seal-preserved. Its transverse complement is positive
for both witnesses. Therefore nonzero coordinate cross terms do not obstruct construction of a
complete orthogonal frame once that full reciprocal/angular lift is chosen.

But the lift is not currently selected. Identity, minus-identity, axis-reflection, and conditional
Hopf angular actions remain inequivalent registered completions, with normal and time-on actions
also open.

## CSN and volume cannot finish the selection

Positive common scaling leaves the pair invariant unchanged. Unit full determinant also fails:

```text
H_base=[[1,-k],[-k,1]],
Q_angular=I2/sqrt(k^2-1)
```

has full determinant `-1` for every `k>1`, while retaining

```text
I=2(1+k^2)/(1-k^2).
```

Volume normalization can trade reciprocal determinant against angular area; it cannot determine
the dimensionless mixing.

## Cartan and bootstrap ruling

Cartan geometry can **see** `mu` after a metric is supplied. For the exact varying base witness

```text
g(r)=[[exp(-2r),-k],[-k,exp(2r)]],
R=4 exp(-2r)/(k^2-1).
```

Different `k` values therefore need not have the same curvature. But the Levi-Civita construction
and Bianchi identities compute and constrain the consistency of the supplied geometry; they do not
set `k` to a preferred value.

The current bootstrap supplies still less of the needed tensor type. It is an after-solution
admissibility predicate. It contains no coframe map, representative section, or equation involving
the pair invariant. A future varied global functional or representative section could add one, but
neither exists in current authority.

## Supported preregistered outcomes

- `ANGULAR_SEAL_STRUCTURE_LEAVES_MU_OPEN`;
- `NONZERO_ANGULAR_COUPLING_LEAVES_MU_OPEN`;
- `CSN_OR_VOLUME_NORMALIZATION_LEAVES_MU_OPEN`;
- `CARTAN_HOLONOMY_IS_CONDITIONAL_ON_COFRAME_CHOICE`;
- `BOOTSTRAP_HAS_NO_CURRENT_SOLDERING_EQUATION`;
- `METRIC_NATIVE_SOLDERING_RULE_ABSENT_FROM_CURRENT_LEDGER`, scoped strictly to a complete selected
  lift and global continuation; and
- `FULL_ANGULAR_DYNAMIC_COMPLETION_COULD_STILL_SELECT_OPEN`.

The new positive intermediate status is
`DERIVED_CONDITIONAL_WITHIN_PRE_SPLIT_MIXED_BASE_AT_SEAL` for the seal-local base soldering.

## What remains open

The smallest missing object is now a selected complete reciprocal/angular/normal/time-on lift and a
global continuation/closure equation that acts on the pair invariant. This is narrower than an
unspecified new observer postulate. It is also not currently supplied by the finite-cell words,
CSN, Cartan identities, conditional C2 tiles, or on-shell bootstrap.

No action, topology, representative, carrier, source, boundary charge, scale, mass, or GPU result
was selected here.

## Evidence gates

1. **Preregistered:** yes, commit `6dc52f5`, before candidate-source inspection and algebra.
2. **Full space or bounded scope:** exact for the mixed constant symmetric base, its seal-local
   normalization, the tested full axis-reflection lift with complete parity-compatible cross block,
   and CSN/determinant counterfamilies; not every possible full angular/global completion.
3. **Independent verification:** separate standard-library rational reconstruction, source/status
   replay, and fail-closed mutations.
4. **Premise audit:** all readout, full-lift, Cartan, bootstrap, angular, boundary, and observer
   qualifications are explicit in the ledgers.

Maximum conclusion:

`UDT_CURRENT_METRIC_NATIVE_SOLDERING_SELECTOR_STATUS_CHARACTERIZED`.
