# Cold repair replay request

Read-only. Inspect the original `COLD_REVIEW_RETURN.md`,
`POST_REVIEW_CORRECTION_PREREGISTRATION.md`, `LOAD_BEARING_SOURCE_LOCATORS.tsv`,
`POST_CORRECTION_SOURCE_LOCATORS.tsv`, `DATE_RULE_ADJUDICATION.tsv`,
`SEMANTIC_FAMILY_RULES.tsv`, `ACTIVE_REGRADING_LEDGER.tsv`, `AUDIT_REPORT.md`, both regrade
verifiers, and their current results.

Determine independently whether:

1. locator rows `L13`-`L18` now unambiguously resolve against frozen base `682adb6c`, while the
   seven current corrected locations are separately exact;
2. all 254 old F18 identities are preserved exactly once with identity SHA-256
   `e85e3a26940e9369dd7ff6b24da33c2cac493de9f19084e671d9f48870fc4e98`;
3. exactly the C1 packet, founding reciprocal derivation and its verifier move from the
   date-inferred historical class to conditional current founding evidence;
4. the other 251 identities retain historical/superseded scientific authority for explicit
   family reasons rather than date alone;
5. corrected totals are 1,091 conditional, 335 historical, 99 conclusion-regraded, 40 frozen and
   zero immediate rederivation; and
6. no physics, action, source, pointwise owner, `Xmax`, bootstrap return, or mass claim was promoted.

Return `REPAIR_ACCEPTED` or `REPAIR_REJECTED` with exact load-bearing objections. Do not edit files.
