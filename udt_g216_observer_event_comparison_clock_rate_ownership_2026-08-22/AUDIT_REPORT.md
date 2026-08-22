# G216 audit report — observer-event comparison-clock rate ownership

Date: 2026-08-22

## Primary landing

```text
PAIR_GERM_PROPER_CLOCK_RATE_LAW_DERIVED_CONDITIONALLY
__UNIT_PROPER_CLOCK_TRIVIALIZES_THE_LOCAL_ENDPOINT_SCALAR
__COMMON_PAIR_REPARAMETERIZATION_CANCELS
__PHYSICAL_PAIR_GERM_POPULATION_REMAINS_OPEN
```

## Result first

For a supplied timelike observer worldline with metric-unit tangent (U_X), and one supplied pair
map with common clock parameter (y),

\[
u_X=\frac{d\tau_X}{dy}U_X,
\qquad
T_X=\sqrt{-g(u_X,u_X)}=\frac{d\tau_X}{dy}.
\]

G176/G215 therefore gives

\[
\Phi_X=-\log\frac{d\tau_X}{dy},
\qquad
\boxed{
\delta_{AB}=\Phi_B-\Phi_A
=-\log\frac{d\tau_B}{d\tau_A}.
}
\]

The auxiliary pair parameter cancels. Reversal is the inverse-function rule and scalar
composition is the chain rule for actually composable event-pair germs.

A unit proper-time tangent has (T=1) and (\Phi=0). Thus G215's shared calibrated clock must be
read as a shared observer-incidence **comparison** clock tangent, not as a bare unit four-velocity.
In the primary static chart, the shared coordinate (x^0=c_Et) gives

\[
d\tau_X/dx^0=e^{-\phi_X},
\]

so (\Phi_X=\phi_X) and the earlier kernel is recovered exactly.

## What changed

- Proper time closes the observer-clock normalization, but not by creating a nonzero absolute
  endpoint potential.
- The invariant scalar is the derivative of the supplied event pairing between the two proper-time
  axes.
- A supplied calibrated pair map therefore needs no additional independent clock-scale coefficient.
- G215 remains correct on its stated shared-clock antecedent, but its ownership wording is narrowed
  from persistent observer clock to observer-event comparison-clock germ.
- Physical event pairing and pair-germ population remain supplied/open.

## Evidence

- alternatives and falsifiers preregistered and pushed at commit `65c5cfe7`;
- 12/12 frozen source hashes pass;
- 36/36 dependency-free exact production checks pass;
- independent `Fraction` replay passes 190,000 assertions over 10,000 cases;
- 17/17 hostile semantic and algebraic catches pass;
- aggregate package replay is fail-closed and no-write.

## Four gates

1. **Preregistered:** PASS.
2. **Full space or bounded scope:** PASS WITH CAVEATS — regular timelike observer worldlines and
   supplied regular G176-completed local pair germs only.
3. **Independent verification:** PASS — separate exact `Fraction` implementation.
4. **Premise audit:** PASS WITH CAVEATS — G176 remains a working clarification and physical pair
   germs remain supplied.

## Maximum conclusion

G216 closes the extra-clock-scale question on a supplied calibrated event-pair germ: the completed
scalar is the metric proper-clock rate ratio, not a new coefficient. It does not select or populate
the physical event-pair germ, generate metric values/profiles or history evolution, close full
non-scalar carry, or derive downstream physics.

Current grade: `DERIVED_CONDITIONAL__INDEPENDENT_EXACT_REPLAY_PASS__FRESH_REVIEW_REQUIRED`.
