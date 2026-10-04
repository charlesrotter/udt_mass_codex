# ACP1 source-first fidelity reconstruction

Status: source-first reconstruction sealed before access to a new ACP1 mathematical candidate, equations file, implementation, or result. This is a fixed review artifact, not another maintained scientific development.

Reviewer context: `/root/acp_fidelity`, a real separate context from the author and other reviewer; same inherited model, exact model revision unavailable. No human or different-model independence claimed. The parent's dispatch, WORK_ORDER, BASELINE.json and prior OEV1 review record were exposed. Published outcomes and the maintained R6/R13/OEV1 discussion were exposed; this is not blind empirical confirmation. A broad read of BASELINE plus PRIOR_REVIEW_RECORD initially produced truncated prior-package metadata; no new ACP1 proof was in that read. Source-first describes the ordering relative to ACP1 candidate exposure, not ignorance of prior conclusions.

Startup attribution: the top-level parent owns the mandatory startup, synchronization and full premise audit, as recorded by BASELINE.json. Independently checked local branch `grok`, HEAD `7fc10f933236880dc6e0c842e0dc31d3da834aa0`, and dirty/untracked status. Protected prefixes were encountered only as path names in status/baseline metadata; their payloads were neither opened nor hashed. Read on-disk AGENTS.md, scoped CLAUDE sections and triggered no-shortcuts/completeness-map/verifier-before-record protocols. No central mutation, solver/GPU process, registry grade change, stage or commit.

## Source versions and direct checks

Pinned primary sources, with byte bindings in SOURCE_VERSIONS.json:

- MCP XI: Pesce et al., arXiv 2001.04581v1, `M2_Pesce_2001.04581v1.pdf` and its extracted text. Directly inspected §3, §4.1–4.3, Table 4 p7, Table 5 p11, Appendix A pp17–18 and Appendix B pp18–21. Rendered and visually checked p7, p18, p21.
- MCP XIII: Pesce et al., arXiv 2001.09213v2, `M1_Pesce_2001.09213v2.pdf` and extracted text. Directly inspected Table 1 p4 and associated distance/velocity conventions; rendered and visually checked p4.
- Maintained UDT_DEVELOPMENT.md R6 and R13, plus the controlling FSL1 INITIAL_CANDIDATE §§1–2, G348 EXACT_DERIVATION §3 and G349 AUDIT_REPORT findings/distinctions. These are conditional query/geometry sources, not source-dynamics authority.

A bounded retrieval log is in ACQUISITIONS.json. Four requests were used. Arxiv's abstract identified journal DOI `10.3847/1538-4357/ab6bcd`; local source retrieval failed DNS, primary publisher search was robots-blocked, and web arxiv source retrieval returned cache miss. No complete machine-readable Table 4 was acquired. No source response was fabricated. Existing six printed rows are an illustration subset, not the full catalog. No authors were contacted. Acquisition is exposed researcher work, not fresh blind observation.

## What the measurements and summaries mean

1. **Angles:** each VLBI channel defines a maser spot, fitted with the known restoring-beam Gaussian to obtain a centroid in sky x/y (east/north) relative to a phase center. Retained spots meet measured S/N >=3. Position uncertainty and added x/y error floors are part of the inference. These are processed angular positions, not physical source separations.
2. **Velocity:** Table 4 velocities are optical-convention `v=c_E z` in the barycentric frame. A channel center is not a precisely measured physical velocity vector. Its effective uncertainty includes finite channel width, a line spanning channels, and drift over the VLBI observation span. The model has separate systemic/high-velocity error floors. The paper's stated CGCG conversion is `v_CMB=v_bary+263.3 km/s`; that is a source reduction convention, not a universal observer-independent speed or a native preferred frame.
3. **Acceleration:** Eq(2) obtains linear spectral-centroid drift against monitoring epoch from time-dependent Gaussian decomposition. Lines are fitted over nine successive observations with variable amplitudes and fixed widths; resulting drifts are binned to match VLBI channels. Table 4 flags `1` measured and `0` modeled accelerations. B21 explicitly omits unmeasured accelerations from its measurement likelihood. Reusing flag0 values as data would make a circular test of the disk model.
4. **Summary:** MCP XIII's CGCG row is `D=87.6(+7.9,-7.2) Mpc`, optical CMB `v=7172.2 +/-1.9 km/s`, posterior medians and marginal 16th–84th percentiles, sourced to MCP XI. MCP XI Table 5 instead gives barycentric systemic `6908.9(+1.8,-1.9) km/s`; the stated frame offset maps its median to7172.2. It separately gives model-choice systematics `1.5 Mpc` and `1.7 km/s`. Those systematics must not disappear when quoting the distance's scope. MCP XIII's printed CGCG interval is not asserted to include them.
5. **Distance source dependence:** Appendix A uses physical radius `R=r D`, warped thin-disk geometry, point-mass inverse-square acceleration `GM/R^2`, Keplerian velocities, SR Doppler factors and a Schwarzschild gravitational-redshift factor. A15 multiplies these local factors by a systemic redshift factor. The selected fit fixes eccentricity and inclination warp to zero, retaining a position-angle warp; alternate fits assess source-model systematics. These are conventional source/readout hypotheses, not native UDT equations. The fit avoids an imposed cosmological distance–redshift curve at this stage; it is not independent of gravity/disk physics.
6. **Joint inference:** Appendix B defines Gaussian factors for angular coordinates and measured accelerations with quadrature error floors and velocity factors with group-specific widths, then multiplies them under its measurement-independence assumptions. Normalization terms matter if widths vary. Parameters and all nuisance spot locations are jointly fitted; source priors and model choices matter. Conditional measurement-factor independence does not imply posterior parameter independence. Two marginalized intervals do not recover a joint likelihood or covariance; a product of Gaussian surrogates is an additional statistical model. MCP XIII and MCP XI CGCG summaries share the same underlying source data and cannot be counted as independent evidence.
7. **Excluded cosmological stage:** MCP XI §4.3 and MCP XIII §3 subsequently introduce flat-LambdaCDM/H0 and peculiar-flow treatments. Their `7308 +/-150 km/s` flow value in XI is not the measured systemic `7172.2` summary. ACP1's comparison must not silently import that cosmological stage, peculiar correction or a fitted D(z).

## Received-time and optical-convention seam

This is an independent mathematical reconstruction under the R6 conditional interface, not a statement that the source pipeline implements an uninspected correction.

Supply a regular null correspondence with source and observer proper times `s,t`, stable source transition frequency, and `Z=dt/ds=nu_e/nu_o>0`. If the observed ratio is identified with this stable transition, the optical proxy is `V=c_E(Z-1)` and its reception-proper-time derivative is

    dV/dt = c_E dZ/dt = (c_E/Z) dZ/ds = c_E d(log Z)/ds.

If reduced observation epoch differs from receiver proper time or a frame correction depends on epoch/direction, carry that derivative explicitly. The printed monitoring slope is a fitted finite-window spectral drift, so an instantaneous derivative also needs an epoch/estimator approximation or replayed observation model.

For a supplied factorization `Z=Z0 Q` with constant bulk factor `Z0`,

    dV/dt = c_E Q'/Q,  where prime means d/ds.

Thus the bulk factor multiplying the optical velocity change cancels the same bulk factor in received-time stretching. Adding an isolated division by `(1+z0)` to an already consistent optical-velocity derivative can be wrong. For varying factors one must differentiate both. A source coordinate-time derivative is not automatically a source proper-time derivative. Appendix A A6–A7 gives projected Newtonian acceleration; the pinned text does not describe a standalone new `(1+z0)` acceleration correction or establish an exact equivalence between every relativistic spectral derivative and A6. Neither assert a source defect nor repair the source numerically by assumption. A native UDT time correction is not supplied here.

## Angular-distance seam

R13 establishes a two-dimensional metric screen and its full Jacobi map; determinant reciprocity controls area. It does not state that a finite, warped, moving source disk is transported by a common scalar angular distance. Full ray/source-history incidence is required first. A local approximation then needs a specified source screen/projection, branch, angular patch, derivatives and error bound.

For a regular local angle-to-source-screen map J, area distance is `D_area=sqrt(|det J|)`. It discards shear and orientation. The same-area family `J=diag(D q,D/q)` with positive q has unchanged area distance and different directional spot predictions. It follows that area equality alone cannot justify importing the scalar D from Appendix A's `R=rD` into a general supplied-metric comparison. A similarity-map approximation `J=D O` needs actual control of anisotropy and finite-patch variation. Disk-plane projection, depth and retarded source positions are separate required incidence data; R13 area geometry does not remove them.

## Source bookkeeping defect and honest ceiling

The p21 PDF visibly states `Nr=71, Nb=50, Ns=45, Na=20`, then `604` constraints and `348` parameters, while stating formula `4(Nr+Nb+Ns)-Na` and an extra `Na` free-parameter contribution. Literal arithmetic gives644 for that measurement formula;16+2*166+20 gives368, not348. The printed totals604-348 do yield256, but the preceding definitions do not establish those totals. This is an unresolved source bookkeeping inconsistency, not a refutation of the distance fit. Do not invent full-table counts or fix the source by choosing whichever numbers fit. Without full data/code, do not rely on this narrative for a reconstructed degrees-of-freedom or likelihood validation.

The strongest available return is a conditional forward observable specification with source-assumption and approximation gates, plus faithful marginal readouts. No native metric has been selected, no disk/source law derived, no full likelihood reconstructed, no numerical fit or empirical goodness-of-fit obtained, and no source or UDT grade upgraded. This source-first note is ready for candidate exposure and adversarial checks.
