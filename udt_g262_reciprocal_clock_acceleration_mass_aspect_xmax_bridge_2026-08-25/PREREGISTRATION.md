# G262 preregistration

Date: 2026-08-25

## Candidate landings

1. `NATIVE_MASS_AND_VALUE_LAW_CLOSED`
2. `ONE_METRIC_STATE_HIERARCHY_DERIVED__PHYSICAL_MASS_AND_VALUE_LAW_OPEN`
3. `ONLY_IMPORTED_GR_RELATIONS_RECOVERED`
4. `CLOCK_MASS_XMAX_IDENTIFICATION_INCONSISTENT`

No candidate is preferred by the test contract.

## Exact tests

On arbitrary positive twice-differentiable `f(r)` define

\[
N=\sqrt f=e^{-\phi},
\qquad
\mu=\frac r2(1-f).
\]

The production derivation must independently check:

1. static proper-clock rate `d tau/dt = N` after the declared `c_E` coordinate calibration;
2. signed orthonormal static-observer acceleration `a_hat = dN/dr`;
3. `f=1-2 mu/r` without a field equation;
4. G259 residual identities `E0=-2 mu'` and `E1=-r mu''`;
5. G260 angular trace `A_parallel+A_perp=2 mu'-r mu''`;
6. pair clock ratio `q_AB=N_B/N_A=exp(-delta_AB)` on an endpoint-exact matched branch;
7. `Z_AB=1/q_AB` and the already conditional G95 carried-covector energy ratio
   `epsilon_AB=q_AB` under the same orientation;
8. reversal and composition for `q` and `epsilon`;
9. for the working normalized pair coordinate `chi=tanh(delta)`,
   `q=sqrt((1-chi)/(1+chi))` on `|chi|<1`;
10. the two directional limits `q->0` and `q_reverse->infinity` as `chi->1`;
11. a generic continuous positive mass factor depending only on `q` and composing
    multiplicatively has the character family `q^w`; current premises must be audited for ownership
    of `w` and of the physical object being transformed.

## Nonidentity gate

A claimed value/history law must distinguish two preregistered smooth positive profiles for a
reason not equivalent to defining `N`, `mu`, acceleration, curvature, or pair readouts. If every
identity holds for both profiles, the history law remains open.

Use the controls

\[
f_0(r)=1,
\qquad
f_a(r)=1+\frac{a r^2}{1+r^2},
\qquad 0<a<1, r\ge0.
\]

Both are positive and smooth-centered. They have different acceleration, mass-aspect, and
curvature data. Passing the same identities is evidence of evaluation/interlock, not selection.

## Ownership rules

- The metric clock/acceleration/mass-aspect/curvature identities may be `DERIVED` in the bounded
  primary chart.
- `epsilon=1/Z` remains `DERIVED_CONDITIONAL` on the supplied carrier-covector identification from
  G95.
- Local rest mass, physical UDT mass, a source, and a normalized total charge remain `OPEN` unless
  an existing frozen source supplies the missing type.
- The mass-equivalent attachment `M=(c_E^2/G_obs) mu` is an `OBSERVED/CONDITIONAL` dimensional
  attachment, not a native source law.
- `X_max` is used only through the current working normalized asymptotic coordinate. Its value,
  physical separation map, global realization, and boundary completion may not enter.

## Evidence contract

- preregister this document before running the algebra;
- use arbitrary symbolic functions plus exact-rational profile cases;
- independent verification must not import production code or its output;
- catch at least eight sign, factor, direction, ownership, and profile-selection mutations;
- run the full current premise verifier before banking;
- maximum conclusion is bounded interlock/ownership, not matter theory or a complete history.
