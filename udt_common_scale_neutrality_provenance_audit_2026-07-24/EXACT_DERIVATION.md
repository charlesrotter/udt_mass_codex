# Exact derivation and logical separation

## 1. What Reciprocity actually derives

Use the dimension-matched pair

```text
q = (c dt, dr)^T
```

and the fixed reciprocal pairing

```text
K = [[0,1],[1,0]].
```

For a positive diagonal positional comparison

```text
P = diag(u,v),
```

exact dual-pair preservation gives

```text
P^T K P = uv K = K,
```

hence

```text
uv = 1.
```

With regular additive composition and the registered sign/unit convention,

```text
P(phi)=diag(exp(-phi),exp(+phi)).
```

This is the registered reciprocal kinematic result.

## 2. The common factor does not follow from that result

Retain the most general positive common factor:

```text
P_A = A diag(exp(-phi),exp(+phi)).
```

Then

```text
P_A^T K P_A = A^2 K,
det(P_A)=A^2.
```

If `K` is fixed and the same exact dual-pair preservation law is imposed,
positivity gives

```text
A=1.
```

Therefore the exact reciprocal comparison does not leave an arbitrary common
factor inside its `K`-preserving group. An arbitrary `A` belongs either to:

1. a separate calibration operation outside the reciprocal comparison;
2. conformal rather than exact preservation of `K`; or
3. a larger physical configuration space.

Choosing among those interpretations is not accomplished by `uv=1`.

The identity

```text
diag(u,v)
 = sqrt(uv) diag(exp(-phi),exp(+phi))
```

is only an algebraic decomposition of a general positive diagonal matrix. It
does not prove that `sqrt(uv)` is physically unobservable. The July 15 CSN
record states this correctly as a declaration:

> Common-Scale Neutrality declares the first factor calibrational.

That declaration is the extra premise.

## 3. What measured c does and does not determine

Measured Einsteinian `c_E` supplies a physical conversion between clock and
ruler dimensions. In the reciprocal metric it remains explicitly present in
the clock leg.

Under a common positive rescaling,

```text
d tau -> Omega d tau,
d ell -> Omega d ell,
```

the pointwise ratio `d tau/d ell` is unchanged. The metric null cone is also
unchanged. Thus observed `c_E` does not by itself choose `Omega`.

This prevents an overcorrection: the co-present clock-distance interpretation
does not algebraically refute local conformal equivalence merely because
`1/c_E` is physical.

But the rescaling changes physical metric quantities unless an independent
gauge/equivalence premise is supplied:

```text
proper length   -> Omega times proper length,
four-volume     -> Omega^4 times four-volume.
```

For constant `Omega` in four dimensions,

```text
sqrt(|g|) R     -> Omega^2 sqrt(|g|) R,
sqrt(|g|) C^2   -> sqrt(|g|) C^2.
```

For a nonconstant flat-space control `Omega=exp(kx)`,

```text
R[Omega^2 eta] = -6 k^2 exp(-2kx),
```

which is nonzero for nonzero `k`. Null-cone preservation therefore does not
establish physical equality of all metric observables.

Dimensional algebra also confirms that `c_E` and `G_obs` alone cannot form an
absolute length. They calibrate mass per length. A native mass, density,
curvature, boundary, or other scale-bearing output is still required to
determine `X_max`.

## 4. Exact provenance

The chronology is unambiguous:

1. The Reciprocal-c derivation obtains `uv=1`, the exponential comparison, and
   the conditional reciprocal metric. It explicitly leaves `X` and action
   open.
2. A separate July 15 owner record introduces local
   `g ~ Omega(x)^2 g` equivalence as a locked foundational postulate.
3. The July 17 cold packet carries that postulate as input and instructs the
   arms not to weaken it.
4. The July 18 C2/EH audit consequently treats exact local CSN as a class
   premise, not as a theorem rederived by the arms.
5. The July 19 premise-reset accepts `c_E` and `G_obs` at a later calibrated
   observational layer but explicitly retains the scale-free core as an owner
   ruling.
6. The current owner correction reopens that retained ruling.

Agreement among cold arms conditional on C0/C1 cannot independently establish
the truth of a premise they were forbidden to challenge.

## 5. Relation to extending GR

There is no formal contradiction in a scale-neutral fundamental theory
recovering a calibrated GR regime. It could do so through a derived section,
symmetry breaking, global closure, or another native scale-selection theorem.

The repository, however, has already verified that no current noncircular
representative selector exists. Therefore a conformal class by itself does not
yet recover the calibrated physical metric required for a complete UDT-to-GR
reduction.

Two live architectures must now be separated.

### M — physical reciprocal metric

The calibrated reciprocal metric is physical from the outset. Reciprocal
kinematics controls opposed clock/ruler dilation, while common rescaling is in
general a physical change. Ordinary unit freedom remains. The action is not
required to be locally Weyl invariant.

### C — conformal-class foundation

The local conformal class is fundamental. A native selector or breaking law
must produce the physical metric and calibrated GR regime. `C^2` remains
unique only inside its already named additional action class.

Current evidence does not derive architecture C over M. The current owner
correction makes C `CHALLENGED`, not automatically false.

## 6. Consequences for prior work

The correction is surgical:

- reciprocal kinematics survives;
- normalized shape and topology calculations survive as exact ratios and
  invariants;
- conformal cone invariance survives as mathematics;
- WR-L/SNe and the conditional finite-box Hopfion retain their scoped
  representative-specific results;
- the claim that CSN gives physical priority to pre-scale `C^2` is withdrawn
  unless CSN is separately retained;
- EH is not thereby derived;
- the representative-selection stage of the proposed bridge may be
  superfluous on architecture M;
- action, source, boundary, mass, `X_max`, and bootstrap closure remain open.

The detailed regrades are in `STATUS_LEDGER.tsv` and
`DOWNSTREAM_IMPACT_LEDGER.tsv`.
