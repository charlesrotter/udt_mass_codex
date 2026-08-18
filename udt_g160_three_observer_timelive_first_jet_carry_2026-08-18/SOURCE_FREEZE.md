# G160 source freeze

Date: 2026-08-18

The ten sources in `SOURCE_MANIFEST.tsv` are frozen at repository commit `4a89d922`. Production and
independent scripts must verify each source from `git show 4a89d922:<path>` by byte count and
SHA-256 before accepting an outcome.

Protected untracked packages, observations, archived execution chronologies, and the stopped
native-on-shell draft are excluded and must not be read, cited, or staged.
