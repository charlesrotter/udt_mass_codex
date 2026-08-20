# G181 repair-only recovery review

The prior follow-up process exhausted its context by dumping complete documents. Review the same
authorized sealed intake again, strictly within the existing repair-only scope. Do not continue the
research and do not print any source or report longer than 40 lines.

Perform only these checks:

1. Run `verify_sealed_intake.py` and `verify_package.py` under `python3 -I -S`.
2. Independently hash every intake file before and after the three `UDT_READ_ONLY_REPLAY=1`
   executions and verify no hash changes.
3. Use short Python/AST or JSON checks—not document dumps—to verify: no third-party production
   import; 20,000 rational trials with noninteger cases; nine cross-classes; 28 executable-mutant
   entries; six separate semantic guards; 19 witnesses; seven manifest sources; unchanged landing.
4. Inspect only the repair preregistration, the prior-review adjudication, and the exact landing and
   ceiling paragraphs needed to determine whether the scientific formulas, witness set, premise
   grade, and maximum conclusion were altered. The preserved first-review materials in the intake
   are the comparison record; absence of git metadata is not itself a repair failure.

Return at most six concise bullets and exactly one leading verdict:

- `G181_REPAIR_ACCEPTED`; or
- `G181_REPAIR_INCOMPLETE`, followed by the exact numbered repair condition that failed and the
  concrete evidence of failure.

Do not derive or propose new physics, an action, source, matter model, `X_max`, observational fit,
radiative-transfer law, or signalling law.
