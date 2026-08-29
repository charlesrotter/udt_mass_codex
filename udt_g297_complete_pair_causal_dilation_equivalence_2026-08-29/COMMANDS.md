# G297 registered commands

## Repository checkout

Run from this package directory. These commands write only the registered result envelopes in the
package; `verify_package.py` performs its production/independent replay inside its own temporary
directory.

```bash
python3 derive_causal_dilation_equivalence.py
python3 verify_causal_dilation_independent.py
python3 verify_package.py
python3 run_catch_proofs.py
```

The package verifier reruns production and independent checks in a writable ephemeral copy and
does not alter evidence files.

## Sealed read-only intake

Do not run result writers against the sealed files. Copy the **entire intake**, not only this
package, to a writable ephemeral directory so that the source-manifest paths remain available:

```bash
review_runtime=$(mktemp -d)
cp -R /intake/. "$review_runtime"/
chmod -R u+w "$review_runtime"
cd "$review_runtime/udt_g297_complete_pair_causal_dilation_equivalence_2026-08-29"
G297_SOURCE_ROOT="$review_runtime" python3 derive_causal_dilation_equivalence.py
G297_SOURCE_ROOT="$review_runtime" python3 verify_causal_dilation_independent.py
G297_SOURCE_ROOT="$review_runtime" python3 verify_package.py
G297_SOURCE_ROOT="$review_runtime" python3 run_catch_proofs.py
```

If only the package is copied, set `G297_SOURCE_ROOT` to the unchanged intake root containing the
15 source-manifest paths. `verify_package.py` and `run_catch_proofs.py` both honor that inherited
root. The sealed intake remains unchanged in either workflow.
