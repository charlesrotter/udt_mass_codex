REPAIRS_ACCEPTED

I verified `REVIEW_SCOPE.json` first and stayed within the sealed 41-file intake. All 40 scoped payload hashes matched, and the visible file count matched `40 + REVIEW_SCOPE.json = 41`.

Within the authorized R1/R2 surface, the package satisfies the repair contract: `ATTACHMENT_OWNERSHIP.tsv` has 18 rows with explicit Boolean `E/I/C/W` fields and 72/72 nonblank cited legs; every locator resolves inside an exact manifest source; the independent verifier rebuilds the ledger digest byte-identically and does not reference `derive_attachment_ownership.py`, `ATTACHMENT_OWNERSHIP.tsv`, or saved output JSONs. I ran all registered no-write replays with `PYTHONDONTWRITEBYTECODE=1`: production, independent, hostile, sealed-premise, and package all returned `PASS`; hostile coverage is `26/26` and includes the four new ledger-mutation catches. The sealed premise-registry replay checks the exact `233`-row `CURRENT_SCIENTIFIC_PREMISES.tsv` plus the load-bearing G249/G250 scope rows, and `COMMANDS.md` correctly distinguishes that sealed verifier from the broader repository-only startup verifier.

The retained bounded landing is unchanged: same landing string, same `18/7/3/0` census, zero observational values, zero fitted coefficients, and no anchor value, history, branch population, fit, or outcome selection. No remaining defects found within review scope.
