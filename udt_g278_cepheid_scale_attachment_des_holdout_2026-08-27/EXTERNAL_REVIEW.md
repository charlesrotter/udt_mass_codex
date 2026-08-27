**Verdict**

`ACCEPT-WITH-REPAIRS`

The bounded scientific landing does **not** change. After rebuilding only the minimum writable replay layout under `/work/replay` from sealed evidence, I reproduced the sealed primary result, the implementation-distinct verification, the hostile controls, and the follow-up diagnostic. The strongest bounded landing still supported is `SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE`; the follow-up still says `PHYSICAL_CURVE_RESOLUTION_SENSITIVITY_PERSISTS` and `cannot_regrade_original=true`.

**Integrity And Recomputed Numbers**

- `REVIEW_SCOPE.json` matched exactly: sha256 `a66da444c9be988cb7560470cc719a81826c36ed4b97bc6369cc42a08c732555`, `597` bytes.
- `REVIEW_MANIFEST.tsv` has `47` rows; all `47/47` listed entries matched fresh size and sha256.
- Physical file count is `48`; symlink count is `0`.
- The one unmanifested physical file is `/intake/REVIEW_MANIFEST.tsv`, `7065` bytes, sha256 `03772e058a2009bd0a94786e199032df130b8e79626f4c524915027402ea7e29`.
- Primary `K=12` recomputation: `M=-19.24888454008354`, `a=12.28378312894975 mag`, `sigma_a=0.03900777435632015 mag`, `ell=286.25733633510214 Mpc`, `sigma_ell=5.142253493374308 Mpc`, `B=18.038122851079788`, `chi2_cal=57.134728577478334`, `dof=76`, ceiling `137.64414002968977`.
- Control scales: `K=8 -> a=12.38023489659988`, `K=16 -> a=12.253963675931999`, `K=24 -> a=12.228184697720636`.
- Exact resolution vector: `d=(0.0964517676501302, -0.02981945301775113, -0.05559843122911445)`, covariance rank `3`, `chi2=60.40538886961107`, ceiling `15.24744871391589`; this is a real failure, not a rank artifact.
- Max subset excursion remained below threshold: `leave_out_2007af`, `3.1114981409837474 sigma`.
- Serialization sensitivity stayed tiny: max `3.565870798638571e-08 mag`.
- DES no-retuning score reproduced exactly: `chi2=1434.579290816418`, `dof=1623`, ceiling `1907.8683906648823`, adequate `true` at `K=12`; all four frozen `K` values also pass.
- I found no hidden DES offset fit, preferred-resolution selection, scale averaging, kernel retuning, `P1`, angular fit, `X_max`, or LCDM distance insertion; the replay preserved a nonzero DES residual mean `0.1759203914730402`, so no offset was silently forced away.
- The two-stage reduction retained shared-data coupling: `max |Cov(c,B)| = 2.456957847364722e-04`, `||Cov(c,B)||_2 = 6.537339110752545e-04`, `Var(B)=6.199765146356744e-04`.
- Pantheon uncertainty was propagated into DES: `max |corr(a,theta)| = 0.55251970991062`; added prediction-covariance diagonal range was `0.0010282989810687763` to `0.0362319479158108`.

**Defects**

- `High`: the sealed intake is not self-replayable as packaged. The builder copies frozen sources under `sources/...`, but the replay scripts resolve Pantheon, G236, and G277 inputs at the intake root. `SOURCE_MANIFEST.tsv` is also root-relative. An intake-shaped bounded replay failed immediately in `verify_sources()` for exactly those files.
- `Medium`: the integrity manifest is incomplete. `REVIEW_MANIFEST.tsv` lists `47` payload files but omits the manifest file itself. That omission is deterministic because the builder enumerates files before writing the manifest. This weakens full chain-of-custody coverage for the sealed tree.
- `Medium`: the advertised replay surface is incomplete. `COMMANDS.md` registers `python3 verify_current_scientific_premises.py`, but that file is absent from the intake, and `verify_package.py` does not require it in its completeness check.

**Repair Scope**

1. Reseal the package only: make the copied source layout consistent with the replay scripts, or make the scripts and `SOURCE_MANIFEST.tsv` consistently read from `sources/`. No scientific recomputation or model change is needed.
2. Repair integrity coverage for `REVIEW_MANIFEST.tsv` with a detached checksum or outer manifest; direct self-hashing inside the same TSV is not workable.
3. Make the registered command surface consistent: either include `verify_current_scientific_premises.py` in the sealed intake and verify it, or remove that command from `COMMANDS.md`.

With those repairs, I would upgrade this from package-defective to scientifically verified-with-caveats.

Raw external response SHA-256:
`33f115f9820fa8f536da4216d0fd04268cdb12c8439dbbfbca48eb015ac14178`
