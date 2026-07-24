# Four evidence gates

1. **Preregistered:** PASS  
   Commits `2fe47fd` and `223d460` froze the question, axes, transformations,
   completion classes, probes, sources, falsification rules, and exact sample
   values before outcome calculation.

2. **Full space or bounded scope justified:** PASS WITH BOUNDED SCOPE  
   All registered complete-coframe axes and all twelve inherited finite-cell
   classes were covered. The 25-point torus-shape grid is explicitly not the
   full continuous moduli space.

3. **Independently verified on the load-bearing premise:** PASS  
   A standard-library implementation independently recomputed the lattice
   selector, transformation covariance, conditional response anchors, source
   hashes, and completion coverage. No production import was used. Sixteen
   adversarial mutations were rejected. No external model arm was run.

4. **Every premise audited:** PASS  
   `PREMISE_AUDIT.tsv` grades all 22 registered premises. The carrier, action,
   physical selection, phase section, density map, and bootstrap closure
   remain open or conditional.

Package grade: `VERIFIED-WITH-CAVEATS`.

