# Same-verifier closure report — stability-foundations amendments

Date: 2026-08-01  
Verdict: **AMENDMENT-REQUIRED**

## Result first

The two substantive cold-verifier amendments are closed:

- **A1 closes.** The four current-premise controlling sources are forward-frozen with exact roles,
  byte counts, and SHA-256 values. All four rows explicitly say
  `DISCOVERED_BY_COLD_VERIFIER_POST_OUTCOME_NOT_PREREGISTERED` and
  `FORWARD_FROZEN_NO_RETROACTIVE_CLAIM`. The original 94-path preregistration freeze was not
  rewritten.
- **A2 closes.** The fixed-realization gate is now a compatible pullback/fiber-product over one
  field assignment, equation, differentiable boundary problem, and premise stack. A live claim
  requires nonzero time-live and angular-live sectors. The same live-witness predicate rejects a
  static/mode-zero witness in both the amended producer and amendment-verifier paths.

The scientific result is unchanged and passes: `FOUNDATIONS_PARTIAL_MINIMAL_JOIN_IDENTIFIED`, with
`CONDITIONAL_STABILITY_ONLY`; fixed realized live coexistence remains `OPEN`.

One bookkeeping correction is still required before `CLOSED-PASS`: the final sentence of
`EXACT_DERIVATION.md` says the producer “exercises six mutation catches,” while
`DERIVATION_RESULT.json` and `DERIVATION_STDOUT.txt` correctly record **seven**. Change only “six” to
“seven” and return for same-verifier closure. No computed result, gate, source freeze, or scientific
verdict needs amendment.

## A1 closure

`TRANSITIVE_PREMISE_FREEZE.tsv` has exactly four rows:

| Premise | Role | Source SHA-256 |
|---|---|---|
| G01 | `FOUNDED_PHI_IDENTITY_CONTROL` | `3c7fed27fae474c8718ffe8f09dad858c12b0aba068494e2a8248fe19f642783` |
| G02 | `FOUNDED_PHI_ACTION_CONTROL` | `7a4fba1c6f9d02eb7ca12ac953d04e1c04e2b7271598dc99e51db5baeddedb08` |
| G06 | `OBSERVED_SCALE_ANCHOR_CONTROL` | `18076d2145bfb954b7a998c71de1f0eedad919c63c59ec75dcbf408a4432e0c6` |
| G12 | `BOOTSTRAP_STATUS_CONTROL` | `54f055a4800e0650e17f2a5ec842ed3a7b97fd13ef6b7a124d0c29a640c6e4dd` |

All current source bytes and sizes match. Their contents independently confirm the registered
roles: founded additive logarithmic depth; reciprocal `diag(exp(-phi),exp(phi))` action; observed
`c_E`/`G_obs` anchors; and bootstrap as on-shell admissibility with no registered same-solution
fixed point.

The transitive manifest passes 4/4. Its package hashes are:

- `TRANSITIVE_PREMISE_FREEZE.tsv`:
  `acb4a391badfdefa40ff08e08e25ceb0bef98646e3a928bcfc07291f4566803e`
- `TRANSITIVE_PREMISE_MANIFEST.sha256`:
  `93e8bd58a553ad5dd749975ea7369be3f81b1f6e3ca0cd365e390f733659eab3`

## A2 closure

The corrected artifacts consistently retain the gate as `OPEN`:

- G05 requires one common full field assignment and nonzero time/angular sectors for a live claim;
- G09 is a nonempty compatible realized pullback/fiber-product;
- S03 requires nonzero live sectors and rejects a purely static or mode-zero control;
- `EXACT_DERIVATION.md` records restriction maps, both nonzero conditions, the common equation,
  common boundary, and common premise stack; and
- `CORRECTION_LAYER.md`, `AUDIT_REPORT.md`, `COMPLETENESS_MAP.md`, and `LAY_REPORT.md` propagate the
  same distinction without promoting a solution.

AST inspection finds six calls to `live_witness_violations` in `verify_amendments.py` and one in
`derive_stability_foundations.py`. Both the baseline static control and its mutation use that same
predicate. The exact rejection is:

```text
[time_live_nonzero, angular_live_nonzero]
```

## Preservation and independent checks

The original cold-verifier artifacts remain byte-identical:

| Artifact | SHA-256 |
|---|---|
| `VERIFIER_INDEPENDENT_CHECK.py` | `4ae6fa294c2d7146d8e618d5031bcebf4bfb045753ea5632524c9b243902842e` |
| `VERIFIER_RAW.jsonl` | `cafbaea0427ee08c3f8ad1e1cbadf780ee55b880f8a2fa3dba4c34ec317c27a4` |
| `VERIFIER_RESULTS.json` | `374ac4e5c4b35fd2234058f5715e82a6da948c545ecc51a4841de7b53d40b9b1` |
| `VERIFIER_REPORT.md` | `98200cafd7376e63f5ec974d3b0d9a129b6dc20322d3302a7c9059e1471c6bb3` |

The original preregistration records also remain byte-identical:

- `SOURCE_PATHS.txt`: `dcc6d0e546589cd7fa22d89a9405dac5643db3fba7b85a4004405464b879572b`
- `SOURCE_INVENTORY.tsv`: `7fac171e72d4430a08a69fe039598845af20e49a6a504fcc2e385483a0d9fc61`
- `SOURCE_MANIFEST.sha256`: `32389f254adf1bac339dea5b9cf65ddf2c95237315b07e26e90053efb7414949`
- `PREREG_SNAPSHOT.json`: `1f7ea55bdc23b6f6942507f3cd392ed0e50daaa6e969047604979248c7362fe2`

All 94 original source identities pass. Independent standard-library algebra rechecks the stable,
unstable, and neutral flow signs and contracting/expanding fixed-point derivatives. Conditional
P4/Hopfion, action-open, fixed-solution-open, and schema-only bootstrap statuses remain unchanged.

## Exact counts and mutation record

- Amended producer: **17/17 checks**, **7/7 mutation catches**.
- Amendment verifier: **10/10**.
- Same-verifier closure: **28/28 ordinary checks**.
- Closure mutations: **8/8 caught**—missing source, retroactive promotion, source-role promotion,
  changed hash, static-as-live, joint-witness promotion, schema-to-map promotion, and original
  verifier mutation.
- Required follow-ups: **1**, bookkeeping only.

Closure machine hashes:

- `CLOSURE_VERIFIER_RAW.jsonl`:
  `145d76d405c3335fac4e63a932ab8998789fc44eee5ea57397249a28a77a36f1`
- `DERIVATION_RESULT.json`:
  `8eebb99176e07430ea9d82f763b0079cbec28377a0be96a893aa462655e5d0f0`
- `DERIVATION_STDOUT.txt`:
  `77fedd8ece8c888087a6e893353ac7a668a3b04ea41789c527c394a10bee91f8`
- `EXACT_DERIVATION.md` before the required count-word correction:
  `90da1e3d32598306fd6cfe58dc921e4c94247bcf3e51485675d546dcf30a1d03`

## Stop line

Verdict: **AMENDMENT-REQUIRED**, solely for the stale six-versus-seven sentence. A1 and A2 are
substantively closed. No T4, GPU work, stability solve, action/carrier/source/boundary/mass
adoption, physical branch selection, navigation edit, or canonization follows.
