# G262 evidence repair note

Date: 2026-08-25

The first package-verifier run failed closed because the G216 source hash in
`SOURCE_MANIFEST.tsv` was 62 characters: `b5` had been omitted during manual transcription.

Both the live file and the frozen preregistration Git object at `fdd18b9b` have SHA-256

```text
a30cc5ec78093ca4e1f2efb2c4156bb2b5b83143a2d41c33ab447ec2a18feed2
```

The manifest is repaired to that exact value. No source bytes, scientific equation, candidate
landing, test threshold, or result changed.
