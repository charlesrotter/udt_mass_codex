# UDT CSN one-mass global calibration theorem — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | grok at 64af120; pre-existing dirty work preserved |
| Mode | Analytic DERIVE + dependency-free exact audit; DATA-BLIND |
| MAP frozen first | UDT_CSN_ONE_MASS_GLOBAL_CALIBRATION_MAP.md, SHA-256 08f47a0bb8dcbe1dbf9989f88e94bb3cf7d9a3621c58db098cd9d582ebfad86d |
| Exact verifier | verify_udt_csn_one_mass_global_calibration.py — 24/24 checks pass |
| Observational inputs | No numerical value loaded |
| GPU | Not used; dimensionless continuum problem remains open |
| Independent verification | OPEN |
| Build-on grade | PROVISIONAL ANALYTIC THEOREM; not banked and not canon |

## 0. Result

For any complete static Common-Scale-Neutral cell whose full action has one overall action
normalization \(\mathcal A\), every native energy and mass must have the form

\[
\boxed{
E_i=\frac{\mathcal A c}{X}\,\varepsilon_i,
\qquad
m_i=\frac{\mathcal A}{cX}\,\varepsilon_i,
}
\]

where \(\varepsilon_i\) is a dimensionless output of the full metric–matter–global solution.

Therefore:

1. one observed mass alone fixes \(\mathcal A/X\), not \(\mathcal A\) and \(X\) separately;
2. a normalized \(G\)-bridge supplies the second relation;
3. if the dimensionless theory derives that bridge and an electron branch, observed \(m_e\) fixes
   \(X\) and \(\mathcal A\) exactly;
4. all mass ratios are then predictions independent of the calibration.

The exact bridge is

\[
\boxed{
\widehat g=\frac{G\mathcal A}{c^3X^2},
\qquad
\beta_i=\frac{Gm_i}{c^2X}
=\widehat g\,\varepsilon_i.
}
\]

If \(\widehat g\) and \(\varepsilon_e\) are native dimensionless outputs, then

\[
\boxed{
X=\frac{Gm_e}{c^2\widehat g\,\varepsilon_e},
\qquad
\mathcal A=\frac{Gm_e^2}{c\,\widehat g\,\varepsilon_e^2}.
}
\]

This is the sought one-mass calibration route. Its algebra is complete; the dimensionless UDT
solution that must supply \(\widehat g\) and \(\varepsilon_e\) is still OPEN.

## 1. Static action scaling

Use dimensionless coordinates on the complete cell:

\[
y^\mu=\frac{x^\mu}{X},
\qquad
y^0=\tau=\frac{ct}{X}.
\]

For a CSN-invariant action built from dimensionless four-dimensional invariants, write

\[
S=\mathcal A\,\widehat S,
\]

where \(\mathcal A\) has dimensions of action and \(\widehat S\) is dimensionless.

For a static solution over

\[
\Delta\tau=\frac{c\Delta t}{X},
\]

the on-shell action has the exact form

\[
S_{\rm on}
=\mathcal A\,\Delta\tau\,\ell
=\mathcal A\,\frac{c\Delta t}{X}\,\ell.
\]

Define the positive dimensionless energy readout by

\[
\varepsilon=-\ell
\]

with the final sign to be verified by the eventual Hamiltonian convention. Then

\[
E=-\frac{\partial S_{\rm on}}{\partial\Delta t}
=\frac{\mathcal A c}{X}\varepsilon,
\]

and

\[
\boxed{
m=\frac{E}{c^2}
=\frac{\mathcal A}{cX}\varepsilon.
}
\]

No quantum action constant is imported. \(\mathcal A\) is simply the overall classical action
normalization required before an action value can be read as physical energy.

## 2. What enters the dimensionless equations

For a future full action

\[
S=\mathcal A\left[
I_0[g,\Psi]
+\sum_a\lambda_a I_a[g,\Psi]
+I_\partial[g,\Psi]
\right],
\]

the Euler equations are

\[
\delta I_0+\sum_a\lambda_a\delta I_a+\delta I_\partial=0.
\]

The overall \(\mathcal A\) cancels. The dimensionless relative coefficients \(\lambda_a\) do not.

Consequently:

- observed \(m_e\) may calibrate the final overall normalization;
- it may not choose the carrier invariant basis or the \(\lambda_a\);
- multiplying the complete action by a constant cannot repair an incorrect dimensionless solution;
- mass-ratio predictions require every compared charge to share the same native normalization.

This preserves the no-fitting rule.

## 3. Why one mass alone still leaves one scale orbit

Suppose the dimensionless theory supplies \(\varepsilon_e\). Then

\[
m_e=\frac{\mathcal A}{cX}\varepsilon_e
\]

fixes only

\[
\frac{\mathcal A}{X}=\frac{m_ec}{\varepsilon_e}.
\]

Indeed,

\[
\mathcal A\mapsto\lambda\mathcal A,
\qquad
X\mapsto\lambda X
\]

leaves every mass unchanged while scaling every physical length by \(\lambda\).

\[
\boxed{
m_e\text{ alone calibrates the mass unit but not the absolute length unit.}
}
\]

This is the exact one-equation/two-unknowns obstruction anticipated in the discussion.

## 4. The normalized \(G\)-bridge closes the orbit

The unique dimensionless combination of \(G,\mathcal A,c,X\) is

\[
\boxed{
\widehat g=\frac{G\mathcal A}{c^3X^2}.
}
\]

For any charge \(m_i=\mathcal A\varepsilon_i/(cX)\),

\[
\frac{Gm_i}{c^2X}
=\frac{G\mathcal A}{c^3X^2}\varepsilon_i
=\widehat g\varepsilon_i.
\]

Thus

\[
\boxed{\beta_i=\widehat g\varepsilon_i.}
\]

For the accepted electron calibration,

\[
\beta_e=\widehat g\varepsilon_e,
\]

and the inversion in the result follows.

The provenance of \(\widehat g\) must be explicit:

- **DERIVED possibility:** a complete native charge/response definition fixes it;
- **CALIBRATION possibility:** an observed \(G\), together with a declared charge normalization,
  fixes it after the dimensionless functional is derived;
- **NOT ALLOWED:** silently choosing \(\widehat g=1\);
- **CURRENT STATUS:** OPEN because the native boundary/global charge and \(G\) normalization are not
  yet fixed.

The theorem says exactly what \(G\) must accomplish. It does not derive \(G\).

## 5. Predictions after one-mass calibration

Let the complete dimensionless solution supply:

\[
\varepsilon_e,\qquad
\varepsilon_U,\qquad
\sigma_e=\frac{R_e}{X},\qquad
\widehat g.
\]

Then

\[
R_e=\sigma_eX,
\]

\[
\beta_e=\widehat g\varepsilon_e,
\qquad
\mu_U=\widehat g\varepsilon_U,
\]

and

\[
\boxed{
\frac{M_{\rm total}}{m_e}
=\frac{\varepsilon_U}{\varepsilon_e}
=\frac{\mu_U}{\beta_e}.
}
\]

The overall action normalization, \(X\), \(c\), and \(G\) cancel from the mass ratio. This is the
sector-predictive content: one accepted mass can calibrate absolute units while leaving dimensionless
ratios as genuine outputs.

The ratio \(M_{\rm total}/m_e\) is not automatically a particle count. Composition, other matter
sectors, horizon storage, and recycling require their own derived ledger.

## 6. CSN does not forbid a finite dimensionless particle size

For a localized branch in a complete cell, the most general CSN scaling is

\[
\boxed{
E(R;X)
=\frac{\mathcal A c}{X}
\varepsilon\!\left(\sigma\right),
\qquad
\sigma=\frac RX.
}
\]

The stationary-size equation is purely dimensionless:

\[
\frac{\partial E}{\partial R}
=\frac{\mathcal A c}{X^2}\varepsilon'(\sigma)=0
\quad\Longleftrightarrow\quad
\boxed{\varepsilon'(\sigma_*)=0.}
\]

Stability requires

\[
\varepsilon''(\sigma_*)>0.
\]

Therefore CSN forbids an unexplained absolute radius in the pre-scale equations; it does not forbid a
finite ratio \(R/X\).

This opens a logically clean possibility:

\[
\boxed{
\text{global geometry/topology may select a finite }\sigma_e
\text{ without a primitive local length.}
}
\]

It is an allowed route, not a derived matter solution.

### Scoped contrast: flat quartic-only carrier

For the historical \(L_4\) probe on unbounded flat space,

\[
\varepsilon_4(\sigma)=\frac{k_4}{\sigma},
\qquad
\varepsilon_4'(\sigma)=-\frac{k_4}{\sigma^2}\ne0.
\]

That scoped model still has no finite stationary size. A complete-cell geometry, topology,
interface, or additional CSN invariant would have to change the dimensionless function
\(\varepsilon(\sigma)\). No such term is inserted here.

Accordingly, the theorem does not prove that the historical \(L_2\) term is unnecessary. It proves
only that global dimensionless stabilization is a separate admissible route worth testing before
postulating a local scale-breaking term.

## 7. What the dimensionless solve must contain

Before any GPU run, UDT still must fix:

1. **complete fields:** metric-only, emergent matter, reopened \(S^2\), or replacement;
2. **dimensionless invariant basis:** including every relative coefficient \(\lambda_a\);
3. **complete domain:** not merely the one-sided WR-L static patch;
4. **boundary/interface action and variation class;**
5. **native charge and \(G\) normalization, hence \(\widehat g\);**
6. **electron-branch identification rule** that does not use \(m_e\) or a target number;
7. **criticality and stability gates** for a finite \(\sigma_e\).

Once these are fixed, the numerical solve is entirely dimensionless and data-blind. It should output

\[
(\varepsilon_e,\varepsilon_U,\sigma_e,\widehat g)
\]

before the observed electron mass is inserted.

## 8. Status ledger

| Claim | Status |
|---|---|
| \(E_i=\mathcal A c\,\varepsilon_i/X\) for a static CSN cell | **DERIVED under complete-cell/action assumptions** |
| \(m_i=\mathcal A\varepsilon_i/(cX)\) | **DERIVED** |
| One mass fixes \(\mathcal A/X\) | **DERIVED** |
| One mass alone fixes \(X\) | **FALSE** |
| \(\widehat g=G\mathcal A/(c^3X^2)\) is dimensionless | **DERIVED** |
| \(\beta_i=\widehat g\varepsilon_i\) | **DERIVED** |
| Derived \(\widehat g,\varepsilon_e\) plus observed \(m_e,G,c\) fix \(X,\mathcal A\) | **DERIVED conditional inversion** |
| Native theory currently fixes \(\widehat g\) | **OPEN** |
| Mass ratios equal dimensionless energy ratios | **DERIVED for common native normalization** |
| CSN permits a finite dimensionless radius \(\sigma\) | **DERIVED compatibility** |
| A finite stable electron branch exists | **OPEN** |
| Flat quartic-only carrier has finite stationary size | **NO, scoped result unchanged** |
| GPU solve ready | **NO** |

## 9. Frontier

\[
\boxed{
\begin{gathered}
\text{One accepted mass can be a clean final calibration, not a fitted mechanism.}\\
\text{It fixes the absolute UDT scale iff the dimensionless solve also fixes }\widehat g\varepsilon_e.\\
\text{Mass and size ratios can remain predictions.}\\
\text{Complete CSN matter/global action and electron branch = OPEN.}
\end{gathered}}
\]

## 10. Verification scope

The dependency-free script checks 24 exact statements: action/energy/mass scaling, the one-mass
scale degeneracy, \(\widehat g\) and \(\beta\), the two-input inversion, dimensions, mass ratios,
finite-\(\sigma\) compatibility, the flat quartic-only derivative, and overall-versus-relative action
normalization. It does not derive the complete action, carrier, electron branch, \(G\), \(\widehat g\),
or any numerical value.

