# Saved-diff whitespace diagnostic

The final cached whitespace check reported eleven single-space empty context
lines in LIVE_SURFACE_DIFF.patch. These are unified-diff syntax in the saved
evidence artifact; the six edited source documents themselves passed their
whitespace check. Commit 137855d9 was created before the parent processed the
cached-check failure. No scientific failure or changed reviewed source occurred.

The saved patch is preserved byte-for-byte. The package-local .gitattributes
marks only LIVE_SURFACE_DIFF.patch as exempt from whitespace lint, because
removing its required context prefixes would corrupt the exact recorded diff.
No source, code, prose or other artifact is exempted. This is a separate
packaging-only commit, with no history rewrite or scientific re-review claim.

After this format rule, the complete change receives a fresh whitespace check;
the patch is compared again with the exact six-file baseline diff, all reviewed
science/documentation/source hashes are checked, and the manifest is refreshed.
The final response reports the actual push result. Earlier check and review
records retain their original time and scope.
