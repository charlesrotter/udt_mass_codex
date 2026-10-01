# TDS1 — three-spatial-coordinate extension and smoke gate

Charles's “continue” follows SMK1's explicit next step: prepare the broader
solver, smoke-test its actual scope, and measure a short workload before any
hours-long exploration. This is the next bounded implementation/validation stage.
It does not launch the proposed six-hour tranche or 24–48h extensions.

Question: can a metric evolution code with all ten symmetric metric components
and unrestricted three-coordinate spatial dependence recover exact controls and
evolve non-collinear, constraint-satisfying initial data for a short regular slab?
The comparison equation is unchanged CONDITIONAL Ric(g)=0, Lambda=0, under G312
GR FILTER ONLY. No E=Ric identification, native field-law selection, source,
carrier, physical scale, X_max, observation fit or preferred center is supplied.
Sources: UDT_DEVELOPMENT.md R9–R12N; current G312 AUTHORITY_RECORD; G316 conformal
constraint construction read under that authority. Prior science stays fixed.

## Construction and choices

Use harmonic coordinates H_mu=0 as a numerical gauge for the same conditional
equation. Derive/check its reduced metric wave equation against original Ricci;
do not use an evolution residual as the only validity test. Standard harmonic
methods and conformal initial-data methods are permitted mathematical methods.
Primary method references: Pretorius gr-qc/0407110v2, equations7–14;
Lindblom et al. gr-qc/0512093v3; Alcubierre et al. gr-qc/0305023 gauge-wave controls.
These sources do not establish UDT premises. No matter term is imported.

Evolve g and its time derivative on a supplied periodic marked three-torus.
Fourier collocation and RK4 are initial numerical choices; no filtering,
dissipation, fitted terms or constraint damping is added in this stage.
Use float64. Solve initial constraints with positive conformal factor, flat
conformal seed, nonzero constant mean curvature and explicit transverse-traceless
multi-direction tensor modes. Retain initial conformal-flatness/CMC restrictions;
they are not maintained as restrictions on the evolved metric. No spatial Killing
symmetry is imposed on the evolution code. Constant and pure-gauge metrics are
validation controls, not the explored universe or additional UDT requirements.

Pinned-by-THEORY within this conditional branch: Ric=0, Lorentz signature, exact
constraint identities, tensor transformation and gauge-reduction bookkeeping.
Pinned-by-HABIT, explicitly limited for this stage: periodic topology/coordinate
period, harmonic gauge, Lambda=0, CMC/conformally-flat seed construction. These
are supplied comparison choices, not derived physical predictions. Mode directions,
polarizations, phases and amplitudes are free-and-explored in a frozen small case
list. Mesh/step/dtype and finite time slab are declared numerical controls.

## Gates and bounded resources

1. Derive the equations and harmonic-compatible initial metric velocities; an
   actual separate-context reviewer checks signs, constraints and tensor indices.
2. Test flat, curved homogeneous/Kasner and finite-amplitude gauge-wave limits.
   Construct genuinely multi-direction initial data and independently check the
   original Hamiltonian/momentum constraints, not only the conformal solve.
3. Freeze code/cases/tolerances before the reported GPU smoke run. Check spatial
   and time refinement, original Ricci/constraint residuals, signature/finite data,
   saved outputs, and at least an explicitly marked null/clock control readout.
4. Reuse SMK1 immutable checkpoint I/O with new code/spec signatures. Test actual
   short-run restart and stops for the changed state; old smoke results alone
   cannot certify this extension. Preserve every failed run and source edition.
5. Measure a short representative workload; report memory/output/throughput and
   remaining production gates. Two actual fresh contexts review mathematics,
   numerical evidence and scope. One bounded same-premise scientific repair and
   ordinary source-preserving implementation repairs/re-review are included.
6. Return reviewed short-slab evidence or a precise unresolved blocker, plus the
   next concrete production-preparation step. Update the relevant central argument
   and coverage only to match actual evidence, then required checks/commit/push.

One GPU process at a time on the remeasured local V100, float64, initial meshes
8^3,12^3,16^3, with24^3 only if refinement needs it. At most 5 minutes summed GPU
run time in this stage; each invocation120s, peak allocated GPU memory4GiB;
total saved artifacts512MiB. CPU numerical/reviewer checks each180s/2GiB working
data; existing CUDA capture virtual-address allowance128GiB is mapping only.
Required repository audit retains its existing900s/2GiB cap. No installs,
external compute, purchases or hour-long runs. Recheck hardware before GPU use.
Stop for nonfinite/signature failure, severe original-equation/constraint error,
resource exhaustion, unresolved refinement, or a substantive review objection.
Keep diagnostics; do not silently reduce amplitudes or remove difficult cases.

Maximum conclusion: a reviewed numerical tool/short conditional history family,
with exact tested coverage. No continuum certification, long-time stability,
genericity, full solution-space census or native UDT law follows. A multi-hour
production dispatch requires the actual measured broader workload and completed
smoke gates. Missing native selection remains a distinct scientific boundary.
Protected and unrelated files remain untouched. Workspace is this package only
until the reviewed central/operational integration; CANON/registry grades stay fixed.
