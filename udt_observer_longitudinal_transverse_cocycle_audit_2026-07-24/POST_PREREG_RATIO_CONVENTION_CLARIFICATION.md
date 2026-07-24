# Post-preregistration ratio-convention clarification

Date: 2026-07-24

State: before production or independent calculation

The first preregistration commit wrote

`Q_gamma = omega_start / omega_end`.

That ordering is inconsistent with the already registered centered WR-L
readout, whose directed start-to-end ratio is

`Q_gamma = omega_end / omega_start = N_start / N_end`.

The audit therefore fixes the latter order before outcome inspection. For
successive segments `p -> q -> r`,

`Q_pr = Q_pq Q_qr`.

In the centered WR-L control, `N_start=1` and
`N_end=exp(-phi)`, hence `Q=exp(phi)`, exactly matching the frozen optical
ledger. This is an orientation convention only. Reversing the directed path
replaces `Q` by `Q^-1`; it does not change any existence, composition,
branch, or physical-solder gate.
