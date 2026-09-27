# WORKSTATION DISPATCH — boundary-evidence patch, then H3 behavioral F

**Date:** 2026-07-16  
**Branch:** `grok`  
**Input commit:** `837d633`  
**Order:** patch the boundary-virial record → verify → if and only if green, run F → STOP  
**Data discipline:** DATA-BLIND. No particle labels, observed masses, fitted couplings, invented cutoffs, or new
continuum terms.  
**Record discipline:** preserve unrelated dirt; do not edit `LIVE.md` or `CANON.md`; do not overwrite any certified
carrier, Hessian, Schur, G, or boundary-virial artifact.

## 0. Audit verdict on `837d633`

The load-bearing result passes audit:

- the continuum carrier stress and residual sign are correct;
- the exact discrete common-scale response is correct;
- the fixed-\(h\) larger-box carriers genuinely meet the registered criticality gate;
- \(|\delta_{\rm vir}|\) decreases monotonically with wall distance at both probed spacings;
- the local surface construction improves with refinement but is not yet closed.

Therefore the bounded conclusion remains:

\[
\boxed{
\text{BOX-STRESS NUMERICAL LEAD; local discrete surface closure OPEN; }
L\to\infty\text{ closure OPEN.}
}
\]

Under the separately stamped conditional lapse premise,

\[
M_N^{(0)}=2E_4=E_{\rm carrier}+B_{\partial\Omega}+W_{\rm res}.
\]

At an exact finite-domain stationary point \(W_{\rm res}=0\).  None of this promotes the carrier or EH premise to
native UDT derivations.

The following record defects do **not** reverse the result, but must be corrected before F:

1. the exact padding/start construction and command ledger for V4 were not committed as a reproducible script;
2. the scout JSON/verifier retained only `Q_fwd`, although both `Q_fwd` and `Q_sym` were required;
3. the fine \(N=240\) row omitted `theta_max` and the requested \(E_2/E_4\) localization;
4. the measured \(a=2.95\) closure error scales approximately as \(h^2\), not \(h\), over the three available
   points (do not elevate three points to a theorem);
5. a literal two-point \(1/L\) fit at \(h_f\) has an unstable negative intercept, not an intercept “approximately
   zero.”  Delete that phrase.  The correct conclusion is that no intercept is identifiable from this scout.

## 1. Preflight

Run and show:

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

Read in order:

1. `LIVE.md` CURRENT STATE;
2. `HANDOFF.md`;
3. `stability_branch_follow_256_DECISION.md`;
4. `UDT_H3_BOUNDARY_VIRIAL_CLOSURE_BEFORE_F_DISPATCH.md`;
5. `noNull_virial_identity_derivation.md`, `noNull_boundary_virial.py`, and all boundary JSON/logs;
6. `noNull_energy.py`, `noNull_resolve.py`, `noNull_hess_refine.py`, `noNull_schur_inertia.py`;
7. the saved refined mode and critical-field manifests for \(128^3,192^3,256^3\).

Hash every input used below.  Confirm the workstation still has the three V4 relaxed NPZs with the hashes recorded
in `artifact_manifest.json`.  If a hash differs, stop; do not reconstruct a result around a changed field.

---

# PART A — evidence patch (no relaxation rerun)

## 2. Commit the deterministic V4 constructor

Create `noNull_boxscout_build.py`.  It must:

- read the original \(N=128,L=6\) carrier for the coarse starts and the original \(N=192,L=6\) carrier for the
  fine start;
- assert the exact expected \(N,L,h,\xi,\kappa\) and finite/unit field;
- fill the new arrays with the same solver asymptote
  \(\mathbf n_\infty=(0,0,-1)\);
- embed the old array centrally with integer offsets \(16,32,24\) for \(128\to160\), \(128\to192\), and
  \(192\to240\), respectively;
- neither rescale nor interpolate any source site;
- apply only the already-stated two-layer pin after embedding;
- save new, explicit `*_start_rebuilt.npz` files without touching the relaxed scout fields;
- assert bitwise identity of the embedded core and exact constancy of every added site;
- report the start energy and verify it matches the corresponding first line of each raw NK log to printed
  roundoff;
- record exact build and relaxation commands.  The historical relaxation need not be rerun.

Add a compact construction JSON and SHA-256/shape/dtype/parameter manifest entries for the rebuilt starts and the
existing relaxed scouts.

## 3. Complete the scout observables

From the unchanged relaxed fields, regenerate a complete `noNull_boxscout_observables.json` containing, for every
box in both fixed-\(h\) sequences:

\[
N,L,h,E_2,E_4,E,E_4-E_2,\delta_{\rm vir},Q_{\rm fwd},Q_{\rm sym},
\|g_f\|_{M^{-1}},\theta_{\max}.
\]

Also include the same preregistered cube and sphere localization fractions for **both** \(E_2\) and \(E_4\).  Do
not change any previously reported scalar.  Explain any change beyond serialization roundoff and stop if it is
load-bearing.

Extend `verify_noNull_boundary_virial.py` so its independent path recomputes:

- both no-null charges;
- `theta_max`;
- at least the \(a=2.5\) cube localization of \(E_2,E_4\);
- the central-copy/constant-fill predicates of the rebuilt starts;
- all old 38 checks.

The verifier may use the shared audited gradient only for the criticality scalar, as before; label that one check
`shared-gradient convention`, not an independent derivative implementation.

## 4. Correct the prose and quantify rather than characterize

Amend only `noNull_boundary_virial_results.md` and, if necessary, an evidence erratum—not `LIVE.md` or `CANON.md`:

- list the actual closure errors at \(a=2.95\);
- report the two successive empirical powers
  \(p=\log(e_i/e_{i+1})/\log(h_i/h_{i+1})\) and describe them as “approximately second order over these three
  grids,” not a proven asymptotic order;
- print the literal coarse three-point and fine two-point \(1/L\) intercepts for both the gap and
  \(|\delta_{\rm vir}|\);
- state that the two-point fine intercept is nonphysical/unstable and supports **no** limit inference;
- retain the conclusion `BOX-STRESS NUMERICAL LEAD`; local surface closure and infinite-volume closure remain
  `OPEN`.

Run syntax checks, the boundary verifier, the CAS verifier, and the existing evidence checker.  Preserve complete
stdout/stderr.  If the existing evidence checker requires workstation-only NPZs, run it there and commit its new
raw output.

Commit and push this evidence-only patch separately.  If any old check fails, either charge changes
inconsistently, or the regenerated start does not match the historical start energy, **STOP before F**.

---

# PART B — F: finite-amplitude behavioral branches

## 5. What F is—and is not

F asks how the already-certified static carrier's **energy basin** behaves at finite amplitude along its softest
shape directions.

It is **not** physical time evolution: no native UDT time-dependent action has been derived.  The trajectories are
trust-region minimization paths and may be called `relaxation behavior` or `basin behavior`, never dynamics or
dynamical stability.

Premise ledger:

- \(S^2\) carrier and \(L_2+L_4\) functional: **POSIT / CHOSE**;
- corrected eight-orientation discretization: same tested continuum functional, **DERIVED numerically**;
- finite-grid positive Hessian at \(L=6\), `HBW=2`: **OBSERVED / NUMERICALLY CERTIFIED**;
- F outcomes: **OBSERVED numerical basin behavior**, scoped to each grid/box;
- EH lapse premise and G mass readout: not used in F;
- physical dynamics, infinite-volume basin, and native matter emergence: **OPEN**.

Use only `energy_noNull`, `grad_noNull`, `hvp_exact`/`hvp_exact_chunked`, and the two no-null charge readouts.  No
centered energy, centered charge, Derrick rescaling, topology constraint, effective correction, or new coupling.

## 6. Build and verify the perturbation directions

Create `noNull_behavioral_F.py` with branch-specific filenames and restart-safe manifests.  Never import an old
branch script that executes the centered functional.

At each grid use the independently relaxed \(L=6\) carrier and both saved refined-mode seeds.  Before selecting a
representative basis:

1. form the free tangent projector (`HBW=2`);
2. remove exact target-space \(U(1)\);
3. build the six T/R generators with the same definitions as the certification and rank-revealing QR;
4. compare the two saved doublet subspaces by principal angles and the isolated vectors by absolute overlap;
5. stop if the seed agreement does not reproduce the committed certification;
6. project the selected three vectors afresh into the \(U(1)+T/R\) complement and orthonormalize them in the
   certification convention (Euclidean site inner product, with physical Hessian values divided by \(h^3\));
   also print the corresponding \(M=h^3I\) Gram matrix so the normalization is unambiguous.

T/R removal here defines **shape directions** only.  T/R must not be removed from the primary relaxation after
initialization.  Exact \(U(1)\) removal is gauge fixing and may remain.

The doublet **subspace** is basis-independent, but a finite angular sample is not.  Fix its angular origin to the
seed-0 refined basis after Procrustes-aligning seed 1, record that choice, and use the eight-direction plane sample

\[
v_{\alpha_k}=\cos\alpha_k\,v_5+\sin\alpha_k\,v_6,
\qquad \alpha_k=k\pi/4,\quad k=0,\ldots,7.
\]

For the isolated mode use \(+v_7\) and \(-v_7\).  Record all raw overlaps, QR singular values, Gram errors, and
boundary/tangency errors.  For cross-grid direction labels, align the two-dimensional bases by a documented
two-by-two Procrustes map after interpolating vectors **only for the overlap calculation** and reprojecting on the
destination grid.  Never use an interpolated mode in an energy or relaxation run.  Report forward/reverse-map
principal angles; if the cross-grid alignment is ambiguous, confirm the whole eight-angle set rather than
pretending individual angles correspond.

## 7. Pointwise geodesic perturbations and the small-amplitude gate

For each direction set \(w=v/\max_x|v(x)|\), so the coefficient is the maximum pointwise target-space rotation.
Generate

\[
\mathbf n_{\theta}(x)=
\cos(\theta|w(x)|)\,\mathbf n_0(x)
+\sin(\theta|w(x)|)\frac{w(x)}{|w(x)|},
\]

with the zero-vector limit handled analytically.  Because \(w=0\) on the pinned layers, the boundary must remain
bitwise fixed.  Verify \(|\mathbf n_\theta|=1\), the realized maximum angle, and finite values to roundoff.

Before any long relaxation, at all three grids and for at least one direction from the doublet plus the isolated
direction, perform the symmetric sweep

\[
\theta\in\{2\times10^{-3},10^{-3},5\times10^{-4}\}.
\]

Compare

\[
q_\theta=\frac{E(\mathbf n_{+\theta})+E(\mathbf n_{-\theta})-2E_0}{\theta^2}
\]

with \(\langle w,Hw\rangle\) from the **exact** normalized-field HVP (chunked at \(256^3\)).  Gate: the two
smallest amplitudes must agree with each other and the exact HVP to relative \(10^{-2}\), with absolute errors
also printed.  If cancellation prevents this gate, enlarge the entire preregistered triplet by one factor of two,
record the failure, and do not tune direction by direction.  Stop if no controlled quadratic window is found.

This gate checks operator provenance and geodesic construction; it does not re-certify the spectrum.

## 8. Calibrated control first

At every grid, first run the unperturbed carrier through the same repaired moving-tangent Newton–Krylov code and
save a branch-specific control trajectory.  Require \(\|g_f\|_{M^{-1}}<0.05\) without loosening.  This final
control—not a rounded historical energy—is the comparison baseline for branch classification.

Also run:

- one finite exact-\(U(1)\) target rotation as an energy/charge invariance control;
- the six geodesic T/R-generator controls at \(\theta=0.10\) on \(128^3\), with one representative translation
  and rotation repeated at the finer grids.

The T/R controls measure finite-box/grid walls.  They are not intrinsic physical modes.

## 9. Adaptive amplitude bracket at \(128^3\)

For each of the eight doublet-plane directions and both isolated signs, begin at

\[
\theta_{\max}=0.05
\]

and double only as needed through the fixed ladder

\[
0.05,\ 0.10,\ 0.20,\ 0.40,\ 0.80,\ 1.20\ \text{radians}.
\]

At each amplitude:

1. save the unrelaxed geodesic state and all observables;
2. run the full nonlinear corrected energy with fixed boundary and repaired moving-tangent trust-region
   Newton–Krylov;
3. remove only exact \(U(1)\) in the primary solve—do **not** hold T/R;
4. retain every accepted/rejected step and complete observables;
5. stop increasing that direction once an outcome differs from the preceding amplitude, then bisect that one
   interval at most three times in \(\theta\).

If every amplitude through \(1.20\) returns, report only `no transition found within the registered resolved
amplitude range`; do not invent a larger physical cutoff.  Stop a trajectory as numerically unresolved if the
maximum nearest-neighbor angle reaches \(\pi/2\); this is a resolution guard, not a physical wall.

For every recorded step report

\[
E,E_2,E_4,Q_{\rm fwd},Q_{\rm sym},\|g_f\|_{M^{-1}},\theta_{\rm nn,max},
\]

plus imposed/realized rotation, raw displacement, core energy centroid, nested localization, T/R/U(1)
projections, trust radius, damping, predicted/actual decrease, acceptance ratio, and elapsed time.

Primary endpoints must meet the same criticality gate or be labeled `UNRESOLVED`.  A T/R-held repeat may be run
only when free drift obscures classification; label it `CONSTRAINED DIAGNOSTIC`, never the primary outcome.

## 10. Preregistered endpoint classes

Classify by comparison with the same-grid unperturbed control:

- **RETURNED BASIN:** criticality passes; both charges remain on the same branch; final energy and localization
  agree with the control within the measured control/restart variability; any displacement is explained by the
  separately measured T/R drift.
- **DISTINCT LOWER \(Q\simeq1\) STATIONARY POINT:** criticality passes; both charges and smoothness retain the
  topology; energy is below the control by more than five times the control/restart variability and at least
  \(5\times10^{-3}\); the result repeats from a neighboring amplitude or opposite/nearby direction.
- **RESOLVED LATTICE TOPOLOGY SLIP:** both charge readouts change coherently toward the vacuum branch and the raw
  trajectory resolves the required loss of lattice smoothness.  A single noisy charge or a run stopped at the
  \(\pi/2\) resolution guard is only `SLIP CANDIDATE / UNRESOLVED`.
- **OTHER STATIONARY BRANCH:** criticality passes and topology holds, but the final shape is not the control and
  is not lower by the preceding gate.
- **UNRESOLVED:** criticality, smoothness, charge agreement, or runtime gate fails.

Measure control/restart variability by two identical control launches and record it before applying these
classes.  Pre-register the numerical comparison envelopes as

\[
\tau_E=\max(5\sigma_E,10^{-3}),\qquad
\tau_Q=\max(5\sigma_Q,0.02),\qquad
\tau_{\rm loc}=\max(5\sigma_{\rm loc},0.01),
\]

where each \(\sigma\) is the maximum absolute difference between the two controls (not a fitted statistical
error).  `RETURNED BASIN` requires both charge differences below \(\tau_Q\), energy difference below \(\tau_E\),
and every registered localization-fraction difference below \(\tau_{\rm loc}\).  A resolved slip requires both
charge magnitudes to fall by at least \(0.4\) from their same-grid control values in addition to the smoothness
history already required above.  Print values even when a class fails.  Do not silently choose tolerances after
seeing a branch.

## 11. Fine-grid confirmation—not an exhaustive rerun

After the \(128^3\) bracket is complete:

- select the earliest transition bracket, if any, for each of: the doublet plane and isolated mode;
- if doublet anisotropy is seen, also select its most- and least-resistant registered directions;
- repeat only the inner/outer bracket endpoints and midpoint at \(192^3\), then \(256^3\);
- if no transition occurs at \(128^3\), repeat \(\theta=0.40,0.80,1.20\) only for two orthogonal doublet
  directions and both isolated signs at the finer grids;
- retain the same physical box \(L=6\), `HBW=2`, functional, amplitude definition, and classification gates.

This establishes grid sensitivity of the observed basin behavior.  It does not establish an infinite-volume
basin.  The new \(L=7.5\) scouts are not certified Hessian/mode backgrounds and must not replace the \(L=6\)
production carriers in F.

## 12. Independent verification and evidence

Create `verify_noNull_behavioral_F.py` without importing production branch construction or classification
functions.  It must independently check from saved artifacts:

1. mode subspace overlaps, tangent/free/U(1)+T/R projections, rank, and Gram matrices;
2. unit norm, fixed boundary, and realized geodesic angles for every initial branch;
3. selected small-amplitude energies using its own eight-orientation loop and the exact-HVP comparison;
4. both no-null charges, energy split, criticality convention, smoothness, and localization for all bracket
   endpoints;
5. every endpoint classification predicate by replaying the raw JSON—never repairing it;
6. all field hashes and branch-to-grid/angle/direction metadata.

Save compact JSON and complete stdout/stderr.  Save every \(128^3\) endpoint locally and at least all fine-grid
controls plus bracket endpoints; manifest large NPZs with SHA-256, bytes, shapes, parameters, source-mode hashes,
exact command, software/CUDA versions, and timestamps.  Never overwrite an endpoint from another branch.

Run syntax checks and the existing evidence checker.  Commit and push one F evidence commit containing sources,
compact outputs, verifier output, raw logs, and manifests.  Leave `LIVE.md` and `CANON.md` untouched.

## 13. Stop and return

Stop after the F evidence commit.  Return:

- Part-A patch commit and all corrected/added checks;
- F commit;
- control variability and small-amplitude gate table;
- \(128^3\) bracket table by registered direction;
- fine-grid confirmations;
- endpoint classes with raw gate values;
- independent-verifier verdict;
- `git status --short --branch` and `git log -8 --oneline`;
- all failures, stopped trajectories, and unresolved cases.

The maximum allowed conclusion is:

\[
\boxed{
\text{Within the corrected finite-grid }L=6\text{ carrier frame, the registered relaxation basin}
\text{ was characterized along the certified soft shape directions.}
}
\]

Do not call this physical dynamics, infinite-volume stability, native matter emergence, or a particle-mass
prediction.
