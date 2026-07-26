# Fresh adversarial review

Verdict: `VERIFIED-WITH-CAVEATS`.

The reviewer froze `ADVERSARIAL_SOURCE_FIRST_EXPECTATION.md` before reading
the production implementation or result tables. Its original temporary
artifact had SHA-256
`6e197767abf3e4efc8da01fe9eba6d237effd036c246c6c1c9118405008b6569`.

## Independent algebra

The fresh Koszul/noncoordinate-frame implementation did not import or execute
the production script. It matched:

- 24/24 connection pair/basis slots;
- 36/36 curvature pair-labelled slots;
- 10/10 symmetric Ricci slots and the scalar contraction;
- Riemann pair exchange and first Bianchi;
- all six derivative families and 19/21 quadratic family pairs; and
- the neutral-coordinate-jet bridge, with every symbolic delta zero.

A second coordinate-metric Christoffel/Riemann calculation used distinct
nonzero rational first and second jets in all eight amplitudes. It matched all
36 curvature slots and the scalar

```text
13650311 / 27518400
```

exactly. The portable implementations and raw streams are preserved in this
package and replay through `run_adversarial_replay.py`. The hashes from the
original fresh-context scripts are retained in `ADVERSARIAL_RESULT.json`;
portable copies differ only in path handling, formatting, and readability.

## Semantic review

- The right Maurer-Cartan sign is `dK-K wedge K=0`.
- Direct `phi--sigma`, `phi--alpha`, and `phi--shear` component couplings are
  present.
- Direct quadratic `phi--f2` and `phi--f3` component edges are absent.
- Both `f` families connect indirectly through angular families.
- This graph is specific to the registered torus-invariant triangular
  coframe components; it is not a frame-independent physical interaction
  graph.
- All twelve completion classes occur once. FC11 retains the general
  non-toric scope failure. No complete global witness or selected completion
  follows.
- Cartan, Maurer-Cartan, and Bianchi identities provide no response one-form,
  action, source, density law, selector, or dynamics.

## Corrections applied before banking

1. `PREREGISTRATION_CORRECTION.md` distinguishes 24 connection slots from 18
   generically nonzero entries, and 36 curvature slots from the generic 20
   algebraic Riemann components after symmetries.
2. The lay description is explicitly scoped to the chosen component atlas.
3. `NEXT_STEP.md` now follows `LIVE.md`: response availability first, then a
   bootstrap-to-local derivation if no candidate survives. The global-witness
   atlas is only a later proposal.
4. `FINE_COFAME` was corrected to `FINE_COFRAME`.
5. Second Bianchi is described as an abstract exact identity proof rather
   than an independent component replay.

Maximum honest conclusion:

`EXACT_NONLINEAR_GEOMETRIC_CARTAN_ATLAS_ON_THE_REGISTERED_REGULAR_TORUS_INVARIANT_TRIANGULAR_COFRAME; SCOPED_LOCAL_APPLICABILITY_ACROSS_12_REGISTERED_COMPLETION_CLASSES; CONNECTED_BASIS_DEPENDENT_SIX_FAMILY_GRAPH_WITH_ANGULARLY_MEDIATED_PHI_TO_F_CHANNELS; NO_GLOBAL_SELECTION_ON_SHELL_BRANCH_RESPONSE_ONE_FORM_ACTION_SOURCE_DENSITY_LAW_OR_DYNAMICS_DERIVED.`
