# WR-L scaffold versus native action — inverse-variational results

> **SUBSEQUENT METRIC-ONLY RESULT (2026-07-15):** The no-go below remains exact for regular local
> first-gradient $F(Y)$ actions. A separate metric curvature-squared audit has now found a regular,
> scale-free conditional conformal action whose full Bach equation admits WR-L. WR-L has $C^2=0$
> in that branch, so this does not select WR-L and remains compatible with a zero-cost scaffold
> interpretation. See `UDT_RECIPROCAL_C_CONFORMAL_ACTION_DERIVATION_RESULTS.md`.

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Trigger | Charles Rotter: “Perhaps WR-L is a non-native scaffold.” |
| Mode | Full nonlinear analytic inverse-variational audit; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Symbolic verifier | `verify_udt_wrl_scaffold_separation.py`: **17/17 checks pass** |
| Canon discipline | WR-L canon `C-2026-07-09-1` remains untouched and valid within its stated derivation |
| GPU | Not used or needed |

## 0. Result within the tested $F(Y)$ class

The scaffold hypothesis is substantially strengthened within a broad, natural action class:

$$
\boxed{
\begin{gathered}
\text{No nontrivial regular universal action }I_F=\int\sqrt{-g}\,F(Y)\,d^4x\\
\text{makes WR-L stationary when }Y=\tfrac12\operatorname{Tr}(J_\mu J^\mu)\\
\text{is contracted with the full reciprocal physical metric.}
\end{gathered}
}
$$

The exact inverse action required by WR-L has two defects:

1. $F'(Y)$ diverges at the regular center;
2. it contains $X$ and cannot, even up to normalization, support a second WR-L scale.

Therefore the verdict is:

$$
\boxed{
\text{TESTED CLASS EXCLUDES REGULAR NATIVE WR-L; SCAFFOLD LEAD STRENGTHENED.}
}
$$

This does **not** prove that WR-L is non-native for every possible UDT action. It proves that the
entire local first-gradient reciprocal-current family fails unless singular or profile-scale
structure is inserted.

## 1. What remains banked

The macro result

$$
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2,
\qquad
A(r)=1-\frac rX,
$$

remains

$$
\text{DERIVED under residual re-centering plus wall regularity,}
$$

canon `C-2026-07-09-1`.

That derivation selected a geometric branch. It did not prove that the branch extremizes a unique
off-shell native action. The present result separates those claims rather than retracting the
geometry.

## 2. Action class tested

Start from the reciprocal-c positional group

$$
S(\phi)=\operatorname{diag}(e^{-\phi},e^\phi),
\qquad
J_\mu=S^{-1}\partial_\mu S.
$$

For a static radial field in the full reciprocal physical metric,

$$
ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2,
$$

the invariant first-gradient scalar is

$$
Y=\frac12\operatorname{Tr}(J_\mu J^\mu)
=g^{rr}(\phi')^2
=e^{-2\phi}(\phi')^2.
$$

Because

$$
\sqrt{-g}=c r^2\sin\theta
$$

is independent of $\phi$, the complete static radial reduction of the local class is

$$
I_F=\mathcal N\int_0^X dr\,r^2F(Y).
$$

No expansion, weak-field approximation, fitted term, cutoff, or fixed-background contraction is
used. $F$ is initially arbitrary.

## 3. Full nonlinear variation

Let

$$
p(Y)=F'(Y).
$$

Since

$$
\frac{\partial Y}{\partial\phi}=-2Y,
\qquad
\frac{\partial Y}{\partial\phi'}=2e^{-2\phi}\phi',
$$

the exact Euler equation is

$$
\boxed{
\frac{d}{dr}\left(2r^2e^{-2\phi}\phi' p(Y)\right)
+2r^2Yp(Y)=0.
}
$$

The metric dependence of $Y$ supplies the second term. Omitting it would be the prohibited
fixed-background variation.

## 4. Insert WR-L only after varying

For

$$
A=e^{-2\phi}=1-\frac rX,
$$

one has

$$
\phi=-\frac12\ln\left(1-\frac rX\right),
\qquad
\phi'=\frac{1}{2(X-r)},
$$

and therefore

$$
A\phi'=\frac{1}{2X},
$$

$$
\boxed{
Y_{\rm WR-L}(r)=\frac{1}{4X(X-r)}.
}
$$

The range sampled by the complete interior is

$$
Y_0=\frac{1}{4X^2}
\quad\text{at }r=0,
\qquad
Y\to\infty
\quad\text{as }r\to X^-.
$$

Also

$$
\frac{dY}{dr}=4XY^2.
$$

Substitution into the already varied equation gives

$$
\frac{d}{dr}\left(\frac{r^2}{X}p(Y)\right)
+2r^2Yp(Y)=0.
$$

## 5. Exact inverse solution for the action

Define

$$
z=4X^2Y=\frac{X}{X-r}.
$$

Using

$$
r=X-\frac{1}{4XY},
$$

the Euler equation becomes

$$
\boxed{
Y(z-1)\frac{dp}{dY}+\frac{z+3}{2}p=0.
}
$$

Its nonzero solution is

$$
\boxed{
F'(Y)=p(Y)
=C\,\frac{(4X^2Y)^{3/2}}{(4X^2Y-1)^2}.
}
$$

This is not a fitted candidate. It is the unique nonzero derivative, up to normalization $C$, that
the entire $F(Y)$ action class would need in order to admit the WR-L profile.

## 6. Regularity failure at the center

At the regular WR-L center,

$$
z=4X^2Y_0=1.
$$

The required derivative obeys

$$
F'(Y)\sim\frac{C}{(z-1)^2}
\qquad (z\to1^+).
$$

Thus

$$
\boxed{
\lim_{Y\to Y_0^+}|F'(Y)|=\infty
}
$$

for every nonzero $C$. Setting $C=0$ makes $F$ constant and supplies no dynamics.

The weighted on-shell action could be integrable despite this behavior; that does not repair the
failure. A local off-shell variational law whose first derivative diverges at the regular
configuration value $Y_0$ is not $C^1$, much less the preregistered $C^2$, and has a singular
linear response at the center.

Therefore no nontrivial regular member of the tested class admits WR-L.

## 7. $X$ cannot be an integration constant in this class

The required $F'$ contains the combination $4X^2Y$ and has its singular point at

$$
Y_0(X)=\frac{1}{4X^2}.
$$

For two distinct scales $X_1\neq X_2$, the required functions are

$$
p_{X_i}(Y)\propto
\frac{(4X_i^2Y)^{3/2}}{(4X_i^2Y-1)^2}.
$$

Their ratio depends on $Y$; no choice of overall normalization makes them the same function.
Hence one nontrivial universal $F$ cannot support a WR-L family with varying $X$.

Within this class, WR-L would require inserting one particular $X$ into the action itself. That
would make $X$ an action parameter, not a solution integration constant or a later global datum.
Doing so now would violate the instruction not to smuggle $X$ into the native derivation.

## 8. Quadratic action recovered as a failed special case

For the canonical quadratic group action,

$$
F'(Y)=\text{constant}.
$$

The inverse equation cannot vanish. Equivalently, writing $A=e^{-2\phi}$ reduces the action to

$$
I_{\rm quad}\propto\int dr\,\frac{r^2(A')^2}{4A},
$$

whose exact Euler expression on WR-L is

$$
\boxed{
\left.\mathcal E_A\right|_{\rm WR-L}
=-\frac{r(4X-3r)}{4(X-r)^2}\neq0
\quad(0<r<X).
}
$$

The earlier single-action failure is therefore one instance of the stronger arbitrary-$F$ result.

## 9. What the result does and does not establish

### DERIVED

- No nontrivial $C^2$ universal $F(Y)$ in the tested physical-metric first-gradient class has WR-L
  as a stationary profile.
- The formal inverse action derivative is singular at the regular center.
- The formal inverse action explicitly encodes $X$.
- One such $F$ cannot support distinct WR-L scales.
- WR-L still reaches infinite reciprocal group depth as $r\to X^-$.

### STRONG WORKING LEAD

WR-L is a geometric/global scaffold rather than the stationary profile of the simplest native
reciprocal-current dynamics.

### NOT DERIVED

- WR-L is non-native under every possible UDT action.
- The macro WR-L derivation is false.
- The correct native action is known.
- $X$ must be a postulated fundamental constant.

## 10. Remaining action escape routes

WR-L could still be native only if independently derived UDT structure lies outside the tested
class, for example:

1. an explicit $\phi$ dependence or potential;
2. curvature or higher-derivative invariants of the reciprocal metric;
3. coupling to additional native geometry or a subsequently derived matter carrier;
4. a nonlocal/global bootstrap functional;
5. a boundary principle in which WR-L is a scaffold/readout rather than an Euler stationary point.

These are a census, not proposed repairs. Selecting one merely to recover WR-L would be reverse
engineering, not a UDT derivation.

## 11. Consequence for the research order

The native action search should now proceed from the Reciprocal-c Identity and UDT Reciprocity in
the full time-live geometry, without requiring WR-L as a target solution. Once a candidate action
is independently derived:

1. solve its native static/global sector;
2. determine whether a scale analogous to $X$ emerges;
3. compare that solution with WR-L;
4. retain WR-L as a macro scaffold if it remains useful but is not stationary.

No GPU numerics are warranted before the off-shell action class is analytically specified.

## 12. Honest status

$$
\boxed{
\begin{gathered}
\text{WR-L geometric derivation: RETAINED within its canon stamps;}\\
\text{regular local first-gradient }F(Y)\text{ provenance: FALSIFIED;}\\
\text{WR-L-as-scaffold hypothesis: STRONGLY STRENGTHENED, not proved globally;}\\
\text{native action and global origin of }X:\text{ OPEN.}
\end{gathered}
}
$$
