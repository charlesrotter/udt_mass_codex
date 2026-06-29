# GR/spectral numerics research — posing a singular-core elliptic BVP as DETERMINED (for the D1 fix)

*Deep-research workflow `wf_ba9b4d9d-ef3` (102 agents; 20 primary sources; 81 claims → 25 adversarially
verified, 0 refuted). All sources peer-reviewed/foundational; methods are stable numerics. Run for the D1
finding (the static solve is underdetermined: 1776 eqns / 4224 unknowns). This MINES the GR corpus
(Principle 4) for the proven fix — category-A technique.*

## Bottom line
A singular-core elliptic BVP is made DETERMINED by **exact equation-counting**, never by excising interior
nodes. Every spectral DOF gets exactly one equation: the PDE residual at the **interior (non-boundary)
collocation nodes** + boundary conditions + (multidomain) interface-matching → rows == unknowns, solved as
ONE square residual S(u)=0 by Newton/GMRES. Our D1 bug (masking 3 layers each end, all layers kept as
unknowns, one BC) is exactly the failure this prevents.

## Verified findings (with sources)
1. **Exact equation-counting / boundary-bordering (HIGH, 3-0).** Enforce the PDE residual ONLY at interior
   collocation nodes; allocate the remaining rows to BCs (+ interface-matching in multidomain) so rows ==
   unknown spectral coefficients. The discretized elliptic operator is *singular until BCs are prescribed at
   both endpoints*. Sources: Grandclément-Novak, *Living Rev. Relativity* 12:1 (2009) [lrr-2009-1]; Boyd,
   *Chebyshev & Fourier Spectral Methods* (boundary-bordering); Pfeiffer-Kidder-Scheel-Teukolsky, *Comput.
   Phys. Commun.* 152:253 (gr-qc/0202096).
2. **One square residual S(u)=0; solve for COEFFICIENTS, not real-space values (HIGH, 3-0).** SpEC: "the
   combined problem of solving the PDE, satisfying the BCs, and matching between subdomains is cast into one
   set of equations." Imposing more collocation equations than spectral DOF makes the solver fail — solve for
   the actual spectral DOF. Source: gr-qc/0202096.
3. **Origin regularity via PARITY, not excision (HIGH, 3-0).** Decompose into angular modes; a regular field's
   radial coefficient behaves as **r^l** (scalar, mode l) or **r^|m|** (azimuthal mode m); enforce by
   restricting the Chebyshev expansion to the matching parity (even polys for even l, odd for odd l). Sources:
   Bonazzola-Gourgoulhon-Marck (gr-qc/9811089, LORENE); Boyd Parity Theorem 35; Mohseni-Colonius, *JCP* 157
   (2000).
4. **Galerkin basis-recombination (HIGH, 3-0).** Expand on recombined functions (e.g. T_2n−T_2n+2 for even l)
   that satisfy origin regularity automatically; the l-mode operator is rank-deficient by exactly one (the
   homogeneous r^l mode), closed by adding the homogeneous to a particular solution in coefficient space.
   Source: gr-qc/9811089. **Caveat:** stated for the LINEAR scalar Poisson iteration with an analytic r^l null
   mode; transferring to a coupled nonlinear scalar-tensor system needs per-iteration recomputation (not
   literally proven in-source).
5. **Avoid-the-origin grids (HIGH, 3-0).** Place NO node at r=0: Gauss-Radau, even-count doubled-interval
   Chebyshev, or differentiate through the pole — no pole condition needed. Sources: Mohseni-Colonius *JCP* 157;
   Chen-Su-Shizgal *JCP* 160 (2000). **TRADE-OFF:** validated for SMOOTH/parity-regular fields and the Poisson
   equation — NOT automatic for a genuinely singular ~1/r² winding-defect density.
6. **The gravitating global monopole, concretely (HIGH, 3-0).** Hedgehog Φ^a=h(r)x^a/r + Schwarzschild-type
   metric → small ODE system; **center-regularity (h=f1·r+O(r³), even-power metric functions) leaves ONE free
   origin datum h'(0)**, fixed by the outer BC via shooting/relaxation → exactly one solution per 0<η̄<η̄max.
   Sources: Watabe-Torii (gr-qc/0206046); Maison-Liebling (gr-qc/9908038); DBI variant (arXiv:0902.1051).
   Finite-core "ballpoint-pen" regularization also exists (arXiv:0807.3919).

## THE KEY PHYSICS POINT THE RESEARCH SURFACED (a MAP/PONDER item, not mine to decide)
The global-monopole literature makes the core **regular by letting the scalar AMPLITUDE vanish at the center**
(profile h(r)→0 linearly, so the gradient energy ~h²/r² stays FINITE there — symmetry restored in the core).
**Our solver instead holds |n|=1 RIGID everywhere** (the unit-norm constraint), so n=x/r is genuinely singular
at r=0 (direction undefined, |∂n|²~1/r² diverges) — and we currently regulate it only by the rc=0.1 cutoff (a
"ballpoint-pen"/finite-core model). So:
- **Is |n|=1-everywhere a THEORY choice or a HABIT?** If a vanishing-amplitude profile is admissible, the core
  regularizes naturally (à la global monopole) and the standard parity methods apply cleanly. If |n|=1 is
  physically required, the core is genuinely singular and the rc-regularized finite-core treatment is the
  honest frame. This is a matter-model question for Charles — the research can't decide it.

## Application to the D1 fix — proven strategies (choose with Charles)
- **CORE FIX (unambiguous, must do regardless):** re-pose as a DETERMINED square system — impose the PDE
  residual at ALL interior radial nodes (drop the 3-layer body excision), with exactly enough BCs at the two
  true endpoints (core, seal), so rows == unknowns; solve as one residual S(u)=0. [findings 1,2]
- **ORIGIN treatment (two proven options, trade-off hinges on the physics point above):**
  - (A) **Parity/Galerkin basis** — bake r^l / r^|m| origin behavior into each field's radial basis *per its
    tensor/vector parity* (Boyd's per-component rules; the hedgehog couples angular structure to the warps).
    Principled; keeps r=0; the canonical LORENE/Kadath approach. [findings 3,4]
  - (B) **Avoid-origin grid** (Gauss-Radau / even-Chebyshev) — no node at r=0. Cheaper retrofit, BUT validated
    for smooth cores; questionable if our |n|=1 core is genuinely singular. [finding 5]
- **OUTER boundary:** the finite-cell DtN/Calderón closure was the THINNEST-sourced angle (under-sourced). The
  monopole literature uses asymptotic/horizon BCs; our finite seal needs its own determined closure — flag as
  needing more work or a junction-condition treatment.

## Open questions (honest gaps)
- Is our ~1/r² core genuinely singular (|n|=1 rigid) or should the amplitude vanish (regularizing it)? — drives
  the origin-treatment choice. **Physics decision for Charles.**
- Finite outer-boundary DtN/Calderón recipe for [r_core, r_seal] — under-sourced; not resolved here.
- Bonazzola homogeneous-closure for a COUPLED NONLINEAR system — needs per-iteration handling, not literally proven.
- Per-component tensor/vector parity for each warp + dilaton vs the scalar — must use Boyd's tensor-parity rules.
