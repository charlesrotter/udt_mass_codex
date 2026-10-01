# One bounded resolution repair — outcome-informed and source-preserving

The original65 PASS/13unqualified split and all234fields remain fixed. Fresh
saved-field diagnosis reproduces the original failures. N24coarse→half changes
the computed Ricci tensor by about4.07e-9 axially and1.13–1.34e-8 obliquely,
comparable to N32coarse residuals, while N24oblique spatial residuals persist.
This motivates reducing evolution-time contamination on both meshes. It is not
a promise of PASS, evidence of a physical singularity, or a measured RK4 order.
The independent diagnosis and its controls own exact numbers and coverage.

Execute exactly26 additional numerical controls on the existing13maximum-
amplitude datasets: N24quarter and N32half. Reuse each original initial NPZ
byte-for-byte. Derive N24quarter from N24half by halving cfl and max_step_ticks;
derive N32half from N32coarse by the same two changes. Everything else, including
dt_min, endpoint, windows, constraints, dimensions and equations, is unchanged.
No additional physics, parameter dataset or spatial mesh is introduced.

The repaired candidate triple is oldN24half, newN24quarter, newN32half. State
explicitly that its baseline differs from the original triple. Keep original
Ricci/ADM2e-5, final g/v2e-7, and center spatial10fold-or-both<1e-8 criteria;
retain all original five-point Ricci slices and sixth/eighth center restrictions.
Compare the same common8³ events. No tolerance, sampling criterion or outcome
is silently replaced. Do not erase an original FAIL by relabelling its fields.

Use the byte-identical TPS1 worker, supervisor and authenticated assembler.
New manifests/specs and maps live under diagnosis; new immutable runs are under
runs/refinement. First execute oblique_a5_p0_r0's two refined controls and stop
at that case boundary. Check actual original equations/constraints, new step
schedules, capture/source/schema/output/checkpoint correspondence before the
remaining24. Reuse actual earlier interrupt/restart tests because executable,
mesh and checkpoint protocol are unchanged; this pair additionally checks the
new numerical-control workload. Record omissions, not transferable certification.
An inconclusive refinement remains a diagnostic; a source/equation/resource
failure stops execution for review. No second repair cycle follows this26run set.

Runtime: measured TeslaV100-PCIE-32GB,32768MiB total,8MiB idle and no compute
process before dispatch; oneGPU,float64,8GiB allocated ceiling. No elapsed-time
or CPU-time cutoff, including wrappers; manual signalling/checkpoint controls
remain. Original per-case output caps stay256MiB(N24)/512MiB(N32). These sum to
9.75GiB over26runs. Uncompressed three-window extraction plus headers is under
4.1GiB; reserve1GiB for diagnosis/clock/control artifacts. Current production
and diagnostic use is44.822GiB, leaving19.178GiB under the unchanged64GiB global
ceiling. This conservative workflow reservation is below that headroom. Roots
must not overlap in the unchanged supervisor's accounting. No duplicate initial
states. Host disk has about690.7GB available, not a license to exceed64GiB.
CPU checks: at most2concurrent scientific processes,2GiB each. Check actual
storage before each phase. Existing finite case/memory/output/numerical/manual
stops remain. Raw data stay local and ignored; bank compact versioned evidence.

Clock characterization uses the original frozen late-window origins, four
initial directions, query times and2e-7 comparison/null limits. Finish all234
original readouts with original field-qualification labels. Also compute the26
refined readouts to assess the new candidate triples. Keep the original frozen
30dataset independent Hamilton subset on the oldN24half anchor; that anchor is
unchanged. Never use a desired sign as a gate. A clock PASS cannot independently
qualify a field. Unqualified readouts remain explicitly diagnostic.

After the26control cases and fixed checks, return the actual narrowed result
or remaining numerical ambiguity, with scientific limits and fresh separate
review. No further refinement, new parameter family, equation, scale or native
UDT selection is authorized by this numerical repair. Saving remains distinct
from acceptance; no registry grade or CANON edit.
