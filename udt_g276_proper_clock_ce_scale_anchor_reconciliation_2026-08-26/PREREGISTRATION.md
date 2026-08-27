# G276 preregistration

Date: 2026-08-26

## Exact model

Let

```text
g_ell = ell^2 * g_bar,  ell > 0,
```

and let one fixed dimensionless parametrized timelike segment have positive reference clock length

```text
C_bar = integral sqrt(-g_bar(gamma_dot,gamma_dot)) d_lambda > 0.
```

The physical proper duration is

```text
tau_ell = ell * C_bar / c_E.
```

One independent calibrated record `tau_star > 0` attached to that exact segment is accepted as a
scale anchor only if it gives a unique positive

```text
ell = c_E * tau_star / C_bar.
```

The conditional W5 representative is then

```text
x = ell * chi = c_E * tau_star * chi / C_bar.
```

## Required acceptance gates

1. exact homothety weight `+1` of clock length and proper duration;
2. unique positive scale recovery from one independently calibrated same-segment record;
3. exact time-to-length carry by `c_E` after the record is supplied;
4. a second consistent record recovers the same scale and an inconsistent record is rejected;
5. metric self-evaluation reduces to an identity and fixes no scale;
6. `c_E` alone cannot have pure-length unit type;
7. `M=sech(delta)`, `chi=tanh(delta)`, and `d tau/dx=1/c_E` are invariant under common rescaling and
   cannot alone fix scale;
8. no automatic operational-distance or `X_max` identification.

## Falsification contract

Reject alternative B if the proper-clock functional is not weight `+1`, if two positive scales
satisfy one valid nonzero record, if self-evaluation becomes nonidentity, or if the derivation needs
a pre-existing dimensionful distance. Catch hostile implementations that erase independence,
same-object matching, positivity, one-scale consistency, or the `X_max` boundary.

## Evidence contract

- exact production derivation;
- implementation-distinct standard-library census with at least 20,000 cases;
- executable hostile controls;
- no-write replays;
- premise audit before banking.
