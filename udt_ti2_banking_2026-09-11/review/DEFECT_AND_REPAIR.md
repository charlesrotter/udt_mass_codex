# Changed-second-snapshot regression

At 19:01:11 UTC, the independent `probe_second_snapshot.py` check demonstrated that
all eleven historical banking validators using `read_tsv` after the authenticated
historical-byte helper accepted a changed G414 row in that second read. The first
registry read was genuine. The second supplied parsed snapshot replaced G414's
NOT_PHYSICAL_ADOPTION marker with PHYSICAL_LAW_ADOPTED. Each validator excluded
G414 from those rows without authenticating that later snapshot.

`second_snapshot_initial.stdout` records eleven false passes; the capture exits1
with an explicit assertion describing the failure, not an import/dependency or
timeout failure. Duration0.120016773s, maxRSS38500KiB,2GiB/180s. Sources and the actual
registry were never changed by this probe. `INITIAL_verify_current_scientific_premises.py`
preserves the tested implementation exactly at SHA256
219975817232c91a539beb4a332d78f313dd74ae043a3b25098f49af12083344.

This is an integration defect in snapshot authentication, not a TI2 mathematical
counterexample. The strongest survivor remains the full reviewed conditional TI2
argument and its faithful prepared G414 transcription. Banking must wait for repair
and actual rechecks. No source/scientific premise or original row needs changing.

The smallest preferred repair is one authenticated actual registry snapshot per
validator, retaining a derived historical projection for the old-hash comparison
and parsing that same actual snapshot for present owned rows. Parent independently
noticed the repeated-read sites before receiving the actual counterexample, held
edits until this capture completed, and is responsible for the scoped repair.
The original probe will be rerun unchanged, with a separately named capture.
Final repair and test outcomes are not anticipated by this initial defect record.
