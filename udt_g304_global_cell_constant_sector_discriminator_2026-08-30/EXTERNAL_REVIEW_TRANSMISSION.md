# G304 external-review transmission record

Date: 2026-08-30

- authorized intake: `/tmp/udt_g304_review_bcgdvogo`
- total file count: `40`
- manifest payloads: `38`
- `REVIEW_SCOPE.json` SHA-256:
  `d038816e9c1f7da0acfbc097f4523531b23d2554d911990095c0444ca3997f7e`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `a6059c578c0962dea4d41b9960c5fd46aa7732c32679aa8ae18d50f9efa789df`
- detached seal SHA-256:
  `be94b3a6195cfb6eee798558f207e67898655256dc7cd4c8f97e24dd3219868b`
- reviewer/model: external Codex `gpt-5.4`, high reasoning
- session: `01a053c0-a441-7d90-881c-5de8eba8c621`
- final response SHA-256:
  `7e737ad4826e4024fcbb57dde8e78793630d782a2a36a2b1cbea3abfa2dc0a65`
- transcript SHA-256:
  `3eb1cbaaff758cc3d3fb5353df8ba1efe90b42f96fae697bd78668e1835054db`
- verdict: `VERIFIED_WITH_CAVEATS`

Charles explicitly authorized read-only authentication-file use and, after a safety pause,
shared host-network access solely to contact the Codex API. The intake and authentication file
were mounted read-only inside an isolated bubblewrap environment. The reviewer was prohibited from
web browsing, downloads, repository access, protected-package access, evidence edits, or research
continuation.

The reviewer independently reproduced the geometry, all eight domain rows, the sign discriminator,
the G17 scope boundary, the WR-L residual, and 14/14 frozen source hashes. It required two
mechanical replay-packaging repairs before banking and requested no scientific weakening.
