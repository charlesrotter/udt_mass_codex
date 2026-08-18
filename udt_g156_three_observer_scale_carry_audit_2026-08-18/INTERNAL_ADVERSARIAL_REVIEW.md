# G156 fresh internal adversarial review

Date: 2026-08-18

Verdict before repairs: `PASS_WITH_REPAIRS`.

The reviewer independently confirmed the half-density convention, the pullback equation
`M_BA^* ell_B=exp(sigma_BA) ell_A`, endpoint-gauge cancellation, three-observer `kappa`
cancellation, the determinant-one nonclosure witness, and the zero-scale results for one query,
genuine overlap, and Levi-Civita transport.

Required repairs:

1. lead with a qualified landing because arbitrary supplied nonisometric carries need not be flat;
2. call the arbitrary triangle mismatch a determinant defect, not holonomy without a path functor;
3. reconcile source commit `b42c771d` with preregistration commit `7075abcc`;
4. scope the invisible kernel to `B+(2) intersect SL(2)`;
5. distinguish the half-density vector line from its positive ray;
6. base bounded-space coverage on the general symbolic proof, not source verification alone.

No algebraic or premise-changing objection was found.
