# G134 repair record

The first production execution returned 22/23 because SymPy structural matrix equality did not
automatically simplify the symbolic conformal-weight residual. The check was changed from direct
structural equality to entrywise simplification followed by exact comparison with the zero matrix.

The repaired route passes 23/23. The independent Fraction route had already passed the same
conformal-weight claim. No equation, candidate, premise, witness, tolerance, or landing changed.

## External-review intake-count repair

The first sealed intake had 25 manifest-listed payload files plus `REVIEW_MANIFEST.tsv` and
`REVIEW_SCOPE.json`, for 27 files total. Its scope field `file_count_including_manifest` correctly
reported 26 but did not explicitly distinguish that subtotal from the total including the scope
file. The fresh reviewer classified this as a medium boundary defect.

The builder now records all three quantities explicitly: manifest-listed payload files, files
including the manifest, and total intake files including the scope. No scientific file, equation,
premise, witness, or landing changed because of this repair.

The corrected sealed intake contained 19 manifest-listed payloads, 20 files including the manifest,
and 21 files including the scope. External Codex `gpt-5.4` verified every corrected hash and these
three counts in a fresh repair-only context, then returned `FOLLOWUP_PASS`. The bounded scientific
landing was retained unchanged.
