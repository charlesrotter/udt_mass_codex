# G336 external review transmission

Date: 2026-09-03

Charles authorized the sealed 36-file intake at `/tmp/udt_g336_review_27k8tq7e` for fresh,
read-only external `gpt-5.4` adversarial review, including read-only authentication-file use and
network access solely to launch it.

Authenticated before launch:

```text
REVIEW_SCOPE.json     70ac4575f02d4d6d8abdbc205da6bdaa5fbd89ad6d08ae1a779665b5cfcf76dd
REVIEW_MANIFEST.tsv   1dc5b132aac35ac14de9b64b190f2d2a4e18222aed3aa276edafbb38754cee27
detached seal         2c2610c3439e17c3b8e5cbd09b705526265af9b534e5afe328ede5648e479a44
manifest payloads     34 PASS
```

The intake and authentication file were mounted read-only. The reviewer had writable ephemeral
work and return directories, no repository or protected-package mount, and web search disabled.
It authenticated the exact file set, copied the evidence to writable work, independently rederived
the mathematics, and passed all four registered replays.

Returned verdict:

```text
ACCEPT_WITH_REPAIRS__G336_BOUNDED_SILENT_SECOND_JET_RETAINED
```

The sole finding was the textual strict-domain slip registered in
`PREREGISTRATION_EXTERNAL_REPAIR.md`. No mathematical or scientific claim was refuted.
