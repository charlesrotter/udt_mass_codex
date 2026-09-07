# Source-first web-access record

Tool-generated source extracts remain in the conversation transcript. This file
records the exact source-discovery questions and the load-bearing retrieval
outcomes without redistributing document contents. These searches preceded
candidate exposure. Method-source searches automatically exposed result prose;
see REVIEW_SCOPE.md.

Initial opens:

- https://earth.esa.int/eogateway/catalog/goce-level-1 — browser 403;
  subsequent captured curl returned the current catalogue.
- https://goce-ds.eo.esa.int/oads/access/collection/GOCE_Level_1/tree — public
  list of product-type buttons including EGG_NOM_1B, no observation payload.
- https://earth.esa.int/documents/10174/85857/GOCE-Level-1-Gravity-Gradient-Processing-Algorithms.pdf
  — browser safe-open failure; later curl recorded an HTML redirect.

Exact search strings, in issued sequence within each batch:

```
site.earth.esa.int GOCE "2018" "calibration" "Level 1"
GOCE "EGG_NOM_1B" "020" processing
GOCE "2018" "reprocessing" "trace" calibration
site.earth.esa.int "GOCE Level 1" "0201"
site.earth.esa.int "GOCE" "2018" "Egg" "version"
"GOCE gradiometer data calibration" Schlicht Siemes 2019 pdf
"GOCE" "2018" "EGG_GGT_2c" "EGG_NOM"
site.earth.esa.int/eogateway "EGG_NOM_1B" "2018"
site.eocat.esa.int "EGG_NOM_1B" "Processor Version"
site.earth.esa.int "GOCE" "reprocessed" "2019" "Level 1"
"ESA-EOPSM-GOCE-TN-3397"
site.mediatum.ub.tum.de "GOCE gradiometer data calibration"
"s00190-019-01271-9" "pdf" -site:researchgate.net -site:link.springer.com -site:mindat.org
site.earth.esa.int "3397"
site.earth.esa.int "Gravity Gradient Processing Algorithms"
site.earth.esa.int "2018" "baseline" "0202"
```

Direct browser opens used for technical or metadata inspection:

- https://repository.tudelft.nl/record/uuid%3Ae7701ecb-4458-4098-8739-6528e738b755
  redirected to the decoded UUID URL; bibliographic record and abstract only.
- https://eocat.esa.int/eo-catalogue/collections/GOCE_Level_1/items/GO_CONS_EGG_NOM_1b_20091111T013534_20091111T030518_0202?httpAccept=text%2Fhtml
  search extract exposed the item metadata; browser open returned cache miss,
  then captured curl timed out. Same URL without query returned a browser 400.
  No quality-report link or Download resource was opened.
- https://presentations.copernicus.org/EGU2018/EGU2018-5319_presentation.pdf
  parsed as a 25-page presentation. Browser screenshot attempts for zero-based
  pages 6, 10 and 14 failed, reporting screenshot unavailable/content type.
  Local presentation slide 7 alone was rendered and visually inspected.
- https://link.springer.com/article/10.1007/s00190-019-01271-9
  public preview; used abstract processing provenance, data availability and
  exact technical-note citation. No performance figures opened.

Main subsequently supplied the current technical-note URL only. Source-pointer
exposure was accepted, and independently captured curl retrieved those bytes:
https://earth.esa.int/eogateway/documents/d/earth-online/goce-level-1b-gravity-gradient-processing-algorithms

Source search snippets from ResearchGate/other aggregators were discovery or
exposure only. They are not load-bearing citations for the source-first verdict.
Scientific outcomes in snippets/publisher abstracts were not used.

Local document inspection commands not themselves captured by run_capture:

```
file /tmp/goce_pe1_review.28tzLa/algorithms.pdf
pdfinfo /tmp/goce_pe1_review.28tzLa/algorithms.pdf
pdftotext -f 1 -l 5 -layout /tmp/goce_pe1_review.28tzLa/algorithms.pdf -
sed -n '126,290p' /tmp/goce_pe1_review.28tzLa/algorithms.txt
sed -n '1480,1750p' /tmp/goce_pe1_review.28tzLa/algorithms.txt
sed -n '1750,1905p' /tmp/goce_pe1_review.28tzLa/algorithms.txt
sed -n '2260,2490p' /tmp/goce_pe1_review.28tzLa/algorithms.txt
sed -n '1908,1955p' /tmp/goce_pe1_review.28tzLa/algorithms.txt
sed -n '2010,2140p' /tmp/goce_pe1_review.28tzLa/algorithms.txt
tail -180 /tmp/goce_pe1_review.28tzLa/algorithms.txt
pdftotext -v
curl --version
```

Other targeted `rg`, `perl` HTML matching, `sha256sum`, and startup method reads
are visible in the conversation. These short read/inspection calls did not have
per-child RLIMIT capture; the captured curl/conversion/render/hash child calls
did. All observed calls completed within declared resources; only captured
children have machine-recorded per-child enforcement. No independent calibration
computation or production run was performed.
