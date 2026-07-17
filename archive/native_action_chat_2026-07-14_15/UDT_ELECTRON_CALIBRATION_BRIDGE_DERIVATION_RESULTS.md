# UDT electron-mass calibration bridge — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | grok at 64af120; pre-existing dirty work preserved |
| Mode | Analytic DERIVE + exact dependency-free audit; DATA-BLIND |
| MAP frozen first | UDT_ELECTRON_CALIBRATION_BRIDGE_MAP.md, SHA-256 21272e9d3f71fd7ba8cb1253ca985db7b629fa6f1b96c16676b23debd3de3ac7 |
| Exact verifier | verify_udt_electron_calibration_bridge.py — 26/26 checks pass |
| Electron mass | No value loaded; allowed only as a future CHOSE calibration |
| GPU | Not used; no determined nonlinear problem emerged |
| Independent verification | OPEN |
| Build-on grade | PROVISIONAL ANALYTIC RESULT; not banked and not canon |

## 0. Result

\[
\boxed{
\begin{gathered}
\text{The scale-neutral conformal bulk assigns WR-L no nonzero calibratable bulk charge.}\\
\text{An allowed boundary/topological sector has the needed inverse-}X\text{ scaling,}\\
\text{but its coefficient and physical mass normalization are not yet derived.}\\
\text{One observed particle mass fixes one carrier coefficient combination, not the carrier size.}
\end{gathered}}
\]

Therefore accepting \(m_e\) can eventually calibrate UDT, but it cannot yet choose the missing
boundary term, carrier, or action coefficients. The exact target that would make it useful is a
dimensionless full-system output

\[
\boxed{\beta_e=\frac{Gm_e}{c^2X}.}
\]

Once \(\beta_e\) and the normalization called \(G\) are native outputs, observed \(m_e\) fixes the
absolute representative:

\[
\boxed{X=\frac{Gm_e}{c^2\beta_e}.}
\]

## 1. The conformal WR-L bulk is charge-silent

For the reciprocal static metric, define

\[
W[A]=r^2A''-2rA'+2(A-1).
\]

After the angular and time factors are suppressed, the conditional conformal action has radial
density

\[
L_C=\gamma\,\frac{W^2}{r^2},
\]

where \(\gamma\) contains the overall action normalization and fixed integration factors.

Because this is a second-derivative Lagrangian, its exact radial first variation has boundary form

\[
\delta S_C\big|_{\partial}
=\left[P_0\,\delta A+P_1\,\delta A'\right]_{\partial},
\]

with

\[
P_1=\frac{\partial L_C}{\partial A''}=2\gamma W,
\]

\[
P_0=\frac{\partial L_C}{\partial A'}
-\frac{d}{dr}\frac{\partial L_C}{\partial A''}
=-\frac{4\gamma W}{r}-2\gamma W'.
\]

For WR-L,

\[
A=1-\frac rX,\qquad A'=-\frac1X,\qquad A''=0,
\]

so

\[
W=0,\qquad W'=0.
\]

Consequently,

\[
\boxed{
L_C[\mathrm{WR\!-\!L}]=0,\qquad
P_0[\mathrm{WR\!-\!L}]=P_1[\mathrm{WR\!-\!L}]=0.
}
\]

This is stronger than the already-known statement \(C^2=0\): the reduced bulk first variation and
both higher-derivative radial boundary momenta vanish as well. The full covariant reason is the same:
the first variation of a \(C^2\) action is proportional to \(C\) and its derivatives, all of which
vanish on a conformally flat WR-L representative.

Status:

- **DERIVED conditionally:** the minimal conformal bulk does not supply a nonzero WR-L mass
  normalization.
- **NOT CLAIMED:** every possible full-theory charge is zero. An independently derived boundary,
  topological, or matter sector may carry one.

## 2. The boundary channel has the right scaling but an arbitrary coefficient

The four-dimensional Euler density, allowed alongside \(C^2\) without changing the local Bach
equation, reduces in the reciprocal static branch to

\[
r^2E_4
=\frac{d}{dr}\left[4(A-1)A'\right].
\]

On WR-L,

\[
4(A-1)A'=\frac{4r}{X^2}.
\]

Across the conditional interval \(0\le r\le X\),

\[
\boxed{
\left[4(A-1)A'\right]_0^X=\frac4X.
}
\]

Thus an allowed term with coefficient \(\theta_E\) contributes an on-shell boundary quantity
proportional to

\[
\frac{\theta_E}{X}.
\]

This is a real structural lead: it has inverse-length scaling and could participate in an eventual
energy/mass calibration. It is not yet a mass formula, because:

1. \(\theta_E\) is not selected by the Bach bulk equation;
2. the correct finite-cell/horizon Euler boundary completion is not derived;
3. the time-translation generator and reference subtraction are not fixed;
4. the action-to-physical-mass normalization, including the quantity identified as \(G\), is open.

Indeed, changing \(\theta_E\) leaves the local bulk equation and WR-L solution unchanged while
changing the boundary value by \(4\Delta\theta_E/X\). Therefore

\[
\boxed{
\text{the local conformal bulk cannot uniquely determine }\beta_e
\text{ without a distinguished boundary principle.}
}
\]

Using the observed electron mass to fit \(\theta_E\) would be a fudge factor, not a UDT derivation.

## 3. What one observed mass fixes in the carrier probe

Write the exact scale energy as

\[
E(R)=aR+\frac bR,
\qquad
a=C_2\xi>0,\quad b=C_4\kappa_4>0.
\]

Stationarity gives

\[
R_*^2=\frac ba,
\qquad
E_*=2\sqrt{ab},
\qquad
E_2=E_4.
\]

If the conditional \(Q_H=1\) object were independently identified as the electron and one accepted

\[
E_*=m_ec^2,
\]

then only

\[
\boxed{ab=\frac{m_e^2c^4}{4}}
\]

would be fixed. For every positive radius \(R_*\),

\[
\boxed{
a=\frac{m_ec^2}{2R_*},
\qquad
b=\frac{m_ec^2R_*}{2}
}
\]

has the same stationary mass. The ratio

\[
\frac ba=R_*^2
\]

remains free.

Therefore one mass input:

- **CAN** calibrate one overall carrier-energy combination after the carrier and action are derived;
- **CANNOT** determine the particle radius or both \(L_2,L_4\) coefficients;
- **CANNOT** establish that the reopened \(S^2,Q_H=1\) carrier is the electron;
- **CANNOT** supply its coupling to the universal boundary charge.

The certified numerical energy near \(274.958\) is dimensionless/model-normalized evidence about a
chosen carrier functional. Equating it to \(m_ec^2\) now would calibrate that choice, not derive the
choice.

## 4. The minimal bridge that would make \(m_e\) decisive

A complete dimensionless UDT solve must output both a global compactness

\[
\mu_*=\frac{GM_{\rm total}}{c^2X}
\]

and a localized electron-sector compactness

\[
\beta_e=\frac{Gm_e}{c^2X}.
\]

Then accepting \(m_e\) gives

\[
X=\frac{Gm_e}{c^2\beta_e},
\]

and the total universal mass follows as the dimensionless prediction

\[
\boxed{
\frac{M_{\rm total}}{m_e}
=\frac{\mu_*}{\beta_e}.
}
\]

This ratio is not a particle count. It is a mass ratio; interpreting it as a count would require a
derived composition and recycling ledger.

If the solve also outputs a dimensionless particle size

\[
\sigma_e=\frac{R_e}{X},
\]

then

\[
R_e=\sigma_e X
\]

and the carrier coefficient ratio is fixed rather than fitted.

The minimal useful output packet is therefore

\[
\boxed{
(\mu_*,\beta_e,\sigma_e)
\quad\text{from one full metric–boundary–matter solution.}
}
\]

Only \(\beta_e\) is required to calibrate \(X\) from \(m_e\); \(\sigma_e\) is required to fix the
particle length/coupling ratio, and \(\mu_*\) connects the calibration to the global mass ledger.

## 5. Why topology alone does not complete the bridge

The Hopf label

\[
Q_H=1
\]

is dimensionless. It can select a topological sector and protect a configuration from smooth
unwinding in a determined functional. It cannot provide a meter, energy normalization, or
gravitational charge by itself.

Accordingly,

\[
\boxed{
Q_H=1\quad\not\Longrightarrow\quad
\text{electron},\ m_e,\ R_e,\ \beta_e,\ \text{or }M_{\rm total}/m_e.
}
\]

Those identifications require additional derived structure, not nomenclature.

## 6. The narrowed analytic path

The path that can make the electron mass useful is now:

1. **Boundary action:** derive the distinguished CSN-compatible finite-cell/horizon boundary
   functional and variation class. The Euler \(1/X\) result is a target for this audit, not a chosen
   term.
2. **Charge normalization:** derive its time-translation/global generator and the normalization
   identified observationally as \(G\).
3. **Matter-scale completion:** derive or replace the carrier and obtain a legitimate post-scale
   finite-size branch; do not assume \(S^2\).
4. **Full dimensionless solve:** compute \(\mu_*,\beta_e,\sigma_e\) from the same coupled solution.
5. **Single calibration:** only then insert observed \(m_e\) and predict \(X\), \(R_e\), and
   \(M_{\rm total}/m_e\).

Steps 1–3 are analytic. GPU numerics begin only at step 4.

## 7. Status ledger

| Claim | Status |
|---|---|
| \(C^2\) bulk density vanishes on WR-L | **DERIVED conditionally** |
| Reduced \(C^2\) boundary momenta vanish on WR-L | **DERIVED conditionally, exact** |
| Euler reciprocal primitive gives \(4/X\) across \(0\le r\le X\) | **DERIVED conditional geometry** |
| Euler coefficient/boundary completion is native | **OPEN** |
| Conformal bulk alone uniquely normalizes WR-L mass | **EXCLUDED in the tested branch** |
| \(m_e\) fixes \(ab\) for a derived \(L_2+L_4\) electron | **CONDITIONAL-DERIVED** |
| \(m_e\) alone fixes carrier radius or coefficient ratio | **FALSE** |
| \(Q_H=1\) identifies the electron | **NOT DERIVED** |
| Derived \(\beta_e\) plus calibrated \(m_e,G,c\) fixes \(X\) | **DERIVED algebra** |
| Current theory supplies \(\beta_e\) | **OPEN** |
| GPU numerics are ready | **NO** |

## 8. Frontier

\[
\boxed{
\begin{gathered}
\text{Electron mass can be a final one-number calibration.}\\
\text{The current WR-L conformal bulk cannot provide its bridge.}\\
\text{The boundary sector exposes the right }1/X\text{ scaling but not its coefficient.}\\
\text{Next derivation: distinguished finite-cell boundary action and normalized charge.}
\end{gathered}}
\]

## 9. Verification scope

The dependency-free script checks 26 exact statements: the full WR-L conformal bracket, reduced
higher-derivative boundary momenta, Euler boundary primitive, two distinct stationary carrier radii
with identical mass, coefficient product/ratio, \(\beta_e\) dimensions and inversion, the global
mass-ratio identity, and the dimensionlessness of topology. It does not derive the boundary
coefficient, carrier, \(G\), \(\beta_e\), or any observational number.

