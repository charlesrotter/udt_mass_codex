# G216 exact derivation — proper-clock rates on an observer-pair germ

Date: 2026-08-22

## Bounded landing

```text
PROPER_TIME_NORMALIZES_EACH_OBSERVER_CLOCK_BUT_A_UNIT_TANGENT_HAS_ZERO_LOCAL_COMPLETED_SCALAR
__NONZERO_COMPLETED_PAIR_DEPTH_IS_MINUS_LOG_OF_THE_PROPER_TIME_EVENT_PAIRING_DERIVATIVE
__COMMON_PAIR_REPARAMETERIZATION_CANCELS_EXACTLY
__REVERSAL_AND_COMPOSITION_ARE_INVERSE_FUNCTION_AND_CHAIN_RULE_IDENTITIES
__G215_SHARED_CLOCK_IS_A_SHARED_OBSERVER_INCIDENCE_COMPARISON_CLOCK_NOT_A_BARE_UNIT_FOUR_VELOCITY
__A_SUPPLIED_CALIBRATED_PAIR_MAP_NEEDS_NO_ADDITIONAL_FREE_CLOCK_SCALE
__PHYSICAL_EVENT_PAIRING_AND_PAIR_GERM_OWNERSHIP_REMAIN_OPEN
```

Status: `DERIVED_CONDITIONAL__PREREGISTERED__INDEPENDENT_EXACT_REPLAY_PASS__FRESH_REVIEW_REQUIRED`.

## 1. Proper time and the pair-domain clock

Let (z_X(\tau_X)) be a supplied future timelike observer worldline, with dimension-matched proper
clock coordinate (\tau_X). Its metric-unit tangent is

\[
U_X=\frac{dz_X}{d\tau_X},
\qquad
g(U_X,U_X)=-1.
\]

Now let one supplied regular pair map use a common domain clock coordinate (y). At endpoint (X),
the clock tangent entering the pullback is

\[
u_X=\frac{dz_X}{dy}
=\frac{d\tau_X}{dy}U_X.
\]

For a future-oriented regular germ, (d\tau_X/dy>0). Therefore

\[
T_X^2=-g(u_X,u_X)
=\left(\frac{d\tau_X}{dy}\right)^2,
\qquad
\boxed{T_X=\frac{d\tau_X}{dy}.}
\]

Using the G176 working completion and G215 terminal readout,

\[
\boxed{
\Phi_X=-\log T_X
=-\log\frac{d\tau_X}{dy}.
}
\]

This identifies the G215 `calibrated clock tangent and parameter` precisely: it is the
observer-incidence tangent induced by the supplied pair-domain clock, not automatically the unit
four-velocity.

## 2. Unit proper time is canonical but locally trivial

If one chooses (y=\tau_X) at a single observer endpoint, then

\[
u_X=U_X,
\qquad
T_X=1,
\qquad
\boxed{\Phi_X=0.}
\]

Equivalently, the exact exponentiated endpoint quantities are

\[
e^{-2\Phi_X}=T_X^2=1,
\qquad
e^{4\Phi_X}=T_X^{-4}=1.
\]

Thus metric proper time supplies the canonical normalization of each observer clock, but it cannot
by itself be substituted for the nonzero comparison-clock tangent. Doing so would erase every
nonzero completed endpoint scalar.

This is not an inconsistency. A nonzero pair comparison uses one correspondence between two proper
clock lines, not two independently chosen unit parameters pretending to be the same pair
coordinate.

## 3. Parameter-free event-pairing rate theorem

On a supplied pair map, both endpoint proper times are functions of the same (y). Hence the local
event-pairing derivative is

\[
\lambda_{AB}
=\frac{d\tau_B}{d\tau_A}
=\frac{d\tau_B/dy}{d\tau_A/dy}
=\frac{T_B}{T_A}>0.
\]

G170's endpoint-relative completed depth is therefore

\[
\delta_{AB}=\Phi_B-\Phi_A
=\log\frac{T_A}{T_B}
=\boxed{-\log\lambda_{AB}}
=-\log\frac{d\tau_B}{d\tau_A}.
\]

The exponentiated forms avoid any logarithmic convention:

\[
\boxed{
e^{\delta_{AB}}=\lambda_{AB}^{-1},
\qquad
e^{-2\delta_{AB}}=\lambda_{AB}^{2}.
}
\]

So the native scalar datum of one supplied observer-pair germ is the reciprocal derivative between
the two metric proper-clock axes. It is not an independently fitted clock coefficient.

## 4. Common reparameterization is gauge for the edge scalar

Let (y'=f(y)) with (f'(y)>0). Then

\[
T_X'=\frac{d\tau_X}{dy'}
=\frac{T_X}{f'(y)},
\qquad
\Phi_X'=\Phi_X+\log f'(y).
\]

The individual endpoint potential is therefore a chart-weighted quantity. But paired endpoints
share the same domain value (y), so the same factor cancels:

\[
\boxed{
\delta_{AB}'
=\log\frac{T_A/f'}{T_B/f'}
=\delta_{AB}.
}
\]

Equivalently, (\lambda_{AB}=d\tau_B/d\tau_A) contains no auxiliary (y) at all. A fully supplied
event-pairing first jet therefore needs no additional absolute clock-scale choice.

If the two incidences are independently reparameterized by positive factors (a_A,a_B), then

\[
T_A'=\frac{T_A}{a_A},
\qquad
T_B'=\frac{T_B}{a_B},
\]

and

\[
\boxed{
e^{\delta_{AB}'}
=e^{\delta_{AB}}\frac{a_B}{a_A},
\qquad
e^{-2\delta_{AB}'}
=e^{-2\delta_{AB}}\left(\frac{a_A}{a_B}\right)^2.
}
\]

This is exactly the G215 unmatched-clock defect. It compares different pair-germ calibrations; it
is not a failure of the one-pair invariant.

## 5. Reversal and composition

For the inverse event-pair germ,

\[
\lambda_{BA}=\frac{d\tau_A}{d\tau_B}=\lambda_{AB}^{-1},
\]

so

\[
\boxed{\delta_{BA}=-\delta_{AB}.}
\]

For composable event-pair germs (A\to B\to C), the chain rule gives

\[
\lambda_{AC}
=\frac{d\tau_C}{d\tau_A}
=\frac{d\tau_C}{d\tau_B}\frac{d\tau_B}{d\tau_A}
=\lambda_{BC}\lambda_{AB}.
\]

Therefore, when the direct (AC) germ is the actual composite,

\[
\boxed{\delta_{AC}=\delta_{AB}+\delta_{BC}.}
\]

An independently supplied direct (AC) germ is not forced to equal that composite. This retains
the G214 boundary: composition is exact on a coherently composed relation family, not on arbitrary
pair surfaces sharing observer names.

G215's vertex-potential network is the stronger special case in which one common comparison-clock
trivialization is reused across incidences. G216 shows that the invariant edge statement does not
need absolute vertex clock factors; it needs the proper-clock event-pair derivative.

## 6. Primary static specialization

In the declared primary static metric, use the shared dimension-matched coordinate

\[
y=x^0=c_E t,
\qquad
g(\partial_{x^0},\partial_{x^0})=-e^{-2\phi_X}.
\]

Along a static observer worldline,

\[
\frac{d\tau_X}{dx^0}=e^{-\phi_X},
\qquad
U_X=e^{\phi_X}\partial_{x^0}.
\]

The coordinate tangent (u_X=\partial_{x^0}), not the unit tangent (U_X), is the pair-domain
clock tangent. Hence

\[
T_X=e^{-\phi_X},
\qquad
\Phi_X=\phi_X,
\]

and

\[
\boxed{
\delta_{AB}=\phi_B-\phi_A
=-\log\frac{d\tau_B}{d\tau_A}.
}
\]

This exactly recovers G170/G215 and explains why the unit-tangent substitution would have been the
wrong type.

## 7. Event labels and what remains supplied

A persistent observer label is not one endpoint vertex. If one observer visits events (e_1,e_2),
the metric and pair map may give different rates (T_{X,e_1}\) and (T_{X,e_2}). Endpoint
potentials must therefore be indexed by observer-event incidence, not only by the worldline name.

The exact ownership hierarchy is now:

1. a supplied timelike worldline plus metric derives its proper clock and unit tangent;
2. a supplied local event-pair relation derives (d\tau_B/d\tau_A);
3. G176/G215 derives the completed reciprocal depth from that derivative;
4. inverse and composable relation germs derive reversal and addition.

What remains open is which observer events and pair germ are physically realized. G216 does not
derive that population. It does show that **after** the pair germ is supplied, there is no separate
free scalar clock calibration left in the endpoint-relative kernel.

## 8. Orchestra and scope

Angular, screen, mixing, density, shift, pair-plane, and immersion data remain live. They enter the
complete pair pullback and its completion exactly as in G176--G215. G216 neither deletes them nor
adds a post-readout scalar.

- `DERIVED_CONDITIONAL`: metric proper time and the unit tangent on a supplied timelike worldline.
- `DERIVED_CONDITIONAL`: (\delta_{AB}=-\log(d\tau_B/d\tau_A)) on a supplied regular G176-completed
  event-pair germ.
- `DERIVED_CONDITIONAL`: common reparameterization cancellation, reversal, and chain-rule
  composition.
- `RECLASSIFIED_PRECISION`: G215's shared clock is a shared comparison-clock incidence germ, not a
  bare unit four-velocity.
- `RETAINED_OPEN`: physical event-pair/germ population, arbitrary noncomposed direct relations,
  full non-scalar carry, metric values/profiles, singular/global strata, and history evolution.
- `INACTIVE`: `X_max`, fits, transfer, observations, action, source, matter, bootstrap, mass, and
  signalling.
