# Metric-Wide Cartan/Holonomy Audit — Preregistration

Date: 2026-07-19

Base: `ec24c135212d3121e2d5903a29ec669f0b8a982a`

Branch: `codex/metric-cartan-holonomy-audit-2026-07-19`

Mode: CPU-only, metric-led, observing rather than targeting

## Exposure disclosure

The preceding post-July record has already exposed several relevant conclusions before this
preregistration:

- the conformal metric propagates every supplied null ray but does not select an initial ray;
- the normal conformal Cartan/tractor connection supplies conditional representation transport but
  not a tangent-null section;
- representative holonomy families may fix all, two, one conditionally, or no projective rays;
- the reciprocal Hopf orbit match and toric `S3` closure are conditional on unselected physical
  spatial realization, periods, and caps;
- the exact rung-2 mixed-curvature expression is geometry, not a native equation;
- one pre-July/superseded document proposed matter as reciprocal-axis loop holonomy and named
  `C^2[g(phi,n)]` as a test. Under the July-1 firewall, that document may identify a candidate or
  failure only. It supplies no affirmative UDT physics here.

These statements are frozen inputs or challenges, not the desired answer. This audit must add a
metric-wide Cartan decomposition, exact unrestricted counterfamilies within its declared arena, and
an independent post-July test before banking any stronger synthesis.

## Whole question

Take seriously the rule that the metric is the theory. Once the reciprocal temporal/parallel block
is represented inside a full metric with a free transverse zweibein and free mixed/twist data:

1. What connection, curvature, transport, and holonomy follow from the metric alone?
2. Which relations are Cartan/Bianchi identities, and which would be additional equations or global
   restrictions?
3. Does current Reciprocity, CSN, finite-cell structure, or bootstrap force a reduction of
   holonomy, an invariant line/plane, a physical transverse realization, a section of the celestial
   `S2`, a nontrivial topological sector, or a scale?
4. Can metric holonomy itself supply matter, or does it only characterize geometry until a native
   functional, variation domain, boundary law, and global sector are supplied?
5. Are the pre-scale `C^2` and post-scale EH branches two projections of one Cartan identity, or only
   two different curvature contractions available after different premises are chosen?

The audit observes the metric's full structural content. It does not target a particle, Hopfion,
preferred PND, action, EH limit, or desired topology.

## Configuration-space declaration

### Abstract whole frame

On a smooth four-dimensional Lorentzian conformal representative, use a local coframe

\[
e^I=e^I{}_\mu dx^\mu,
\qquad
g=\eta_{IJ}e^I\otimes e^J.
\]

The full local coframe has sixteen components and local Lorentz gauge freedom. The conditional
reciprocal realization fixes only the two singular weights on a separately declared Lorentzian
two-plane; it does not fix a global tetrad, foliation, angular screen, or physical line fields.

For the `2+2` decomposition challenge, write schematically

\[
g=g_{ij}(x,y)dx^idx^j
+q_{AB}(x,y)\big(dy^A+\mathcal A^A{}_i dx^i\big)
                 \big(dy^B+\mathcal A^B{}_j dx^j\big),
\]

where `i,j` label the declared reciprocal base and `A,B` the transverse screen. `q_AB` is an
arbitrary positive two-metric and `A^A_i` retains mixed shift/twist. The diagonal reciprocal block,
zero shift, round transverse metric, integrable screen, and toric periods are all subfamilies—not
the whole space.

### Exact computational tiles

Because a symbolic sixteen-function curvature tensor is not a tractable or illuminating expression,
exact tests will use several complementary subfamilies without promoting any one to the whole:

1. general abstract Cartan structure equations with arbitrary coframe;
2. a diagonal reciprocal metric with two independent transverse warps and free `t,r,theta`
   dependence, inherited only as a regression anchor;
3. an exact twisted-screen family
   `e0=exp(-phi)dt`, `e1=exp(phi)dr`, `e2=dx`,
   `e3=dy+lambda chi(r)dx`, retaining nonintegrable frame data;
4. flat, product-curved, and twisted finite-domain holonomy counterfamilies;
5. a **conditional challenge only** using the single-axis metric
   `h=I+(exp(2phi)-1)n tensor n`, to test whether metric curvature automatically reduces to the
   historical area-only `F^2` structure. The single-axis completion is not adopted.

Any conclusion from a computational tile remains stamped by that tile.

## Premise ledger

| Premise or choice | Status | Treatment |
|---|---|---|
| Positional dilation, Reciprocal-c, dual Reciprocity, CSN | `FOUNDING` | Current C0/C1 authority. |
| Reciprocal exponential comparison pair | `DERIVED_CONDITIONAL` | Composition, regularity, sign/unit, and representation stamps retained. |
| Four-dimensional conformal-Lorentzian metric readout | `INHERITED_CONDITIONAL` | Required for Cartan/Petrov/holonomy arena; not newly derived. |
| Global spacetime coframe or preferred reciprocal two-plane | `OPEN_NOT_ASSUMED` | Used only after an explicit tile declaration. |
| Levi-Civita connection | `DERIVED_FROM_CHOSEN_METRIC_REPRESENTATIVE` | Torsion-free metric-compatible connection; representative dependence audited. |
| Normal conformal Cartan/tractor connection | `CONDITIONAL_CANONICAL_REPRESENTATION_GEOMETRY` | Existing post-July result; no physical section promotion. |
| Independent affine connection or torsion | `FREE_CHALLENGE_NOT_ADOPTED` | Absence from current field census must remain visible. |
| Transverse zweibein, trace, shear, twist, shifts | `free-and-explored` | Never dropped globally because a diagonal tile is simpler. |
| Coordinates/charts and local Lorentz gauge | `CHOSE_COMPUTATIONAL` | No component formula is called invariant without reconstruction. |
| Finite mirrored cell and static phi seal value/parity | `CANONIZED_LIMITED_SCOPE` | No angular frame, holonomy, topology, or boundary functional inferred. |
| Bootstrap narrow-window/global closure | `OWNER_STATED_WORKING` | On-shell admissibility wording only; no local operator inserted. |
| Pre-scale `C^2`/Bach branch | `UNIQUE_CONDITIONAL_BULK_CLASS` | Exact class premises retained; not complete action. |
| Post-scale EH branch | `CONDITIONAL` | Representative, variation, locality, derivative-order, scale, and boundary premises retained. |
| Round `S2`/Hopf carrier | `WORKING_POSIT_CONDITIONAL` | Excluded as derivation input; may appear only as comparison output. |
| Single reciprocal axis `n` | `CHOSE_CONDITIONAL_CHALLENGE` | Must not be reported as native field emergence. |
| Metric holonomy equals matter | `NOT_ASSUMED_DERIVATION_TARGET` | Requires proof, not evocative language. |
| GPU computation | `EXCLUDED` | CPU symbolic/exact work only. |

## Candidate structural outcomes

1. `CARTAN_ONLY`: the metric uniquely supplies connection/curvature/holonomy after a representative,
   but no selector or dynamics.
2. `HOLONOMY_REDUCTION`: current UDT forces a reduced holonomy group preserving a line, plane, spin
   lift, or other physical section.
3. `GLOBAL_COMPATIBILITY_SELECTOR`: finite-cell/bootstrap closure supplies a path-independent or
   topology-selecting restriction not reducible to a local identity.
4. `METRIC_MATTER`: a nontrivial metric-native holonomy/topological density plus its functional,
   variation, source, and boundary sector follow without an added carrier.
5. `CONDITIONAL_AXIS_CURVATURE`: a chosen reciprocal-axis metric produces a fixed orientation
   functional, possibly equal to, larger than, or different from `F^2`.
6. `C2_EH_CARTAN_BRIDGE`: one exact current-premise Cartan/variational relation yields the two
   conditional action branches before and after scale selection.
7. `UNDERDETERMINED_REDUCTION`: the metric gives the language, while global reduction/soldering,
   topology, functional, and scale remain independent choices.

All seven outcomes remain live.

## Exact planned tests

1. Derive the torsion-free metric-compatible spin connection from a general coframe and distinguish
   local Lorentz gauge from invariant curvature/holonomy data.
2. Record the first and second Cartan equations and both Bianchi identities. Test whether any sets a
   curvature component, Ricci tensor, Weyl tensor, or action variation to zero.
3. Decompose connection and curvature into reciprocal-base, transverse, and mixed/twist blocks in
   the abstract `2+2` arena. Track which terms disappear only when shift, shear, or twist is chosen
   zero.
4. Derive the exact connection and curvature of the twisted-screen family. Construct equal-boundary
   members with continuously different interior curvature/holonomy while the reciprocal block and
   static seal datum are unchanged.
5. Compare trivial, product-reduced, and generic/twisted holonomy fixed sets. A selector claim must
   survive all admissible families or prove why complete UDT excludes them.
6. Audit CSN: distinguish the representative-dependent Levi-Civita connection from conformal
   Cartan transport and conformally invariant zero sets/holonomy statements.
7. Express EH and `C^2` as different contractions of the same curvature data; calculate their common
   source object and different scale/derivative behavior. Attempt the strongest identity-level
   bridge without introducing a compensator, scale field, or new action.
8. On the conditional single-axis challenge, compute exact curvature invariants for rank-one and
   multi-direction orientation textures. Test whether metric curvature automatically has the
   historical rank-one-zero/area-only property.
9. Audit whether a metric holonomy class supplies a carrier section, topological charge, local
   energy/source, differentiable boundary generator, or stability law—or only labels geometry.
10. Reconcile the result with the post-July projective-transport, transverse-realization,
    angular-toric, native-Hopfion, native-action, and rung-2 ledgers.

## Falsification and certification contracts

`NATIVE_HOLONOMY_SELECTOR_DERIVED` requires a theorem from current post-July premises that every
admissible complete realized solution has the named holonomy reduction and one globally smooth
physical invariant object, including type-change, seal, and topology gates. A special exact metric
does not pass.

`METRIC_MATTER_DERIVED` requires more than nonzero Riemann curvature. It requires a native,
nontrivial, globally defined metric object; a selected topological sector or charge; its
differentiable functional/variation and source; compatible finite-cell boundary data; and a route
to persistence/stability. Calling curvature “matter” does not pass.

`C2_EH_BRIDGE_DERIVED` requires an exact relation under current premises specifying the
representative-selection map, scale origin, variation order/domain, boundary terms, and why the
post-scale lower-derivative equation follows. Sharing a connection or low-curvature approximation
does not pass.

`CONDITIONAL_AXIS_F2` passes only if the chosen-axis metric curvature is shown exactly to eliminate
all rank-one orientation cost and reduce to the area-only invariant within the declared functional.
If rank-one texture has nonzero curvature cost, the historical loop-only identification fails in
that conditional metric class.

Mutation catches must reject: setting torsion or mixed curvature to zero by ansatz and calling it a
theorem; treating a coframe as unique rather than Lorentz gauge; treating Bianchi as an EOM; calling
Levi-Civita transport CSN-independent; calling reduced holonomy universal from one witness; treating
boundary-equal metrics as holonomy-equivalent; calling a representation-space Hopf connection a
spacetime section; calling generic curvature matter; adopting the single-axis extension; or deriving
EH from `C^2` merely by dimensional or low-curvature rhetoric.

## Maximum allowed conclusions

- `LEVI_CIVITA_CONNECTION_AND_CURVATURE_METRIC_DERIVED_PER_REPRESENTATIVE`;
- `CARTAN_BIANCHI_IDENTITIES_DERIVED_NOT_DYNAMICS`;
- `RECIPROCAL_ANGULAR_MIXED_CURVATURE_GEOMETRIC`;
- `HOLONOMY_REDUCTION_SELECTED`, `CONDITIONAL`, or `UNDERDETERMINED`;
- `CONDITIONAL_SINGLE_AXIS_CURVATURE_EQUALS_F2`, `STRICTLY_LARGER`, `DIFFERENT`, or `UNRESOLVED`;
- `METRIC_HOLONOMY_MATTER_DERIVED`, `CONDITIONAL`, or `NOT_DERIVED`;
- `C2_EH_CARTAN_BRIDGE_DERIVED`, `CONDITIONAL`, or `NOT_DERIVED`;
- a ranked, non-invented next theorem or computation, if one survives.

No result may claim a complete action/source, carrier emergence, matter identity, mass, stable
particle, cosmology, or bootstrap closure beyond its exact gates.

## Completeness stamp

This is one structural metric/connection tile. It covers the abstract torsion-free Cartan system,
one full `2+2` decomposition schema, complementary exact holonomy counterfamilies, one conditional
single-axis curvature challenge, and the relationship between two conditional curvature-action
classes. It does not exhaust arbitrary global four-manifold topology, all Lorentz/conformal
holonomy groups, independent torsionful/metric-affine field theories, every complete action,
time-live global solutions, boundaries/corners, or the ten-component nonlinear solution space.

## Stop line

Stop after the bounded audit package is preregistered, independently verified, frozen, committed,
and pushed. Do not edit `LIVE.md`, `HANDOFF.md`, `INDEX.md`, `CANON.md`, or other startup controls. Do
not launch GPU work, a time-live solve, carrier relaxation, cosmology, canonization, repository
reorganization, or a downstream derivation arm.
