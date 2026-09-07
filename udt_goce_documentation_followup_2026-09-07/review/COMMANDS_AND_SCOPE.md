# Review command and scope record

Reviewer `/root/goce_docs_review`; start clock18:12:17 UTC, source-first
seal18:16:39 UTC on2026-09-07. Assigned ceiling45min active and parent deadline
19:10 UTC. Review work is documentation only, zero GPU processes, no numerical
campaign, observational payload, fit or external contact. New files are only
under this `review/` directory, created with `apply_patch`; no commits, staging,
tracking changes, deletions or other repository mutations by this reviewer.

## Startup and version checks

Commands executed from `/home/udt-admin/udt_mass_codex`:

```text
git status --short --branch
git rev-parse HEAD
git log -8 --oneline
sed -n '1,260p' AGENTS.md
sed -n '/STARTUP_CURRENT/,/END_STARTUP_CURRENT/p' LIVE.md
sed -n '/STARTUP_CURRENT_BEGIN/,/STARTUP_CURRENT_END/p' HANDOFF.md
sed -n '1,220p' CURRENT_RESEARCH_PROGRAM.md
sed -n '1,240p' CURRENT_SCIENTIFIC_PREMISES.md
rg -n '^#{1,4} |SKILL.md|\.claude/skills' CLAUDE.md
sed -n '1,145p' CLAUDE.md
rg --files .claude/skills
sed -n '1,280p' .claude/skills/completeness-map/SKILL.md
sed -n '1,280p' .claude/skills/verifier-before-record/SKILL.md
sed -n '1,280p' .claude/skills/no-shortcuts/SKILL.md
rg -n -i 'GOCE|TM1|TM2|tidal.measure|G364|G366|PE1|current' INDEX.md MEMORY.md
sed -n '1,120p' INDEX.md
sed -n '1,100p' MEMORY.md
sed -n '1,240p' CROSS_MODEL_VERIFY.md
```

All returned exit0. HEAD matched the dispatch baseline. Status showed
`grok...origin/grok` and untracked work; no protected payload was opened.
Mandatory synchronization and full349 premise verification are delegated to
main per explicit dispatch, not claimed independently passed here. The
initial short reads/status commands had no `ulimit` wrapper; tool-reported
elapsed time was below1s each, and peak memory was not measured.

## Source reads

Read complete task WORK_ORDER and initial FOLLOWUP_LOG, PE1 step_01
SOURCE_LEDGER.tsv and ACCESS_AND_EXPOSURE.md with `sed -n '1,260p' FILE`.
Listed TM2 step_02 filenames with `rg --files`, then read only its controlling
`CANDIDATE_ARGUMENT.md` via `sed -n '1,300p' FILE`; its review outputs were not
opened. These command results were exit0; TM2 text ended within that range.

Subsequent shell commands were prefixed with:

```sh
ulimit -v 524288
ulimit -t 60
```

Each child command used `timeout 60s`. Limits are512MiB virtual address space
and60s CPU/wall. No child returned nonzero or timed out. Exact PDF command form
was `pdftotext -f FIRST -l LAST -layout PDF -` (stdout text only), with ranges:

| Temporary PDF | PDF page ranges requested |
|---|---|
| `/tmp/udt-pe-primary-wacMzS/algorithms_2018.pdf` | 1–5;32–37;53–55;60–62;53–55 again;60 again;7–8 |
| `/tmp/udt-pe-primary-wacMzS/handbook.pdf` | 1–8;45–49;89–90;53–55;103–108 |
| `/tmp/goce_pe1_review.28tzLa/egu2018.pdf` | 1–5;6–9;10–13;14–15 |

An overlarge batched tool response was truncated. Algorithm §8.2 and
Algorithm16 were re-requested separately. No claim relies on the unseen tail
of that truncated response. The handbook's printed body page equals PDFpage
minus14; TN3397 printed page>=3 equals PDFpage+1.

`pdfinfo` ran on handbook and presentation. Results: handbook119PDFpages,
presentation25PDFpages; source identity is the document cover/issue, not PDF
creation metadata. `pdftotext -v` returned Poppler22.02.0. `sha256sum` ran on
the three PDFs and all paths listed in SOURCE_VERSIONS.tsv; matched PDF hashes
supplied by dispatch, and TM2 matched its PE1 source-ledger hash.

`rg --files /tmp/goce_pe1_review.28tzLa /tmp/udt-pe-primary-wacMzS` listed only
temporary source/render paths. Existing renders were read with `view_image`:

- `/tmp/udt-pe-primary-wacMzS/alg_p08.png`
- `/tmp/udt-pe-primary-wacMzS/alg_p61.png`
- `/tmp/goce_pe1_review.28tzLa/egu2018_slide7.png`

These provided visual cross-checks of arm notation, Algorithm16, and the
calibration input diagram. Other pages were inspected as extracted text, not
claimed to have full equation/layout verification. No rendering or derivative
copyrighted source file was added to the repository. Source excerpts remain
in transient tool output; repository records retain paraphrases/locators and
hashes only, not whole documents or copyrighted pages.

No web searches or new document/page retrievals were made by this reviewer;
the main task's retrieval budget was not consumed. Official support routing
has not yet been independently verified; main will supply the exact candidate
source, if needed for direct review.

## Source-first seal

`sha256sum` returned at18:16:39 UTC:

```text
c114fbd7c98be748f6e5d9dfdaf0c411464dc1f037bcd5510531094fce452597  SOURCE_FIRST.md
4cc7c993fcebfc3d5f5a05d21f759a615482716b81c199514f250e0cf89082d1  SOURCE_VERSIONS.tsv
```

Main was notified of readiness and these hashes only; source-first findings
were withheld pending main's candidate freeze. A hash establishes exact
content correspondence, not independent truth or timestamp authenticity.

## Checks deliberately not repeated

No TM1/TM2 proof/check replay, registry-wide premise rerun, GOCE processor
implementation, flight-error validation, injection/recovery test, archival
payload/header authentication, release census, cross-model or human review,
or scientific promotion check. They are outside this bounded documentation
review; a documentation verdict must not imply completion of these checks.
