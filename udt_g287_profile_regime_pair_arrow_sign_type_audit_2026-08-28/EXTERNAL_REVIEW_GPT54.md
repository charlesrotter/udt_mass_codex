# External G287 adversarial review — gpt-5.4

## Findings

1. **Medium — vacuous hostile-catch harness.** `run_catch_proofs.py` encoded six claimed
   mutations as literal `False` values and then called each caught because it was false. Replacing
   the dictionary with an empty dictionary still returned `pass=true`.
2. **Medium — incomplete aggregate replay.** `COMMANDS.md` registered six commands, but
   `verify_package.py` did not require or execute the source-manifest and review-intake builders.
   A disposable probe made `build_review_intake.py` abort while the aggregate verifier still passed.
3. **Low — partial mechanical dependency certification.** The production script checked nine
   phrases in five files and the metadata of the 22-row dependency table, but did not mechanically
   validate every row against its cited source. The reviewer manually audited all 22 rows and found
   no scientific alias.

## Verdict

`ACCEPT_WITH_REPAIRS`

The reviewer independently retained the bounded mathematics:

- pair reversal sends `delta_AB` to `-delta_AB` while keeping `g_phi` fixed;
- profile conjugation sends `phi` and its jets to their negatives and generally changes the metric;
- a reversal-invariant regime classifier cannot be `sign(delta_AB)` alone;
- the matched endpoint-potential reduction is correctly scoped in `founding.md` and G272;
- G267 does not itself identify its two ordered-depth ends with micro and cosmological profile
  regimes;
- G286 remains open and is not closed by the sign distinction.

The clean sealed replay ran all six registered commands successfully. The repairs requested are
evidence-engineering repairs only; the scientific landing is unchanged.

