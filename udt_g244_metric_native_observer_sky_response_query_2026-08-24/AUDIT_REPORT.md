# G244 audit — metric-native observer-sky response query

Date: 2026-08-24

Status: `EXTERNALLY_REVIEWED_ACCEPTED_WITH_STATED_BOUNDS`

## Landing

```text
METRIC_NATIVE_OBSERVER_SKY_AREA_SHAPE_QUERY_DERIVED_CONDITIONALLY
__NO_FITTED_ANGULAR_COEFFICIENT
__CATALOG_IDENTIFICATION_AND_HISTORY_OPEN
```

## What was learned

On every supplied regular finite G188 null sheet, the full matrix Jacobi map produces an intrinsic
observer-sky tensor

\[
H=\mathcal D^\dagger\mathcal D.
\]

It splits canonically into metric area and shape:

\[
A=|\det\mathcal D|,
\qquad C=H/A,
\qquad\det C=1.
\]

The scalar

\[
\mathfrak s=\frac{(\operatorname{tr}H)^2}{4\det H}-1
\]

is nonnegative and vanishes exactly for an isotropic/conformal screen map. Source-screen basis
freedom cancels from (H); observer-screen basis changes act tensorially. This gives a native
angular area/shape field without selecting the G225 pointwise comparison as physical transport and
without attaching an angular coefficient after reciprocal readout.

For a declared reference measure, the geometric area field defines the coefficient-free normalized
query

\[
dP_A=A,dQ/\int A,dQ.
\]

An angularly constant (A) cancels exactly. A nonconstant exact finite operator witness gives

\[
w_K^{\rm area}=-1/6.
\]

This number certifies the operator algebra only. The witness is not a physical history or fit, and
no observational outcome was read.

## Important pre-outcome correction

The first preregistration incorrectly called `sign(det(D))` invariant under independent endpoint
`O(2)` bases. Before any result was generated, commit `cf301bc9` corrected it to an
orientation-line-valued channel. Absolute area and shape were unaffected.

## Composition and caustics

G244 retains the G226 full phase as the composable object. The Jacobi position block obeys

\[
B_{20}=A_{21}B_{10}+B_{21}D_{10},
\]

and does not multiply alone. At a caustic, the position tensor becomes semidefinite and the regular
shape/density readouts leave scope; the full phase remains lawful. No position inverse is used.

## Evidence

- preregistered and pushed at `8d1eb059`;
- parity type corrected before outcome and pushed at `cf301bc9`;
- exact symbolic Gram and nonnegative-shear identities;
- 1,024 production exact matrix/gauge/scale cases and 1,024 exact symplectic phase cases;
- independent standard-library `Fraction` replay over 5,000 matrix cases and 5,000 phase cases;
- production and independent routes both recover `w=-1/6` and constant-response `w=0`;
- 14/14 hostile mutations caught;
- fitted angular coefficients: zero;
- BOSS/CMB outcomes: closed and unread.
- fresh sealed GPT-5.4 adversarial review: `G244_ACCEPTED_WITH_STATED_BOUNDS`; no repairs.

## What was not learned

G244 does not determine the values of (H(n)) across the real sky because that requires a supplied
complete metric history and null observation sheet. It also does not identify geometric area
weighting with a galaxy catalogue. That requires source incidence, source measure, branch/detection
semantics, and any transfer law.

It does not select G225 transport, a feature scale, a profile, `X_max`, a cosmology, or a physical
history. Direct reciprocal SNe redshift remains separate and unchanged.

## External adjudication

Fresh GPT-5.4 review of the authorized 29-file sealed intake independently matched all 28 payload
hashes, reran all four registered no-write checks, accepted the tensor typing and pre-outcome parity
correction, and found no fitted coefficient, forbidden outcome access, or source/catalogue
overclaim. It returned `G244_ACCEPTED_WITH_STATED_BOUNDS` and requested no repairs.

## Next gate

The subsequent scientific choice is between:

1. evaluating (H,A,C\) on one independently supplied complete metric history; or
2. declaring and preregistering the minimal source/incidence control needed to compare the geometric
   area query with still-hidden angular catalogue outcomes.

Neither step may fit an angular coefficient after seeing the outcome.
