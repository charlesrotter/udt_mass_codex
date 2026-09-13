# CSS3/5 direct implementation, numerical repair and artifact review

Scientific/implementation verdict: **VERIFIED-WITH-CAVEATS, REVIEWED CONDITIONAL,
UNPROMOTED**. No scientific candidate repair or narrowing is required. The declared
numerical sky-chart coverage repair is accepted. Combined final prose/navigation
fidelity remains a separate later stage.

The reviewer directly read the complete parent step_03/check_evolving.py and the
unchanged reused NTB1 discover_beams.py AFTER independently implementing and running
full affine8 geodesics. The parent retains complete spatial field/Hessian terms,
correct current-epoch source covector and beam ruler, the changing-source-time
-V_e term, and actual reverse propagation with source angular covector factor
omega_o ell_o. Its frozen control passes actual te to all field/Hessian calls and
uses the frozen target lapse/sky, without borrowing a full-history reception clock.
The initial-time and stationary formulas agree with direct metric derivation.
Parent reuse is correctly labeled shared-code regression; source import does not
establish independent derivation. This review's affine solver imports none of it.

The initial parent run preserved a true finite numerical failure: positive-x sky
chart q1 hit its imposed upper bound8 at epsilon0 and later emission. Saved
endpoint_diagnostic.stdout showed q1=8 with residuals.0061604497,.0708307160,
.1282332551 at s=.4,.8,1.2. The previously saved independent affine solutions
had q1=8.11340901599,9.36820954472,10.58407544793. Thus valid solutions of the
same fixed-endpoint problem lie outside the old numerical search box. Enlarging
both q bounds from8 to32 retains the same chart/family/unknowns and is an authorized
same-premise numerical coverage repair. It is not a physical boundary change,
fit to observations or nonexistence result. Repair is outcome-exposed, as disclosed
in parent REPAIR_CONTRACT.md and this review's COMPARE_CONTRACT.md.

A direct byte-text diff between preserved check_evolving_initial.py and current
check_evolving.py shows exactly one changed line: the bounds. Source metric,
endpoints, amplitudes, clock schedule, initial guess, time window, evaluation cap,
ODE/root tolerances and every guard remain identical. Parent REPAIR_FREEZE.json
records the replacement implementation before confirmation. Original failed
capture, diagnostic and initial code remain available.

Parent repaired capture started2026-09-13T00:20:12.654121+00:00, exited0 in
26.630071940016933s, maxRSS117,024KiB, limits180s/2048MiB. It reports PASS with all12
full/tighter/frozen cases and declared derivative/reversal/axial/event/calibration
checks. The reviewer did not treat this PASS as independent proof.

The artifact comparison actually read the saved parent output and independently
computed sources. `parent_comparison` exited0 in.0540672930656001s, maxRSS31,244KiB.
All336 comparisons pass: all12 full and tighter cases compared for te,to,proper
arrival clock,R,both skies,spatial momenta,beam maps/widths/areas; all12 independent
frozen stationary cases compared for timing,R,skies,widths/areas; all3 full-event
durations/means/initial-pulse errors and the3 parent reverse areas compared with
this review's actual backwards full-affine propagation. Maximum scaled central
error2.8056283166907242e-12; maximum scaled beam error3.158129026605949e-8.
This corroborates finite readouts under the frozen comparison thresholds2e-7 and
2e-6. The larger beam tolerance accounts for independently converged finite-angle
differentiation. Shared scipy/Bessel/FLOAT64 limits remain.

Additional independent frozen capture: `frozen_independent`, all12 cases PASS,
exit0 in.5448482140200213s, maxRSS80,668KiB. Its separate affine Hamiltonian sets
all inverse-metric time derivatives to zero while retaining full frozen spatial
derivatives. Conserved p_t and stationary lapse ratio agree. Each is one per-pulse
comparison metric, not a single coherent alternative evolving history.

Mutation-audit warning sent to parent: the script intentionally has a final
`hostile mutation survived intended guards` exception. Nonzero exit alone cannot
show a hostile variant was caught. Each mutation's saved failure must identify
the intended guard rather than this sentinel. This warning concerns evidence
interpretation, not the correct unmutated implementation. All four completed saved
mutations were subsequently inspected: source_epoch failed actual_source_frequency
(.2596166255639776 vs2e-12); missing_initial_flow failed changing_initial_time_clock
(.6350836907124171 vs2e-7); reverse_frequency failed same_segment_area_reciprocity
(.5035783692068871 vs2e-7); beam_epoch failed endpoint_beam_rank_identity
(.061357899410104465 vs2e-7). None reached the sentinel. These are actual intended
guard catches, not evidence inferred from nonzero exit alone.

Final combined text must preserve the initial solver failure, outcome-exposed
repair, finite diagnostic status, exact local quantifiers, UNPROMOTED dependencies,
FILTER ONLY equation authority, jointly rescaled protocol and missing physical
light/native pair/flux/cosmological adoption. No stronger claim is reviewed here.
