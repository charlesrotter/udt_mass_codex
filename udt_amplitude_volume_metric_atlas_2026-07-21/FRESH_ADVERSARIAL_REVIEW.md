# PASS-WITH-CAVEATS

No load-bearing numerical failure found within the exact registered sample.

- Preregistration: PASS. Commit `8abe84b` contains only [PREREGISTRATION.md](PREREGISTRATION.md); outcome artifacts were not in its parent or that commit.
- Design: independently reconstructed. All 64 Halton rows and 80 radial rows match; ranks are 10 metric/11 complete, with radial-direction rank 11.
- Retention: 1,160 unique IDs and 640 unique edges are present; every record is retained. Census is exactly 8 origin `R0_K0_S0_T0_M0` and 1,152 sampled non-origin `R4_K6_S2_T1_M1`.
- Curvature: fresh reconstruction from every saved metric two-jet matched Riemann, Ricci, and scalar data with maximum errors \(1.11\times10^{-16}\), \(1.39\times10^{-16}\), and \(2.22\times10^{-16}\).
- Rank artifact check: PASS. Minimum non-origin margins were \(4.55\times10^{-5}\) Ricci, \(1.43\times10^{-6}\) curvature operator, \(1.04\times10^{-5}\) shear, \(1.49\times10^{-3}\) twist, and \(8.79\times10^{-3}\) mixed curvature. The two-class census is unchanged through threshold \(10^{-6}\).
- Repeated hashes: harmless in this census. All duplicate groups are origin records; no non-origin duplicate occurs.
- Parent freeze: both named parent manifests and every file they enumerate currently pass `sha256sum -c`.

Caveats and flaws:

1. The package verifier reconstructs curvature from metric jets at only three anchors; for the other 1,157 rows it reranks already-saved curvature tensors. Thus “all-record reconciliation” is accurate, but “all-record independent curvature reconstruction” would not be.
2. The verifier imports the frozen parent verifier’s curvature and split-rank routines. It does not share the volume builder, but it is reused evidence—not a fresh adversarial implementation.
3. Source checks hash the two manifest files, not every file listed by them. A parent-file mutation leaving its manifest untouched is not caught automatically, although the current files all match.
4. The preregistered mutation list requires changed bases, directions, and radii. The suite exercises a changed Halton coordinate and radius, but no explicit changed-base or changed-Hadamard-direction catch. It also lacks a common-mode test where builder and verifier constants drift together.
5. `NUMERIC_RANK_MARGINS.tsv` records only Ricci and curvature-operator margins. Shear, twist, and mixed-curvature margins are load-bearing parts of the class but are absent; their robustness required fresh calculation.
6. The 128 first-edge changes only distinguish sampled radii \(0\) and \(1/8\). They locate no activation threshold or bifurcation. The formal report avoids physical-transition language.
7. “Easy to activate rather than a rare accident,” “enough raw amplitude mapping,” and “no further same-chart sweep required” overstate what a deterministic, non-probabilistic finite design establishes. They are not supported frequency, rarity, or coverage-sufficiency conclusions.
8. “Volume characterized” is acceptable only as shorthand for the registered 145 amplitude identities across eight contexts—not the continuum eleven-cube. Unsampled amplitudes may contain other rank classes.
9. Functions, alternative charts, global completion, equations, dynamics, boundaries, scale, carrier, topology, and physical selection are clearly left open.

Four gates: preregistered—yes; bounded scope—yes, finite design only; independently verified—yes with the shared-code caveats above; premises audited—yes for the registered construction, not for excluded/global scope.

Maximum defensible grade: `VERIFIED-WITH-CAVEATS` for the registered finite configuration sample only.
