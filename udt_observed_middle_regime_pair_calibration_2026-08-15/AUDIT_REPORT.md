# Audit report — observed middle-regime observer-pair calibration

Date: 2026-08-15

Status:

```text
INTERNALLY_VERIFIED_WITH_CAVEATS
__OBSERVED_CONDITIONAL_TERMINAL_CALIBRATION_FROZEN
```

## Result

The already verified Pantheon+ P1 relation is now frozen once as UDT's provisional observational
middle-regime calibration. No new fit was run and no BAO, CMB, endpoint, `X_max`, bootstrap, or
protected-package result was read.

The frozen object is deliberately narrower than a spacetime history:

```text
dL_cal(z)=n X_eff (1+z)^2 [1-(1+z)^(-2/n)],

n=1.0559332414320268,
X_eff=2085.9586748597476 Mpc  [conditional on M_B and the registered transfer],
0.02307 <= zCMB <= 2.2613.
```

The accompanying terminal relation is

```text
phi_pair=log(1+z),
c_eff^(pair)/c_E=(1+z)^(-2).
```

It is an inter-frame readout, not local signal-speed physics.

## What changed

Before G99, P1 was retained as a conditional low-redshift compatibility anchor. G99 makes one
explicit development choice: use its already observed central relation as the frozen middle chord
against which future complete histories and independent observational lanes must be tested.

This is an `OBSERVED/CONDITIONAL` premise, not a claim that the metric derived P1. It eliminates
future freedom to refit `n` or `X_eff` using BAO, CMB, or endpoint behavior. It does not eliminate
the upstream complete-history freedom exposed by G98.

## Important typing correction

SNe magnitudes calibrate the effective `dL(z)` relation. Decomposing it into

```text
d_A=r_cal,
d_L=(1+z)^2 d_A
```

still uses the registered conditional area/transfer convention. The physical carrier, screen-area
map, `eta`, `epsilon`, source population, and caustic completion remain open.

## Evidence

- 10/10 preregistered source hashes pass;
- production extraction used no optimizer and read no holdout;
- a standalone standard-library implementation independently reconstructed all parameters and six
  preregistered curve nodes, with maximum absolute disagreement `1.137e-13`;
- origin, slope, positivity, monotonicity, and factorization checks pass;
- 11/11 hostile semantic mutations are rejected;
- package verifier passes 25/25 checks;
- current premise verifier passes 99 guards on the final 87-row registry;
- repository tests pass `90 passed, 1 xfailed`.

## Caveats

1. The absolute scale carries `M_B=-19.253 +/- 0.027` and the conditional luminosity readout.
2. The frozen artifacts do not contain the full joint `(n,X_eff)` covariance. Separate profile
   intervals may not be combined as an independent box; no rigorous joint uncertainty band or
   marginal `R_w` interval is owned.
3. The primary `m_b_corr` layer is BBC-bias-corrected and remains LCDM-adjacent observational
   processing. The previously banked mode-C and redshift-column shifts travel as diagnostics.
4. No complete `B,Q,S,Y,Z` history, physical `J`, cross-regime score, or time-live continuation is
   selected.
5. Fresh external semantic review of the G99 adoption has not been performed. The underlying G65
   fit and retyping were externally verified.

## Four gates

1. **Preregistered — PASS.** Commit `5587c62e` froze the object, source universe, holdouts,
   certification contract, and conclusion ceiling before result generation.
2. **Full or bounded — PASS.** Complete for adopting and typing the registered G65 central P1
   relation; not complete for a joint uncertainty surface, all SNe queries, or complete histories.
3. **Independently verified — PASS WITH CAVEAT.** A separate direct-power standard-library route
   reconstructs the result. This is independent finite-dimensional replay; no fresh external G99
   semantic adversary has yet reviewed the adoption.
4. **Premises audited — PASS.** Shape, anchor, transfer, screen, complete-history, holdout, signal,
   `X_max`, bootstrap, action, source, matter, and mass roles are explicitly separated.

## Maximum conclusion

G99 freezes one observed conditional middle-regime observer-pair luminosity relation. It does not
derive the physical spacetime history, native transfer, loud ends, `X_max`, cosmology, action,
source, matter, mass, or bootstrap closure.

## Next bounded action

Before opening a holdout, derive and preregister its observable map from the complete pair
geometry. The strongest next candidate is the BAO observer-angle query because the raw R2--R5 data
lane is prepared. Its map must be written without reading the BAO curves and without importing a
standard-ruler or Lambda-CDM interpretation. Only then may the frozen G99 calibration be exposed to
the BAO holdout.
