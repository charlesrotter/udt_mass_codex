# G149 exact witness registration

Date: 2026-08-17

This file freezes the local smooth witness before any outcome calculation. Every number is a
mechanically chosen small rational. They are numerical controls, not physical constants,
coefficients, initial data selected by UDT, or observational fits.

Use coordinates `x=(t,r,y,z)` and

```text
E(x)=[[B(x),0],[Q(x)S(x),Q(x)]],  g(x)=E(x)^T diag(-1,1,1,1) E(x).
```

At `x=0`:

```text
B0=[[2,1/2],[0,3]]
Q0=[[1,1/3],[0,2]]
S0=[[1/5,-1/7],[1/4,1/6]]
```

The affine coordinate slopes are:

```text
dB_dt=[[1/11,1/13],[-1/17,1/19]]
dB_dr=[[-1/23,1/29],[1/31,-1/37]]
dB_dy=[[1/41,-1/43],[1/47,1/53]]
dB_dz=[[-1/59,-1/61],[1/67,1/71]]

dQ_dt=[[1/73,-1/79],[1/83,1/89]]
dQ_dr=[[-1/97,1/101],[1/103,1/107]]
dQ_dy=[[1/109,1/113],[-1/127,1/131]]
dQ_dz=[[1/137,-1/139],[1/149,-1/151]]

dS_dt=[[-1/157,1/163],[1/167,-1/173]]
dS_dr=[[1/179,1/181],[-1/191,1/193]]
dS_dy=[[1/197,-1/199],[1/211,1/223]]
dS_dz=[[-1/227,1/229],[-1/233,1/239]]
```

The quadratic pair immersion is registered by its marked-point jets. Its first derivatives are

```text
J_tau   =[1,0, 1/10,-1/12]
J_sigma =[0,1,-1/8, 1/9]
```

and its second derivatives are

```text
F_tau_tau   =[ 1/59,-1/67,-1/73, 1/83]
F_tau_sigma =[ 1/61, 1/71, 1/79, 1/89]
F_sigma_sigma=[1/241,-1/251,1/257,-1/263]
```

Equivalently,

\[
F^\mu(\tau,\sigma)=J_\tau^\mu\tau+J_\sigma^\mu\sigma
+\tfrac12F_{\tau\tau}^\mu\tau^2
+F_{\tau\sigma}^\mu\tau\sigma
+\tfrac12F_{\sigma\sigma}^\mu\sigma^2.
\]

The block-removal liveness controls set only the corresponding first-jet family to zero while
leaving its base value and every other registered datum unchanged:

```text
B control: all dB_dx -> 0
Q control: all dQ_dx -> 0
S control: all dS_dx -> 0
Y control: base-coordinate components of F_tau_tau and F_tau_sigma -> 0
Z control: screen-coordinate components of F_tau_tau and F_tau_sigma -> 0
```

For the `Y` and `Z` controls, the names refer to the base and screen rows of the pair Jacobian
`[J_tau,J_sigma]`; they are not new spacetime coframe blocks.
