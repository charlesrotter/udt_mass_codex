# GRC1 researcher A — evolving discovery record

## Scope, exposure and initial question formation

Scoped context `/root/grc_researcher_a`; inherited model, no different-model or human independence claim. Parent continuing-session startup and synchronization attributed. Independently checked branch `grok`, HEAD `89b4b473bed869f5ca296e9bfc67559a3c9ceaff`, and visible status names. Read AGENTS, campaign WORK_ORDER/BASELINE, required CLAUDE sections and no-shortcuts, completeness-map, solution-space-not-imposition protocols. No protected payload or baseline unrelated untracked file opened. Only this directory is writable by this researcher. Parent owns integration and Git.

Initial proposals below were formed before receiving the other researcher's or coordinator's hypotheses. Exposure already includes central D1/R1–R6/R9/R17/R18, R7 transport discussion, founding F1–F4/W1–W6; these are scientific context, not independence from existing research.

1. **SCT (scalar-composable transport), UNADOPTED.** Can the founded additive depth be physically realized as a positive character of metric parallel transport on a declared comparison network? General Lorentz transport is nonabelian; the first discriminating test is whether it admits a nontrivial smooth positive character. If not, look for meaningful reduced holonomy sectors rather than declaring the campaign exhausted. LKT1 already treats an actual Lorentz2/totally geodesic sector; novelty would have to lie in a four-dimensional invariant realization or a new physical clock test, not its already-known two-dimensional connection integral.
2. **RNC (recurrent-null comparison), UNADOPTED alternative suggested by SCT.** A null line preserved by metric transport admits a scalar scale character while retaining screen transport. Investigate whether its loop depth is curvature flux and whether ordinary clock comparisons can read it. A null line must be specified covariantly by the metric or stated as a sector/existence hypothesis; it is not an independent physical field. No preferred timelike observer is introduced. First tests: derive integrability and construct a nonflat metric witness, then check whether nontrivial scalar scaling survives physically normalized endpoint clocks or is only frame gauge.
3. **Clock optimization/global geometry (reserve).** If scalar transport does not give a viable physical connection, examine whether globally comparable ordinary clock readings plus a physically stated extremal/protocol property can restrict conformal geometry without assigning a preferred observer. Distinguish actual proper-time differences from scalar endpoint potentials; do not repeat GCP1's invalid support-to-chronology implication.

All are conditional investigations, not accepted deductions. No response identification E=Ric, physical action, fitted profile, population, or physical field equation is imported. The goal is an informative geometric/clock restriction beyond an evaluator. A source gap is a boundary to investigate, not by itself a reason to stop.

## Premise and method ledger

- F2/F3 reciprocal/additive representation and W1/W5 complete pair semantics: source-owned working/posit/readout scopes in founding.md and UDT_DEVELOPMENT R1–R7, not canon.
- W4 one metric, ordinary clocks and null rays: working metric interface, not a selected comparison network.
- SCT or RNC: newly invented exploratory connection, explicitly unadopted and permitted by campaign.
- Lie groups, holonomy, metric parallel transport and differential geometry: mathematical methods; primary literature hypotheses will be inspected before reliance.
- Metric witnesses, coordinates, null sector: `free-and-explored` supplied examples. No claim that UDT chooses them.

## Resource and calculation predeclaration

Exact pencil derivations first. Any executable check will use the existing TPS1 capture wrapper, CPU, one BLAS thread and 2 GiB virtual memory; no GPU, installations, field solves or numerical survey. Quantifier, domain, equations and error meaning will be recorded before each check. Pure exact rational/symbolic calculations have no floating point convergence claim.

## Milestone A1 — recurrence gives a connection, with a physical normalization test

The SCT obstruction is explicitly already in UDT_DEVELOPMENT R7/LKT1: the derivative of a real additive character kills brackets, and Lorentz rotations/boosts are all brackets. It is retained as prior tool, not a new result.

**RNC hypothesis, unadopted:** the metric on a connected regular Lorentz4 domain admits a parallel null line bundle. A nonzero local section l satisfies ∇_X l=ω(X)l. This is an existence restriction on the metric; specifying one line among several is further comparison data, not a new independent physical field. No timelike observer is selected by the hypothesis. The connection is Levi-Civita, not a new connection field.

Direct differentiation gives R(X,Y)l=(dω)(X,Y)l. Under l→e^f l, ω→ω+df. Along an arbitrary path, metric transport gives Pγ l_e=exp(-∫γ ω)l_o. On an actual affine null ray tangent to this line, define N_i=-g(l_i,U_i)>0 for future unit endpoint clocks. Then the actual frequency factor is

    fγ = frequency_o/frequency_e = exp(-∫γ ω) N_o/N_e,
    Phi_clock = log fγ = -∫γ ω + log(N_o/N_e).

This formula is gauge invariant and carries the endpoint clocks. It does not equate an arbitrary transport loop with an actual future signal-return experiment. Matching endpoint clocks at a common event cancels N in a mathematical loop; causal realization of such loops is a separate protocol question. Ordinary future signal legs are not assumed to close in spacetime.

A general local Walker metric is g=2du dv+h_ij(u,x)dx^i dx^j+2A_i(u,x)dx^i du+H(u,v,x)du². Its preserved null line is l=∂v and ω=(H_v/2)du. Galaev's primary papers support the normal form; only this geometric part is used, not the Einstein equations studied later in those papers. The recurrence is also checked directly below for a bounded polynomial witness.

Screen projection of ∇l vanishes, so this congruence has zero optical expansion, shear and twist. This is a real restriction, not a relabelled arbitrary metric. In the Walker gauge ω(l)=0; a ray along l is affine and its nonzero received clock shift can come from endpoint N. That is not an absence of gravitational redshift. It does mean loop curvature flux must not be claimed as the frequency change of an arbitrary light path.

**Check A1 predeclaration:** Exact symbolic CPU check on smooth real-coordinate Lorentz4 witness g=2du dv+dx²+dy²+(k v²+b x²)du², arbitrary real k,b (free-and-explored, no equation selected). Quantifier: all coordinates/parameters for polynomial tensor identities; no boundary, source, global completion or stability claim. Compute inverse, Levi-Civita symbols and all R(X,Y)l components independently from metric entries; check recurrence, curvature=dω and nonflat k term. Dtype SymPy exact integer/rational symbolic arithmetic; simplification residual exactly zero, not numerical tolerance/certification. CPU, one process/one BLAS, 2GiB virtual, wrapper capture, tiny JSON/text output, manual interruption, no wall/CPU killing timeout. Planned extension: exact curvature operators in a nonzero Schwarzschild tidal frame to test common-null-line obstruction, using the already sourced static vacuum curvature as a supplied GR comparison rather than adopting it as UDT.

## Milestone A2 — RNC narrowed; learned alternative NAR

A1 exact check passes (Python 3.10.12, SymPy1.13.1, 10 grouped identities; groups are not independent scientific confirmations). Direct geometry, not field equations, gives a nonflat recurrent-line witness for k!=0. The static subcase H=-a²v², a>0,v>0, is locally g=-(av)²dt²+dv²/(av)²+dx²+dy². For fixed-v proper clocks and an ingoing future ray, Z=v_o/v_e; thus recurrence does allow genuine nonzero received ticking shifts. Their sign depends on endpoints/direction. It does not create an all-direction cosmological redshift or select a scalar sign/scale.

**Universal-RNC quiet-limit obstruction, analytic argument.** For a recurrent line, every curvature endomorphism R(X,Y) preserves the same null line. At a regular Schwarzschild exterior point with nonzero geometric parameter mu, two curvature endomorphisms in a static orthonormal frame are nonzero multiples of the boosts B01 and B02 (full coordinate recomputation follows). B01's only real null eigenlines are e0±e1; B02 carries each outside its line. Its zero eigenspace span(e2,e3) is positive definite. Therefore no common invariant null line exists. This already excludes local recurrence, without a classification of holonomy groups. If recurrent-line metrics converged in C² to this metric on a fixed patch, normalize their null vectors against a smoothly chosen timelike frame; compactness of the normalized celestial sphere yields a convergent subsequence. Curvature-line preservation passes to the limit, contradicting the two-boost test. Thus universal RNC cannot have that C² quiet limit. This rejects this universal conjecture, not UDT, no preferred observer, selected-direction protocols, non-C² limits, or generic physical redshift. Recurrence only in the actual ray direction is not this restriction: an affine geodesic already obeys ∇_k k=0.

The optical restriction suggests allowing radial screen expansion instead of preserving a four-dimensional null line.

**NAR — null-affine areal reciprocity, UNADOPTED.** Supply a smooth spherical Lorentz4 region with r>0, metric g=h_AB dx^A dx^B+r²dΩ², and an untrapped region F=h^-1(dr,dr)>0. The symmetry/ruler choice is a declared sector, not a universal preferred center. Let K be the oriented h-Hodge dual of dr and choose its future orientation, K²=-F. Set U=K/sqrt(F). These are geometry-defined test clocks; actual population and a universal observer are not postulated. Proposed physical condition: for every sufficiently short regular radial affine null signal between these clocks, both ingoing and outgoing,

    Z = sqrt(F_o/F_e).

Equivalently, frequency times sqrt(F) is conserved. For radial null k, E=-g(K,k)=±k(r)=sqrt(F) frequency. Thus the proposed clock relation is equivalent to d²r/dλ²=Hess_h r(k,k)=0 on both null directions. In two Lorentz dimensions this means Hess_h r=(Box_h r/2)h. The warped-product Ricci identity then gives Ric_g(k,k)=-2r^-1 Hess_h r(k,k)=0 for radial null k only. The condition is NOT Ric=Lambda g and NOT zero focusing for all null directions. Its actual optical statement for spherical radial beams is r''=0: area expands as r² and shear vanishes by the supplied spherical symmetry; screen expansion is not erased.

As Hess_h r is pure trace, ∇_(A K_B)=0; since K(r)=0 it is also Killing for the full four-metric. Also dF=(Box_h r)dr, hence F=F(r) locally. In adapted coordinates the metric is

    g=-F(r)dt²+dr²/F(r)+r²dΩ²,

with arbitrary smooth positive F. Conversely every such metric meets NAR. No Einstein equation, action, stress tensor or selected profile enters. The causal character/horizon/constant-r sectors beyond F>0 are omitted deliberately from this first claim.

**Relation to prior UDT results.** The endpoint comparison is closely related to LKT1's actual zero-shift reciprocal-sector test; that source already shows equality with the same presentation-potential difference forces stationarity. NAR would provide a coordinate-free spherical extension with a metric-defined areal ruler/Kodama clock preparation, not claim discovery of its already known static result. Native W1 normalization alone does not imply NAR. A dynamic reciprocal chart can have determinant -1 while its actual received depth includes LKT1's time-derivative term. Kodama is divergence-free in any spherical geometry; its existence is not itself stationarity.

NAR leaves arbitrary F, and therefore arbitrary radial clock curves; allows Schwarzschild/Kottler supplied quiet witnesses; gives neither additional positional attribution nor a matched reference geometry. It is a real conditional restriction to test, not a physical derivation from F1–F4/W1. One direction alone will be tested using a time-dependent Eddington–Finkelstein/Vaidya-type metric; it must not silently be upgraded to both directions.

Cross-exposure: at this point the coordinator disclosed researcher B's independent matched-extra PSW1 sign/null-screen line. I did not read B's notes or proof. Both touch null optics, but B uses all null directions of a matched curvature difference; NAR is radial null Ricci of one spherical metric with a specified clock congruence. No merging or shared-premise claim yet.

**Check A2 predeclaration:** exact symbolic original-coordinate Christoffel/Riemann check in Schwarzschild static exterior with mu>0,r>2mu,0<theta<pi; tetrad only after computing curvature. Confirm two nonzero boost endomorphisms rather than assuming a generic holonomy classification. Then general symbolic 2D base h=-A(t,r)dt²+B(t,r)dr², A,B>0, r>0; verify radial Hessian/null contractions and Kodama Killing condition. For conditional witness h=-f(v,r)dv²+2dv dr, verify one affine null direction always has r''=0 while both require f_v=0. Exact symbolic expressions, no floating tolerance, no empirical fit or field equation; same CPU/wrapper/2GiB/one-thread controls. This check supports identities, not a proof by finite examples.

## Milestone A3 — exact clock/ruler defect and executable checks

A2 passed all14 grouped checks in1.49s, maximum RSS51,312KiB, with all angular geometry retained in the original4D curvature recomputation. Schwarzschild operators are exactly R(e0,e1)=2mu/r³ B01 and R(e0,e2)=-mu/r³ B02 on the stated exterior patch, confirming the RNC obstruction.

NAR has a useful exact diagnostic before setting it to zero. Let a radial affine ray stay in F>0, take σ=sign(k(r)), E=-g(K,k)=σk(r)=sqrt(F)omega. Then

    Z = sqrt(F_o/F_e) E_e/E_o,
    M := log Z - (1/2)log(F_o/F_e)
       = - integral [r''/r'] dλ
       = integral [r Ric_g(k,k)/(2 k(r))] dλ.

The ray and clocks are physical conditional W4/R6 objects; the null Ricci identity is warped-product geometry. F can be read geometrically as (dr/dell)², with ell a local proper radial ruler in the U rest space and r defined from sphere area. No arbitrary clock-potential gauge or separate field is introduced. This formula gives an experimentally specifiable discrepancy between received ticking and the proposed area/ruler factor; setting M=0 on every sufficiently short ray is the unadopted NAR restriction. A zero integral on one finite path does not imply zero integrand.

The A2 dynamic reciprocal control h=-q(t,r)dt²+dr²/q has det h=-1 but Hess r(k_±,k_±)=±q_t/q for k_±=(q^-1/2,±q^1/2). Thus completed determinant normalization does not impose NAR. The one-direction control h=-F(v,r)dv²+2dv dr has affine ingoing l=-∂r and r''=0 for arbitrary F(v,r); outgoing n=∂v+(F/2)∂r has Hess r(n,n)=F_v/2. Its4D outgoing radial Ricci is -F_v/r. Both-direction condition really adds information; one direction is not enough.

**Check A3 predeclaration:** actual finite proper-tick map, no solver. Supply q(t)=1+t on t>-1,r>0, and two fixed-areal-radius Kodama clocks separated by L>0. Outward radial null incidence solves L=int(te,to)(1+t)dt, hence to=-1+sqrt((1+te)²+2L). Differentiate this actual map and include proper-time factors; independently evaluate endpoint frequency from affine k^t=1,k^r=q. Check original null/geodesic equations and exact equality with the integrated defect. This supplied metric is not a physical UDT admission. SymPy exact algebra; all radical signs use te>-1,L>0 by variable substitution te=s-1,s>0. No numerical errors/tolerances or global/large-radius conclusions. Same existing capture controls, one short CPU process,2GiB.

## Milestone A4 — optical reciprocity and a global conformal question

Parent requested a concrete test of whether ordinary optical reciprocity supplies NAR or B's extra no-defocusing condition. The spherical radial Jacobi equation answers it without adopting wave/matter dynamics. For any positive areal r(λ) along an affine radial ray, D_e(λ)=r_e r(λ) integral_e^λ ds/r(s)² solves D''+(Ric(k,k)/2)D=0, D(e)=0,D'(e)=1. Reversing endpoints gives D_e(o)=-D_o(e) for arbitrary r''. Physical launch-angle normalization multiplies by endpoint omega, yielding the ordinary endpoint area-distance reciprocity ratio Z. It supplies no sign of Ric(k,k), no r''=0 and no complete two-way future-clock identity. Photon-number/flux/luminosity laws are not used.

The relevant metric countercheck uses q(t)=exp(Ht), H>0, in the dynamic reciprocal spherical family. On its affine radial ray t=λ,r=exp(Hλ)/H, r''/r=H², so radial null Ricci=-2H² and NAR fails. Yet D_e(λ)=sinh(H(λ-λe))/H obeys exact vertex reciprocity. This is an original-equation example, not a claim that every point-source cone shares the global spherical congruence.

This failure suggested **CNR (conformal null rigidity), UNADOPTED physical trial, mathematical conditional theorem**. Suppose the proposed additional geometry preserves all unparameterized reference null paths/cones, implemented as g=ψ^-2 g0 with ψ>0 C². This is a physical comparison hypothesis, not a Weyl gauge, not F2, and not an adopted metric modification. If g0 is connected, null-geodesically complete and has Ric0(k,k)=0 on all null vectors, B's all-frame nonnegative additional PSW1 coefficient implies Ricg(k,k)<=0. With reference-affine k,

    Ricg(k,k)=Ric0(k,k)+2 ψ''/ψ.

Thus ψ is positive concave on each entire reference-affine real line, forcing it constant on that line. All null directions span tangent, so ψ is constant globally. This uses completeness of the REFERENCE null geodesics, not completeness of g; it is a new global restriction on this trial identification, not UDT or a proof that an extra premise is necessary.

An informative allowed-domain control is ψ=cos(Hη) on the finite reference Minkowski slab |Hη|<pi/2. Then physical g=-dt²+cosh²(Ht)d⃗x², t∈R. It is not spaceform: Hubble=H tanh(Ht), acceleration a''/a=H², R=6H²(1+tanh²(Ht)). The full prepared-clock all-frame coefficient relative to flat is H²+H²sech²(Ht)|m|²>0 for each unit timelike plane (b²-m²=1). Its null Ricci is negative. All physical timelike/null geodesics are complete from conserved spatial momentum and a>=1, while the reference slab null geodesics are incomplete. Both ends have regular spacelike conformal boundaries with dψ nonzero timelike. This directly tests the theorem's domain hypothesis; it is neither a source-selected bounce nor a reference for every UDT situation. H is a free geometric parameter and this family has only a fixed-compact-patch Minkowski limit H→0, not a generic GR recovery theorem.

Cross-exposure: parent disclosed its separate conformal Weyl-scaling C2 argument after I had formed the positive-concavity route; C2 is not used in this proof. B's all-frame sign proposal is now a premise source, not an independently originated A proposal; the needed sign-to-null implication is rederived in the supplement. B's quartic profile suggested a rational asymptotic counterprofile, but no further rational example is executed or claimed because the current optical/conformal theorem-control pair answers the live question more directly.

**Check A4 predeclaration:** exact symbolic CPU identities only. Verify the generic spherical radial Jacobi reduction by formal differentiation with arbitrary positive r, the explicit sinh map and nonzero-focusing witness, conformal Ricci null contraction from original diagonal metric ψ(η)^-2 eta, and cosh scale curvature/normalization identities. Universal positive-concavity proof is analytic, not sampled. No field equation, physics fit, luminosity law or wave amplitude is computed. One process/one BLAS,2GiB virtual via existing capture, tiny output, no wall or CPU killing timeout. This is the last planned exploratory check before parent review.

A4 completion: initial capture at04:05:39UTC passed18 of19 grouped exact comparisons. The remaining mixed sinh/exp representation did not normalize under generic SymPy simplify. Preserved initial source and stdout/stderr; applied the exact sinh-to-exp identity only to that residual. Second capture at04:06:11UTC passed19/19 and saved zero residual,1.24s,50,808KiB RSS. All original-metric/geodesic/curvature checks passed initially as well. CPU slot released to parent; no further research computation planned.

Parent's subsequent caution is incorporated: CNR constancy is a necessary consequence, not sufficient to ensure full directional S after an arbitrary constant rescaling of a curved reference. Physical cosh causal completeness does not establish the founding past-asymptotic target; actual comoving history includes contraction blueshift. Supplemental source inspection and SUPPLEMENT.md record those boundaries. Initial CANDIDATE.md is unchanged. Exploration now returns the conditional theorem/control package for two fresh adversarial reviews; no budget-filling examples and no physical adoption. The unexecuted rational profile remains an untested idea only.

First fidelity-review repair: parent relayed the ambiguity of "additional" in the initial candidate's total radial Ricci statement and the stale initial source-access log. REVIEW_REPAIR.md gives the precise total-Ricci reading and dated source access, preserving initial CANDIDATE and SOURCES wording. Primary Schmidt and Abreu-Visser equations were reopened at04:09-04:10UTC; no exact earlier per-page access timestamps are invented. SOURCES was briefly updated during supplement finalization and restored when this preservation request arrived, with that sequence disclosed in the addendum.
