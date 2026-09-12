# Source-first finite outcomes

Both executions completed before parent candidate/code/outcome exposure.

1. `invariant_initial`: eight signed amplitudes, t=1..80. No nonvertex scalar
   X crossing was detected. Runtime 1.702s, maximum RSS83152KiB. No all-time or
   whole-sky nonconjugacy follows. Small coordinate X at large amplitude is not
   a small physical width: the physical longitudinal separation is N X.
2. `geodesic_initial`: eleven frozen cases with central/full original-Christoffel
   geodesics and three great-circle offset sizes. Runtime11.580s, RSS80344KiB.
   All derivative, screen-orthogonality, nullness, axial quadrature, pure-transverse
   scalar and background momentum-quadrature checks passed. Largest normalized
   finest-versus-Richardson derivative difference7.876112896932584e-7; largest
   central null residual5.540012892879531e-14. These are float64 diagnostics,
   neither interval bounds nor all-time claims. Both source-sky derivatives are
   preserved in the saved 3x2 physical variation matrices.

No numerical failure occurred in these two runs. No scalar crossing refinement
was triggered. No parent implementation is imported. Independent implementation
and separate argument/context are established; different library/model, formal
proof, human-specialist and interval-certification axes are UNTESTED.

The fixed scalar grid and eleven full-geodesic cases are not a substitute for a
theorem over every finite direction or a proof that no unsampled zero exists.
