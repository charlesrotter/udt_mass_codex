# Preregistration — intrinsic contact descent on the explicit twisted `S3` witness

Date: 2026-08-02  
Branch: `grok`  
Preregistration base: `ab5ed373b14bbd11dac21a91b7ebfdcca3b75b5f`

## Whole question

On the already verified explicit complete-cell, off-shell twisted stationary `R x S3` witness,
replace the formerly supplied reciprocal-pair/screen split by the metric-derived clock/ruler
projector. Determine which inherited full-screen Cartan/contact objects descend to tensors or
scalars of that metric, which are only sign-local-system or reference-dependent objects, and which
still require a screen frame, path, global completion datum, or physical law.

This is metric-led and observational: it classifies every registered descendant in
`OBJECT_UNIVERSE.tsv`. It does not target a nonzero contact form, a Hopf object, matter, mass, or an
action.

## Exact bounded family

Use only the previously verified primary analytic profile

```text
u=exp(2 phi)=3+q0^2+2q1^2+4q2^2+8q3^2,   sum q_i^2=1,
4 <= u <= 11,
theta0=u^(-1/2)(dt+sigma3),
theta1=u^(+1/2)sigma3,
theta2=u^(lambda/2)sigma1,
theta3=u^(lambda/2)sigma2,
g=-theta0^2+theta1^2+theta2^2+theta3^2,
d sigma3=kappa sigma1 wedge sigma2,  kappa=-2,
lambda in {-1,0,+1}.
```

`c_E=R=a=1` are the frozen existence-unit choices. No other profile, arbitrary real `lambda`,
time-live metric, general `GL(2,R)` screen, on-shell equation, or other completion is included.

## Intrinsic definitions under test

Let `L_T` be the unique timelike Killing line and `L_S` the nonzero Killing-twist line already
verified on the witness. Choose any local unit representatives `T` and `S`. Define

```text
Pi_pair=-T tensor T_flat+S tensor S_flat,
H=identity-Pi_pair,
F_T_ab=H_a^c H_b^d (d T_flat)_cd,
F_S_ab=H_a^c H_b^d (d S_flat)_cd,
Q_T=(1/2) F_T_ab F_T^ab,
Q_S=(1/2) F_S_ab F_S^ab,
Q=Q_S-Q_T.
```

`Q_T`, `Q_S`, and `Q` are candidate metric scalars because all sign choices are squared away. The
old signed contact pair is retained separately: relative to an oriented orthonormal screen it is
`q=(q_T,q_S)`, with `q_T^2=Q_T` and `q_S^2=Q_S`. Its signs are not preregistered as scalars.

The exact candidate formulas to test, not assume as outcomes, are

```text
Q_T=kappa^2 u^(-1-2 lambda),
Q_S=kappa^2 u^(+1-2 lambda),
Q=kappa^2 u^(-1-2 lambda)(u^2-1),
dphi=(1/4) d log(Q_S/Q_T),
dsigma=-(1/4) d log(Q_S Q_T),  sigma=log(|D|/D0)=lambda log u.
```

On the non-null set define the reference-dependent contact coordinate

```text
z=(1/2) log(|Q|/T0^2).
```

The derivative `dz` is tested separately from the absolute reference choice `T0`.

## Controls and strata

1. all three registered `lambda` values are retained;
2. the constant-depth control must not inherit the unproved unique Killing projector;
3. the twist-free control must not acquire a ruler line or pair projector;
4. the prior slice-null control remains ineligible and is not crossed;
5. signs of `T`, `S`, screen orientation, spacetime orientation, and constant rescalings of the
   unnormalized Killing generator are varied algebraically;
6. passive pair/screen-changing coframes must leave tensor contractions unchanged after the
   intrinsic projector is reconstructed; merely relabeling transformed slots is an invalid route;
7. the `Q<0`, `Q=0`, and `Q>0` strata are all retained even if the witness occupies only one;
8. reference shifts in `T0`, `D0`, `phi`, and `sigma` are kept distinct from their derivatives.

No candidate, `lambda`, point, frame, or object classification may be added after outcome.

## Certification and falsification

The production route will use exact exterior/coframe algebra. A fresh verifier must rebuild the
coordinate metric and the projected exterior derivatives independently, without importing the
production functions. Exact symbolic identities certify formulas; nonzero/zero strata use exact
inequalities, not sampled tolerance. Every mutation in `FALSIFICATION_CONTRACT.tsv` must be
exercised.

The result fails or narrows if any candidate scalar changes under an allowed sign, orientation,
Killing-rescaling, chart, or passive-frame choice; if a control is promoted; if the old raw slots
are reused without reconstructing the projector; if a reference-dependent primitive is called
unique; or if the witness is generalized beyond its frozen scope.

## Maximum allowed conclusion

At most: a verified branch-intrinsic descent atlas for the three frozen off-shell witness metrics,
possibly with exact absence of one or more causal strata. No on-shell selection, neighborhood
theorem, universal UDT observable, response law, primitive selection, action, carrier, source,
boundary, density/bootstrap return, `X_max`, matter, mass, stability, or phenomenology may follow.

