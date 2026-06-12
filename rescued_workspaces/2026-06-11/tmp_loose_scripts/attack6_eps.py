# ATTACK 6: phase vs eps table. eps multiplies psi_new relative to psi_old. eps is the recycling
# amplitude (NON-DERIVED input, charter admits this). The table:
#  eps=0   -> 21.3 (in-phase baseline)
#  eps=0.25-> 13.6 (MOVES BACK TOWARD in-phase! non-monotonic)
#  eps=1.0 -> 46.7
#  eps=2.0 -> 73.4
#  eps=4.0 -> 77.8
#  eps=10  -> 70.0 (turns back down)
# Observations:
# 1. Non-monotonic: adding a little new channel (eps=0.1-0.5) makes it LESS quadrature (back to ~14).
#    The new channel first partially CANCELS the old channel's small phase before building quadrature.
# 2. The phase is NOT pinned: it sweeps the whole range 14-78 deg depending on eps.
#    There is NO derived eps, so the predicted phase is ANYWHERE in [14,78] -- not a prediction of
#    quadrature, but a free dial that CAN reach quadrature for eps~2-4.
# 3. "66 deg quadrature target" = the eps->inf (pure new channel) limit, which is itself only 66
#    (not 90) and weight-choice-dependent (37 bare / 66 W_EE / 87 TT-weight).
# CONCLUSION: the phase is a TUNABLE output of a non-derived amplitude eps, not a derived value.
# The mechanism EXISTS (a derived term that, if eps is large enough, rotates toward quadrature),
# but the SPECIFIC ~66 deg is (a) weight-dependent and (b) the eps->inf limit, while any finite
# realistic eps gives something between in-phase and 66.
print("Phase is a tunable function of non-derived eps; range [14,78] deg over eps in [0,10].")
print("Non-monotonic near small eps. 66 deg = eps->inf limit AND weight-choice dependent.")
