# Development notes

The final derivation and verifier pass. Two implementation-level false failures occurred while the
independent SymPy calculation was being written:

1. SymPy returned an optical primitive in a form not structurally identical to the displayed
   logarithm. The check was corrected to differentiate the primitive and independently evaluate
   the endpoint limit. No physical expression, branch, or expected result was changed.
2. An unconstrained symbolic expression obscured the one-sided positive square-root limit at the
   WR-L wall. The calculation was rewritten with `epsilon=1-r/X>0`, which is the preregistered
   interior approach. No tolerance or physical premise was introduced.

The verifier also exposed and corrected three fail-closed bookkeeping errors during construction:
an outdated row count after the closure ledger was expanded, a literal Unicode/source-spelling
mismatch, and a potentially vacuous raw-flux catch-proof. The final catch-proof changes the flux
status and invokes the full quantity-ledger validator, so its PASS is exercised rather than vacuous.

One orchestration failure occurred while recording the final candidate-census transcript. The
Git-history census exceeded the shell's initial yield and remained active while a consumer was
started, so the consumer detected a partially rewritten TSV containing sparse NUL bytes and failed
closed. The writer was isolated and polled to exit code 0; the final TSV has 1,062 physical lines
(header plus 1,061 rows), zero NUL bytes, and is regenerated before all final consumers. The failed
consumer result was not used as evidence.

These were code-construction corrections before banking. They do not alter the preregistered
question, evidence grades, surface identities, or maximum conclusion.
