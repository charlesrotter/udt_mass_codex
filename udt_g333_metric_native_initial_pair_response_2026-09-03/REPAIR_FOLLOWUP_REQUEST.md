# G333 repair-only external follow-up request

Act as a zero-context repair-only reviewer. Inspect only the corrected sealed intake. Do not edit
evidence files or continue the research.

Verify only preregistered repairs R1--R4 in `REPAIR_PREREGISTRATION.md`:

1. `H(v,v)` is explicitly typed as `gamma(Hv,v)` wherever the result is used.
2. The general vector-extension derivative is stated and the reduced pair formula requires
   `[n,v]=L_n v=0` at the evaluation point.
3. The analytic all-direction proof is separated from representative independent sampling.
4. The detached seal is limited to internal integrity and replay consistency.

Confirm that no coefficient, sign, branch, classification, topology boundary, or scientific
landing changed. Run the registered checks in a writable ephemeral copy.

Return exactly one verdict:

- `REPAIRS_ACCEPTED__G333_BOUNDED_FIRST_RESPONSE_RETAINED`
- `REPAIRS_INCOMPLETE__G333_BOUNDED_FIRST_RESPONSE_RETAINED`
- `REFUTE__G333_BOUNDED_FIRST_RESPONSE`
