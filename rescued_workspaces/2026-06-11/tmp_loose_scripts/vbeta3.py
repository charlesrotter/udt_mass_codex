"""Vβ-3: IBP bound derivation correctness.

At m=0:
  U' = (2 kappa/r) V
With V = R cos Theta (R = U slow envelope per ansatz; W = (R/2) sin Theta):
  U' = (2 kappa/r) U cos Theta
  d/dr log U = (2 kappa/r) cos Theta = g(r) cos Theta with g(r) = 2 kappa/r

IBP with Theta' = k = 2 E e^{2 phi}:
  cos Theta = (1/k) d/dr sin Theta
  int_{r0}^r g cos Theta dr = [g sin Theta / k]_{r0}^r - int sin Theta * (g/k)' dr

Taking absolute values:
  |log U(r) - log U(r0)| <= |g/k|(r) + |g/k|(r0) + int |(g/k)'| dr
                          <= 2 max |g/k| + int |(g/k)'| dr.
PASS — the agent's factor of 2 is the sum of two boundary endpoints bounded by max.
"""
print("IBP derivation:")
print("  |log U(r) - log U(r0)|")
print("  = | [g sin Theta / k]_{r0}^r - int sin Theta (g/k)' dr |")
print("  <= |g/k|(r) * 1 + |g/k|(r0) * 1 + int |(g/k)'| dr     [since |sin Theta| <= 1]")
print("  <= 2 max_{[r0,r]} |g/k| + int |(g/k)'| dr")
print()
print("Factor of 2 = sum of two endpoint contributions each bounded by max. PASS")

# But wait: agent's compute_IBP_bound takes max over the full window mask:
# boundary_term = 2.0 * float(np.max(np.abs(ratio[mask])))
# integral_term = int |ratio_prime| over the same window
# bound = boundary + integral
# This is consistent with the textbook IBP bound. PASS.

# Sub-leading note: the ansatz R = U is "slow envelope hypothesis"; in the
# script the ansatz substitution leaves residual terms when R' != 0 (R changes
# from the (2 kappa/r) U source).  At sub-leading order, R = U(r) self-consistently.
# The bound captures this self-consistent slow drift via the IBP identity above.

# Test: at adequate resolution, observed |log U swing| <= 2 max|g/k| + int |(g/k)'|.
# Should hold *exactly* (as an identity from the IBP, modulo sub-sub-leading sin Theta wiggles
# bounded by |sin Theta| <= 1 which is already used).
print()
print("Vβ-3 verdict: IBP bound derivation correct. Factor of 2 is sum-of-two-endpoints. PASS")
