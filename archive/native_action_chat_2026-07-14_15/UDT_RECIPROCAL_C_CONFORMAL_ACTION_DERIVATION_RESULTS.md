# Reciprocal-c metric-only conformal action — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Foundational origin | Charles Rotter's Reciprocal-c Identity plus UDT Reciprocity |
| Mode | DISCLOSED NON-COLD analytic action sieve; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Symbolic verifier | `verify_udt_reciprocal_c_conformal_action.py`: **29/29 checks pass** |
| Full-tensor gate | Bach tensor reconstructed directly from metric, connection, curvature, and covariant derivatives |
| Adoption | **Common-Scale Neutrality owner-LOCKED after this audit**; resulting action remains conditional on the other named premises |
| GPU | Not used or needed |

> **OWNER STATUS UPDATE (2026-07-15):** Charles Rotter has locked Common-Scale Neutrality as a
> foundational UDT postulate. See `UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md`. Statements
> below calling it OPEN preserve the derivation-time audit trail; for subsequent work its status is
> FOUNDATIONAL. Locality, four-dimensionality, parity, lowest derivative order, unrestricted metric
> variation, and boundary viability remain separate premises.

## 0. Decisive result

The Reciprocal-c Identity exposes one further structural choice that was previously hidden.

Every positive time/radial calibration decomposes uniquely as

$$
\operatorname{diag}(u,v)
=\underbrace{\sqrt{uv}\,I}_{\text{common scale}}
\underbrace{\operatorname{diag}(e^{-\phi},e^\phi)}_{\text{reciprocal depth}},
$$

where

$$
\phi=\frac12\ln\frac vu.
$$

Reciprocal-c plus UDT Reciprocity fixes the determinant-one depth part. It leaves the common scale
undetermined because simultaneous rescaling of time and length does not change $c$.

If—and only if—one adds the candidate principle

> **Common-scale neutrality:** the reciprocal $c/c^{-1}$ identity is the complete local
> time-length standard, so simultaneous local rescaling changes calibration rather than physics,

then the metric has the local equivalence

$$
g_{\mu\nu}\sim\Omega(x)^2g_{\mu\nu}.
$$

Under the further named premises metric-only, four-dimensional locality/covariance, parity-even
bulk, no inserted length, lowest nontrivial derivative order, and unrestricted metric variation,
the bulk action is uniquely

$$
\boxed{
S_C=\alpha_C\int d^4x\sqrt{-g}\,
C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
}
$$

up to normalization, the Euler topological term, boundary terms, and parity-odd topology.

This is a **UNIQUE-CONDITIONAL** action branch, not yet an unconditional UDT derivation.

Its full covariant equation admits WR-L exactly, with $X$ as a solution constant rather than an
action parameter. However WR-L is conformally flat and has zero action density in this branch. The
action admits WR-L but does not select it or assign it local conformal-curvature cost.

## 1. What is new and what is not

### New

The proposed Reciprocal-c foundation naturally separates:

1. inverse time/radial positional depth, fixed by Reciprocity;
2. common time-length calibration, invisible to the value of $c$.

This identifies common-scale neutrality as a precise possible bridge from kinematics to a
metric-only action principle.

### Not yet derived

The fact that a common scale leaves $c$ unchanged does not logically prove that the scale is
unphysical. Clocks, rulers, matter, or global boundary data could supply an absolute local scale.
Therefore common-scale neutrality remains an **OPEN FOUNDATIONAL CANDIDATE**, not something silently
contained in the arithmetic of $c$.

## 2. Why the action begins at curvature squared

Under

$$
g_{\mu\nu}\mapsto\Omega^2g_{\mu\nu}
$$

in four dimensions:

- $\sqrt{-g}$ has conformal weight $+4$;
- the volume term is not invariant;
- $\sqrt{-g}R$ is not locally conformally invariant;
- $C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}$ has weight $-4$, so its product with
  $\sqrt{-g}$ is invariant.

At curvature-quadratic order the parity-even basis is

$$
R^2,
\qquad
R_{\mu\nu}R^{\mu\nu},
\qquad
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}.
$$

The exact identities are

$$
E_4=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
-4R_{\mu\nu}R^{\mu\nu}+R^2,
$$

$$
C^2=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
-2R_{\mu\nu}R^{\mu\nu}+\frac13R^2.
$$

In four dimensions $E_4$ contributes topology/boundary rather than a local bulk equation. Thus

$$
C^2-E_4
=2R_{\mu\nu}R^{\mu\nu}-\frac23R^2.
$$

Local common-scale invariance selects $C^2$ inside this basis. Without that new principle,
$R^2$ and $R_{\mu\nu}R^{\mu\nu}$ have independent Euler operators, so metric-only locality remains
nonunique.

Higher-derivative conformal invariants remain possible if the lowest-derivative premise is dropped.

## 3. Full covariant equation

Varying the unrestricted metric gives the trace-free Bach equation

$$
\boxed{
B_{\mu\nu}=0,
}
$$

with the convention

$$
B_{\mu\nu}
=\left(\nabla^\rho\nabla^\sigma+\frac12R^{\rho\sigma}\right)
C_{\mu\rho\nu\sigma}.
$$

The verifier reconstructs this tensor from the metric rather than importing a precomputed spherical
equation. This is essential because reciprocal reduction before variation can otherwise lose
normal metric equations.

The equation is fourth differential order. Whether its time-live initial-value problem, finite-cell
boundary terms, energy, and additional modes are acceptable is **OPEN**. Lowest nontrivial
conformal order is not the same as second-order dynamics.

## 4. Reciprocal static invariant basis

For

$$
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2,
$$

direct metric calculation gives

$$
R=-A''-\frac{4A'}r-\frac{2(A-1)}{r^2},
$$

and

$$
\boxed{
C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
=\frac{\left[r^2A''-2rA'+2(A-1)\right]^2}{3r^4}.
}
$$

The Euler density reduces exactly to a boundary derivative:

$$
r^2E_4
=4\left[(A-1)A''+(A')^2\right]
=\frac{d}{dr}\left[4(A-1)A'\right].
$$

The reciprocal reduction of $\sqrt{-g}R$ is also a boundary term. In contrast, $R^2$ and
$R_{\mu\nu}R^{\mu\nu}$ give independent fourth-order bulk equations.

For $C^2$, the reduced Euler equation is

$$
\boxed{
rA''''+4A'''=0,
}
$$

equivalently

$$
\frac{d}{dr}\left(r^4A'''\right)=0.
$$

## 5. Static solution family found without inserting WR-L

The complete reduced solution is

$$
A(r)=a_0+a_1r+\frac{a_{-1}}r+a_2r^2.
$$

The full Bach tensor, not merely the reduced equation, imposes

$$
\boxed{
a_0^2-3a_1a_{-1}=1.
}
$$

Specifically, on the reduced four-constant family,

$$
B^t{}_t=B^r{}_r
=\frac{a_0^2-3a_1a_{-1}-1}{6r^4},
$$

$$
B^\theta{}_\theta=B^\varphi{}_\varphi
=-\frac{a_0^2-3a_1a_{-1}-1}{6r^4}.
$$

This trace-free full-tensor constraint was reconstructed directly in the verifier.

## 6. WR-L appears afterward

WR-L is the member

$$
a_0=1,
\qquad
a_1=-\frac1X,
\qquad
a_{-1}=0,
\qquad
a_2=0.
$$

It satisfies the full constraint for every positive $X$. Therefore

$$
\boxed{
B_{\mu\nu}[\text{WR-L}]=0
}
$$

without placing $X$ in the action.

This is the first audited metric-only action branch in the present arc that:

1. follows from a clearly stated possible extension of Reciprocal-c;
2. is regular and scale-free at the action level;
3. admits WR-L under full covariant variation;
4. leaves $X$ as solution/boundary data.

It does not uniquely select the WR-L member from the larger solution family.

## 7. Why this may still describe a scaffold

For WR-L,

$$
A=1-\frac rX,
\qquad
A'=-\frac1X,
\qquad
A''=0.
$$

Therefore

$$
r^2A''-2rA'+2(A-1)=0,
$$

and hence

$$
\boxed{C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}=0.}
$$

Yet

$$
R_{\rm WR-L}=\frac{6}{Xr}\ne0.
$$

So WR-L is curved but conformally flat. In the conditional $C^2$ action it is a zero-density vacuum
configuration.

This yields three distinct statements:

- **DERIVED conditionally:** the action admits WR-L.
- **FALSE:** the action uniquely selects WR-L.
- **VIABLE INTERPRETATION:** WR-L is a conformal/causal scaffold—an observational geometry with no
  conformal-curvature cost—while physical localized structure requires departures, boundaries, or
  additional derived sectors.

The last statement is a working interpretation, not yet a matter-emergence derivation.

## 8. What happens to $X$

The action contains no $X$. The coefficient $a_1$ is an integration/boundary constant, and WR-L
identifies

$$
X=-\frac1{a_1}.
$$

Thus the conditional conformal branch demonstrates that $X$ **can** arise without being a local
action constant. It does not compute $X$, prove its universality, or connect it to $c$, total mass,
or $G$. Those require global closure and boundary physics.

There is therefore still no reason to postulate $X_{\max}$ at the local-action stage.

## 9. Relationship to the $F(Y)$ no-go

There is no contradiction.

The previous inverse theorem excluded regular local first-gradient actions

$$
\int\sqrt{-g}\,F(Y)
$$

for the reciprocal group current. The present action is metric curvature-squared and contains
second derivatives of the metric before variation. It lies outside that class.

The new result weakens any broad claim that WR-L cannot be native, while preserving the exact
$F(Y)$ no-go. Because WR-L has $C^2=0$, the result is also compatible with the narrower statement
that WR-L behaves as a scaffold rather than an energetic dilation soliton.

## 10. Matter and mass remain open

> **SUBSEQUENT OWNER LOCK AND MATTER SIEVE (2026-07-15):** Common-Scale Neutrality is now
> foundational. In the conditional $C^2$ metric branch the pre-scale source must be trace-free;
> fixed primitive mass and the historical $L_2$ term violate CSN, while four-derivative carrier
> densities such as $L_4$ pass the scale-weight gate but remain nonunique. See
> `UDT_COMMON_SCALE_MATTER_EMERGENCE_DERIVATION_RESULTS.md`.

Nothing here derives:

- a matter carrier or $S^2$;
- a positive localized energy theorem;
- the coupling of matter to $B_{\mu\nu}$;
- the observed gravitational constant;
- the electron mass;
- $M_N=2E_4$;
- matter recycling or bootstrap closure.

The existing EH-based lapse identity remains conditional on a different geometric action and cannot
be imported into this branch.

If the conformal branch is pursued, matter emergence must arise from independently derived
conformal structure, boundary/global symmetry breaking, or another native sector. No such mechanism
is supplied here.

## 11. Exact status

$$
\boxed{
\begin{gathered}
\text{Reciprocal-c decomposition into reciprocal depth plus common scale: DERIVED;}\\
\text{common-scale neutrality: OPEN FOUNDATIONAL CANDIDATE;}\\
\text{minimal metric-only }C^2\text{ action: UNIQUE-CONDITIONAL;}\\
\text{full Bach equation and reciprocal solution family: DERIVED under that action;}\\
\text{WR-L full-equation membership and }C^2=0:\text{ DERIVED;}\\
\text{WR-L selection, action viability, mass, matter, and global }X:\text{ OPEN.}
\end{gathered}
}
$$

The next owner-level question is now precise:

> Is common local time-length scale itself physical, or is only the reciprocal $c/c^{-1}$ relation
> fundamental?

If common scale is neutral, the conformal action branch is the first sharply selected native-action
candidate generated by the Reciprocal-c foundation. If common scale is physical, this branch loses
its selector and the curvature-action family remains open.
