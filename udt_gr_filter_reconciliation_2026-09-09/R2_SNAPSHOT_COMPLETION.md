# Completing the same grouped R2 repair

During focused review, parent and reviewer identified another instance of
R2's same authenticated-snapshot defect: the transition JSON was SHA-checked
as bytes, then parsed through a separate read_text. The first repair closed
the registry reread but not this transition reread. This is not merely a
multi-file atomicity caveat and the first repair is NOT labeled complete.

The first repair patch/14-file seal and its actual352-pass tests remain
unchanged evidence. The grouped R1/R2 repair is completed by retaining each
authenticated source byte buffer and parsing the transition from that
already-authenticated buffer. No additional defect class, scientific premise,
authority wording or registry change is introduced. No further repair class
is authorized by this record.

The added test restores the old G312 row and makes a hypothetical second
transition read return an unpinned matching after_line. Both current and
historical guards must reject the old row, and the second read must never
occur. Final focused review must check both R2 seams and R1, not only the
original71 probes. Final actual full365 must still be attempted.

Parent applied this completion before the reviewer's supplemental output
arrived. If the reviewer had not already loaded the first repair, its old-
version probe uses a hash-verified POST-HOC reconstruction from preserved
REPAIRED_IMPLEMENTATION.patch plus baseline Git; it must not be described
as a contemporaneously saved full-source file. Review receipts determine
the actual execution sequence. The pinned earlier patch itself is original.

FINAL_IMPLEMENTATION.patch and FINAL_IMPLEMENTATION_SHA256SUMS identify the
completed grouped-repair candidate. Those are evidence freezes, not revised
current-status pages. The verdict and original false-pass evidence remain
explicit; checksums do not establish independent chronology or truth.
