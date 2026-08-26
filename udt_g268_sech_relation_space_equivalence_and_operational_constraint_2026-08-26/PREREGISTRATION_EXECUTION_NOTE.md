# G268 preregistration execution note

The frozen question, landings, domains, tests, and maximum conclusion were committed and pushed at
`fc9b13ca` before outcome computation.

The first production invocation stopped before writing `DERIVATION_RESULT.json` because SymPy did
not automatically simplify three real-branch hyperbolic identities. The implementation was
repaired without changing a premise, candidate, tolerance, domain, or landing:

- hyperbolic expressions are normalized through exponentials before exact cancellation;
- `atanh(tanh(delta))=delta` on finite real depth is verified by exact unit derivative and equality
  at the origin, together with the declared real-domain range of `tanh`.

The repaired production run then executed the preregistered contract. No outcome-dependent
physical retuning occurred.
