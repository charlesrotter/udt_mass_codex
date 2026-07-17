# Workstation dispatch — cold audit of WR-L scaffold/native-action separation

## Scope

Audit the hypothesis proposed by Charles Rotter:

> Perhaps WR-L is a non-native scaffold.

The supplied derivation does not retract WR-L canon `C-2026-07-09-1`. It tests whether WR-L can be
stationary in the complete local physical-metric first-gradient reciprocal-current class

$$
I_F=\int\sqrt{-g}\,F(Y)\,d^4x,
\qquad
Y=\frac12\operatorname{Tr}(J_\mu J^\mu).
$$

Audit only:

- `UDT_WRL_SCAFFOLD_NATIVE_ACTION_SEPARATION_MAP.md`
- `UDT_WRL_SCAFFOLD_NATIVE_ACTION_SEPARATION_DERIVATION_RESULTS.md`
- `verify_udt_wrl_scaffold_separation.py`
- `verify_udt_wrl_scaffold_separation_out.txt`

Do not alter `LIVE.md` or `CANON.md`, demote existing canon, invent a repair action, or start F/G.

## 1. Operator provenance

Starting from

$$
ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2,
$$

derive independently:

$$
\sqrt{-g},
\qquad
Y=e^{-2\phi}(\phi')^2,
\qquad
I_F\propto\int dr\,r^2F(Y).
$$

Confirm that the physical metric, not a fixed background metric, contracts the current.

## 2. Variation-before-substitution gate

Vary arbitrary $F$ with respect to $\phi$ before imposing WR-L. Audit every sign and the reported
equation

$$
\frac{d}{dr}\left(2r^2e^{-2\phi}\phi'F'(Y)\right)
+2r^2YF'(Y)=0.
$$

Check fixed-endpoint boundary terms and state any regularity assumed for $F$ and $\phi$.

## 3. WR-L reduction

Independently compute for

$$
A=1-r/X,
\qquad
\phi=-\tfrac12\ln A:
$$

$$
\phi',
\qquad
A\phi',
\qquad
Y(r),
\qquad
Y'(r),
\qquad
Y(0),
\qquad
\lim_{r\to X^-}Y.
$$

No supplied intermediate expression should be trusted.

## 4. Inverse-action ODE

Set $p(Y)=F'(Y)$ and $z=4X^2Y$. Re-derive and solve

$$
Y(z-1)p'(Y)+\frac{z+3}{2}p(Y)=0.
$$

Audit the claimed solution

$$
p(Y)=C\frac{(4X^2Y)^{3/2}}{(4X^2Y-1)^2}.
$$

Search for missing branches, weak solutions, or integration choices that could yield a nonzero
$C^1$ function at $Y_0=1/(4X^2)$.

## 5. Regularity adversary

Determine precisely:

1. the order of the $F'$ singularity at $Y_0$;
2. the corresponding leading behavior of $F$;
3. whether the weighted on-shell action is finite;
4. whether the first variation and linearized operator are well-defined at the center;
5. whether integrability alone is enough for a native variational law.

The supplied derivation uses a $C^2$ local-action gate. Challenge that gate explicitly rather than
silently changing it.

## 6. $X$ universality

Test whether inverse solutions for $X_1\neq X_2$ can be related by:

- overall action normalization;
- a universal change of variables not containing the solution label;
- a boundary improvement;
- treating $X$ as an integration constant.

Report whether one universal nontrivial $F$ can support more than one WR-L scale.

## 7. Scope adversary

List native action structures not covered by $F(Y)$, but do not propose one solely to rescue WR-L.
Determine whether the exact warranted conclusion is:

- only the quadratic action fails;
- the regular universal $F(Y)$ class fails;
- or every conceivable native UDT action fails.

The last verdict requires a proof far beyond the supplied class.

## 8. Required report

Return:

1. PASS/FAIL for sections 1–7;
2. corrected equations for every failure;
3. raw CAS or symbolic scripts and output;
4. exact regularity classification of the formal inverse $F$;
5. exact $X$-dependence verdict;
6. one final classification:
   - **WR-L NATIVE IN REGULAR UNIVERSAL F(Y)**;
   - **WR-L REQUIRES SINGULAR/X-INSERTED F(Y)**;
   - **SUPPLIED NO-GO INCORRECT**, with counterexample;
7. a separate statement on whether the broader scaffold hypothesis is proved or only strengthened.

Stop after reporting. No canon/frontier rewrite without Charles's explicit verdict.

