# UDT smooth bootstrap-substrate closure — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| Mode | Exact global-substrate closure; DATA-BLIND |
| Frozen map | `UDT_SMOOTH_BOOTSTRAP_SUBSTRATE_CLOSURE_MAP.md`, SHA-256 `bfc5b29e2e8e4baa2f1b4b6ad461c2f1e5a3fb636bc20fa7639ee7dff345a1b6` |
| Verifier | `verify_udt_smooth_bootstrap_substrate_closure.py` — 115/115 checks pass |
| Macro firewall | WR-L remains unchanged in its separate macro/readout lane |
| Substrate status | CONDITIONAL on the metric-only conformal action and stated global smooth-domain premises |
| Empirical densities | Not used |
| GPU | Not used; full 3D carrier/backreaction problem remains open |
| Independent verification | OPEN |
| Banking | None; `LIVE.md` and `CANON.md` untouched |

## 0. Result

The smooth bootstrap background does not require a fitted density profile. Within the conditional
metric-only conformal branch, it is the unique smooth zero-action configuration with the universal
endpoint:

\[
\boxed{
A_B(r)=1-\frac{r^2}{X^2}.
}
\]

Equivalently,

\[
\boxed{
q_B(r)=\frac1{1-r^2/X^2}.
}
\]

Its reciprocal-depth flux and flux divergence are

\[
\boxed{
J_q=\frac{q'}{q^2}=-A'=rac{2r}{X^2},
}
\]

\[
\boxed{
\mathcal D_q
=\frac1{r^2}\frac{d}{dr}(r^2J_q)
=\frac6{X^2}.
}
\]

Thus a uniform density-like geometric profile emerges as a consequence of the selected metric; it
was not inserted as a mass-density source.

Combined with the preceding background/carrier calculation, this substrate produces

\[
\boxed{
K_\parallel=\frac{4(r/X)^2}{3X^2}>0,
\qquad
c_\parallel=\frac{4(r/X)^4}{3}>0.
}
\]

The pre-registered verdict is

\[
\boxed{\text{SMOOTH BOOTSTRAP SUBSTRATE SELECTED, conditionally}.}
\]

This is not yet a particle or a mass calculation. It is a coefficient-free background capable of
supplying the scale competition a carrier would need.

## 1. Unique minimum

For the reciprocal spherical metric, the conditional conformal action reduces, up to positive
constants, to

\[
I[A]=\int_0^Xdr\,\frac{W[A]^2}{r^2},
\]

\[
W[A]=r^2A''-2rA'+2(A-1).
\]

Therefore

\[
I[A]\ge0.
\]

The complete zero-action equation is

\[
W[A]=0,
\]

whose solution is

\[
A=1+a r+b r^2.
\]

The substrate conditions

\[
A(0)=1,
\qquad
A'(0)=0,
\qquad
A(X)=0
\]

give

\[
a=0,
\qquad
b=-X^{-2}.
\]

Hence the selected configuration is the unique member of the zero-action set satisfying the stated
smooth global conditions.

It also passes the previously derived unrestricted Bach constraint

\[
a_0^2-3a_1a_{-1}=1,
\]

with

\[
a_0=1,
\qquad a_1=a_{-1}=0.
\]

The minimum is therefore not merely a reduced tangent extremum.

## 2. Why uniform reciprocal flux is an output

The identity

\[
q=A^{-1}
\quad\Longrightarrow\quad
\frac{q'}{q^2}=-A'
\]

contains no field equation. On the selected substrate,

\[
J_q=2r/X^2.
\]

The flux through a coordinate sphere is

\[
\Phi_q(r)=4\pi r^2J_q
=\frac{8\pi r^3}{X^2}.
\]

It equals the integral of the constant geometric source-like quantity

\[
\mathcal D_q=6/X^2
\]

over the enclosed coordinate volume:

\[
\Phi_q(r)
=4\pi\int_0^r\mathcal D_q s^2ds.
\]

This realizes a precise bootstrap picture: the global endpoint fixes the uniform reciprocal-flux
profile, which in turn fixes the local carrier coefficients.

However,

\[
\boxed{
\mathcal D_q\text{ is a geometric flux divergence, not yet physical mass/energy density.}
}

A native charge and normalization are still required before assigning it units of mass density.

## 3. Counterprofile sieve

Consider the endpoint family

\[
A_m=1-(r/X)^m.
\]

Its Weyl numerator is

\[
\boxed{
W[A_m]=-(m-1)(m-2)(r/X)^m.
}

The reduced action is

\[
I_m
=\frac{(m-1)^2(m-2)^2}{(2m-1)X}.
\]

Thus:

- `m=1` has zero action but fails smooth-center regularity;
- `m=2` has zero action and passes smoothness;
- smooth higher powers have positive action.

Endpoint and smoothness alone allow many profiles; the positive conformal functional selects the
quadratic zero-action member among them.

For the same power family,

\[
J_q'=\frac{m(m-1)}{X^2}(r/X)^{m-2},
\]

\[
\mathcal D_q
=\frac{m(m+1)}{X^2}(r/X)^{m-2}.
\]

Only `m=2` makes `D_q` uniform. Uniformity is therefore a consequence of the action-selected smooth
profile, not an additional premise in this branch.

## 4. Carrier bridge

The metric-derived parallel carrier coefficients for a general depth background are

\[
K_\parallel
=\frac{2(q-1)}{3q}J_q',
\qquad
c_\parallel
=\frac{4(q-1)^2}{3q^2}.
\]

For the selected substrate,

\[
\frac{q-1}{q}=\frac{r^2}{X^2},
\qquad
J_q'=rac2{X^2},
\]

which yields the positive coefficients in the result box.

Their pointwise ratio is

\[
\boxed{
\frac{c_\parallel}{K_\parallel}=r^2.
}

For a nontrivial three-dimensional carrier with positive integrated two- and four-derivative
sectors, the fixed-background scaling would have the form

\[
E(R)=\alpha_Cc\left(
\mathcal E_2\frac R{X^2}
+\mathcal E_4\frac1R
\right).
\]

This has a finite formal stationary ratio

\[
\frac RX=\sqrt{\mathcal E_4/\mathcal E_2}.
\]

The statement is **CONDITIONAL/WORKING** because the full three-dimensional functional,
backreaction, topology, and boundary domain have not yet been solved.

## 5. Relationship to WR-L

This result does not replace or revise the live macro metric

\[
A_L=1-r/X.
\]

The lanes answer different questions:

- WR-L is the derived residual macro/readout geometry under its wall package.
- `A_B=1-r^2/X^2` is a conditional smooth pre-matter substrate selected by the conformal action and
  global smooth-domain premises.

Attempting to splice the two as source-free regions was already proved impossible. Treating the
smooth geometry as a separate substrate avoids claiming such a splice. A future complete theory
must still explain how its physical readout produces the WR-L macro law.

The earlier rejection of the quadratic profile under a different historical native `phi` equation
is not silently overturned. This is a distinct conditional action branch with explicit provenance.

## 6. Density calibration gate

The calculation determines

\[
\mathcal D_q=6/X^2
\]

geometrically. It does not determine a conversion

\[
\rho_{\rm physical}=\mathcal N\mathcal D_q.
\]

The normalization `N`, conserved charge, and backreaction meaning remain open. Consequently,
bracketing Standard Model or observed mass densities at this stage would fit `N` rather than test
UDT.

Those values become admissible only after the full action supplies a normalized energy or boundary
charge. They may then calibrate one overall conversion and test all remaining ratios.

## 7. Honest status

### DERIVED within the conditional substrate branch

- Unique smooth fixed-endpoint zero-action metric `A_B=1-r^2/X^2`.
- Full Bach compatibility.
- Uniform reciprocal-flux divergence `6/X^2`.
- Positive, coefficient-free parallel carrier stiffness and quartic cost.

### WORKING

- The smooth global substrate may be the background envisioned by the bootstrap principle.
- Its carrier coefficients have the right scaling signs for finite-size balance.

### OPEN

- Full covariant three-dimensional carrier functional on the substrate.
- Whether a protected carrier target emerges or must be independently postulated.
- Carrier backreaction and time-live stability.
- Normalized energy/mass density and charge.
- The physical map between this substrate and the WR-L macro readout.

\[
\boxed{
\text{The bootstrap background and its density-like profile are now derived conditionally;}
\quad
\text{matter and mass remain open.}
}
\]
