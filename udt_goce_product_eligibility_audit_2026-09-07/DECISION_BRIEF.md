# GOCE eligibility audit — decision brief

PE1 and this brief: VERIFIED-WITH-CAVEATS at their document-only scope.
Final premise, preservation and review checks passed. No scientific banking or data fit.

The missing2018 processing note has been recovered from ESA. That is useful
progress: we can now see where calibration, filtering and shared inputs enter.
The target is EGG_NOM_1B baseline0202; one cached official item identifies
processor07.00. Actual item/header bytes and its deployed configuration were
not verified. Collection version1.0 and Level-2 release numbers are different
identifiers. [Approved ESA method, issue1.0,27Aug2018](https://earth.esa.int/eogateway/documents/d/earth-online/goce-level-1b-gravity-gradient-processing-algorithms).

The final gradient calculation does not itself impose zero trace. But that
does NOT establish an unused test: the preceding calibration uses star-tracker
and gravity-model information, shared science/shaking inputs, data-dependent
choices and nonlocal processing. A model input is neither automatic proof of
complete erasure nor proof of independence. The note also contains a
half/full-arm normalization inconsistency, verified from the displayed
definitions and an independent full-matrix calculation. No flight bug is
established, and no accepted mathematics or source was repaired.

The controlling test assumes the owner-provisional connected Ric=Lambda g
arena, W4 WORKING/POSIT ideal coupling and the explicitly SUPPLIED TM1
instrument interface; none is an empirical device validation:

    tr(T)=kappa=-c_E^2 Lambda, with Lambda connected-constant;
    y=P(kappa 1+N beta)+epsilon, M=[P1,PN].

Here a justified FIXED LINEAR P and nuisance N would leave genuine scalar
noiseless structural test dimension rank(P)-rank(M), not a demonstrated
detectability or significance. The retrieved dossier does not yet justify
those P/N/error inputs for this release. Quadratic calibration and adaptive
masking cannot silently be treated as fixed linear processing; interpolation
of calibration matrices cannot justify additive affine scalar drift. Nor
does a filter weighting/noise model automatically bound all trace errors.
Ordinary initial/query choices remain legitimate data, not missing laws.

The actual blocker is the release-specific calibration/support/error bridge,
not absence of the algorithm PDF, lack of a uniquely selected geometry,
failure of UDT, or a demonstrated need for new physics. Before fitting, we
need a trustworthy processor/configuration and arm/channel crosswalk; the
calibration estimator's target conditions, parameter/epoch/mask provenance
and raw-support map; and justified uncertainties/correlations or deterministic
bounds that leave a retained contrast. Equivalent trusted support records may
suffice; retrieving every raw shaking sample is not imposed as a universal
requirement. Their public availability has not been established or ruled out.

I recommend ending this audit after one reviewed step. Step1 did not close
the indispensable provenance gates; a second conditional example would not
supply them. The next useful choice is whether to obtain that specific
calibration/processor dossier (potentially through an authorized ESA enquiry),
or compare a different instrument route. No enquiry was sent. Empirical
analysis, new physical assumptions and any new campaign still need direction.
Geometric testing and emergence remain parallel, neither prerequisite.

TM1/TM2 remain unpromoted. Accepted registry, original evidence, fixed-snapshot
manuscript and canon are unchanged. Backup completeness and pre-reboot
unsaved-state disposition remain UNVERIFIED. ScratchDisk was not used and
blocks archive-dependent tasks only. Fresh-context review is real; exact model
identity UNKNOWN, different-model and human-specialist review UNTESTED;
prior qualitative source exposure remains disclosed.
