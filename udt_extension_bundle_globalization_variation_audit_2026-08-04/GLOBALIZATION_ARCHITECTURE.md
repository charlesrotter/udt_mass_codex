# Globalization architecture

Date: 2026-08-04

## Short result

The local `3+4` extension chart is not stranded merely because spacetime lacks one global coframe.
Its coordinate-free screen metric and mixing data can live on nontrivial bundles. The extension fiber
therefore adds no new existence obstruction after a reciprocal query/reduction has been supplied.

That statement does not globalize the reciprocal realization itself and does not choose a law.

## Object hierarchy

```text
supplied regular Lorentzian metric/coframe atlas
  |
  +-- total associated ordered pair-frame query bundle P -> M
  |     no global observer/ruler section required
  |     |
  |     +-- tautological reciprocal 2-plane N in pi*TM
  |     +-- pullback screen Q = N^(perp_(pi*g))
  |     +-- extension fiber SPD(Q) x Hom(N,Q)
  |
  +-- optional realized reciprocal field over spacetime
  |     requires a global section/reduction and smooth split TM=N+Q: OPEN
  |     |
  |     +-- screen bundle Q
  |     +-- extension fiber SPD(Q) x Hom(N,Q)
  |
  +-- optional branch-derived reciprocal section
        available only where an intrinsic construction is regular
```

## What needs a section

| Object | Global section required? | Current status |
|---|---:|---|
| Pair-frame query bundle | No | container derived on a supplied regular metric |
| One physical observer/ruler field | Yes | open and not selected |
| Screen positive metric after smooth `N,Q` bundles are supplied | A section exists | no additional existence obstruction |
| Mixing bundle | A section exists; zero is canonical | no additional existence obstruction, but zero is not selected |
| Global triangular `D` matrix | Yes, as a strong frame choice | not required |
| Global complete coframe | Yes | stronger conditional witness, not required |
| Parallel pair-screen split | Yes plus connection reduction | branch-conditional, not foundational |

## Transition-family disposition

All seven preregistered families remain in `TRANSITION_FAMILY_LEDGER.tsv`. In particular:

- nontrivial screen bundles survive;
- reversal-twisted reciprocal cocycles survive algebraically, but their physical metric lift remains
  conditional;
- global coframes survive as strong witnesses but are not promoted to a parent requirement;
- rank-changing objects remain outside this smooth tile rather than being filtered out.

## Variation-domain fork

The same vertical displacement can have different meanings in different architectures:

- changing an observer/ruler pair in the query bundle is a query change, not a field variation;
- changing a realized reciprocal field would be a physical section variation, if that architecture
  and ownership are selected;
- changing a branch-derived reciprocal object follows from variation of its parent metric by the
  chain rule wherever the construction is regular.

This is why the bundle architecture must be typed before an action can be varied honestly.

The component transition law must also be typed. With

```text
x_N,j=P_ij x_N,i,
x_Q,j=Q_ij x_Q,i,
```

the tensor data obey

```text
h_j=Q_ij^-T h_i Q_ij^-1,
sigma_j=Q_ij sigma_i P_ij^-1.
```

Arbitrary ambient `GL(4)` coframe transitions need not preserve the local triangular `3+4` chart.
The global statement is therefore about the associated tensor bundles after a smooth split is
supplied, not about one triangular matrix surviving every overlap.

## Maximum allowed use

This architecture can constrain future candidate laws: a law must be well defined on the selected
bundle architecture and respect its transition data, or explicitly and consistently break/reduce it.
It cannot select `C^2`, EH, `S^2`, `L2+L4`, a source, or a boundary functional by itself.
