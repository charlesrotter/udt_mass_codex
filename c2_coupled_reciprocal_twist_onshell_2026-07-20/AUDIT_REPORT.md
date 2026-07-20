# Coupled reciprocal-background/full-Bach twist selector audit

Date: 2026-07-20  
Base: `2d2809ca7c83d9262d8db99d7962806c9487dfff`  
Preregistration commit: `89bf079`  
Compute: CPU-only exact SymPy full Bach algebra and independent Torch forward-AD component replay  
Status: **VERIFIED-WITH-CAVEATS** — complete in the declared local tile; no fresh external-model
review was authorized.

## Result first

Putting the reciprocal background on the full conditional `C2` equation does **not** select the sign
of the lower-order transverse-twist term. It restricts the background to an exact constrained-cubic
family, but that family permits positive, zero, and negative coefficient strata—even within one
smooth positive local branch.

Define the positive reciprocal clock factor

```text
y(r) = exp(-2 p(r)).
```

The twist-free curvature-squared density becomes exactly

```text
L_background = y_second^2 / 3.
```

Restricted variation of this one function gives

```text
y_fourth = 0.
```

The complete four-dimensional Bach tensor adds the independent transverse constraint

```text
2 y_first y_third - y_second^2 = 0.
```

Together, these equations are necessary and sufficient for every Bach component in this tile. Their
complete local solution is

```text
y = A r^3 + B r^2 + C r + D,
B^2 = 3 A C,
y > 0 on the local interval.
```

The parent audit's twist coefficients become

```text
higher-order coefficient = y^2,
lower-order coefficient  = -(2/3) y y_second.
```

The first is positive. The second is not selected. The admissible branch `y=2-r^3` is positive on
`[-1/2,1/2]` and has

```text
Q = p_second - 2 p_first^2 = 3r/(2-r^3),
```

which is `-12/17`, `0`, and `4/5` at `r=-1/2,0,1/2` respectively.

The exact registered outcomes are:

```text
FULL_BACH_PERMITS_MULTIPLE_Q_STRATA
REDUCED_STATIONARITY_FALSELY_SELECTS_EXTRA_BRANCHES.
```

Maximum conclusion:

`CONDITIONAL_LOCAL_FULL_BACH_RECIPROCAL_BACKGROUND_TWIST_COEFFICIENT_STRATUM_CHARACTERIZED`.

## Lay reading

The previous audit found that one metric law naturally creates the two mathematical effects used by
the old finite-box particle model within its stated carrier premises. But the strength and sign of
the ordinary-twist effect depended on the clock-dilation background.

This audit made that background obey its own full metric equation. The equation narrows the possible
clock curves to a special cubic family. That is a substantial simplification—but it still does not
choose one curve. A permitted curve can favor twist on one side, be neutral at a point, and oppose
it on the other side.

So the bridge survives, but local dynamics does not close it. The missing selection has moved into
view: intrinsic angular geometry, the finite-cell boundary, or the whole-universe bootstrap must
choose which cubic and which physical region are realized.

## Exact full-tensor equations

At zero twist the scalar curvature and `C2` density are

```text
R  = 2 (p_second - 2 p_first^2) exp(-2p),
C2 density = (4/3) (p_second - 2 p_first^2)^2 exp(-4p).
```

The full covariant Bach tensor has four nonzero diagonal entries, with the two transverse entries
equal. Their exact unabridged expressions are in `BACKGROUND_DERIVATION.json`. The tensor is
symmetric and trace-free exactly.

Writing `y=exp(-2p)` exposes the system without dividing by `Q` or assuming nonzero curvature. The
reduced equation becomes `y_fourth=0`. One independent full-tensor component becomes

```text
-2 y_first y_third + y_second^2 = 0.
```

Exact component identities prove that these two equations imply both remaining diagonal equations;
they are therefore a necessary-and-sufficient local system, not selected component samples.

## Why the full metric variation mattered

The one-function reduced action accepts every cubic `y`. The full tensor equation accepts only
cubics satisfying `B^2=3AC`.

The positive comparison `y=1+r^2` has `y_fourth=0`, so it is reduced-stationary. Its omitted
transverse constraint numerator is `4`, so it is not Bach-flat. This is an exact counterexample to
using the attractive reduced clock equation as the complete UDT equation.

The reduced Euler expression equals `-4` times the full raised-index metric-path projection in the
recorded conventions. Its complete endpoint variation in `p` is retained in
`BACKGROUND_DERIVATION.json`; no endpoint condition or boundary action was chosen.

## Complete local branch classification

Because `y_fourth=0`, every local solution is cubic. Substitution into the full transverse
constraint gives exactly

```text
4(B^2 - 3AC) = 0.
```

This classification includes the zero-curvature stratum rather than dividing it away. Linear
positive `y` has `Q=0`; nonzero cubic branches can have either sign and may cross zero. Positivity of
the metric on a chosen interval restricts the constants but does not locally force one sign.

This is not a global solution classification. Caps, a finite-cell seal, angular topology, and
bootstrap closure can eliminate local branches or select their constants. None is supplied in this
flat tile.

## Independent verification

The verifier reuses the already banked independent Torch forward-AD coordinate tensor/Bach engine,
not the SymPy expressions. At the preregistered `P1`, `P2`, and constant `P3` profiles it compared
all sixteen Bach components at eight points:

- component records: `128`;
- nonzero records: `24`;
- maximum nonzero scaled error: `5.017742234854814e-15` against `1e-8`;
- maximum zero-component absolute error: `0.0` against `1e-9`;
- constant-profile control: `0.0`;
- transverse-component witness magnitude: `0.6335310293911997`.

Thus the independent replay explicitly exercises the component that the reduced equation omits.
The algebraic branch classification is exact SymPy arithmetic. No fresh external-model review was
authorized.

## What this does to the matter lead

The result neither closes nor kills the geometric parent route:

- favorable nonzero full-Bach backgrounds exist locally, so the lower-order twist term is not merely
  an off-shell artifact;
- unfavorable and zero backgrounds also exist, so no coefficient or stability conclusion follows;
- the same branch can change sign, so a radial orientation or selected physical region cannot be
  silently assumed;
- no section, topology, carrier, scale, source, boundary charge, or time-live stability has appeared.

The clearest remaining selector is no longer another local scalar premise. It is the omitted join
between reciprocal dilation and intrinsic angular/global geometry.

## Premise and provenance firewall

- `C2` remains `UNIQUE-CONDITIONAL` only under the frozen pre-scale metric-only/local/4D bulk
  premises. It is not declared the complete UDT action.
- The reciprocal exponential block retains its existing conditional premise stamps.
- No GR field equation, EH law, carrier, `S2`, `L2+L4`, source, physical scale, fitted coefficient,
  cutoff, or GPU calculation entered.
- The independent Torch engine is a banked separate coordinate implementation; its source is
  disclosed in `VERIFICATION_RESULT.json`.
- Controlling source blobs and SHA-256 hashes are recorded in `SOURCE_LINEAGE.tsv`.

## Four banking gates

1. **Preregistered:** yes, commit `89bf079`, before inspecting the background result.
2. **Full space or bounded scope:** complete for all local analytic branches of the declared
   twist-free reciprocal direct-product tile and every full Bach component. Angular curvature,
   global boundary, topology, time dependence, and unrestricted metrics remain open.
3. **Independently verified:** yes, 128 component records from a separate Torch forward-AD Bach
   engine; no fresh external-model review.
4. **Every premise audited:** yes for the bounded verdict; the conditional action, representative,
   flat transverse slice, absent boundary, angular, bootstrap, carrier, source, and scale are
   explicit.

Banked grade: **VERIFIED-WITH-CAVEATS**.

## Scientific decision

Do not fit a cubic, select a favorable radial side, or launch a flat-tile GPU search. The next
bounded derivation should restore intrinsic angular curvature, transverse area/shear, and the twist
connection in one reciprocal 2+2 coframe. Its full Bach and boundary equations should be tested for
whether they select the `Q` stratum. That is the smallest current metric-led join capable of turning
this local family into a genuine selector.
