# Finite reciprocal quotient-lift audit

Date: 2026-07-27

Grade: **VERIFIED-WITH-CAVEATS**.

## Result first

The finite integration problem is now exactly classified under the registered quotient query.

If the complete four-coframe is required to preserve the founded reciprocal clock/ruler pair as an
exact quotient, every finite lift must have block form

```text
F(phi) = [[B(phi), 0],
          [L(phi), Q(phi)]].
```

That quotient condition alone leaves eight arbitrary smooth function components. It does not derive
a constant generator or the earlier triangular chart.

If the **complete** lift is additionally required to obey the additive one-parameter group law, the
class becomes

```text
F(phi)=exp(phi X),
X=[[H,0],[C,K]],
```

with eight constant parameters: four in `C` and four in `K`. The founded pair law does not by itself
select this stronger complete-coframe premise.

## What the metric response fixes

The first complete metric response has exact rank seven. It fixes `C` and the symmetric part `S` of
`K`, while leaving one screen-rotation rate in

```text
K=S+wJ.
```

The earlier seven-parameter positive-triangular extension is therefore a screen-flag section of the
eight-parameter quotient-representation class. Its seven first-response directions remain exact and
independent; it was complete only inside its registered triangular chart.

Neither upper nor lower triangularity is metric-selected. Given the same response, an upper screen
flag fixes `w=+b` and the opposite flag fixes `w=-b`. A screen rotation interchanges the displayed
flag.

## The finite distinction

The missing screen rotation is not generically a gauge artifact. Exact second-jet algebra proves:

- with no pair/screen mixing, nonzero `w` is metric-invisible only when the symmetric screen response
  is isotropic, `S=lambda I`;
- even on that isotropic screen, any nonzero mixing `C` makes `w` visible in the cross metric at
  second order;
- only the combined `C=0`, `S=lambda I` stratum gives exact finite metric equality for every `w`.

Thus two quotient generators can share the entire first metric response yet generate inequivalent
finite metric paths. The special isotropic/unmixed family is a genuine fixed-metric coframe rotation;
the generic family is finite metric data.

The unique full metric-self-adjoint representative is also not a general answer: when `C` is nonzero
it has a nonzero upper-right block and violates the exact quotient. It belongs to the quotient class
only on the no-mixing stratum.

## Independent gates

- 12/12 preregistered candidate classes classified;
- exact quotient constraint rank: 8;
- complete quotient-group generator dimension: 8;
- first metric response rank: 7;
- fixed-response generator fiber: 1;
- 42 production SymPy checks passed;
- 18 separate standard-library `Fraction` checks passed, including metric-series equality through
  order eight on the isotropic/unmixed control;
- 26 audit-verifier checks passed; and
- 11 exercised false-promotion catches were rejected.

The independent implementation imports neither SymPy nor the production derivation/output. It
reconstructs the ranks, first-response kernel, flag pair, second-jet controls, and a fixed-metric
quotient path that fails group composition and reversal.

## Honest status change

Before this audit:

```text
finite complete-coframe lift from the seven-dimensional response: OPEN.
```

After this audit:

```text
exact quotient finite normal form:           DERIVED IF EXACT QUOTIENT IS SUPPLIED
complete constant-generator class:           DERIVED IF COMPLETE GROUP LAW IS SUPPLIED
generator parameters before flag choice:     8
complete first metric response rank:         7
fixed-response finite lifts:                 one-parameter family
triangular seven-parameter chart:            CONDITIONAL ON SCREEN FLAG
screen rotation as finite metric gauge:      only C=0 and S=lambda I
physical quotient/group/response/flag choice: OPEN
global screen subbundle and transitions:      OPEN
```

The local finite-lift ambiguity is smaller and more sharply typed, but no physical complete lift has
been selected.

## Authority boundary

No GR/SR observer mechanics, field equation, action, matter carrier, source, boundary functional,
bootstrap selector, `X_max`, mass law, or dynamics was imported or promoted. Founded `phi` and the
two-channel reciprocal action remain `DERIVED`; strong local CSN remains inactive; `c_E` and `G_obs`
retain their observed-anchor status.

## Four gates

1. **Preregistered:** yes, commit `ea66d8f`, pushed before the new finite algebra was run.
2. **Full or bounded:** complete for all 12 registered local/global lift classes in the exact
   four-dimensional quotient/group/first- and second-jet regime. It is not a classification of every
   nonlinear global bundle topology or physical observer realization.
3. **Independent:** exact SymPy and separate standard-library/Fraction implementations agree on all
   load-bearing ranks and countercontrols. No fresh zero-context model-family review was used, so the
   grade retains that caveat.
4. **Premises:** exact quotient semantics, complete group law, ordered pair/screen, flag,
   self-adjointness, global subbundle, physical section, and downstream objects are separately
   stamped.

Maximum conclusion:

`EXACT_FINITE_QUOTIENT_AND_GROUP_LIFT_CLASSES_DERIVED_CONDITIONALLY;_FIXED_RESPONSE_LEAVES_ONE_SCREEN_ROTATION_AND_GLOBAL_PHYSICAL_SELECTION_OPEN`.
