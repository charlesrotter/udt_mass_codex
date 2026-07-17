# WR-L off-shell action provenance — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic DERIVE + adversarial inverse-variational audit |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| MAP | `UDT_WRL_OFFSHELL_PROVENANCE_MAP.md`, SHA-256 `44dd0059c40be3f612e32b03bf8ac6487410401cb3d810c221869f309e64527a` |
| Driver | DISCLOSED NON-COLD; the target WR-L ODE was known |
| Symbolic verifier | `verify_udt_wrl_offshell_provenance.py` — **28/28 checks pass**, SymPy 1.13.3 |
| GPU | Not used; no determined numerical problem emerged |
| Independent verification | **OPEN** |
| Build-on grade | **PROVISIONAL NEGATIVE ON UNIQUENESS / POSITIVE INVERSE LEAD**, not banked |

No GR field equation, EH premise, carrier, observed mass, fit, cutoff, or invented physical coupling
is used.

## 0. Result

The next analytic step is decisive:

\[
\boxed{
\begin{gathered}
\mathcal I_0[A]
=\frac12\int dr\left[r(A')^2+\frac{(A-1)^2}{r}\right]
\text{ is conditionally unique in the narrow quadratic radial class;}\\
\text{it is not unique in the general local, scale-free, first-derivative class.}
\end{gathered}}
\]

An explicit one-parameter counterfamily exists.  Let

\[
B=A-1,
\qquad
F_B=B''+\frac{B'}r-\frac{B}{r^2},
\]

and define

\[
L_0=\frac12\left[r(B')^2+\frac{B^2}{r}\right],
\]

\[
L_6=
\frac{r^5(B')^6}{480}
-\frac{r^3B^2(B')^4}{96}
+\frac{rB^4(B')^2}{32}
+\frac{B^6}{96r}.
\]

For every dimensionless \(\lambda>0\),

\[
L_\lambda=L_0+\lambda L_6
\]

has Euler expression

\[
\boxed{
E[L_\lambda]
=r\left[1+\frac{\lambda}{16}left(B^2-r^2(B')^2\right)^2\right]F_B.
}
\]

The multiplier is strictly positive for (r>0).  Therefore every (L_\lambda) has **exactly the
same bulk Euler equation and the same WR-L solution**, with no extra solution branch caused by a
vanishing multiplier.  The family is not related by overall normalization or first-order total
derivatives because

\[
\frac{\partial^2L_\lambda}{\partial(B')^2}
=r\left[1+\frac{\lambda}{16}left(B^2-r^2(B')^2\right)^2\right]
\]

depends nontrivially on the field and derivative.

Most importantly, the boundary momentum changes even though the metric equation does not.  On

\[
B_{\rm WR-L}=-r/X,
\]

\[
\mathcal I_\lambda[A_{\rm WR-L}]
=\frac12+\frac{\lambda}{180},
\qquad
p_\lambda(X)
=\frac{\partial L_\lambda}{\partial B'}\bigg|_{X}
=-1-\frac{\lambda}{30}.
\]

Thus the WR-L solution space cannot determine a unique action value, boundary generator, or mass
normalization.  That missing information is genuinely off shell.

The honest verdict is:

\[
\boxed{
\text{The metric exposed the correct inverse-action seed, but the solution alone cannot select it.}
}
\]

## 1. Residual re-centering is on-shell, not an off-shell action symmetry

Let

\[
F_r[A]=r^2A''+rA'-A+1
\]

and

\[
A_R(s)=\frac{A(R+s)}{A(R)},
\qquad y=R+s.
\]

Direct substitution gives

\[
\boxed{
A(R)F_s[A_R]
=F_y[A]
-R(2s+R)A''(y)-RA'(y)+A(R)-1.
}
\]

The extra terms do not vanish for a general off-shell field.  Hence the WR-L Euler operator is not
covariant under residual re-centering on the entire configuration space.

The general stationary solution is

\[
A=1+a r+\frac br.
\]

After re-centering,

\[
F_s[A_R]
=\frac{b s^2(3R+s)}{(R+s)^3(R^2a+R+b)}.
\]

Only the bounded-seat branch (b=0) is closed.  That is enough for the physical WR-L solution
family, but it is on-shell closure after a boundary selection, not an off-shell symmetry principle
that can select an action.

The action itself fails the stronger test.  Use the fixed-endpoint perturbation, with (X=1),

\[
A_\epsilon(r)=1-r+\epsilon r(1-r).
\]

Then

\[
\mathcal I_0[A_\epsilon]=\frac{\epsilon^2+4}{8}.
\]

Re-center at (R) and integrate over the remaining interval (0<s<1-R).  Exact algebra gives

\[
\mathcal I_0[A_{\epsilon,R}]
=\frac{5R^2\epsilon^2-2R\epsilon^2+8R\epsilon+\epsilon^2+4}
{8(1+R\epsilon)^2},
\]

and

\[
\mathcal I_0[A_{\epsilon,R}]-\mathcal I_0[A_\epsilon]
=-\frac{R\epsilon^2(1+\epsilon)(R\epsilon-R+2)}{8(1+R\epsilon)^2}.
\]

This is nonzero off shell and vanishes at \(\epsilon=0\), the exact WR-L profile.  Because all
fields have the same fixed endpoint values in this comparison, the \(\epsilon\)-dependent difference
cannot be removed by a value-only total derivative.  The invariance is on shell only.

## 2. What is conditionally unique

Consider the named quadratic class

\[
L_Q
=\frac12p(r)(B')^2+\sigma(r)BB'+\frac12q(r)B^2.
\]

Its exact Euler expression is

\[
E[L_Q]
=pB''+p'B'+(\sigma'-q)B.
\]

The mixed term is only a boundary term plus a potential shift:

\[
\sigma BB'
=\frac{d}{dr}\left(\frac12\sigma B^2\right)
-\frac12\sigma'B^2.
\]

Requiring the WR-L equation up to a nonzero multiplier fixes

\[
\frac{p'}p=\frac1r,
\qquad
p=Cr,
\qquad
q-\sigma'=\frac Cr.
\]

Therefore

\[
L_Q
\simeq
C L_0,
\]

where \(\simeq\) means equality up to the displayed total derivative.  This proves:

\[
\boxed{
\mathcal I_0\text{ is unique up to normalization and boundary improvement only if the action is
postulated to be quadratic in }B,B'.
}
\]

Quadraticity is not currently derived by positional dilation, reciprocity, or wall regularity.  It
would be a new off-shell simplicity principle unless independently obtained.

## 3. The counterfamily is a strict nonuniqueness theorem

The (L_\lambda) family above has all of the properties that made (L_0) initially attractive:

- local in (r,A,A');
- first differential order;
- no fitted datum or physical cutoff;
- scale-free;
- full nonlinear dependence retained;
- regular Legendre Hessian for (r>0,lambda>0);
- exactly the same Euler equation, not merely the same one selected solution.

Yet its action value and endpoint momentum differ.  Therefore adding the requirements “local,”
“scale-free,” “first derivative,” and “same WR-L equation” does not select (L_0).

The family is a logical countermodel, not a proposal that sixth-power derivative terms are physical.
Its job is to prove that an additional UDT rule must exclude them.  Choosing “the lowest polynomial
degree” would select (L_0), but that is a CHOSE minimality rule until derived.

## 4. Global depth scaling can be restored, but it does not restore uniqueness

The seat-normalized equation is not invariant under a raw depth scaling (A\mapsto kA):

\[
F_r[kA]=kF_r[A]+1-k.
\]

That is expected because (A(0)=1) is already a gauge/reference choice.  Introduce an explicit
reference residual (A_0) and define

\[
\mathcal I_{\rm rel}[A,A_0]
=\frac1{2A_0^2}\int_0^X
\left[r(A')^2+\frac{(A-A_0)^2}{r}\right]dr.
\]

It is invariant under

\[
A\mapsto kA,
\qquad A_0\mapsto kA_0,
\]

and gives

\[
r^2A''+rA'-A+A_0=0.
\]

With (A(0)=A_0, A(X)=0),

\[
A=A_0(1-r/X),
\qquad
\mathcal I_{\rm rel}=\frac12.
\]

This is a clean **CONSTRUCTED relational completion**.  It requires (A_0), its boundary meaning,
and its variation class.  More decisively, writing

\[
B=\frac{A}{A_0}-1
\]

restores the entire (L_\lambda[B]) counterfamily while preserving simultaneous depth scaling.
Thus global depth covariance does not select \(\lambda=0\).

## 5. The obvious geometric parent still fails

The parent audit identified

\[
\mathcal J[N;\gamma]
=\frac12\int_\Sigma
\left[(DN)^2-\frac14{}^{(3)}R\,N^2\right]dV.
\]

Holding (gamma) fixed while varying (N) gives the WR-L lapse identity.  But reciprocity ties

\[
\gamma_{rr}=N^{-2}.
\]

After substituting this relation and varying the actual one-field reciprocal functional,

\[
E_N\big|_{N=\sqrt{1-r/X}}
=\frac{r(5r-6X)}{8X(X-r)}\ne0.
\]

Therefore this (\mathcal J) is not the required one-field UDT parent.  It could be used only by
declaring (N) and (gamma) independent off shell and then adding a constraint prescription.  That
is extra action structure, not a consequence of the metric solution.

No theorem here excludes every possible covariant or UDT-foliated parent.  What is proved is that
the presently visible parent fails and that any successful parent must also explain why its
off-shell field space and boundary generator eliminate the (L_\lambda) ambiguity.

## 6. Status ledger

| Claim | Status |
|---|---|
| WR-L equation closed under re-centering on the regular linear solution branch | **DERIVED** |
| WR-L equation is off-shell re-centering covariant | **FALSE** |
| \(\mathcal I_0\) is off-shell re-centering invariant | **FALSE** |
| \(\mathcal I_0\) unique inside the named quadratic class | **CONDITIONAL-DERIVED** |
| \(\mathcal I_0\) unique among local scale-free first-derivative actions | **FALSE** |
| Strictly nondegenerate (L_\lambda) family with identical bulk equation | **DERIVED counterexample** |
| Same bulk equation fixes boundary momentum/mass generator | **FALSE** |
| Reference residual restores simultaneous depth scaling | **DERIVED for the constructed completion** |
| Depth scaling removes the (L_\lambda) ambiguity | **FALSE** |
| Fixed-(gamma) curvature-lapse functional is a reciprocal one-field parent | **FALSE** |
| Unique native UDT action | **OPEN / not derived** |

## 7. What the missing constraint now is

The missing information is not another solution-space boundary value.  The solution space cannot
distinguish actions that have identical Euler equations.

UDT needs one genuinely off-shell principle, for example a derivation of one of the following—not
an arbitrary adoption:

1. **quadratic infinitesimal dilation cost** in a derived measure;
2. a covariant/foliated parent whose allowed invariant inventory truncates uniquely at (L_0);
3. a canonical boundary generator or symplectic structure that rejects (L_{\lambda\ne0});
4. an independent composition rule acting on off-shell histories, not only solutions.

The owner's statement that positional-dilation cost should be analogous to velocity/acceleration
dilation becomes mathematically decisive here only if that analogy derives a quadratic norm and its
measure.  Without that step, “choose the simplest quadratic action” is a reasonable research lean,
not a UDT theorem.

## 8. Next step

No GPU numerics are warranted.  The next honest operation is independent analytic verification of
the counterfamily and then a focused founding-principle question:

\[
\boxed{
\text{Does UDT require the local cost of an infinitesimal residual change to be a quadratic norm?}
}
\]

If yes and independently justified, (L_0) becomes conditionally selected and its full boundary
variation can be developed.  If not, the native action remains nonunique and numerics would only
solve an arbitrarily chosen member of (L_\lambda).

## 9. Self-audit

- The counteraction is a falsification device, not invented physics.
- No target mass or carrier result was used.
- No linearization was used.
- The field-dependent Euler multiplier and Legendre Hessian are displayed.
- Boundary momenta are compared explicitly; identical bulk equations were not treated as identical
  actions.
- Quadratic conditional uniqueness is not promoted to unconditional UDT truth.
- The failed geometric parent is not rescued by changing its variation after the fact.
- Fresh independent verification remains OPEN.

## 10. Reproduction

In an environment with SymPy 1.13.3:

```bash
python3 verify_udt_wrl_offshell_provenance.py
```

The script checks 28 exact identities.  Passing verifies the encoded algebra, not a choice of native
action.

