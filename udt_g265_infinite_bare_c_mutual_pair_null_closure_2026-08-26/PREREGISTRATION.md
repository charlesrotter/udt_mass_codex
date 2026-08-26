# G265 preregistration

Date: 2026-08-26
Status: `PREREGISTERED_BEFORE_OUTCOME_ALGEBRA`

## Candidate premises under test

`P_INF` (`PROPOSED_FOUNDATIONAL_RECOVERY_NOT_ADOPTED`): bare transfer has zero intrinsic duration;
all finite observed propagation duration and causal structure arise from the completed UDT metric.

`P_MUT` (`PROPOSED_FOUNDATIONAL_RECOVERY_NOT_ADOPTED`): separation owns a nonnegative pair magnitude
`q(A,B)=q(B,A)` and each observer assigns the same clock-slowing magnitude to the other.

Neither statement is canonized by this test. The existing F1--F4, W1, W3, and W4 status remains
unchanged.

## Frozen metric identities

On a radial future-null branch with endpoint radii `r_A,r_B`, define

\[
N=\sqrt f,\qquad
D_{\rm opt}=\int_{r_A}^{r_B}\frac{|dr|}{f},\qquad
\ell=\int_{r_A}^{r_B}\frac{|dr|}{\sqrt f}.
\]

The metric gives coordinate null duration `c_E Delta t=D_opt`, endpoint static proper-clock
durations `c_E Delta tau_A=N_A D_opt` and `c_E Delta tau_B=N_B D_opt`, and the G220 signed null clock
arrow `r_AB=N_B/N_A` after orientation is declared.

## Closure alternatives to test

1. **Optical closure:** `c_E Delta t=D_opt`. Determine whether adding zero bare duration changes
   this identity or rejects any `f`.
2. **Literal proper-distance closure:** impose `c_E Delta t=ell` for every subinterval. Determine
   its entire solution family.
3. **Observer-clock finite-speed closure:** compare `ell/Delta tau_A` and `ell/Delta tau_B`; test
   whether equal mutual finite-speed/slowdown readouts can coexist with nonconstant static `f`.
4. **Signed-versus-even reciprocal channels:** compare the G220 factor `exp(-delta)` with the
   reversal-even group invariant `cosh(delta)` and the candidate SR-analogue mutual clock rate
   `sech(delta)`. The `sech` interpretation is a candidate projection, not a founded readout.
5. **Metric-delay-density closure:** classify `dt/dr=1/(c_E f)` as value law or tomography of a
   supplied metric.

## Candidate outcomes

1. `INFINITE_C_NATIVE_VALUE_LAW`: one closure follows from `P_INF` and founded structure, rejects at
   least one G264 profile, and retains a nontrivial regular solution family compatible with `P_MUT`.
2. `INFINITE_C_NULL_IDENTITY_OR_TRIVIALITY`: the metric-owned reading is an identity for every `f`,
   while stronger distance equalities either trivialize `f` or require another premise.
3. `STATIC_ENDPOINT_REALIZATION_INCOMPATIBLE_WITH_MUTUALITY`: a nontrivial static lapse can carry
   the signed null arrow but cannot represent equal mutual slowdown on the same reversal class;
   time-live or genuinely two-point realization remains open.
4. `FOUNDING_CHAIN_INCONSISTENT`: no nontrivial metric-owned interpretation of either statement
   survives even after respecting output types.

Multiple bounded outcomes may hold if they refer to different explicitly typed closures.

## Certification and falsification contract

A positive value-law landing requires all of:

- a residual not identically zero for arbitrary positive `f`;
- rejection of at least one preregistered G264 witness;
- at least one nontrivial regular survivor;
- pair-exchange compatibility appropriate to `P_MUT`;
- no preferred distance definition inserted after the result;
- exact symbolic derivation and an implementation-distinct numerical quadrature replay.

The analysis fails if it calls an optical-distance identity dynamics, treats coordinate speed as a
local measured signal speed, equates causal return with inversion, identifies `exp(-delta)` with an
even mutual slowdown without proof, imports light physics, or promotes flatness because a stronger
unstated equality forced it.

## Maximum conclusion

An exact static-radial classification of whether `P_INF` and `P_MUT` close values, expose a
type mismatch, or redirect the theory toward a time-live/two-point realization. No complete
physical history, propagation mechanism, source law, or canon result can follow.
