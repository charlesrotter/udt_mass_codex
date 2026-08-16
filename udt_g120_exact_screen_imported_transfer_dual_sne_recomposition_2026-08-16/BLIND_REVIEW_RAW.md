# G120 fresh blind review — first pass

Landing: `REPAIR_REQUIRED`

The reviewer independently reproduced:

```text
Pantheon+ chi2 = 1260.8480887274914 / 1366 fixed-n replay dof
DES chi2       = 1444.1864417504914 / 1622 nominal dof
wrong T=1      = 2279.762824418193 and 2135.46660444151
```

It accepted the G94+G119+imported-transfer algebra and conditional P1 radius retyping. Mandatory
repairs were: restrict the radius interpretation to `Z>=1`; replace the vacuous slope assertion;
and make package replay noncircular by comparing against pre-run bytes in a temporary copy.

Optional requests were to move hard-coded method facts out of pass/fail checks and explicitly state
Pantheon+'s calibration-sample and fitted-versus-fixed degree-of-freedom provenance.

The reviewer accepted the disclosed exact-algebra gate repair as a strengthening rather than
target-aware weakening. All requested repairs are recorded in `CORRECTION_RECORD.md`.
