# Fresh external G250 adversarial review — exact final response

Date: 2026-08-24

Reviewer: external Codex `gpt-5.4`, high reasoning, web disabled, sealed read-only intake.

## Findings

1. High: the sealed-intake self-verifier does not pass. The registered replay
   `python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/verify_package.py` returned
   `FAIL` with `failed=["source_manifest_nine_exact"]`. The intake builder copies manifest sources
   under `sources/`, while the verifier looks for them at the intake root. In the sealed copy, all
   nine manifest entries exist only under `sources/`, so the package's own provenance check is
   broken in the environment it tells the reviewer to use.

2. Medium: one registered command is not executable from the sealed intake. `COMMANDS.md` registers
   `python3 verify_current_scientific_premises.py`, but that file is not present in the intake.

3. Medium: the certification is nonvacuous for the homothety and dimensional-algebra core, but
   thinner than claimed for some provenance classifications. In production code, the G236/G237 and
   G99 checks are equality checks against hardcoded table entries. In the independent verifier,
   three key provenance claims are literal `True` constants. In the hostile ledger,
   `g99_native_promotion_rejected` is proved only by checking a nonempty set. That does not refute
   the scientific claim, but it means part of the certification is assertion-like rather than
   evidentiary.

## Primary landing

No scoped scientific refutation of the G250 claim was found. The one-anchor homothety theorem, the
"second anchor is a consistency condition not a second scale" point, the distinction between
dimensional eligibility and an owned metric-attachment law, the `c_E`/`G_obs` no-length result,
reciprocal-redshift weight-zero status, the relative-SNe zero-point deletion, and historical G99
`X_eff` conditionality are all supported by the scoped derivations and ledgers.

The strongest failure is not scientific but certification/provenance: the sealed-copy package
verifier fails, and one registered replay is absent. The scientific landing survives within scope,
but the package is not yet cleanly certifiable as a sealed external-review intake.

## Exact replay/check results

- `derive_absolute_scale_anchor_types.py --cases 4096`: `PASS`; 7/7 exact checks true; 4096
  recovery cases; 4096 two-anchor consistency cases.
- `verify_absolute_scale_anchor_types_independent.py --cases 12000`: `PASS`; 24,010 assertions; all
  rejection controls passed.
- `run_catch_proofs.py`: `PASS`; 20/20 hostile mutations caught.
- `verify_package.py`: `FAIL`; only `source_manifest_nine_exact=false`.
- `verify_current_scientific_premises.py`: unavailable in the sealed intake.
- Bounded hash check against `REVIEW_SCOPE.json`: 32/32 payloads present, zero hash mismatches.
- Manifest-location check: all nine sources had `root_exists=False` and `sources_exists=True`.

## Required repairs

- Repair the intake/verifier path contract so `verify_package.py` validates the sealed copy.
- Either include `verify_current_scientific_premises.py` in the sealed intake or remove it from the
  registered sealed-copy command list.
- Replace the hardcoded/tautological G236/G237, G99, and attachment-law certification checks with
  source-reading or manifest-backed checks.

## Scientific refutations

None found within the scoped sources and permitted replays.

## Maximum bounded scientific conclusion

At most: one matched nonzero-homothety-weight direct metric anchor can conditionally calibrate the
single G249 positive scale; additional independent anchors test consistency of the supplied
dimensionless history. `c_E`, `G_obs`, reciprocal redshift, and the current relative SNe state do
not by themselves fix absolute scale. Mass/density/energy composites remain dimensional candidates
only until a lawful metric-attachment bridge is supplied. Historical G99 `X_eff` remains a
conditional external cross-check, not a native G249 anchor. No anchor value, history, branch
population, or outcome is selected.
