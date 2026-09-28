# Data lane commands and runtime history

Working directory for commands below: `/home/udt-admin/udt_mass_codex`.
All files owned by this lane lie in the campaign's `data/` and `DATA_RESULT.md`.
The initial source/metadata reads and git checks are in the agent transcript;
parent startup is attributed to LAUNCH.json, not independently reenacted.

## Persisted principal commands

```bash
timeout 600s python3 udt_observation_guided_function_search_2026-09-28/data/download_release.py > udt_observation_guided_function_search_2026-09-28/data/download.stdout.log 2> udt_observation_guided_function_search_2026-09-28/data/download.stderr.log
timeout 600s env OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 MPLCONFIGDIR=/tmp/udt_function_data_mpl python3 udt_observation_guided_function_search_2026-09-28/data/fit_empirical.py > udt_observation_guided_function_search_2026-09-28/data/fit.stdout.log 2> udt_observation_guided_function_search_2026-09-28/data/fit.stderr.log
timeout 600s env OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 python3 udt_observation_guided_function_search_2026-09-28/data/independent_anchor.py > udt_observation_guided_function_search_2026-09-28/data/anchor.stdout.log 2> udt_observation_guided_function_search_2026-09-28/data/anchor.stderr.log
timeout 600s env OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/udt_function_data_mpl python3 udt_observation_guided_function_search_2026-09-28/data/summarize_checks.py > udt_observation_guided_function_search_2026-09-28/data/summary.stdout.log 2> udt_observation_guided_function_search_2026-09-28/data/summary.stderr.log
timeout 600s env OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/udt_function_data_mpl python3 udt_observation_guided_function_search_2026-09-28/data/repair_alias_validation.py > udt_observation_guided_function_search_2026-09-28/data/alias.stdout.log 2> udt_observation_guided_function_search_2026-09-28/data/alias.stderr.log
```

All principal commands returned exit 0 with empty stderr. Scripts refuse to
overwrite their saved result directories/seals. To reproduce, copy the source
scripts and raw products to a fresh task-specific directory; do not delete
evidence to rerun in place. Raw covariance is stored as deterministic gzip;
SOURCE_MANIFEST records both compressed and original-byte SHA-256.

Preflight Python packages: Python3.10.12, NumPy2.2.6, SciPy1.15.3,
Matplotlib3.10.8;24 visible/affinity CPUs. A matplotlib import before setting
MPLCONFIGDIR warned that `/home/udt-admin/.config/matplotlib` is not writable and
created a temporary cache. Computation set MPLCONFIGDIR explicitly; no scientific
run failed. Process namespace/host utilization limits remain parent LAUNCH caveats.

## Source metadata and diagnostic read history

Before download, `urllib.request.urlopen` of
`https://api.github.com/repos/PantheonPlusSH0ES/DataRelease/commits/main` failed
in the sandbox with `URLError: [Errno -3] Temporary failure in name resolution`.
The identical read under the authorized public-network escalation returned
commit `c447f0fea703fcd0fff57de5000947b5ca81286b`; the recursive tree was used only
to locate the magnitude/covariance files and public likelihood. Schema README
and likelihood were read before rows. `4_DISTANCES_AND_COVAR/README.md` returned
HTTP404; the actual source is `README`. Download command then saved the same
metadata alongside observational products. These source-access failures did
not alter the model or data selection.

After the fit, the schema mismatch was diagnosed by direct source reparse;
the independently saved anchor reproduces the numerical discrepancy. A public
repository search found existing issues6/10/13. The following exact Python loop
retrieved and saved issue bodies/comments under the public-network escalation:

```python
import urllib.request,json,hashlib
from pathlib import Path
p=Path('udt_observation_guided_function_search_2026-09-28/data/raw')
for n in [6,10,13]:
 for suffix in ['', '/comments']:
  u=f'https://api.github.com/repos/PantheonPlusSH0ES/DataRelease/issues/{n}{suffix}'
  raw=urllib.request.urlopen(u,timeout=30).read();out=p/f'issue_{n}{"_comments" if suffix else ""}.json'
  if out.exists():raise RuntimeError('refuse overwrite')
  out.write_bytes(raw)
  d=json.loads(raw)
  for item in (d if isinstance(d,list) else [d]):print(n,suffix,item['user']['login'],item.get('body',''))
```

The source JSON bytes and hashes, rather than a regenerated transcript, are
preserved. Issue comments are provenance/diagnostic history, not scientific
authority beyond what the source owner actually establishes. No speculative
comment was used to change covariance or repair physics.

No candidate fit was discarded. The substantive construction limitation was
the initial exact-CID grouping, repaired with a separately sealed possible-alias
grouping check. Initial scores remain in results/ and repaired scores in
alias_validation/. Primary estimates are identical because no full-data model
or sample was changed. All outcomes remain DRAFT for the later fresh reviewer.

Construction snapshot sealing command:

```bash
python3 udt_observation_guided_function_search_2026-09-28/data/seal_artifacts.py
```

ARTIFACT_MANIFEST.json includes retained stdout/stderr logs, including empty
stderr files. Repository ignore rules hide `.log` files from ordinary staging;
the parent must explicitly include these authorized evidence logs when banking
the package. The manifest excludes itself and interpreter caches. It is a
construction snapshot, not a scientific acceptance or cryptographic timestamp.
The first patch adding this sealing script failed on a documentation context
mismatch before any file changed; the corrected patch succeeded. No scientific
run was affected.
