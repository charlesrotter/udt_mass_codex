# Symbolic checker normal-form repair

Initial capture failed before any finite records/guards at the v-identity
assertion. SymPy trigsimp left a noncanonical expression instead of literal0.
A separate captured diagnostic using expand_trig followed by trigsimp still
left the same identity unreduced; both failures are preserved. The identity
is checked by expanding sin(2theta),cos(2theta), expressing tan as sin/cos and
performing rational cancellation on the already-required cos(theta)!=0 domain.
The hand identity follows by combining (2cos²-1)-4cos²=-(1+2cos²).

This is an implementation normal-form repair, not a changed scientific formula,
sample, tolerance or outcome selection. Initial code/candidate/freeze and failed
captures survive. The revised code is frozen below before numerical examples.
Review must examine the identity and domain, not infer proof from a pass.
