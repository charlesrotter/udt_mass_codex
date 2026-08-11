# G75 post-bank navigation layer

The 23-file G75 payload listed in `PACKAGE_SHA256SUMS.txt` is the fixed preregistered calculation
record banked at commit `e5f9730a`. Its `SOURCE_MANIFEST.tsv` correctly hashes the then-current
premise registry from base `ac01381b`.

After banking, live navigation advanced from 67 to 68 premise rows by adding the G75 status. That
expected update changes the live `CURRENT_SCIENTIFIC_PREMISES.tsv` hash; it does not invalidate the
historical calculation input. `verify_post_bank_gates.py` therefore replays that one source from
`ac01381b:CURRENT_SCIENTIFIC_PREMISES.tsv`, verifies the other source rows live, verifies all 23
banked package hashes, and separately tests the current 68-row startup surface.

This is a provenance/navigation overlay. It does not alter the G75 family, evidence, result, or
status, and it does not supply fresh blind adversarial review.
