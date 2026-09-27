# Source-first mathematical check plan

Reviewer: `/root/postulate_math`, separate context, inherited model (exact model
identifier not exposed; different-model independence UNTESTED). Baseline independently
observed: `97af29a72322fa686dd0158a33947a91ac27d678`, branch `grok`.
Parent's completed startup, earlier 406-row PASS and this-turn successful sync are
attributed, not independently replayed here. Local HEAD/status were checked directly.

Question: does inverse clock/ruler structure merely normalize a pair, or constrain
the primary static spherical geometry? What does a full Einstein-tensor diagnostic
then say, without making Einstein's equation a UDT law?

Frame and quantifiers: exact symbolic differential geometry on any connected open
interval in r>0 with positive C2 functions A,B (and f when specialized), static
diagonal spherical metric, regular angular chart. x0=c_E t is dimension-matched.
Staticity, round areal spheres, diagonal form, and the selected diagnostic are
declared restrictions. Existing primary f/B relationship is pinned-by-THEORY only
at F1-F4's stated source-relative grade. General A,B are free-and-explored controls,
not declared physical UDT solutions. No radial profile is fitted or proposed.

Methods: independently implement Christoffel -> Ricci -> mixed Einstein from a
metric matrix in SymPy, without importing repository scientific code. Check all
components; separately verify matrix pairing/normalization/reconstruction. Exact
symbolic zero is required, no floating tolerances or finite numerical census.
Retain equations, actual results, stdout/stderr, versions and source SHA-256 pins.

Checks:

1. F2's preserved conversion form and non-preserved fixed Lorentz readout.
2. W1's shifted-pair normalization and full pullback reconstruction with density.
3. Generic areal A,B Einstein difference; specialize B=1/A and verify G257/G260.
4. Existing angular-residual/Bianchi identities, vacuum and trace-balanced branches.
5. An explicit positive A,B control with AB nonconstant: pair normalization still
   works, while Einstein difference is nonzero. This distinguishes the operations;
   it does not establish native admission of the control.
6. Full angular sector versus isolated two-dimensional Einstein tensor.

CPU only, one small symbolic process, timeout 120 seconds, no GPU/grid/data; output
below 1 MiB. Stop on timeout, contradiction or a requirement for new physical
premises. Maximum claim is source-relative exact algebra plus external GR scoping.
No empirical, source, matter, dynamical-law, global-completeness or canon claim.

Exposure: before this freeze the reviewer read the work order, current authority,
F1-F4/W1/W4-W6, G176/G213 and G257/G260/G312 source arguments, previous FSR1/PJC1
candidates. No current investigation candidate, parent proof, new output or prior
review verdict was exposed. The parent additionally requested checking generic
A,B and G^r_r-G^t_t versus AB const; this targeted question exposure is explicit.
The independent implementation is formula-exposed and source-first, not blind.
