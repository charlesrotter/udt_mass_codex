# Exact derivation

## 1. What the founding readout fixes

On a supplied observer comparison, use dimension-matched units and write

```text
g_E = diag(-1,+1),       H = diag(-1,+1).
```

`H` is the infinitesimal reciprocal response: `-1` on the clock channel and `+1` on the ruler
channel. It is self-adjoint with respect to `g_E`, and its two eigenlines have opposite causal
signs. Consequently the metric and operator together mark the clock and ruler eigenlines
intrinsically. Their simultaneous stabilizer is only four independent sign choices; there is no
continuous boost that preserves both objects separately.

This result retains the exact premise stamp from the source: the reciprocal pair action is founded,
while its Lorentzian physical-metric interpretation uses the recorded `DECLARED READOUT /
SR-CONTINUITY` premise.

## 2. Mixed components versus a mixed physical pair

Under a passive basis change `S`, both objects must transform:

```text
g_E' = S^T g_E S,        H' = S^-1 H S.
```

The transformed components can both be nondiagonal, but self-adjointness survives. So does

```text
I = tr(g_E^-1 H^T g_E H) = 2.
```

If the metric is transformed while `H` is artificially left diagonal, self-adjointness and `I=2`
generally fail. That operation changes the metric/operator pair; it is not a new chart for the same
pair.

The exact swap-isometric witness

```text
g_mix = [[1,-2],[-2,1]],       H = diag(-1,+1)
```

has Lorentzian determinant `-3`, but `H` is not self-adjoint and `I=-10/3`. It is therefore not a
basis presentation of the founded pair. It remains valid counterfactual algebra, but adopting it as
the physical clock/ruler readout would replace the recorded declared-readout premise.

## 3. The complete metric need not be coordinate block diagonal

Mark the founded nondegenerate two-plane `E` but make no assumption about the chosen complementary
coordinates. Every complete symmetric metric with the exact pair restriction has block form

```text
G = [[g_E, W],
     [W^T, Q]].
```

The metric is Lorentzian with one negative direction exactly when the Schur complement

```text
Q_perp = Q - W^T g_E^-1 W
```

is positive definite. Thus all four entries of `W` may be nonzero. A local complement change that
fixes every vector in `E` pointwise sends `G` to `diag(g_E,Q_perp)`. This proves two different facts:

- coordinate pair/screen cross terms do not change the intrinsic founded-pair metric; and
- their local removability does not prove a globally flat connection, path-independent transport,
  or trivial holonomy.

The exact witness `W=diag(1/4,1/4)` and `Q=I` has
`Q_perp=diag(17/16,15/16)`, so nonzero cross terms and the exact founded pair coexist in a regular
Lorentz metric.

## 4. Why coframe block orientation matters

For a positive screen metric, the earlier triangular lower-shift coframe family has schematic form

```text
E_lower = [[P,0],
           [C,I]].
```

Its total metric restricted to the founded base is

```text
P^T g_E P + C^T C.
```

Over the reals, `C^T C=0` implies `C=0`. A nonzero lower shift therefore preserves the displayed
top-left transformation slots but not the exact physical metric restriction of the founded pair.
It is a projection/slot extension, not a counterexample to invariant physical-pair alignment.

The dual upper-shift family

```text
E_upper = [[P,D],
           [0,I]]
```

does preserve the base metric restriction while allowing pair/screen metric cross terms. It no
longer retains a literal direct-sum coframe presentation. These two families explain why “mixed
coframe,” “mixed metric components,” and “mixed physical clock/ruler readout” cannot be used as
synonyms.

## 5. Invariant self-adjoint complete extensions

Use the intrinsic orthogonal splitting `E direct-sum E_perp`. A general metric-self-adjoint complete
response with founded top-left compression is

```text
X = [[H, g_E^-1 B^T Q_perp],
     [B, D]],
```

where `D` is self-adjoint on the positive screen. The four entries of `B` mix the founded pair into
the screen. Merely fixing the top-left block does not set them to zero.

If `E` is required to be invariant, then `B=0`. Self-adjointness immediately makes the upper block
zero as well. Equivalently, for `e in E` and `s in E_perp`,

```text
G(Xs,e)=G(s,Xe)=0,
```

so `Xs` also lies in `E_perp`. Therefore

```text
X = H direct-sum D.
```

This is the coordinate-free result: a nondegenerate invariant pair of a self-adjoint physical
response automatically brings an invariant orthogonal complement.

`D` still has three symmetric components. Only after separately imposing screen-rotation
equivariance does `D=lambda I`. Complete trace zero would then set `lambda=0`; neither screen
equivariance nor complete trace zero follows from the founded pair restriction.

## 6. Local closure and global remainder

The local fork is now closed under current premise precedence:

- the founded physical pair is aligned under its declared readout;
- a genuinely mixed fixed-operator readout is a different premise branch, not gauge;
- complete coordinate cross terms remain allowed;
- a true self-adjoint invariant-pair extension has no intrinsic pair/screen mixing; and
- the screen response remains unselected.

What is not closed is the global object. The foundation supplies a reciprocal pair for a positional
comparison, but it does not yet supply one smooth universal rank-two subbundle, an event-pairing
path, transport between comparisons, overlap maps, or cut-locus handling. A pair-indexed relational
family therefore remains more strongly supported than a single global pair field, but that family
still needs a consistency law.

