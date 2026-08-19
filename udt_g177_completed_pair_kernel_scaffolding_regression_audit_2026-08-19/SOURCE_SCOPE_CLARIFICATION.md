# G177 source-scope clarification

The source universe was frozen at commit `1dadbb04`. Eight package/evidence sources remain
byte-identical in the working tree. `AGENTS.md` was deliberately updated after the G177 outcome to
route startup through G177, so its current working copy no longer matches the frozen manifest hash.

Both G177 verifiers therefore check `AGENTS.md` against the exact Git blob
`1dadbb04:AGENTS.md`. The manifest, preregistered source universe, and scientific calculation are
unchanged. This is a provenance repair, not a source substitution or scientific regrade.
