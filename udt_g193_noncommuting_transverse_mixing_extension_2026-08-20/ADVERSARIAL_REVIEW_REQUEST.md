# G193 fresh adversarial review request

## Required stance

Treat this as a cold attempt to break a bounded result, not to help continue UDT.  Inspect only the
sealed intake.  Do not edit files or extend the research.  Run only the registered no-write replay.

## Claimed landing to audit

```text
MATRIX_FACTORIZATION_AND_NO_CAUSTIC_SURVIVE_IN_DECLARED_NONCOMMUTING_SYMMETRIC_SCREEN_FAMILY
```

strictly bounded to arbitrary positive `a(eta)`, arbitrary real `mu(eta),nu(eta)`, the displayed
symmetric matrix `M`, and one supplied central completed pair.

## Load-bearing questions

1. **Typing and scope.** Are the coframe, symmetry of `M`, pair, orientation, and functions honestly
   typed?  Does the packet overstate the result as a general complete-coframe theorem?
2. **Direct tensor reconstruction.** Audit the exact inverse coframe, Christoffel/Riemann convention,
   affine ray, parallel screen, and

   \[
   \mathcal T=\tau_0I+(2M'-4M^2)/a^4.
   \]

   In particular check both `nu^2` diagonal terms, `nu'`, and the `A nu` cross term.
3. **Noncommutativity.** Verify the displayed commutator and that the frozen control genuinely
   defeats one constant diagonalizing rotation.  Check that the derivation does not nevertheless
   commute matrices silently.
4. **Affine reduction and factor order.** Verify that `D=aY` converts the affine Jacobi equation to
   `Y''+(2M'-4M^2)Y=0`, and that the ordered factorization is

   \[
   (d/d\eta-2M)(d/d\eta+2M)Y=0.
   \]

5. **Fundamental representation.** Check `L'=-2ML`, `(L^-T)'=2ML^-T`,
   `K'=L^-1L^-T`, `Y=LK`, and the affine vertex normalization.  Look specifically for a hidden
   left/right multiplication error.
6. **No-caustic theorem.** Does definiteness of `K` and positivity of `det L` prove `det D>0` on
   both sides of the vertex?  Identify any dimension, orientation, endpoint, or regularity loophole.
7. **Independent replay.** Determine whether Torch metric jets/Riemann and the SciPy matrix IVP are
   independent enough to support the exact derivation, whether the ceilings are meaningful, and
   whether all 3,961 assertions and 15 catches are honestly counted.
8. **Scaffolding audit.** Search for P1, G116, G189, transfer, fitted profiles, post-readout angular
   coefficients, `X_max`, or physical-history promotion entering the construction.
9. **Maximum conclusion.** Separate exact derivation, numerical observation, inference, and open
   scope.  Do not accept a universal no-caustic statement.

## Required replay

From the intake root run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/verify_package.py --no-write
```

## Required return

Return exactly one primary grade:

- `G193_ACCEPTED_WITH_STATED_BOUNDS`
- `G193_ACCEPTED_WITH_REPAIRS`
- `G193_REJECTED`

Give concrete algebraic and replay evidence, every caveat, and exact repair text if required.  Do
not canonize the result or continue to another family.
