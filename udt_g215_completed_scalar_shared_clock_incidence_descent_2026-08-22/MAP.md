# G215 map — completed scalar descent on shared observer clocks

Date: 2026-08-22

## Whole question

After the G176 completed-pair normalization, does the terminal reciprocal scalar at one observer
depend on the whole incident pair plane, or only on that observer's calibrated clock germ? If the
latter, do completed scalar depths telescope across an observer network even though the full
`AB`, `BC`, and `AC` pair metrics still have no native product?

## Metric-led frame

- one supplied Lorentz metric and supplied regular completed pair germs;
- G168 endpoint tangents `(u_X,s_XY)` and primary pullback `h=J^TgJ`;
- G176 working clarification `m=sqrt(-det h_sigma)` and `det h_s=-1`;
- one shared calibrated clock germ at an observer means the same clock tangent and clock coordinate
  are used by every incident pair;
- ruler directions, angular participation, density, shift, and full pair planes may differ;
- independently rescaled edge clocks are retained as a hostile control.

This is a scalar-incidence audit. It does not multiply pair metrics, populate observers, derive a
metric profile, select a path, or generate a history.

## Candidate simplification

For

```text
h_sigma = -T^2(dy0 + beta dsigma)^2 + L_sigma^2 dsigma^2,
m = T L_sigma,
```

G176 gives

```text
Phi_completed = -log(T),   T^2 = -g(u,u).
```

Therefore every incident pair using the same calibrated clock germ `u_X` should have one endpoint
potential `varphi_X=-log sqrt(-g(u_X,u_X))`, regardless of its ruler direction. The pair depth would
then be `delta_XY=varphi_Y-varphi_X`, so every matched observer cycle telescopes.

## Anticipated boundary

This cannot identify full pair planes or their shifts. If the same observer is independently
reparameterized on different edges, then its `T` values differ and scalar descent fails by the
clock-calibration mismatch. The exact remaining carry datum should therefore be common clock
calibration, not a full-tuple multiplication law.
