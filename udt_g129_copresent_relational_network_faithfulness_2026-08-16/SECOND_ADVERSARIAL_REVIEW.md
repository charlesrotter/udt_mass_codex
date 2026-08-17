# Second code-level adversarial review

`PASS_WITH_REPAIRS`

The bounded mathematics passes:

- Independent reconstruction gives six-plane rank 10 and three-axis rank 7, with kernel exactly
  `{g12,g13,g23}`.
- The registered rational metric reconstructs exactly.
- All six pair-regularity guards are genuine: `h00=-4` and all six exact determinants are negative.
- Independently, the curved invisible germ has `Rxy=Ryx=-a` and `Ricci^2=2a^2`; it is Lorentzian
  for `|az^2|<1` and shares every axial pullback with Minkowski.
- Terminal scalar nonfaithfulness holds even without changing `h00`, for example
  `diag(-1,1)` versus `[[-1,1/2],[1/2,3/4]]`.
- Fresh isolated production, independent, and package runs pass with byte-identical artifacts.

The regular-overlap theorem is justified only conditionally on supplied smooth query maps, a fixed
transition atlas, overlap compatibility, and a regular Hausdorff second-countable quotient. Under
those hypotheses the descended tensor is unique; topology and transitions are not reconstructed
from pair scalars.

Required evidence repairs:

1. Replace the circular independent Ricci-value check with an actual second-jet reconstruction.
2. Separate the analytic smooth-bump proof from the sampled machine regression.
3. Add a deliberately corrupted local metric/transition catch to the constructive overlap witness.

These defects weaken the evidence implementation, not the rank theorem, counterexamples, or bounded
unique-up-to-isometry conclusion.
