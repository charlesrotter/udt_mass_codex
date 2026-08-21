# G200 audit report — primary-metric bidirectional nonradial null response

Date: 2026-08-21

## Landing

```text
ONE_PRIMARY_NONRADIAL_LAW
__FINITE_DIRECTIONAL_DIFFERENCE_IS_RADIAL_REGIME_SAMPLING
```

Grade: `INDEPENDENTLY_VERIFIED_WITH_CAVEATS`

## Result first

The primary static-spherical UDT metric gives the two reversed nonradial null germs the **same
local law**.  At the same event they have the same clock frequency and the same two diagonal
screen tides:

\[
\omega_+=\omega_-=E/\sqrt f,
\]

\[
T_\parallel=\frac{L^2(rf''-f')}{2r^3},
\qquad
T_\perp=\frac{L^2(rf'-2f+2)}{2r^4}.
\]

They can nevertheless produce different finite images.  One branch initially moves toward larger
\(r\), the other toward smaller \(r\), so they sample opposite signs of the same radial tidal
gradient.  With vertex normalization, the first possible difference is

\[
D_{A,+}-D_{A,-}
=-\frac{q_o(\partial_rT_A)_o}{6}\lambda^4+O(\lambda^5).
\]

That is “same orchestra, different part of the score,” not “one direction's instrument is on and
the other's is off.”

## What this changes

G199 showed exact radial reversal symmetry and zero radial optical tide.  G200 now turns on the
primary metric's nonradial angular response without importing the G191--G198 chosen chiral
coframe.  The two branches still start with one common chord.  Directional differences arise only
through finite propagation into different radial regimes.

This is compatible with Charles's proposed loud-at-both-extremes/quiet-near-\(\phi=0\) picture, but
does not derive that full magnitude profile.  Such a claim still requires the supplied primary
history \(f(r)=e^{-2\phi(r)}\) to have the corresponding behavior.

## Evidence

- preregistered and pushed at commit `7b92835e` before confirmatory implementation;
- 64/64 exact symbolic assertions from direct inverse-metric, Christoffel, Riemann, geodesic,
  quotient-screen, tidal, and Jacobi-series reconstruction;
- 2,000 independent exact-`Fraction` third-jet controls and 38,160 assertions;
- all 2,000 controls had a nonzero tidal-gradient mode;
- 40 independent flat controls;
- no production import or artifact read by the independent replay;
- hostile mutation catches, source hashes, no-write replay, premise verifier, repository tests,
  and diff checks are recorded in `EVIDENCE_GATES.md`.

## Four gates

1. Preregistered: yes.
2. Full or bounded: full local same-event result and vertex series through \(O(\lambda^4)\) for the
   two reversed equatorial nonradial germs of every smooth positive primary-metric third jet with
   \(r_o>0\); longer finite paths and turning/cut/focal strata are excluded.
3. Independent: yes, exact-rational radial-dual reconstruction from metric coordinate jets.
4. Premises: audited; the profile, query, calibration, and local branch are supplied, while
   completed-pair Dual Reciprocity retains its working foundational grade.

## Maximum conclusion

The primary metric has one reversal-symmetric local nonradial frequency/tide law.  Finite
directional differences can emerge natively because reversed branches sample different radii of
the same supplied metric history.  G200 does not select that history, derive the full regime
amplitude, or make an observational prediction.
