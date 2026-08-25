# G257 fresh external review — gpt-5.4

Date: 2026-08-25
Sealed intake: `/tmp/udt_g257_review_Wfi05xVb`
Scope SHA-256: `ce4040741ff40233a340be8b702010ea0ba6bb43e063605cf36d36fe3e156144`
Disposition: `ACCEPT`

The text below is the reviewer's verbatim final message. Its links retain the sealed-intake paths
used during review.

`ACCEPT`

**Findings**
- Scientific defects: none found within the sealed, bounded scope.
- Packaging defects: none material found. The package consistently marks W3 as provisional, treats GR vacuum only as an imported comparison condition, and keeps the UDT departure law open, so I do not see a conclusion-ceiling breach ([PREREGISTRATION.md:33](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/PREREGISTRATION.md:33), [EXACT_DERIVATION.md:99](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:99), [AUDIT_REPORT.md:72](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/AUDIT_REPORT.md:72)).

**Adjudication**
1. Yes. The direct tensor derivation gives
   `G^t{}_t=G^r{}_r=(rf'+f-1)/r^2` and `G^theta{}_theta=G^varphi{}_varphi=f''/2+f'/r`, with exact dependence `r dE0/dr=2E1`; solving `E0=0` yields the complete bounded family `f=1+C/r` on each connected `f>0` interval, and the writeup explicitly checks full Ricci/Einstein vanishing on that family ([EXACT_DERIVATION.md:25](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:25), [EXACT_DERIVATION.md:47](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:47), [EXACT_DERIVATION.md:53](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:53), [EXACT_DERIVATION.md:60](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:60)).

2. Yes. `E0,E1` are correctly typed as exact bounded GR-vacuum comparison residuals, not as a UDT law, and their dependence is stated and used exactly rather than heuristically ([PREREGISTRATION.md:34](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/PREREGISTRATION.md:34), [EXACT_DERIVATION.md:91](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:91), [EXACT_DERIVATION.md:99](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:99)).

3. Yes, with the stated conditionals. The pair formulas are derived on the same `f` branch under matched static endpoint calibration/W1, with no fitted coefficient or added response; the angular amplitudes are the previously pinned G201 primary amplitudes evaluated on that same GR branch ([EXACT_DERIVATION.md:115](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:115), [EXACT_DERIVATION.md:140](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:140), [EXACT_DERIVATION.md:153](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:153), [AUDIT_REPORT.md:31](/tmp/udt_g257_review_Wfi05xVb/udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/AUDIT_REPORT.md:31), [AUDIT_REPORT.md:22](/tmp/udt_g257_review_Wfi05xVb/udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/AUDIT_REPORT.md:22)).

4. Yes. The distinction between weak GR quietness and exact zero geometry is scientifically sound in the stated exterior scope: the package defines quietness by vanishing GR residual on the branch together with small `|u|`, while separately showing nonzero curvature on that branch, so “weak GR” is not confused with flatness ([EXACT_DERIVATION.md:185](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:185), [EXACT_DERIVATION.md:192](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/EXACT_DERIVATION.md:192), [AUDIT_REPORT.md:50](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/AUDIT_REPORT.md:50)).

5. I do not find an algebraic, typing, provenance, scope-completeness, or conclusion-ceiling defect in the sealed intake. The important caveats are disclosed rather than hidden: W3 is `WORKING/POSIT`, W1 is conditional, the GR vacuum equation is comparison-only, and matter/horizon/time-dependent/nonspherical/global sectors are excluded ([PREMISE_LEDGER.tsv:6](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/PREMISE_LEDGER.tsv:6), [PREMISE_LEDGER.tsv:8](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/PREMISE_LEDGER.tsv:8), [PREREGISTRATION.md:24](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/PREREGISTRATION.md:24), [AUDIT_REPORT.md:82](/tmp/udt_g257_review_Wfi05xVb/udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/AUDIT_REPORT.md:82)).

A bounded independent recomputation of the mixed Einstein components, the residual identity, and the GR-branch angular substitution agreed with the package formulas. The remaining risks are exactly the declared scope limits, not defects in this bounded audit.
