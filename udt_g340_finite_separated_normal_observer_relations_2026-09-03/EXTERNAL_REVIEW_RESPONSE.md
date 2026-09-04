# External Review Response

Fresh zero-context adversarial review completed against the sealed intake only. I copied `/intake` to `/work/g340_intake_copy`, then verified the copy against the sealed source: `37/37` file paths matched and `37/37` file digests matched exactly. I then authenticated [REVIEW_SCOPE.json](/work/g340_intake_copy/REVIEW_SCOPE.json:1), [REVIEW_MANIFEST.tsv](/work/g340_intake_copy/REVIEW_MANIFEST.tsv:1), and [REVIEW_MANIFEST.sha256](/work/g340_intake_copy/REVIEW_MANIFEST.sha256:1). The detached SHA-256 matched the manifest, the manifest hash for `REVIEW_SCOPE.json` matched, the manifest listed `35` payload entries, and the on-disk set was exactly those `35` payloads plus the manifest and detached seal for `37` total files, consistent with the scope count.

I also ran the registered dependency-free replay in `/work/g340_intake_copy/g340`: production `3868/3868`, independent `5988/5988`, hostile `15/15`, aggregate no-write `17/17`. The aggregate verifier checks source-hash matching, replay success under `UDT_NO_WRITE=1`, and no evidence-byte changes during replay; see [verify_package.py](/work/g340_intake_copy/g340/verify_package.py:36), [verify_package.py](/work/g340_intake_copy/g340/verify_package.py:62), and [verify_package.py](/work/g340_intake_copy/g340/verify_package.py:135).

**Findings**
Critical: none.

High: none.

Medium: none.

Low: none.

**Assessment**
1. Yes. The metric directly yields the conserved spatial covectors, null Hamiltonian, future-branch frequency, and general supplied-branch quadrature in [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:76). The principal arrival maps and powers/signs in [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:118) follow by direct integration of `dX/dT` and `dy/dT` from that Hamiltonian. My independent scratch integration outside the package code reproduced the longitudinal `4/3 -> 3/4` and transverse `1/3 -> 3` laws numerically.

2. Yes. G340 uses G298's exact definitions `r=omega_e/omega_r=d tau_r/d tau_e` and `delta=-log r` from [G298 EXACT_DERIVATION.md](/work/g340_intake_copy/sources/udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/EXACT_DERIVATION.md:33). On the principal transported-planar stratum `W=0`, the projective readout reduces to `chi=tanh(delta)` and `M=sech(delta)` exactly as stated in [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:145). The package also explicitly preserves the sign/type distinction: positive route length `q` is not identified with the sign of `delta` or `chi`; see [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:178).

3. Yes. The unequal-route and equal-route radar equations in [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:183) agree with the G297 causal-diamond first-germ formula `R=2/(a_-' + a_+')` in [G297 EXACT_DERIVATION.md](/work/g340_intake_copy/sources/udt_g297_complete_pair_causal_dilation_equivalence_2026-08-29/EXACT_DERIVATION.md:25). The conformal-power midpoint for equal routes is correct, and the text correctly states that the arithmetic midpoint is a chosen convention rather than co-presence or a universal distance owner; see [G297 EXACT_DERIVATION.md](/work/g340_intake_copy/sources/udt_g297_complete_pair_causal_dilation_equivalence_2026-08-29/EXACT_DERIVATION.md:89) and [STATUS_LEDGER.tsv](/work/g340_intake_copy/g340/STATUS_LEDGER.tsv:10). The `c_E` typing remains a unit conversion only, not a history or scale selector; see [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:203).

4. Yes. Compact winding remains branch-labelled. G340 keeps each lift `q_n=|Delta x+nL|` as a distinct lawful arrival branch, orders earliest arrival by smallest `q_n`, and records the half-period two-branch tie; see [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:260) and [AUDIT_REPORT.md](/work/g340_intake_copy/g340/AUDIT_REPORT.md:35). Nothing in the package collapses later windings into the earliest branch.

5. Yes, with the correct bound. The package limits "no light model required" to metric-null timing and endpoint frequency geometry, not to emission, flux, spectrum, absorption, or detection. That boundary is explicit in [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:280) and [LAY_REPORT.md](/work/g340_intake_copy/g340/LAY_REPORT.md:24). I do not see an overclaim to Maxwell dynamics or detector physics.

6. Yes, within the stated bounded epistemic scope. The production and independent routes are implementation-distinct, and the package explicitly does not overclaim premise independence; see [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:290). The aggregate gate authenticates preregistration linkage, source hashes, replay success, and no-write preservation without requiring repository access in the sealed-copy layout; see [verify_package.py](/work/g340_intake_copy/g340/verify_package.py:79), [verify_package.py](/work/g340_intake_copy/g340/verify_package.py:127), and [verify_package.py](/work/g340_intake_copy/g340/verify_package.py:135). The hostile gate is a mutation/catch gate rather than an independent mathematical derivation, but it is presented that way and does not create circularity in the main mathematical verification.

7. No silent physical selection was found. The package repeatedly keeps physical distance protocol, observer/route population, scale, `X_max`, and canon open; see [STATUS_LEDGER.tsv](/work/g340_intake_copy/g340/STATUS_LEDGER.tsv:13), [EXACT_DERIVATION.md](/work/g340_intake_copy/g340/EXACT_DERIVATION.md:295), and [LAY_REPORT.md](/work/g340_intake_copy/g340/LAY_REPORT.md:28). It also preserves the distinction between implementation independence and premise independence, and between metric-null geometry and a light-transfer model.

**Residual Boundedness**
Acceptance is bounded, not global. The package does not classify generic nonprincipal endpoint inversion, generic caustics, nonprincipal screen transfer, accelerated/nonnormal observers, or any physical protocol/population/scale completion. Those exclusions are explicit and consistent with the accepted scope; see [COMPLETENESS_MAP.md](/work/g340_intake_copy/g340/COMPLETENESS_MAP.md:3) and [STATUS_LEDGER.tsv](/work/g340_intake_copy/g340/STATUS_LEDGER.tsv:6).

On the stated scope, I find no algebraic defect, sign defect, branch-label collapse, protocol conflation, light-model overreach, or gate-circularity defect that blocks the bounded claim.

ACCEPT_G340_BOUNDED_FINITE_PAIR_RELATION_CLASSIFICATION
