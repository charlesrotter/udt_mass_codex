"""bv11 V1 part 3: tolerance cross-check of the root digit discrepancy (2 shots).
Shot A: my interpolated root at TIGHTER tol (rtol 1e-12/atol 1e-14).
Shot B: the CLAIMED a*=1.509995508 (d'=0.006663672) at the same tighter tol.
Slope near root (measured): dmiss/dd' ~ -1.86e4."""
import bv11_lib as L

fA, _ = L.miss_dp(0.0066635593, rtol=1e-12, atol=1e-14)
print(f"A: my root      d'=0.0066635593  tight-tol miss = {fA:+.6e}")
fB, _ = L.miss_dp(0.0066636720, rtol=1e-12, atol=1e-14)
print(f"B: claimed a*   d'=0.0066636720  tight-tol miss = {fB:+.6e}")
slope = -1.86e4
print(f"root shift implied by A (d'): {-fA/slope:+.3e}")
print(f"tight-tol root estimate d'* = {0.0066635593 - fA/slope + 0:.10f}"
      f" -> a* = {1.5*(1+0.0066635593 - fA/slope):.10f}")
print("shots:", L.SHOTS["n"])
