# Exposed parent implementation-repair review

2026-10-03, actual context `/root/esr_math`, same inherited model. This addendum
closes the parent-check inspection left pending in EXPOSED_REVIEW.md. The
scientific candidate remains SHA-256
9828c44c3b89d6b9f6f9f83f98e69a127dfc551e2d65a5c48587cd3b4fb2f59c.

I inspected the initial failure stderr, IMPLEMENTATION_REPAIR, REPAIR_FREEZE,
the full repaired script, its plan, its 16 saved numeric records and receipt.
I compared original/repaired scripts directly: exactly three structural equality
assertions became exact expanded polynomial-difference comparisons. No formula,
case, tolerance or scientific claim changed. I matched every REPAIR_FREEZE hash,
the successful stdout/stderr against receipt hashes, and the stdout summary
against PARENT_CHECK_RESULT excluding its separately saved case array.

The first failure is a genuine expression-tree/canonicalization failure rather
than a counterexample. The negative control Q''=12 retains T^2/4, so the repaired
comparison does not erase the defect it is intended to detect. My independent
source-first exact coefficient check already obtained the same unrestricted
polynomial identity and the correct Q''=14 before seeing either parent script.

The repaired capture returned0: 11 exact assertion groups,16 signed original-
incidence cases at80 digits, a separate flat control and6 unused-side routing
values. Actual recorded maximum original-or-identity error is at most
8.44e-81, below the frozen1e-65 gate. All records have positive p,q and ordered
future first/later times. The source incidence and derivatives agree with my
explicit signed ambient derivation in EXPOSED_REVIEW. The initial root is solved
before the return; Q is used only for comparison, not for generating either
root. This is a sound bounded control, not a tensor-classification proof.

Small method-label correction: PARENT_CHECK_PLAN says "40 Newton iterations";
the script calls mpmath.findroot with two initial values and no solver keyword,
which uses its default secant solver. I directly inspected the installed
function signature, whose solver default is 'secant'. The actual bound is40 root-solver steps
per call. This labeling issue has no effect on equations, saved roots, residuals,
resource ceiling or the analytic theorem; preserve the frozen plan and record
the precision correction in final evidence narration.

I did not rerun the parent's script, which writes its own result file. My one
allowed independently authored short check is already captured source-first.
Receipt/hash inspection is correspondence verification; the independent direct
Taylor/tensor check and displayed argument carry my mathematical review.
No source-first files, old candidate, failed output or source evidence was
modified by this review. Verdict remains VERIFIED-WITH-CAVEATS within the
declared conditional locally symmetric PSW scope; final integration map pending.
