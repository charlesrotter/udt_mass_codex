**Verdict**

`VERIFIED_WITH_CAVEATS`

I verified `33/33` `REVIEW_MANIFEST.tsv` paths and SHA-256 hashes before using any artifact. Reconstructing the package from [PREREGISTRATION.md](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/PREREGISTRATION.md:18), [EXACT_DERIVATION.md](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/EXACT_DERIVATION.md:11), [derive_local_jacobi.py](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/derive_local_jacobi.py:27), and [verify_local_jacobi_independent.py](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/verify_local_jacobi_independent.py:91), I reproduced:

`F01: ds^2=-A dt^2+dr^2/A+r^2(dtheta^2+sin^2theta dpsi^2)`

`F02: ds^2=F01+2h sin^2theta dt dpsi`, so `g_{tpsi}=h sin^2theta`

At the equator, with `D=Ar^2+h^2`,
`u=A^-1/2 ∂t`, `n=A^1/2 ∂r`, `E_theta=r^-1 ∂theta`,
`E_psi=h/(sqrt(A)sqrt(D)) ∂t + sqrt(A)/sqrt(D) ∂psi`,
`k=u+n`.
These satisfy `g(u,u)=-1`, `g(n,n)=g(E_theta,E_theta)=g(E_psi,E_psi)=1`, all cross terms `0`, and `g(k,k)=0`. The query is genuinely identical in the only defensible sense here: same event, same observer, same outward radial direction, same orientation rule, with only the metric-derived orthonormalization changing coordinate components. It is a legitimate local observer-sky control, not a material signal trajectory, and the package keeps that distinction explicit.

Using the declared convention `R(X,Y)Z=∇_X∇_Y Z-∇_Y∇_X Z-∇_[X,Y]Z`, I independently rederived the screen tidal matrix and got exactly
`T_F02 = diag(0,tau)`,
`tau = h0*N / [4*A0*(A0*r0^2+h0^2)^2]`,
with
`N = -4A0^3 h0 + 8A0^3 h1 r0 - 4A0^3 h2 r0^2 - 4A0^2 A1 h0 r0 + 2A0^2 A2 h0 r0^2 - 4A0^2 h0^2 h2 + 4A0^2 h0 h1^2 - 4A0 A1 h0^2 h1 + 2A0 A2 h0^3 + A1^2 h0^3`.
So `D(s)=sI-s^3T/6+O(s^4)`, `T_theta theta=0`, `T_theta psi=T_psi theta=0`, `T_psi psi=tau`, the screen matrix is symmetric, and the antisymmetric/rotation channel vanishes at this order. The `h0=0` cubic degeneracy and the `h0!=0, N=0` cancellation are both real. The independent package check reports `6/6` passes and exact rational witnesses `5312099/109652445` and `-20691746025/246491864192`; I also reproduced the weak-mixing parity: under the declared scaling `(h0,h1,h2)->ε(h0,h1,h2)`, the linear and cubic terms vanish and
`tau_2 = h0(-2A0 h0 + 4A0 h1 r0 - 2A0 h2 r0^2 - 2A1 h0 r0 + A2 h0 r0^2)/(2A0 r0^4)`
is exact. F01 also checks out: `T_F01=0` for arbitrary regular `A(r)`, and along a regular radial null branch `E=A dt/ds` is conserved, nullity gives `dr/ds=+E`, hence `r` is affine and `D_F01(s)=sI` until a caustic, chart failure, or endpoint.

**Defects and caveats**

- [AUDIT_REPORT.md](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/AUDIT_REPORT.md:25) cites preregistration commit `456aeec5`, while [PREREGISTRATION.md](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/PREREGISTRATION.md:4) cites base commit `0634b7f801253fc105d374c4c160dbbe19f5b9de`. That is a documentary inconsistency.
- The “independent” check is only partially independent. It does use a different curvature assembly route and a standalone F01 rebuild, but it still shares the same metric ansatz, the same tetrad/query choice, the same symbolic engine, and it reads the production JSON for comparison [verify_local_jacobi_independent.py](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/verify_local_jacobi_independent.py:130). So it is independent of the final Riemann differentiation path, not of the whole modeling stack.
- The validator architecture is sensitivity evidence, not semantic proof. [verify_package.py](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/verify_package.py:31) mainly checks stored artifacts, strings, factorization, and ledgers; [run_catch_proofs.py](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/run_catch_proofs.py:34) shows `12/12` mutations are caught, but that only shows fail-closed packaging discipline.
- The projection-freedom ruling is substantively correct but must stay local. [PROJECTION_FREEDOM_LEDGER.tsv](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/PROJECTION_FREEDOM_LEDGER.tsv:2) correctly assigns transverse scale-to-angle conversion to the Jacobi map, while [PROJECTION_FREEDOM_LEDGER.tsv](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/PROJECTION_FREEDOM_LEDGER.tsv:3) correctly leaves mode-ladder offset as boundary/operator phase. But this does not yet replace either historical fitted number in a physical CMB comparison because no endpoint, full profile, source scale, or population law has been supplied.

Maximum justified conclusion: the package has established a real local distinction on one preregistered observer-sky control query. Generic F02 gives a one-axis cubic Jacobi correction while F01 stays locally isotropic with exact `D=sI` on a regular radial segment. It has not derived a finite-distance sky map, a physical screen, a profile choice, a source/population rule, TT power, polarization, a local signal law, or a CMB prediction; those premise boundaries are preserved in [PREMISE_LEDGER.tsv](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11/PREMISE_LEDGER.tsv:2) and in the upstream query-typing document [EXACT_DERIVATION.md](/tmp/udt-f01-f02-jacobi-review-GPbfY3f7/udt_cmb_complete_observation_query_map_2026-08-11/EXACT_DERIVATION.md:18). The proposed finite-path next gate is justified as the next control calculation, provided it is separately preregistered and supplies an explicit endpoint, complete profile, and branch/caustic handling. Lay summary: the local sky-geometry calculation is mathematically sound and does distinguish the two control metrics, but only as a small-distance geometric effect, not yet as a physical CMB or signalling prediction.