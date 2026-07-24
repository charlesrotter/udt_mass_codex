# UDT common-scale-neutrality provenance audit

Date: 2026-07-24

Frozen base: `c171b052ad321df7d71832cfa35403f07108d61e`

Preregistration commit: `7e8cd78`

Mode: bounded CPU source, dimensional, and symbolic audit

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Strong local Common-Scale Neutrality was not derived from Reciprocal-c or dual
UDT Reciprocity. It was introduced separately on July 15 as an explicit
owner-locked foundational postulate:

```text
[g]_CSN={Omega(x)^2 g : Omega(x)>0}.
```

The exact source says CSN **declares** the common factor calibrational. The
earlier reciprocal derivation instead gives

```text
uv=1
```

for an exact fixed-pairing-preserving positional comparison. Retaining an
explicit common factor `A` gives

```text
P_A^T K P_A=A^2 K.
```

Exact preservation of the same fixed `K` therefore sets positive `A=1`; it
does not derive a gauge orbit of arbitrary `A` or `Omega(x)`.

The current owner concern is justified. The correct new status is:

```text
STRONG_LOCAL_CSN =
  CHALLENGED_OWNER_POSTULATE_NOT_DERIVED
```

This audit does not prove strong CSN false. Measured `c_E` fixes the
clock/ruler conversion ratio and conformal rescaling preserves that ratio and
the metric null cones. Thus `c_E` alone does not select an absolute common
factor. But neither that fact nor Reciprocity proves that conformally related
physical metrics are equivalent.

## Why the distinction matters

Earlier work conflated three statements:

1. Reciprocity does not supply every physical scale.
2. A common factor may be normalized while doing ratio algebra.
3. Every local common factor is physically gauge.

Only the first two follow without strong CSN. The third is the July 15
postulate.

The epistemological GR objection sharpens the burden. A scale-neutral
fundamental theory can logically extend a calibrated theory such as GR, but it
must derive the physical representative. The repository's prior
representative-selector audit found no such current map. Consequently UDT has
not yet justified both the scale-free fundamental layer and its recovery of a
calibrated physical metric.

The cleaner alternative now reopened is that the reciprocal UDT metric is
already a physical calibrated metric, with `c_E` and `G_obs` accepted as
observational anchors. That alternative still does not derive `X_max`, total
mass, an action, or a source.

## Exact source census

The preregistered frozen-base query contains:

- 1,421 exact source paths;
- 18,612 query hits;
- 29 mandatory load-bearing paths;
- 23 individually adjudicated load-bearing claims/families.

All source blobs and SHA-256 values are frozen in `SOURCE_MANIFEST.tsv`. The
chronology and exact claim roles are in `LOAD_BEARING_SOURCE_LEDGER.tsv`.

The decisive provenance chain is:

- Reciprocal-c derivation: `uv=1`, exponential characters, scale `X` open.
- CSN record: a separate owner postulate declaring local `Omega(x)` gauge.
- C0/C1: cold arms receive CSN as locked input and may not challenge it.
- Final action adjudication: CSN stays `FOUNDING`; `C^2`/Bach is
  `UNIQUE-CONDITIONAL`.
- July 19 scale clarification: observed `c_E` and `G_obs` are accepted only
  in a later calibrated layer while scale-free core remains an owner ruling.
- July 24 correction: Charles reopens that ruling.

## Independent algebra

Production SymPy 1.13.1 passes 20/20 exact checks. A separate standard-library
implementation reconstructs the fixed-pairing algebra numerically, the
clock/ruler scaling ratio, the dimensional obstruction, and the source
provenance without importing the production module.

All 10 exercised corruptions are rejected, including:

- promoting strong CSN from postulate to theorem;
- allowing arbitrary `A` under exact fixed-`K` preservation;
- claiming `c_E,G_obs` select a length;
- claiming a representative selector exists;
- dropping the CSN premise from the `C^2` grade;
- promoting EH;
- retaining strong CSN as unchallenged; and
- calling the common factor gauge-derived.

## Scientific regrades

### Retained

- Reciprocal-c and dual Reciprocity: `FOUNDING`.
- `uv=1`: `DERIVED` in the supplied dual-pair formalization.
- Reciprocal exponential response: `DERIVED_CONDITIONAL`.
- Observed `c_E` and `G_obs`: observational anchors.
- Conformal preservation of causal cones: exact mathematics.
- Intrinsic nonnull-`dphi` reciprocal `3+3` split.
- Normalized angular shape, torus lattice, and dual-systole mathematics.
- Conditional toric/Hopf topology.
- Scoped WR-L/SNe and conditional finite-box Hopfion evidence.

### Regraded

- strong local CSN: `CHALLENGED_OWNER_POSTULATE_NOT_DERIVED`;
- scale-free physical UDT core: `CONDITIONAL_ON_STRONG_LOCAL_CSN`;
- pre-scale `C^2`/Bach physical priority:
  `UNIQUE_CONDITIONAL_ONLY_IF_STRONG_CSN_RETAINED`;
- CSN-normalized `h0` transport: exact normalization construction, but no
  longer a physical pre-scale connection without strong CSN;
- representative-selection stage: open on the CSN branch and potentially
  unnecessary if the physical metric is primary.

### Not promoted

EH remains `CONDITIONAL_NOT_SELECTED`. Removing a reason to exclude EH does
not derive EH. Complete action, source, boundary, carrier emergence,
unconditional mass, density feedback, `X_max`, scale closure, and time-live
matter remain `OPEN`.

## Smallest corrected conceptual seam

The next question is no longer “what mechanism selects a representative?”
until the ontology is decided. It is:

> Is the physical UDT variable a calibrated reciprocal metric, or a conformal
> class requiring a separately derived physical section?

That is a two-branch foundational-object audit, not an action hunt. If the
first branch survives, much of the two-stage representative machinery becomes
superfluous. If the second survives, UDT still owes the selector already shown
to be absent.

## Four gates

1. **Preregistered:** yes, commit `7e8cd78`.
2. **Full or bounded:** full frozen textual census for the registered CSN
   vocabulary; exact algebra is bounded to reciprocal diagonal comparison,
   conformal weights, one nonconstant curvature witness, and dimensional
   scale counting.
3. **Independently verified:** yes, separate standard-library reconstruction
   and 10 exercised semantic corruptions.
4. **Every premise audited:** yes for CSN provenance and the enumerated
   downstream families; no action or future ontology is exhaustively solved.

The caveat is that no fresh external model context was used. The maximum
banked result is a premise correction and dependency regrade, not
canonization.
