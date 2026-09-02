# G323 independent-verifier failure and repair

The first independent run failed closed before producing `INDEPENDENT_VERIFICATION.json`.

Its generic centered finite-difference derivative of the independently reconstructed Christoffel
array gave a maximum Ricci cancellation error of `1.274324063161e-06` at `R=0.73`, above the frozen
`5e-8` code threshold and far above the preregistered `5e-10` numerical-error ceiling.

The repair did not relax a tolerance or change the candidate geometry. It replaced that noisy
finite-difference derivative with explicit derivatives of the independently reconstructed nonzero
connection components. The repaired Ricci route remains independent of production's exact dual-
number metric/index implementation. Its four residuals are between `4.44e-16` and `1.14e-13`.

The extrinsic check retains a separate centered derivative only for the solved embedding function;
its maximum error is `1.224e-10`, inside the preregistered `5e-10` ceiling. The executable threshold
was aligned to that frozen ceiling after the successful diagnostic.

No scientific landing or maximum conclusion was changed.

