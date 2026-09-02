# G324 External Adversarial Review Response

I authenticated the sealed intake before relying on it. The top-level manifest hash in
`/intake/REVIEW_MANIFEST.sha256` matches the computed SHA-256 of `REVIEW_MANIFEST.tsv`, and every
payload row in `REVIEW_MANIFEST.tsv` matched both its recorded SHA-256 and byte count. I inspected
only `/intake`, except for copying the authenticated package into `/work/g324_review` to run the
registered commands, and I did not edit any evidence file.

## Findings

1. **Load-bearing theorem step is not fully authenticated from the sealed evidence, so the current method does not close the MGHD equality claim.**
   The proof of `C2` inextendibility in [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:142) explicitly uses three GLS ingredients, including item 3, “the time-dual statement holds for a past boundary,” and then uses that past-boundary geodesic localization at [lines 157-159](/intake/package/EXACT_DERIVATION.md:157). But the sealed primary-source evidence file [GLS_PRIMARY_SOURCE_EVIDENCE.json](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:1) contains exact quoted fragments only for nonempty boundary and the future-boundary endpoint statement at [lines 16-17](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:16). The regularity/global-hyperbolicity hypotheses and the past-boundary time-dual step appear only inside `scope_paraphrase` at [line 18](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:18), not as authenticated quoted theorem content. The declared import is also narrower in [PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:15): it records GLS only for “future C0-boundary exclusion from future timelike completeness,” not for the additional past-boundary endpoint theorem actually used. Because the contradiction at `R -> 0` needs the past-boundary localization step, this is a load-bearing support gap, not a cosmetic citation issue.

2. **Three of the four registered replay commands fail exactly as written.**
   The registered commands in [REPLAY_COMMANDS.txt](/intake/package/REPLAY_COMMANDS.txt:1) write into `.review_runtime/...`, but the directory is never created by those commands. In a clean writable copy, the first three commands fail with `FileNotFoundError` at the output write sites in [derive_taub_mghd.py](/intake/package/derive_taub_mghd.py:164), [verify_independent.py](/intake/package/verify_independent.py:203), and [run_catch_proofs.py](/intake/package/run_catch_proofs.py:42). Only `python3 -S verify_package.py` passes as written. After I created `.review_runtime/` manually, all four commands completed. This is a bounded repair, but it is still a real failure under required attack 9.

3. **The package self-verifier does not actually replay the first three commands as registered.**
   [verify_package.py](/intake/package/verify_package.py:103) claims an “Exact replay,” but it redirects outputs to a temporary directory at [lines 112-117](/intake/package/verify_package.py:112) instead of exercising the paths from `REPLAY_COMMANDS.txt`. That is why `verify_package.py` passes even though the first three registered commands fail verbatim in a fresh copy. This does not refute the mathematics, but it means the package overstates its command-level replay hygiene.

## Independent attack results

1. **Kasner transformation, Ricci tensor, and Kretschmann scalar:** pass.
   From
   \[
   g_\mu=-\frac{R}{\mu}dR^2+\frac{\mu}{R}dX^2+R^2(dy^2+dz^2),
   \]
   the change of variable \(T=\frac{2}{3\sqrt{\mu}}R^{3/2}\) gives `-dT^2` exactly, and the metric becomes diagonal Kasner with exponents \((-1/3,2/3,2/3)\). Those satisfy \(\sum p_i=\sum p_i^2=1\), so the vacuum Kasner Ricci identities give `Ric=0`. Directly from the `R`-chart,
   \[
   \Gamma^R{}_{RR}=\frac1{2R},\quad
   \Gamma^R{}_{XX}=-\frac{\mu^2}{2R^3},\quad
   \Gamma^R{}_{yy}=\Gamma^R{}_{zz}=\mu,\quad
   \Gamma^X{}_{RX}=-\frac1{2R},\quad
   \Gamma^y{}_{Ry}=\Gamma^z{}_{Rz}=\frac1R,
   \]
   and the Kretschmann scalar reduces to
   \[
   R_{abcd}R^{abcd}=12\mu^2R^{-6}.
   \]
   I found no tensor error in the package on this point.

2. **Conserved momentum first integral and all timelike branches, including `p_X=0`:** pass.
   The translational Killing fields give
   \[
   p_X=\frac{\mu}{R}\dot X,\qquad p_y=R^2\dot y,\qquad p_z=R^2\dot z.
   \]
   Substituting into the norm constraint yields
   \[
   \dot R^2=p_X^2+\frac{\mu(p_y^2+p_z^2)}{R^3}-\kappa\frac{\mu}{R}.
   \]
   For unit timelike geodesics, `kappa=-1`, so \(\dot R^2>0\) for all `R>0`. In the chosen future orientation, future-directed timelike geodesics have `dot R>0`. As `R -> infinity`,
   \[
   \frac{d\tau}{dR}=\frac{1}{\sqrt{p_X^2+\mu P/R^3+\mu/R}}.
   \]
   If `p_X != 0`, this tends to a positive constant, so the proper-time integral diverges. If `p_X=0`, then \(d\tau/dR \sim \sqrt{R/\mu}\), which also diverges on integration. I found no missed finite-future-proper-time branch.

3. **Compact-slab / finite positive `R` endpoint attack:** pass.
   On any slab `a <= R <= b` with `0<a<b<infinity`, the metric coefficients, inverse coefficients, and Christoffel symbols are bounded on the compact quotient. The first integral bounds `dot R`; the conserved momenta bound the spatial coordinate speeds. So a geodesic with finite parameter endpoint while staying in such a slab has bounded state and extends by the standard geodesic ODE continuation theorem. I found no finite-positive-`R` endpoint.

4. **Extension endpoint at `R=infinity`:** no counterexample found.
   With the chosen time orientation, `R` increases on future timelike curves and decreases on past timelike curves. A past-boundary endpoint geodesic, if supplied by the theorem interface, cannot run from a finite interior point to `R=infinity` while remaining past-directed. So the only remaining candidate endpoint is `R -> 0`.

5. **`R=0` / curvature obstruction:** conditionally pass.
   Once a boundary-reaching past-directed timelike geodesic is available, the scalar \(12\mu^2/R^6\) diverges as `R -> 0`, which is sufficient to obstruct a `C2` endpoint and only a `C2` endpoint. The package correctly keeps past `C0` inextendibility outside its claim at [EXACT_DERIVATION.md lines 178-179](/intake/package/EXACT_DERIVATION.md:178).

6. **MGHD-surjectivity implication:** conditionally pass.
   Given smooth time-oriented `C2` inextendibility, the step from G323’s data-preserving embedding into the G322 smooth MGHD to surjectivity is sound. G322’s category is explicitly fixed-datum, smooth, time-oriented, and data-preserving at [G322 EXACT_DERIVATION.md lines 83-95](/intake/sources/udt_g322_g321_maximal_globally_hyperbolic_development_2026-09-01/EXACT_DERIVATION.md:83). A proper image would indeed define a proper smooth, hence `C2`, extension. I found no separate flaw here.

7. **Inherited lattice-modulus claim:** conditionally pass.
   The transfer step is valid if the MGHD equality step is valid. G323 already sealed the primitive quotient invariant and its strict mode dependence in [G323 EXACT_DERIVATION.md lines 148-220](/intake/sources/udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/EXACT_DERIVATION.md:148). G324 does not enlarge the quotient category; it only pushes that invariant through the claimed equality.

8. **No unauthorized physics or new model content:** pass.
   I found no introduction of a new field equation, source, action, topology choice, occupancy rule, scale, `X_max`, or kernel/angular modification. The package consistently keeps C0 past inextendibility and physical selection outside scope.

## Registered command replay

In `/work/g324_review/package`, the four registered commands behaved as follows when run exactly as listed:

1. `python3 -S derive_taub_mghd.py --output .review_runtime/DERIVATION_RESULT.json`
   Failed: `FileNotFoundError: [Errno 2] No such file or directory: '/work/g324_review/package/.review_runtime/DERIVATION_RESULT.json'`
2. `python3 -S verify_independent.py --output .review_runtime/INDEPENDENT_VERIFICATION.json`
   Failed: `FileNotFoundError: [Errno 2] No such file or directory: '/work/g324_review/package/.review_runtime/INDEPENDENT_VERIFICATION.json'`
3. `python3 -S run_catch_proofs.py --output .review_runtime/CATCH_PROOF_RESULT.json`
   Failed: `FileNotFoundError: [Errno 2] No such file or directory: '/work/g324_review/package/.review_runtime/CATCH_PROOF_RESULT.json'`
4. `python3 -S verify_package.py`
   Passed.

After creating `.review_runtime/` manually in the writable copy, all four commands passed. That repair is operational, not mathematical.

## Conclusion

I did **not** find a concrete tensor, geodesic, or modulus counterexample inside the sealed evidence. The positive case is plausible on the mathematics already written. But the present package does not authenticate the full GLS theorem interface it actually uses: the past-boundary time-dual endpoint step is load-bearing, while the sealed primary-source evidence quotes only the future-direction endpoint statement and the nonempty-boundary fragment, and the premise ledger declares a narrower import than the proof consumes. Under the review request’s allowed landings, that leaves the result unresolved rather than accepted.

Minimal bounded repairs are clear:

- seal exact support for the precise GLS hypotheses actually used, including the past-boundary/time-dual endpoint step, or narrow the proof so it avoids that step;
- align the premise ledger with the exact imported theorem content;
- make the registered replay commands create `.review_runtime/` or write to an existing output directory.

UNRESOLVED__CURRENT_METHOD_DOES_NOT_CLOSE_TAUB_QUOTIENT_MAXIMALITY
