# G252 repair-only follow-up request

Verify only the preregistered sealed-source repairs R1–R5 and the unchanged bounded scientific
landing. Do not continue the research.

Required checks:

1. verify every fresh-intake payload hash;
2. confirm `80581067` froze the repair before implementation;
3. run all four registered no-write replays from the sealed intake root;
4. verify production and independent source resolvers accept exactly one repository or sealed copy
   with the registered hash;
5. verify the package catches missing, ambiguous, and mutated source layouts;
6. confirm saved scientific outputs and the bounded landing are unchanged;
7. report `REPAIRS_ACCEPTED`, `REPAIRS_INCOMPLETE`, or `SCIENTIFIC_LANDING_CHANGED`.
