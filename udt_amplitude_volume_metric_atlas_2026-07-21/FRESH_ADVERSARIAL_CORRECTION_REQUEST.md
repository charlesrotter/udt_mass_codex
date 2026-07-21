# Fresh adversarial correction review request

The initial review in `FRESH_ADVERSARIAL_REVIEW.md` returned `PASS-WITH-CAVEATS` and found no
load-bearing numerical failure. Audit whether the following corrections close its actionable
caveats without strengthening the scientific conclusion:

1. all 1,160 saved metric two-jets are now curvature-reconstructed inside the verifier;
2. every entry in both named parent manifests is replayed;
3. explicit changed-Halton-base and changed-Hadamard-direction catches are exercised;
4. shear singular margin, twist norm, and mixed-curvature margin are saved and independently
   reconciled for every record;
5. source constants are bound to exact text in the committed preregistration;
6. duplicate-hash wording now identifies origin-only repetitions;
7. statistical rarity, ease, and mapping-sufficiency wording has been removed; and
8. the reports explicitly identify reused frozen geometry code and retain all finite-scope caveats.

Run the builder and verifier read-only with respect to source files if needed; their generated
outputs may be replayed only if byte-identical. Return `PASS` only if these corrections are complete
and no new load-bearing flaw appears. Do not propose physics or edit files.

