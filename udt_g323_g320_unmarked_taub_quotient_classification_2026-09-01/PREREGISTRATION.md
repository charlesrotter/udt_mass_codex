# G323 preregistration — explicit unmarked development classification

Date: 2026-09-01
Status: `PREREGISTERED_CONFIRMATION_AFTER_EXPLORATORY_WHITEBOARD`

## 1. Frozen data

Use the G319/G320 physical data

\[
\gamma=\psi^4(dx^2+dy^2+dz^2),\qquad
B=\epsilon\psi^{-3}\sqrt{36(\psi')^2+J_0},
\]

\[
F=12\psi''\psi^{-5},\qquad A=F/B,
\]

\[
K^x{}_x=(3A-B)/6,\qquad K^y{}_y=K^z{}_z=B/3,
\]

with `J0>0`, `epsilon=+-1`, and smooth positive `2 pi`-periodic `psi`. No data formula may be
changed after seeing the confirmation outputs.

## 2. Candidate common ambient metric

Set

\[
\mu=J_0/9,\qquad R=\psi^2,
\]

and preregister the explicit metric

\[
g_\mu=-\frac{R}{\mu}dR^2+\frac{\mu}{R}dX^2+R^2(dy^2+dz^2),
\qquad R>0.
\tag{1}
\]

The production route must calculate its connection and Ricci tensor directly and must not assume
Ricci flatness by name or analogy.

## 3. Candidate Cauchy embedding

Define `X` along the supplied profile by

\[
X'(x)=-\frac{3B\psi^6}{J_0}.
\tag{2}
\]

Preregister the exact requirements:

1. the pullback of (1) by `(x,y,z)->(R(x),X(x),y,z)` equals `gamma`;
2. with `K=-1/2 L_n gamma`, the induced mixed extrinsic curvature equals all three registered G320
   eigenvalues;
3. `X'` never vanishes, so the embedded circle is a graph over the compact `X` direction;
4. the graph is a Cauchy surface because `R` is a temporal function, the graph is spacelike, and
   the spatial quotient is compact.

The forced primitive `X` period is

\[
L_X[\psi]
=\frac{3}{J_0}\int_0^{2\pi}
\psi^3\sqrt{36(\psi')^2+J_0}\,dx.
\tag{3}
\]

A smaller divisor period is forbidden if it makes the embedding noninjective.

## 4. Local-versus-global classification

The coordinate change

\[
R_*=aR,\quad X_*=X/a,\quad y_*=y/a,\quad z_*=z/a,
\quad \mu_*=a^3\mu,
\tag{4}
\]

must be checked as an exact local isometry. It rescales all three compact coordinate periods by
the same factor. Because the `X` direction is the unique one-dimensional curvature eigendirection
and the `y,z` plane is the repeated eigenspace, preregister the compact-lattice shape modulus

\[
\boxed{\mathcal Q_X=L_X/\sqrt{L_yL_z}}
\tag{5}
\]

as the proposed time-independent unmarked discriminator. The controls keep `L_y=L_z=2 pi`.

For

\[
\psi_n=p+a_0\cos(nx),\qquad p=3/2,\quad a_0=1/5,
\]

equation (3) becomes

\[
L_X(n)=\frac{3}{J_0}\int_0^{2\pi}
(p+a_0\cos u)^3
\sqrt{J_0+36a_0^2n^2\sin^2u}\,du.
\tag{6}
\]

Preregister the exact prediction `L_X(n+1)>L_X(n)` for every positive integer `n`, because the
integrand is pointwise nondecreasing and strictly larger on a set of positive measure. If (1)--(6)
all pass, `n=1` and `n=2` share the same local metric form but define inequivalent compact unmarked
quotients.

## 5. Four-curvature and orientation controls

Directly verify

\[
R_{ab}=0,\qquad
R_{abcd}R^{abcd}=12\mu^2/R^6.
\tag{7}
\]

The curvature scalar must diverge at `R->0`, while radial null affine parameter and timelike proper
time must have infinite reach as `R->infinity`. These are bounded maximal-development interface
checks, not a claim about arbitrary Lorentzian extensions.

Changing `epsilon` reverses `K` and `X'` but leaves (1), (3), and (5) unchanged. Preregister:

- after forgetting time orientation, the two signs are the same unmarked metric quotient;
- with time orientation retained, they are opposite orientations of that quotient;
- a time-orientation-preserving identification is not automatic and must be rejected if the
  monotone curvature time direction forbids it.

## 6. Numerical and independent confirmation contract

- Production: standard-library quadrature for `n=1..4`, both signs, at 16,384 points; exact formula
  assertions for the pullback, extrinsic curvature, Ricci tensor, local isometry, mode monotonicity,
  and forbidden promotions.
- Independent: no import of production code or output; different `p,a0,J0`, modes `1,2,3,5`, and
  sample count; rebuild the ambient connection/Ricci and embedding residuals by a different route.
- Raw tolerances: pullback and extrinsic errors below `2e-11`; Ricci below `2e-11`; independent
  quadrature monotonic margins strictly positive and numerical errors below `5e-10`.
- Hostile mutations must catch a wrong `mu`, sign or factor in (2), omitted primitive-period gate,
  a slice-only `Q_R` substituted for (5), loss of time-orientation typing, false profile selection,
  and any metric/kernel/scale/occupancy promotion.
- Run `python3 verify_current_scientific_premises.py` and the full repository suite before banking.
- Fresh independent adversarial review is required before an externally accepted grade.

## 7. Possible landings

1. `COMMON_LOCAL_GEOMETRY__DISTINCT_COMPACT_UNMARKED_QUOTIENTS` if the explicit embedding and
   strictly different modulus pass;
2. `COMMON_UNMARKED_DEVELOPMENT__PROFILES_ARE_REFOLIATIONS` if the embeddings pass but the global
   modulus is equal or removable by an isometry;
3. `INITIAL_DATA_NOT_EMBEDDED_IN_CANDIDATE_AMBIENT` if either complete pullback fails;
4. `UNMARKED_CLASSIFICATION_INCONCLUSIVE` if the independent or global-invariance gate fails.

## 8. Maximum conclusion

At most, G323 may classify the registered LRS `T^3`, `Lambda=d=0`, `J0>0` family as explicit
unmarked Ricci-flat compact quotient developments and distinguish their quotient moduli and time
orientations. It may not select physical data, a universe, topology, orientation, scale, source,
matter/mass, observation, `X_max`, or promote the provisional dynamics to canon. The UDT metric,
reciprocal kernel, and angular cancellation are unchanged.

