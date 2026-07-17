# Common-Scale Neutrality and matter emergence — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Foundational input | Owner-locked `UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md` |
| Mode | Analytic consequence audit; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Symbolic verifier | `verify_udt_common_scale_matter_emergence.py`: **18/18 checks pass** |
| Carrier discipline | Historical $S^2,L_2+L_4$ used only as a probe; provenance remains OPEN |
| GPU | Not used or needed |

## 0. Result

Locked Common-Scale Neutrality produces a strong ordering principle for matter:

$$
\boxed{
\begin{gathered}
\text{A primitive local mass scale is forbidden in the pre-scale UDT action.}\\
\text{The conditional conformal metric equation accepts only a trace-free pre-scale source.}\\
\text{Four-derivative carrier structure can exist before scale selection, but the historical}\\
\text{two-derivative term and a finite stable particle size require an emerged physical scale.}
\end{gathered}
}
$$

This is not yet a derivation of matter. It is a derived **phase ordering**:

$$
\boxed{
\text{pre-scale geometry}
\longrightarrow
\text{global/boundary scale selection}
\longrightarrow
\text{possible finite-size massive matter}.}
$$

The result is structurally consonant with the owner bootstrap principle that matter exists only in
a narrow range of total cosmic density. It does not derive that window or its width.

## 1. Trace gate from the metric action

Under the minimal conditional metric branch,

$$
S_C=\alpha_C\int\sqrt{-g}\,C^2d^4x,
$$

write the sourced equation without fixing normalization as

$$
\mathcal N_C B_{\mu\nu}=T_{\mu\nu}.
$$

The Bach tensor is trace-free:

$$
g^{\mu\nu}B_{\mu\nu}=0.
$$

Therefore

$$
\boxed{T^\mu{}_\mu=0}
$$

for a source in the unbroken/pre-scale branch.

The same result follows directly from local Common-Scale Neutrality. For an infinitesimal common
rescaling

$$
\delta g_{\mu\nu}=2\sigma(x)g_{\mu\nu},
$$

metric variation of a scale-neutral matter action gives, on its field equations,

$$
0=\delta S_m
=\int\sqrt{-g}\,\sigma T^\mu{}_\mu\,d^4x.
$$

Arbitrary $\sigma(x)$ requires the trace to vanish.

Trace-free does not mean zero energy, a fluid, or zero eventual gravitational mass. It is a
pre-scale source constraint. Once a physical scale is selected, the scale-setting sector and the
material sector must be treated together before any trace or mass is assigned.

## 2. Why primitive mass is excluded

A massive point action contains

$$
S_p=-mc\int ds.
$$

Under

$$
g_{\mu\nu}\mapsto\Omega^2g_{\mu\nu},
$$

one has

$$
ds\mapsto\Omega ds.
$$

A fixed nonzero $m$ therefore violates Common-Scale Neutrality.

Likewise, even if a local scalar-like field is assigned scale weight $-1$, a fixed mass density

$$
\sqrt{-g}\,m^2\psi^2
$$

has residual weight $+2$ in four dimensions. The coefficient $m$ would have to come from a
scale-setting quantity rather than be primitive.

Thus

$$
\boxed{
\begin{gathered}
\text{no fixed primitive rest-mass parameter is allowed before scale selection;}\\
\text{observed rest mass must be relational/emergent.}
\end{gathered}
}
$$

This statement does not supply the mechanism or numerical mass.

## 3. General derivative-weight sieve

For a dimensionless field with $2p$ derivatives contracted by $p$ inverse metrics, the
four-dimensional density has common-scale weight

$$
w=4-2p.
$$

Hence:

| Sector | Weight in 4D | Pre-scale CSN status |
|---|---:|---|
| two derivatives ($p=1$) | $+2$ | forbidden without scale-setting structure |
| four derivatives ($p=2$) | $0$ | allowed by scale weight |
| six derivatives ($p=3$) | $-2$ | requires additional weight/scale structure |

This is only a weight sieve. Covariance, topology, signs, target geometry, field equations, and
stability still have to be derived.

## 4. Historical $S^2$ carrier as an explicit probe

Consider conditionally

$$
S_n=-\int d^4x\sqrt{-g}\left[
\frac\xi2g^{\mu\nu}\partial_\mu\mathbf n\cdot\partial_\nu\mathbf n
+\frac{\kappa_4}{4}F_{\mu\nu}F^{\mu\nu}
\right],
$$

with dimensionless $\mathbf n$.

### Two-derivative sector

The density scales as

$$
\sqrt{-g}\,g^{\mu\nu}\partial_\mu\mathbf n\cdot\partial_\nu\mathbf n
\mapsto
\Omega^2
\sqrt{-g}\,g^{\mu\nu}\partial_\mu\mathbf n\cdot\partial_\nu\mathbf n.
$$

Its stress trace in $D$ dimensions is

$$
T_{(2)}{}^\mu{}_\mu
=\xi\left(1-\frac D2\right)
\partial_\rho\mathbf n\cdot\partial^\rho\mathbf n.
$$

At $D=4$,

$$
T_{(2)}{}^\mu{}_\mu
=-\xi\,\partial_\rho\mathbf n\cdot\partial^\rho\mathbf n\ne0
$$

generically. Thus the historical $L_2$ term is not fundamental in the pre-scale CSN phase.

### Four-derivative sector

The density

$$
\sqrt{-g}\,F_{\mu\nu}F^{\mu\nu}
$$

has weight zero in four dimensions. Its Maxwell-form metric stress has trace

$$
T_{(4)}{}^\mu{}_\mu
=\kappa_4\left(1-\frac D4\right)F_{\rho\sigma}F^{\rho\sigma},
$$

so

$$
\boxed{T_{(4)}{}^\mu{}_\mu=0\quad(D=4).}
$$

The historical $L_4$ term therefore passes the pre-scale CSN weight and trace gates.

## 5. What CSN does not derive about the carrier

Four-derivative scale neutrality is not unique to $F_{\mu\nu}F^{\mu\nu}$. For the derivative Gram
tensor

$$
M_{\mu\nu}=\partial_\mu\mathbf n\cdot\partial_\nu\mathbf n,
$$

both

$$
Q_1=(\operatorname{Tr}M)^2,
\qquad
Q_2=\operatorname{Tr}(M^2)
$$

have the same scale weight and are independent. A rank-one derivative probe gives $Q_1=Q_2$, while
a rank-two unit probe gives $Q_1=4$ and $Q_2=2$.

Therefore

$$
\boxed{
\text{CSN permits a four-derivative carrier class; it does not derive }S^2\text{ or }L_4.
}
$$

The reopened carrier status is unchanged.

## 6. Why stable finite-size matter must be post-scale

For the historical static two-term carrier, exact spatial scaling gives

$$
E(R)=C_2\xi R+\frac{C_4\kappa_4}{R},
\qquad C_2,C_4>0.
$$

The pre-scale-compatible quartic term alone has

$$
E_4(R)=\frac{C_4\kappa_4}{R},
\qquad
\frac{dE_4}{dR}=-\frac{C_4\kappa_4}{R^2}\ne0.
$$

It has no finite stationary radius and tends to delocalize toward larger $R$.

Once a legitimate scale-setting structure allows a positive two-derivative coefficient, the
stationary radius satisfies

$$
R_*^2=\frac{C_4\kappa_4}{C_2\xi},
$$

with

$$
E_2(R_*)=E_4(R_*),
\qquad
E''(R_*)=\frac{2C_4\kappa_4}{R_*^3}>0.
$$

Thus the familiar $L_2+L_4$ balance has a new possible interpretation:

- $L_4$ belongs to a pre-scale shape/topology sector;
- $L_2$ can exist only after physical scale is supplied;
- their balance can then produce finite-size massive matter.

This is a **WORKING EMERGENCE INTERPRETATION**, not yet a derivation of $L_2$, its coefficient, or
the carrier.

## 7. The possible role of $X$

Dimensional consistency would allow a post-scale coefficient of the form

$$
\xi=\frac{\hat\xi}{X^2}
$$

for dimensionless $\hat\xi$. But CSN does not derive this equation. $X$ might instead set a global
gauge, combine with another emerged quantity, or be unrelated to the carrier scale.

The permitted conclusion is only:

$$
\boxed{
X\text{ can emerge globally before matter acquires scale; it need not appear in the pre-scale bulk action.}
}
$$

Computing $X$, $\hat\xi$, particle size, or particle mass requires the still-open bootstrap and
scale-setting dynamics.

## 8. Relationship to the certified carrier

The corrected $Q_H=1$ carrier and its scoped stability certification use both $L_2$ and $L_4$.
Those numerical results remain valid within their conditional post-scale model.

CSN changes their provenance interpretation:

- they do not describe the scale-neutral pre-matter phase;
- they may describe a scale-set material phase;
- their existence does not prove that $S^2$, $L_2$, or the coupling ratio is fundamental.

No new GPU run is warranted until a scale-setting completion specifies the post-scale action.

## 9. Falsification and next missing equation

This emergence ordering fails if:

1. a primitive fixed mass term is required in the foundational action;
2. a finite stable massive carrier exists in the pre-scale phase without any scale-setting sector;
3. the complete sourced metric equation cannot accommodate the total trace after scale selection;
4. global closure cannot generate or fix any physical standard;
5. the eventual carrier has no compatible scale-neutral precursor.

The next missing derivation is not another carrier solve. It is:

$$
\boxed{
\text{What native global/boundary equation selects a physical scale while preserving the pre-scale CSN law?}
}
$$

## 10. Honest status

$$
\boxed{
\begin{gathered}
\text{Common-Scale Neutrality: FOUNDATIONAL / owner-LOCKED;}\\
\text{pre-scale trace-free source and no primitive mass: DERIVED in the conformal branch;}\\
L_4\text{ weight/trace compatibility and }L_2\text{ incompatibility: DERIVED for the probe;}\\
\text{finite-size matter requires a scale-set phase: DERIVED for }L_2+L_4\text{ scaling;}\\
\text{carrier, scale-setting mechanism, }X\text{ closure, couplings, and masses: OPEN.}
\end{gathered}
}
$$
