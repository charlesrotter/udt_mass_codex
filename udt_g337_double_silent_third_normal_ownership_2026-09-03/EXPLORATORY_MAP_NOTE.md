# G337 exploratory-map disclosure

Date: 2026-09-03

Before preregistration, hand differentiation exposed the candidate tensor structure below. No
coordinate evaluation, sign census, witness search, or executable calculation was performed.

With `A=K^sharp`, `F=nK`, and `B=K gamma^{-1} K`, the active Gaussian-normal equations give

```text
n gamma = -2K,
F = Ric3 + tau K - 2B - Lambda gamma.
```

For an inherited Lie-carried direction satisfying `K(v,v)=F(v,v)=0`, define

```text
s2 := (1/2)n^3[gamma(v,v)] = -n^2 K(v,v).
```

The mapped candidate is

```text
s2 = -(n Ric3)(v,v) + 2(nB)(v,v),
nB = F gamma^{-1}K + K gamma^{-1}F + 2K gamma^{-1}K gamma^{-1}K.
```

The Ricci-variation term appears to contain second spatial derivatives of `K`. Whether constraints
or the special G332 family reduce those derivatives is deliberately left for the registered test.
This disclosure prevents the production calculation from being represented as a blind discovery.
