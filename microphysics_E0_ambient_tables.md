# Microphysics re-entry E0 -- extracted ambient tables (N=0 fundamentals)

**Date:** 2026-07-03. **Stage:** E0 (EXTRACTION ONLY; pre-registration = `microphysics_reentry_miniMAP.md`). **Script:** `microphysics_E0_extract.py`; full dense profiles (~2500 pts/bracket) in `microphysics_E0_ambient_tables.json`. **No new physics; no interpretation.** Solver = banked `cell_solver_universe_T3.rhs` via `cascade_stageA_lib` (all EOM/fold/anchor provenance tags inherited).

Definitions implemented (cited): H_amb = the conserved radial corner Hamiltonian `H = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho)` (embedded_cell_closure_H_amb_results.md:29,36-38 == cell_solver_universe_T3.py:119); sigma_ma = (e^{2phi}/4) U'(rho) (universe_cell_fold_jc_sigma_results.md:75-76, potential-only); sigma_geo from the geometry via m'_MS = 4 pi rho^2 rho' eps (doc:94; derive_universe_einstein_d3.py:122-124, m'_MS by 5-pt numerical FD -- non-circular) with sigma isolated per derive_universe_einstein_d3.py:108-110.

## A1 m=3 Z=8

- a* banked = 1.4813439688814254; **a* re-shot = 1.4813439682567** (rel drift 4.22e-10); two-method verify: CONFIRMED
- r_s = 577.502698, rho_s = 2.26140213, rho_c = 1.0000000000, q = 12.6244424439 (banked 12.62444244426475)

**Identity gates (solver-correctness):**

| gate | value |
|---|---|
| Delta-phi - ln(1101) | +2.665e-15 |
| phi(r_s) (event residual) | +2.717e-15 |
| 2m/rho core / seal | 1.000000000000 / 1.000000000000 |
| E_m(core) - 2 | +0.000e+00 (U(rho_c)=2 built into the slice normalization -- exact by construction) |
| H drift max / H(seal) | 1.924e-10 / -1.547e-11 |
| rho'(r_s) at root (miss) | -1.729e-12 |
| U_seal conservation identity residual | -1.547e-11 |
| sigma two-route residual (rel, interior mask) | max 4.078e-09, median 2.754e-10 (271 pts) |
| N_delta / N_rhop / N_phip (graduated floors [1e-06, 1e-07, 1e-08, 1e-09, 1e-10]) | {0} / {0} / {0} |

**Turning-point / fold map:** interior rho'=0 zeros: NONE; interior phi'=0 zeros: NONE. Folds: r_c=0 (phi'=rho'=0 exact ICs), r_s=577.5027 (rho'=0 seal root; phi'(r_s)=q/(Z rho_s^2)>0, NOT a phi-turning point). N=0 confirmed: no interior turning points.

**Station wall data** (core fold, 5 even interior stations, outer seal; sigma_geo is 0/0-indeterminate AT the folds -- reported None there, honest):

| station | r | phi | phip | rho | rhop | H_amb | sigma_ma | sigma_geo | e2phi | E_m | m_MS | two_m_over_rho | pi_phi_qflux | pi_rho |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core_fold | 0 | -7.00397 | 0 | 1 | 0 | 0 | 1.53902e-08 | None | 8.24946e-07 | 2 | 0.5 | 1 | 0 | -0 |
| interior_1of6 | 96.1542 | -7.00295 | 4.23799e-05 | 1.00007 | 1.47724e-06 | 6.50147e-13 | 1.52466e-08 | 1.52466e-08 | 8.2663e-07 | 2.00001 | 0.500034 | 0.999997 | 0.000339087 | -7.14826 |
| interior_2of6 | 192.597 | -6.9876 | 0.000340212 | 1.00029 | 3.01619e-06 | 6.44818e-13 | 1.51749e-08 | 1.51749e-08 | 8.52401e-07 | 2.00002 | 0.500138 | 0.999989 | 0.00272326 | -14.1539 |
| interior_3of6 | 288.751 | -6.92021 | 0.00118568 | 1.00067 | 5.0724e-06 | 5.76428e-13 | 1.62585e-08 | 1.62585e-08 | 9.75408e-07 | 2.00005 | 0.50032 | 0.999974 | 0.00949806 | -20.8011 |
| interior_4of6 | 384.906 | -6.72334 | 0.00320917 | 1.00134 | 9.71224e-06 | 4.72955e-13 | 2.12154e-08 | 2.12154e-08 | 1.44604e-06 | 2.00009 | 0.500636 | 0.999935 | 0.0257421 | -26.8658 |
| interior_5of6 | 481.348 | -6.17797 | 0.00957578 | 1.00305 | 3.41301e-05 | -1.24167e-12 | 4.12057e-08 | 4.12057e-08 | 4.30413e-06 | 2.00017 | 0.50139 | 0.999729 | 0.0770745 | -31.7185 |
| outer_seal | 577.503 | 2.71678e-15 | 0.308579 | 2.2614 | -1.7285e-12 | -1.54678e-11 | -0.0700935 | None | 1 | 0.0521799 | 1.1307 | 1 | 12.6244 | 6.914e-12 |

## A1 m=3 Z=1

- a* banked = 1.4942743251421744; **a* re-shot = 1.4942743250396** (rel drift 6.87e-11); two-method verify: CONFIRMED
- r_s = 620.426082, rho_s = 1.36180608, rho_c = 1.0000000000, q = 1.4808683519 (banked 1.480868375016805)

**Identity gates (solver-correctness):**

| gate | value |
|---|---|
| Delta-phi - ln(1101) | -3.109e-14 |
| phi(r_s) (event residual) | -3.086e-14 |
| 2m/rho core / seal | 1.000000000000 / 1.000000000000 |
| E_m(core) - 2 | +0.000e+00 (U(rho_c)=2 built into the slice normalization -- exact by construction) |
| H drift max / H(seal) | 6.924e-11 / +6.911e-11 |
| rho'(r_s) at root (miss) | +1.849e-12 |
| U_seal conservation identity residual | +6.911e-11 |
| sigma two-route residual (rel, interior mask) | max 5.087e-10, median 1.622e-11 (239 pts) |
| N_delta / N_rhop / N_phip (graduated floors [1e-06, 1e-07, 1e-08, 1e-09, 1e-10]) | {0} / {0} / {0} |

**Turning-point / fold map:** interior rho'=0 zeros: NONE; interior phi'=0 zeros: NONE. Folds: r_c=0 (phi'=rho'=0 exact ICs), r_s=620.4261 (rho'=0 seal root; phi'(r_s)=q/(Z rho_s^2)>0, NOT a phi-turning point). N=0 confirmed: no interior turning points.

**Station wall data** (core fold, 5 even interior stations, outer seal; sigma_geo is 0/0-indeterminate AT the folds -- reported None there, honest):

| station | r | phi | phip | rho | rhop | H_amb | sigma_ma | sigma_geo | e2phi | E_m | m_MS | two_m_over_rho | pi_phi_qflux | pi_rho |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core_fold | 0 | -7.00397 | 0 | 1 | 0 | 0 | 4.72337e-09 | None | 8.24946e-07 | 2 | 0.5 | 1 | 0 | -0 |
| interior_1of6 | 103.301 | -7.00295 | 3.9573e-05 | 1.00003 | 4.86783e-07 | 4.88498e-14 | 4.67077e-09 | 4.67087e-09 | 8.26636e-07 | 2 | 0.500012 | 1 | 3.9575e-05 | -2.35549 |
| interior_2of6 | 206.912 | -6.98757 | 0.000317078 | 1.0001 | 9.9213e-07 | 4.88498e-14 | 4.6223e-09 | 4.62246e-09 | 8.5246e-07 | 2 | 0.50005 | 0.999999 | 0.000317142 | -4.65537 |
| interior_3of6 | 310.213 | -6.92021 | 0.00110137 | 1.00024 | 1.66301e-06 | 4.13003e-14 | 4.89675e-09 | 4.8966e-09 | 9.75399e-07 | 2.00001 | 0.500116 | 0.999997 | 0.00110189 | -6.81983 |
| interior_4of6 | 413.514 | -6.72436 | 0.0029633 | 1.00047 | 3.16169e-06 | 3.10862e-14 | 6.22783e-09 | 6.22782e-09 | 1.44308e-06 | 2.00001 | 0.500232 | 0.999993 | 0.00296609 | -8.76372 |
| interior_5of6 | 517.125 | -6.18746 | 0.00870297 | 1.00106 | 1.0829e-05 | -1.50102e-13 | 1.07439e-08 | 1.07438e-08 | 4.22322e-06 | 2.00002 | 0.500518 | 0.999972 | 0.00872148 | -10.2566 |
| outer_seal | 620.426 | -3.08616e-14 | 0.79852 | 1.36181 | 1.8486e-12 | 6.91127e-11 | -0.657486 | None | 1 | 1.40875 | 0.680903 | 1 | 1.48087 | -7.3944e-12 |

## A3 Z=8

- a* banked = 0.9762462714900255; **a* re-shot = 0.9762462704088** (rel drift 1.11e-09); two-method verify: CONFIRMED
- r_s = 720.990651, rho_s = 2.42108235, rho_c = 1.0000000000, q = 11.1655353477 (banked 11.165535352874318)

**Identity gates (solver-correctness):**

| gate | value |
|---|---|
| Delta-phi - ln(1101) | -3.642e-14 |
| phi(r_s) (event residual) | -3.649e-14 |
| 2m/rho core / seal | 1.000000000000 / 1.000000000000 |
| E_m(core) - 2 | +0.000e+00 (U(rho_c)=2 built into the slice normalization -- exact by construction) |
| H drift max / H(seal) | 1.147e-10 / +5.236e-11 |
| rho'(r_s) at root (miss) | +3.507e-13 |
| U_seal conservation identity residual | +5.236e-11 |
| sigma two-route residual (rel, interior mask) | max 5.077e-09, median 1.014e-10 (262 pts) |
| N_delta / N_rhop / N_phip (graduated floors [1e-06, 1e-07, 1e-08, 1e-09, 1e-10]) | {0} / {0} / {0} |

**Turning-point / fold map:** interior rho'=0 zeros: NONE; interior phi'=0 zeros: NONE. Folds: r_c=0 (phi'=rho'=0 exact ICs), r_s=720.9907 (rho'=0 seal root; phi'(r_s)=q/(Z rho_s^2)>0, NOT a phi-turning point). N=0 confirmed: no interior turning points.

**Station wall data** (core fold, 5 even interior stations, outer seal; sigma_geo is 0/0-indeterminate AT the folds -- reported None there, honest):

| station | r | phi | phip | rho | rhop | H_amb | sigma_ma | sigma_geo | e2phi | E_m | m_MS | two_m_over_rho | pi_phi_qflux | pi_rho |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core_fold | 0 | -7.00397 | 0 | 1 | 0 | 0 | 9.91553e-09 | None | 8.24946e-07 | 2 | 0.5 | 1 | 0 | -0 |
| interior_1of6 | 120.045 | -7.00295 | 3.4224e-05 | 1.00007 | 1.18801e-06 | 4.98712e-13 | 9.81732e-09 | 9.81719e-09 | 8.26644e-07 | 2 | 0.500035 | 0.999998 | 0.000273831 | -5.7486 |
| interior_2of6 | 240.45 | -6.98748 | 0.000274571 | 1.00029 | 2.42478e-06 | 4.95159e-13 | 9.75531e-09 | 9.75536e-09 | 8.5262e-07 | 2.00001 | 0.50014 | 0.999993 | 0.00219783 | -11.3757 |
| interior_3of6 | 360.495 | -6.9196 | 0.000956127 | 1.00067 | 4.07748e-06 | 4.48086e-13 | 1.04244e-08 | 1.04243e-08 | 9.76592e-07 | 2.00003 | 0.500326 | 0.999983 | 0.00765926 | -16.7008 |
| interior_4of6 | 480.54 | -6.7215 | 0.00258568 | 1.00134 | 7.81349e-06 | 3.83249e-13 | 1.35325e-08 | 1.35325e-08 | 1.45137e-06 | 2.00006 | 0.50065 | 0.999958 | 0.0207411 | -21.5342 |
| interior_5of6 | 600.946 | -6.17315 | 0.00770981 | 1.00307 | 2.75357e-05 | -8.71747e-13 | 2.55479e-08 | 2.55479e-08 | 4.34581e-06 | 2.00011 | 0.501446 | 0.999826 | 0.0620574 | -25.3446 |
| outer_seal | 720.991 | -3.64948e-14 | 0.238106 | 2.42108 | 3.50673e-13 | 5.23641e-11 | -0.130494 | None | 1 | 0.670709 | 1.21054 | 1 | 11.1655 | -1.40269e-12 |

## A3 Z=1

- a* banked = None; **a* re-shot = 0.9928086029892** (rel drift FRESH (Stage-A budget-cut; see note)); two-method verify: CONFIRMED
- r_s = 784.414776, rho_s = 1.35295717, rho_c = 1.0000000000, q = 1.0717827824
- NOTE: A3 Z=1 was Stage-A BUDGET-CUT (no banked a*); fundamental converged fresh (coarse grid + same-sign-run subdivision; nodeless N_delta=N_rhop=0 selection). Coarse grid's own first crossing is the N=2 member -- the Stage-A even-pair hazard, confirmed live.
- fresh-hunt below-stuck roots (all refined + N-diagnosed): p*=0.9928086030 N_delta=0 N_rhop=0 q=1.0718; p*=0.9948382694 N_delta=1 N_rhop=1 q=0.3962; p*=0.9954460049 N_delta=2 N_rhop=2 q=0.2859; p*=0.9959433029 N_delta=3 N_rhop=3 q=0.2151; p*=0.9962974266 N_delta=4 N_rhop=4 q=0.1745; p*=0.9965928052 N_delta=5 N_rhop=5 q=0.1458; p*=0.9968313365 N_delta=6 N_rhop=6 q=0.1256; p*=0.9970380760 N_delta=7 N_rhop=7 q=0.1101; p*=0.9972145818 N_delta=8 N_rhop=8 q=0.0981; p*=0.9973715143 N_delta=9 N_rhop=9 q=0.0884; p*=0.9975098190 N_delta=10 N_rhop=10 q=0.0805; p*=0.9976349649 N_delta=11 N_rhop=11 q=0.0739; p*=0.9977475390 N_delta=12 N_rhop=12 q=0.0683; p*=0.9978506919 N_delta=13 N_rhop=13 q=0.0635; p*=0.9979448044 N_delta=14 N_rhop=14 q=0.0593; p*=0.9980318422 N_delta=15 N_rhop=15 q=0.0556; p*=0.9981120637 N_delta=16 N_rhop=16 q=0.0524; p*=0.9981867699 N_delta=17 N_rhop=17 q=0.0495; p*=0.9982561447 N_delta=18 N_rhop=18 q=0.0469; p*=0.9983210900 N_delta=19 N_rhop=19 q=0.0446; p*=0.9983817431 N_delta=20 N_rhop=20 q=0.0425; p*=0.9984387541 N_delta=21 N_rhop=21 q=0.0406; p*=0.9984922306 N_delta=22 N_rhop=22 q=0.0389; p*=0.9985426567 N_delta=23 N_rhop=23 q=0.0373; p*=0.9985901208 N_delta=24 N_rhop=24 q=0.0358; p*=0.9986349937 N_delta=25 N_rhop=25 q=0.0344; p*=0.9986773509 N_delta=26 N_rhop=26 q=0.0331; p*=0.9987174837 N_delta=27 N_rhop=27 q=0.0320; p*=0.9987554580 N_delta=28 N_rhop=28 q=0.0309; p*=0.9987915071 N_delta=29 N_rhop=29 q=0.0299; p*=0.9988256900 N_delta=30 N_rhop=30 q=0.0289; p*=0.9988581967 N_delta=31 N_rhop=31 q=0.0280; p*=0.9988890801 N_delta=32 N_rhop=32 q=0.0272; p*=0.9989184972 N_delta=33 N_rhop=33 q=0.0264; p*=0.9989464956 N_delta=34 N_rhop=34 q=0.0256; p*=0.9989732062 N_delta=35 N_rhop=35 q=0.0249; p*=0.9989986719 N_delta=36 N_rhop=36 q=0.0242; p*=0.9990230030 N_delta=37 N_rhop=37 q=0.0236; p*=0.9990462376 N_delta=38 N_rhop=38 q=0.0230; p*=0.9990684694 N_delta=39 N_rhop=39 q=0.0224; p*=0.9991296222 N_delta=42 N_rhop=42 q=0.0209; p*=0.9991483476 N_delta=43 N_rhop=43 q=0.0204; p*=0.9991663096 N_delta=44 N_rhop=44 q=0.0200; p*=0.9991835671 N_delta=45 N_rhop=45 q=0.0195

**Identity gates (solver-correctness):**

| gate | value |
|---|---|
| Delta-phi - ln(1101) | -1.155e-14 |
| phi(r_s) (event residual) | -1.173e-14 |
| 2m/rho core / seal | 1.000000000000 / 1.000000000000 |
| E_m(core) - 2 | +0.000e+00 (U(rho_c)=2 built into the slice normalization -- exact by construction) |
| H drift max / H(seal) | 3.333e-11 / -1.275e-11 |
| rho'(r_s) at root (miss) | -1.043e-11 |
| U_seal conservation identity residual | -1.275e-11 |
| sigma two-route residual (rel, interior mask) | max 6.888e-10, median 2.781e-11 (245 pts) |
| N_delta / N_rhop / N_phip (graduated floors [1e-06, 1e-07, 1e-08, 1e-09, 1e-10]) | {0} / {0} / {0} |

**Turning-point / fold map:** interior rho'=0 zeros: NONE; interior phi'=0 zeros: NONE. Folds: r_c=0 (phi'=rho'=0 exact ICs), r_s=784.4148 (rho'=0 seal root; phi'(r_s)=q/(Z rho_s^2)>0, NOT a phi-turning point). N=0 confirmed: no interior turning points.

**Station wall data** (core fold, 5 even interior stations, outer seal; sigma_geo is 0/0-indeterminate AT the folds -- reported None there, honest):

| station | r | phi | phip | rho | rhop | H_amb | sigma_ma | sigma_geo | e2phi | E_m | m_MS | two_m_over_rho | pi_phi_qflux | pi_rho |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core_fold | 0 | -7.00397 | 0 | 1 | 0 | 0 | 2.97696e-09 | None | 8.24946e-07 | 2 | 0.5 | 1 | 0 | -0 |
| interior_1of6 | 130.605 | -7.00294 | 3.17581e-05 | 1.00003 | 3.87786e-07 | 4.61853e-14 | 2.94117e-09 | 2.94115e-09 | 8.26661e-07 | 2 | 0.500013 | 1 | 3.17597e-05 | -1.8764 |
| interior_2of6 | 261.602 | -6.98734 | 0.000254224 | 1.0001 | 7.89963e-07 | 4.52971e-14 | 2.90335e-09 | 2.90319e-09 | 8.52854e-07 | 2 | 0.500051 | 0.999999 | 0.000254276 | -3.70503 |
| interior_3of6 | 392.207 | -6.9191 | 0.000882017 | 1.00024 | 1.32428e-06 | 3.90799e-14 | 3.06323e-09 | 3.06323e-09 | 9.77559e-07 | 2 | 0.500118 | 0.999998 | 0.000882435 | -5.41874 |
| interior_4of6 | 522.812 | -6.72093 | 0.00237069 | 1.00047 | 2.52268e-06 | 3.33067e-14 | 3.86327e-09 | 3.86329e-09 | 1.45302e-06 | 2.00001 | 0.500235 | 0.999996 | 0.00237294 | -6.94464 |
| interior_5of6 | 653.81 | -6.17797 | 0.00696206 | 1.00107 | 8.70012e-06 | -1.04805e-13 | 6.28658e-09 | 6.28657e-09 | 4.30412e-06 | 2.00001 | 0.500528 | 0.999982 | 0.00697702 | -8.08539 |
| outer_seal | 784.415 | -1.17264e-14 | 0.585516 | 1.35296 | -1.04345e-11 | -1.27465e-11 | -0.335103 | None | 1 | 1.68623 | 0.676479 | 1 | 1.07178 | 4.17379e-11 |

## Extraction-level observations (facts only, no interpretation)

1. **H_amb(r) = 0 to solver precision along the ENTIRE interior of every bracket** (max |H| ~ 1e-10--1e-11). This is by construction: the transversality closure U(rho_c)=2 sets H_tot(fold)=0 and H is conserved (autonomous L). The seal value the embedded C2 closure consumes from the PURE (unperturbed) universe cell is therefore 0 at every station. Flagged for E1 as an extraction fact (what H_amb becomes when a particle cell is inserted and the ambient re-solves is E1's question, not answered here).
2. sigma two-route agreement at 1e-9--1e-8 relative (interior mask) on all four brackets = the armed-audit machinery is consistent on the pure cell, as the pre-registration expects (gate, not evidence).
3. A3 Z=1 (Stage-A budget-cut) fundamental converged fresh: the coarse Stage-A grid's first sign change there is the N=2 member; the N=0 fundamental hides in a same-sign dip (the pre-named Stage-A even-pair hazard, now confirmed live). Its q=1.07 sits with the Z=1 fundamental cluster (q ~ 1.27-1.48, now 1.07-1.48). Side data (recorded, not interpreted): the hunt's subdivision incidentally refined a CONSECUTIVE below-stuck root list N_delta = 0..39 and 42..45 for A3 Z=1 (N_delta = N_rhop on every member), consistent with the Stage-B complete-integer-ladder finding in a fourth family x Z combination.
4. Gradient structure (E1 feeds on this): strictly, |rho'|,|phi'| > 0 everywhere between the folds (no interior turning points; the only exactly-gradient-free positions are the two folds). BUT the magnitudes are strongly seal-concentrated: max|phi'| (0.41--0.84) and max|rho'| (0.14--0.35) both sit at r/r_s ~ 0.995--0.999, while |phi'| stays below 1e-3 of its max out to r/r_s ~ 0.38--0.46 and the deep interior is a near-flat plateau (phi ~ -7.004, rho ~ 1, |rho'| ~ 1e-6--1e-5 at the even-sixth stations). So the ambient offers a CONTINUUM from near-gradient-free (core plateau) to strongly gradient-carrying (seal vicinity); E1's labeled turning-point slices are fold-vicinity slices, and the even-sixth stations span the plateau-to-wall transition as controls.

## Chosen parameters (ALL Category-A conditioning -- none physics)

rtol=1e-11/atol=1e-13 (re-shoot, tighter than banked 1e-10); r_max=1e6; dense grid 2001 uniform + 256 geometric per fold ([1e-8,1e-2]*r_s); FD step 1e-6*r_s (5-pt); graduated zero floors 1e-6..1e-10 rel; sigma-gate mask |rho'|>=1e-3*max, r in [2h, r_s-2h]; brentq xtol=1e-13; station placement = even sixths (reporting choice; E1 re-slices the dense grid freely); fresh-hunt subdivision FINE_N=19; fundamental selection = pre-registered nodeless count N_delta=N_rhop=0 (provenance/count, not merit). No physics value was chosen anywhere in this extraction; every physics premise is inherited from the banked solver and carries its original tag (see script header ledger).

---

## VERIFIER RECORD (blind spot-verification — agent aaa9ca9e751d1f6fb, 2026-07-03)

All six attacks HOLD; tables SAFE TO BANK as E1 input. Independent re-shoots (own RHS from the
doc equations, DOP853 vs E0's LSODA/Radau, own counters/brackets/FD): A3 Z=1 fresh a* confirmed
to 1e-10 incl. the even-pair N-diagnosis (coarse first sign-change = the N=2 member; N=0+N=1 in
the same-sign dip); A1 m=3 Z=8 profiles reproduce ≥6 digits at random stations; identity gates
reproduce; σ two-route independence confirmed non-circular (route (b) never touches U).

**H_amb ≡ 0 ADJUDICATED REAL-AND-FORCED, NON-VACUOUS:** sympy proof — the corner Hamiltonian is
conserved on-shell (r-autonomy) and its fold value is U(ρ_c)−2 = 0 exactly by the transversality
closure, so H≡0 along the interior of ANY exact trajectory of this family; the E0 implementation
reads NONZERO (1e-3…1e-2; conserved +0.04 on an off-closure U) on non-solution/off-closure
profiles — the zero comes from the closure, not from construction.

**CORRECTIONS (supersede the corresponding claims above):**
1. The A3 Z=1 "unique nodeless" statement is SCOPED TO BELOW-STUCK: the fresh-hunt rule silently
   skipped one ABOVE-stuck coarse sign-change; the verifier refined it — b* = 1.0016211844 with
   N_δ = N_ρ' = 20 (not nodeless; fundamental selection unaffected).
2. Gradient-max band: A1 m=3 Z=8 argmax|φ'| sits at r/r_s = 0.9946 — read the band as
   ≈0.994–0.999 (argmax|ρ'| = 0.9969 in band). Cosmetic; seal-concentration stands.
3. Scope note: the headline σ two-route agreement (1e-9–1e-8) is the MASKED near-seal region;
   unmasked interior agrees at FD-noise level (1e-5–7e-5) — nothing physical hidden.
