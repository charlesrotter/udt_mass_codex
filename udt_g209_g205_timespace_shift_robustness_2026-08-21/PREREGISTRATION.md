# G209 preregistration — time-space shift robustness

Date: 2026-08-21

## Exact tests

1. **Dependency theorem.** For arbitrary positive `h_A`, prove that the ADM shift is a complete
   independent local sector for fixed lapse and supplied spatial metric. Trace-changing shape must
   not be assumed zero in the local algebra.
2. **Local block algebra.** For

   \[
   g_b=\begin{pmatrix}-f+b^THb&(Hb)^T\\Hb&H\end{pmatrix},
   \]

   derive `det g_b=-f det H`, Lorentz signature, the exact inverse, and
   `g_b^{-1}(dt,dt)=-1/f` for every `b`.
3. **Shifted causal cone.** Prove

   \[
   h_A(v+b,v+b)\le f,
   \]

   and for every radial covector

   \[
   |dr(v)+dr(b)|\le\sqrt f\,|dr|_{h_A^{-1}}.
   \]

   Recover `|dr/dt+b^r|<=f` on G205 and the G208 width
   `f sqrt(cosh(2s))` on its radial-screen tile.
4. **Growth-controlled global hyperbolicity.** On each finite time slab suppose

   \[
   |dr(b)|+\sqrt f\,|dr|_{h_A^{-1}}\le q_I(r),
   \qquad \int^\infty\frac{dr}{q_I(r)}=\infty.
   \]

   Prove or refute that `t` is Cauchy. Include bounded G205 radial shift as a corollary.
5. **Uniformly subluminal static survivor.** On G205 assume static smooth `b` and
   `|b|_{h_0}<=q sqrt(f)` for one `q<1`. Use the conserved stationary energy and exact affine
   bounds to prove or refute two-ended null completeness.
6. **Compact-time-live survivor.** Let `b=0` outside `|t|<T`, with
   `|b|_{h_0}<=q sqrt(f)`, `q<1`, and
   `|partial_t b|_{h_0}<=K sqrt(f)` inside. Use the exact energy equation and Gronwall control;
   do not infer an unrestricted live theorem.
7. **Smooth static failure witness.** On G205 take

   \[
   b=b(r)\partial_r,
   \qquad b(r)=v\frac{r}{\sqrt{R^2+r^2}},
   \qquad v,R>0.
   \]

   Prove Cartesian-center smoothness and global hyperbolicity. For equatorial null geodesics derive

   \[
   \dot r^2=E^2-\left(f-\frac{b^2}{f}\right)\frac{L^2}{r^2}
   \]

   and prove or refute finite affine reach to the outer end for `L!=0`.
8. **Completed pair response.** For `J_i=alpha_i partial_t+v_i`, derive

   \[
   (h_b)_{ij}=-f\alpha_i\alpha_j
   +h_A(v_i+\alpha_i b,v_j+\alpha_j b)
   \]

   and the completed `Phi_b`. Classify coordinate-static, Eulerian-normal, and generic clock germs.

## Certification contract

- Production: exact symbolic block determinant/inverse, cone, stationary Hamiltonian, energy, and
  pair formulas.
- Independent: separate exact-rational implementation with at least 10,000 distinct arbitrary-SPD
  local metric/shift/pair cases, plus an independently parameterized radial Hamiltonian replay.
- High-precision outer-tail controls on at least four G205 profiles and the smooth radial witness.
- At least 20 hostile catches spanning sector completeness, signs, causal center/width, energy,
  smoothness, global/affine distinction, pair strata, evidence ceiling, history selection, and
  `X_max`.
- Saved artifacts replay byte-identically with no writes.
- Fresh external adversarial review before final banking.

## Falsification

The strongest candidate landing fails if determinant/signature or temporal `dt` depends on shift;
if the causal ellipsoid does not translate by `-b`; if the growth condition permits finite-time
escape; if the subluminal static/live survivor is null incomplete; if the radial witness is not
smooth, remains null complete, or loses global hyperbolicity; or if completed pairs fail to hear a
generic shift before readout.

## Scope lock

This is the full local shift sector but one bounded global tile. It does not classify timelike or
spacelike completeness, lapse freedom, trace-changing/full spatial histories, maximal extension,
physical shift/history selection, transfer, observations, action/source/matter, or `X_max`.
