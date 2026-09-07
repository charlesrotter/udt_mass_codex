# Bounded search and exposure record

2026-09-07, main context /root. Prior PE1 candidate/ledger/access and direct
review were read, so this is explicitly a follow-up, not a blind audit.
Main's new assessment was not informed by the new reviewer's conclusions
before its initial freeze. Existing source discovery and older review exposure
remain disclosed. Exact model identity UNKNOWN; no different-model claim.

## Reuse rather than repeated searches

Authenticated existing temporary sources with source_identity.*:

- TN3397 issue1.0 approved27Aug2018, SHA256
  3ba0639bd03adb2d9cbea49af6840991b0d2c7dfea67dc6d40eed2e0a47e935f.
  New targeted read: §8.2 and adjoining covariance-use text, printed54–58
  (pdftotext -layout PDF53–57). This identifies the scope and approximation
  of an attitude-reconstruction covariance, not delivered trace uncertainty.
- L1b handbook issue2rev0,25Jun2008, SHA256
  cc4110aa5232934962afe89b7ba3f71c0aff14900a5e21ba2f92e8523e36783b.
  New targeted reads: printed26 (processor-format applicability),32–35
  (MPH),40–41 (reference DSD filenames),89–90 (calibrated channels),95–97
  (frame/pair definitions),18–20 (full pair distance context). pdftotext
  -layout used PDF pages39–40,46–49,54–55,103–104,108–111,32–34.
  Cover/TOC pages1–8 revisited solely to locate the new sections; broad first
  output was truncated, all load-bearing targeted sections were then read.
- April13,2018 primary author presentation, SHA256
  ceb0d099b5a66321eeb037c879275711c62c4160ea9d8fc4908930b11ad0b053.
  Prior reviewer had inspected these methods; main now read slides10–15
  to sharpen the enquiry, not to claim a new document discovery. Text plus
  pdftoppm renders of10,13,15 (-scale-to1600 -png -singlefile), visually
  inspected. Formula layout was not inferred from missing PDF text.

## Seven new targeted web queries; no further search expansion

1. `"GOCE" "07.00" processor`, official ESA documentation domains.
2. `"GOCE" "0202" calibration configuration`, same domains.
3. `"GOCE" "support" "TellUS"`, ESA domains.
   Combined response gave generic ESA catalogue/support references and
   irrelevant archive results; no new release/configuration evidence used.
4. `"s00190-019-01271-9" "constraint"`, link.springer.com.
5. `"GOCE" "AUX_EGG_DB" "2018"`, official ESA documentation domains.
6. `"GOCE" "Proc_Config_Params_File"`, earth.esa.int/esamultimedia.esa.int.
7. `"GOCE" "TN-3397" calibration`, official ESA documentation domains.
   Queries4–7 returned no results. This is bounded retrieval evidence, not
   proof that records do not exist. No repeat institutional download-link
   search, failed eocat request, dead announcement or guessed TN URL.

## Two new primary-page/document targets

Public normal curl initially failed DNS in sandbox (support_fetch.* and
onorbit_fetch.*, exit6). Authorized read-only network retries succeeded
(support_network.* and onorbit_network.*, curl45s). No credential, form
submission, external contact or access-control bypass.

- ESA catalogue-linked TellUS simple request portal:
  https://esatellus.service-now.com/csp?id=esa_simple_request
  HTML SHA256257025d148c293b670db8b65948fd50e1fd44ac1cf44edd38d4a21c15c6c49ba.
  Title confirms ESA TellUS Customer Service Portal; browser read returned
  a loading shell. Exact current form categories and named processing-team
  assignment NOT verified. Draft addresses EOHelp/User Services and requests
  forwarding to GOCE Level1b processing/calibration support; no direct named
  specialist/email invented. The GOCE catalogue's support link is prior P1.
- Already identified ESA-linked Gradiometer On-Orbit Calibration Procedure
  Analysis, exact URL in onorbit_network.json; SHA256
  796cb64ecfa95057d5343d6f5d07c18de05cdfaba4a8fca1c09c3a254f8a0154.
  pdftotext -layout PDF1–5 identifies GO-TN-AI-0069 issue04,14Feb2008,
  93pages: preflight, not a2019 release-specific note despite later web
  metadata. Stopped at cover/change record/TOC/purpose/references. No
  simulation/performance chapters mined. Officially public retrieval does
  not authorize reproducing its historically marked controlled-distribution
  payload; full file remains temporary, not redistributed here.

## Exposure and limits

Method reads included empirical covariance constants/prose in TN3397 and
the ASD illustration on presentation slide15. These were incidental to
the method/stochastic-model pages, not untouched confirmation evidence.
Historical overview/preflight performance prose and broad search snippets
were also visible. No spectral values, flight residuals or performance
outcomes were extracted, fitted, used to choose a test band/epoch/threshold,
or accepted as scalar error bounds. Future empirical analysis needs its own
exposure-aware freeze. No observation payload, calibration array or quality
report opened; no pristine-blindness claim.

Temporary public sources/renders are in /tmp/udt-goce-docs-CvpkoQ and the
authenticated prior PE1 temporary directories. New source text was read
through tool output only; preserve paraphrases/locators/hashes, not whole
copyrighted sources. No new scientific computation or source theorem replay.
The previous exact convention checks remain the unchanged prior evidence.

## One bounded review repair

After initial author freeze18:18:26UTC and preservation commit8ebd7d02,
main read the new sealed source-first report. It independently identified
the historical handbook Table43 trace-monitoring flag, missing as an explicit
question from the first draft. Main then used pdftotext -layout PDF106–108
and visually inspected a pdftoppm render of PDF107/printed93. No new network
search or observation read was required. The explicit applicability/selection
question was added as R1; this source discovery is reviewer-led, not claimed
independent main discovery. Initial candidate, enquiry and search record
remain recoverable at8ebd7d02. No0202 flag use or flight censoring is inferred.
