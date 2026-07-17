# UDT CSN dimensionless action and reference-particle branch — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | grok at 64af120; pre-existing dirty work preserved |
| Mode | Analytic DERIVE + dependency-free exact audit; DATA-BLIND |
| MAP frozen first | UDT_CSN_DIMENSIONLESS_ACTION_REFERENCE_BRANCH_MAP.md, SHA-256 83f713e3751b26ce4f5377b0e95a4921a8b8856016964c24c2db26fc31dfac65 |
| Exact verifier | verify_udt_csn_dimensionless_action_reference_branch.py — 22/22 checks pass |
| Carrier status | \(S^2\) remains a reopened conditional probe |
| GPU | Not used; action and branch remain underdetermined |
| Independent verification | OPEN |
| Build-on grade | PROVISIONAL ANALYTIC RESULT; not banked and not canon |

## 0. Result

\[
\boxed{
\begin{gathered}
\text{A classical CSN solve can determine a dimensionless geometric charge-to-energy response}\\
\widehat g=\beta/\varepsilon
\text{ without determining the overall action normalization.}\\
\text{But CSN + static positivity do not uniquely select the historical }S^2\ L_4\text{ action.}\\
F^2\text{ is unique only after an additional rank-one-zero/area-only premise.}
\end{gathered}}
\]

A data-blind reference-particle branch can be defined as the lightest stable nontrivial branch of a
complete theory. Its observed mass may calibrate the theory. Calling that branch the electron remains
an empirical identification, not a derivation from mass alone.

The current corrected \(Q_H=1\) carrier is a strong conditional reference-branch candidate, but it
does not yet provide the native tuple

\[
(\varepsilon_\star,\sigma_\star,\beta_\star)
\]

needed by the one-mass calibration theorem.

## 1. What the dimensionless classical equations can determine

Write a complete CSN action as

\[
S=\mathcal A\left[
I_g[g]
+\sum_a\lambda_a I_a[g,\Psi]
+I_\partial[g,\Psi]
\right].
\]

Its field equations have the schematic form

\[
\mathcal E_g+\sum_a\lambda_a\mathcal E_a+\mathcal E_\partial=0.
\]

The overall action normalization \(\mathcal A\) cancels, while every relative dimensionless
coefficient \(\lambda_a\) remains.

Suppose a complete dimensionless solution produces:

- a normalized geometric charge readout \(q_i\);
- a dimensionless action/Hamiltonian energy \(\varepsilon_i\).

If the native charge theorem identifies

\[
q_i=\beta_i=\frac{Gm_i}{c^2X},
\]

then

\[
\boxed{
\widehat g=\frac{\beta_i}{\varepsilon_i}
=\frac{q_i}{\varepsilon_i}.
}
\]

This ratio is independent of \(\mathcal A\). It can therefore be a classical dimensionless response
of the coupled equations.

The essential caveat is the word normalized. The preceding boundary audit showed that the present
WR-L conformal branch does not yet possess a distinguished charge generator. Until \(q_i\) is
defined by the complete action and boundary/interface law, \(q_i/\varepsilon_i\) is not native.

Thus:

- **DERIVED:** overall action normalization does not prevent a dimensionless response prediction;
- **OPEN:** the action, relative couplings, and normalized charge needed to compute it.

## 2. Minimal quartic census for the historical \(S^2\) probe

For a dimensionless map

\[
\mathbf n:\mathcal M\to S^2,
\]

define the derivative Gram tensor

\[
M_{\mu\nu}
=\partial_\mu\mathbf n\cdot\partial_\nu\mathbf n.
\]

Two independent first-derivative/four-derivative scalars are

\[
Q_1=(\operatorname{tr}M)^2,
\qquad
Q_2=\operatorname{tr}(M^2).
\]

Both have Weyl weight \(-4\); with \(\sqrt{-g}\) they define CSN-invariant four-dimensional action
densities. CSN therefore permits at least the family

\[
\boxed{
I_{4}[a,b]
=\int d^4x\sqrt{-g}\,
\left(aQ_1+bQ_2\right).
}
\]

This family is a census, not an adoption of \(S^2\).

For the pullback area two-form

\[
F_{\mu\nu}
=\mathbf n\cdot
\left(\partial_\mu\mathbf n\times\partial_\nu\mathbf n\right),
\]

the tangent vectors lie in the two-dimensional tangent plane of \(S^2\). On a static positive
spatial slice, the Gram determinant identity gives

\[
\boxed{
F_{ij}F_{ij}
=(\operatorname{tr}M)^2-\operatorname{tr}(M^2)
=Q_1-Q_2.
}
\]

Thus the historical quartic carrier is the coefficient ray

\[
(a,b)\propto(1,-1).
\]

CSN permits that ray but does not select it.

## 3. Exact static positivity cone

Because an \(S^2\) derivative Gram matrix has rank at most two, write its nonzero spatial eigenvalues
as

\[
x,y\ge0.
\]

Then

\[
Q_1=(x+y)^2,
\qquad
Q_2=x^2+y^2,
\]

and

\[
\rho_4=a(x+y)^2+b(x^2+y^2).
\]

Necessity follows from:

- \(y=0\): \(a+b\ge0\);
- \(x=y\): \(2a+b\ge0\).

These conditions are also sufficient:

- if \(a\ge0\), then
  \[
  \rho_4=(a+b)(x^2+y^2)+2axy\ge0;
  \]
- if \(a<0\), the two inequalities imply \(b>0\), and with
  \(s=x+y,\ d=x-y\),
  \[
  \rho_4
  =\left(a+\frac b2\right)s^2+\frac b2d^2\ge0.
  \]

Therefore

\[
\boxed{
\rho_4\ge0\ \text{for every static spatial derivative configuration}
\quad\Longleftrightarrow\quad
a+b\ge0,\qquad 2a+b\ge0.
}
\]

This is a two-dimensional cone, not a unique ray. It contains, for example,

\[
Q_1,\qquad Q_2,\qquad Q_1-Q_2.
\]

\[
\boxed{\text{Static positivity does not derive the historical }F^2\text{ carrier.}}
\]

This positivity result does not prove Lorentzian hyperbolicity, absence of ghosts, or dynamical
stability. Those require the full time-live action.

## 4. The exact premise that would select \(F^2\)

Impose the additional condition:

> Every rank-one derivative configuration has zero quartic cost.

For rank one, \(y=0\), so

\[
\rho_4=(a+b)x^2.
\]

Vanishing for every \(x\) forces

\[
a+b=0.
\]

Nonnegative, nontrivial energy then requires

\[
a>0,\qquad b=-a,
\]

and hence

\[
\boxed{\rho_4=a(Q_1-Q_2)=aF_{ij}F_{ij}.}
\]

Thus:

\[
\boxed{
\text{CSN + static positivity + rank-one-zero}
\Longrightarrow
F^2\text{ uniquely up to positive normalization.}
}
\]

The rank-one-zero statement has a clear lay interpretation: one-directional stretching carries no
matter cost; only oriented area distortion does. It would connect the carrier directly to a
two-form/area notion.

However:

- it is not implied by CSN;
- it is not implied by positivity;
- it is not presently recorded as a UDT founding principle;
- it does not derive the target \(S^2\) itself.

Its status is therefore **CHOSE candidate premise**, not DERIVED.

## 5. Relative matter–geometry coupling remains open

Even if the area-only premise selected \(F^2\), the smallest conditional action would still contain
a relative dimensionless coupling:

\[
S=\mathcal A\left[
I_C[g]+\lambda_4 I_{F^2}[g,\mathbf n]+I_\partial
\right].
\]

The overall \(\mathcal A\) cancels, but \(\lambda_4\) controls the dimensionless backreaction,
solution shape, and charge-to-energy response.

Neither CSN, positivity, nor rank-one-zero fixes \(\lambda_4\). A future global-bootstrap theorem
might restrict it by requiring a regular stable matter-bearing root, but using observed masses to
choose it would be fitting.

Consequently the currently missing dimensionless data are not merely numerical:

\[
\boxed{
\text{carrier ontology/invariant ray, relative coupling, complete domain, and normalized charge.}
}
\]

## 6. Data-blind reference branch versus electron identity

Once a complete theory exists, the criterion

\[
\boxed{
\text{lightest stable nontrivial localized branch}
}
\]

is data-blind and mathematically meaningful, provided:

1. the charge/energy ordering is native;
2. all competing sectors are included;
3. criticality and physical stability are certified;
4. the global domain and boundary class are fixed.

Such a branch may be denoted \(\star\) and used as the one-mass calibrator:

\[
m_\star\ \overset{\rm calibration}{=}\ m_e.
\]

This equality is a **CHOSE observational identification**. It becomes falsifiable because all other
dimensionless mass ratios, sizes, responses, and branches must then agree without refitting.

Other possible labels are weaker:

- **unit topology:** meaningful only after topology and carrier are derived;
- **most symmetric:** need not be lightest or unique;
- **historical \(Q_H=1\):** conditional on the reopened \(S^2\) carrier and chosen functional.

Mass calibration alone cannot derive electric charge, spin, statistics, or full electron identity.
Those properties are not imported here.

## 7. What the certified carrier presently supplies

The corrected no-null \(Q_H=1\) solution supplies, within the chosen post-scale \(S^2,L_2+L_4\)
functional:

- a genuinely critical configuration;
- scoped positive static spectrum;
- conditional dimensionless model energy near \(274.958\).

It does not yet supply:

- a cosmic size ratio \(\sigma_\star=R_\star/X\);
- a native geometric compactness \(\beta_\star\);
- a CSN-derived invariant ray or \(\lambda_4\);
- a complete global domain;
- an electron identity.

Therefore

\[
\boxed{
\text{the certified carrier is a CONDITIONAL reference-branch candidate, not yet the calibrator.}
}
\]

No new GPU solve is warranted until the missing continuum objects are fixed.

## 8. Status ledger

| Claim | Status |
|---|---|
| Overall action normalization cancels from classical equations | **DERIVED** |
| Native \(q/\varepsilon\) can determine \(\widehat g\) | **CONDITIONAL-DERIVED on normalized charge** |
| \(Q_1,Q_2\) are independent CSN quartic invariants | **DERIVED in \(S^2\) probe** |
| \(F_{ij}F_{ij}=Q_1-Q_2\) | **DERIVED, exact static identity** |
| Positivity cone \(a+b\ge0,\ 2a+b\ge0\) | **DERIVED** |
| Positivity uniquely selects \(F^2\) | **FALSE** |
| Rank-one-zero uniquely selects \(F^2\) up to scale | **CONDITIONAL-DERIVED** |
| Rank-one-zero is a current UDT postulate | **NO; CHOSE candidate only** |
| Relative metric–matter coupling \(\lambda_4\) is fixed | **OPEN** |
| Lightest stable branch can be defined data-blindly | **CONDITIONAL-DERIVED once theory is complete** |
| That branch is necessarily the electron | **NOT DERIVED** |
| Existing \(Q_H=1\) carrier provides native calibration tuple | **NO** |

## 9. Frontier

\[
\boxed{
\begin{gathered}
\text{One-mass calibration architecture = DERIVED.}\\
\text{Dimensionless response }q/\varepsilon\text{ can close }\widehat g\text{ once charge is native.}\\
\text{Minimal quartic matter action = ALLOWED POSITIVITY CONE, not unique.}\\
\text{Area-only/rank-one-zero selects historical }F^2\text{ conditionally.}\\
\text{Reference branch can be data-blind; electron identity remains observational.}
\end{gathered}}
\]

## 10. Verification scope

The dependency-free script checks 22 exact statements: overall and relative action normalization,
charge-to-energy ratios, a generic tangent-plane Gram identity, rank-one behavior, positivity-cone
necessity examples and exact nonnegative probes, area-only uniqueness, the surviving relative
matter coupling, and incompleteness of the existing carrier calibration tuple. It does not derive
\(S^2\), rank-one-zero, \(\lambda_4\), a boundary charge, an electron branch, or a numerical value.

