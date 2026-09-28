# Horizons specialist: bounded check freeze

Recorded 2026-09-28 before running symbolic checks. Mathematical exploration
preceded this freeze; the proposed formulas are author candidates, not independently
reviewed results. Work order: ../WORK_ORDER.md; parent startup and full premise
audit are attributed, not duplicated. HEAD independently checked:
be806b1830b24328caf47d99328fc1ecf992e6fe on grok.

Question: in supplied static positive-lapse Lorentzian comparison metrics, what
additional endpoint restriction follows if infinite redshift must also have infinite
radial null affine extent? Compare the distinct SR boost and accelerated-observer
limits and derive the local static acceleration/tidal relation. Maximum claim:
conditional mathematical restrictions/counterexamples, no native profile selection.

Frame: metric-led exact calculation in c_E=1 units. Staticity, selected comparison
congruence, radial product sector, function N, boundary class, and positive constants
are free-and-explored mathematical restrictions, not physical UDT premises. The
supplied regular pair readout/normalization and its source limits are pinned-by-THEORY
only to G176/current program at their conditional/working grades. No G312 equation
is assumed. No spatial radial center or physical preferred observer is selected.

Objects: g=-N(l)^2 dt^2+dl^2 on a static radial sector, with optional flat transverse
product for an actual Lorentzian four-metric; N>0 and sufficiently smooth on the open
domain. A freely chosen reference static clock fixes N(0)=1. delta=-log N is the
matched static source-to-reference redshift depth, not an arbitrary pair depth.
Use the standard curvature convention R^a_bcd=partial_c Gamma^a_db-...
Define K=N''/N by explicit computation, avoiding convention-free tidal signs.

Checks: exact Christoffels/Ricci for g, static acceleration, radial null conserved
energy/geodesic residual, reciprocal coordinate dr=N dl, analytic integral
primitives for N=(1+k l/p)^(-p), p>0, and N=exp(-k l); inertial Doppler maps,
uniform-acceleration send/return maps; exact Rindler transform; Schwarzschild
comparison small-x metric relative errors. No data, optimization, PDE solve or
numerical sampling. Symbolic residual tolerance exactly zero; failures are retained
and stop their dependent claims. Explicit counterchecks must distinguish gamma from
received Doppler and optical from affine extent.

Resources: CPU only, at most two threads and 2 GiB, one symbolic process, timeout
600 s; artifacts in this horizons/ subtree only. No GPU, grids or host-idle claim.
No fresh measurement/fit, no OFS coefficients used. OFS REVIEWED_RESULT was read
as directed and its first section exposed coefficients; this is not a blind-data
claim. No sibling solutions seen before INITIAL_NOTE sealing.

Omissions: general nonstationary/rotating caustic geometry, full kernel native
membership, Einstein/source-law adoption, global extension classification, physical
light transfer, measured local GR precision, selection of X_max. The checks support
the author derivation and are not independent review. Parent arranges a fresh reviewer.
