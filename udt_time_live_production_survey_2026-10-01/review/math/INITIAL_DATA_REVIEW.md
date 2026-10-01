# TPS1 supplied initial-data review

All156 mesh-specific initial states passed the frozen independent checks:
78 supplied datasets on24³ and32³, with no omitted state. Maximum original
Hamiltonian, momentum and harmonic-vector residuals are respectively
5.29932e-12,6.86821e-14 and2.59326e-15 against2e-5. Maximum TT trace/divergence
are3.33067e-16/4.21191e-15; independent transverse-SVD reconstruction differs
from the supplied seed by at most4.44089e-16. Every deliberately perturbed
harmonic velocity was detected, with residual at least.010.

The check authenticated each state against the actual234-case manifest,
reconstructed live ADM quantities from saved g/v, checked the saved gamma/K
correspondence and spatial positivity, and reused the fixed independent TDS1
original constraint/harmonic implementations. The method/exposure record is
`SOURCE_FIRST_PLAN.md`; `CHECKER_FREEZE.json` preceded new initial outcomes.
`ALL_INITIAL.json` binds all input and checker hashes and gives per-state values.

The no-timeout capture recorded36.603seconds,153660KiB peak RSS and a2GiB
address-space cap. No GPU was used. The exact/nonvacuum and interface controls
are in `PREPRODUCTION_CONTROLS.json` and `preproduction_adapter_controls.stdout`.
Earlier control captures remain preserved as pre-freeze engineering history.

This checks the finite supplied initial states, not their evolution or generic
admissibility. The flat-conformal/CMC seed, marked periodic torus and mode
families are still restrictions; no native UDT law or physical population is
selected. First-three-history original-equation/refinement checks remain pending.
