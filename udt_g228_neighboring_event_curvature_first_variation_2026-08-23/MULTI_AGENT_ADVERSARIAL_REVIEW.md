# G228 fresh multi-agent adversarial review

Date: 2026-08-23

All reviewers were launched fresh with no conversation context, were restricted to read-only work,
and did not inspect protected packages.

## Lorentzian tensor reviewer

Agent: `/root/g228_lorentzian_adversary`

Initial verdict: `ACCEPT_WITH_REPAIRS`.

Independent full-slot reconstruction retained all 84 raw symmetric-bivector derivative entries.
It found algebraic-Bianchi rank `4`, combined rank `24`, incremental differential-Bianchi rank
`20`, module dimension `60`, and subset projection ranks `20,40,54,60`. It confirmed the G227
bivector sign, differential cyclic ordering, null tetrad, moving-screen commutator, and both Jacobi
connection blocks.

Required repairs:

1. reverse the neighboring-tensor pullback notation to `P_{p->q}^* R_q`;
2. keep all rank conclusions explicitly algebraic differential-Bianchi-compatible and distinguish
   them from metric-3-jet/smooth realization;
3. replace the generic Hamiltonian finite-phase control with an admissible G188 Jacobi witness;
4. build the final evidence manifest after repair.

## Screen/symplectic reviewer

Agent: `/root/g228_symplectic_adversary`

Initial verdict: `ACCEPT_WITH_REPAIRS`.

The reviewer independently derived

```text
T_E' + [Omega,T_E] = C^T T' C
A_E = [[-Omega,I],[-T_E,-Omega]]
```

and verified that `A_E` is Hamiltonian precisely for symmetric tide and skew screen connection. It
confirmed that `C(lambda)` is gauge choice, not G225-selected transport, and that no extra angular
coefficient was introduced.

Required repairs:

1. call the generator Hamiltonian and its transfer symplectic;
2. state the G188 curvature-sign convention and distinguish the underlying affine generator from
   a continuously clock-normalized G226 generator;
3. replace the generic finite-phase ambiguity with the Liouville/Schwarzian G188 Jacobi family.

## Evidence reviewer

Agent: `/root/g228_evidence_adversary`

Initial verdict: `ACCEPT_WITH_REPAIRS`.

The reviewer confirmed that commit `b54f4c51` predates every production result and that the tracked
pre-outcome bytes were unchanged before repairs. It independently replayed the exact ranks, all 15
census entries, all 15 syzygy lists, source hashes, and screen identities.

Required repairs:

1. add and verify the final evidence manifest;
2. expand aggregate saved-artifact checking beyond three JSON files;
3. add an orthogonal full-index tensor anchor or narrow the independence grade;
4. replace two weak hostile controls with actual mutants and audit the outcome reports for value-
   generation promotion;
5. retain frozen-census and necessary-compatibility scope throughout.

## Implemented repair set

- corrected the tensor pullback type;
- preserved the original preregistration hash and recorded the post-review type/evidence repair;
- added `verify_full_index_anchor.py` and `FULL_INDEX_ANCHOR.json` using the unreduced 84-slot
  representation;
- replaced the finite-phase control by a regular Liouville-reparameterized one-period Jacobi tide
  with identical identity transfer and different initial tide derivative;
- replaced the zero-stub algebraic duplicate and positive one-ray recheck by actual wrong-constraint
  mutants;
- expanded the aggregate verifier to saved JSON, TSV census, syzygy basis, source hashes, and the
  full-index anchor;
- narrowed every result statement to necessary algebraic differential-Bianchi compatibility on the
  frozen linearly independent subset census;
- distinguished Hamiltonian generators, symplectic transfers, affine G188 phase, endpoint-normalized
  G226 phase, and G225 pointwise screen comparison.

Repair-only follow-up verdicts are recorded in `REPAIR_VERIFICATION.md`.

All three follow-ups accepted the repaired science and evidence. The tensor and evidence reviewers
identified only stale pre-repair counts in `EVIDENCE_GATES.md` and `RUN_LOG.txt`; both were corrected
before final manifest construction.
