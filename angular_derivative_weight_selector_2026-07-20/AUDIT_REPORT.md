# Angular-Derivative Weight Selector Audit

Date: 2026-07-20  
Base: `f571842106f0a341e2b8db4e7dd64fc3e4ac03cc`  
Preregistration commit: `30e4fc3`  
Compute: CPU-only exact symbolic and coordinate-tensor algebra  
Status: **VERIFIED-WITH-CAVEATS** — deterministic base-source census, exact derivation, independent
coordinate-tensor reimplementation, and exercised fail-closed catches pass; no fresh external-model
review was authorized.

## Result first

The current UDT foundation does **not** derive a nonzero relative two-/four-derivative angular
weight without first adding an action, carrier/actor, reduction, or scale-selection rule.

It does expose a much sharper structure than “two arbitrary terms”:

1. Before physical scale selection, exact Common-Scale Neutrality separates the derivative orders.
   In four dimensions, for a dimensionless CSN-neutral angular variable, a constant-coefficient
   quadratic first-derivative density has common-scale weight `+2` and is therefore not pre-scale
   invariant. Quartic first-derivative densities have weight `0` and are compatible with pre-scale
   CSN.
2. The pure-metric comparison says the same thing in native geometric language: EH has weight `+2`
   and is post-scale `CONDITIONAL`; the `C^2`/Bach bulk has weight `0` and remains
   `UNIQUE-CONDITIONAL` only inside the frozen metric-only/local/4D/unrestricted-variation class.
3. CSN does not select which quartic angular invariant, its sign, or its normalization. Selecting a
   representative also does not algebraically turn a four-derivative functional into a
   two-derivative one.
4. The reciprocal angular/Hopf route supplies a conditional connection and topological flux, but
   smooth depth-shape and fiber/base-squashing freedoms change the local normalization while
   preserving the reciprocal orbit pair, caps, topology, and common-scale class.
5. The finite-cell seal, current bootstrap wording, and `Xmax` reciprocity do not close those
   freedoms. `Xmax` supplies at most the form

   `a4/a2 = Xmax^2 f(dimensionless global state)`.

   It does not fix `f`, the sign, the presence of both terms, or their action placement.

The exact maximum conclusion is:

`PRE_SCALE_DERIVATIVE_ORDER_SEPARATION_DERIVED_IN_NEUTRAL_BRANCH;`
`NONZERO_RELATIVE_WEIGHT_NOT_SELECTED_IN_CURRENT_FOUNDATION`.

This is a scoped negative about the current selectors, not a claim that a complete UDT metric
solution cannot select the ratio.

## Lay reading

The old particle model contained a “smoothness cost” and a “twisting cost.” Their balance gave the
soliton a finite size, but their relative strength was put into the model.

This audit found that UDT may be telling us **when** those two kinds of behavior are allowed to
appear:

- the four-derivative behavior naturally fits the scale-free, pre-material geometry;
- the two-derivative behavior needs a physical ruler or scale-bearing geometric state;
- therefore their eventual balance may record the moment the scale-free universe selects a
  physical metric and material phase.

That is promising. But the current rules still do not tell us the numerical balance. The missing
step is not another Derrick calculation and not a fitted coefficient. It is an exact metric
reduction or bootstrap equation that selects the angular shape, scale, and effective lower-order
term together.

## Exact CSN weight audit

Under the founding pre-scale equivalence

`g -> Omega^2 g`, `sqrt(|g|) -> Omega^4 sqrt(|g|)`, `g^{-1} -> Omega^{-2} g^{-1}`.

For a dimensionless neutral angular variable `Y` and a separately supplied target tensor, this gives

- `sqrt(|g|) K2 -> Omega^2 sqrt(|g|) K2`;
- `sqrt(|g|) (tr K)^2 -> sqrt(|g|) (tr K)^2`;
- `sqrt(|g|) tr(K^2) -> sqrt(|g|) tr(K^2)`;
- `sqrt(|g|) F_mu_nu F^mu_nu` also has weight zero if an angular two-form `F` is separately supplied.

Thus exact pre-scale CSN rules out a **nonzero constant-coefficient** `K2` in this branch. It permits
a family of quartic structures rather than selecting one.

This result does not assume a round `S2`, but it also does not derive an angular actor. If the
angular sector is only the metric itself, the native inventory is curvature rather than a map
energy. In that branch the corresponding distinction is EH versus `C^2`; translating curvature
into a particle functional still requires an exact quotient/section/soldering and reduction.

A formal field of CSN weight `-1` could dress `K2` as `sqrt(|g|) chi^2 K2`. That is a useful
counterexample to uniqueness, not proposed UDT content: the existence, metric origin, dynamics, and
selected value of `chi` are not supplied.

## Why scale selection alone is not the bridge

Choosing one representative of `[g]_CSN` changes the interpretation of the existing functional; it
does not change its derivative order. A `C^2` or quartic action remains that functional after gauge
fixing. Obtaining EH or a quadratic angular term requires at least one of:

- a scale-bearing field or geometric modulus;
- expansion/reduction around a selected nonzero-curvature metric state;
- integrating out genuinely identified degrees of freedom;
- a distinct post-scale action plus a derived matching law.

The exact algebraic pattern

`(K0+q2)^2 = K0^2 + 2 K0 q2 + q2^2`

shows the most economical conditional possibility. One scale-free four-derivative parent can yield
both an effective two-derivative cross-term and a four-derivative term after a nonzero background
curvature `K0` is selected. With `K0=0`, the quadratic cross-term disappears. This identity is not
an action derivation; it identifies the precise kind of full-metric reduction that could close the
join without assuming two independent matter terms.

## Angular quotient: topology fixed, local normalization open

Retain the conditional reciprocal toric orbit pair but leave its depth coefficient free:

`ds3^2 = H(eta)^2 d eta^2 + cos^2(eta) d xi1^2 + sin^2(eta) d xi2^2`.

For the diagonal circle generator `V=d_xi1+d_xi2`, its norm is one. With
`delta=xi1-xi2`, the quotient data are

`h_H = H^2 d eta^2 + cos^2(eta) sin^2(eta) d delta^2`,

`A = cos^2(eta) d xi1 + sin^2(eta) d xi2`,

`F = -2 cos(eta) sin(eta) d eta wedge d delta`.

The flux is `-2 pi` in the registered orientation for every positive admissible `H`, but the local
norm is

`F_ab F^ab = 8/H^2`.

The smooth nonround family

`H_epsilon = 1 + epsilon sin^2(2 eta)`, `epsilon > -1`,

has the same orbit coefficients, smooth cap values and first derivatives, `S3` topology, circle
action, connection, and Chern flux. At `epsilon=1/3`, `eta=pi/8`, exact direct tensor algebra gives

`F^2 = 288/49`, `R_base = 2592/343`, `R_base/F^2 = 9/7`.

The round value of the last ratio is one. Therefore the reciprocal pair and topology do not fix the
local metric/curvature normalization. The missing equation would have to select `H`.

There is a second independent modulus. For the smooth Hopf submersion

`g3 = b^2 h_round + a^2 A^2`,

`R3 = 8/b^2 - 2 a^2/b^4`.

Common scaling changes `a` and `b` together but leaves `a/b` invariant. Even a chosen EH
submersion comparison produces a relative connection/base weight proportional to `(a/b)^2`; CSN
does not choose it. Neither roundness nor that EH comparison is adopted here.

These are complete counterfamilies for the bounded claim that the already-registered reciprocal
orbit block, caps, topology, and CSN alone fix the normalization. They are not complete competing
UDT universes.

## Finite cell, bootstrap, and Xmax

The binding static finite-cell datum is `phi=0` at the mirrored seal with its normal derivative free.
It supplies no angular boundary values, corner terms, primitive, charge, or differentiable boundary
functional. Consequently it cannot make an integration-by-parts convention into a bulk coefficient
equation.

The current bootstrap is an on-shell requirement on a future complete universe. It deliberately
does not provide a local action, density center, response function, or varied global functional.
Turning the narrow density window directly into a coupling would violate its “no nonlocal
insertion” rule.

If both effective orders and an action have already been obtained, dimensions allow

`a4/a2 = Xmax^2 f(state)`.

The normalized position `x/Xmax` is unchanged by common homothety, so conditional `Xmax`
reciprocity is compatible with this form. It gives no equation for `f` and no proof that both terms
exist. The same conclusion survives the earlier global compactness audit.

Finally, Derrick stationarity gives `E2=E4` **for a chosen coefficient ratio**. It selects a solution
size from that input; it cannot be inverted into a native coefficient law without circularly using
the desired size.

## Provenance and carrier firewall

The census froze 3,825 base-tree sources matching the preregistered vocabulary. Thirty-three
load-bearing sources were individually adjudicated. Pre-July or mixed-date material was used only
for provenance, failure modes, or counterexamples. The current owner clarifications and final
post-firewall adjudication control:

- round `S2`: historical working posit, reopened;
- static `L2+L4`: `CONDITIONAL / CHOSE`;
- `C^2`/Bach: `UNIQUE-CONDITIONAL` in the exact frozen branch;
- EH: `CONDITIONAL` post-scale;
- complete action/source/boundary charge: `OPEN`.

No `S2` target, `L2+L4` action, coefficient, EH law, or carrier boundary condition entered the
derivation.

## Four banking gates

1. **Preregistered:** yes, commit `30e4fc3`, before source census and outcome calculation.
2. **Full space or bounded scope:** complete for the declared neutral first-derivative invariant
   inventory, pure-metric frozen comparison class, general `H_epsilon` reciprocal-Hopf family,
   base/fiber squashing, and current boundary/bootstrap/`Xmax` rules. The exact omitted layers are in
   `COMPLETENESS_SCOPE.tsv`.
3. **Independently verified:** yes in-package. A second implementation directly constructed the 2D
   and 3D coordinate connections/Ricci tensors, reproduced the nonround quotient and Berger
   curvatures, replayed all 33 base blobs/hashes, and exercised 27 corruption/overclaim catches.
   Fresh external-model review was not authorized.
4. **Every premise audited:** yes for the bounded verdict. Four-dimensionality, field census,
   locality, target tensors, toric completion, circle action, roundness, squashing, representative,
   boundary functional, bootstrap equation, and `Xmax` value retain explicit statuses.

Maximum banked grade: **VERIFIED-WITH-CAVEATS**.

## Scientific decision

Do not tune the old `L2/L4` coefficients and do not launch GPU solution-space grinding for this
question. The highest-value next derivation is an exact **metric-only angular reduction** of the
conditional pre-scale `C^2` branch on the most general reciprocal-toric coframe that retains `H`,
squashing, radial/time coupling, caps, and finite-cell boundary data.

The test should ask whether its own Bach/boundary/bootstrap equations select the angular moduli and,
only after a physical scale is selected, generate a uniquely normalized lower-derivative cross-term.
Failure would sharply rule out this economical one-parent bridge within that conditional branch;
success would still require the variation domain, global solution, section/soldering, and carrier
interpretation to be audited before any matter-action claim.
