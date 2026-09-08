# CF1 fresh adversarial review

**Disposition: VERIFIED-WITH-CAVEATS.** The exact classification in
CANDIDATE_INITIAL.md survives independent reconstruction and direct adversarial
review. One additional finite-harness false pass was found, executed, preserved
and caught by focused reviewer fixtures. It does not refute the analytic proof.
No unresolved load-bearing mathematical objection remains at CF1 scope.

## Exact reviewed conclusion

On the supplied smooth S3, let `s=|z2|^2` and
`X=Z1+r(s)Z2`, where the Zj are the global rotations and r has a smooth
strictly positive extension around [0,1]. This is a chosen mathematical
sector, not a physical field law.

| Property in this sector | Exact criterion |
|---|---|
| Every integral curve is closed | r is a constant positive rational |
| Leaves are a regular smooth circle fibration | r is identically 1 |
| Hopf equivalence under an arbitrary smooth diffeomorphism | r is identically 1 |
| Smooth isotopy persistence for a jointly smooth family starting at r=1 | r(t,s) remains 1 throughout the interval |

All-time closure on a connected time interval starting at Hopf also forces
r=1. At isolated times a constant rational r=p/q other than 1 can close every
leaf while axis holonomy has orders q and p, respectively. One of these orders
can equal 1; both equal 1 only at Hopf. Axes are closed even when some interior
orbits are not. Reparametrization and orientation reversal do not remove the
holonomy obstruction. The proof covers non-equivariant diffeomorphisms because
they preserve leaf compactness and conjugate holonomy germs.

For an ACTUAL jointly smooth family in this sector, the candidate's condition
`partial_t partial_s r(0,s0)!=0` implies nonconstant spatial slope for every
sufficiently small nonzero time. The differentiability argument is valid.
CF1 supplies no lawful K, Ricci eigenline, symmetry reduction or vacuum
development realizing that condition. CF2 must separately supply that join;
its absence is an explicit scope boundary, not an objection to CF1.

## Sources, seals and independence

Initial HEAD/grok/cached origin-grok matched
`32d23fb47dc4e440acc8c721aef6cb8201796ded`. The parent 358-row audit receipt was
authenticated by exit/no-timeout fields, byte correspondence with its separate
stdout/stderr, and matching registry/verifier bytes at that commit. It was
reused, not rerun. No fresh network synchronization is claimed. Later shared
startup/registry edits were observed during permitted concurrent integration;
the reused receipt remains a snapshot receipt, not a check of those new bytes.
The changed AGENTS diff only replaced its registry count, 358 by 361.

The allowed definitions and original sources are pinned in
[SOURCE_FIRST_SEAL.md](SOURCE_FIRST_SEAL.md). The independent argument and
checker were written and checked before the seal. First author exposure was
the freeze read at `2026-09-08T20:35:53.807256+00:00`, after both seals existed.

| Pinned artifact | SHA-256 |
|---|---|
| SOURCE_FIRST_SEAL.md | e36ffe8e69b94d56676008be64bc3ce1aaf173c4dbb46245318857210b6c4a0a |
| Author CANDIDATE_FREEZE.md | 5276ee4859ca0ca0bf3758c122c498a1897f6a58bd397cb8aeddcbae29bf0b8e |
| Author CANDIDATE_INITIAL.md | 35263178061ec4ad2e65add33b43e8f66c008a6447a76bf2fb1263f8f42b92ea |
| Author check_cf1.py | 3272d699a432c86f4137505a99e44af18588e942fcf310d375acde35ee7367c9 |
| Author check_baseline.stdout | ac9d854ced7c7b0daf46e66f7a888083a9dc8e1958902062346907083a1c4d41 |

| Independence axis | Actual status |
|---|---|
| Context | Fresh review-only context as dispatched; no resume, fork or new agent |
| Model | Backend identity UNKNOWN; configured CLI label is not authentication; different-model review UNTESTED |
| Argument | Source-first reconstruction from declared definitions, sealed before author exposure |
| Implementation | New standard-library exact checker; author replays are separately labeled same-code regression |
| Shared methods | Elementary torus-flow/return-map argument, Python/Fraction, and required run_capture.py |
| Exposure | Definitions/target and allowed source controls before seal; author freeze/proof/code/results only afterward |

No campaign log, other review or advisory file was read. Details and chronology
are preserved in [EXPOSURE_AND_REVIEW_NOTES.md](EXPOSURE_AND_REVIEW_NOTES.md).

## Actual checks and defect finding

The sealed independent run passed 331 exact assertions, including 55 primitive
rational slopes, both axes, one-exceptional-axis cases, rational reduction,
Cartesian tangency/nonvanishing samples and four false-criterion catches.
The proof, not the fixtures, supplies the real/smooth universal quantifiers.

All author modes were executed again through the existing capture utility:

| Mode | Passed / total | Exit | Observed result |
|---|---:|---:|---|
| baseline | 29 / 29 | 0 | Matches frozen stdout byte-for-byte |
| integer_only | 24 / 29 | 1 | Four noninteger closure guards and sampling guard fail |
| all_rational_regular | 25 / 29 | 1 | Four regularity guards fail |
| wrong_period | 25 / 29 | 1 | Four interior-period guards fail |
| swap_axes | 25 / 29 | 1 | Four axis-order guards fail |

All four mutant outputs also matched the author's saved stdout bytes. Each
failure was the expected mathematical guard failure, with empty stderr and no
timeout, not an import/syntax/resource crash.

**Defective step: incomplete finite fixture coverage in check_cf1.py.** An
additional in-memory mutation replaced `axis_orders(r)==(1,1)` by
`1 in axis_orders(r)`. This incorrectly treats either trivial axis as enough
for regularity. The author's original five fixtures actually passed 29/29,
exit 0, with this wrong rule. The false pass is retained verbatim in
false_pass_either_axis.{stdout,stderr,json}.

Keeping the same wrong rule and adding reviewer fixtures r=2 and r=1/2 gave
exit 1 with exactly regular_2 and regular_1/2 failing (37/39 passed), retained
in catch_either_axis.{stdout,stderr,json}. These cases were also present in
the independent pre-exposure reconstruction/checks. The survivor is the whole
stated mathematical theorem and the four originally claimed catches, with
the finite harness's additional blind spot disclosed.

Smallest optional same-premise author repair: add the two one-exceptional-axis
fixtures and the either-axis mutation, while preserving the initial checker
and false-pass history. No author repair was made or claimed here; that
decision belongs to the author within the one-repair budget. The direct proof
already handles both axis orders, so CF1 mathematics does not require a repair
to remain VERIFIED-WITH-CAVEATS.

## Limits and return point

Both author and reviewer single rescaling identities are weak algebraic checks,
excluded as evidence for global leaf equivalence; that conclusion has a direct
line-distribution argument. The deliberately retained rational-sampling example
is also a warning about finite coverage, not universal closure evidence.
There is no numerical near-rationality, grid or empirical-fit inference here.

The candidate's ancillary Albach--Geiges section attribution was not verified:
both exact-v2 PDF/abstract web fetches returned cache-miss failures. No paper
contents were received or used. The direct proof is self-contained and does
not require that terminology source or a general Seifert classification.

No full premise-audit duplication, formal proof-assistant or human-specialist
review, different-model comparison, CF2 construction, metric evolution,
protected-payload/raw-grid/archive/observational checks, or scientific promotion
was performed. Parent synchronization/audit reuse follows the explicit dispatch.
All authored and generated review files stay under step_01/review; original
candidate/evidence and sealed source-first artifacts are unchanged.

Return point: reviewed conditional CF1 mathematical discriminator and preserved
harness caveat. No physical selection, stability, topology change, carrier/action
adoption, grade/canon change or lawful vacuum counterexample follows. No author
repair decision or downstream CF2 execution is taken by this review context.
