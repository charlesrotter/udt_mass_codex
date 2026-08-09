# Center-spectrum correction — pre-run numerical tolerance addendum

Date: 2026-08-09  
Timing: committed before the correction solver is implemented or run

The upstream correction preregistration required an independent adaptive-collocation check but did
not attach a numerical agreement threshold. Freeze it here:

- shooting versus adaptive-collocation frequency agreement: maximum relative difference `<1e-5`
  for every positive root;
- an exact zero mode is checked by absolute frequency/residual `<1e-10` rather than a relative ratio;
- adaptive-collocation boundary residual `<1e-8` and solver status success for every checked root.

No observational value is involved in these physics-blind numerical thresholds.
