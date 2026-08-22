# G211 evidence gates

Date: 2026-08-22

1. **Preregistered — PASS.** Commit `7220e71f` was pushed before outcomes.
2. **Full space or bounded scope — PASS WITH CAVEATS.** The local rank-two scalar plane is complete;
   global controls are restricted to exact G205 radial classes and conditional transfer theorems.
3. **Independent verification — PASS.** A separate Fraction implementation checks 10,000 distinct
   exact cases and 280,003 assertions without importing production code.
4. **Radial controls — PASS.** Four registered G205 profiles passed at 120 digits.
5. **Premise audit — PASS.** The 194-row verifier passed before the solve.
6. **Hostile catches — PASS.** All 31 registered mutations are caught. The first harness run stopped
   before writing because one helper mishandled repeated tokens; the registered helper-only repair
   changed no formula, target, or conclusion.
7. **Fresh external review — PASS WITH CAVEATS.** External `gpt-5.4` verified all 34 payload
   hashes and the registered no-write replay, found no refuting defect, retained the exact
   rank-two theorem, and required no repair. Universal global causal and affine claims remain
   analytic rather than independently mechanized.

Current grade: `EXTERNALLY_VERIFIED_WITH_CAVEATS__NO_REPAIRS_REQUIRED`.
