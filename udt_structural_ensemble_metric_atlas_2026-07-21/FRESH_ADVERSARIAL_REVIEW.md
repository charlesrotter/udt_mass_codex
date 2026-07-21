# PASS-WITH-CAVEATS

The finite ledger is numerically and algebraically consistent in its registered scope. No blocking algebraic defect was found.

Independent read-only recomputation found:

- Both frozen-parent manifests replay completely: 31/31 and 24/24 entries.
- The 11 controls form the stated disjoint `3+3+4+1` partition.
- All 48 carriers exactly match the preregistered parent rows.
- All 16 masks, 6,144 configuration identities, 5,760 interaction identities, and 135 span-rank rows are present and unique.
- Metric two-jets rebuilt from slot jets agree within `4.44e-16`.
- All saved curvature and split-kinematic quantities recompute exactly at stored precision.
- An independent Boolean Möbius transform reproduced every interaction norm within `2.25e-16` and every span result within `4.98e-16`.
- No Möbius activity or span rank lies in the registered uncertainty band.

Caveats and defects:

1. Package verification is not fully independent. The verifier duplicates the evaluator’s curvature, Weyl, shear, twist, payload-flattening, threshold, and rank conventions. It recomputes curvature from saved metric jets but does not independently regenerate the primitive slot jets from the analytic banks and coordinates. Thus it verifies internal consistency conditional on the frozen raw jets.

2. The advertised “23 exercised corruption catches” are substantially overstated. Most catches manually throw assertions after tautological comparisons rather than corrupting an artifact and exercising the actual validation path. The `phi_source_promotion`, authority, GPU, and physicalization catches especially do not establish the claimed absence.

3. [ANTI_IMPOSITION_AUDIT.tsv](ANTI_IMPOSITION_AUDIT.tsv) is builder-generated with hard-coded `ABSENT` values; the verifier merely checks those values. It is a declaration, not an independent content audit.

4. The 120 uncertain configurations are correctly retained. They occur only in `M1`, `M2`, `M9`, and `MA`. The two `K5` rows are the same `V013_B2_P2` metric jet with and without phi; their sixth curvature singular value is `1.77e-11`, below the `1e-9` cutoff and inside the uncertainty band. No robust rank-five conclusion follows.

5. Ranks use a fixed absolute `1e-9` threshold without normalization, condition-number analysis, coordinate rescaling, or higher-precision sensitivity testing. Consequently rank labels and component-space dimensions are numerical chart diagnostics. The principal Möbius conclusions nevertheless have comfortable registered margins: the smallest active core-triple Riemann component is `8.49e-6`.

6. “Exact” zero language means zero at the registered threshold or inherited algebraic construction. Phi independence is imposed because beta never feeds the metric; it is not learned from the atlas.

7. Pair/triple “interaction” is only Boolean inclusion–exclusion of nonlinear curvature assembly. [AUDIT_REPORT.md](AUDIT_REPORT.md) mostly preserves this boundary, but the “orchestra,” “symphony,” “couples,” and “what the complete metric itself is doing” phrasing in the lay/next-decision reports is rhetorically stronger than the evidence. No coupling, force, source, action, or causal mechanism is established.

8. “Complete” applies only to the Cartesian product of 48 registered carriers, 16 masks, and eight contexts. The 6,144 identities contain only 5,092 distinct configuration hashes and 2,369 distinct metric-jet hashes; duplicates were properly retained.

9. The partition, Möbius terms, active components, and span ranks can change under coframe choice, chart, base/screen split, field basis, nonlinear reparameterization, or scaling. Functions, continuum amplitudes, alternate charts, global completion, boundaries, topology, dynamics, physical scale, carrier selection, and physical selection remain excluded.

Four gates:

1. Preregistered: documented and hashes match, but structural preregistration chronology was not independently re-established under the mandated no-Git audit.
2. Scope: justified only as the registered finite chart-level atlas.
3. Independent verification: yes for the saved numerical ledger in this audit; conditional on the frozen primitive jets.
4. Every premise audited: no—shared-formula independence, chart invariance, and excluded global/physical premises remain open.

Maximum defensible grade: `VERIFIED-WITH-CAVEATS`. No repository files were edited.
