# Audit report — carried/intrinsic middle-morphism ownership

Date: 2026-08-10

Status: **VERIFIED-WITH-CAVEATS**

## Result

Across all six preregistered regular twisted-`S3` strata, the branch owns a nonempty path-labelled
alignment set between the carried and locally rebuilt clock/ruler/screen reductions. With the full
projector triple retained, that set is an `SO(2)` bitorsor. It is never a singleton.

Sharpened post-review landing:

```text
GAUGE_GROUPOID_ALREADY_SUFFICIENT_FOR_PROJECTOR_ALIGNMENT__CALIBRATION_DESCENT_OPEN
```

The preregistered `RELATIVE_ORBIT_DERIVED__REPRESENTATIVE_OPEN` remains a correct lower bound. The
metric owns the ordered projector pair, the full path-labelled `SO(2)` alignment bitorsor, and exact
balanced representative-free composition. It does not select a screen-phase representative, nor
does projector alignment by itself supply calibration density. Grading-only stabilizer dimensions are
`1,3,1,1,3,1` for `lambda=-2,-1,0,1/2,1,2`; full-projector stabilizer dimension is one in all six
rows.

## Exact gates

- six/six `lambda` strata classified;
- two distinct exact proper-orthochronous projector alignments exhibited on every stratum;
- 18/18 frozen local rows retain nonzero clock/ruler `nabla X`;
- 36/36 frozen loops are nonidentity and fail endpoint closure;
- 36/36 retain path composition;
- independent pure-Python `Fraction` verifier reproduces the matrix and stabilizer results;
- production SymPy and independent `Fraction` implementations reproduce exact balanced bitorsor
  composition across three reductions;
- 18/18 frozen source hashes replay;
- 11/11 catch-proofs reject identity smuggling, false uniqueness, hidden screen axes, path-label
  erasure, false quotient composition, false equivariant section, incomplete lambda coverage,
  absent-atlas promotion, scalar promotion, Euclidean minimization, and one-sided gauge changes.
- fresh external gpt-5.4 review accepted the load-bearing algebra and sharpened the object type from
  a double-coset shadow to the full compositional alignment bitorsor.

## Interpretation boundary

This result proves that no screen-phase representative is needed for projector-level composition.
It does not prove that a screen phase is irrelevant to every scalar or calibration-density readout,
and it does not include pair-surface integrability. The proposed next test is whether all
load-bearing reciprocal readouts and calibration-density data descend to the `SO(2)`
bitorsor/gauge-groupoid level.

No action, source, matter, mass, bootstrap, boundary, `X_max` value, CMB spectrum, or signalling law
is inferred.

## Four banking gates

1. **Preregistered:** yes, commit `44591433` before derivation.
2. **Full space or bounded scope:** complete for all six retained regular C01--C06 `lambda` strata
   and the frozen path/loop census; not universal over all UDT metrics or degenerate/null strata.
3. **Independently verified:** yes, by a code-independent rational implementation and a fresh
   manifest-confined external adversarial review.
4. **Every premise audited:** yes for metric/projector ownership, path transport, screen gauge,
   lambda strata, common-atlas conditionality, and excluded physics; calibration-density ownership
   remains explicitly outside scope.

Maximum conclusion: projector-alignment existence, nonuniqueness, and balanced composition are
`VERIFIED-WITH-CAVEATS` on the retained regular strata. Scalar/calibration descent remains `OPEN`.
