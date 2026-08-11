# Preregistration — native observer-query SNe replay and regrading

Date: 2026-08-11

Mode: `MAP -> OBSERVE`; CPU only

Question type: metric-led provenance/replay, not a new cosmology fit

## Whole question

Reproduce the latest frozen M3 Pantheon+ SNe result without changing its data, cuts, covariance,
profile menu, fit freedom, or anchor. Then determine whether the corrected UDT observer-query
architecture changes the prediction when it is applied with **no new physical choice**.

Here “better natively” has one permitted meaning: a formula already forced by the corrected native
geometry may score differently with the same statistical freedom. It does not authorize an added
profile term, coefficient, branch choice, screen, transport, source, bootstrap rule, or retuning.

## Frozen replay universe

The baseline universe is exactly the historical M3 V-SNe universe:

- Pantheon+SH0ES catalog and STAT+SYS covariance identified in `SOURCE_MANIFEST.tsv`;
- all 18 fits: modes A/B/C and D on `zCMB`, plus D on `zHD` and `zHEL`, each with P1/P2/P3;
- each mode's historical cuts, covariance treatment, nuisance structure, optimizer bounds, and
  external mode-B anchor unchanged;
- the committed `sne_results.json` is the frozen reference return;
- no BAO or CMB datum is read by the calculation.

The regrading universe contains exactly the same three endpoint profile families, now written in
terms of the terminal reciprocal coordinate on a supplied regular calibrated pair relation:

```text
phi_pair = log(1+z),
d_L = exp(2 phi_pair) d_A,
d_A = r(phi_pair)
```

with the historical P1/P2/P3 `r(phi_pair)` formulas. The last two lines remain the registered
conditional SNe area/optical readout; they are not silently promoted into a universal consequence
of the complete metric.

## Premise discipline

`PREMISE_LEDGER.tsv` is controlling. In particular:

- reciprocal `c_E` is the observed calibration anchor and cancels from the dimensionless shape;
- `phi_pair` is derived as the reciprocal log-imbalance only **after** a regular calibrated pair
  relation is supplied;
- identifying `phi_pair=log(1+z)` is conditional on the registered SNe redshift query;
- P1/P2/P3 are a frozen historical profile menu, not the complete metric solution space;
- `d_A=r` and `d_L=(1+z)^2d_A` are conditional measurement/readout premises;
- common scale, shift, time dependence, angular screen, mixing, extrinsic data, path/holonomy, and
  global branch data are not declared absent. The historical scalar fit simply does not own or
  determine them;
- P1 remains an observer-pair/SNe profile and is not promoted into a smooth centered CMB lapse.

## Falsification and certification contract

1. Every source hash must match `SOURCE_MANIFEST.tsv` before and after the run.
2. The production replay must reproduce all numerical fields of all 18 frozen results to absolute
   tolerance `5e-9` for floating values and exact equality for labels, counts, and booleans.
3. An independent implementation must reconstruct the primary A:`zCMB`:P1 profile, its best shape,
   profiled offset, chi-square, the fixed `n=1` chi-square difference, and the mode-B scale without
   importing the production fitting functions. Required absolute tolerances are `2e-6` in shape,
   `2e-6` in offset, `2e-5` in chi-square, and `5e-3 Mpc` in scale.
4. Exact symbolic checks must prove that rewriting each historical profile through
   `phi_pair=log(1+z)` returns the same `r(z)` and `d_L(z)` formula.
5. A nonzero “native correction” may be evaluated only if one frozen source uniquely supplies its
   complete SNe query, screen/area readout, branch, and coefficient-free formula. Otherwise its
   status is `OPEN_NOT_OWNED`, and no correction is inserted.
6. Catch-proofs must reject: changed data/cut/menu/anchor; an extra shape coefficient; use of CMB or
   BAO data; P1 promoted to a centered complete lapse; `c_eff` called a material signal speed;
   angular/mixing channels called zero; and an unowned orchestra correction.
7. Full repository tests and current premise guards must remain at their documented baseline.

## Registered outcome classes

- `REPLAY_OBSTRUCTED`: a source/hash/environment failure prevents exact replay.
- `BASELINE_REPRODUCED__NATIVE_RETYPE_ALGEBRAICALLY_IDENTICAL`: all replay and equivalence gates
  pass; no numerical improvement follows from semantics alone.
- `OWNED_NATIVE_FORMULA_DIFFERS`: an already-owned coefficient-free complete-query formula differs;
  report its score in either direction without retuning.
- `NO_OWNED_COMPLETE_SNE_QUERY_CORRECTION`: the complete orchestra may matter structurally, but the
  existing sources do not select its SNe realization; no numerical comparison is lawful.

The second and fourth outcomes may coexist.

## Maximum allowed conclusion

This work may certify reproduction and correct the interpretation of the SNe result. It may not
derive a physical observer query, a universal `c_eff`, a signal law, `X_max`, a CMB profile, an
action, source, bootstrap closure, matter, mass, or a complete cosmology.
