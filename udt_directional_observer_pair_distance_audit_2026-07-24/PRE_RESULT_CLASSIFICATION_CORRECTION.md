# Pre-result classification correction

This correction is registered before the directional audit is banked.

## Issue

The initial implementation distinguished complete on-shell branches but used
“complete metric witness” too narrowly. The conditional stationary `C^2`
source also supplies a smooth complete constant-squashing `S3` metric as an
off-shell mathematical control:

```text
h_s=b^2[e1^2+e2^2+s^2 alpha^2],  s>0,

e1=d eta,
e2=sin(eta)cos(eta)(d xi1-d xi2),
alpha=cos(eta)^2 d xi1+sin(eta)^2 d xi2.
```

Only `s=1` was observed on shell in the bounded solve. The `s!=1` metrics
must nevertheless remain in the geometry census.

## Corrected distinctions

The audit will keep separate:

1. `COMPLETE_METRIC_CONFIGURATION`;
2. `COMPLETE_ON_SHELL_CONDITIONAL_BRANCH`; and
3. `COMPLETE_CLOCK_SOLDERED_PHYSICAL_BRANCH`.

The constant-squashing family is category 1 only. The round B19 witness is
categories 1 and 2. No current witness is category 3.

## Frozen added calculations

For the constant-squashing control the audit may derive only:

- its smooth positive complete metric for `s>0`;
- transitivity/no privileged point under the metric's preserved homogeneous
  action;
- exact Hopf-fiber closed-geodesic length `2 pi b s`;
- exact horizontal great-circle closed-geodesic length `2 pi b`;
- the two corresponding half-path lengths to the antipode; and
- bounds or sensitivity statements that follow without solving the full cut
  locus.

It may not claim an exact directional cut-distance band, injectivity radius,
diameter, physical `X_max`, or CMB signal without a complete geodesic/cut
analysis.

## Corrected maximum conclusion

The on-shell round branch may yield an exact zero directional band. The
off-shell squashed control may establish that no privileged center is
compatible with nonround directional structure, but any exact nonround
`X(p,n)` distribution remains open until separately computed.

This correction changes no source candidate, physical premise, or action
status. It prevents the false statement that the repository contains no
complete nonround metric configuration.
