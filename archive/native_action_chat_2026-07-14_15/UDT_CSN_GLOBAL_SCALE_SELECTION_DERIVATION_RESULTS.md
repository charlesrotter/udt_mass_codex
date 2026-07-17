# UDT Common-Scale Neutrality and global scale selection — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | grok at 64af120; pre-existing dirty work preserved |
| Mode | Analytic DERIVE + dependency-free exact audit; DATA-BLIND |
| Foundational input | Owner-locked Common-Scale Neutrality |
| MAP frozen first | UDT_CSN_GLOBAL_SCALE_SELECTION_MAP.md, SHA-256 7c6a5f6799c7ab2fe3612a97bd98f0613fead60ea4482e70a40a08f66074a44a |
| Exact verifier | verify_udt_csn_global_scale_selection.py — 28/28 checks pass |
| GPU | Not used; no determined numerical problem emerged |
| Independent verification | OPEN |
| Build-on grade | PROVISIONAL ANALYTIC RESULT; not banked and not canon |

The live WR-L scope, the reopened carrier status, the conditional EH mass identity, and the
provisional status of the global-bootstrap work are unchanged.

## 0. Result

\[
\boxed{
\begin{gathered}
\text{Under Common-Scale Neutrality, the WR-L parameter }X\text{ is a pre-scale gauge modulus.}\\
\text{The existing wall and bootstrap equations can select shape and compactness, not absolute }X.\\
\text{A normalized dimensionful global datum is still required to make }X\text{ physical.}
\end{gathered}}
\]

This is not a failed search for one more local equation. It is a resolution of why that equation
kept disappearing: a CSN-respecting pre-scale law is not allowed to distinguish members of the
common-scale orbit.

The smallest clean completion is therefore:

\[
\boxed{
\text{dimensionless bootstrap root}
\quad+\quad
\text{native normalized global charge or other scale-setting datum}.
}
\]

The first factor may determine \(GM/(c^2X)\). The second must determine one physical member of the
otherwise gauge-equivalent family.

## 1. Exact WR-L scale orbit

Start from

\[
ds^2=-\left(1-\frac rX\right)c^2dt^2
+ \left(1-\frac rX\right)^{-1}dr^2+r^2d\Omega^2.
\]

Define dimensionless coordinates

\[
\rho=\frac rX,\qquad \tau=\frac{ct}{X}.
\]

Then, without approximation,

\[
\boxed{
ds^2=X^2\,d\hat s^2,
\qquad
d\hat s^2=-(1-\rho)d\tau^2
+(1-\rho)^{-1}d\rho^2+\rho^2d\Omega^2.
}
\]

More formally, if \(F_X(\tau,\rho)=(t=X\tau/c,r=X\rho)\), then

\[
F_X^*g_X=X^2\hat g.
\]

For any \(X_1,X_2>0\),

\[
F_{X_2}^*g_{X_2}
=\left(\frac{X_2}{X_1}\right)^2F_{X_1}^*g_{X_1}.
\]

Therefore, after a diffeomorphic coordinate identification, all positive-\(X\) members are related
by precisely the common conformal factor declared calibrational by CSN:

\[
\boxed{[g_{X_1}]_{\rm CSN}=[g_{X_2}]_{\rm CSN}.}
\]

This statement is **DERIVED from WR-L + owner-locked CSN**. It does not assert that WR-L itself has
been dynamically selected by the native action.

The raw scalar-curvature readout illustrates the distinction:

\[
R=\frac{6}{Xr}=\frac{6}{X^2\rho},
\qquad
X^2R=\frac6\rho.
\]

The dimensionful representative \(R\) changes along the orbit; the dimensionless shape does not.
Before scale setting, comparing raw curvature numbers between representatives is comparing
calibrations, not different UDT geometries.

## 2. What the wall fixes

The WR-L wall condition becomes

\[
A=1-\rho=0\quad\Longleftrightarrow\quad\rho=1.
\]

It selects a dimensionless endpoint. The exact proper radial distance of the conditional static
patch is

\[
\ell_X=X\int_0^1\frac{d\rho}{\sqrt{1-\rho}}=2X,
\]

and its proper volume is

\[
V_X=4\pi X^3\int_0^1\frac{\rho^2\,d\rho}{\sqrt{1-\rho}}
=\frac{64\pi}{15}X^3.
\]

Those quantities scale as \(X\) and \(X^3\); they do not select the representative. Thus

\[
\boxed{
A(X)=0,\quad \ell_X=2X,\quad V_X=\frac{64\pi}{15}X^3
\quad\text{do not determine an absolute }X.
}
\]

A fixed physical value of \(\ell_X\) or \(V_X\) would determine \(X\), but that value would be an
additional dimensionful global datum.

This does not identify the WR-L wall with the canonical odd fold. The prior finite-cell result still
stands: WR-L horizon, odd-fold quotient/interface/boundary, and numerical carrier box are distinct.
Odd/even parity and dimensionless endpoint pins likewise do not supply an absolute length.

## 3. Why the conformal bulk action does not choose \(X\)

Under the previously stated locality, four-dimensionality, parity, derivative-minimality, and
unrestricted-variation premises, CSN conditionally selects the conformal metric action

\[
S_C=\alpha_C\int d^4x\sqrt{-g}\,
C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}.
\]

Its static reciprocal solution family already contains

\[
A=a_0+a_1r+\frac{a_{-1}}r+a_2r^2,
\qquad
a_0^2-3a_1a_{-1}=1,
\]

and WR-L is the branch

\[
a_0=1,\qquad a_1=-\frac1X,\qquad a_{-1}=a_2=0.
\]

No Bach equation fixes \(a_1\), hence none fixes \(X\). That is now seen as required rather than
accidental: fixing it in the pre-scale bulk would distinguish CSN-equivalent representatives.

Status:

- **DERIVED:** CSN forbids an absolute-\(X\) selector in a CSN-invariant pre-scale bulk equation.
- **CONDITIONAL-DERIVED:** the minimal conformal action realizes that requirement and leaves the
  WR-L slope free.
- **OPEN:** whether that conditional action is the complete native UDT action and how its boundary
  functional is selected.

## 4. Exact bootstrap homogeneity

Retain the recorded full-solution response definitions

\[
M_{\rm pred}(\delta)
=\frac{c^2X}{G}\mu(\delta),
\qquad
V(\delta)=X^3\nu(\delta).
\]

Then

\[
\bar\rho
=\frac{c^2}{GX^2}\frac{\mu}{\nu},
\qquad
\delta_U
=\frac{G\bar\rho X^2}{c^2}
=\frac{\mu}{\nu},
\qquad
\chi_U=\frac{GM_{\rm pred}}{c^2X}=\mu.
\]

Thus the bootstrap equation is

\[
\boxed{F_{\rm boot}(\delta)=\mu(\delta)-\nu(\delta)\delta=0.}
\]

There is an important audit distinction:

- after a self-consistent solution is known, \(\delta=\mu/\nu\) is exact bookkeeping;
- it is a nontrivial nonlinear field-selection equation only because the action and boundary
  problem must independently produce the response functions \(\mu(\delta)\) and \(\nu(\delta)\).

At fixed dimensionless branch and fixed \(c,G\) normalization,

\[
X\mapsto\lambda X
\]

gives

\[
\boxed{
M_{\rm pred}\mapsto\lambda M_{\rm pred},\qquad
V\mapsto\lambda^3V,\qquad
\bar\rho\mapsto\lambda^{-2}\bar\rho,\qquad
\delta_U\mapsto\delta_U,\qquad
\chi_U\mapsto\chi_U.
}
\]

Therefore even a unique, narrow, stable bootstrap root can fix only dimensionless compactness and
shape:

\[
\chi_*=\mu_*=\nu_*\delta_*,
\qquad
\alpha_*=\frac1{\chi_*}.
\]

It cannot select a unique \(X\) while the scale orbit is intact.

This sharpens the owner bootstrap principle: under CSN, the physically meaningful narrow
pre-selection window is a window in the dimensionless density \(\delta_U\), not in an unqualified
number of kilograms per cubic meter. A fixed dimensionful density could arise after scale setting;
if imposed before it, it would itself be a hidden scale anchor.

## 5. Conservation is not scale selection

The proposed recycling ledger may require

\[
\frac{dM_{\rm total}}{dt}=0.
\]

That is a conservation law within a selected universe. It does not select the numerical value of
\(M_{\rm total}\). If one solution carries conserved \(M\), the CSN scale orbit above carries
conserved \(\lambda M\).

Three statements must remain separate:

1. **charge existence:** the action has a boundary/Hamiltonian generator;
2. **charge normalization:** that generator is invariantly identified with physical mass;
3. **charge value:** the complete solution selects or is supplied a particular total mass.

The current record has not derived all three. In particular, the finite-cell analysis showed that
boundary primitives can shift endpoint momenta and transversality data without changing bulk
equations. A native charge cannot be read from the wall profile alone.

\[
\boxed{
\text{Mass recycling can preserve the chosen scale ledger; it does not choose the scale ledger.}
}
\]

## 6. What would actually fix \(X\)

Suppose a complete solve produces a unique dimensionless root

\[
\mu_*=\nu_*\delta_*.
\]

Then any one independently fixed, properly normalized dimensionful datum can select a representative.
Examples are:

### 6.1 Fixed total mass

If a native mass charge and its value \(M_0\) are independently fixed,

\[
\boxed{
X=\frac{GM_0}{c^2\mu_*}
=\frac{GM_0}{c^2\nu_*\delta_*}.
}
\]

This is exact. But if \(M_0\) is observational input, the absolute scale is calibrated by that input,
not predicted from the scale-neutral bulk alone. If \(G\) is also to be UDT-emergent, its
normalization remains part of the same closure problem.

### 6.2 Fixed proper volume or boundary size

\[
X=\left(\frac{V_0}{\nu_*}\right)^{1/3},
\]

or, for the conditional WR-L static-patch radial length,

\[
X=\frac{\ell_0}{2}.
\]

Again \(V_0\) or \(\ell_0\) is the anchor.

### 6.3 A genuine scale-setting phase

A new phase could make one common-scale representative physically distinguished through a
dynamically generated dimensionful order parameter or normalized global charge. CSN alone allows
this category but does not derive its field, action, coupling, or nonzero solution. No such object
is introduced here.

### 6.4 What cannot fix \(X\) alone

- \(c\) alone: it converts length and time but cannot construct an absolute length;
- a dimensionless topological number alone;
- \(A(X)=0\) or \(\rho=1\);
- a unique \(\delta_*\), \(\chi_*\), or \(\alpha_*\);
- conservation without charge normalization and value;
- an observed particle mass without an independently derived bridge from that local mass to the
  universal charge/geometry.

## 7. The actual missing object

The missing constraint is not another local deformation-cost term. It is the transition from the
pre-scale conformal geometry to a physical scale representative.

Within the present program, the smallest native route is:

1. derive the finite-cell off-shell action and its distinguished boundary primitive;
2. derive a normalized total charge from that action;
3. solve the dimensionless global bootstrap and matter-stability problem;
4. determine whether the charge value is dynamically selected, topologically fixed together with a
   mass unit, or must remain observational calibration;
5. only then assign a physical \(X\).

This is analytic work first. GPU numerics cannot select a gauge representative or a boundary charge
that the continuum theory has not defined.

## 8. Falsification

The scale-orbit conclusion would be falsified if any of the following is demonstrated:

1. a dimensionless, CSN-invariant observable distinguishes \(g_{X_1}\) from \(g_{X_2}\) before scale
   setting;
2. a native CSN-respecting boundary/action equation fixes \(X\) without any hidden dimensionful
   datum;
3. the full solution cannot be written as a common-scale orbit because an additional derived field
   supplies a nontrivial scale weight and nonzero invariant normalization;
4. Common-Scale Neutrality itself fails its owner-stated falsification test.

An explicit primitive \(X\), fixed density, length, mass, or dimensionful action coefficient would
select a scale, but would not falsify the theorem—it would violate one of its pre-scale premises.

## 9. Status ledger

| Claim | Status |
|---|---|
| WR-L \(g_X=X^2\hat g\) in dimensionless coordinates | **DERIVED, exact** |
| Positive WR-L \(X\)-family is one CSN orbit | **DERIVED from WR-L + locked CSN** |
| WR-L wall fixes \(\rho=1\), not absolute \(X\) | **DERIVED** |
| Minimal conformal bulk leaves WR-L \(X\) free | **CONDITIONAL-DERIVED**, prior action premises retained |
| Bootstrap fixes \(\chi_*,\delta_*,\alpha_*\) if a root exists | **CONDITIONAL-DERIVED** |
| A bootstrap root exists and is unique/narrow | **OPEN** |
| Total-mass conservation selects its numerical value | **NOT DERIVED; false as a general inference** |
| Fixed normalized \(M_0\) plus \(\mu_*\) fixes \(X\) | **DERIVED conditional algebra** |
| Native mass charge, normalization, and selected value | **OPEN** |
| Absolute \(X\) from present premises | **OPEN; not selected pre-scale** |
| Need for GPU numerics now | **NO** |

## 10. Frontier

\[
\boxed{
\begin{gathered}
\text{Common-Scale Neutrality = OWNER-LOCKED FOUNDATIONAL POSTULATE.}\\
\text{WR-L }X\text{ = PRE-SCALE GAUGE MODULUS, DERIVED.}\\
\text{Global bootstrap = POSSIBLE DIMENSIONLESS COMPACTNESS SELECTOR.}\\
\text{Absolute scale = REQUIRES NATIVE NORMALIZED GLOBAL DATUM OR SCALE-SETTING PHASE.}\\
\text{Boundary action, total charge, charge value, carrier, and unique action = OPEN.}
\end{gathered}}
\]

## 11. Verification scope

The dependency-free exact script checks 28 statements: WR-L common-\(X^2\) factorization, wall
invariance, conditional static-patch length and volume coefficients, curvature scale weight,
bootstrap reconstruction, scale-orbit weights, fixed-anchor formulas, and dimensions of \(GM/c^2\).
It does not prove CSN, the conformal action premises, a bootstrap root, a native boundary charge, a
matter window, or a carrier.
