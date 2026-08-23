# G236 audit report — dual-SNe relational-state reconstruction

Date: 2026-08-23

## Landing

```text
DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD
__TWO_DEOVERLAPPED_PROCESSED_RELEASES_SUPPORT_ONE_RELATIVE_R_OF_PHI_SHAPE
__NO_P1_XMAX_LCDM_DISTANCE_OR_PHYSICAL_PROFILE_FIT
__OBSERVATIONAL_PROCESSING_AND_IMPORTED_TRANSFER_CAVEATS_RETAINED
```

## What was learned

Under the bounded central-static query and the already declared temporary transparent-transfer
bridge, SNe directly measure

\[
m-10\log_{10}(1+z)=5\log_{10}R(\phi)+B_c,
\qquad \phi=\log(1+z).
\]

After removing all 203 Pantheon+ survey-10 rows—including 148 exact CID overlaps with the DES-only
release—the remaining 768 Pantheon+ rows and 1,623 DES rows reconstruct compatible relative state
shapes at every preregistered resolution.

The primary `K=12` comparison gives

\[
\chi^2_{\rm shape}=14.409356
\]

for 11 relative-shape degrees of freedom, below the preregistered conservative ceiling
`34.452079`. The `K=8,16,24` controls also pass.

## What was not learned

G236 does not derive `R(phi)` from the founding postulates, predict SNe, validate a physical UDT
history, establish native radiative transfer, determine `X_max`, or remove release-processing
dependence. It reconstructs one observational state projection.

The released Pantheon+ and DES vectors already include light-curve standardization and bias
corrections. DES explicitly uses an approximate reference cosmology in its bias-correction
simulations. The correct result grade is therefore `OBSERVED_PROCESSED_CONDITIONAL`.

## Evidence

- preregistration committed and pushed before reconstruction at `184b1a78`;
- pre-outcome hostile repair committed and pushed at `318f35de`;
- 11 frozen source/data hashes pass;
- exact release counts and 148-CID overlap check pass;
- full covariance retained for both de-overlapped samples;
- four fixed resolution controls pass raw adequacy and cross-release concordance;
- implementation-independent precision-domain replay agrees within the frozen tolerances;
- duplicate, slope, redshift-reassignment, and nine validator mutation catches pass;
- no P1 value, `tanh` profile, `X_max`, Lambda-CDM distance, or optimizer enters production.

## Current grade

```text
EXTERNALLY_VERIFIED_WITH_CAVEATS
__OBSERVED_PROCESSED_CONDITIONAL
__REPAIR_FOLLOWUP_ACCEPTED_SCIENTIFIC_LANDING_RETAINED
```

Fresh external `gpt-5.4` review reproduced every load-bearing number and found no scientific,
statistical, type, data, provenance, or scaffolding error. Its sole initial objection was the lack
of sealed immutable chronology evidence. The preregistered evidence-only repair supplied raw Git
objects, tree listings, the exact repair patch, and an explicit hostile-noninterference proof. The
repair-only follow-up accepted those repairs and retained the scientific landing unchanged.

The chronology proof has one honest ceiling: Git proves the identity, ordering, and contents of
committed trees; it cannot retroactively prove that no untracked private computation existed.

## Next gate

Estimate one joint finite-resolution relative state from both processed releases, freeze it, and
carry it without refitting into one separately typed held-out observational query. BAO requires a
source-pattern and query-operator audit before it can serve as that held-out channel; CMB likewise
requires its own source/sky typing. The joint estimate remains an observational state projection,
not a metric-native profile law.
