# Exact profile and query crosswalk

## Profile algebra

Write `Z=1+z`.

For the `grok2` chosen hyperbolic profile,

```text
r_tanh = X_tanh (Z^2-1)/(Z^2+1),
```

direct differentiation gives

```text
r_tanh(1)=0,
dr_tanh/dz|0=X_tanh,
d2r_tanh/dz2|0=-X_tanh,
lim_(Z->infinity) r_tanh=X_tanh.
```

For G99 P1,

```text
r_P1=n X_eff [1-Z^(-2/n)],
```

one gets

```text
r_P1(1)=0,
dr_P1/dz|0=2 X_eff,
d2r_P1/dz2|0=-2 X_eff(1+2/n),
lim_(Z->infinity) r_P1=n X_eff.
```

The equality of nearby slopes fixes only

```text
X_tanh=2 X_eff.
```

It does not imply equality of profiles or endpoints. At the frozen G99 central values,

```text
n=1.0559332414320268,
X_eff=2085.9586748597476 Mpc,
```

the P1 local slope is `4171.917349719495 Mpc`, the P1 radius asymptote is
`2202.6331050379085 Mpc`, and the matched-slope `tanh` asymptote is
`4171.917349719495 Mpc`.

## Megamaser translation

Using the primary-source combined value and exact conventional `c` in km/s,

```text
H0=73.9 +/- 3.0 km s^-1 Mpc^-1,
c=299792.458 km/s,
```

gives

```text
L_maser=c/H0=4056.731502029769 Mpc,
sigma_L=c sigma_H/H0^2=164.6846347238066 Mpc.
```

This is a local inverse rate. Its rebranding as a finite asymptote requires an independently owned
global radius law.

## BAO query typing

The frozen BOSS estimator is a function of angular pairs of observed directions. Schematically,

```text
theta_12 = arccos(n1 dot n2),
xi(theta) = normalized DD - 2 normalized DR + normalized RR.
```

Therefore a future UDT map must accept at least two complete observer--source evaluations joined at
one common observer. A single Earth--source scalar cannot by itself produce the two-point curve.
This typing statement does not decide whether the joined response is reducible, factorized,
correlated by the source field, or path dependent.
