# Primary-source access and exposure

Access date07Sep2026. Main author reconstructed the argument before reading
reviewer findings. Main and reviewer are separate contexts, not established
different runtime models. Model identities UNKNOWN; different-model axis UNTESTED.

Primary public technical PDFs E1/E2 were downloaded only to the temporary
directory /tmp/udt-tm1-primary-g4Ms9J. No observation payload was downloaded.
No whole copyrighted PDF or rendered page is redistributed in this package.
SOURCE_LEDGER.tsv records source hashes, URLs, dates and limits.

Exact E1 retrieval command:
`curl --fail --location --max-time 45 --output /tmp/udt-tm1-primary-g4Ms9J/GOCE_L1b_2006.pdf https://esamultimedia.esa.int/docs/GOCE_Level1bProduct_User_Handbook.pdf`
Sandbox DNS failed exit6; authorized ordinary network execution succeeded exit0.
Browser PDF screenshots failed with cache/internal errors. Local layout inspected
using `pdftoppm -f 23 -l 24 -scale-to 1600 -png -singlefile` (first page only,
warning preserved in tool transcript), then `-f 24 -l 24 -scale-to 1800`.
Both relevant pages were viewed. Printed19/20 correspond to PDFpages23/24.

Exact E2 retrieval command:
`curl --fail --location --max-time 45 --output /tmp/udt-tm1-primary-g4Ms9J/GOCE_processing_report.pdf https://earth.esa.int/eogateway/documents/20142/37627/GOCE-gradiometer-calibration-and-level-1b-data-processing.pdf`
Web403; ordinary public unauthenticated retrieval succeeded exit0. No credential,
paywall bypass, private endpoint, observational array or empirical fit involved.
`pdftotext -layout` was used; load-bearing eqs6-10/32-38/74-78 and the upper-band
assumptions on printed17/20/31/40 were also rendered at1600pixels and viewed.
The report is dated differently on its cover and page headers; both retained.
Sections3.1-3.2,5.1-5.3 and6.1-6.2 read; §5.4 is cited only for its explicitly
displayed trace-constrained proposed adjustment, not implemented release status.
Section8.1 inspected for processing provenance, not performance certification.

E5 retrieval used the exact source-led old URL via the same ordinary curl
options. It exited0 but yielded HTML, not the requested PDF (`file` checked).
It is a failed document retrieval, not a successful algorithm audit. Two
targeted bibliographic searches and institutional E6 did not obtain the full
2018 method. No broad access impossibility is claimed and no author contacted.

Exposure limitation: search results and E3/E6 abstracts auto-displayed qualitative
historical performance claims. The E2 first240-line extraction inadvertently
included its preface; a pages17-23 technical extraction included §3.3 qualitative
performance prose/graph labels; §8.1 technical prose also mentions performance
motivations. No empirical numerical residual/fit or plotted outcome was used.
Full results chapters7/8.2 were not inspected. Later reading used exact sections.
An unrelated paper returned by a targeted bibliography search was not relied on.
This is disclosed exposure, NOT pristine pre-outcome confirmation. Future actual
observation work would need its own exposure-aware freeze. Source-method claims
alone support the present audit; no performance statement is a campaign result.

These shell/source inspection events are recorded from the live tool transcript;
they are not falsely labeled saved raw network logs. Computational stdout/stderr
and command metadata ARE separately saved by the existing run_capture utility.

One documentation patch failed atomically because a guessed log line was absent;
git diff verified no partial tracked change. Exact log text was read and the
patch then applied. No scientific repair or source change resulted.
