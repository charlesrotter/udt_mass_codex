ACCEPT_WITH_REQUIRED_REPAIRS

- Independent algebra passes. From `theta_j=L_ij theta_i` and `bar_theta_j=R_ij bar_theta_i`, I
  obtain

  ```text
  E_j=L_ij E_i R_ij^-1,
  L_ik=L_jk L_ij,
  R_ik=R_jk R_ij.
  ```

  For `E=[[A,0],[DS,D]]`,

  ```text
  E^-1=[[A^-1,0],[-S A^-1,D^-1]],
  delta(E) E^-1=[[delta(A) A^-1,0],[D delta(S) A^-1,delta(D) D^-1]].
  ```

  Direct differentiation also gives

  ```text
  e_j=ell_ij+Ad(L_ij)e_i-Ad(E_j)r_ij.
  ```

  The orders and signs in `EXACT_DERIVATION.md` Sections 2–4 were correct.

- The central non-obstruction theorem is valid under its proper hypothesis: on a smooth paracompact
  base, once smooth rank-two bundles `N,Q` are supplied, `Sym^2_+(Q*)` admits a global section by
  convex partition-of-unity gluing and `Hom(N,Q)` has its invariant zero section. No global screen
  frame, global coframe, parallelizability, zero-mixing selection, action, or nonnull `dphi` is
  required.

- Required globalization repair: the generic two-sided `GL(4)` identity alone does not prove that
  arbitrary `L_ij,R_ij` preserve the seven-dimensional triangular fiber. State explicitly whether
  the supplied reduction is a smooth split of `TM` or `T*M`, name the metric used in `Q=N^perp`, and
  derive both transition laws—especially the omitted mixing law, schematically
  `sigma_j=Q_ij sigma_i P_ij^-1` under the chosen convention. A single query point proves only
  fiberwise existence; the global query claim lives over the total pair-frame query bundle.

- Required reversal repair: “every closed reciprocal transition loop has even reversal parity” is
  too strong. Only a product required to equal the identity—such as a triple-overlap cocycle
  closure—must have even `F` parity. A nontrivial `Z2`-twisted bundle can have odd monodromy around a
  noncontractible loop. Correct the current derivation and ledgers without rewriting immutable
  historical evidence. This is necessary for consistency with retained reversal-twisted family F03.

- Required ledger repairs: B05 says `Hom(B,N)`, while the derivation and report use `Hom(N,Q)`; I12
  likewise says `Hom_B_N`. Normalize the bundle typing. Also qualify V17: crossing a
  rank-changing/projector-degenerate stratum can be a tangent in an ambient configuration space, but
  it is not a tangent within the fixed-rank bundle tile.

- Query bundle versus field section is otherwise handled correctly. Bundle-container existence does
  not create a spacetime section; a realized reciprocal field, global `phi`, time orientation,
  topology/boundary glue, rank-changing atlas, variation ownership, and native law remain open.

- Banking-verifier repair: `verify_audit.py` searched for `ACCEPT` as an arbitrary substring, so a
  rejection discussing `ACCEPT` could pass, and `ACCEPT_WITH_REQUIRED_REPAIRS` could pass before
  repairs were applied. Parse the first verdict token exactly and require documented repair closure
  before final `PASS`.

Read scope/commands: first read `REVIEW_DISPATCH.md`; inspected every textual package file with
`nl`/`sed`, enumerated all files with `rg --files -uuu`, and inspected compiled-cache metadata with
`file`/`sha256sum`. Read the manifest-controlled skeleton, reciprocal-bundle, screen, cocycle,
premise, variation, completion, and temporal sources; used targeted `rg -n` for remaining manifest
sources. Independently checked all 24 manifest rows against current SHA-256, size, and HEAD blob:
zero mismatches. Neither packaged verifier was run.

No files were changed, created, deleted, staged, committed, or pushed. Final tracked and cached diff
checks both returned zero; final status matched the initial pre-existing untracked state.
