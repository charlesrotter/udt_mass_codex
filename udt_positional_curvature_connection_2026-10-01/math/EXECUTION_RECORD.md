# Mathematical review execution and normalization repair

The initial source-first argument and checker were frozen before PCC1 candidate
or peer review exposure. Their SHA-256 values were sent to the parent:

* SOURCE_FIRST_ARGUMENT.md: 1fc5bb25db42292b850936ca5267cc99cc97f97bb1d728094aea15dbfcea6959
* check_geometry.py: ccb3bbcb920492d020130e1c4f653ca646ff6c4179c516df2deaa7cccf0a06a6

After freezing, the parent disclosed that its own check required a trigonometric
zero normalization repair. No parent code/output or argument was seen. The
math reviewer then received the sole scientific CPU slot and ran:

    python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_positional_curvature_connection_2026-10-01/math/geometry_check_capture python3 udt_positional_curvature_connection_2026-10-01/math/check_geometry.py

This failed after 0.783 s on the exact expression

    r*(sin(2*theta)*tan(theta)+cos(2*theta)-1)/(2*tan(theta)).

The numerator is zero by the double-angle identities. The expression arose in
an off-pattern coordinate-curvature component. No tolerance was loosened and no
assertion removed. The complete original checker and its failed receipt/stdout/
stderr remain unchanged. A separate `check_geometry_repaired.py` applies
`expand_trig` before `simplify` in the exact assertion residual normalizer.
No curvature construction, expected expression, physical assumption, output
schema or scientific claim changed. This is implementation normalization, not
a substantive repair of the mathematical candidate.

The analogous command with `geometry_repaired_capture` and the repaired checker
passed 1014 exact symbolic assertions in 1.103 s, maximum resident memory
55048 KiB. It used Python 3.10.12 and SymPy 1.13.1 as recorded by the saved output.
The wrapper enforced 2147483648 bytes of virtual address space, one CPU-thread
environment and no elapsed/CPU timeout; no GPU was used. The script writes a
small JSON output and no evolution/grid checkpoints are applicable. After the
completed receipt, the process listing showed no Python/python3/torchrun workers
and the slot was explicitly released. These assertions include dependent tensor
component identities and are not 1014 independent proofs.

Saved artifacts:

* check_geometry_repaired.py: 2679d43ac16d627e17ddf0790ea51748f47eb5d5e12645eb7fc6242307ceb515
* geometry_output.json: f715798798ec1091d8c31aa883815771a967669f10203bf3dd54c10c34ba08cf
* geometry_repaired_capture.json: b1ed4f427560e968f5b88a5b3df5172afe814d5d12302d7ca65833226f5d7714
* reused capture.py: 217cdbac5486e8a531552f4d74a15ce641299b65dafb5d58f7b60f4ba51781bc

The independent curvature code reconstructs Christoffel symbols and all 256
original-coordinate curvature components for two metric forms. Vanishing mixed
components and six sectional values support full tensor comparison. It also
contracts the static Ricci/scalar independently. Differential Bianchi was not
separately run by this checker; it follows analytically for the smooth
Levi-Civita metrics and the variable-contrast example explicitly prevents
misapplying it across two connections. The all-frame conclusion is supplied by
the algebraic argument, not finite observer sampling. Physical selection,
finite-L accuracy and UDT admission remain untested.
