# Adversarial-review correction layer

Date: 2026-08-04

The preregistration remains immutable at commit `5399d850`. The fresh read-only reviewer returned
`ACCEPT_WITH_REQUIRED_REPAIRS`. This file records the append-only correction layer applied before
banking.

## 1. Ambient coframe identity versus reduced extension bundle

The ambient identity

```text
E_j=L_ij E_i R_ij^-1
```

is exact, but arbitrary `GL(4)` transitions do not preserve the local positive-triangular `3+4`
slice. The corrected global statement begins only after smooth rank-two bundles `N,Q` are supplied:
over the total pair-frame query bundle in A01, or by a smooth split `TM=N+Q` in A02. In the declared
component convention,

```text
h_j=Q_ij^-T h_i Q_ij^-1,
sigma_j=Q_ij sigma_i P_ij^-1.
```

The existence theorem is for these tensor bundles, not for one global triangular matrix.

## 2. Reversal parity

The preregistered phrase “even closed-loop reversal parity” and the inherited historical wording are
too broad. The exact algebra proves even reversal parity only for a product required to equal the
identity, including identity-required triple-overlap closure. A noncontractible loop may have odd
`Z2` monodromy. That possibility is consistent with the retained reversal-twisted family F03.

The committed preregistration and the historical
`udt_global_coframe_cocycle_audit_2026-07-20/STATUS_LEDGER.tsv` are preserved as provenance. The
current exact derivation and ledgers supersede their overbroad wording for this audit.

## 3. Type and stratum repairs

- The mixing bundle is consistently `Hom(N,Q)`.
- A path that crosses `s_phi=0` or a projector-rank defect may be tangent in an ambient stratified
  configuration space, but is not tangent within the fixed-rank bundle tile.

## 4. Evidence-gate repair

The final verifier now parses the first review verdict token exactly. A rejected review that merely
mentions “ACCEPT” cannot pass. Because the actual verdict required repairs, final `PASS` also requires
all six repair rows to be `CLOSED` and an exact `REPAIRS_ACCEPTED` replay verdict.
