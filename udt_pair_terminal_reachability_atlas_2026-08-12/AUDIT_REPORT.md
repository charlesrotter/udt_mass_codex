# Audit report — pair-terminal reachability atlas

Date: 2026-08-12

Status: **FRESH ADVERSARIALLY REVIEWED — VERIFIED WITH CAVEATS**

## Result

The complete zero-order solution space is analytically closed for one fixed symbolic
A-calibrated Lorentzian base pair metric.

After removing the base shift by an invertible covector shear, write

```text
h0=diag(-t,ell),
G=[[p,m],[m,n]]>=0.
```

Every completed signature is classified by

```text
det(h)=(p-t)(ell+n)-m^2.
```

The exact terminal image is

```text
0<T^2<=T0^2,
L^2>=L0^2,
(T0^2-T^2)(L^2-L0^2)
    >=T0^2 T^2 (beta-beta0)^2.
```

These conditions are necessary and sufficient. An explicit inverse reconstructs the unique
shift-removed Gram matrix and therefore a complete-orchestra factor.

## Main structural consequence

Within the same A-calibrated chart, PSD orchestra additions are ordered:

```text
T<=T0,
L>=L0,
phi>=phi0,
c_eff^(pair)/c_E <= its base value.
```

The inequalities are strict away from the base for `phi` and the pair-calibration ratio. This is
a fixed-base, zero-order observer-pair result. It is not a local signal-speed law and does not
identify the `T->0` chart boundary with physical `X_max`.

## Evidence

- preregistration committed before derivation: `7ce7b634`;
- 12/12 exact SymPy identities;
- 324-case production rational atlas spanning all Gram ranks and completed signatures;
- hermetic stdlib `Fraction` replay: 328 forward cases and 146 inverse targets;
- exact pair-basis congruence and screen-frame rotation controls;
- 8/8 hostile catches.

A fresh, read-only adversarial rederivation added 2,279 forward PSD cases, 776 independently
constructed admitted targets, and 7,050 exact Loewner-order comparisons. It reproduced all theorem
boundaries and the stored 324-row atlas. All 6,815 nonzero comparable increments that remained in
the A-terminal chart strictly increased `phi`.

## Important retained boundary

The full Gram atlas is larger than the terminal chart. At `h00=0`, the completed form may be
degenerate or still Lorentzian. For larger clock-slot Gram content it may remain Lorentzian or
become degenerate or positive definite. These are classified states, not solver failures.

The completed form, signature, and Gram rank are congruence-covariant. The terminal variables and
their reachability inequality are deliberately A-calibrated readouts, not invariants under an
arbitrary replacement of the observer calibration axis.

## Scope ceiling

No derivative response, time-live history, physical branch, path composition, action, source,
matter, bootstrap, `X_max`, SNe, CMB, material signal, or dynamics is selected. The pointwise
atlas does not prove that arbitrary reachable states coexist in one smooth or on-shell global
history.

## Next bounded question

The local chord vocabulary is now closed at zero order. The next scientific choice is between a
matched first-/second-jet compatibility atlas (how chords can vary) and a global network-descent
audit (how edge readouts compose). Neither is launched by this package.
