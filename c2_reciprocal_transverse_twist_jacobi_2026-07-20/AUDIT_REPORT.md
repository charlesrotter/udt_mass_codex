# Reciprocal-background transverse-twist C2 Jacobi audit

Date: 2026-07-20  
Base: `ee5690c49f27d230e5b802d08af9e36b5213f5ae`  
Preregistration commit: `ccf8384`  
Compute: CPU-only exact SymPy curvature algebra plus independent Torch forward-AD tensor/Bach replay  
Status: **VERIFIED-WITH-CAVEATS** — exact within the registered local quadratic tile; no fresh
external-model review was authorized.

## Result first

The lead was worth pursuing. Coupling a genuine transverse metric twist to an arbitrary reciprocal
dilation background makes the single conditional pre-scale `C2` invariant generate **both** a
higher-derivative and a lower-derivative twist term. No `S2` carrier and no historical `L2+L4`
particle action were inserted.

For the coframe

```text
e0 = exp(-p(r)) dt
e1 = exp(+p(r)) dr
e2 = dx
e3 = dy + epsilon u(r) dx,
```

the determinant is exactly `-1`, and the coefficient of `epsilon^2` in
`sqrt(-g) C_abcd C^abcd` is

```text
L_twist = exp(-4p) [ u_second^2
          + (4/3)(p_second - 2 p_first^2) u_first^2 ].
```

The coefficient of `u_second^2` is positive for every finite real `p`. The lower-order coefficient
is positive, zero, or negative according as `p_second` is greater than, equal to, or less than
`2 p_first^2`. The current calculation does not select that reciprocal background, so it derives the
two-order structure but leaves its physical sign and relative weight open.

The exact outcome combines two preregistered classes:

```text
BACKGROUND_CURVATURE_GENERATES_BOTH_DERIVATIVE_ORDERS
TWIST_OPERATOR_SIGN_OR_BRANCH_DEPENDENT.
```

Maximum conclusion:

`CONDITIONAL_LOCAL_C2_RECIPROCAL_TRANSVERSE_TWIST_JACOBI_STRUCTURE_CHARACTERIZED`.

## Lay reading

The earlier stable Hopfion needed two mathematical effects: one penalized ordinary distortion and
one penalized sharper twisting. Their balance kept the configuration from simply spreading out or
collapsing, but that two-term carrier model had been supplied as a premise.

Here, one metric curvature law produced both kinds of response by itself. The sharper-twist term is
always present. The ordinary-twist term appears because the twist lives inside a dilated clock/ruler
background. This is the clearest evidence yet that the old two-term balance might be a shadow of one
geometric parent rather than two independently chosen matter terms.

It is not closure. We have tested a small static wrinkle in one direction, not a complete linked
three-dimensional object. The background was held arbitrary instead of solving its own equation, so
the second term can help or hurt stability. The next honest gate is to solve the background and twist
together and see whether the metric selects the favorable branch.

## Exact algebra and zero modes

The full coordinate connection, Riemann tensor, Ricci tensor, scalar, Weyl tensor, and Weyl-squared
density were constructed from the metric. The scalar curvature is

```text
R = ( -epsilon^2 u_first^2 - 8 p_first^2 + 4 p_second ) exp(-2p) / 2.
```

The twist-linear density vanishes. The quadratic density contains no undifferentiated `u`, is even
under `u -> -u`, and vanishes for constant `u`. That constant mode is a coordinate shear rather than
physical local winding.

The exact fourth-order Jacobi operator is stored without abbreviation in
`DERIVATION_RESULT.json`. In the flat-profile limit it reduces to the variation of
`exp(-4p) u_second^2`; all lower-order background terms disappear.

The complete endpoint variation was not discarded. Its two coefficients are

```text
delta u:
  (2/3) exp(-4p) [ -8 p_first^2 u_first + 12 p_first u_second
                    +4 p_second u_first -3 u_third ]

delta u_first:
  2 exp(-4p) u_second.
```

Direct symbolic integration by parts leaves exactly zero remainder after separating the bulk
Jacobi operator and this endpoint current. No physical endpoint condition, boundary action, or
boundary charge is thereby selected.

## Independent tensor/Bach verification

The independent verifier uses Torch forward automatic differentiation and reconstructs the metric,
connection, curvature, Weyl tensor, Weyl divergence, and Bach tensor directly. It does not call the
SymPy derivation.

Across ten preregistered points in two nontrivial profiles, a flat control, and a constant-twist
control:

- maximum quadratic-density relative error: `3.229666020728108e-09` against `1e-8`;
- action-Jacobi/full metric-path Bach ratio: `-7.999999999999781`;
- ratio spread: `5.845990358466224e-12` against relative `1e-7`;
- constant-twist maximum absolute value: `1.1796119636642288e-10` against `1e-9`;
- missing metric-backreaction mutation difference: `0.6192986571248871`;
- Euclidean-time mutation difference: `9.025268310480783e-10`.

The Bach comparison must follow the complete coframe-induced metric path. Because
`g_xy=epsilon u` and `g_xx=1+epsilon^2 u^2`, the required raised-index projection is

```text
(d B^xy / d epsilon)|_0 + u B^xx|_0.
```

The background term exactly cancels the spurious constant-coordinate-shear component. The two
pre-bank verifier corrections are preserved rather than hidden.

The static quadratic density happened to be signature-independent under the registered
Euclidean-time mutation. That is a classified observation, not a Lorentzian stability statement.

## Relation to the nonround Hopfion

The result strengthens, but does not complete, the Hopfion lead:

1. The banked configuration is a genuine full-3D, toroidal, nonround Hopf texture inside its stated
   finite-box and carrier premises.
2. This audit shows that a genuine off-diagonal **metric** twist naturally obtains the two derivative
   orders that were previously supplied in the carrier action.
3. No gauge-invariant section, Hopf topology, round target, global soldering, scale, or time-live
   stability was derived here.

Thus the overlap is structural, not yet an identity between the metric twist and matter.

## Why the sign is still decisive

The arbitrary local background permits exact witnesses for all three strata:

- `p_first=0, p_second=1`: positive lower-order coefficient;
- `p_first=1, p_second=2`: zero lower-order coefficient;
- `p_first=1, p_second=0`: negative lower-order coefficient.

Nothing in this tile prefers one. A favorable hand-picked profile would therefore be a fit, not a
UDT result. The missing information is now concrete: the jointly varied reciprocal-background
equation, with its admissible global boundary/bootstrap completion, must select or reject a stratum.

## Premise and provenance firewall

- `C2` remains `UNIQUE-CONDITIONAL` only in the already frozen pre-scale metric-only/local/4D bulk
  class. It is not declared the complete native action.
- The reciprocal exponential block is used with its existing conditional premise stamps.
- The transverse twist is free and varied; the reciprocal profile is an arbitrary off-shell
  background.
- No GR field equation, EH action, fluid, Standard Model field, quantum mechanism, carrier, `S2`,
  `L2+L4`, source, fitted coefficient, physical cutoff, or GPU computation entered.
- Pre-July and historical material supplies no affirmative UDT physics. Exact controlling source
  blobs and hashes are recorded in `SOURCE_LINEAGE.tsv`.

## Four banking gates

1. **Preregistered:** yes, commit `ccf8384`, before the curvature result was computed.
2. **Full space or bounded scope:** complete for the declared static cohomogeneity-one reciprocal
   block, one transverse metric twist, exact quadratic order, and arbitrary local `p,u` jets. The
   omitted sectors are explicit in `COMPLETENESS_MAP.tsv`.
3. **Independently verified:** yes in-package by a separate Torch tensor/Bach implementation and ten
   frozen witnesses. No fresh external-model review was authorized.
4. **Every premise audited:** yes for the bounded verdict; background on-shellness, topology,
   boundary completion, physical scale, carrier, source, stability, and mass remain open.

Banked grade: **VERIFIED-WITH-CAVEATS**.

## Scientific decision

Do not fit the lower-order coefficient and do not start a full GPU Hopfion search. First vary the
reciprocal background and transverse twist together in a bounded completed variational problem. The
test is whether an on-shell reciprocal branch forces the positive, zero, or negative coefficient
stratum. That result determines whether the economical one-parent metric bridge deserves a full
three-dimensional finite-cell extension.
