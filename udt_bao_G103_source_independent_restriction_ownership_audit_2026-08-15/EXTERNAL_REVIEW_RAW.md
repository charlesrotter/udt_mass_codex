PASS_WITH_CAVEATS

**Reruns**
- `REVIEW_SCOPE.json`: declared payload count `30`; recomputed payload count `30`; all `30/30` byte counts and SHA-256 digests matched exactly.
- Exact direct reruns in this sealed read-only intake:
  - `verify_package.py`: exit `1`; `OSError [Errno 30]` on `VERIFICATION_RESULT.json`
  - `derive_restriction_atlas.py`: exit `1`; `OSError [Errno 30]` on `DERIVATION_RESULT.json`
  - `run_catch_proofs.py`: exit `1`; `OSError [Errno 30]` on `CATCH_PROOF_RESULT.json`
  - `verify_restriction_independent.py`: exit `1`; `OSError [Errno 30]` on `INDEPENDENT_VERIFICATION.json`
- Non-writing shadow replays of the same four scripts all exited `0` and reproduced the stored headline results:
  - `verify_package.py`: `PASS`, `gate_count=14`, `failures=[]`
  - `derive_restriction_atlas.py`: `PASS`; landing exactly `LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED__COMMON_SKY_GRAM_AND_GENERIC_MEASURE_CONSISTENCY_ONLY__NO_NONTRIVIAL_SOURCE_INDEPENDENT_PATTERN_RESTRICTION_OWNED_IN_FROZEN_SOURCE_UNIVERSE__GLOBAL_CRITICAL_BOOTSTRAP_AND_SOURCE_HISTORY_JOINTS_OPEN`
  - `run_catch_proofs.py`: `PASS`; `11/11` hostile mutations caught
  - `verify_restriction_independent.py`: `PASS`; `imports_production=false`

**Independent Mathematical Adjudication**
- Zero-order surjectivity is valid on the stated scope. If `E in GL(4,R)` and the target pair coframe `V_*` has rank `2` with Lorentzian pullback, then `J=E^-1 V_*` exists, `rank(J)=2`, `EJ=V_*`, and `J^T E^T eta E J=V_*^T eta V_*`. That proves local reachability while `J` remains supplied; it does not own a physical query law.
- First-jet surjectivity is also valid on the stated scope. From `V=EJ`, `dot V = dot E J + E dot J`; for arbitrary target `dot V_*`, setting `dot J = E^-1(dot V_* - dot E J)` gives `dot(EJ)=dot V_*` identically. This is first-jet kinematics only, not a global smooth-history or singular-branch theorem.
- The fixed-base positive-Gram theorem is real but conditional. With one fixed A-calibrated base and PSD addition, `(t-A)(B-ell) >= t A Delta^2` and `phi >= phi0` hold. G103 is correct not to promote that to released `J`: once `J` is freed, the witness with base `phi_base=log(9/4)/4` and target `phi_released=log(4/9)/4` shows lower `phi` is reachable without contradiction because the shared-base/query-calibration premise has changed.
- The common-sky Gram classification is correct. For two directions, `G=[[1,c],[c,1]]` is realizable iff `|c|<=1`, so there is no extra two-source angular restriction beyond legal sky realizability. Rank `<=3` is a real constraint only on simultaneously labeled multi-direction skies.
- The three finite symmetric couplings do have the same one-point marginal and distinct angle laws `0`, `pi/2`, and `pi`. The continuum construction is mathematically sound by rotational invariance: sampling `n` uniformly on `S^2`, `c~rho`, and `m` uniformly on the circle `n·m=c` yields uniform marginals and the prescribed cosine law `rho`.

**False-Pass Analysis**
- A false pass would occur if the review froze `J`, omitted the `-dot E J` term, promoted fixed-base reachability after releasing `J`, treated one-point marginals as determining pair law, globalized a local result, or treated endpoint composition as a selector of star depths. Those are exactly the registered hostile mutations, and all were caught.
- I found no overlooked active source-independent restriction in the nine frozen sources. Endpoint composition is a coherence law on a supplied matched calibration family; overlap gives coexistence/gluing conditions; joint Gram gives simultaneous realizability conditions; none excludes an otherwise regular two-source observable pattern once `J`, source pair measure, and global completion remain open.
- Outcome blindness and protected-source exclusion are preserved within this intake: the source manifest is exactly the nine frozen entries, the executable audit checks no outcome artifacts were read, and no protected-package paths appear in scope.

**Retained Caveats And Maximum Justified Conclusion**
- The executable harness is not read-only-clean: exact direct reruns fail operationally because the scripts rewrite sealed JSON outputs.
- The negative result is strictly source-bounded, regular, local, and first-jet. It does not cover singular/critical strata, global completion/topology, bootstrap, or any joint source-history law.
- Real residual constraints remain: common-observer typing, `Z>0`, sky Gram `PSD` with unit diagonal and rank `<=3`, generic measure consistency, fixed-base PSD reachability on a shared calibrated base, and endpoint composition on a supplied coherent family.

Maximum justified conclusion:
`LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED__COMMON_SKY_GRAM_AND_GENERIC_MEASURE_CONSISTENCY_ONLY__NO_NONTRIVIAL_SOURCE_INDEPENDENT_PATTERN_RESTRICTION_OWNED_IN_FROZEN_SOURCE_UNIVERSE__GLOBAL_CRITICAL_BOOTSTRAP_AND_SOURCE_HISTORY_JOINTS_OPEN`
