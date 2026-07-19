# Null-Section / Hopfion Metric Audit — Preregistration

Date: 2026-07-19
Branch: `codex/null-section-hopfion-audit-2026-07-19`
Base: `715fa57767ecc2ec370599ad18cd9f87911798d8`
Mode: CPU-only, metric-led, bounded conceptual/algebraic audit

## Whole question

Does the conditional conformal-Lorentzian null-direction `S2` fiber provide an intrinsic realization
of the existing full-3D Hopfion carrier, or does identifying the two require additional unselected
structure such as a foliation, frame/soldering map, connection, section, or boundary rule?

The audit tests an identity/bridge. It does not search for a new action, fit a model, evolve the
soliton, or assume that matching `S2` topology establishes physical identity.

## Frozen status premises

- Reciprocal kinematics retain their current premise-stamped `DERIVED` status.
- Four-dimensionality is `INHERITED`.
- A local Lorentzian representative and material clock/ruler realization remain
  `POSIT / CHOSE / CONDITIONAL` after representative selection.
- Positive Common-Scale rescaling preserves the projective null cone.
- Time orientation, foliation, carrier section, carrier framing/trivialization, and other-field
  finite-cell boundary data are not selected by exact C0/C1.
- The round-`S2` unit-vector carrier remains `WORKING / POSIT / CONDITIONAL`.
- The existing H3/no-null implementation is `FULL_3D_HOPF_CAPABLE`; the banked field is
  `OBSERVED_CARRIER_CONDITIONAL`; its static stability is
  `SETTLED_STATIC_FINITE_BOX_CONDITIONAL`.
- Co-presence means whole-solution event membership, not instantaneous influence, zero travel time,
  or a propagation law.
- Complete native action/source, physical carrier boundary, normalized charge, unconditional mass,
  and time-live topology propagation remain `OPEN`.

## Candidate constructions to test

1. `TYPE_IDENTITY`: treat the existing internal triplet `n(x) in S2` directly as a local null
   direction `k proportional to u+n`.
2. `SOLDERED_SECTION`: introduce a spacelike slice normal `u` and spatial frame/soldering map to
   turn the internal triplet into a tangent null-line section.
3. `INTRINSIC_BUNDLE_SECTION`: formulate a section of the celestial sphere bundle with metric- or
   conformal-geometry transport, without reducing it prematurely to a fixed target `S2`.
4. `WHOLE_HISTORY_CONGRUENCE`: ask whether a four-dimensional null line field/congruence has a
   slice-independent topological meaning compatible with co-presence and the finite cell.
5. `ANGULAR_PHI_SELECTOR`: audit whether the actual UDT angular metric block and its coupling to
   `phi` supply a nontrivial frame, connection, shear, twist, or holonomy capable of selecting or
   transporting a carrier section.

No candidate is privileged before the tests.

## Load-bearing tests

### T1 — Type and transformation law

Determine whether the code's carrier is an internal scalar triplet with global target rotations or a
spatial tangent vector. Record every additional structure needed to identify the two.

### T2 — Frame/trivialization dependence

Construct an exact local-frame countermodel on `S3`: a constant physical direction described in a
winding frame must be capable of acquiring standard Hopf-map components. If so, component Hopf
number is not an invariant of an unframed sphere-bundle section.

### T3 — Energy covariance

Test whether the existing ordinary-derivative `L2+L4` carrier energy is invariant under
position-dependent frame rotations. Exhibit the connection term required to cancel a pure frame
change. Do not infer that this connection or its action is selected by UDT.

### T4 — Null and conformal structure

Verify the null lift, positive-CSN invariance, Lorentz-frame aberration on the celestial sphere, and
the distinction between a conformal sphere fiber and a fixed round target metric.

### T5 — Hopf fibers versus congruence curves

Distinguish the preimage-linking definition of Faddeev–Skyrme Hopf charge from the integral curves of
a tangent/null direction field. Do not call them identical without an explicit soldering and
integrability/geodesic proof.

### T6 — Global/co-present and boundary status

Audit foliation dependence, time orientation, global section existence, finite-cell boundary
completion, topology propagation, caustics/singular changes, and what current bootstrap wording does
or does not select.

### T7 — Angular-sector / phi interaction

Inspect the exact registered metric rather than assuming a generic round sphere. Separate:

- a common `phi`-dependent angular/areal scale, whose mixed connection is proportional to the
  identity and therefore selects no angular direction;
- coordinate-basis spin-connection terms, which are not automatically a physical carrier selector;
- invariant angular shear, anisotropy, off-diagonal twist, or holonomy, which could distinguish or
  transport directions if it is actually derived from the metric/foundation;
- finite-cell angular boundary structure, if any, from solver-imposed angular framing.

Audit the mixed connection `Gamma^A_(phi B)` or its coordinate-invariant equivalent and the angular
curvature/holonomy. A selector may be credited only if it survives frame changes and does not require
adding unregistered angular functions, a preferred axis, or a hand-chosen dyad.

## Exact algebra contract

A runnable SymPy script must independently check at least:

1. `k=(1,n)` is null iff `|n|=1` in an orthonormal Lorentz frame;
2. positive conformal rescaling preserves nullness;
3. a Lorentz boost maps the celestial sphere to itself by projective aberration, not generally by a
   fixed spatial rotation;
4. a unit quaternion rotation of a constant axis produces a normalized standard Hopf map;
5. the registered Hopf connection gives nonzero unit Hopf charge while the constant map gives zero;
6. a position-dependent rotation makes the ordinary derivative energy of constant components
   nonzero;
7. the induced pure-gauge connection cancels that derivative covariantly;
8. the output of a map `S3 -> S2` and a tangent vector to `S3` are different geometric types until a
   soldering/trivialization is supplied;
9. for a round warped angular block `h_AB=R(phi)^2 gamma_AB`, the mixed connection is
   `Gamma^A_(phi B)=(R'/R) delta^A_B`, so pure angular scale coupling supplies no eigendirection;
10. any apparent selector from a rotating round dyad is removable frame gauge;
11. a nondegenerate angular shear/twist can select axes or transport only when additional anisotropic
    metric data are present and provenance-audited.

## Falsification and adjudication rules

- Mere equality of fiber topology (`S2`) is insufficient for `CARRIER_DERIVED`.
- If an allowed local frame change alters the component Hopf charge or ordinary-derivative energy,
  direct unframed identification fails.
- If a foliation/frame/connection/reference section/boundary must be chosen, each remains explicit
  `CHOSE`, `POSIT`, or `OPEN`; it cannot be relabeled metric-derived.
- A metric-derived Levi-Civita object after representative and foliation selection remains conditional
  on those selections. Conformal null geodesics do not automatically supply arbitrary fiber
  comparison or a carrier action.
- A `phi`-dependent round angular scale is not a section selector. Angular anisotropy, shear, twist,
  or holonomy may count only when it is invariant and comes from registered UDT metric data rather
  than a coordinate frame or an added angular ansatz.
- Co-presence may motivate a whole-history section but cannot select it by semantic reinterpretation.
- A successful kinematic lift may be banked only as a `WORKING_CANDIDATE` unless section selection,
  invariant topology, and boundary completion are also derived.

## Maximum allowed conclusion

The audit may determine whether the null-direction `S2` match is:

- a superficial topological analogy;
- a valid but framed/connection-dependent kinematic lift;
- an intrinsic conformal-bundle construction with an open section selector; or
- a genuinely selected UDT carrier bridge.

It may not derive or canonize the action, source, mass, dynamics, physical finite-cell boundary, or a
time-live stability theorem.

## Evidence and stop gates

- Preserve source inventory, exact algebra, status ledger, full stdout/stderr, and SHA-256 manifest.
- Use a deterministic fail-closed verifier with exercised corruptions.
- Obtain a fresh adversarial semantic review of every load-bearing promotion or no-go.
- Replay repository tests and all frozen manifests; preserve the original dirty checkout by metadata
  only.
- Commit and push the audit branch, then stop before startup integration, `grok` advancement, a
  time-live solve, action construction, GPU work, canonization, or repository reorganization.
