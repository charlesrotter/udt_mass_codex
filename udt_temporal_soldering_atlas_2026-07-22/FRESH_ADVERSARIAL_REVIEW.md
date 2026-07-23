# Fresh Adversarial Review

Date: 2026-07-22

Final status: `PASS`

The review was performed in a fresh read-only agent context. The reviewer did not edit files or
mutate repository state.

## Scientific review

- The exact algebra is sound: for non-null `dphi`, with
  `s=g^{-1}(dphi,dphi)` and `D=grad(phi) tensor dphi`, `D^2=sD` and `P_phi=D/s`
  is a metric-self-adjoint rank-one projector with kernel `ker(dphi)`.
- The timelike and spacelike complement signatures and the exact local integrability of
  `ker(dphi)` follow as reported.
- Independent aggregation reproduced 95,232 path presentations, 720 `LINE_PLUS_THREE` paths,
  1,055 `FOUR_LINES` paths, 12,240 timelike-phi nodes, 36,720 spacelike-phi nodes, and the
  consolidated node census.
- The production and independent routes are materially distinct for metric jets, projector
  reconstruction, signatures, and Frobenius calculations.
- The two threshold conflicts were frozen before refinement; both routes resolve both as
  integrable, while the original production evidence remains preserved.
- No physical branch, global time, physical clock, particle/cosmic interpretation, carrier,
  action, source, or emergence is overclaimed.

## Evidence-layer correction and final replay

The first adversarial pass required two corrections: removal of an unsupported CPU-oversubscription
phrase and replacement of tautological catch assertions with explicit corruption tests. Those
defects were preregistered in `ADVERSARIAL_EVIDENCE_CORRECTION_PREREGISTRATION.md` before mutation.

The final review confirms:

- all 20 package catches and all 20 independent catches perform one coherent explicit mutation on a
  previously validated deep-copied evidence state;
- every mutation is rejected by the named fail-closed validator with the expected reason;
- action, carrier, and SNe-fit mutations are exercised separately;
- paired census edits are coherent single reclassification mutations;
- `REPLAY_RESULT.json` reports `PASS`, all seven stages exit zero, and all regenerated outputs are
  byte-identical;
- both required corrections are closed and no scientific evidence or claim boundary changed.
