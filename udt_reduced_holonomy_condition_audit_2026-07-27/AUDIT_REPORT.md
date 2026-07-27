# Reduced-holonomy condition audit

Date: 2026-07-27

Preregistration commit: `66ef48c` (base `1c91169`)

Status: **VERIFIED-WITH-CAVEATS, EXACT BOUNDED COFRAME CLASSIFICATION**

## Result first

The complete exact classification contains one regular parallel survivor and no survivor that keeps
the nontrivial intrinsic clock/ruler structure.

| Stratum | Exact `nabla X=0` condition | Regular result |
|---|---|---|
| `lambda != +/-1` | `p1=p2=p3=A=B=0` | impossible because regular `S3` has `B!=0` |
| `lambda=+1` | `p1=p2=p3=A=0` | complete untwisted constant-`phi` `R x round S3` |
| `lambda=-1` | `p1=p2=p3=B=0` | impossible because regular `S3` has `B!=0` |

The `lambda=+1` survivor has spatial `so(3)` holonomy and a parallel clock-versus-space grading, but
it also has:

```text
phi=constant, a=0, Q=1,
```

spatial isotropy, no clock twist, and no metric-distinguished reciprocal ruler.  Therefore it does
not close the nontrivial UDT clock/ruler structure.

The structural finding is the fork supplied by the angular sector: its nonzero contact coupling
`B` either mixes a distinguished ruler with the angular plane, or `lambda=+1` absorbs that mixing by
making all spatial directions equivalent.

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

No co-presence or signalling premise entered the algebra.

## Exact algebra census

- 30 nonzero Cartan connection components retained.
- 22 symbolic nonzero `nabla X` components in the generic stratum.
- 10 components at `lambda=+1`.
- 14 components at `lambda=-1`.
- Every clock–ruler, clock–screen, ruler–screen, and internal stabilizer distinction retained.
- `C` cancels only from off-eigenspace `nabla X`; it remains in the full connection.

The independent Koszul implementation used four exact case probes: generic `lambda=0`, generic
`lambda=2`, `lambda=+1`, and `lambda=-1`.  It independently verified sufficiency and detected each
required-zero variable separately.

## Surviving curvature

For `lambda=+1`, constant `phi0`, and `a=0`, exact Cartan curvature contains three spatial rotation
generators with coefficient `k^2/4`, where `k=kappa exp(-phi0)`.  Its algebra rank is three and every
generator commutes with `X_+1`.

An independent coordinate-metric/Torch calculation at P00, P01, and P02 reproduced rank three with
maximum scaled curvature error

```text
1.4432899320127035e-15.
```

All three coordinate metrics had nonzero determinant.

## What this means

Demanding a single globally parallel full reciprocal frame was stronger than the founding scalar
clock law.  On the tested contact geometry, that demand erases precisely the features it was meant
to preserve: nonconstant depth, twist-selected ruler, and ruler/screen distinction.

This makes the path-groupoid result more—not less—natural.  Local reciprocal structures can be
Lorentz-equivalent and compare along paths without one global rigid orientation, just as curved
geometry generally lacks one global inertial frame.

That interpretation is a lead, not yet a ruling on the founding postulates.  The repository has not
yet audited whether observer-frame Reciprocity actually demands a global parallel grading.

## Current-premise comparison

No registered premise supplies the parallelism conditions:

- Reciprocity fixes the local pair but not its global covariant constancy.
- Finite-cell contact geometry provides the obstructing nonzero `B`.
- The seal does not force constant `phi` or zero twist.
- Bootstrap remains on-shell admissibility, not a local equation.
- Strong local CSN is inactive and was not used.

No `lambda` or physical branch is selected.

## Evidence gates

1. **Preregistered:** yes, committed and pushed before outcome calculation.
2. **Full space or bounded scope justified:** full symbolic eigenvalue-stratum classification inside
   the stated stationary coframe; explicitly not all UDT coframes/topologies.
3. **Independently verified load-bearing premise:** yes; separate Koszul implementation plus
   coordinate/Torch curvature.
4. **Every premise audited:** yes; see `PREMISE_LEDGER.tsv`.

Grade remains `VERIFIED-WITH-CAVEATS` because the family is off shell and bounded, time-live and
other topology cases are outside scope, and no fresh external-model semantic adjudication was run.

## Authority boundary

No startup control, `CANON.md`, frozen evidence, physical `lambda`, seam, quotient, action, source,
carrier, boundary, density, bootstrap realization, mass, `X_max`, dynamics, signalling law,
observation fit, GPU work, or repository organization was changed or selected.
