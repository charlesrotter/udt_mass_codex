**Primary Landing**
`VERIFIED_WITH_CORRECTIONS`

**Exact Corrections**
- The load-bearing mathematics is intact, but the sealed-intake preregistration/source replay is mechanically broken. In [SOURCE_MANIFEST.tsv](/tmp/udt_timelive_orchestra_review_x5rxTT/udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/SOURCE_MANIFEST.tsv:2) through line 14, every frozen source path is recorded without the required `sources/` prefix, while [verify_preregistration.py](/tmp/udt_timelive_orchestra_review_x5rxTT/udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/verify_preregistration.py:12) resolves each row as `ROOT / row["path"]`. In this sealed intake the files actually live at `ROOT / "sources" / row["path"]`. The shipped replay therefore fails immediately on `CURRENT_SCIENTIFIC_PREMISES.tsv`.
- This is a packaging correction, not an algebra correction. All 13 manifest hashes match once `sources/` is prefixed.

**Maximum Justified Conclusion**
The scientific result in [EXACT_DERIVATION.md](/tmp/udt_timelive_orchestra_review_x5rxTT/udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/EXACT_DERIVATION.md:1) is verified within its declared local regular split-relative scope. I independently replayed the shipped checks: production exact algebra `15/15` passed, independent rational reconstruction `1200/1200` passed, and catch proofs `20/20` passed. The chart count and Schur-complement converse are correctly scoped to a supplied regular reciprocal/angular split with positive screen block and Lorentzian base Schur complement; the right Maurer-Cartan sign and the mixed block
`partial_t C_i-partial_i C_t-(C_tP_i-C_iP_t+R_tC_i-R_iC_t)=0`
are correct; `H_R`, `H_A`, and pair-state derivative formulas are correct with query terms retained.

The strongest justified scientific landing remains:

`EXACT_COMPATIBILITY_ORCHESTRA_BUT_NO_EVOLUTION_LAW`

More sharply: the block identities are smooth-coframe compatibility identities, not a native time-live selector; time-only histories remain unrestricted; Cartan/Bianchi/Levi-Civita structure does not by itself add an evolution law; and none of the sealed upstream sources upgrades R17, calibration transport, causality, reciprocity, or `c_E` into an owned principal differential operator selecting a physical history.

**Smallest Next Mathematical Joint**
An owned principal differential relation on the full regular pair-adapted movie `(B,Q,S)`, or an equivalent global completion rule, that cuts the smooth full-rank history space down to a proper subset. Without that joint, characteristics, dispersion, frequencies, trajectories, and regime labels remain unselected.

**Runnable Algebra For Load-Bearing Corrections**
No load-bearing algebra correction is justified.

Runnable sealed-intake correction replay for the actual defect:
```bash
python3 - <<'PY'
import csv, hashlib
from pathlib import Path

root = Path("/tmp/udt_timelive_orchestra_review_x5rxTT")
here = root / "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10"
rows = list(csv.DictReader((here / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))

for row in rows:
    path = root / "sources" / row["path"]
    assert path.is_file(), row["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]

print(f"PASS corrected source replay rows={len(rows)}")
PY
```
