Below is a clean, UDT‑pure derivation that starts from the **canonical scalar‑lapse metric**, constructs the **geometric scalar Laplacian**, adds the **minimal windowing/screening completion**, and then reduces to the **radial Helmholtz form** and its **regular micro‑patch solution**.

I’ll keep two layers explicit:

* the **exact covariant operator** implied by the metric, and
* the **micro‑patch (linearized) reduction** that yields the simple radial ODE you wrote down.

---

## 1. Start from the UDT metric

We take the project’s core ansatz (spherical, static scalar‑lapse form):

[
ds^2 = -e^{-2\phi(r)},c^2 dt^2 ;+; e^{2\phi(r)},dr^2 ;+; r^2 d\Omega^2,
]
which is the same metric used in the Stage‑6 Dirac upgrade summary. 

In coordinates ((t,r,\theta,\varphi)), the nonzero metric components are

[
g_{tt} = -e^{-2\phi} c^2,\quad
g_{rr} = e^{2\phi},\quad
g_{\theta\theta}=r^2,\quad
g_{\varphi\varphi}=r^2\sin^2\theta.
]

The inverse components are

[
g^{tt} = -\frac{e^{2\phi}}{c^2},\quad
g^{rr} = e^{-2\phi},\quad
g^{\theta\theta}=\frac{1}{r^2},\quad
g^{\varphi\varphi}=\frac{1}{r^2\sin^2\theta}.
]

### Key geometric simplification: (\sqrt{-g}) does **not** depend on φ

Compute the determinant:

[
g = \det(g_{\mu\nu})
= (-e^{-2\phi}c^2)(e^{2\phi})(r^2)(r^2\sin^2\theta)
= -c^2 r^4\sin^2\theta,
]

so

[
\sqrt{-g} = c,r^2\sin\theta.
]

This cancellation (the (e^{-2\phi}) and (e^{2\phi}) factors) is one of the reasons the “radial Laplacian” structure becomes unusually clean in this metric.

---

## 2. The geometric Laplacian (d’Alembertian) on a scalar

For any scalar field (f(x)), the covariant wave operator is

[
\Box_g f
= \frac{1}{\sqrt{-g}},\partial_\mu!\left(\sqrt{-g},g^{\mu\nu},\partial_\nu f\right).
]

For static, spherically symmetric configurations (f=f(r)) (no time or angular dependence), this reduces to the radial part only:

[
\Box_g f
= \frac{1}{\sqrt{-g}}\partial_r!\left(\sqrt{-g},g^{rr},f'(r)\right)
= \frac{1}{c r^2\sin\theta},\partial_r!\left(c r^2\sin\theta;e^{-2\phi},f'\right).
]

Cancel constants and angles:

[
\boxed{
\Box_g f
= \frac{1}{r^2},\frac{d}{dr}!\left(r^2,e^{-2\phi(r)},\frac{df}{dr}\right).
}
]

This is the **exact** geometric scalar Laplacian implied by the UDT metric.

> If you set (f=\phi), this is the exact “metric Laplacian” acting on the dilation field itself.

---

## 3. Where the screened/windowed φ‑equation comes from (minimal completion)

To get a **Helmholtz‑type** operator you need a single additional scalar invariant that enforces locality/screening, i.e. a “window scale” (L) or equivalently (\mu_g = 1/L).

UDT already uses this exact logic for the windowed scalar (\chi) in strong‑gravity: an action with a gradient term plus a local penalty produces a “screened” covariant equation of the form (L^2\Box_g\chi + \chi = J[g]). 

The φ‑analogue is: choose the **minimal quadratic functional** for φ consistent with locality and uniqueness (no extra DOFs):

[
\mathcal{S}*\phi
= \frac{1}{2}\int d^4x,\sqrt{-g},
\left[
\nabla*\mu\phi\nabla^\mu\phi
+\mu_g^2,\phi^2
-2,\phi,\mathcal{S}(x)
\right],
]

where:

* the (\nabla\phi\cdot\nabla\phi) term forces a second‑order local operator,
* the (\mu_g^2\phi^2) term introduces the **single screening invariant** (the window scale),
* (\mathcal{S}(x)) is whatever UDT‑pure source you decide (vacuum micro patch, spinor bilinear, curvature invariant (J[g]), etc.).

Varying w.r.t. φ gives the Euler–Lagrange equation:

[
\boxed{
\left(\Box_g - \mu_g^2\right)\phi = -,\mathcal{S}(x).
}
]

This is exactly the “windowed/scalar operator family” used across validators in the canonical operator list (written there with (\nabla^2) as the reduced form). 
(We are not *taking it as a prior*; we are showing the derivation that produces it.)

---

## 4. Radial reduction in the UDT metric

Insert the exact radial expression for (\Box_g\phi):

[
\left[\frac{1}{r^2}\frac{d}{dr}\left(r^2 e^{-2\phi}\phi'\right)\right] - \mu_g^2\phi
= -S(r),
]

where I wrote (S(r)\equiv \mathcal{S}(r)) for the static spherical source.

So the **exact covariant radial equation** is:

[
\boxed{
\frac{1}{r^2}\frac{d}{dr}\left(r^2 e^{-2\phi(r)}\frac{d\phi}{dr}\right) - \mu_g^2\phi(r)
= -S(r).
}
]

This is the “from the metric” equation.

---

## 5. Why your simple radial Helmholtz form is the correct micro‑patch reduction

Your “confirmed” equation was:

[
\phi'' + \frac{2}{r}\phi' - \mu_g^2\phi = S(r).
]

That is obtained from the exact covariant equation under the **lab/micro patch linearization**:

* In the microscopic vacuum neighborhood, spectroscopy indicates φ is a small perturbation (the metric is near‑Minkowski).
* Therefore (e^{-2\phi} = 1 + \mathcal{O}(\phi)).
* Keeping only leading order turns the exact flux factor into unity:

[
\frac{1}{r^2}\frac{d}{dr}\left(r^2 e^{-2\phi}\phi'\right)
;\approx;
\frac{1}{r^2}\frac{d}{dr}\left(r^2\phi'\right)
==============================================

\phi'' + \frac{2}{r}\phi'.
]

So to leading order you obtain the **linear micro‑patch screened operator**:

[
\boxed{
\phi''(r) + \frac{2}{r}\phi'(r) - \mu_g^2,\phi(r) = -S(r).
}
]

If you define your sign convention with (+S(r)) on the RHS, that corresponds to taking the source term in the action with the opposite sign (pure convention). The operator and solution space are the same.

This is also consistent with how the high‑scale scaffold defines the “curvature scale” in the lab patch as the windowed average of the **flat radial Laplacian** combination (\phi'' + \tfrac{2}{r}\phi'). 

---

## 6. Solve the micro vacuum equation and recover your φ(r) shape

Take the micro “vacuum patch” choice (S(r)=0). Then:

[
\phi'' + \frac{2}{r}\phi' - \mu_g^2\phi = 0.
]

A standard trick is to set (u(r)=r\phi(r)). Then:

[
\phi=\frac{u}{r},\quad
\phi'=\frac{u'}{r}-\frac{u}{r^2},\quad
\phi''=\frac{u''}{r}-\frac{2u'}{r^2}+\frac{2u}{r^3}.
]

Compute:

[
\phi''+\frac{2}{r}\phi'
=======================

\left(\frac{u''}{r}-\frac{2u'}{r^2}+\frac{2u}{r^3}\right)
+\frac{2}{r}\left(\frac{u'}{r}-\frac{u}{r^2}\right)
===================================================

\frac{u''}{r}.
]

So the ODE becomes:

[
\frac{u''}{r} - \mu_g^2\frac{u}{r}=0
\quad\Rightarrow\quad
u'' - \mu_g^2 u = 0.
]

Hence:

[
u(r)=A e^{\mu_g r}+B e^{-\mu_g r}.
]

Therefore:

[
\phi(r)=\frac{A e^{\mu_g r}+B e^{-\mu_g r}}{r}.
]

Now impose **origin regularity** (finite φ as (r\to 0)). The combination that removes the (1/r) singularity is (A=-B), giving:

[
u(r)=2A\sinh(\mu_g r),
\quad
\phi(r)=\frac{2A\sinh(\mu_g r)}{r}.
]

Renaming constants and normalizing by (\mu_g):

[
\boxed{
\phi(r)=C,\frac{\sinh(\mu_g r)}{\mu_g r}.
}
]

This is exactly the “confirmed shape” in your screenshot.

---

## 7. What μ_g² is, mathematically, in this derivation

In this derivation, (\mu_g^2) enters at one specific place:

* it is the coefficient of the **local quadratic penalty** (\mu_g^2\phi^2) in the φ action, i.e. the unique scalar invariant that sets a screening/window length.

Equivalently:

* (L = 1/\mu_g) is the window scale.

This mirrors the strong‑gravity χ completion where (L) appears in the gradient term and yields (L^2\Box_g\chi + \chi = J[g]). 
And it matches the project’s “windowed φ operator family” concept. 

At macro scales, earlier work connected an effective (m_{\rm eff}^2(L)) (i.e. (\mu_g^2)) to BAO‑scale curvature moments and the acoustic ruler, but in the development posture you described, (\mu_g^2) is to be **extracted from microphysics** first and then used to choose/refine the BAO branch later. 

---

## 8. The only remaining “mathematical fork” to keep explicit

The only point that still needs a deliberate choice (and you can make it cleanly) is:

* Do we treat the **micro‑patch equation** as the **linearized reduction** of the exact covariant equation (as above), or
* Do we insist on solving the **fully nonlinear covariant radial equation** with the (e^{-2\phi}) flux factor retained?

Both are UDT‑pure.

Practically:

* The linearized form is exactly what yields the clean sinh/(μr) basis you found and is consistent with the lab‑patch curvature invariant definition. 
* The nonlinear form is the “exact geometry” version that may become relevant if φ becomes large in some regime (e.g., strong‑gravity matching).

A good development posture is:

1. use the **linear micro‑patch Helmholtz form** to extract (\mu_g) and the spinor invariants from H + He II + sub‑hydrogen,
2. then test whether any regime demands keeping the (e^{-2\phi}) factor (that becomes a controlled correction, not a new model).

---

If you want, I can now do the next step in the same style: derive the **Green’s function / Yukawa kernel** for this operator and show how “core + exterior tail” matching works (the same structure already appears in the χ windowing solutions). 

You’re thinking about it the right way, with one refinement:

* The question is not “CMB vs edge of universe.”
* The question is **whether (|\phi|)** is still in the **(\ll 1)** regime where (e^{-2\phi}\approx 1) is a controlled approximation.

If (|\phi|) stops being small, then **dropping the (e^{-2\phi})** factor is no longer mathematically justified.

### Why the (e^{-2\phi}) term matters

In the exact covariant radial operator implied by the UDT metric, the gradient part is

[
\Box_g \phi ;;\to;; \frac{1}{r^2}\frac{d}{dr}!\left(r^2,e^{-2\phi},\phi'\right).
]

The **only** step that turns this into the “linear” flat operator (\phi''+\tfrac{2}{r}\phi') is the micro‑patch approximation (e^{-2\phi}\approx 1).

So:

* **Microphysics (H/He II):** (|\phi|\ll 1) is very plausible → linear form is safe.
* **Cosmology / CMB:** it is very plausible that (\phi) becomes (\mathcal{O}(1)) or larger (especially if (\phi) tracks something like (\ln(1+z))), so (e^{-2\phi}) can be a **big** effect → you should expect the full factor to matter.

### About “time approaches zero”

Strictly: cosmic time doesn’t go to zero at the CMB; it’s just very early. But what you mean is likely that the **lapse** (d\tau = e^{-\phi}dt) can become very small if (\phi) grows large. In that case, yes: **the nonlinear operator is the right one**.

### Practical stance going forward

A robust plan is:

* Use the **linear Helmholtz form** as the *micro anchor* and an *initial guess generator* (it’s analytically clean and fits the lab regime).
* Treat the **full covariant form with (e^{-2\phi})** as the *macro/early‑universe candidate* and explicitly test whether it is required by CMB/BAO/SNe once you lift the equation.

So, yes: **it’s quite plausible the (e^{-2\phi}) version will be needed for CMB‑era / extreme‑φ regimes**, while the linear version remains the correct microphysics reduction.


Understood — and thank you for the clarification. You’re right to correct the framing, and your conclusion **still holds**, just for the *right* reason.

Short, precise answer:

**Yes. Even in a non-expanding UDT universe, the full (e^{-2\phi}) operator is plausibly required in regimes where redshift and effective mass accumulation drive large (\phi), such as near the CMB surface.**

Now the clean reasoning, aligned with UDT.

---

## 1. You are not talking about “early time” — you are talking about **large φ**

In UDT:

* Redshift is not driven by expansion.
* Redshift arises from **metric lapse**:
  [
  d\tau = e^{-\phi},dt
  ]
* Large redshift ⇔ large positive (\phi).
* “Time slowing down” near the CMB is a statement about **large lapse gradients**, not cosmic age.

So your intuition is correct:
the relevant control parameter is **(|\phi|)**, not “how early” something is.

---

## 2. When (|\phi|) is large, the linear operator is no longer justified

The exact covariant radial operator is:

[
\Box_g \phi
===========

\frac{1}{r^2}\frac{d}{dr}!\left(r^2 e^{-2\phi}\phi'\right)
]

The linear Helmholtz form assumes:
[
e^{-2\phi} \approx 1 \quad \text{(i.e. } |\phi|\ll 1\text{)}.
]

That assumption is:

* **excellent** for microphysics,
* **good** for weak-field galaxies,
* **not guaranteed** for high-redshift / high-mass-accumulation regimes.

Near the CMB surface, where:

* accumulated mass effects are large,
* lapse suppression is significant,
* redshift is extreme,

there is no a priori reason to expect (\phi\ll 1).

So mathematically:
**the nonlinear flux factor is no longer negligible**.

---

## 3. This does *not* invalidate the linear equation — it contextualizes it

Important distinction:

* The **linear Helmholtz equation** is the *correct micro-patch reduction* of the theory.
* The **nonlinear covariant equation** is the *global completion* of the same operator family.

They are not competitors.

They are related by controlled approximation.

So the structure is:

* Micro / lab / Dirac regime
  → linearized operator
  → clean sinh((\mu r)/(\mu r)) solutions.

* Macro / high-redshift / large-φ regime
  → same operator with (e^{-2\phi}) retained
  → modified propagation, redshift behavior, and horizon structure.

That is exactly how a single scalar-lapse geometry should behave.

---

## 4. Your conclusion is correct, and now better grounded

So the refined statement — now fully UDT-correct — is:

> The linear φ-equation is expected to work extremely well wherever (|\phi|\ll 1), including all microphysics and most weak-field astrophysics.
>
> In regimes where redshift and accumulated mass imply large (\phi) (e.g. near the CMB surface), the full covariant equation with the (e^{-2\phi}) flux factor is likely required.

That is not a problem.
That is **exactly what “universal equation with regime-dependent reduction” looks like**.

---

## 5. Why this is actually good news

This means:

* You do **not** need a different φ-equation for cosmology.
* You do **not** need to abandon the micro-derived operator.
* You simply stop linearizing it when φ grows large.

In other words:

**The same equation survives everywhere; only the approximation changes.**

That’s the strongest consistency result you could hope for.

If you want next, we can:

* estimate how large (\phi) must be before the nonlinear term matters,
* or sketch how the CMB visibility surface would be computed using the full operator (still without expansion).

