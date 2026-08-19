# G168 audit report — ordered co-present pair-plane ownership

Date: 2026-08-18

Grade: `VERIFIED_WITH_CAVEATS__FRESH_EXTERNAL_REVIEW_OPEN`

## Primary landing

```text
ORDERED_COPRESENT_PAIR_GERM_OWNS_LOCAL_CALIBRATED_PAIR_PLANE
__BARE_LABELS_DO_NOT
__NO_PATH_REQUIRED
```

## Result first

The final local input left open by G167 is now isolated. A physically typed local positional
comparison must contain a calibrated clock tangent (u_A) and a nonzero ordered separation tangent
(s_{AB}). The metric uniquely removes the clock component,

\[
r_{AB}=s_{AB}-\frac{g(u_A,s_{AB})}{g(u_A,u_A)}u_A,
\]

and thereby owns the Lorentzian pair plane

\[
E_{AB}=\operatorname{span}(u_A,r_{AB}).
\]

No path, geodesic, curvature selector, complete pair surface, independent screen, or scalar `mu`
is needed for this local step. In the primary metric, the coordinate components of
((u_A,s_{AB})) are exactly the G167 (Y,Z) blocks, so nonradial angular participation enters the
pullback automatically before terminal reciprocal readout.

## The important caveat

Two observer names do not supply the germ. An exact flat counterfamily has the same two boundary
worldlines and the same event pairing but different regular surface tangents—and hence different
local pair planes. The result therefore does not derive an event-pairing or global realization
law.

This is a type closure, not a new mechanism:

- the **completed local relation** supplies its one-jet;
- the **metric** derives its ruler, pair plane, screen, and pullback;
- the reciprocal kernel reads the completed pullback.

The remaining global question is which calibrated relation germs coexist and how frames are
carried between their different basepoints. It is no longer a local pair-plane selection problem.

## Boundary controls

- Local ruler reversal preserves the unoriented plane but does not alone reverse reciprocal depth.
- Full A/B reversal changes tangent fibers and still requires lawful carry.
- At coincidence the separation direction vanishes and the plane drops to rank one.
- B's velocity can lie outside the A-side positional plane; the plane is not a complete
  relative-motion state.
- A radial pair has (Z=0); a nonradial pair has metric-determined angular (Z).
- Rescaling the raw separation germ preserves the plane, while terminal scalar coordinates retain
  their declared calibration dependence.

## Evidence so far

- preregistered and pushed at `1341994a` before production;
- 36/36 exact symbolic/source checks pass after one recorded structural-simplification repair;
- independent standard-library `Fraction` replay: 6,012/6,012 checks over 1,200 trials;
- exact nonradial, radial, angular-coordinate, reversal, coincidence, relative-motion, and
  same-label counterfamily controls pass;
- 11/11 semantic mutation catches pass;
- the complete 153-row current-premise verifier passes;
- repository regression: 125 passed, 1 registered xfail;
- the package gate passes; fresh external review remains open before startup promotion.

## Maximum conclusion

Within the regular local primary-metric arena, the ordered co-present pair **germ**, not a path,
owns the pair plane needed by G167. Bare labels remain insufficient. No global relation family,
history, profile, `X_max`, dynamics, observation, or general ambient completion is derived.
