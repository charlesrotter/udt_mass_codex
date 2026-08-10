# External-review intake correction

The first sealed intake had 49 files and the correct 20 pinned sources, but its builder excluded
`EXTERNAL_REVIEW_DISPATCH.md` because of an overbroad filename-prefix filter. The reviewer verified
its working directory and discovered the missing instructions before performing the scientific
review. That run was terminated and supplies no verdict.

The builder was corrected to exclude only named prior-review outputs. A fresh intake and fresh
ephemeral reviewer are required. No source, derivation, candidate table, or classification changed.
