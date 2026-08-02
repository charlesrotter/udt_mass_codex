# Intrinsic contact descent on the explicit twisted `S3` witness

## Production result

`METRIC_DERIVED_PROJECTOR_MAKES_QT_QS_Q_INTRINSIC_ON_EXPLICIT_WITNESS__Q_POSITIVE__ALTERNATING_CONTACT_TWO_FORM_ZERO__GENERAL_SCREEN_AND_SELECTION_OPEN`.

On each of the three frozen `lambda=-1,0,+1` off-shell witness metrics, the previously derived
clock/ruler lines define a sign-independent pair projector and orthogonal screen projector. The
screen-projected exterior derivatives of the unit clock and ruler one-forms give three
orientation-free metric scalars:

```text
Q_T=4 u^(-1-2 lambda),
Q_S=4 u^(+1-2 lambda),
Q=Q_S-Q_T=4 u^(-1-2 lambda)(u^2-1).
```

Because `4<=u<=11`, `Q` is strictly positive through the complete cell for all three registered
metrics. The null and negative contact strata are absent on this witness, not refuted elsewhere.

## What descends—and what does not

On the frozen `a=R=1` witness the dimensionless ratio also reconstructs an absolute branch scalar,
and its derivative reconstructs depth:

```text
Phi_contact=(1/4)log(Q_S/Q_T)=phi,
dphi=(1/4)d log(Q_S/Q_T),
dsigma=-(1/4)d log(Q_S Q_T)=2 lambda dphi.
```

For general unfrozen constants this scalar would read `phi+(1/2)log(R/a)`, so it does not supply a
universal zero. The absolute screen-area log and contact log retain dimensional reference freedom;
their differentials are intrinsic. Signed contact components remain a sign/orientation local
system; screen axes, first-Cartan slots, and connection coefficients remain frame dependent. Path
holonomy still needs a path, and no global carrier section follows.

The decisive limitation is exact:

```text
dphi wedge dz=dphi wedge dsigma=0.
```

The projector closes the prior authority/descent obstruction on this explicit witness, but the
frozen screen area is only a function of depth. This witness therefore contains no independent
depth–angular alternating response.

## Scope

This is one exact complete-cell configuration atlas. It does not cover a general `GL(2,R)` screen,
independently varying area/shears, other profiles or completions, time-live metrics, geodesic
completeness, or any on-shell equation. No action, source, boundary, density/bootstrap return,
carrier, `X_max`, matter, mass, stability, phenomenology, or universal UDT observable is selected.

## Verification

Production exact algebra, 22 parent-object classifications with two O13 subclassifications, three
lambda certificates, ten controls, and 24 fail-closed mutations pass. A fresh zero-context
adversary independently rebuilt the stereographic metric, Hodge-normalized Killing twist,
projectors, and projected exterior derivatives with PyTorch coordinate autodiff. Across all three
lambda values at three parent points plus the `u=4,11` endpoints, the maximum `Q_T,Q_S,Q` error was
`3.98e-12`, raw-twist normalization error `1.44e-15`, and projector-idempotence error `6.74e-15`.

The first return caught the bundled O13 classification: the frozen unit witness fixes absolute
`Phi_contact=phi`, while absolute `sigma` remains reference-dependent. The preregistration was
preserved, the stable O13 parent was subclassified, and a fresh follow-up returned `VERIFIED`.

Final evidence grade:
`VERIFIED_EXACT_WITNESS_LOCAL_INTRINSIC_CONTACT_DESCENT`.
