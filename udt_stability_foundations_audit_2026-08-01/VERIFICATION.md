# Final verification — UDT stability foundations

Date: 2026-08-01  
Branch: `codex/stability-foundations-audit-2026-08-01`  
Base: `5adeb59dde063770c0619d37b76b03f735d82038`  
Preregistration commit: `134c163`

## Four evidence gates

1. **Preregistered: PASS.** The 94-path, 13-premise contract was committed before result artifacts.
2. **Full space or bounded scope justified: PASS.** This is the complete frozen current-authority
   source/type audit declared in the preregistration, not a field-solution or stability solve.
3. **Independently verified on the load-bearing premise: PASS.** A fresh stdlib-only verifier did
   not import the producer, independently reconstructed the countermodels and source semantics,
   required two amendments, and closed them through a same-verifier pass.
4. **Every premise audited: PASS with disclosed forward freeze.** The 13 direct premises are fully
   populated. Four transitive authorities discovered by the cold verifier are explicitly
   post-outcome/not-preregistered and forward-frozen; they introduced no semantic conflict.

Grade: **VERIFIED-WITH-AMENDMENTS / CLOSED-PASS**. Scientific outcome:
`FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED`; present operational stability:
`CONDITIONAL_STABILITY_ONLY`.

## Exact checks

- Producer: **17/17** checks, comprising 12 substantive and 5 guards; **7/7** mutation catches.
- Producer determinism: two consecutive runs had byte-identical stdout, JSON, and generated TSVs.
- Producer result SHA-256:
  `8eebb99176e07430ea9d82f763b0079cbec28377a0be96a893aa462655e5d0f0`.
- Producer stdout SHA-256:
  `77fedd8ece8c888087a6e893353ac7a668a3b04ea41789c527c394a10bee91f8`.
- Initial cold verifier: **30/30** checks and **7/7** mutations; it returned
  `PASS-WITH-REQUIRED-AMENDMENTS` rather than silently passing the two defects.
- Amendment verifier: **10/10**, deterministic across two runs.
- Historical amendment closure: **28/28** plus **8/8** mutations; one stale count word found.
- Final same-verifier closure: **28/28** plus **9/9** mutations, zero failures, `CLOSED-PASS`.
- Original direct source identities: **94/94**.
- Forward transitive premise identities: **4/4**.
- Current premise verifier: **18** premise guards, **9** startup controls, **754** candidate
  dispositions, pass.
- Test baseline: **70 passed, 1 expected xfail**.
- Accepted P4 review-repair manifests and 13 transitive dependencies: all hashes pass.

## Amendments retained as evidence

1. The four transitive premise sources were absent from the original direct freeze. They are now
   forward-frozen without rewriting the preregistration.
2. The realized-coexistence gate is a compatible pullback/fiber product, not a literal intersection
   of module images. A time/angular-live claim requires nonzero live sectors, and the static/mode-zero
   control is rejected.
3. A final explanatory sentence was corrected from six to seven producer mutations. The verifier
   proved that reversing this single phrase reconstructs the prior file hash exactly.

## Stop line

The package does not derive stable matter or authorize T4. It selects no action, response law,
carrier, source, boundary, mass, bootstrap map, physical branch, GPU work, canonization, or
repository reorganization. It is not integrated into `grok` by this audit commit.
