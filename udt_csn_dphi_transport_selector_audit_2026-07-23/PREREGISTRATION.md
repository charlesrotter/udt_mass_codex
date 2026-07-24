# CSN–`dphi` transport-selector audit — preregistration

Date: 2026-07-23

Base: `bc802bb0ec3b612f841963cc471440fc88741bbf`

Mode: metric-led, CPU-only exact local differential geometry plus independent
symbolic/rational verification

## Whole question

The finite-cell Cartan transport atlas established that the normalized
`dphi` line and its induced `3+3` two-form reduction are unchanged by
positive Common-Scale rescaling, while the Levi-Civita mixing profile of
an arbitrary representative is not.

This audit asks the exact bounded next question:

> Does the registered pre-scale UDT data supply a conformally natural
> connection or transport for the intrinsic `dphi` reduction, and if so
> is that transport unique and physically selected; or must a later
> bootstrap/scale-bearing law first select additional structure?

Existence, preservation, uniqueness, and physical authority are separate
gates. A connection may pass one without passing the others.

## Frozen geometric universe

The local parent data are:

```text
(M,[g]_CSN,phi),  alpha=dphi,  s=g^{-1}(alpha,alpha).
```

The audit includes every causal stratum:

- timelike nonzero `dphi`;
- spacelike nonzero `dphi`;
- null nonzero `dphi`;
- zero `dphi`; and
- passage between those strata.

On each connected nonnull stratum it tests the full local classes below:

1. Levi-Civita connections of arbitrary representatives;
2. all torsion-free Weyl connections relative to a representative;
3. the scalar-gradient compensator candidate
   `h0=|s|g` and its Levi-Civita connection;
4. the invariant conformal family
   `h_f=exp(2 f(phi)) h0`, including nontrivial exact witnesses;
5. torsion-free Weyl connections preserving the normalized `dphi` line;
6. metric-compatible projected/Kato connections preserving the line and
   induced `3+3` reduction;
7. the complete residual stabilizer-valued freedom of such
   split-preserving metric connections;
8. the normal conformal Cartan/tractor connection as a distinct
   representation-bundle object; and
9. the null, zero, and type-changing interface limits.

The `h_f` family is a registered counterfamily, not asserted to exhaust
every higher-jet natural construction. The torsion-free Weyl class and
the metric-compatible split-preserving affine class are exhausted within
their declared local differential orders.

## Objects that must remain distinct

1. the CSN conformal class;
2. a chosen representative;
3. a CSN-invariant metric constructed from `dphi`;
4. an affine connection;
5. representative covariance of a connection formula;
6. preservation of the `dphi` line/projector;
7. preservation of the induced `3+3` two-form projector;
8. torsion freedom;
9. metric compatibility;
10. uniqueness in a declared connection class;
11. a geometric comparison rule;
12. physical time evolution or force;
13. a local nonnull construction;
14. a through-interface/global finite-cell completion; and
15. a physical scale/representative selector.

## Exact tests

### T1 — common-scale algebra

For arbitrary smooth positive `Omega=exp(sigma)`, derive exactly

```text
g' = exp(2 sigma) g,
s' = exp(-2 sigma) s,
h0' = h0.
```

Require

```text
h0^{-1}(dphi,dphi)=sign(s)
```

on both nonnull causal strata.

### T2 — invariant Levi-Civita/Weyl connection

Set

```text
A0=(1/2)d log|s|.
```

Verify that `LC(h0)` equals the Weyl connection of `(g,A0)` under the
registered sign convention and that

```text
A0' = A0-dsigma
```

leaves the affine connection unchanged.

### T3 — uniqueness counterfamily

For arbitrary smooth `f(phi)`, test

```text
h_f=exp(2 f(phi))h0,
A_f=A0+f'(phi)dphi.
```

At least two nonconstant exact witnesses must be inequivalent as affine
connections while satisfying all registered local CSN and causal data.
Reciprocal reversal `phi -> -phi`, seal normalization at `phi=0`, and
any additive-origin convention must be audited separately rather than
silently used to delete the family.

### T4 — torsion-free split preservation

Solve the complete local equation for a torsion-free Weyl connection to
preserve the normalized `dphi` line/projector. Derive necessary and
sufficient conditions, not merely a fitted witness. The exact-gradient
orthogonal screen, its trace and trace-free second fundamental form, and
the line acceleration must remain live.

### T5 — metric split-preserving transport

For the `h0`-self-adjoint projector `P`, test the projected/Kato
connection on `TM` and its induced connection on `Lambda^2(TM)`:

```text
K_X=(nabla_X P)P-(nabla_X P)(1-P),
D_X=nabla_X-K_X.
```

Verify `D P=0`, metric compatibility, induced `3+3` preservation, and
the exact torsion. Characterize every metric-compatible addition that
commutes with `P`; a preferred zero addition may not be called unique
without a registered premise.

### T6 — degeneration and bundle-type guards

Prove what fails at `s=0` and `dphi=0`. Keep normal conformal
Cartan/tractor transport distinct from tangent-bundle transport and from
a selected tangent section.

## Falsification and certification contract

The package fails if it:

- treats `LC(g)` for an arbitrary representative as pre-scale invariant;
- calls `h0` physical merely because it is a natural formula;
- calls one natural formula unique without defeating the `h_f` or
  Weyl/stabilizer counterfamilies;
- calls projected/Kato transport torsion-free without exact proof;
- calls geometric transport physical time evolution, force, action, or
  source;
- deletes the trace-free screen/shear equations;
- extends a normalized nonnull construction through null or zero `dphi`;
- uses the conformal tractor connection as a tangent section;
- imports GR field equations, an action, carrier, boundary functional,
  density, `X_max`, or a desired finite-cell branch; or
- promotes a local theorem to global finite-cell closure.

Certification requires:

1. exact symbolic identities for T1–T6;
2. explicit inequivalent countermodels where nonuniqueness is claimed;
3. an independent implementation that imports no production code;
4. exercised fail-closed mutations for every load-bearing distinction;
5. unchanged frozen packages/current paths/frontier targets; and
6. the documented repository test baseline.

## Frozen outcome classes

The audit may return any compatible combination of:

1. `NO_PRE_SCALE_CONNECTION_AVAILABLE`;
2. `CSN_INVARIANT_LOCAL_CONNECTION_AVAILABLE_NONNULL_ONLY`;
3. `CSN_INVARIANT_CONNECTION_UNIQUE_IN_DECLARED_CLASS`;
4. `CSN_INVARIANT_CONNECTION_FAMILY_REMAINS`;
5. `TORSION_FREE_SPLIT_PRESERVATION_GENERIC`;
6. `TORSION_FREE_SPLIT_PRESERVATION_CONDITIONAL`;
7. `METRIC_SPLIT_PRESERVING_TRANSPORT_AVAILABLE_WITH_TORSION`;
8. `SPLIT_PRESERVING_CONNECTION_FREEDOM_REMAINS`;
9. `NULL_ZERO_INTERFACE_OBSTRUCTS_GLOBAL_EXTENSION`;
10. `NORMAL_TRACTOR_TRANSPORT_DOES_NOT_CLOSE_TANGENT_SELECTOR`;
11. `BOOTSTRAP_NOT_NEEDED_FOR_LOCAL_EXISTENCE_BUT_ADDITIONAL_SELECTOR_NEEDED_FOR_PHYSICAL_GLOBAL_AUTHORITY`;
12. `BOOTSTRAP_OR_EQUIVALENT_SCALE_BEARING_SELECTOR_REQUIRED_BEFORE_PHYSICAL_MIXING`;
13. `AUDIT_INCONCLUSIVE`.

## Maximum conclusion

```text
LOCAL_CSN_NATURAL_CONNECTION_AND_DPHI_SPLIT_TRANSPORT_FAMILY_CHARACTERIZED_WITH_EXACT_EXISTENCE_UNIQUENESS_TORSION_AND_INTERFACE_GATES
```

No action, field equation, source, carrier, Hopf section, boundary
functional, branch, physical time law, absolute scale, mass, GPU work,
canonization, or repository reorganization is authorized.
