Subject: GOCE EGG_NOM_1B baseline 0202 — calibration/processing documentation and arm convention

Dear ESA Earth Observation User Services,

Could you please direct this documentation enquiry to the GOCE Level 1b
processing/calibration team? I am assessing whether a gravity-gradient trace
consistency check would retain information not already imposed or absorbed
by calibration. This is not a report of a flight-data defect.

For EGG_NOM_1B baseline 0202, which documents or support records establish:

1. The applicable processor/configuration and validity ranges, its relation
   to EGG_NOM 07.00 and ESA-EOPSM-GOCE-TN-3397 issue 1.0 (27 August 2018), and how
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
   Does the 2008 L1b handbook's Table 43 trace-threshold flag Qual_Flag_Ggt
   have a baseline 0202 counterpart, and does it only annotate records or influence
   calibration, processing, weighting or recommended exclusions?
4. Appropriate joint uncertainty/correlation information or conservative
   bounds for a contrast of the diagonal sum, including calibration and
   angular-rate contributions and cross-epoch/cross-channel effects?
   TN3397 §8.2 describes an approximate attitude covariance; is there a
   separate applicable gradient/contrast uncertainty assessment?
5. The arm-length convention: TN3397 equations 6–9 use half-differences of
   accelerations/positions, while Algorithm 16 includes a factor 2 with L.
   Does L in Algorithm 16/AUX_EGG_DB denote full pair separation, and how
   does this map to the calibrated differential-acceleration channels?
   Is there a convention note or erratum clarifying the notation?

Document identifiers, an applicable processing/configuration summary, or
validated transfer/error bounds would be welcome; I am not requesting every
raw sample. An indication of which records are available and their scope
would help determine whether a meaningful unused test can be specified.

Thank you,
Charles Rotter

Public reference: https://earth.esa.int/eogateway/documents/d/earth-online/goce-level-1b-gravity-gradient-processing-algorithms
