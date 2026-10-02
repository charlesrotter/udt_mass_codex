# ERC1 source-first mathematical result

The frozen independent computation completed successfully in 2.21 seconds under
the existing TPS1 capture (2 GiB virtual memory, one BLAS thread, no time cutoff).
Its 27 exact checks include symbolic component identities and two deliberately
nonzero defects; the count is not 27 independent scientific results. No
implementation repair was needed. The frozen analytic scope remains controlling.

The three tolerances for one supplied FLRW case gave maximum original tensor/
constraint residuals 1.40e-11, 2.54e-13 and 2.15e-15. The two tightest endpoint
states differed by at most 6.66e-15; finite period ratios differed by at most
2.81e-13. The finest solution gives one-way finite received/emitted period ratio
1.0204534498293365 and immediate-echo finite period ratio 1.0415126833996369.
Its final R=0.003418107981252671 differs from supplied initial R=0.1, while
F>=1.0068362159625053 on the 101 sampled audit points. These are qualified
floating-point checks, not interval certification or a proof about all times.
The independently derived constraint propagation and smooth ODE local existence
provide the analytic support for the constrained witness; sampled residuals alone
are not a PDE existence theorem.

The full static linearized metric calculation confirms both potentials and all
16 response components; off-diagonal zeros are included and are not separate
nontrivial results. Suppressing the independent spatial potential leaves a
nonzero original 00 response. Perturbing initial P by 1/1000 leaves C=3/5000,
so the constraint check is not an automatic consequence of integrating the
trace equation. Numerical spatial residuals still use RHS-derived derivatives;
they are consistency checks, not a distinct independent differentiator.

This source-first result has not yet reviewed the parent's actual candidate or
central integration. Its independent argument and code were sealed before that
exposure. Same inherited model and scientific libraries remain shared; a
different-model or different-library review is not claimed. No protected payload
was read, and only the authorized math/ workspace was written.
