# Next bounded gate — conformal fiber rank test

This is a proposed preregistration target, not an executed result.

## Whole question

After quotienting presentation and freezing the physical relation domain, which currently owned
global UDT conditions have nonzero differential rank on positive conformal variations of the
reconstructed metric?

## Family

For a supplied smooth regular metric `g` and arbitrary smooth compactly supported `f`, use

```text
g_epsilon = exp(2 epsilon f) g.
```

Keep fixed the normalized pair data, causal structure, co-presence incidence, observer labels, and
every anchor locus on which `f` is required to vanish.

## Candidate conditions

Inventory only source-owned conditions that purport to restrict the metric itself. Exclude:

- definitions and readout formulas;
- Cartan, metricity, Bianchi, or overlap identities true for every supplied metric;
- reconstruction statements whose input already includes the full valued scale function;
- conditions imposed only on independently supplied query fields;
- desired asymptotic behavior or an observational target inserted as the condition.

For every surviving condition `C[g]=0`, compute

```text
P_g[f] = d/depsilon C[exp(2 epsilon f)g] at epsilon=0.
```

## Preregistered classifications

1. `FUNCTIONAL_KERNEL`: the joint kernel remains infinite-dimensional.
2. `FINITE_MODULI_N`: exactly `N` physical calibration parameters survive.
3. `CONSTANT_PER_COMPONENT`: only constant `f` survives on each connected component.
4. `VALUED_NETWORK_RECONSTRUCTION_ONLY`: the conformal function closes only because its full
   values were supplied as part of the relation network.
5. `NO_OWNED_NONIDENTITY_CONDITION`: the candidate inventory is empty after type checking.

## Nonlinear catch

Any finite-rank landing must also exclude a finite positive conformal twin that:

- agrees on every calibration-anchor neighborhood;
- preserves all registered regularity, causal, overlap, and composition gates;
- changes at least one diffeomorphism-invariant metric quantity away from the anchors.

## Scale holonomy catch

An anchor propagates through a scale carry only when the physical carry is owned and path
independent, or when every remaining loop modulus is explicitly classified. Local flatness alone
does not establish global single-valued scale.

## Maximum conclusion

This gate may classify the rank of the **currently owned** relative-scale restrictions. It cannot
prove that no future native UDT restriction exists, choose an action or source, assign a physical
query family, derive a numerical `X_max`, or turn an observational fit into a law.
