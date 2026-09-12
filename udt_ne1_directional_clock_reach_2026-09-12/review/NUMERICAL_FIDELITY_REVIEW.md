# Direct numerical and captured-audit fidelity

The parent implementation matches its21:11:45 implementation freeze at
SHA256 `c0a38fe8f4eb37bb7a286a3b22ac4a43fcd384a53f15b902404025653dca47d4`.
Inspecting the actual equations found no scientific or coding defect.
The original-metric areal-frequency transport is

    (log omega)'=-a_t v^2-a_xi v
       +(1-v^2)[-1/(2t)+r P_t/2],

with the correct spatial-lapse sign and transverse mixture. It agrees with
the separately reconstructed metric connection. The code uses the complete
lambda derivative response and exact Bessel P; solving with rapidity and
log frequency is a change of variables, not an angle/amplitude truncation.
The source-sky zero-amplitude formula, exact equatorial control and finite
momentum upper bound match the frozen candidate. The omitted signs of the
individual transverse momenta are covered analytically by dependence on
their squares; the independent original-connection check also includes a
negative mixed transverse component.

The parent baseline and replay captured actual exit0 and byte-identical
scientific stdout, SHA256
`25dad536081e6faf44508323bb5528be5eb06d2a57947f03ca9bb9360e1e018d`.
There are144 finite endpoint cases,12 long-reception rays with five samples
each, one finite tighter-repeat endpoint and five long tighter-repeat
samples. The recorded tighter-repeat mixed scaled errors are
3.9918604346014474e-12 and4.5705485690942765e-11. No warnings were recorded.
These replays are parent same-code regression; the reviewer authenticated
the saved captures and equality rather than claiming to rerun them personally.

After freezing SAVED_STATE_CHECK_CONTRACT.md, the reviewer used a new
mpmath1.3.0 implementation at50 decimal digits to recompute frequency,
the same-sky background, contrast and finite upper bound from all210 saved
states, without importing parent code. Maximum integrated log-frequency
discrepancy was3.7535192325472774e-10; maximum stored algebraic log-frequency
discrepancy was3.8097627969422310e-10, log-contrast discrepancy
3.7535152076518155e-10 and stored log-bound discrepancy
3.8097705675173610e-10. All frozen checks passed without changing states,
equations or tolerances. The stored log contrast contains the integrated
frequency and therefore uses that comparison's2e-7 threshold; purely
algebraic stored reconstruction/bound correspondence uses2e-8. Both are
well above the observed discrepancies.

This is a distinct special-function evaluation library on the same saved
float64 trajectory states. It is not different-library geodesic integration,
an independent trajectory, a higher-precision trajectory certificate,
interval certification or an asymptotic proof. The prior reviewer original-
connection integrations are the distinct trajectory implementation.

The actual parent hostile failures are retained and authenticated:

| Mutation | Rejecting scientific check | Recorded defect |
|---|---|---|
| Drop spatial b_xi term | clock_transport |0.010191087833639693|
| Freeze lambda derivatives | clock_transport |0.004375042844665878|
| Substitute axial background | zero_amplitude_recovery |0.1324522506708322|

Each parent hostile capture exited1 and its saved scientific result is FAIL.
The reviewer also injected an actual in-memory1e-3 corruption of a saved
integrated log frequency; the unchanged saved-state metric frequency check
exited1 with discrepancy0.0009999999997787971. Original files were unchanged.
The source-stage two independent hostile failures remain separately saved.
Guard successes/counts do not imply exhaustive error detection.

The parent current398 receipt exactly matches the actual captured command,
start21:00:11.363590UTC, duration406.54052357096225seconds, exit0 and empty
stderr. Its stdout hash matches the receipt. The reviewer separately checked
present source-pin correspondence and saved that result; it does not claim
to have run or independently monitored the parent audit or an atomic input
snapshot. This audit precedes later navigation edits, whose proportionate
checks and final-documentation fidelity remain a separate final stage.

Scientific verdict remains the entire direct-review survivor, conditional
and UNPROMOTED. No numerical outcome establishes the infinite-time claims;
the reviewed explicit argument does. No scientific repair was needed.
