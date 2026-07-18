# Arm C adversarial derivation audit

This is an isolated adversarial return for later driver/owner audit. It is not final cross-arm adjudication, canonization, or authority to modify the frozen record.

## C.0 Provenance and integrity

### Session evidence and time

- Role: fresh Arm C at `/root`, working directory `/return`.
- Model information exposed in-session: Codex, an agent based on GPT-5. No exact checkpoint, model-version string, opaque session identifier, or external run UUID was exposed.
- Local task date: 2026-07-18. Initial integrity/read phase began before substantive classification; the premise-ledger freeze was recorded before verdict assembly. Artifact assembly timestamp sampled at `2026-07-18T12:33:21Z`. Final verification time is recorded in `final_response.md`.
- No network, GPU, host repository, host home, or undeclared path was inspected. Runtime binaries were tools, not project evidence. No sub-agent or other arm was launched.

### Exact exposure census

The aggregate received manifest contains exactly 212 entries:

| Mount/package | Files represented |
|---|---:|
| Controller | 1 |
| Cold C0/C1 | 2 |
| Packet manifest | 1 |
| Stage-I Arm A package | 30 |
| Stage-I Arm B package | 16 |
| Stage-II Arm A package | 14 |
| Stage-II Arm B package | 14 |
| A1-A6 packet | 134 |
| Total | 212 |

The A1-A6 packet byte-read covered 134 files and 862,594 bytes. The two long Stage-I and two long Stage-II outer transcripts were read byte-completely and used only for provenance. Scientific authority was restricted to C0, C1, the frozen returns, and A1-A6 as directed by the controller.

### Manifest verification before analysis

1. `/manifests/UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt`
   - exact SHA-256: `010e7922423ab724467d94f6408425905fb872c5ccaebc5fa5941fc66080f2dc`;
   - exact entry count: 212;
   - `sha256sum -c` run from filesystem root: all 212 entries `OK`.
2. `/manifests/UDT_NATIVE_ACTION_STAGE2_A1_A6_SHA256SUMS_2026-07-18.txt`
   - exact SHA-256: `85776969410e6dc8bee6b1aa901331dcc139e718dbdfd28c593df3f2054408b7`;
   - exact entry count: 134;
   - `sha256sum -c` run from `/packet`: all 134 entries `OK`.
3. Stage-I Arm A `SHA256SUMS.txt`: external hash `d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19`; all 29 internal entries `OK` from `/stage1/arm_A`.
4. Stage-I Arm B `SHA256SUMS.txt`: external hash `a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92`; all 15 internal entries `OK` from `/stage1/arm_B`.
5. Stage-II Arm A `SHA256SUMS.txt`: external hash `ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a`; all 13 internal entries `OK` from `/stage2/arm_A`.
6. Stage-II Arm B `SHA256SUMS.txt`: external hash `30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45`; all 13 internal entries `OK` from `/stage2/arm_B`.

`RECEIVED_ARM_C_INPUT_SHA256SUMS.txt` is byte-identical to the 212-entry aggregate input manifest and has the expected aggregate hash.

### Ordered-read and immutability statement

The mandated order was followed: controller; exact C0; exact C1; complete Stage-I A then B packages, including D0-D5, scripts, outputs, driver audits, manifests and transcripts; complete Stage-II A then B packages, including separate D6 returns, censuses, scripts, outputs, launch records, audits and transcripts; then all 134 A1-A6 files in received-manifest order, including banners, README, source and outputs. Duplicate packaged C0/C1 copies were byte-compared to `/cold` and were identical. All input mounts remained unchanged. Writes were confined to `/return`.

## C.1 Adversarial map and premise ledger

This section was fixed before substantive verdicts. Its rule is symmetric: an attractive candidate is not a countermodel until it passes the whole applicable foundation, and an attractive classification theorem is not unique UDT dynamics until every premise of its class is forced.

### Completeness dimensions

| Dimension | Complete foundation supplies | It does not supply |
|---|---|---|
| Fields | Positional comparison data; a CSN conformal class; a conditional reciprocal block; reopened conditional S2 branch | Full transverse/time-live metric, independent status/weight of phi, carrier ontology, multiplier/coframe census |
| Action | Requirement that a native pre-scale law respect CSN | Stationarity, locality, covariance, polynomiality, invariant inventory, coefficients, derivative order |
| Equations | Kinematic composition/reciprocity identities | A distinguished update law, Euler operator, source equation or constraint propagation law |
| Solution/domain | Finite mirrored cell; observed realized nontriviality; phi=0 remains a mathematical configuration | Complete manifold/slice, regularity class, existence theorem, proper time-live volume, realized full solution |
| Boundary data | Static phi is odd at the seal, so phi=0 and normal derivative free; no spatial infinity as native input | Other-field data, corners, differentiable boundary functional, primitive, reference subtraction, charge normalization |
| Topology | Finite mirrored setting; conditional S2 maps and historical topology are evidence only | Full spacetime topology, quotient versus one-copy/interface ontology, carrier topology through degeneracies |
| Dynamics | Working global self-consistency principle | Local dynamics, hyperbolicity/ellipticity, constraint algebra, time variable |
| Branches | H2 hierarchy, carrier-agnostic branch, reopened S2, universal Xmax posit, global-density selection | A selector among C2, EH, scalar, foliation, nonlocal, boundary or nonvariational branches |
| Stability | Historical S2 stability only within its stated flat-static numerical model | Time-live stability of any completion, Bach/EH stability, solution persistence under counterfamily deformation |
| Regime | Controlled expansions allowed only after exact equations; finite cell is primary | Weak-field parameter, large-cell hierarchy, uniform remainder, asymptotic limit |

### Foundation premise ledger

- **FOUNDING:** positional dilation; Reciprocal-c Identity; dual UDT Reciprocity; Common-Scale Neutrality.
- **POSIT:** difference/composition/reversal, positive regular comparison and positional-relativity formalization.
- **DERIVED / CONDITIONAL:** `uv=1` from the supplied dual pairing; reciprocal exponentials from additive composition plus regularity.
- **CHOSE / POSIT:** sign/unit of phi, Lorentzian quadratic readout, CSN representative, and slot-to-gradient identification.
- **OBSERVED:** realized nontrivial dilation; the trivial `phi=0` configuration remains mathematically allowed.
- **CANONIZED / BINDING:** finite mirrored cell and static seal parity `phi=0`, normal derivative free; spatial infinity is not native input.
- **WORKING / POSIT / REOPENED:** round S2 carrier; the displayed E2+E4 is only a conditional static branch.
- **WORKING / POSIT / OPEN:** one universal unattainable Xmax exists; its origin, formula, normalization and value remain open.
- **WORKING:** realized global bootstrap and an extremely narrow matter-bearing proper-total-density window; no center, width or local coupling is supplied.

### Classification standard

- `CONFIRMED-FORCED`: the exact claim follows from the complete applicable ledger or, for an explicitly conditional theorem, from every named premise without adding another premise.
- `ACTUALLY-CHOSEN`: the result is valid only after a field, action, covariance, representative, weight, domain, boundary, topology or regime choice.
- `CIRCULAR`: a discarded/full equation, target structure or conclusion is restored by assuming it.
- `IMPORT`: a GR/standard equation, asymptotic construction or other physics is used as UDT authority rather than scoped reference.
- `UNDETERMINED`: neither the claim nor its negation is forced after whole-foundation testing.

### Symmetric falsification tests

For a uniqueness/forced claim, Arm C asks for a distinct completion satisfying every applicable gate: H2, both reciprocal principles, CSN, realized nontriviality while retaining phi=0, finite mirror/parity, reopened-carrier status, Xmax/bootstrap/density, complete equations, an actual solution, differentiable boundary data and declared variation domain. If only a compatible construction is available, every remaining check is bounded and the status is `CONDITIONAL-COMPLETABLE`, not a completed refutation.

For an underdetermination/open claim, Arm C adds the strongest coherent selector: coordinate nonpreferencing interpreted as covariance, CSN as local Weyl symmetry, metric-only fields, locality, parity, derivative-order bounds and known classification theorems. Each added premise is then tested against C0/C1. A unique conditional class defeats broad rhetoric but not foundation-level underdetermination unless those premises are forced.

## C.2 Claim audit

The exhaustive claim-by-claim audit is `ARM_C_CLAIM_MATRIX.tsv`. It covers both arms' D1 maps, every load-bearing D2 construction, all Q1-Q3 D4 rows, both D6.2 audits, carrier-covariance routes, mass/virial tests, revisions, sign audit and the historical C2/EH/variation/boundary/global claims used by D6.

Major results are:

1. **Kinematics survives.** Both arms correctly locate `uv=1` in dual Reciprocity, not Reciprocal-c alone, and correctly keep exponentials conditional on additive depth, positivity and regularity. Verdict: `CONFIRMED-FORCED` within C1's supplied faithful formalization.
2. **Representative discipline survives.** The reciprocal metric product is representative-dependent; it gains `Omega^4` under common Weyl rescaling. Verdict: `CONFIRMED-FORCED`.
3. **Action underdetermination survives, but the countermodel proof is weaker than both arms imply.** CM0, C2, X2, generic scalar, foliation and nonlocal sketches do not each pass the full solution/global/boundary gates. They establish non-entailment or conditional families, not two solved complete universes. Verdict on foundation-level action selection: `UNDETERMINED`.
4. **Carrier completion underdetermination survives.** The restriction-kernel argument rigorously shows a static functional cannot fix terms vanishing on the static slice. Complete-foundation admissibility and solution persistence of arbitrary kernel terms are additional checks. Verdict: `UNDETERMINED`.
5. **Arm-B algebra required repair.** Frozen Stage-I `S_rel` omitted the overall minus sign under its `(-,+,+,+)`, `E=-integral L_static` convention; `S_fol` requires `gamma=-kappa4` with its written electric sign, or the sign must flip for positive `gamma`. D6 repairs both. Verdict: `CONFIRMED-FORCED` on the correction; the original completions were `ACTUALLY-CHOSEN`.
6. **Variation-order warnings survive.** Hard constraint, multiplier, unrestricted-then-restrict, restrict-then-vary and normal equations are inequivalent without an equivalence theorem. Verdict: `CONFIRMED-FORCED`.
7. **Finite-cell charge remains open.** Seal parity fixes a value, not a primitive, reference or normalization. Verdict: `UNDETERMINED` for a native mass; boundary nonselection is `CONFIRMED-FORCED`.
8. **Carrier covariance does not presently force a source weight.** `rho+S=2rho4` is exact for the chosen minimal covariant completion and unrestricted metric variation; reciprocal-tangent variation gives a directional source. Verdict: conditional identity `CONFIRMED-FORCED`, native source `UNDETERMINED`.
9. **The D6 priority no-go is too strong.** Both arms prove the current materials do not put mass ahead of Q1, but do not exclude a shared static sourced sector across inequivalent full actions. Verdict: `UNDETERMINED`.
10. **Three-part mass/virial bookkeeping survives exactly.** It does not prove EH, a boundary theorem or a controlled limit. Verdict: `CONFIRMED-FORCED` given the named premises.

## C.3 Complete-foundation countermodel admissibility audit

`ARM_C_COUNTERMODEL_MATRIX.tsv` gives separate columns for every gate. No displayed Stage-I candidate earns `COMPLETE-ADMISSIBLE` on the supplied record. That is a material qualification: incomplete sketches do not, by themselves, defeat a uniqueness theorem.

### No-action / CM0

Arm A's CM0 preserves kinematics but supplies no update law, full equations, solution notion, carrier/global density realization or Xmax closure. It is `INCOMPLETE`. A zero-action completion with separate coordinate-neutral nonvariational/global selection equations is logically compatible and is `CONDITIONAL-COMPLETABLE`; the missing equations and nontrivial finite-cell solution are explicitly bounded. Thus CM0 proves only that stationarity is not stated, not that a complete no-action universe was constructed.

### Conformal C2 / Weyl / Bach

`sqrt(-g) C^2` passes exact four-dimensional CSN and has Bach bulk equation under unrestricted metric variation. It still needs reciprocal-constraint implementation, finite-cell fourth-order boundary/corner data, matter trace/coupling, a nontrivial solution, stability and global Xmax/bootstrap/density closure. WR-L being Bach-flat or conformally flat is an admission result, not selection or global completion. Status: `INCOMPLETE`; the named class is `CONDITIONAL-COMPLETABLE`.

### Scalar X2

For weight-zero independent phi, `sqrt(-g) X^2` is exactly Weyl invariant in four dimensions and has trace-free stress. This defeats C2 uniqueness only after adding phi as an independent field. The positional reciprocal relation does not decide that status, and no coupled nontrivial finite-cell solution is supplied. Status: `INCOMPLETE`.

### Conditional EH / Lovelock routes

The Lovelock route needs unrestricted metric-only fields, 4D local diffeomorphism covariance, at-most-second-order metric equations and minimality. Exact pre-scale CSN does not admit volume or EH densities; EH therefore needs a post-scale representative and emergent normalization. Lambda, G, boundary/corner completion and finite-cell reference remain free. H3 additionally uses asymptotic-flat local-room data, so it is `INADMISSIBLE` as a complete native-cell countermodel while remaining a legitimate scoped comparison.

### Illustrative S2 completions and counterfamilies

The corrected minimal covariant completion passes its static reduction, but L2 with constant xi is not pre-scale CSN; a compensator or post-scale representative is required. The foliation family exposes free time coefficients but adds a preferred time structure and has no time-live stability/solution proof. Both are `INCOMPLETE`. The `S_min+ker(R)` affine statement is exact as a restriction theorem. It becomes countermodel-forceful only after a completed base solution and an admissible kernel deformation with preserved differentiability and solution existence are provided.

### Conformal weights

In four dimensions, measure has weight `+4`; EH has constant-scale density weight `+2`; C2, scalar X2 and carrier F2 have weight zero; the constant-coefficient carrier L2 density has weight `+2`. These necessary weight checks are exact. Local Weyl transformation of R contains additional derivative terms, so the EH obstruction is stronger than constant scaling alone. A compensator of weight `-1` can repair L2, but its field/action/solution are new premises.

### Constraint and variation gates

The reciprocal relation can be hard-built, imposed by multiplier, imposed after unrestricted variation, or used only as a readout restriction. Hard/multiplier variation gives the tangent projection and can lose normal equations. Imposing the missing normal Einstein equation by hand is circular. A least-squares normal equation can also have stationary points that do not solve the original equation. No arm derives a unique domain.

### Total derivatives and boundary primitives

Adding `dF(phi)/dr` leaves the bulk Euler equation unchanged and shifts canonical boundary momentum by `F'(phi)`. Even with `delta phi=0` at the seal, the momentum, on-shell primitive and charge assignment can differ. Reciprocal-spherical EH is itself a radial total derivative after early restriction. Reference subtraction and normalization are independent choices. These become `CONDITIONAL-COMPLETABLE` counteractions after a complete base boundary problem is specified.

### Global/nonlocal candidates

A bilocal relational action is not forbidden because locality is open, but no concrete CSN-covariant kernel, mirror behavior, existence theorem or bootstrap root is supplied. A fitted average-density local coupling is explicitly `INADMISSIBLE`. A separate global constraint on proper density/Xmax is `CONDITIONAL-COMPLETABLE`, but proper volume, native charge, root existence/uniqueness and the local/global variation must be constructed.

## C.4 Strongest unique-action counter-derivation

### Conditional C2 route

The strongest route is:

1. Four time-live dimensions: supported by the question and carrier-completion frame.
2. CSN interpreted as exact local Weyl gauge symmetry: forced for a native pre-scale law.
3. Full coordinate nonpreferencing interpreted as local diffeomorphism covariance: **not forced**; C1 explicitly leaves covariance open.
4. Unrestricted metric as the only independent geometric field: **not forced**; C1 leaves scalar/coframe/multiplier/readout branches open.
5. Local polynomial parity-even bulk: **not forced**.
6. No dimensionful inserted constant and lowest nontrivial derivative order: absence of a primitive scale supports the first phrase, but it does not force polynomiality or the lowest-order truncation.
7. Curvature-square inventory: under steps 1-6, the parity-even local basis reduces to `p C^2 + q Euler`; modulo topology/boundary and normalization, the bulk equation is Bach.

The algebra succeeds. The foundation-level derivation fails first at steps 3-5 and again at step 6. It also fails to select normalization, boundary completion, source, solution or stability. Therefore the strongest result is a `UNIQUE-CONDITIONAL` bulk class, not a unique UDT action.

### Conditional EH/Lovelock route

Assume unrestricted metric-only variation, local 4D covariance, at-most-second-order metric equations and Lovelock minimality. The bulk is EH plus Lambda, topology and boundary terms. This route fails earlier against exact pre-scale CSN: EH needs a physical representative and dimensionful coefficient. Even post-scale, the foundation does not fix Lambda, G, GHY/corners, reference subtraction or a solution. It is a valid conditional comparison, not forced UDT.

### Strongest no-go within a narrow class

If one simultaneously demands exact pre-scale CSN, metric-only fields and at-most-second-order non-topological metric equations, there is no nontrivial EH-like local bulk in the admitted inventory. This is a class-scoped no-go, not a universal no-action theorem: C2, scalar/compensator, higher-derivative, nonlocal, coframe and global routes remain.

## C.5 Sector audits

### (a) C2 sector

- **Weights:** exact as in C.3 and `cas_armc_unique_action_weights.py`.
- **Bach variation:** unrestricted variation gives a trace-free fourth-order bulk equation. A reciprocal ansatz imposed before variation can lose normal metric equations.
- **Source/constraint handling:** exact Weyl invariance requires a compatible trace condition. Minimal S2 L2 with fixed xi is not pre-scale conformal; coupling it directly to Bach dynamics needs a compensator, post-scale phase or explicit breaking. `rho+S=2rho4` is not a Bach source equation.
- **Boundary:** a fourth-order metric action normally requires more boundary data or a boundary completion than phi seal parity supplies. Euler/topological additions preserve bulk Bach equations while changing finite-cell action/charge accounting.
- **Verdict:** conditional bulk classification survives; complete action and finite-cell physics remain open.

### (b) EH sector

- **CSN tension:** EH selects a representative/scale and is not exact pre-scale Weyl invariant.
- **Lovelock premises:** metric-only, locality/covariance, second-order equations and minimality are added, not derived from positional comparison.
- **Boundary completion:** an EH Dirichlet branch needs its boundary/corner completion; the canon does not choose its data, reference or orientation.
- **Mass:** the finite-cell Hamiltonian/covariant-phase-space generator and normalization must be derived. Asymptotic ADM-like normalization is not native input.
- **Verdict:** conditional reference/possible post-scale branch only.

### (c) Carrier covariance

- **Signs and factors:** with `(-,+,+,+)`, `F_mn F^mn=B-2E/N^2` under zero shift and ordered antisymmetric sums. The corrected covariant action has an overall minus sign and maps to a foliation action with a positive electric quartic term.
- **Weights:** L4/F2 is pre-scale conformal in four dimensions; constant L2 is not.
- **Measure/time:** `sqrt(-g)` and Lorentz time are choices; a foliation time and free kinetic coefficients share the same static energy.
- **Representative:** lapse-longitudinal cancellations occur only in a selected reciprocal representative/decomposition.
- **Source:** unrestricted metric variation gives `rho+S=2rho4`; reciprocal tangent variation gives `rho+p_parallel=2(rho2_parallel+rho4_parallel)`, generically different. Direct weights change every coefficient.
- **Verdict:** covariance classifies a chosen completion; it does not force the native weight or source.

### (d) Variation domain

- **Vary then restrict:** retains all unrestricted Euler equations evaluated on the reciprocal surface.
- **Restrict then vary:** returns only the tangent projection; reciprocal-spherical EH becomes bulk-empty.
- **Multiplier:** imposes the constraint but, after eliminating the multiplier, can still yield only the tangent difference rather than both unrestricted equations.
- **Normal equations:** least-squares stationarity is not logically equivalent to the original equations without rank/zero-residual conditions.
- **Lost equations:** restoring a discarded normal equation because it is Einstein's equation is `CIRCULAR`/`IMPORT`.

### (e) Boundary charge

- The native cell is finite; spatial infinity is excluded.
- Odd parity fixes phi and its variation at the seal, not normal derivative, other fields, topology or a primitive.
- Total derivatives leave bulk equations invariant while shifting canonical momentum/on-shell action.
- Exact quotient, one-copy endpoint and matched interface have different boundary variations.
- Reference subtraction, orientation and normalization remain independent.
- No raw flux in the record is a forced gravitational mass.

### (f) Three-part mass/virial test

1. **Source identity:** under minimal covariant S2 plus unrestricted metric variation, `rho+S=2rho4`; under conditional EH lapse dynamics this gives `M_N^(0)=2E4` in the controlled weak branch.
2. **Finite-cell identity:** `E4-E2=B_boundary+W_res`, hence `M_N^(0)=E2+E4+B_boundary+W_res`.
3. **Controlled closure:** `M_N^(0)=Ecarrier` only along a specified sequence for which both boundary and residual vanish while the weak expansion remains uniform.

For an exact critical point only `W_res=0` follows; `B_boundary` remains. The corrected L=6 continuum gap near `-2.7%` rules out current finite-box `E2=E4`. Boundary stress is a strong lead, not a proved local surface theorem. The old `0.05%` centered-operator result is superseded provenance because its operator has a Nyquist null; it is neither evidence nor a criterion.

## C.6 Strongest counter-derivation against each major conclusion

| Major conclusion | Strongest attack | Result |
|---|---|---|
| Reciprocal kinematics is forced | Try ordinary `u=v` or arbitrary exponent slopes | Fails full dual Reciprocity except the trivial intersection; exponential orientation/unit remain chosen |
| No unique action | Exact CSN plus 4D metric-only local parity-even lowest curvature-square classification | Produces unique-conditional C2 modulo Euler/boundary, but class premises and completion are unforced |
| No action existence is forced | Treat global self-consistent solution language as implicitly dynamical | It may imply an update/solution concept, but not stationarity; CM0 must be completed rather than assumed |
| Fields/domain are underdetermined | Interpret coordinate nonpreferencing as full covariance and phi as metric-only | C1 explicitly leaves covariance and off-shell field status open |
| Carrier is underdetermined | Treat the free angular block as selecting S2 | A free slot does not select its occupant; A3 provenance says S2 is a posit |
| Static energy does not fix 4D completion | Demand Lorentz covariance and minimal coupling | Narrows to a corrected minimal completion, but covariance/minimality/representative remain extra and L2 conflicts with pre-scale CSN |
| Source weight is underdetermined | Use unrestricted stress identity `rho+S=2rho4` | Exact only on one variation/completion; reciprocal tangent and direct-weight channels differ |
| Boundary charge is open | Use EH Hamiltonian or Euler/one-copy primitive | Requires a chosen action/domain/reference/normalization; topology branches differ |
| Q1 must precede static mass | Argue source equation and generator belong to full action | Shows current route incomplete, not that inequivalent full actions cannot share one forced static sourced sector |
| Mass equals carrier energy | Combine source identity with Derrick virial | Fails at finite boundary/residual; only a separately controlled closure yields equality |
| C2 is viable native dynamics | Bach equation and WR-L admission | Boundary, matter trace, modes, stability and global solution remain open |
| EH is native | Lovelock uniqueness and familiar mass | Adds unforced premises and conflicts with exact pre-scale CSN until representative/scale selection |

No attack derives a unique complete action or defeats the broad underdetermination result. Conversely, no supplied candidate is a fully solved complete-foundation countermodel. That double qualification is the central Arm-C finding.

## C.7 Smuggle audit

The full locator-level list is `ARM_C_SMUGGLE_LIST.tsv`.

Arm A is generally explicit about choices. Its material weakness is countermodel completeness: CM0, C2 and X2 are treated as admissible enough to defeat uniqueness without a full realized solution/global closure. Arm B has the same completeness issue and two concrete Stage-I convention errors repaired in D6. Both D6 returns overstate the claim that a scoped static mass route can never precede resolution of full-Q1 uniqueness.

Historical GR imports are distinguished from legitimate reference work:

- Legitimate: Lovelock/EH as a named conditional classification; H3 as a scoped local-room comparison; Schwarzschild or asymptotic methods as reference only.
- Import: reinstating unrestricted Einstein equations after reducing EH to a total derivative; using asymptotic-flat mass as native finite-cell normalization; treating GR vacuum form as derived UDT without a native action.
- Circular: setting the discarded normal equation to zero by hand; using a desired boundary primitive or mass identity to select the action.

The A6 README firewall is binding: all archive scripts certify encoded algebra only. Superseded field-equation and centered-operator records were not promoted.

## C.8 Runnable algebra inventory and certification limits

All five original Arm-C scripts compile, run offline, exit zero and print unambiguous PASS summaries:

| Script | Result | What it certifies | What it cannot certify |
|---|---|---|---|
| `cas_armc_unique_action_weights.py` | PASS 11/11 | 4D Weyl exponents; C2/Euler coefficient identities; conditional one-bulk-direction classification; EH/CSN scale tension | Class premises, local Weyl derivative analysis in full generality, boundary law, solutions, physical adoption |
| `cas_armc_carrier_covariance.py` | PASS 8/8 | Correct S_rel/S_fol signs and mapping; ordered factors; static kernel; traced/directional sources; direct-weight freedom | Carrier selection, representative, covariance, stability, boundary/global solution or mass |
| `cas_armc_variation_domain.py` | PASS 6/6 | Tangent projection, lost normal equation, multiplier elimination, normal-equation false-stationarity witness | Continuum constraint qualification, gauge and boundary equivalence |
| `cas_armc_boundary_charge.py` | PASS 5/5 | Total-derivative bulk invariance and momentum shift; reciprocal EH primitive; reference/normalization freedom | Differentiable gravity boundary action, topology, charge selection |
| `cas_armc_mass_virial.py` | PASS 5/5 | Conditional source identity and three-part bookkeeping | EH, numerical gap measurement, boundary theorem, exact criticality, controlled limit or physical normalization |

The matching `_out.txt` files are exact captured executions. Historical and prior-arm scripts were inspected under their stated limits and were not copied or wrapped as Arm-C proof.

## C.9 Self-audit and stop line

- No premise was promoted because a symbolic script passed.
- No locality, covariance, derivative order, polynomiality, analyticity, topology, boundary data, solution existence, stability or regime premise was silently added.
- No incomplete candidate was labeled `COMPLETE-ADMISSIBLE`.
- The C2 and EH attacks were pursued to their exact failure points rather than dismissed by preference.
- The S2 sign/factor audit independently reproduces the Stage-II B correction.
- The finite-cell boundary/residual terms remain explicit; no superseded numerical match is used.
- All input manifests are reverified after artifact completion in `final_response.md`.

**STOP LINE: Arm C stops with this adversarial return for later audit. It does not perform final cross-arm adjudication, canonization, GPU work, another-arm launch, repository reorganization, or any mutation of frozen inputs.**
