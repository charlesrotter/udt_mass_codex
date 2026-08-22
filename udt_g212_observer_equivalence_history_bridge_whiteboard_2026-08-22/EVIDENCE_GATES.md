# G212 evidence gates

1. **Preregistered:** pass. Competing landings and T1--T6 were committed and pushed at `8c7a0b5c`
   before synthesis.
2. **Bounded scope:** pass. This is a no-solve exact whiteboard over G129--G130, G171, G176, and
   G211, plus a conditional constant-curvature control. No global physical-history claim is made.
3. **Independent verification:** pass with caveats. Three independently tasked agents reconstructed
   the relational-state, anchor/tomography, and differential-geometric/no-go arguments. A separate
   exact SymPy replay checks the finite-dimensional algebra, and a dependency-free `Fraction`
   implementation checks independent random rational instances. The universal geometric
   implications remain analytic rather than mechanized over all metrics.
4. **Premise audit:** pass. The 195-row current premise verifier passed before the whiteboard.

Maximum grade: `VERIFIED_WITH_CAVEATS__EXACT_RECONCILIATION_AND_CONDITIONAL_CONTROL`.
