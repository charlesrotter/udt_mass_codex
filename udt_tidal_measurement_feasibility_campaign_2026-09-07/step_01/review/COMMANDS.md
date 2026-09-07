# TM1 reviewer commands and source access

Read-only git status/rev-parse returned grok and
508eb238d1321a3bdce9a45eb47a97b63fb1b541. No checkout/fetch/pull was repeated;
the coordinating author handled synchronization. No git mutations.

Full audit was parent-run, not independently repeated. After its pass notice:

    awk -F '\t' 'NR==1 || $1=="G261" || $1=="G313" || $1=="G358"' CURRENT_SCIENTIFIC_PREMISES.tsv

The wrapper was read completely, then used unchanged:

    python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_tidal_measurement_feasibility_campaign_2026-09-07/step_01/review/stage_a_exact /home/udt-admin/udt_mass_codex python3 udt_tidal_measurement_feasibility_campaign_2026-09-07/step_01/review/stage_a_exact.py

Exact child command, resource limits, start time, result, stdout and stderr are
captured in stage_a_exact.json/.stdout/.stderr. No output overwrites.

Temporary source directory was created with:

    mktemp -d /tmp/tm1-review-docs.XXXXXX

It returned /tmp/tm1-review-docs.kNElPm. Three official PDFs were downloaded by
curl -L --fail --max-time 30 -o to that directory, using exactly the URLs in
PRIMARY_SOURCES.tsv. Initial sandbox L1b curl failed DNS, exit 6; an approved
read-only network escalation succeeded. The other two downloads used the same
approved network mechanism. PDF SHA-256 values were computed with sha256sum.

Equation/source inspection included:

    pdftotext -layout -f 23 -l 27 /tmp/tm1-review-docs.kNElPm/GOCE_L1b_2006.pdf -
    pdftotext -layout -f 45 -l 46 /tmp/tm1-review-docs.kNElPm/GOCE_L2_2008.pdf -

Further bounded text was read through the web PDF parser (sections/pages listed
in PRIMARY_SOURCES.tsv). Screenshots of L1b pages failed cache/403 and were not
used. The later earth.esa.int handbook URLs failed safe-open/access; catalogue
lookup timed out. These unavailable accesses leave modern release provenance
unverified, not disproved. No payloads or performance sections were opened.
