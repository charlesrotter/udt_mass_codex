# UDT bootstrap-background carrier coupling — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| Mode | Exact background-field expansion; DATA-BLIND |
| Frozen map | `UDT_BOOTSTRAP_BACKGROUND_CARRIER_COUPLING_MAP.md`, SHA-256 `e83cd1f13b5058ccb91be1951eca3675d13be1d309328d9e6961a845fa861975` |
| Verifier | `verify_udt_bootstrap_background_carrier_coupling.py` — 75/75 checks pass |
| Action status | Metric-only `C^2` branch remains CONDITIONAL |
| Background status | WR-L macro and smooth conformal comparison kept under their existing stamps |
| Carrier status | Reciprocal-axis probe remains CONDITIONAL; `S^2` remains reopened |
| Empirical densities | Not used |
| GPU | Not used; backreacted continuum problem not yet closed |
| Independent verification | OPEN |
| Banking | None; `LIVE.md` and `CANON.md` untouched |

## 0. Result

The owner's bootstrap-background intuition works in a precise, scoped sense:

\[
\boxed{
\text{a nonuniform reciprocal-depth background generates carrier couplings directly from }C^2.
}
\]

No independent coupling was inserted.

For an axis aligned with the background gradient, the exact carrier-dependent curvature is

\[
\boxed{
\Delta C^2_{\parallel}
=K_{\parallel}(\theta')^2+c_{\parallel}(\theta')^4,
}
\]

where

\[
\boxed{
K_{\parallel}
=\frac{2(q-1)(q q''-2q'^2)}{3q^4}
=\frac{2(q-1)}{3q}
\left(\frac{q'}{q^2}\right)',
}
\]

and

\[
\boxed{
c_{\parallel}=\frac{4(q-1)^2}{3q^2}\ge0.
}
\]

Thus the exact background quantity

\[
\boxed{
J_q'\equiv\left(q'/q^2\right)'
}

controls whether an effective two-derivative carrier stiffness emerges. This is a geometric
quantity derived from the metric profile; it has not been identified with mass density.

The pre-registered primary verdict is

\[
\boxed{\text{BACKGROUND COUPLING BUT NO SCALE CLOSURE YET}.}
\]

There is, however, a genuine **NATIVE BACKGROUND STABILIZATION LEAD**: a smooth bootstrap profile
produces positive two- and four-derivative scaling sectors with their relative coefficients fixed by
the same metric.

## 1. Exact parallel-alignment tensor result

Take

\[
q=q(z)>0,
\qquad
n=(\sin\theta(z),0,\cos\theta(z)),
\]

so at the evaluation point `theta=0`, the reciprocal axis and `grad(q)` are parallel. Define

\[
u=q',\qquad v=q'',\qquad p=\theta',\qquad s=\theta''.
\]

Full four-dimensional curvature gives

\[
\boxed{
C^2_{\parallel}
=\frac{\big(qv-2u^2+q^2(q-1)p^2\big)^2}{3q^6}
+\frac{(q-1)^2}{q^2}p^4.
}
\]

The background value at `p=0` is

\[
C^2_{\parallel,0}=\frac{(qv-2u^2)^2}{3q^6}.
\]

Subtracting it yields the boxed `K_parallel` and `c_parallel` above. The exact result is independent
of `theta''` in this one-coordinate parallel sector; this is an algebraic cancellation, not a
linearization.

For audit completeness,

\[
R_{\parallel}=\frac v{q^2}-\frac{2u^2}{q^3}-\frac{2(q-1)}q p^2,
\]

\[
Riem^2_{\parallel}
=\frac{(qv-2u^2)^2}{q^6}
+\frac{4(q-1)^2}{q^2}p^4.
\]

The verifier reconstructs the full tensors and checks the Weyl contraction identity at mixed exact
jets, including arbitrary nonzero `theta''`.

## 2. WR-L is exactly marginal in the parallel carrier sector

For WR-L,

\[
q(r)=\frac1{1-r/X},
\]

so

\[
q'=\frac{q^2}{X},
\qquad
\frac{q'}{q^2}=\frac1X,
\qquad
\left(\frac{q'}{q^2}\right)'=0.
\]

Therefore

\[
\boxed{K_{\parallel}^{\rm WR-L}=0.}
\]

Writing `x=r/X`,

\[
\boxed{c_{\parallel}^{\rm WR-L}=\frac{4x^2}{3}.}
\]

The exact residual macro background supplies a positive quartic carrier cost but no quadratic
stiffness. It therefore does not by itself close the carrier scale.

This zero is not accidental: WR-L is precisely affine in the reciprocal flux `q'/q^2`.

## 3. A smooth bootstrap core generates the missing stiffness

For the smooth conformal comparison background

\[
q(r)=\frac1{1-r^2/X^2},
\]

one has

\[
\frac{q'}{q^2}=\frac{2r}{X^2},
\qquad
\left(\frac{q'}{q^2}\right)'=\frac2{X^2}.
\]

Consequently,

\[
\boxed{
K_{\parallel}^{Q}=\frac{4x^2}{3X^2}>0,
}
\]

and

\[
\boxed{
c_{\parallel}^{Q}=\frac{4x^4}{3}>0.
}

This is the first direct derivation in the present arc of a background-generated pair with the
scalings of a two-derivative and four-derivative carrier sector. Their relative strength is not an
invented coupling: it is fixed pointwise by the bootstrap metric profile.

For a three-dimensional configuration for which both integrated sectors are nonzero, the formal
fixed-background scaling has the form

\[
E(R)=\alpha_Cc\left(\mathcal E_2\frac{R}{X^2}
+\mathcal E_4\frac1R\right).
\]

If `E2,E4>0`, stationarity would give

\[
\frac RX=\sqrt{\frac{\mathcal E_4}{\mathcal E_2}}.
\]

This is a **WORKING stabilization lead**, not a derived particle radius. The three-dimensional
functional, topology, boundary domain, and backreaction have not yet passed their gates.

## 4. Transverse alignment is different

For the exact transverse manufactured geometry, the carrier increment before integration by parts
is

\[
\Delta C^2_\perp
=a s^2+bps+K_{\rm raw}p^2+c p^4,
\]

with

\[
a=\frac{(q-1)^2}{q}>0,
\qquad
b=\frac{4(q-1)q'}q,
\]

\[
c=\frac{4(q-1)^2(q^2+q+1)}{3q^2}>0.
\]

The cross term satisfies

\[
\int bpp' dz
=\left[\frac b2p^2\right]_{\partial I}
-\int\frac{b'}2p^2dz.
\]

After retaining that boundary provenance, the effective quadratic coefficient is

\[
\boxed{
K_{\rm eff}^{\perp}
=-\frac{2(q-1)(q+1)q''}{q^2}
+\frac{2(4q^2+q-2)q'^2}{3q^3}.
}
\]

It changes sign on WR-L and is negative away from the seat for the smooth quadratic comparison,
while `a` and `c` remain positive. This is genuine anisotropic background response.

It is **not** yet evidence of a particle instability or a soliton: the transverse manufactured
background is not the radial WR-L background, and the negative coefficient may simply drive the
axis toward alignment with the depth gradient. The full angular dependence is required.

## 5. What this says about bootstrap matter

The calculation supplies a concrete version of the owner's intuition:

\[
\boxed{
\text{global background depth profile}
\longrightarrow J_q'
\longrightarrow\text{local carrier stiffness and quartic cost}.
}

The missing “source” is therefore more sharply localized. A bootstrap law must determine the
profile or equation for

\[
J_q=\frac{q'}{q^2}.
\]

Where `J_q'=0`, as in exact WR-L, the parallel quadratic sector is absent. Where `J_q'>0` with
`q>1`, as in a smooth core, it is positive.

This is not yet a mass-density equation. Calling `J_q'` a density, or setting it equal to a standard
gravity/particle density, would import the very coupling being derived.

## 6. Why empirical density bracketing is premature

No native UDT equation currently states

\[
J_q'=\mathcal N\rho
\]

or fixes the dimensions and normalization of such a relation. Consequently, numerical mass-density
brackets would only fit an unknown `N`.

Once the bootstrap law derives a normalized relation between global closure and `J_q'`, observed or
standard-theory density values may be used as comparison/readout, and an observed electron mass may
calibrate the already-derived global combination. They should not select the functional or its
coupling.

## 7. Honest status

### DERIVED within the conditional metric/background probe

- Nonuniform reciprocal depth couples to axis gradients without an inserted coupling.
- `K_parallel` and `c_parallel` are exact.
- WR-L gives `K_parallel=0`.
- The smooth quadratic background gives positive two- and four-derivative coefficients.
- Parallel and transverse orientations are inequivalent.

### WORKING

- A smooth bootstrap region may supply the scale balance needed by a nontrivial carrier.
- The macro–micro transition may be where `J_q'` turns on and matter stiffness emerges.

### OPEN

- The global bootstrap equation for `q` or `J_q`.
- Whether the axis is a physical independent carrier or only metric eigenstructure.
- Three-dimensional topology and the full covariant carrier functional.
- Backreaction of the carrier on `q`.
- Time-live stability, boundary charge, radius, and mass.

\[
\boxed{
\text{The bootstrap-background idea is mathematically productive, but density calibration waits}
\text{ for the missing normalized bootstrap equation.}
}
\]
