# G225 repair-only follow-up review

Date: 2026-08-22

Primary verdict:

```text
G225_REPAIR_INCOMPLETE
```

## Accepted repair evidence

The repaired aggregate verifier exited `0` inside the sealed intake with the scientific landing
unchanged. It reproduced:

- `9` source hashes;
- `39` symbolic checks;
- `20,000` independent cases;
- `580,013` exact-rational assertions;
- `19,922` nontrivial composition defects;
- `21/21` payload mutations and `4/4` algorithm mutations rejected.

All `34/34` sealed payload hashes matched after replay. The source-resolution repair itself passed.

## Remaining mechanical evidence gap

The intake named the builder `HEAD` but did not include evidence allowing a reviewer without
repository access to verify that the R1 preregistration commit preceded the R1 implementation
commit. This is a provenance-packaging gap only. It does not reopen or weaken the accepted bounded
G225 theorem or the passing R1 replay.
