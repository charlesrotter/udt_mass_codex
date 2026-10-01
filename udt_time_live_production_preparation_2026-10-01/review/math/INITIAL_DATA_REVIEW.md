# TPP1 initial-data and numerical-control review

Reviewer `/root/tpp_math`, same inherited model, actual separate context.
Startup and source exposure are recorded in `SOURCE_FIRST_REVIEW.md`.
This is the initial gate before scientific GPU histories, not final readiness.

The producer TT projector `P S P - tr(P S P)P/2` with `P=I-kk^T/|k|²`
is symmetric, transverse and trace-free for nonzero k and symmetric S.
Frobenius normalization does not change these properties. The explicit
strict-below-Nyquist guard is appropriate for the sampled seed. I found no
equation defect in the unchanged positive conformal solve or initial harmonic
velocities. Its selected CMC/conformal-flat background remains conditional.

`INITIAL_CONSTRAINTS.json` checks all ten supplied noncontrol initial artifacts
at meshes8,16,24,32, covering all scientific families and the engineering seed.
It reuses the fixed independent TDS1 NumPy original ADM/Christoffel methods,
with a new thin adapter and independently constructed SVD transverse basis.
No producer module is imported by this saved-data check. The Fourier method
is shared with the producer and no independent time evolution is claimed.

Across the scientific meshes16–32, maximum original Hamiltonian residual is
1.7422e-12, maximum original momentum residual2.9855e-13 and maximum harmonic
vector residual9.6402e-15. The engineering8³ case has H=1.2034e-6, below2e-5.
The saved TT divergence maximum is3.3304e-15; independently reconstructing
each projected seed using its transverse SVD basis agrees within4.9961e-16.
Each initial harmonic check detects an intentionally changed g00 velocity.
The exact Kasner16³ initial metric and velocity agree with an independently
constructed diagonal solution exactly, with original constraints below1e-14.
The initial48³ artifact remains a load-only input outside this checker's
bounded mesh scope; the actual worker must check its constraints too.

The principal-frequency implementation was compared onCPU against independent
ADM metric construction and all4913 cubical Fourier vectors for20 seeded
positive spatial metrics with nonzero shifts; all pass. Three invalid metric
hypotheses are rejected. This imports the producer's bound specifically to
test it; it is distinct from the no-producer-import saved-data checks.
The first2GiB capture failed while loading a Torch shared library, before the
test. The identical test passed under the work-order4GiB cap in0.815s with
416228KiB peak RSS. Both receipts/stderr are preserved. The small capture
adapter changes only the previously reviewed wrapper's allowed memory ceiling.

I flagged that halving the maximum step alone need not halve CFL-limited late
steps. Before GPU outcomes, the parent preserved the initial specifications
and also halved the fine-case CFL bound to.125. Actual accepted jump schedules
will be examined rather than inferred from a filename. The worker checks its
frozen-principal bound at all RK stages and the endpoint. This remains an
engineering control, not variable-coefficient or nonlinear stability proof.

Disposition: initial scientific inputs and reviewed local numerical controls
pass their scoped gate. Original saved-g Ricci, evolved ADM, refinement,
exact-control histories and final integration remain pending. Nothing here
selects native UDT dynamics or qualifies a multi-hour run.
