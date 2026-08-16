# G121 correction record

## Fresh blind-review repairs

1. **Screen holonomy type:** the initial exact loop was an `O(2)` reflection with determinant
   `-1`. It was replaced with a nonidentity `SO(2)` quarter rotation, and both implementations now
   check determinant `+1`. Production grew from `19` to `20` checks; independent replay grew from
   `9` to `10`.
2. **Noncircular descent theorem:** the derivation now begins with an antisymmetric scalar
   1-cochain, imposes zero triangle periods, proves the endpoint-potential equivalence, and only then
   calls the result an additive pair-groupoid cocycle.
3. **Mixed-map typing:** the premature raw matrix defect was removed. The next gate must preregister
   common fibers `W_A,W_B`, metric-derived maps `q_A,q_B`, and test the typed square
   `q_B R_causal = R_pair q_A`.
4. **Jacobi scope:** G121's new witness certifies nonidentity oriented screen holonomy and separately
   certifies symplectic phase composition. It does not claim to construct a new closed nonidentity
   Jacobi-phase loop; G114 remains the conditional source for that structure.
