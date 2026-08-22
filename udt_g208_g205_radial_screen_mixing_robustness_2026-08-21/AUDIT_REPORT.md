# G208 audit — radial-screen mixing robustness

Date: 2026-08-21

## Landing

```text
RADIAL_SCREEN_MIXING_PRESERVES_SIGNATURE_AND_AMBIENT_VOLUME_BUT_REPLACES_THE_RADIAL_CAUSAL_BOUND
__GROWTH_CONTROLLED_AND_BOUNDED_STATIC_CLASSES_SURVIVE
__A_SMOOTH_CENTER_REGULAR_UNBOUNDED_STATIC_MIXER_DESTROYS_GLOBAL_HYPERBOLICITY_AND_NULL_COMPLETENESS
__COMPLETED_PAIRS_HEAR_RADIAL_MIXING_BEFORE_READOUT
__NO_PHYSICAL_MIXER_HISTORY_OR_XMAX_SELECTION
```

Grade:
`EXTERNALLY_VERIFIED_WITH_CAVEATS__ANALYTIC_GLOBAL_THEOREMS__INDEPENDENT_ALGEBRAIC_CORE`.

## What was turned on

G208 starts with every supplied G205 base and turns on a smooth self-adjoint spatial endomorphism
that mixes only the radial line and one angular-screen direction. With `A=exp(C)`, the metric is

\[
g_C=-fdt^2+h_0(A\cdot,A\cdot).
\]

The deformation occurs before pair pullback. `C` is a `CHOSE_EXTENSION_CLASS`, not a selected UDT
history.

## Exact result

Locally the mixer is a hyperbolic `2 x 2` block with spatial eigenvalues `exp(+/-2s)` and one
unchanged screen eigenvalue. It preserves Lorentz signature and ambient determinant exactly.

Unlike pure screen shear, it changes radial causality. The sharp law is

\[
|dr/dt|\le f\sqrt{\cosh(2s)}.
\]

If the mixing growth on every finite time slab obeys the preregistered divergent radial-integral
condition, the G205 `t` slices remain Cauchy and the spacetime remains globally hyperbolic. Every
globally bounded static mixer is null complete. Compact-time-live uniformly controlled mixers also
supply a genuine null-complete survivor class.

Smoothness alone is insufficient. A center-regular static mixer with equatorial rapidity
`sigma=4phi` has a contracting-eigenline spiral of optical length

\[
\sqrt2\int f(r)dr<\infty.
\]

Its optical metric is incomplete; the resulting spacetime is neither globally hyperbolic nor null
complete despite remaining smooth, Lorentzian, and determinant-preserving.

## Pair response and factorization

For `J_i=alpha_i partial_t+v_i`,

\[
(h_C)_{ij}=-f\alpha_i\alpha_j+h_0(Av_i,Av_j),
\]

and completed-pair Dual Reciprocity gives

\[
\Phi_C=-\frac12\log[f\alpha_0^2-h_0(Av_0,Av_0)].
\]

Static clocks and the untouched screen direction are blind; radial and generic mixed clock
components respond. Pair area and shift can change despite unchanged ambient determinant.

The G206 common scale composes rather than creating a separate prior mechanism:

\[
d\widehat\lambda=e^{2\Omega}d\lambda_C,
\qquad
\widehat\Phi=\Phi_C-\Omega\circ F.
\]

## Evidence

- Preregistered at commit `fb1af9df` before outcomes.
- 20 production symbolic assertions pass.
- A separate implementation passes 10,000 distinct exact-rational local algebra/pair cases and
  120,004 assertions without importing production code or artifacts.
- Separate 240-digit diagnostics pass four profile tails and five sharp-bound controls.
- 23 hostile mutations are caught.
- The global theorems are analytic; neither finite script independently mechanizes them.
- Live-repository provenance is a separate nine-hash gate and is not rerun by the sealed package
  replay.
- Fresh external review returned `VERIFIED_WITH_CAVEATS`: no mathematical refutation, with only
  the evidence-scope and lay-wording repairs recorded above.

## Ceiling

G208 classifies one supplied configuration-space tile. It does not select a mixer, physical
history, observer population, transfer law, action/source/matter, `X_max`, or a full spacetime
model. Timelike/spacelike completeness, trace-changing modes, shift, and arbitrary spatial maps
remain open.
