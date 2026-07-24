# Dual-systole wall-crossing selector audit

Date: 2026-07-24

Mode: preregistered CPU-only exact algebra, source adjudication, and
completion-family classification

## Result

The current UDT principles do not select one shortest angular character
through the reciprocal tie. They do something more precise:

```text
RECIPROCAL_TIE_SET_CONTINUATION_DERIVED
NO_EQUIVARIANT_SINGLE_SHORTEST_LINE_AT_SYMMETRIC_SEAL
SWAP_GLUE_CONDITIONAL_ON_UNSELECTED_GLOBAL_LIFT
REGISTERED_UDT_WALL_CROSSING_SELECTOR_NOT_FOUND
```

At `phi=0`, the two shortest primitive lines are exactly tied. Reciprocity
exchanges them and preserves the whole set, but fixes neither member.
Therefore no single-valued shortest-line selector can both be defined at the
symmetric seal and respect the reciprocal exchange.

This is a positive structural result, not merely “nothing was derived.” The
metric naturally preserves an exchanged pair. A reciprocal-swap transition
can glue the one-sided lines into one global line, but exact C1 supplies only
the odd scalar-`phi` seal condition; it does not select that angular lattice
lift. The full pair/set is derived geometry. Its physical role remains open.

Grade: `VERIFIED-WITH-CAVEATS`. Production exact controls and an independent
standard-library implementation pass. No fresh zero-context model review was
authorized.

## Preregistration and correction record

- Initial preregistration: `393de99`.
- Direct-authority source amendment before outcomes: `c42580c`.
- Exact C0/C1 source correction after a preliminary source-completeness
  challenge and before banking: `dc50f70`.

The preliminary output was not banked. The final production and independent
replays use 35 exact base-source identities. The original candidate and
falsification contracts remain visible and unchanged.

## Exact reciprocal obstruction

On the shear-free reciprocal control,

```text
phi<0 : W_min={[e1]}
phi=0 : W_min={[e1],[e2]}
phi>0 : W_min={[e2]}.
```

The exchange matrix `J` swaps `e1` and `e2`. At the symmetric metric,
equivariance of a single selector would require its chosen line to be fixed
by `J`. Neither shortest line is fixed. The two fixed diagonal lines are not
shortest.

In a fixed lattice trivialization, a discrete line also cannot vary
continuously from `e1` to `e2`. A transition function changes the question:
`J` gluing succeeds, while identity gluing does not preserve shortestness
across the control. The transition is precisely the additional global datum
that current finite-cell authority leaves open.

Full details and controls are in `EXACT_DERIVATION.md` and `RESULTS.json`.

## Principle audit

Fifteen principle/object types were classified in
`PRINCIPLE_CAPABILITY_MATRIX.tsv`.

- Reciprocal-c concerns the founding clock/ruler pair, not an angular
  character.
- Observer-frame Reciprocity requires covariance, but the tied set is
  already covariant.
- `X_max` reciprocity has no derived join to the absolute angular `phi` field
  or the finite-cell seam.
- CSN multiplies all character norms together and preserves the tie.
- The static seal fixes scalar `phi=0`, not the transverse angular lift.
- The complete coframe group law lives in a chosen trivialization and does
  not choose its physical section.
- Cartan/Kato transport transports a supplied subbundle; it does not select
  one from a degenerate pair.
- Connection curvature, holonomy, and cap annihilators constrain supplied
  choices without choosing them.
- Primary bootstrap is after-solution admissibility.
- The stronger local bootstrap fork remains meaningful but lacks a native
  operator, density-to-geometry law, and wall rule.

Boundary framing is the only listed object that could directly lift a line
to a phase or choose a seam transition. It is currently open.

## Completion audit

All twelve registered completion classes were retained without preference.

- Boundary cases require framing.
- Cap cases require annihilation, amplitude vanishing, or patching.
- Periodic bundles require tie avoidance and monodromy compatibility.
- Mirrors require a supplied identity/swap/conjugate lift.
- Nonorientation can retain an unoriented line while reversing sign.
- Rank loss or nontoric anholonomy terminates the character object.
- The reciprocal diagonal retains the set and exposes the exact tie.

No complete on-shell universe or completion selector was inferred.

## Meaning for mass emergence

This audit does not close mass, and it does not invalidate the conditional
stable Hopfion result. It corrects the proposed geometric bridge.

Trying to make the metric choose one angular “instrument” at the reciprocal
seal conflicts with the exact exchange symmetry. The symmetry-respecting
object is the pair. A future matter-emergence law might:

- use the whole reciprocal pair;
- supply a physical swap/mirror lift;
- let an amplitude vanish where a phase is undefined;
- or break the symmetry through a separately derived boundary or dynamical
  equation.

Only the first item is already present geometrically, and it is not yet a
carrier. This gives a sharper next question than inserting density or
tuning the old `L2/L4` coefficients.

## Verification

- 35/35 frozen source identities reproduced from the preregistration base;
- 20/20 production controls passed;
- 32/32 candidate rules classified;
- 15/15 registered principle/object types classified;
- 12/12 completion families classified without preference;
- independent implementation imports no production module;
- 20/20 adversarial mutations were caught;
- zero matter solves, density scans, or GPU work.

Repository-wide tests, frozen-package manifests, navigation, and dirty
checkout metadata are recorded separately in `REPOSITORY_GATES.json`.

## Four gates

1. **Preregistered:** yes, with the source amendments/correction preserved.
2. **Full or bounded:** complete for the exact reciprocal tie, all 32 frozen
   candidates, 15 registered principles, and twelve completion families;
   not every future action, boundary law, or complete universe.
3. **Independent:** yes, by separate standard-library reconstruction and
   exercised mutations; no fresh external model.
4. **Premises:** audited in `PREMISE_AUDIT.tsv`.

No canonization follows.

