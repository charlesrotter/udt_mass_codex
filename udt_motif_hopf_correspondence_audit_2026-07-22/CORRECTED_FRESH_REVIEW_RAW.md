# Verdict: FAIL

The corrected scientific maximum and `LEAD` status survive, but the package’s `VERIFIED-WITH-CAVEATS` certification does not. The failure concerns the correction contract and verifier strength, not the raw census or toric/Hopf algebra.

## Blocking findings

1. The nonlinear edge-covariance correction is not implemented as claimed.

[verify_review_corrections.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/verify_review_corrections.py:141) reuses the same Jacobian `j` at every path node. The frozen transforms have nonzero second and third jets but constant stored Jacobians ([verify_motif_atlas.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_instrument_motif_atlas_2026-07-21/verify_motif_atlas.py:425)). Consequently, the edge test uses a fixed component-frame transformation, not a nonlinear chart whose Jacobian varies along the path.

A post-review read-only probe interpreted those coefficients as global polynomial maps with node-dependent Jacobians. It still found zero discordances over all 63,438 eligible comparisons, so I found no numerical counterexample. However, that post-outcome probe was neither the preregistered implementation nor package evidence and cannot repair the certification retrospectively.

2. Uncertain and skipped covariance cases are not retained and counted as preregistered.

The contract explicitly requires “every uncertain/discordant case retained and counted” ([correction preregistration](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/ADVERSARIAL_REVIEW_CORRECTION_PREREGISTRATION.md:58)). Independent replay found:

- 60 uncertainty-bearing point comparisons: 34 one-sided classified/uncertain and 26 both uncertain.
- 50 of 63,488 possible edge comparisons skipped by the unconditional `continue` at [verify_review_corrections.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/verify_review_corrections.py:198).

None is counted or classified in `REVIEW_CORRECTION_RESULT.json`. The report states only 63,438 successful comparisons and zero discordance ([AUDIT_REPORT.md](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/AUDIT_REPORT.md:84)).

3. The “13 mutation catches” are literal but do not make the validator fail-closed.

All 13 listed mutations are passed through `validate_result` and rejected. But independent mutations of the following load-bearing fields all survived that same validator:

- edge comparison count set to zero;
- intrinsic covariance residual set to `1e9`;
- sampled-path status promoted to `CONTINUOUS_BUNDLE_THEOREM`;
- symbolic angular gap replaced with nonsense;
- seed source SHA-256 corrupted;
- seed sample count reduced from 1,000 to one.

The top-level verifier checks only selected status/count fields ([verify_package.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/verify_package.py:65)). Therefore the 13 catches cannot support the package’s broad correction-validation claim.

## Findings that passed

- An unchanged temporary-copy execution of `verify_package.py` reproduced all three banked outputs byte-for-byte.
- Raw-ledger keys are unique and counts reproduce exactly: 3,072 identities, 1,618,944 path rows, 95,232 summaries, and 143,487 distribution rows.
- All distribution records retain `GLOBAL_DATA_ABSENT`; all 13 uncertain stencils remain present.
- Frobenius claims are honestly restricted to `REGISTERED_CHART_ONLY`.
- Independent metric algebra reproduced
  \[
  H^\mu{}_\nu=\mathrm{diag}\left(0,-A'/A^3,\frac{\Omega'/\Omega-1}{A^2},\frac{\Omega'/\Omega+1}{A^2}\right),
  \]
  angular gap \(2/A^2\), and
  \[
  \mathcal A=\frac{d\xi_1+e^{4\phi}d\xi_2}{1+e^{4\phi}}.
  \]
- Independent direct execution of the frozen `hopf_seed` agreed at maximum residual \(6.46\times10^{-15}\).
- Frozen-source hashes and manifest contents passed.
- The supplied circle action, absent construction-time `S2` carrier, and absent `L2+L4` functional are correctly separated in the report.
- Sampled-path wording and overall `LEAD` status are appropriately conservative.

## Four evidence gates

1. Preregistered: **NO** for the correction as executed; uncertainty accounting and genuine path-dependent nonlinear coordinates were not implemented.
2. Full space or bounded scope: **YES** for the registered raw census; incomplete for the claimed covariance accounting.
3. Independently verified: **YES** for the bounded census and toric/seed witness; **NO** for the package’s fail-closed covariance certification.
4. Premises audited: **YES in the scientific prose**, but incompletely enforced by machine validators.

## Strongest honest maximum

The evidence still supports, but does not package-certify as fully corrected:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

plus

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The overall motif-to-Hopf correspondence remains a `LEAD`. Continuous/global continuation, toric-stratum and circle-action selection, caps, carrier emergence, action, dynamics, stability, source, and mass remain open.

No repository file was intentionally edited; all write-producing verification ran in a temporary mirror.