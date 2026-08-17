# G136 exact derivation — what “distance” can mean in the reciprocal kernel

Date: 2026-08-17

## 1. Start with the completed pair, not an external distance

For a supplied regular calibrated complete pair metric, the full orchestra has already entered
`h`. Its unique positive clock/ruler densities give

```text
phi_pair=(1/2)log(L/T),
chi=(L-T)/(L+T)=tanh(phi_pair).
```

G135 derives `chi` as the contrast/common projective slope of the completed reciprocal pair. G136
does not attach a distance correction afterward.

## 2. Classification over all continuous same-law coordinates

Let `F:R->(-1,1)` be a continuous strictly increasing coordinate satisfying

```text
F(0)=0,
F(-phi)=-F(phi),
lim(phi->+/-infinity)F(phi)=+/-1,
F(phi+psi)=(F(phi)+F(psi))/(1+F(phi)F(psi)).
```

Define

```text
H(phi)=atanh(F(phi)).
```

The addition identity for `atanh` makes `H(phi+psi)=H(phi)+H(psi)`. Continuity excludes pathological
Cauchy solutions, so

```text
H(phi)=k phi,
F(phi)=tanh(k phi)
```

for a constant `k>0`. Equivalently, differentiating the composition law at the identity gives

```text
F'(phi)=k(1-F(phi)^2),
F(0)=0,
```

whose unique regular solution is the same family.

The founding derivation explicitly chooses the sign and unit of `phi`, but that choice alone does
not impose the slope of a separately defined physical-position coordinate. The same-law
classification therefore leaves `k>0`. If the physical normalized-position unit is separately
fixed by the local convention `F'(0)=1`, then `k=1` and

```text
F(phi)=tanh(phi)=chi.
```

This strengthens G135: within all continuous charts obeying the same Mobius law and an explicitly
chosen unit position slope, not merely first-degree projective charts, the coordinate is unique.
Neither `c_E` nor endpoint saturation imposes this slope.

G135's smooth endpoint-preserving re-markings do not contradict the theorem. They compose only
under a conjugated law. The exact slope-matched witness

```text
g(x)=x+(1/4)x^3(1-x^2)
```

fails the same Mobius law by `390123/25975936` at `x1=1/3`, `x2=1/5`. G135's separate
`-45/29728` witness uses its non-slope-matched `f_epsilon` family; both demonstrate the same
coordinate-law distinction.

## 3. What the theorem does not prove

The proof begins with the requirement that physical normalized position is a coordinate on the
completed reciprocal orbit and uses that orbit's same composition law. Algebra cannot decide that
type assignment.

The frozen sources do not presently entail it:

- the original provenance explicitly says the word “distance” was unspecified;
- the founding derivation starts from supplied ordered depth and chooses its sign/unit;
- the older hyperbolic derivation labels the distance-like chart as a `NAMED identification`;
- the current `X_max` correction leaves tanh and other profiles open;
- current co-presence means event co-membership in a supplied solution and does not supply depth;
- G135 explicitly leaves the operational physical-separation identification open.

Therefore the remaining statement is not another mechanism or fitted function. A minimal
foundational clarification can avoid naming the answer:

> Physical normalized position for a regular co-present observer pair is a continuous strictly
> increasing coordinate of the completed reciprocal relation, carries that relation's native
> Mobius composition law, and uses the local unit convention `F'(0)=1`.

If Charles adopts that statement, the classification derives rather than presupposes the formula:

```text
signed x/X_max=chi=tanh(phi_pair),
nonnegative separation/X_max=abs(chi).
```

## 4. What remains distinct

Even after adoption:

- `x` is compositional observer-pair position, not automatically path proper length or areal radius;
- `X_max` supplies dimensional scale but its numerical value and global realization remain open;
- signed orientation and nonnegative separation remain distinct types;
- the physical pair realization and the numerical complete metric history remain open;
- causality constrains admissible observation and signal relations but co-presence does not imply
  instantaneous signalling.

The dimensional composition law would be

```text
x12=(x1+x2)/(1+x1 x2/X_max^2).
```

This is the exact positional counterpart of writing an additive hyperbolic parameter in a bounded
coordinate. It is not a claim that positional distance is velocity.
