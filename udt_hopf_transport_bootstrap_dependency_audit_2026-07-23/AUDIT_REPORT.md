# Hopf–transport–bootstrap dependency audit

## Result

The conditional Hopf **topological core** does not wait on the open
physical affine-transport selector.

For a supplied smooth map `n:M3->S2`, target area-form normalization,
oriented domain, and closed or fixed boundary class,

```text
F = n*omega
dF = 0
da = F
Q proportional to integral(a wedge F)
```

are differential-form constructions. No affine tangent connection is
needed. The exact conditional ruling is:

```text
TOPOLOGICAL_CORE_TRANSPORT_INDEPENDENT_IN_DECLARED_CARRIER_DOMAIN
```

This does not make the carrier native. The round internal `S2` remains
a `POSIT`, the physical boundary remains open, and the intrinsic
celestial/screen `S2` remains a fiber rather than a selected section.

## Torsion is a rewrite issue, not a change in topology

For a two-form `F` and a general affine connection,

```text
dF_abc =
  3 nabla_[a F_bc]
  + T^d_ab F_dc
  + T^d_bc F_da
  + T^d_ca F_db.
```

Every torsion-free member of the `Gamma_f` and derivative-only Weyl
families therefore gives the familiar covariant antisymmetrization.
The projected/Kato transport is generically torsionful, so the naive
covariant rewrite fails; the torsion correction restores the same
connection-independent exterior derivative.

The production controller proves the symbolic identity. A separate
stdlib/Fraction implementation verified 17 exact rational cases, with
16 explicit failures of the naive torsionful rewrite.

## What remains transport or metric dependent

A Hodge/Coulomb **choice of primitive** depends on metric, gauge, and
boundary, even though the exact Hopf integral does not. The conditional
Hopf principal `U(1)` connection is also not the unresolved affine
connection: the former lives on a principal bundle, while the latter
acts on tangent-bundle sections.

The supplied internal-target `L2+L4` energy contains no affine
connection directly, but it is not metric-independent. On a
three-dimensional spatial slice,

```text
h -> q^2 h
E2 -> q E2
E4 -> q^-1 E4.
```

Thus the exact `h_f=exp(2f(phi))h0` counterfamily changes the relative
energy balance. Connection independence of the topological integer
cannot be exported to energy or stability.

A field realized as a section of a tangent, screen, or associated
bundle would need a selected bundle connection or a separately derived
intrinsic derivative. The ordinary derivatives in the existing
internal-target action cannot be silently reinterpreted as that law.

## Stability and time

The existing static result remains:

```text
SETTLED_STATIC_FINITE_BOX_CONDITIONAL
```

under its exact carrier, `L2+L4`, metric, finite-box, boundary, and
operator premises. This audit neither weakens nor enlarges it.

Time-live persistence remains `OPEN`. Static relaxation and a static
Hessian do not supply physical evolution, regularity across all
strata, topology-change rules, or a physical finite-cell boundary.

## Bootstrap brackets

The user's expectation that bootstrap remains close to this work is
correct, with a crucial placement rule.

- **B0:** the conditional topological identity is classified without
  bootstrap.
- **B1:** the presently registered bootstrap is an after-solution
  admissibility test. It may eventually bracket complete
  matter-bearing topological branches by total proper density.
- **B2:** an explicitly derived future `Sigma` map could select a
  representative section or branch. No such map exists now.
- **B3:** an explicitly derived and varied global functional could
  feed closure back into local equations. No such functional exists
  now.

The density bracket is not operational until a native complete action,
source, total mass, proper volume, boundary, and complete solution
family exist. It cannot be inserted pointwise as a mechanism.

The current ruling is:

```text
CURRENT_BOOTSTRAP_IS_OUTER_ADMISSIBILITY_ONLY
```

## The remaining join

The unresolved scientific object is not the definition of the Hopf
integer. It is the native realization:

```text
complete UDT metric/coframe
  -> selected global section or carrier map
  -> physical derivative/action/boundary
  -> static and time-live solution
  -> outer bootstrap admissibility
```

The status is:

```text
EMERGENT_HOPF_REALIZATION_DEPENDS_ON_OPEN_SECTION_TRANSPORT_BOUNDARY_OR_DYNAMICS
```

## Verification

- Exact SymPy controller: 12/12 checks passed.
- Independent stdlib/Fraction verifier: 9/9 exact checks, 13/13
  catch-proofs, and 5/5 agreement checks passed.
- All frozen source hashes and package manifests in
  `SOURCE_MANIFEST.tsv` replayed successfully.
- Final repository gates are recorded in `REPOSITORY_GATES.json`.

## Four evidence gates

1. **Preregistered:** yes, commit `73c4683`, before outcome scripts ran.
2. **Full or bounded scope justified:** bounded—conditional carrier and
   domain topology, exact connection rewrites, and energy weights; no
   global carrier emergence or time evolution.
3. **Independently verified:** yes for the load-bearing algebra using a
   separate stdlib/Fraction implementation; no fresh physical model
   family was used.
4. **Every premise audited:** yes within the frozen source set; open
   carrier, boundary, transport, action, and bootstrap forms remain
   explicit.

The result is therefore banked as `VERIFIED-WITH-CAVEATS`, not
canonized physics.
