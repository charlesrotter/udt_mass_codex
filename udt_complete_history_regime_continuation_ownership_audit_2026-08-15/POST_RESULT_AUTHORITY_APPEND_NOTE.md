# Post-result authority append note

`CURRENT_SCIENTIFIC_PREMISES.tsv` was a preregistered input at SHA-256
`9cc5a500a35e309d2d4be373d871a310106ae9deb2569c1960da45e51597ff1c`.

After the result, the live registry acquired exactly one final row: G98, which records this audit.
That administrative self-registration was not an input to the derivation. Removing exactly the
final G98 row from the current live file reproduces the preregistered SHA-256 above byte-for-byte.

The source manifest remains unchanged. Production, independent, and package verifiers therefore:

1. require G98 to be the final and only projected row;
2. remove it in memory;
3. hash the resulting pre-result bytes against the frozen manifest.

This is an append-only authority bookkeeping note, not a source substitution or scientific
correction.
