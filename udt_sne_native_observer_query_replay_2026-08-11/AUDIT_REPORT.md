# Audit report — native observer-query SNe replay and regrading

Date: 2026-08-11

Status: **EXTERNALLY REVIEWED — VERIFIED WITH CAVEATS**

## Result

The latest native SNe result reproduces exactly, and the corrected observer-query framing leaves
its numerical formulas unchanged.

```text
BASELINE_REPRODUCED__NATIVE_RETYPE_ALGEBRAICALLY_IDENTICAL
AND
NO_OWNED_COMPLETE_SNE_QUERY_CORRECTION
```

This is useful progress, but not an automatic fit improvement. The corrected geometry places the
successful P1 relation in its proper home: a conditional terminal observer-pair/SNe readout. The
full angular/mixing orchestra can influence that terminal readout upstream, but the current bank
does not yet select the complete SNe pair immersion, screen-area law, time-live trajectory, or
coefficient-free correction. Nothing extra was inserted.

## Reproduction

The unchanged production path replayed all `18` historical M3 fits:

```text
compared stored leaf fields:       443
maximum absolute numeric change:  0.0
```

The primary A:`zCMB`:P1 result remains:

```text
1/n = 0.9470295666076658
n   = 1.0559332414320268
chi2/dof = 1260.8480887040496 / 1365
```

The mode-B external anchor still conditionally gives:

```text
X_eff = 2085.9586748597476 Mpc
R_w at best n = 2202.6331050379085 Mpc
```

These absolute values retain the frozen `M_B=-19.253 +/- 0.027` external-anchor premise.

## Independent reconstruction

A separate implementation did not import the production fitter. It used NumPy Cholesky whitening,
an independently written P1 formula, a 208-point full-bounds control scan, and a separate bounded
scalar minimizer. It found:

```text
1/n = 0.9470305108426823
n   = 1.0559321886157444
chi2 = 1260.8480887249352
X_eff = 2085.9590069567967 Mpc
Delta chi2(n=1) = 7.944900501660641
one-parameter equivalent = 2.8186699880725024 sigma
```

Every value is inside the preregistered tolerance. The result remains an observed conditional P1
shape, not a derivation of `n`, `R_w`, or `X_max`.

## Native retyping result

All `9/9` exact symbolic checks pass. On a supplied regular calibrated SNe pair relation,

```text
phi_pair=log(1+z)
```

turns the three historical `r(phi_pair)` families into exactly the same P1/P2/P3 `r(z)` and
`d_L(z)` formulas already fitted. The conditional pair-cone identity becomes

```text
c_eff^(pair)/c_E=(1+z)^(-2),
```

with `c_E` cancelling from the dimensionless shape. This is not a material signal-speed claim.

The area/flux join

```text
d_A=r,
d_L=(1+z)^2 d_A
```

remains a conditional registered SNe readout. It is not newly derived from the complete metric by
the act of retyping `phi`.

## Ownership result

`CORRECTION_OWNER_LEDGER.tsv` separates the relevant layers. The bank owns:

- the terminal reciprocal coordinate on a supplied calibrated pair relation;
- the conditional supplied-pair cone ratio;
- the structural fact that angular and mixing components can modulate `phi_pair` before readout;
- P1's conditional observer-pair/SNe role.

It does not own:

- the physical complete SNe pair immersion or branch;
- the complete SNe screen-area map;
- the physical time-live curve through the orchestra atlas;
- a bootstrap selector;
- any coefficient-free native correction to the frozen P1/P2/P3 readout.

Therefore “native improvement” is still a legitimate possibility, but not yet a defined
calculation. A lower chi-square cannot be obtained honestly by interpreting the same formula more
natively; it requires the missing upstream geometry to determine a genuinely different formula.

## Scope and completeness

This covers the full frozen 18-fit M3 universe and the exact retyping of all three frozen profile
families. It does not cover every SNe query, complete metric branch, screen, cut-locus realization,
time-live solution, source model, or observational catalog. The historical scalar fit freezes or
omits complete-query channels and cannot be promoted to a full-metric solution-space census.

No BAO/CMB data, bootstrap, action, source, matter, mass, or GPU calculation entered.

## Four gates

1. Preregistered: **YES**, commit `b585572f`; one-character source-hash correction separately
   preregistered and committed at `307144b5` before the numerical replay.
2. Full or bounded scope justified: **YES**, complete for the frozen 18-fit M3 universe and three
   exact profile retypings; not complete for all SNe realizations or full UDT geometry.
3. Independently verified: **YES WITH CAVEATS**. Production replay, independent primary
   reconstruction, `9/9` exact checks, `14/14` scope catches, and a fresh sealed gpt-5.4 review
   pass. The reviewer reproduced the science and ownership conclusion, found one replay leaf-type
   weakness, and retained `VERIFIED_WITH_CAVEATS`. The preregistered correction adds `3/3` type
   controls and raises the final package verifier to `43/43`; see
   `EXTERNAL_REVIEW_ADJUDICATION.md`.
4. Premises audited: **YES**, including the external absolute anchor, BBC-adjacent layer,
   conditional area/flux readout, P1 role guard, live orchestra, inactive bootstrap, and open
   physical pair realization.

Repository gates at this stage:

```text
pytest: 98 passed, 1 xfailed
current premise guard: 63 PASS
```

## Next step

If the external review sustains the result, retain SNe as a low-redshift conditional compatibility
anchor and return to the actual CMB observation query. Do not copy P1 into a centered CMB lapse.
The CMB query must expose its own endpoint, screen/area, Jacobi, ambient-transport, and
normal-transport channels. Any complete geometry selected there can later be projected back through
this SNe query to test whether it predicts the observed P1-like relation without extra freedom.
