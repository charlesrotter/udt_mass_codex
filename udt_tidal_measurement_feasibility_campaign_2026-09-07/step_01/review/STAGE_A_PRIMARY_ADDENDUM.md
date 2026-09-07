# TM1 additional primary source — still before author-candidate exposure

The parent supplied a public technical-document access route after the initial
Stage A seal, carrying no scientific finding. I independently inspected its
bytes and relevant method sections. Initial STAGE_A.md and its seal remain
unchanged. Exact model remains UNKNOWN; this is the same fresh reviewer.

Source: ESA EWP-2384, GOCE gradiometer calibration and Level 1b data processing,
cover date 2011-11-21, page headers 2012-01-06. Public URL:
https://earth.esa.int/eogateway/documents/20142/37627/GOCE-gradiometer-calibration-and-level-1b-data-processing.pdf
SHA-256 d6326134e8f55bf8a4449961c48a817f1b18b05107a5940b2fe3fb0d8c78ad69.
Temporary PDF /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf;
the author downloaded it, and I independently checked the hash. No full PDF
is redistributed. Source location is shared; source reading and analysis are
independent. This does not certify a particular later product generation.

Bounded source check: equations 6–38 (pages 17–20) agree with the independently
derived force sign, half difference, rotation and trace map, and remove the
old handbook's sign/yy transcription ambiguity. Section 5 distinguishes an
explicit zero-trace redundancy from other calibration approaches. The baseline
method uses 50–100 mHz assumptions, 28 additional conditions including average
gain one, then star-sensor fitting near 1.3 mHz for absolute scale. Section 6.2
also assumes negligible gravity signal in the upper band; this is not a
derivation of negligible signal. Section 8.1 describes calibration-matrix
interpolation and attitude/angular-rate processing.

Assessment: a claim that every L1b gradient trace was set identically to zero
would still overstate the evidence. Different trace, negligible-signal,
normalization and external-model procedures need separate dependence audits.
The ideal local map survives; independent absolute scalar eligibility still
requires the actual calibration/processing chain and bounded errors.

## Exact reads and exposure

    sha256sum /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf
    pdftotext -layout -f 7 -l 8 /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf -
    pdftotext -layout -f 17 -l 22 /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf - | sed '/3.3 Impact/,$d'
    pdftotext -layout -f 31 -l 40 /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf -
    pdftotext -layout -f 31 -l 32 /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf -
    pdftotext -layout -f 41 -l 41 /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf - | awk '/^6\.3[[:space:]]/{exit} {print}'
    pdftotext -layout -f 77 -l 81 /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf -

The sed stop pattern failed because PDF heading spacing differed. As a result,
qualitative Section 3.3 prose was incidentally exposed, despite the intended
stop before it. Page 19 and Section 8.1 also contain qualitative motivation
from mission behavior alongside methods. I immediately disclosed the extraction
defect to the parent. No plotted flight outputs, outcome/residual arrays or
Section 7/8.2 results were opened or used. Page 80 contains the specified noise
model/filter weights, not an observed residual series. The claims above use
equations, procedures and assumptions only. All such exposure remains recorded;
it is not upgraded to outcome blindness or flight-data validation.

No new computation is needed: the already sealed independent symbolic map
matches this primary document. READY for direct review of the frozen candidate.
