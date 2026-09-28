# Final packaging exception — preserved raw diff

The first staged whitespace check returned2, solely on
review/INITIAL_REVIEW_INPUT.txt. That file preserves the reviewer's raw initial
Git diff and surrounding exposure. Git diff context lines intentionally begin
with a space, including otherwise blank lines; the capture also ends with a
blank line. These are raw evidence bytes, not whitespace defects in the edited
documentation. The first failure was reproduced and preserved at
checks/staged_raw_whitespace.* after discovery, not presented as a blind check.

Keep this raw file unchanged. Its diagnostic stdout also repeats the captured
space-prefixed lines. The final whitespace gate therefore checks every staged
path except these two exact raw captures: review/INITIAL_REVIEW_INPUT.txt and
checks/staged_raw_whitespace.stdout. No global Git setting or test expectation is
relaxed for current documents. Independently require every reported whitespace
warning to name one of these exact paths and confirm their bytes against the
manifest. Reviewed document pins, scientific source pins and archive byte identity
remain unchanged. This is a packaging qualification, not a scientific repair.

The initial package manifest is retained at checks/INITIAL_SHA256_MANIFEST.json;
the final manifest includes these additional packaging records. Earlier manifest
counts refer to the pre-exception snapshot. Final stage verification and commit
record the actual scope. No scientific or documentation-fidelity review is reopened.
