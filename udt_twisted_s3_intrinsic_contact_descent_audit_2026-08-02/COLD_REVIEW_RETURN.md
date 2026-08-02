# Fresh zero-context adversarial review return

Reviewer: `/root/intrinsic_contact_cold_review`
Date: 2026-08-02
Repository mode: read-only; scratch work under `/tmp`; no repository edit

## Independent method

The reviewer did not import the production code. A fresh PyTorch float64 CPU implementation rebuilt
the unit-quaternion stereographic `S3` coframe, full coordinate metric, Killing covector and exterior
derivative, four-dimensional Hodge-normalized Killing twist, unit clock/ruler fields, pair/screen
projectors, projected `dT_flat,dS_flat`, and their full metric contractions.

It tested all three `lambda=-1,0,+1` metrics at three parent-preregistered points and the exact
`u=4,11` endpoints: 15 coordinate checks total. An independent SymPy rational helper computed exact
values at the three nontrivial points.

## Mathematical return

The reviewer independently reproduced

```text
Q_T=4 u^(-1-2 lambda),
Q_S=4 u^(+1-2 lambda),
Q=4 u^(-1-2 lambda)(u^2-1).
```

Maximum absolute errors were:

- `Q_T,Q_S,Q`: `3.98e-12`;
- raw twist normalization: `1.44e-15`;
- projector idempotence: `6.74e-15`.

The normalized twist aligned with `theta1` to machine precision, with `T^2=-1`, `S^2=1`, and
`T.S=0`. The exact range, positive-only causal stratum, `dphi`, `dsigma`, `dz`, and zero alternating
two-form identities were independently sustained. Signs, orientations, and constant Killing
normalization did not change the projectors or squared contractions. Controls and all excluded
scopes remained blocked.

## Adversarial correction and closure

The first verdict was `VERIFIED-WITH-CAVEATS` because the production atlas bundled absolute `phi`
and `sigma` together as reference-dependent. The reviewer showed that on the frozen `a=R=1`
witness

```text
Phi_contact=(1/4)log(Q_S/Q_T)=phi
```

is an absolute dimensionless metric scalar. In the unfrozen constant-parameter family it becomes
`phi+(1/2)log(R/a)`, so no universal founded zero follows. The dimensionful product `Q_S Q_T`
still leaves absolute `sigma` reference-dependent.

The preregistration remained unchanged. O13 was resolved within its stable parent identity through
`O13_SUBCLASSIFICATION.tsv`; producer, result, atlas, status, exact derivation, audit, lay report,
and semantic base assertion were repaired. A fresh follow-up verified the repair and all 24 catches.

Final verdict: `VERIFIED` in the exact preregistered witness-local scope. All four gates pass.

## Preserved implementations and hashes

- independent coordinate verifier:
  `60ab5a11767dcefa60a7178c991b5294ac16263c4c720317d5902d37e5f739f1`;
- independent exact-value helper:
  `2a9b924f330f312f799d023cdb3d633c4cd083cec99077ad3c4fa9b59ae2b603`;
- independent source-manifest verifier:
  `69fdeee14ce22e42c50f3cc2bf51ebba3af470627b278a7a43cf8f1d5902fdc3`;
- frozen source manifest:
  `b0ea71998dc5e0cb1c2e1aebe4f256c541863e062ceaf30625e304e80765ad4d`;
- unchanged preregistration:
  `2535d0be7eca5213afb83210adebde2820da502e35baeee6d14eac1bf007144c`;
- repaired semantic verifier:
  `f35a8e2f58d34ebed387cc8b8483e33ad97afb8002aac58dc2ebb67424b8b8c9`;
- repaired result:
  `cc49a65de1d888b01d19f66e6ff069e8eaf3d101505ffb3b4c59dd346af5b724`;
- repaired atlas:
  `4b03f0206f5d9b9e3921e074eb67db765ab46be2b6c6fbf059a8d801da86fa8a`;
- repaired catches:
  `35047e72d558b61a179b031600062796b063d511ba8c13e52520f959015c39a5`.
