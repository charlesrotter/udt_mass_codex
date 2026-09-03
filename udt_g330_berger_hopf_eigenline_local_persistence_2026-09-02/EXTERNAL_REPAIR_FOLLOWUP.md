# G330 Repair-Only External Follow-Up Response

## Scope and compliance

I treated this as a zero-context, repair-only external review of the sealed intake at `/intake`.
I inspected only `/intake`, copied that intake to one writable workspace copy at
`/work/g330_followup.en4h98`, ran executable checks only from writable `/work` copies, wrote no
transient outputs outside `/work`, did not edit intake evidence files, and did not continue the
research.

## Authentication and replay

The registered intake verifier [verify_review_intake.py](/intake/package/verify_review_intake.py:1)
authenticated the sealed tree at `/intake` directly. The command

```bash
python3 -S /intake/package/verify_review_intake.py --root /intake
```

returned:

```text
G330 sealed intake authentication PASS: 45 payloads; 47 files
```

This authenticated the detached seal [REVIEW_MANIFEST.sha256](/intake/REVIEW_MANIFEST.sha256:1),
the manifest [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:1), the scope file
[REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:1), and every manifest-listed payload.

From the single writable copy at `/work/g330_followup.en4h98/package`, I ran the four registered
commands from [COMMANDS.md](/intake/package/COMMANDS.md:1):

```bash
python3 -S derive_berger_hopf.py --output DERIVATION_RESULT.json
python3 -S verify_berger_hopf_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json
```

All four passed:

- `derive_berger_hopf.py`: `G330 production PASS: 39 exact checks`
- `verify_berger_hopf_independent.py`: `G330 independent PASS: 40 exact checks`
- `run_catch_proofs.py`: `G330 hostile PASS: 8/8 caught`
- `verify_package.py`: `G330 package PASS: 169 aggregate gates`

The repaired aggregate verifier output retained the same landing token and the same
follow-up-pending maximum grade in the replayed outputs
([PACKAGE_VERIFICATION_RESULT.json](/work/g330_followup.en4h98/package/PACKAGE_VERIFICATION_RESULT.json:177),
[DERIVATION_RESULT.json](/work/g330_followup.en4h98/package/DERIVATION_RESULT.json:72)).

## R1

R1 passes.

The source verifier is now intake-local. In [verify_package.py](/intake/package/verify_package.py:16),
`ROOT` is the package directory, `REPO` is its parent, and
`SOURCE_ROOT = REPO / "sources" if (REPO / "sources").is_dir() else REPO`
([verify_package.py](/intake/package/verify_package.py:18)). The verifier then loads
[SOURCE_MANIFEST.tsv](/intake/package/SOURCE_MANIFEST.tsv:1), requires exactly `15` source rows
([verify_package.py](/intake/package/verify_package.py:162), [verify_package.py](/intake/package/verify_package.py:164)),
rejects absolute and traversal paths
([verify_package.py](/intake/package/verify_package.py:167), [verify_package.py](/intake/package/verify_package.py:168)),
and checks existence, byte count, and SHA-256 of each resolved intake-local source file
([verify_package.py](/intake/package/verify_package.py:170), [verify_package.py](/intake/package/verify_package.py:171),
[verify_package.py](/intake/package/verify_package.py:172), [verify_package.py](/intake/package/verify_package.py:174)).

The manifest itself contains exactly 15 safe relative source paths
([SOURCE_MANIFEST.tsv](/intake/package/SOURCE_MANIFEST.tsv:2) through
[SOURCE_MANIFEST.tsv](/intake/package/SOURCE_MANIFEST.tsv:16)).

I also ran two bounded negative checks under separate writable `/work` copies:

- Traversal mutation: I changed `S01` to `../REVIEW_SCOPE.json`. `verify_package.py` failed with
  `AssertionError: source_path_safe_S01`.
- Missing-source mutation: I removed the copied `sources/CURRENT_SCIENTIFIC_PREMISES.tsv`.
  `verify_package.py` failed with `AssertionError: source_exists_S01`.

Those failures confirm that the repaired sealed replay does not weaken the path-safety or
source-existence gates.

## R2

R2 passes.

The exact report states the intrinsic normalization in the required order. It introduces the metric
fibre length
([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:107),
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:110)),
then states
`eta=(2*pi/ell_fibre) alpha`
before recording the Berger-coordinate evaluation
`= alpha/c = +/- sigma_3`
([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:113),
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:116),
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:117)).
It then says explicitly that `c` is only the Berger-coordinate evaluation of the metric fibre
length and not an external ruler, physical scale, or added premise
([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:121),
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:122)).

The lay report preserves the same intrinsic priority in plain language: the normalization uses each
fibre's own metric-measured circumference and does not import a ruler or promote the Berger
parameter into a physical scale
([LAY_REPORT.md](/intake/package/LAY_REPORT.md:10),
[LAY_REPORT.md](/intake/package/LAY_REPORT.md:11),
[LAY_REPORT.md](/intake/package/LAY_REPORT.md:12)).

I found no introduced external ruler, absolute scale, target carrier, or frame-component
normalization.

## R3

R3 is not fully complete.

The exact report is correct and explicit. It conditions local persistence on the general imported
smooth marked Einstein-Cauchy existence/uniqueness theorem and spells out the isometry-extension
step; it also types G321 only as a scoped application/interface rather than as a proof
([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:164),
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:165),
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:166),
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:167)).
The premise ledger is also explicit on both the imported theorem and its standard isometry
extension, again typing G321 only as an interface/application
([PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:10)).

The problem is that the lay, status, and evidence records do not all carry that full explicitness.
They do preserve the imported-theorem dependence and the G321 scoping:

- [LAY_REPORT.md](/intake/package/LAY_REPORT.md:15) through
  [LAY_REPORT.md](/intake/package/LAY_REPORT.md:17)
- [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:8)
- [EVIDENCE_GATES.md](/intake/package/EVIDENCE_GATES.md:27) through
  [EVIDENCE_GATES.md](/intake/package/EVIDENCE_GATES.md:29)

But those three records do not explicitly state the standard isometry-extension consequence used by
the exact derivation. A direct text search found no `isometry` occurrence in `LAY_REPORT.md`,
`STATUS_LEDGER.tsv`, or `EVIDENCE_GATES.md`, while the required wording does appear in
`EXACT_DERIVATION.md` and `PREMISE_LEDGER.tsv`.

I therefore cannot certify R3 as fully implemented under the stated follow-up requirement that the
exact, lay, premise, status, and evidence records explicitly condition local persistence on the
imported theorem and its isometry-extension consequence.

That incompleteness does not refute the bounded result. On the contrary, the bounded-claim guards
remain intact:

- no canon upgrade
  ([PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:3),
  [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:16))
- no global conservation or long-time persistence claim
  ([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:180) through
  [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:182),
  [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:9))
- no arbitrary nonsymmetric stability claim
  ([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:182),
  [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:13),
  [LAY_REPORT.md](/intake/package/LAY_REPORT.md:22),
  [LAY_REPORT.md](/intake/package/LAY_REPORT.md:23))
- no occupancy or universe-selection claim
  ([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:193) through
  [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:195),
  [LAY_REPORT.md](/intake/package/LAY_REPORT.md:21) through
  [LAY_REPORT.md](/intake/package/LAY_REPORT.md:24),
  [PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:5))
- no matter, mass, source, scale, or calibration claim
  ([PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:13),
  [PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:17),
  [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:17),
  [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:122))

## Unchanged bounded scientific landing

The bounded landing itself is unchanged in the exact report
([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:209) through
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:215)).
The prior external review retained that same bounded scientific landing while requesting only the
three repairs
([EXTERNAL_REVIEW.md](/intake/package/EXTERNAL_REVIEW.md:16),
[EXTERNAL_REVIEW.md](/intake/package/EXTERNAL_REVIEW.md:238),
[EXTERNAL_REVIEW.md](/intake/package/EXTERNAL_REVIEW.md:240)).
The corrected replayed outputs preserve the same landing token and do not promote it beyond the
bounded conditional form
([PACKAGE_VERIFICATION_RESULT.json](/work/g330_followup.en4h98/package/PACKAGE_VERIFICATION_RESULT.json:177),
[DERIVATION_RESULT.json](/work/g330_followup.en4h98/package/DERIVATION_RESULT.json:72)).

## Conclusion

R1 passes. R2 passes. The bounded scientific landing remains retained and unchanged. R3 is still
short of the follow-up requirement because the lay, status, and evidence records preserve the
imported-theorem dependency but do not explicitly state the isometry-extension consequence that the
repair request asked to be carried across all named records.

REPAIR_INCOMPLETE__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED
