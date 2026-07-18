# GR -> UDT selector audit preregistration

Date: 2026-07-18  
Branch: `grok`  
Starting commit: `ded310a` (`Freeze final native-action A/B/C adjudication`)  
Frozen adjudication package: `native_action_final_adjudication_2026-07-18/`  
Frozen package-manifest SHA-256: `57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33`

## Authorized scope

1. Verify the frozen final-adjudication package without changing it.
2. Add an external verifier with an exactly pinned SymPy environment.
3. Run that verifier in a fresh CPU-only virtual environment and an external work directory.
4. Construct a GR -> UDT selector audit from the accepted final adjudication and its immutable A/B/C inputs.
5. Update `LIVE.md`, `HANDOFF.md`, `INDEX.md`, and `MEMORY.md` so startup reaches the adjudication at `ded310a` and the selector audit.
6. Commit and push the authorized additions and pointer updates.

Excluded: canonization, GPU work, carrier assumptions, new derivation arms, repository reorganization, deletion, and any edit or permission change inside the frozen package.

## Classification vocabulary frozen before audit

- `INHERITED`: retained from the GR comparison frame, without claiming that C0/C1 derives it.
- `MODIFIED`: retained in altered form because an existing UDT selector changes its domain or interpretation.
- `REJECTED`: not admissible as the default/native UDT choice. This does not erase a separately stated conditional branch.
- `OPEN`: C0/C1 and the accepted audit do not select among the live alternatives.

A row may have one primary classification and an explicit open residue. The residue must not be hidden by the primary label.

## Preregistered selector ledger

| Item | Primary classification | Preregistered reason / residue |
|---|---|---|
| Four-dimensional arena | INHERITED | The conditional C2 and EH comparisons use the GR four-dimensional arena; C0/C1 does not derive the dimension count. |
| Dynamical-field census | OPEN | Metric-only, coframe, explicit scalar, multiplier, and readout-only completions are not selected. |
| Covariance class | OPEN | Full diffeomorphism covariance is usable conditionally but is not forced by C0/C1. |
| Locality | OPEN | CSN does not select local versus nonlocal dynamics. |
| Variation domain | OPEN | Unrestricted metric variation, constrained variation, multiplier enforcement, and readout interpretations remain live. |
| Derivative order | OPEN | Neither the second-order EH restriction nor the fourth-order C2/Bach route is forced. |
| Boundary completion | MODIFIED | The finite mirrored cell replaces the usual spatial-infinity ontology; the differentiable boundary functional and native charge remain open. |

The four UDT-native selectors to be tabulated are already named by the authorized record: Reciprocity, Common-Scale Neutrality, finite-cell structure, and bootstrap closure. The audit may state what each already selects and what it does not select; it may not strengthen any of them into a new action principle.

## Branch comparison hypotheses

- `Pre-scale C2`: UNIQUE-CONDITIONAL only under the accepted metric-only, local, parity-even, four-dimensional, exact-CSN/Weyl-compatible, curvature-squared and variation premises. Its Bach equation is fourth order; source, boundary, global solution, and stability closure remain open.
- `Post-scale EH`: CONDITIONAL only after a physical scale/representative is available and under the accepted metric-only, local, generally covariant, unrestricted-variation, at-most-second-order/Lovelock premises. It is not an exact pre-scale CSN invariant, and its normalization, cosmological term, source, and boundary completion remain open.
- `Two-stage bridge`: admissible only as a possibility. A finite-cell/bootstrap rule would first have to select a physical representative or scale; a further demonstrated matching rule would be required to obtain EH rather than merely permit it. No bridge is to be reported as derived.

## Smallest-missing-selector decision rule

The audit will distinguish two questions:

1. The smallest immediate discriminator at the C2/EH fork is whether variation is fundamental on the pre-scale CSN equivalence class or on a physical representative selected after finite-cell/bootstrap closure.
2. That discriminator alone cannot derive a complete action. If independent field-census, covariance, locality, variation-domain, derivative-order, source, or boundary premises are still required, the audit must say that no single selector presently closes the action.

This is an identification of the smallest already-exposed logical fork, not the invention of a new UDT postulate.

## External-verifier acceptance gates

Dependency lock:

```text
sympy==1.13.1
mpmath==1.3.0
```

The `mpmath` pin closes SymPy's runtime dependency rather than adding a physics input.

The verifier must:

1. live outside `native_action_final_adjudication_2026-07-18/`;
2. make no writes, chmod operations, or metadata changes to that package;
3. independently validate the internal manifest and the expected external manifest hash;
4. copy the 24 load-bearing CAS scripts to an external clean work tree and run those copies with `PYTHONNOUSERSITE=1`, `PYTHONDONTWRITEBYTECODE=1`, an empty CUDA visibility, and the pinned virtual environment;
5. require zero exit status, empty stderr, and byte-exact stdout agreement with the frozen outputs for every script;
6. record Python, SymPy, and mpmath versions and confirm execution from a virtual environment with user-site disabled;
7. include catch-proof checks showing that an altered manifest value, altered stdout, nonzero exit status, or dependency-version mismatch would fail;
8. recompute the complete package state after execution and require byte-for-byte hash identity with the pre-run state; and
9. emit its result outside the frozen package.

Acceptance requires all 24 replays to pass, all catch-proof probes to pass, and identical package-manifest and complete per-file hashes before and after. Any failure stops pointer promotion and is reported rather than repaired inside the frozen package.

## Evidence and provenance rule

Affirmative status language remains bounded by the July 1, 2026 provenance firewall and the accepted final adjudication. Pre-July-1 material may expose a failure, fork, or counterexample, but may not supply affirmative UDT physics. The selector audit is a classification and dependency map, not canonization or a new derivation.
