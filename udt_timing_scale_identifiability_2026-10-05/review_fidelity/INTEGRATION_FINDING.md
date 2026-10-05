# Integration wording finding

After the candidate itself passed fidelity review, a semantic check of the
draft CENTRAL_INSERT.md found one sign-label mismatch. It says:

> the received logarithmic frequency drift is dlog Z/dt_o-dlog nu_e/dt_o.

From nu_o=nu_e/Z, the displayed RHS is **negative** logarithmic received-frequency
drift, -dlog nu_o/dt_o. INITIAL_CANDIDATE.md section2 already states the correct
minus-sign formula. Smallest source-preserving repair: explicitly label the
central quantity `negative logarithmic frequency drift, -dlog nu_o/dt_o`.
No candidate formula, physical premise or numerical output requires change.

The original insert is preserved byte-for-byte in
CENTRAL_INSERT_BEFORE_DRIFT_WORDING.md. The parent was messaged before central
integration. Final semantic review must check the corrected insertion and
adapters. Initial candidate review verdict remains scoped to its original
candidate; it did not pre-clear this later draft central wording.
