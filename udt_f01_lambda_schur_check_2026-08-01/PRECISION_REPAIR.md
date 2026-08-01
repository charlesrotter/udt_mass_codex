# Cold-review precision repair

The fresh independent review found no mathematical contradiction but correctly returned
`PASS-WITH-CAVEATS`: the preregistration required primary arithmetic at no less than 80 decimal
digits, while the first primary certificates used 50/60.

The original review is preserved unchanged. Before banking, both primary scripts were repaired to
run nested 80-digit/4,096-part and 100-digit/8,192-part outward interval enclosures. Both certificate
JSON files were regenerated; every refined enclosure remained nested, retained its sign, and
excluded zero. `EXACT_DERIVATION.md` was updated to describe the actual registered execution.

The same independent verifier was then rerun without changing its decision logic. It now returns
`PASS`, records `[80,100]` for both primary certificates, finds overlap on all four branches, and
reports no remaining required repair. This closes the procedural caveat without changing any
scientific sign, branch, or conclusion.

Current certificate SHA-256:

```text
53a7b62088e14724b9da496f186722043566bcd2920190a542339765a8adaecc  FREE_SCHUR_CERTIFICATE.json
6bac2c0321f1761c520202db4004e65e4d899c3a2c8c84d1ae258d2bfe673389  NEGATIVE_WITNESS_CERTIFICATE.json
28ebbc25ccce7c0072370ff892a3c7b50d28a0113e24a55b2cb9ac388b77c525  INDEPENDENT_RESULT.json
4cda4d63037403ef1dd85df5a32f695bace805e14812859048d05bb85709def6  INDEPENDENT_RAW.jsonl
```
