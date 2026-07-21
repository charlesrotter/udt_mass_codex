PASS-WITH-CAVEATS

No blocking algebraic or evidence-ledger defect remains. Maximum justified grade: `VERIFIED-WITH-CAVEATS`.

Correction findings:

- Analytic regeneration: PASS. An independent direct-polynomial implementation regenerated all 6,144 slot/phi two-jets, reassembled the metrics, and calculated curvature from those rebuilt metrics. Maximum disagreements were:
  - primitive jets: `2.220446049250313e-16`
  - metric jets: `4.440892098500626e-16`
  - curvature/Weyl/Ricci/scalar: `3.0531133177191805e-16`
  - kinematics: `4.163336342344337e-17`
- Verifier correction: PASS. The current [verifier](verify_structural_ensemble_atlas.py), SHA-256 `5f2f13bde0d8737bbd6f62b6577e91cb0389949b56943cb036a91564c6086362`, now uses regenerated slots, reassembled metrics, rebuilt curvature/kinematics, and reconstructed payload cubes throughout.
- Negative tests: 30/30 fired in an isolated replay. Twenty-seven mutate copies of package data structures; three are algorithm/expected-digest tests rather than literal artifact mutations. None uses the former manually forced assertion pattern. Thus the correction is material, though “30 artifact-mutation catches” remains slightly imprecise.
- Authority gates: PASS. Ten separate fields and mutations prohibit physical interaction, physical Möbius coupling, phi sourcing, ensemble ontology, action/EOM, dynamics, solutions, physics ranking, finite exhaustiveness, and GPU use.
- Anti-imposition: manual semantic review PASS. The machine only checks declaration consistency; independently reading the code and reports found no hidden physical promotion. The [audit report](AUDIT_REPORT.md) and [lay report](LAY_REPORT.md) now consistently describe Boolean nonlinear remainders—not forces, couplings, sources, or mechanisms.

Exact replay:

- Parent manifests: `31/31` and `24/24`.
- Partition: `3+3+4+1`; carriers: `48/48` exact parent rows.
- Masks/configurations/interactions/span rows: `16 / 6,144 / 5,760 / 135`, complete and unique.
- Distinct hashes: `5,092` configuration and `2,369` metric-jet hashes; duplicates retained.
- Möbius norm errors: L2 `≤4.46161098096929e-16`; max-component `≤4.440892098500626e-16`; span singular values `≤1.7763568394002505e-15`; margins exact.
- Riemann activity:
  - `M3`: `384/384`, rank `19`, minimum active `1.1022444689885152e-3`
  - `M5`: `384/384`, rank `20`, minimum `8.20369194574861e-4`
  - `M6`: `384/384`, rank `20`, minimum `2.3196296521397564e-3`
  - `M7`: `336/384`, rank `20`, minimum active `8.487611927782048e-6`; 48 inactive `B0:P0` rows have maximum `8.326672684688674e-17`
- Screen–shift metric term `M6`: `384/384`, span rank `105`.
- Uncertain configurations: `120`—`M1:36`, `M2:24`, `M9:36`, `MA:24`.
- The two `K5` rows share one metric jet; sixth singular value `1.771577695204194e-11`.
- Phi-containing Riemann terms: maximum `2.7755575615628914e-17`; this is built-in phi independence, not derived physics.

Remaining caveats:

- Results depend on the chosen chart, coframe, base/screen partition, field basis, and parameterization.
- Ranks use the fixed absolute `1e-9` threshold without normalization or high-precision sensitivity analysis.
- The design is finite, not continuum/global exhaustive.
- Möbius “interaction” is inclusion–exclusion bookkeeping only.
- Preregistration hashes are frozen, but chronology was not independently reconstructed because the audit prohibited git.

Four gates:

1. Preregistered: PASS-WITH-CAVEAT—documents and hashes match; chronology not independently established.
2. Full space or bounded scope: PASS—complete only within the registered finite design.
3. Independently verified: PASS—all load-bearing jets, curvature, kinematics, Möbius rows, ranks, and margins reproduced.
4. Every premise audited: PASS for the bounded chart-level claim; invariance and physical/global premises remain explicitly open.

No repository files were edited and git was not used.
