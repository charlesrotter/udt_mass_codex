# G126 fresh blind review — raw bounded verdict

Date: 2026-08-16

Verdict: `PASS_WITH_REPAIRS`

The reviewer independently replayed both implementations and reproduced the original 15/15 and
12/12 results byte for byte. The bounded conclusion stood, subject to these repairs:

1. The original affine witness checked only a rate ratio at `Z=1`; it did not prove the absolute
   normalization `K_1(1)=K_2(1)=1`. Impose `u_i(1)=1/(2X)` and verify both absolute rates.
2. The production screen witness used unconstrained symbols `c,s`. Use an exact orthogonal matrix,
   then verify its Gram matrix, area, normalized-angle behavior, and zero shear.
3. The reference witness used only a uniform footprint. Demonstrate radial-factor cancellation
   against a nonuniform registered footprint and state the result relative to that footprint.
4. The nine-source manifest did not independently establish that the R5 curves inherited R2's
   Landy--Szalay reference projection and observed-redshift windows. Add the banked curve-
   construction source or weaken the object-type claim.
5. Reconcile `EVIDENCE_GATES.md`, which said package replay was pending, with the completed replay.
6. Reconcile `STATUS.md`, which still said no executable evaluation had occurred.

Maximum reviewer conclusion: the repairs strengthen proof hygiene and provenance but do not alter
the preregistered bounded landing.
