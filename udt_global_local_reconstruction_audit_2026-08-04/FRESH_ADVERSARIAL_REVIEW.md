# Fresh external adversarial review

Model: `gpt-5.4`
Context: fresh, read-only, no research continuation
Date: 2026-08-04
Verdict: `PASS_WITH_CAVEATS`

## Verbatim return

**Blocking errors**

None in the package’s bounded scientific claim. The only hard failure I hit was environmental:
`verify_audit.py` could not run in this session because it creates mutated temp copies and the
sandbox provides no writable temp directory. That is a replay limitation here, not evidence of a
scientific or logical defect in the package itself.

**Caveats**

- The verifier replay is incomplete in this read-only environment. I reran
  `derive_reconstruction.py` and `independent_reconstruction.py` directly, and I inspected
  `verify_audit.py` plus the saved `VERIFICATION_RESULT.json`, but I could not execute the mutation
  harness end-to-end.
- The strongest genuinely new content is partial. The “correspondence” home is mostly a sharpening
  of the adopted `WORKING POSIT`, not a new metric theorem. The metric-native advance is narrower:
  completion data already give a real partial global-to-local admissibility piece, while
  cover/descent/readout stay nonselecting.
- The nonuniqueness controls are logically adequate against any claim that “same readout + same
  symmetry” forces a unique relation, but they are finite exact countermodels, not a classification
  theorem for all admissibility relations.

**Replay numbers**

- `derive_reconstruction.py`: passed. Output matches the prose and saved `RESULT.json`.
- `independent_reconstruction.py`: passed. Output matches the production replay and saved
  `INDEPENDENT_RESULT.json`.
- Cover/reconstruction control: cover-A descent dimension `4`, cover-B descent dimension `4`,
  descent+readout graph rank `4`, nullity `4`, global configuration dimension `4`.
- Monodromy control: `8` graph witnesses, all graph dimensions `2`, all `28` graph pairs distinct,
  pairwise intersection histogram `{0: 16, 1: 12}`, nonzero ambiguous endpoint-line pairs `12`,
  zero endpoint pair in all graphs.
- Counterrelation control on the `16`-point rational grid: survivor counts
  `A_reconstruction_identity = 16`, `A_product = 2`, `A_quadratic = 4`.
- Saved verifier record: `21` checks passed, `12` mutations caught, status `PASS`.

**Whether the correspondence framing is a genuine refinement**

Yes, but only as a bounded refinement.

It is not mere relabeling, because it adds two exact controls the parent audits did not yet package
together this way: `restriction/descent/reconstruction + readout` is shown explicitly to preserve
the full configuration nullity, and `same readout + same observer symmetry` is shown explicitly not
to determine a unique admissibility relation. That is a real sharpening of the August 1
ownership/open-return results.

But it is not a new physical closure law. The correspondence form `K subset O x C` comes from the
owner-authorized `WORKING POSIT`; the metric contribution is only the partial kinematic join piece
from monodromy/seam/conditional-cap fibers.

**Strongest bounded conclusion**

The package supports:

`DERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE__WORKING_POSIT_REQUIRES_BUT_DOES_NOT_DERIVE_COMPLETE_RETURN`.

More plainly: under the adopted working posit, the right mathematical home is a possibly
multibranch admissibility correspondence, not a scalar optimizer or automatic self-map. Current
metric/completion data contribute a genuine but partial global-to-local kinematic restriction at
joins. Ordinary descent/refinement/reconstruction and free readout remain nonselecting, and neither
readout nor observer symmetry determines the missing interior return relation. Action, source,
carrier, density, boundary law, mass, `X_max`, stability, and dynamics remain open.
