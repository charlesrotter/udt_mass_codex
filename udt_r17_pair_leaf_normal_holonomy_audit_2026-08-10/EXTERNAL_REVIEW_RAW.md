**Verdict**

`VERIFIED_AS_STATED`.

Package hashes check out: `sha256sum -c PACKAGE_MANIFEST.sha256` passes for all 34 listed members, and the intake contains 35 local files because the manifest is not self-listed [PACKAGE_MANIFEST.sha256](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/PACKAGE_MANIFEST.sha256:1). The only consistent reading of the “47 files” instruction inside the seal is 35 local artifacts plus 12 manifest-pinned source snapshot rows [SOURCE_MANIFEST.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/SOURCE_MANIFEST.tsv:1).

The core bounded claim survives adversarial review: the supplied metric does derive the stated projected rank-two normal connection, curvature, and representative-free closed-loop holonomy classification, conditional on the already-fixed pair foliation and inherited `R x S1` leaf topology [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:54), [STATUS_LEDGER.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/STATUS_LEDGER.tsv:2).

**Load-Bearing Reconstructions**

- Frame/bracket reconstruction is correct. From `e0=uT`, `e1=u^-1(Z-aT)`, `e2=v^-1X`, `e3=v^-1Y` and `[X,Y]=2εZ`, `[Z,X]=2εY`, `[Y,Z]=2εX`, one gets
  `[e0,e1]=-(p1/u)e0`,
  `[e1,e2]=(p2/v)e1-(λp1/u)e2+(2ε/u)e3`,
  `[e1,e3]=(p3/v)e1-(2ε/u)e2-(λp1/u)e3`,
  `[e2,e3]=(2εa/(uv^2))e0+(2εu/v^2)e1+(λp3/v)e2-(λp2/v)e3` [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:58), [derive_normal_holonomy.py](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/derive_normal_holonomy.py:46).
- Koszul gives the normal connection coefficients exactly:
  `A(e0)=g(∇e0 e2,e3)=εa/(uv^2)`,
  `A(e1)=g(∇e1 e2,e3)=ε(2/u-u/v^2)` [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:75), [derive_normal_holonomy.py](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/derive_normal_holonomy.py:76).
- Curvature recomputation is correct and does not need assumed second-derivative cancellation:
  `F(e0,e1)=e0A(e1)-e1A(e0)-A([e0,e1])`.
  Here `e0A(e1)=0` by stationarity, `e1A(e0)=-(1+2λ)εap1/(u^2v^2)`, and `A([e0,e1])=-(p1/u)A(e0)=-εap1/(u^2v^2)`, so
  `F_perp(e0,e1)=2εa(1+λ)p1/(u^2v^2)` [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:102), [verify_normal_holonomy_independent.py](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/verify_normal_holonomy_independent.py:170).
- The two special roles are genuinely distinct. `λ=-1` forces `F_perp=0` for arbitrary stationary `φ`; `λ=0` forces `L_Z q_H=2λZ(φ)q_H=0`, so `q_H` is Hopf-basic for arbitrary stationary `φ` [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:169), [LAMBDA_STRATUM_ATLAS.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/LAMBDA_STRATUM_ATLAS.tsv:2). Neither fact selects a physical branch [STATUS_LEDGER.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/STATUS_LEDGER.tsv:9).
- The holonomy-type distinction is correctly drawn. A local signed connection one-form is gauge-dependent; the oriented `SO(2)` loop angle is defined mod `2π`; under reflection it changes sign; the `O(2)` representative-free datum is `trace(Hol)=2cos(Θ)`; this is not ambient Lorentz holonomy [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:158), [HOLONOMY_CLASSIFICATION.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/HOLONOMY_CLASSIFICATION.tsv:6).
- Cylinder topology is handled correctly at the level claimed: flat `λ=-1` kills contractible-loop curvature flux but can retain nontrivial wound-loop `π1` character, so flat does not imply globally trivial holonomy on `R x S1` [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:131), [HOLONOMY_CLASSIFICATION.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/HOLONOMY_CLASSIFICATION.tsv:3).
- `H=span(e2,e3)` supplies horizontal lift only after a base path and starting point are given; it does not canonically choose a cross-leaf path [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:194), [HOLONOMY_CLASSIFICATION.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/HOLONOMY_CLASSIFICATION.tsv:8).

**Objections**

- Provenance objection, not a formula objection: the recorded verification runs were executed from `/home/udt-admin/udt_mass_codex/...`, not from the sealed intake copy [COMMAND_TRANSCRIPT.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/COMMAND_TRANSCRIPT.tsv:4). That weakens strict run-location provenance, but not the mathematical result, because the sealed copy contains the full derivation logic and an independent constructive checker [derive_normal_holonomy.py](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/derive_normal_holonomy.py:16), [verify_normal_holonomy_independent.py](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/verify_normal_holonomy_independent.py:143).
- Scope objection, not a failure: the 12 upstream source snapshots are represented only by manifest rows and roles inside the seal, not by their file contents [SOURCE_SCOPE.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/SOURCE_SCOPE.tsv:2), [SOURCE_MANIFEST.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/SOURCE_MANIFEST.tsv:2). So the review verifies the normal-holonomy package conditional on the fixed foliation/topology premise; it does not re-prove that premise from scratch inside this intake.
- No load-bearing sign, basis-change, gauge, degeneracy, topology, or ownership error was found inside the bounded claim. The package’s own mutation catches target exactly those failure modes and reject all 16 mutants [CATCH_PROOFS.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/CATCH_PROOFS.tsv:2).

**Required Landing**

`CONDITIONAL_METRIC_OWNED_NORMAL_CONNECTION_AND_REPRESENTATIVE_FREE_HOLONOMY_DATA_ON_SUPPLIED_R17_PAIR_LEAVES__PHYSICAL_PATH_AND_COMPLETE_ARROW_OPEN` [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:203).

The `λ=-1` flat-connection fact and the `λ=0` Hopf-basic-normal-metric fact are genuinely distinct, and neither selects a physical branch, leaf, path, winding, or observer arrow [EXACT_DERIVATION.md](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/EXACT_DERIVATION.md:186), [PREMISE_LEDGER.tsv](/tmp/udt-r17-normal-review.DG0LY5/udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/PREMISE_LEDGER.tsv:10).
