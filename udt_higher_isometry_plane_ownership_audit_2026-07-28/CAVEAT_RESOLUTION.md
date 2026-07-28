# Corrected-review caveat resolution

The fresh corrected reviewer returned `PASS_WITH_CAVEATS`. Its record remains unchanged. The three
bounded caveats are resolved mechanically as follows:

1. The original `FRESH_ADVERSARIAL_REVIEW.md` SHA-256 is now published in `CORRECTION_LAYER.md` and
   enforced by `verify_audit.py`:

   ```text
   21e99ac850291d189aaf578a47c238094e08d866dfa7c5c785e04408b25102cc
   ```

2. R07 no longer mentions the separately unverified constant-depth round illustration. Its
   refutation statement now relies only on the exact smooth nonconstant-depth R06 countercontrol.

3. `verify_audit.py` now pins and checks all four corrected production/independent stdout/stderr
   hashes after replay. It cannot pass merely because `run_and_capture.py` regenerated matching
   internal files.

These changes narrow or strengthen evidence bookkeeping. They do not change the corrected
scientific classification or fill the open fixed-profile and response-degeneracy classifications.
