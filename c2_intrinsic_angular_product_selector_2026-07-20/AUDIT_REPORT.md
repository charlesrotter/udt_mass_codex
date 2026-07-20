# Intrinsic-angular product selector audit

Date: 2026-07-20  
Base: `8860d4229a4daaea358450df8ce53762e5502a21`  
Preregistration commit: `852389d`  
Compute: CPU-only exact SymPy full-tensor algebra and independent Torch forward-AD replay  
Status: **VERIFIED-WITH-CAVEATS** — complete only in the declared local product tile; a fresh
external-model review was not authorized.

## Result first

Intrinsic angular curvature enters both the reciprocal-background equation and the transverse-twist
operator, but it does **not** select a unique background or one sign of the lower-derivative twist
response.

For

```text
e0 = sqrt(y) dt,
e1 = dr/sqrt(y),
e2 = d theta,
e3 = F(theta) [d psi + epsilon u(r) d theta],
F_second + K F = 0,
```

the twist-free Weyl-squared action density is

```text
sqrt(-g) C2 = F (y_second - 2K)^2 / 3.
```

Full Bach stationarity is equivalent locally to

```text
y_fourth = 0,
y_second^2 - 2 y_first y_third - 4 K^2 = 0.
```

Hence every local analytic branch is

```text
y = A r^3 + B r^2 + C r + D > 0,
B^2 = 3 A C + K^2.
```

Nonzero `K` shifts the algebraic constraint; it does not remove the continuous family or its
positive, zero, and negative reciprocal-curvature strata.

The exact quadratic twist action density is

```text
L2 = F^3 [
       y^2 u_second^2
       + (y/3) {4K - 2 y_second + 27 (F_first/F)^2} u_first^2
     ].
```

Thus intrinsic curvature adds a genuine lower-derivative contribution, but the chosen twist also
sees the directional screen connection `F_first/F`. Scalar Gaussian curvature `K` alone does not
specify that directional data. A constant `u` remains an exact local coordinate-shear zero mode.

The registered outcomes are

```text
INTRINSIC_CURVATURE_DOES_NOT_CHANGE_LOCAL_SELECTOR_UNDERDETERMINATION
INTRINSIC_CURVATURE_CHANGES_TWIST_DERIVATIVE_INVENTORY.
```

Maximum conclusion:

`CONDITIONAL_LOCAL_C2_INTRINSIC_ANGULAR_PRODUCT_SELECTOR_CHARACTERIZED`.

## Lay reading

We put a curved angular screen beside the reciprocal clock geometry and asked whether their mutual
curvature equations finally choose one allowed universe-clock profile and one favorable twist
response.

They do interact. The angular curvature changes the allowed clock curves and adds an ordinary
twist-like term to the same metric expression that already supplies the higher-derivative term.
That is useful structural evidence.

But it still does not make the choice. Many clock curves remain allowed, and one allowed positive
curve can make the lower-order twist coefficient positive, zero, and negative at different places.
The calculation also exposes why a scalar curvature number was insufficient: a twist points along a
particular angular direction, and its response retains information about how that direction turns
across the screen.

So this audit did not hit a dead end. It located the next missing join more precisely. The full
transverse coframe—its area, shear, directional connection, and global completion—must participate
before the angular sector can honestly be tested as a selector.

## Exact background classification

At zero twist,

```text
R = 2K - y_second,
C2 = (y_second - 2K)^2/3.
```

Restricted variation of `y` gives `y_fourth=0`. The full four-dimensional Bach tensor adds the
second equation above. Both are necessary and sufficient for every nonzero Bach component when
`y>0`; no component was discarded.

Substituting the general cubic into the full constraint gives exactly

```text
4 (B^2 - 3 A C - K^2) = 0.
```

The positive `K=1` witness

```text
y = r^3 - r/3 + 2,   r in [-1/2,1/2]
```

satisfies full Bach. Its reciprocal curvature `Q=-y_second/(2y)` is positive at `r=-1/2`, zero at
`r=0`, and negative at `r=1/2`. At the registered equatorial angular point, the complete lower twist
coefficient is positive at `r=0`, zero at `r=1/3`, and negative at `r=1/2`.

The comparison `K=1, y=2+2r^2` obeys the reduced fourth-order equation but violates the full
transverse constraint by `12`. It is an exact warning against treating a one-function reduction as
the complete metric equation.

## Twist action and directional data

The calculation includes the exact `epsilon^2 u^2 F^2` metric backreaction before expanding
`sqrt(-g) C2`. The linear term vanishes; the quadratic term is even under `u -> -u`; no
undifferentiated `u` appears; and both endpoint-variation channels are retained.

For `K=0,F=1`, the result reduces exactly to the parent Cartesian tile:

```text
L2 = y^2 u_second^2 - (2/3)y y_second u_first^2.
```

For a general constant-curvature chart, `F_first/F` remains. This is not a failure of covariance or
an extra physical field. It says that the selected coordinate twist is directional data. Demanding
that its local coefficient depend on scalar `K` alone would have silently imposed the missing
section/framing instead of deriving it.

## Independent verification

The verifier independently reconstructs the metric, determinant, connection, Riemann tensor,
Ricci tensor, Weyl tensor, full Bach tensor, and `sqrt(-g) C2` using Torch forward automatic
differentiation. It does not import the SymPy formulas.

- Bach component records: `288`;
- twist records: `24`;
- maximum nonzero Bach scaled error: `6.776684983100927e-14`;
- maximum zero Bach absolute error: `4.179891099825019e-17`;
- maximum nonconstant-twist scaled error: `1.5488354459819203e-09`;
- constant-twist finite-amplitude invariance: `2.6645352591003757e-15`;
- omitted-angular-derivative mutation difference: `0.662627161405321`;
- missing-backreaction mutation difference: `2.4768979400846547e-07`.

The registered nonzero tolerance was `1e-8`; the zero tolerance was `1e-9`. A cancellation-prone
second-difference diagnostic and the pre-bank action-density correction are preserved rather than
hidden in `VERIFIER_ZERO_MODE_CORRECTION.md` and `ACTION_DENSITY_CORRECTION.md`.

## What remains open

This product control freezes transverse area and shear, uses one toric directional twist, stays
static and local, and supplies no cap, period, topology, finite-cell seal, boundary action, or
bootstrap condition. Therefore it does not determine the intrinsic angular shape, select a section,
derive a carrier, or close the reciprocal–angular field equations.

The conditional `C2` action remains `UNIQUE-CONDITIONAL` only in its frozen pre-scale action class.
No EH equation, GR field equation, `S2` carrier, `L2+L4` matter action, source, physical scale,
electron anchor, mass, or GPU computation entered.

## Four banking gates

1. **Preregistered:** yes, commit `852389d`, before inspecting the result.
2. **Full space or bounded scope:** complete for every local analytic twist-free background branch
   and the exact quadratic twist operator of the declared product coframe. Area, shear, unrestricted
   angular dependence, global boundary, topology, and time remain open.
3. **Independently verified:** yes, by a separate Torch coordinate implementation at all registered
   witnesses. No fresh external-model review was authorized.
4. **Every premise audited:** yes for the bounded verdict; the action, representative, local
   constant-curvature seed, omitted coframe sectors, boundary, topology, carrier, scale, and source
   are explicit.

Banked grade: **VERIFIED-WITH-CAVEATS**.

## Scientific decision

Do not select a favorable cubic, fix `K=+1`, choose an equator, or reinterpret the directional twist
as a derived carrier. The smallest next metric-led task is a gauge-invariant transverse-coframe
closure audit: restore area and shear, express twist through the complete screen connection, and
then determine whether the full coupled Bach plus boundary equations reduce the branch family. That
is algebra first; no GPU search is justified yet.
