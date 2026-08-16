# G112 evidence gates

## Preregistration

Passed at commit `c181d903` before the G112 likelihood ran.

## Bounded completeness

Every retained Pantheon+ and DES row was evaluated. No row or survey was selected by outcome. This
is complete only for the fixed P1 shape and declared reductions, not for all SNe data or complete
metric histories.

## Independent verification

Production uses covariance-domain Cholesky whitening and full 1,820-object precision-matrix
inversion before extracting the DES marginal covariance. The implementation-distinct route uses
direct-power P1, precision-domain profiling, and the DES Schur complement. Both reproduce the same
fixed-shape likelihoods. They share NumPy/SciPy and source data, so this is not end-to-end software
or provenance independence. Fresh blind review returned `VERIFIED_WITH_CAVEATS`.

## Catch proofs

Executable mutations reject pair/sky identification, moving `n`, appending an orchestra correction,
using the DES precision subblock, reading forbidden cosmology fields, invoking a shape optimizer,
promoting the screen representative to a complete history, and calling the flux rule native.
String and fixed-property checks are semantic regression guards, not independent proof.

## Premise audit

The test preserves every conditional status. No Lambda-CDM distance, BAO/CMB result, complete R17
history, `X_max`, bootstrap, action, source, or matter law entered.
