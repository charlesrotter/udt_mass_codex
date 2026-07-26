# Exact derivation

## 1. Complete reciprocal-pair readout

Let

```text
H=[[A,B],[B,C]],
X=diag(-1,+1),
F_b=[[0,b],[1/b,0]].
```

`H` is Lorentzian exactly when

```text
AC-B^2<0.
```

Self-adjoint reciprocal dilation requires

```text
X^T H-HX=[[0,-2B],[2B,0]]=0,
```

so `B=0`. Lorentz signature then requires `A` and `C` to have opposite
signs. The reciprocal eigenlines are orthogonal and opposite causal. The
founding calibrated readout `diag(-1,+1)` is this class.

## 2. Complete inverting-isometry family

Direct multiplication gives

```text
F_b^T H F_b-H
 = [[C/b^2-A,0],[0,A b^2-C]].
```

Thus `F_b` is an isometry exactly when

```text
C=A b^2.
```

The determinant becomes

```text
A^2 b^2-B^2,
```

so Lorentz signature requires `B^2>A^2 b^2`; in particular `B` is nonzero.
The two reciprocal eigenlines have norms `A` and `A b^2`: the same sign when
`A` is nonzero, or both are null when `A=0`. They cannot be the aligned
timelike clock and spacelike ruler.

## 3. Positive conformal freedom cannot repair the conflict

Suppose

```text
F_b^T H F_b=Omega^2 H,
Omega^2>0.
```

Because `F_b^2=I`, applying the relation twice gives

```text
H=Omega^4 H.
```

For nondegenerate `H` and positive `Omega^2`, this forces `Omega^2=1`.
Therefore the positive-conformal class is exactly the isometry class. It
cannot swap opposite causal lines.

Intersecting with self-adjointness gives

```text
B=0,
C=A b^2,
det H=A^2 b^2>0,
```

or a degenerate zero case. There is no Lorentzian intersection.

Invariantly, a positive-conformal metric map preserves causal sign. If it
conjugates `X` to `-X`, it maps the `-1` eigenline to the `+1` eigenline. It
therefore cannot map a timelike reciprocal clock eigenline to a spacelike
reciprocal ruler eigenline.

## 4. What the mixed family means

The exact witness

```text
H=[[1,-2],[-2,1]]
```

is Lorentzian and invariant under the swap. It has an orthonormal Lorentz
frame, so observed `c_E` can calibrate it after a frame choice. But that
physical frame is a mixture of the reciprocal eigenchannels. In it, `X` is
not diagonal.

Relative to the mixed `H`, `X` has both a metric-self-adjoint strain part and
a metric-skew frame part. In the limiting dual readout

```text
K=[[0,1],[1,0]],
```

both reciprocal eigenlines are null, `X` is entirely metric-skew, and
`D(phi)^T K D(phi)=K`; the isolated metric block loses all `phi` visibility.

Thus mixed inversion compatibility is real mathematics, but it changes the
physical interpretation of the reciprocal channels.

## 5. Complete four-dimensional self-adjoint blocks

For

```text
X_lambda=diag(-1,+1,lambda,lambda),
```

self-adjointness forces metric cross terms between unequal eigenspaces to
vanish.

- Generic `lambda`, including zero: `1+1+2` blocks, five readout parameters.
- `lambda=+1`: `1+3` blocks, seven parameters.
- `lambda=-1`: `3+1` blocks, seven parameters.

The aligned metric `diag(-1,+1,+1,+1)` is self-adjoint for every `lambda`.
At `lambda=0`, a complete reciprocal swap conjugates `X` to `-X` but is not
an isometry or positive conformal isometry of that aligned metric. Replacing
the base block by the mixed family makes the swap isometric while losing
self-adjoint aligned clock/ruler channels.

## 6. Ruling

The founding aligned local readout conditionally rules out the physical
inverting-isometry interpretation. It does not rule out:

- an internal sign-twisted reciprocal bundle;
- a conditional mixed physical readout whose clock is not a reciprocal
  eigenline; or
- ordinary trivial/screen-only holonomy branches at any `lambda`, including
  zero.

Nor does it select the larger ordinary `lambda=+1` or `lambda=-1` holonomy
reductions. The remaining decision is a complete-coframe solder/readout and
global-branch question.
