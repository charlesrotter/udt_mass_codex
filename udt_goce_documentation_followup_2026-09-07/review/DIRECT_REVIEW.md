# Direct adversarial documentation review

Initial direct review, 2026-09-07, reviewer `/root/goce_docs_review`.
Verdict: **VERIFIED-WITH-CAVEATS as a bounded documentation assessment;
one concrete documentation omission requires the authorized focused repair
before final closure.** No product/scientific eligibility or grade verdict.

The source-first assessment was sealed at18:16:39 UTC, before main's
18:18:26UTC candidate freeze notice. Main's initial candidate was then read
and all three reported hashes were independently matched:

| Candidate | SHA256 |
|---|---|
| DOCUMENTATION_ASSESSMENT.md | e27f8b9f2593d086bf631bc856b05d75caaa40512d236ee088a58e2d4b9ad05f |
| ESA_ENQUIRY_DRAFT.md | cbddd2ad2b8a02d9059292e88aa53eb72e7f6a8682260b64be59490eaf901daf |
| SEARCH_AND_EXPOSURE.md | 97b2748ee5b87c94d770567988b3cc807b8285528c5b2f8cd17059a62ab3eee4 |

## R1 — make trace-dependent quality selection an explicit question

**Defective step:** assessment item3 and enquiry question3 discuss generic
masks/selection but omit an already available, directly target-related
historical locator. The2008 issue2/rev0 handbook Table43, printed93
(PDF107), explicitly lists a trace-GGT threshold monitoring flag,
`Qual_Flag_Ggt`, among the output quality flags. Its existence was identified
in the reviewer's sealed source-first stage, independently of main's draft.

**Reason:** asking only about calibration fitting, filtering and generic
masking may leave an avoidable ambiguity. An otherwise retained trace could
still be selected using a trace-dependent flag. Whether the flag only
annotates, rejects/downweights samples, affects coefficient/epoch choice, or
is used by a recommended selection rule matters to an unused-test claim.
No such downstream behavior is established by the historical schema alone.

**Strongest survivor:** the draft already correctly keeps support and
selection open, does not claim calibration inevitably erases or retains
signal, and demands justified end-to-end response. Its overall evidence
ceiling and the proposal to request documentation survive.

**Smallest source-preserving repair:** add a short historical-source sentence
and locator to assessment item3, and ask in enquiry question3 whether the
corresponding0202 trace/quality monitoring rule is annotation-only or affects
processing, calibration, selection or recommended exclusions. Explicitly
retain that2008-to0202 applicability is unverified. Main should read PDF107
and record this reviewer-supplied locator/exposure after its initial freeze.
No new observational retrieval, theory premise or wider search is required.

## Claims that survive direct scrutiny

- The handbook fields/Table5 are legitimate historical metadata pointers;
  placeholders do not establish a deployed release configuration. The draft
  consistently retains the0202/07.00/configuration applicability gap.
- Presentation slides10 and13 visually confirm model-gradient,
  star-tracker/equal-common-mode equations and parameter/drift families.
  The draft labels these April2018 method context, not final settings.
  The0.8–10mHz item is calibration weighting context, not a delivered-product
  bandwidth or fitted scalar nuisance law.
- TN3397 §8.3/Table15 (printed58) confirms K and flag-dependent attitude
  weighting. §8.2 supplies a deliberately approximated attitude covariance,
  not a demonstrated end-to-end scalar-contrast covariance. The draft's
  alternative of justified conservative bounds is appropriate.
- The minimum-evidence table admits authoritative equivalent descriptions
  and contrast-level bounds. It does not demand all raw samples, uniquely
  identifiable nuisance parameters or statistical independence of every
  input. It makes no documentation-completeness theorem.
- The fixed-linear TM2 model is explicitly conditional/unpromoted. Unknown
  gains, nonlinear/adaptive calibration, refitting and nonscalar leakage are
  not silently forced into scalar-only P,N. Nonzero response is distinguished
  from attainable sensitivity. This is faithful to the controlling TM2
  argument within this documentation review; its proof was not re-run.
- The arm question identifies written half/full normalization ambiguity and
  seeks an implementation/auxiliary crosswalk. It does not claim a flight
  defect. Existing written equations and visually checked Algorithm16 support
  this narrow question; actual code and auxiliary values remain unexamined.
- The support route is supported by the cached official catalogue's User
  Services link and the retrieved portal title. No category or named
  specialist is claimed verified. The enquiry body contains public document/
  product identifiers and general metrological questions, without repository
  paths, attachments, unpublished scientific claims or instructions to send.
  The internal handling note is explicitly outside the proposed message.

## Additional direct checks and their limits

Commands retained the512MiB/60s wrappers described in
COMMANDS_AND_SCOPE.md. All returned exit0. New independent checks were:

```text
sha256sum DOCUMENTATION_ASSESSMENT.md ESA_ENQUIRY_DRAFT.md SEARCH_AND_EXPOSURE.md
sed -n '1,280p' EACH_CANDIDATE
rg --files /tmp/udt-goce-docs-CvpkoQ
sha256sum /tmp/udt-goce-docs-CvpkoQ/support.html /tmp/udt-goce-docs-CvpkoQ/onorbit.pdf
rg -n -o '<title>[^<]*|TellUS|Customer Service Portal' /tmp/udt-goce-docs-CvpkoQ/support.html
pdftotext -f 57 -l 58 -layout /tmp/udt-pe-primary-wacMzS/algorithms_2018.pdf -
pdftotext -f 1 -l 2 -layout /tmp/udt-goce-docs-CvpkoQ/onorbit.pdf -
pdftotext -f 32 -l 34 -layout /tmp/udt-pe-primary-wacMzS/handbook.pdf -
pdftotext -f 39 -l 40 -layout /tmp/udt-pe-primary-wacMzS/handbook.pdf -
rg -o '.{0,70}(esatellus|EOHelp|User Services).{0,140}' /tmp/udt-pe-primary-wacMzS/catalog.html
```

Candidate paths above are within the follow-up root, with per-file commands
actually run separately. The portal SHA matched
`257025d148c293b670db8b65948fd50e1fd44ac1cf44edd38d4a21c15c6c49ba`;
on-orbit note SHA matched
`796cb64ecfa95057d5343d6f5d07c18de05cdfaba4a8fca1c09c3a254f8a0154`.
The latter's issue04 date14Feb2008 was verified from its change-record page,
not treated as a modern release-specific calibration specification.
Existing `slide10.png` and `slide13.png` were inspected with `view_image`;
no new image was created or redistributed.

Direct source reads added historical handbook instrument-precision prose
incidental to the arm/format sections. These values were not extracted into
the assessment or used as bounds. Main's exact seven search executions,
network failures/retries and every captured command were not replayed or
independently authenticated; their stated scope is plausible and is treated
as an author activity record. No new web queries/retrievals were made here.

Main reports its full349 premise verifier passed at18:17:08.8UTC with
exit0 and399.3357s. This review has not yet independently inspected that
saved result and has not rerun it. Source-first/model/human independence
limitations and all omitted scientific/empirical checks remain as recorded
in SOURCE_FIRST.md and COMMANDS_AND_SCOPE.md. A source or activity hash
certifies bytes, not truth, independent discovery or observational blindness.

## Return for the authorized repair

R1 is the sole required repair identified in this direct pass. Re-review
should inspect its bounded addition, the preserved initial candidate/repair
history and final assessment/enquiry/exposure versions. Any compact delivery
brief/status wording can receive fidelity review without reopening a
scientific campaign. No additional research or scientific promotion follows
from the review verdict.
