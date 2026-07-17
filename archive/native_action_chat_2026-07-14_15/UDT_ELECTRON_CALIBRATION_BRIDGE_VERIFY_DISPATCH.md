# Workstation dispatch — cold audit of the UDT electron-calibration bridge

## Scope

Audit whether the current scale-neutral WR-L/conformal branch supplies any normalized charge that an
observed electron mass could calibrate, and whether the boundary/topological sector can close the
gap without an arbitrary coefficient.

Read:

1. UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md
2. UDT_ELECTRON_CALIBRATION_BRIDGE_MAP.md
3. UDT_ELECTRON_CALIBRATION_BRIDGE_DERIVATION_RESULTS.md
4. verify_udt_electron_calibration_bridge.py
5. verify_udt_electron_calibration_bridge_out.txt

For exact conventions and provenance only:

- UDT_RECIPROCAL_C_CONFORMAL_ACTION_DERIVATION_RESULTS.md
- UDT_CSN_GLOBAL_SCALE_SELECTION_DERIVATION_RESULTS.md
- UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md
- UDT_COMMON_SCALE_MATTER_EMERGENCE_DERIVATION_RESULTS.md

Do not load an electron mass value, lepton wall number, target \(X\), or particle count. Do not alter
LIVE.md or CANON.md, adopt \(S^2\), fit a boundary coefficient, or start F/G.

## 1. Full bulk variation

Independently derive the full covariant first variation and presymplectic boundary term of

\[
S_C=\alpha_C\int\sqrt{-g}\,C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}\,d^4x.
\]

Evaluate them on WR-L. Determine whether conformal flatness makes the covariant bulk
time-translation charge vanish, or whether the reciprocal reduction omitted a nonzero full-tensor
term. Treat the seat, causal wall, and domain carefully.

## 2. Reduced higher-derivative check

For

\[
L_C=\gamma W^2/r^2,
\qquad
W=r^2A''-2rA'+2(A-1),
\]

verify

\[
P_1=2\gamma W,
\qquad
P_0=-4\gamma W/r-2\gamma W',
\]

and their WR-L values. Check all signs and endpoint assumptions.

## 3. Boundary/topological census

Re-derive

\[
r^2E_4=\frac{d}{dr}[4(A-1)A']
\]

and the conditional WR-L value

\[
[4(A-1)A']_0^X=4/X.
\]

Then classify all CSN-compatible local boundary/topological terms at the same derivative order that
can affect the finite-cell generator. Determine whether:

1. differentiability plus a declared boundary variation class fixes their coefficients;
2. topology quantizes any coefficient or only the integrated invariant;
3. a horizon completion cancels or changes the \(4/X\) term;
4. reference subtraction fixes an additive ambiguity but not multiplicative normalization.

Do not use a familiar gravitational boundary term without deriving its applicability to this action
and boundary ontology.

## 4. Carrier one-mass degeneracy

Independently verify for

\[
E(R)=aR+b/R
\]

that \(E_*=m_ec^2\) fixes \(ab\) but not \(b/a\). Challenge whether CSN, topology, the certified
dimensionless carrier shape, or the global bootstrap already supplies the missing ratio. Keep the
carrier identity reopened.

## 5. Minimal dimensionless closure

Audit the proposed required outputs

\[
\mu_*=\frac{GM_{\rm total}}{c^2X},
\qquad
\beta_e=\frac{Gm_e}{c^2X},
\qquad
\sigma_e=\frac{R_e}{X}.
\]

Verify:

\[
X=\frac{Gm_e}{c^2\beta_e},
\qquad
\frac{M_{\rm total}}{m_e}=\frac{\mu_*}{\beta_e},
\qquad
R_e=\sigma_eX.
\]

State whether fewer dimensionless outputs suffice and identify every needed normalization. Do not
interpret \(M_{\rm total}/m_e\) as a particle count.

## 6. Numerical readiness

Determine whether any existing script/functional can compute a native \(\beta_e\), rather than a
dimensionless energy in a chosen conditional carrier model. If not, identify the exact analytic
object that must be fixed before GPU work.

## 7. Required verdict

Return:

1. PASS/FAIL for sections 1–6;
2. corrected equations and raw scripts/output;
3. one bulk-charge verdict:
   - **WR-L CONFORMAL BULK CHARGE-SILENT**;
   - **NONZERO COVARIANT BULK CHARGE FOUND**;
   - **BOUNDARY CONDITIONS PREVENT A VERDICT**;
4. one boundary verdict:
   - **DISTINGUISHED \(1/X\) GENERATOR DERIVED**;
   - **RIGHT SCALING, NORMALIZATION OPEN**;
   - **EULER LEAD CANCELS OR IS INAPPLICABLE**;
5. one calibration verdict:
   - **ONE \(m_e\) INPUT CLOSES THE REMAINING SCALE**;
   - **ONE \(m_e\) INPUT FIXES ONLY ONE COMBINATION**;
   - **CURRENT CARRIER CANNOT BE USED**;
6. the smallest next analytic derivation.

Stop after reporting. No canon/frontier update without Charles's verdict.

