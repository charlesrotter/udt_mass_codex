# ESA enquiry — DRAFT FOR CHARLES'S APPROVAL; NOT SENT

Proposed route: ESA EOHelp / Earth Observation User Services through the
[catalogue-linked TellUS request portal](https://esatellus.service-now.com/csp?id=esa_simple_request).
Please route to the GOCE Level1b processing/calibration team. Current form
categories and a named team contact have not been verified. No attachments.

Subject: GOCE EGG_NOM_1B baseline0202 — calibration/processing documentation and arm convention

Dear ESA Earth Observation User Services,

Could you please direct this documentation enquiry to the GOCE Level1b
processing/calibration team? I am assessing whether a gravity-gradient trace
consistency check would retain information not already imposed or absorbed
by calibration. This is not a report of a flight-data defect.

For EGG_NOM_1B baseline0202, which documents or support records establish:

1. The applicable processor/configuration and validity ranges, its relation
   to EGG_NOM07.00 and ESA-EOPSM-GOCE-TN-3397 issue1.0 (27Aug2018), and how
   to identify these from Software_Ver and configuration/auxiliary references?
2. The external calibration objective, estimated parameters/drifts, priors
   or hard constraints, spectral weighting and science/shaking intervals;
   specifically, whether trace/Laplace conditions or gravity-model matching
   constrain any scalar modes, and which attitude, orbit and gravity-model
   inputs are shared with the delivered gradients?
3. The temporal influence of calibration estimation/interpolation, filtering,
   gap/edge treatment and adaptive masking, or equivalent support bounds;
   and any validated end-to-end sensitivity to trace departures, including
   calibration refitting/selection when inputs are reused?
4. Appropriate joint uncertainty/correlation information or conservative
   bounds for a contrast of the diagonal sum, including calibration and
   angular-rate contributions and cross-epoch/cross-channel effects?
   TN3397 §8.2 describes an approximate attitude covariance; is there a
   separate applicable gradient/contrast uncertainty assessment?
5. The arm-length convention: TN3397 eqs6–9 use half-differences of
   accelerations/positions, while Algorithm16 includes a factor2 with L.
   Does L in Algorithm16/AUX_EGG_DB denote full pair separation, and how
   does this map to the calibrated differential-acceleration channels?
   Is there a convention note or erratum clarifying the notation?

Document identifiers, an applicable processing/configuration summary, or
validated transfer/error bounds would be welcome; I am not requesting every
raw sample. An indication of which records are available and their scope
would help determine whether a meaningful unused test can be specified.

Thank you,
[Name]

Public reference: [TN3397](https://earth.esa.int/eogateway/documents/d/earth-online/goce-level-1b-gravity-gradient-processing-algorithms).

Internal handling note (not part of message): no repository paths, candidate
artifacts, unpublished claims, observations or attachments are included in
the proposed message. Review is pending. Do not submit without approval.
