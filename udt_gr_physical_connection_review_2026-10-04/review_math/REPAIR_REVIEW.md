# GRL1 mathematical repair re-review

Actual review: `/root/grl_math`, 2026-10-04 UTC, same reviewer context as the
sealed source-first and exposed stages. Exact model revision remains unexposed;
no new blind, different-model or human review is claimed.

Reviewed REPAIR.md SHA256
`7da831304cce71ab3937b3108317403f270b2fa1435e81d45e9aab2c2973ba71`.
Verdict: **VERIFIED-WITH-CAVEATS; M1 and M2 resolved** for this same-premise
precision repair. The candidate's operational, local-error and physical-admission
limits remain; final integration is not yet reviewed.

I actually reread the repair and checked its equations against my exposed
derivations. M1 now treats all-direction agreement as sufficient and correctly
notes that two nonparallel common timelike tangents at each point suffice
after cone matching. It preserves the one-congruence counterexample without
claiming a minimal-data theorem.

M2 correctly distinguishes retarded emission labels r_E,n_E from simultaneous
Fermi reception labels r_F,n_F. Expanding
q=(I-r_E B)^(-1)r_E n_E gives q=r_E n_E+r_E² Bn_E+O(r_E³), so the stated
distance/direction conversions and the unchanged limiting J are valid.
Compactness of the sphere gives uniform small-r conversion for this fixed B,
preserving the limiting uniform-sphere average. No finite-distance equality
has been substituted.

The scaled world-function/simple-root argument faithfully records my C1
justification. I also checked the displayed Riccati alternative independently:
put H_n=n.Bn, dot r=r H_n and dot n=Bn-H_n n. Differentiation yields

    (1/r) d(r H_n)/dt
      =n.(dot B+B²)n+|Bn|²-H_n²
      =-T(n,n)+|P_n Bn|².

This works for nonsymmetric B, so it does not silently discard vorticity.
Its use for actual received z still relies on the separately justified C1
remainder. The scalar sphere average, nonzero-H division condition, quarantined
external quadrupole and open native physical join retain their previous scope.

Preservation checks: branch grok and HEAD865a1163 remain; INITIAL_SYNTHESIS.md
retains SHA256 `c22dba85f79bb91334cad3f89ead99e0d1974f0aeebbe123f80c96efd5d56260`.
Both SOURCE_FIRST_SEAL.json and EXPOSED_SEAL.json retain their recorded hashes,
and every file they bind was independently rehashed and matched. No prior
review artifact was edited.

Omissions: no central integration was opened, no sibling report was reread,
no external literature was added, no full registry verifier or historical
science replay was run, and no scientific CPU/GPU calculation was performed.
This re-review approves the repair's fidelity and mathematics, not empirical
truth, physical adoption, source regrading or canon. Await final integration
freeze.
