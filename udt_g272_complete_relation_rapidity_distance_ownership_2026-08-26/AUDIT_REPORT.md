# G272 audit report — complete relation rapidity and distance ownership

Date: 2026-08-26

## Landing

```text
COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_TRANSPORTED_RAPIDITY_STATE
__PLANAR_TANH_DELTA_IS_EXACT_STRATUM
__SCREEN_STATE_PREVENTS_DELTA_ONLY_COMPLETENESS
__CONVENTIONAL_DISTANCE_SCALE_PROFILE_HISTORY_AND_XMAX_REMAIN_OPEN
```

## Result

For a supplied complete null relation, define

\[
\eta_{\rm PT}=\operatorname{arcosh}\Gamma_{\rm PT},
\qquad
\rho_{\rm PT}=\tanh\eta_{\rm PT}.
\]

The metric owns these dimensionless quantities exactly after the branch and endpoint clocks are
supplied. They satisfy

\[
M_{\rm PT}=\operatorname{sech}\eta_{\rm PT},
\qquad
M_{\rm PT}^2+\rho_{\rm PT}^2=1.
\]

The bounded state is the norm of the full transported-frame spatial decomposition, including the
G269 screen mismatch. Therefore the radial result

\[
\chi=\tanh\delta=\tanh(\phi_B-\phi_A)
\]

is an exact oriented planar stratum, not the complete nonradial scalar by itself.

## Distance implication

If the original mutual-distance postulate is later adopted in the precise form

\[
x/X=\chi,
\]

then the primary radial profile follows exactly:

\[
\phi(x)-\phi_A=\operatorname{artanh}(x/X),
\qquad
e^{-2(\phi-\phi_A)}=\frac{1-x/X}{1+x/X}.
\]

G272 does not adopt that identification. It shows that this is now the smallest visible ownership
question; no arbitrary fitted profile is required after the identification is supplied.

## Scope

The result does not attach metres or megaparsecs, determine `X`, select a query population, choose a
complete history, or derive `X_max`. `c_E` supplies a clock/ruler conversion `L/T`, not a standalone
length. No observation, fit, source, matter model, action, or field equation was used.

## Evidence

- preregistered at commit `2dae5034`;
- 20/20 symbolic checks;
- 24,000 independent complete-pair cases;
- 168,530 exact-fraction assertions;
- five formula/type mutations caught;
- six textual scope-regression catches passed.
- external Codex `gpt-5.4`: `ACCEPT_BOUNDED_G272_LEAD`; no repairs.

Current grade: `EXTERNALLY_REVIEWED_BOUNDED_LEAD__NO_REPAIRS`.
