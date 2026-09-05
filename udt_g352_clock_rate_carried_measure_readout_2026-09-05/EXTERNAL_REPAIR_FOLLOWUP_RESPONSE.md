# External G352 R2 repair-only follow-up review

Date: 2026-09-05  
Review boundary: sealed-intake-only, repair-only, no network research, no repository or protected-package access

## Executive finding

The preregistered R2 repairs are complete within the bounded question authorized by the intake. The repaired result now distinguishes a continuous total-phase-variation intensity from a literal atomic crossing count, uses a nonnegative product measure on an explicitly supplied phase-label product measurable space, exposes the factorization and regularity conditions as chosen or supplied rather than derived, and preserves the conditional regular-cut result

```text
T_clock = R A^-1
```

The weights `(p,q)=(1,-1)` are unique only for this chosen continuous clock-rate density within G350's declared full independent positive character domain. The result does not select a universal `p`; the `p=0` observer-neutral density, literal atomic crossings, and other readout types remain distinct or open.

Verdict: accept the G352 R2 repair completion only. This verdict does not canonize the owner premise, establish a physical realization, or continue the research.

## 1. Intake authentication and handling

I authenticated the mounted `/intake` before substantive execution.

- `REVIEW_MANIFEST.sha256` contains the SHA-256 digest `fca43c879c68563619ddf2690559da6f3f7b1b7f33b02f4d52627f7cf2f87224` for `REVIEW_MANIFEST.tsv`; a fresh digest of the manifest matched exactly.
- `REVIEW_SCOPE.json` is 4,493 bytes with digest `868bc1961161e500e2dfb8ca07953ed0b9220cb24f8b9de1057e440483921d70`, matching its manifest row.
- `REVIEW_MANIFEST.tsv` is 6,234 bytes. `REVIEW_MANIFEST.sha256` is 86 bytes and has digest `7861065326057dd98123a773664ad5aa9c996db64466511b419a749f16c9253e`.
- The scope declares 42 payloads. Its 42 listed paths agree exactly with the 42 manifest paths.
- Every payload matched both its declared byte length and SHA-256 digest.
- The mounted tree contains exactly 44 regular files: 42 payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`. It has six nonempty directories and no symlinks or other special filesystem entries.

I copied the complete intake to `/work/g352_r2_repair_followup_intake_copy` before running the registered checks. The copy initially reproduced all 44 files and all manifest hashes. After execution, all 42 payloads still matched their original lengths and hashes, the manifest seal still matched, the file set was still exactly 44 files, and no bytecode or other file had been added.

This establishes internal byte consistency relative to the co-sealed manifest. It does not establish external authorship, a trusted timestamp, or an independently signed chain of custody: the manifest, checksum, scope, and payloads are unsigned and supplied together. The intake's `GIT_PREREGISTRATION_PROOF.txt` correctly grades its chronology as documentary rather than a trusted attestation.

## 2. Registered replay

I ran exactly the four commands registered in `COMMANDS.md`, from the copied G352 package, with `UDT_NO_WRITE=1`, `PYTHONDONTWRITEBYTECODE=1`, and the system interpreter under `python3 -B -S`.

| Registered check | Replayed result | Exit status |
|---|---:|---:|
| `derive_clock_rate_readout.py` | 103,648/103,648 assertions; 2,400 distinct base states | 0 |
| `verify_clock_rate_readout_independent.py` | 73,889/73,889 assertions; 2,700 distinct base states | 0 |
| `run_catch_proofs.py` | 18/18 registered semantic mutations caught | 0 |
| `verify_package.py` | 48/48 aggregate gates | 0 |

The replayed JSON objects exactly matched `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, `CATCH_PROOF_RESULT.json`, and `VERIFICATION_RESULT.json`, as checked by the aggregate verifier. The registered sources use the Python standard library. Their only subprocess operation is the aggregate verifier's local invocation of the three registered child scripts with the same no-write controls; no network import or call is present.

The reported repository suite and 334-row current-premise audit were not rerun. They are not among the four registered follow-up commands and repository access was prohibited. Their appearance in the intake is therefore documentary reporting, not evidence newly authenticated by this replay.

## 3. Continuous intensity and literal atomic crossings

Repair confirmed.

Section 1 of `EXACT_DERIVATION.md` defines

```text
dN_cont = |dTheta|/DeltaTheta,
rho_i = |dTheta/dtau_i|/DeltaTheta = omega_i/DeltaTheta.
```

It explicitly says this is not the ordinary instantaneous derivative of a literal discrete step-count. This is the continuous total-phase-variation realization preregistered in R2.1.

The literal fixed-level branch is retained separately as the atomic phase counting measure `sum_n delta_(Theta_n)`. The repaired derivation states that it has no everywhere-smooth instantaneous rate without an additional averaging, random-offset, interpolation, or coarse-graining premise. It is neither averaged into the continuous branch nor silently discarded. `COMPLETENESS_MAP.md`, `R2_REPAIRED_PREMISE_LEDGER.tsv`, `AUDIT_REPORT.md`, and `LAY_REPORT.md` preserve the same distinction.

The production and independent regression scripts each include a direct witness that an interval can have positive continuous phase variation while containing zero atomic crossings. These finite witnesses guard the distinction; the analytic text, not the assertion count, supplies the mathematical conclusion.

The frozen original `PREREGISTRATION.md` retains its outcome-unseen sign and discrete-rate wording, and the frozen R1 record retains its historical phase-reversal wording. These are clearly identified as historical preregistration artifacts. R2 expressly supersedes those formulations for the repaired result, while preserving their bytes for evidence integrity. The operative exact derivation does not repeat either defect.

## 4. Nonnegative product measure and explicit factorization

Repair confirmed.

The repaired measure is

```text
dXi = (|dTheta|/DeltaTheta) tensor dmu.
```

It is stated as a nonnegative product measure on the explicitly supplied product measurable space of phase and transverse labels. The repaired premise ledger identifies the product sigma-algebra as supplied query data. This removes the signed `dTheta` defect under the retained future-phase convention.

The following are all expressly exposed as supplied conditions or as a `CHOSE_BOUNDED_MATHEMATICAL_REALIZATION`:

- one common fixed positive `DeltaTheta`;
- the same G351 label measure on every phase slice;
- phase-independent support and weight;
- absence of phase-label correlation;
- label preservation across compared cuts;
- measurable cut maps and observer-frequency weights;
- tensor factorization on the product measurable space.

The repaired text expressly denies that this factorization follows from G351, the metric, reciprocity, or the owner premise, and it does not promote it to a new owner-adopted or canonical physical law. A phase-dependent measure family is left open. This satisfies R2.2 and R2.3.

## 5. Orientation, locality, density, and integrability boundaries

Repair confirmed across each registered boundary.

- Future-phase sign: with signature `(-,+,+,+)`, `k_a=nabla_a Theta`, future-raised nonzero null `k`, and future unit timelike `u_i`, the repaired derivation uses `omega_i=-u_i^a k_a>0` and `dTheta/dtau_i=-omega_i`. Positivity comes from total variation, not from reversing the sign convention.
- Nonzero gradient: the retained family explicitly requires a nonzero future-raised phase covector.
- Local observer: an endpoint tangent fixes only the local phase intensity for a worldline extension with that tangent. It supplies neither a global worldline nor interception of every phase level.
- Regular density: the ordinary formula is confined to the absolutely continuous component `dmu_ac=s dlambda` on cuts with finite positive Jacobian `J_i`. A ratio of densities is asserted only on common nonzero regular support.
- Zero density: equation (6) is homogeneous in `s`, and section 7 states that zero measure gives zero `Xi` and zero `nu_i`. Thus the division-free transfer preserves zero, while zero is not used to witness an exponent.
- Singular content: singular measure content is retained measure-wise and is not assigned an ordinary regular density exponent. At rank loss, an ordinary area density may diverge or fail to exist.
- Frequency integrability: the pushforward `nu_i(B)=integral_(X_i^-1(B)) (omega_i/DeltaTheta) dmu` is claimed finite only when the nonnegative measurable frequency weight is integrable against the supplied finite measure on the retained patch.

The many-to-one pushforward remains mathematical preimage accounting. It is not promoted to any physical aggregation rule.

## 6. Conditional algebra and uniqueness domain

Repair confirmed; the scientific landing is unchanged.

On the chosen continuous realization and common nonzero absolutely continuous regular support,

```text
Gamma_i = (omega_i/DeltaTheta) (s/J_i),
Gamma_j/Gamma_i = (omega_j/omega_i)(J_i/J_j) = R_ji A_ji^-1.
```

Therefore this readout has `T_clock=R A^-1`. To test uniqueness inside G350's declared full independent positive character domain, the repaired derivation compares `R^a A^q` with `R A^-1`. Setting `A=1` while varying positive `R` forces `a=1`; setting `R=1` while varying positive `A` forces `q=-1`. This is an analytic functional-equation argument on G350's chosen abstract domain, not a conclusion from a finite coefficient grid or a claim that one geometry realizes every positive pair.

The uniqueness is limited to this repaired readout within that character class. G351's observer-neutral regular density remains the separate `p=0` readout. Literal atomic crossings do not acquire the smooth exponent by implication, and other observer-weighted, nonlocal, phase-dependent, or otherwise typed readouts remain open. No universalization of `p=1` occurs.

## 7. Generated-state and assertion-count integrity

Repair confirmed.

The production loop uses `base=case+1` for 2,400 cases. Its first frequency coordinate `(11*base+1)/5` is injective in `base`, so the generated base states are genuinely distinct; no modular repetition remains. Its 103,648 total is consistent with the per-state identity, phase, transfer, observer, reversal, sewing, and zero checks plus the explicitly separate atomic/product, coefficient, rank-loss, and pushforward witnesses.

The independent loop likewise uses `base=case+1` for 2,700 cases. Its first additive frequency coordinate `11*base/7` is injective, so those base states are genuinely distinct. It uses a separate additive log-coordinate construction, imports no production module, and reads no production result. Its 73,889 total is consistent with its per-state and separate coefficient, atomic/product, and rank-loss checks.

The scripts, `RUN_RECORD.md`, `AUDIT_REPORT.md`, and `EVIDENCE_GATES.md` explicitly grade these numbers as regression assertions over generated states, not independent proofs, analytic completeness, or physical confirmation. Functional uniqueness, the measure statements, and the continuous-versus-atomic distinction remain analytic. The hostile checks are likewise accurately labelled semantic regression evidence.

## 8. Scientific ceiling and unchanged inputs

Repair confirmed within the evidence available in the sealed intake.

The five frozen G347-G351 source derivations match every digest in `FROZEN_SOURCE_HASHES.tsv`. The G352 exact derivation states that the metric, reciprocal kernel, angular sector, and owner-provisional vacuum response equation are unchanged, and it introduces no replacement for any of them. Because no external repository or trust anchor was accessed, this establishes consistency with the frozen sources in this intake, not identity with an external canonical copy.

The prohibited interpretation terms occur only in historical review discussion, open-item lists, explicit exclusion clauses, or negative regression sentinels. They do not enter the repaired equations as premises, selected meanings, generating mechanisms, fitted quantities, or conclusions. In particular, the repaired package selects no light, energy, detector, distance, source, population, history, matter, mass, scale, `X_max`, or canon.

## 9. Evidence-grade conclusion

No repair-completion defect remains within the R2 scope. The accepted maximum conclusion is only this:

On the explicitly chosen continuous total-phase-variation, phase-independent nonnegative product realization, and on common nonzero absolutely continuous regular support, the conditional clock-rate density has `T_clock=R A^-1`; `(p,q)=(1,-1)` is unique only for that readout inside G350's full independent positive character domain; phase normalization, observer covariance, identity, sewing, and comparison reversal close; and the measure-valued rank-loss formulation is finite only under the stated measurability and frequency-integrability conditions. Atomic crossings, `p=0`, other readouts, physical realization, source/population data, and every prohibited interpretation remain distinct or open.

ACCEPT_G352_R2_REPAIR_COMPLETION
