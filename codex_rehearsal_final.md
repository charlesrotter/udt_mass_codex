1. Actual HEAD and full status

- Branch: `grok`
- HEAD: `f239d0b039185fb2f32423e1f80beb54ce7ac68a`
- Commit: `f239d0b Audit F return evidence and fix native-action test`
- Relationship: one commit ahead of `origin/grok`; pull reported “Already up to date.”
- Tracked modifications:

```text
noNull_nk_out.json
noNull_nk_traj.json
noNull_resolve_out.json
```

- Untracked:

```text
AGENTS.md
codex_rehearsal_invocation_error.txt
codex_rehearsal_transcript.txt
scratchpad/ckpt_correctness.txt
scratchpad/controlled.stdout
scratchpad/e2e_tb.txt
scratchpad/hess128.stdout
scratchpad/hess_256_bs8_production.stdout
scratchpad/hess_bs10.stdout
scratchpad/hess_bs8.stdout
scratchpad/hess_bw2_full.stdout
scratchpad/hess_p3.stdout
scratchpad/hess_p4.stdout
scratchpad/hess_pstream2.stdout
scratchpad/hess_pstream_smoke.stdout
scratchpad/hess_smoke.stdout
scratchpad/hess_smoke2.stdout
scratchpad/long_relax_256.stdout
scratchpad/memdiag.py
scratchpad/memdiag2.py
scratchpad/memdiag3.py
scratchpad/memprobe_ckpt.txt
scratchpad/memprobe_hess.py
scratchpad/memprobe_out.txt
scratchpad/memprobe_out2.txt
scratchpad/nk128_relax.stdout
scratchpad/nk192_relax.stdout
scratchpad/nk_full.stdout
scratchpad/nk_smoke.stdout
scratchpad/nkpc_full.stdout
scratchpad/nkpc_smoke.stdout
scratchpad/noNull_hess_U1.stdout
scratchpad/noNull_hess_full.stdout
scratchpad/noNull_hess_smoke.stdout
scratchpad/noNull_relax2_smoke.stdout
scratchpad/noNull_relax_fixed_smoke.stdout
scratchpad/noNull_relax_smoke.stdout
scratchpad/noNull_relaxcg_full.stdout
scratchpad/noNull_relaxcg_smoke.stdout
scratchpad/noNull_relaxlbfgs_full.stdout
scratchpad/noNull_relaxlbfgs_smoke.stdout
scratchpad/noNull_resolve.stdout
scratchpad/noNull_resolve_stage2.stdout
scratchpad/nrx.stdout
scratchpad/nrx_lbfgs.stdout
scratchpad/phaseB_256.py
scratchpad/phaseB_256_clean.py
scratchpad/phaseB_256_relaxed.py
scratchpad/phaseB_scaling.py
scratchpad/rj_test_128.stdout
scratchpad/stability_branch_follow_256.stdout
scratchpad/stability_eigenmode_256.stdout
scratchpad/test_save_summary.py
```

Nothing is staged. I made no changes.

2. Current honest particle-lane claim and premise stamps

The corrected-carrier arc is complete through F:

- **OBSERVED / NUMERICALLY CERTIFIED:** the complete \(U(1)^\perp\) static Hessian of this \(Q\simeq1\), lower-energy carrier is positive at \(128^3,192^3,256^3\), including the T/R sector through the Schur-complement inertia seal. This is static stability in the stated finite-box frame—not dynamical or infinite-volume stability.
- **CONDITIONAL:** under the EH metric-only lapse premise and weak-field unit response,
  \[
  M_N^{(0)}=2E_4,
  \]
  with continuum audit \(2E_4\simeq283.3\text{–}283.5\) in \(\xi=\kappa=1\) units. The carrier energy is instead approximately \(275.9\); they are not identified.
- **OBSERVED:** the corrected \(L=6\) carrier retains a continuum-audit virial gap of about \(-2.7\%\).
- **STRONG LEAD:** the gap is finite-box boundary dilation stress, supported by the exact virial response, the \(E_2\)-rich pinned-wall skin, and monotone two-resolution box scouts. The local surface theorem and \(L\to\infty\) closure remain **OPEN**.
- **STRONG LEAD:** no resolved exit from one robust relaxation basin was found in the preregistered F slice.

Premise ledger:

- \(S^2\) carrier/unit-vector matter field: **POSIT**, not metric-derived.
- Round \(S^2\) target metric and full target \(SO(3)\): **CHOSE + canonized**.
- \(L_2\) and \(L_4\): **DERIVED given the posited carrier**; the carrier-plus-functional frame remains premise-scoped.
- Corrected eight-orientation no-null discretization: **DERIVED numerically** as cubic-symmetric, \(O(h^2)\), and convergent to the same continuum \(L_2+L_4\) functional.
- Carrier: **this** independently relaxed lower-energy \(Q\simeq1\) branch.
- Character: **static**.
- Box \(L=6\): **FREE**.
- Pinned mask `HBW=2`: **FREE**; wider-mask boundary sweep not done.
- Finite grids and all numerical outcomes: **OBSERVED**, not automatically physics or canon.
- EH/metric-only action and lapse identity: **CONDITIONAL-DERIVED** through the minimality/Lovelock premise, not native UDT.
- F does not use EH or G.
- Fixed boundary is a solver boundary, not a claimed physical wall.
- DATA-BLIND; no observed masses, particle labels, fitted couplings, or \(\kappa_g\) were used.
- Physical dynamics, infinite-volume basin/stability, native carrier emergence, \(M_N^{(0)}=E_{\rm carrier}\), and canonization remain **OPEN** or pending Charles.

3. Exact F endpoint counts and classes

| Grid | Endpoints | Exact classes |
|---|---:|---|
| \(128^3\) | 59 | 1 `RETURNED BASIN`; 58 `OTHER STATIONARY BRANCH` |
| \(192^3\) | 12 | 12 `RETURNED BASIN` |
| \(256^3\) | 12 | 12 `RETURNED BASIN` |
| Total | **83** | **25 returned; 58 other stationary** |

There were zero `DISTINCT LOWER Q~1 STATIONARY POINT`, zero `RESOLVED LATTICE TOPOLOGY SLIP`, and zero `UNRESOLVED` endpoints. The repaired independent verifier passed 51/51.

4. Why “single robust basin” is a lead

It is an inference, not the literal census:

- 58 of the 83 raw endpoints are explicitly `OTHER STATIONARY BRANCH`, not `RETURNED BASIN`; those classes were correctly retained.
- Their behavior is consistent with measured near-degenerate T/R finite-box drift, but consistency does not authorize relabeling.
- Only a preregistered soft-direction slice was sampled: finite directions, amplitudes through \(1.20\) radians, three finite grids, fixed \(L=6\), and `HBW=2`.
- The paths are trust-region relaxation trajectories, not physical time evolution.
- The study did not classify all sectors, branches, boundaries, masks, amplitudes, or the infinite-volume solution space.

Thus the literal result is “no topology change, lower stationary state, or resolved basin exit observed”; “single robust basin” is a **STRONG finite-slice LEAD**.

5. Open choices and authorized next action

Charles’s open desk choices are:

- Audit the F return and the G/boundary-virial/audit-patch chain.
- Review §0/§1 of the draft native-action dispatch; its arms have not been launched.
- Decide any stability or basin canonization.
- Choose the next push among the boundary-layer theorem route, native-action arms, box/mask study, or spin-isorotation on the certified carrier.

The particle lane’s next action authorized by [LIVE.md](/home/udt-admin/udt_mass_codex/LIVE.md) is **WAIT on Charles**. No extension, native-action arm, canonization, or new computation is currently authorized.