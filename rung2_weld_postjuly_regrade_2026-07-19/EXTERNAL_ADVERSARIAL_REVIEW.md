# Fresh Adversarial Review — Rung-2 Weld Regrade

Date: 2026-07-19

Mode: fresh read-only context; independent CPU scratch under `/tmp`; no repository edits

Verdict: `PASS_AFTER_TWO_EVIDENCE_WORDING_CORRECTIONS`

## Independent linear-curvature result

Using direct full-metric epsilon differentiation rather than the package's first-variation routine,
the reviewer obtained

\[
\delta R_{t\theta}
=\frac12\left[(fH_1)_{,r}-K_{,t}-2p_{,t}\right]Y_{,\theta},
\]

and therefore

\[
\delta G^t{}_{\theta}
=\frac1f\left[-\frac12(fH_1)_{,r}+p_{,t}+\frac12K_{,t}\right]Y_{,\theta}.
\]

The coefficient and sign structure exactly match `DERIVATION_RESULT.json`. Equating the expression
to `8 pi G tau Y_theta` gives

\[
(fH_1)_{,r}=2p_{,t}+K_{,t}-16\pi Gf\tau.
\]

The reviewer agreed with the controlling provenance distinction: the tensor expression is geometry;
the displayed differential equation requires the imported Einstein/source premise.

## Independent scalar-action result

The reviewer independently expanded the June-10 action and found its complete `H1`-dependent
quadratic density

\[
\mathcal L_2|_{H_1}
=c_*r^2\left(\frac14f^2\phi_0'^2H_1^2-f\phi_0'H_1p_t\right),
\]

so

\[
\frac{\delta S_2}{\delta H_1}
=\frac{c_*r^2f\phi_0'}2\left(f\phi_0'H_1-2p_t\right).
\]

Thus `f phi0' H1=2 p_t` follows only when `phi0' != 0`; at `phi0'=0`, the undivided equation
degenerates to `0=0`. The reviewer confirmed that current C0/C1 supplies no such action/EOM and the
complete action remains open. The package's historical/pre-native regrade is therefore correct.
Omitted angular-gradient terms at this order are `H1`-independent and do not alter this conclusion.

## Independent exact Petrov check

A separate static-lapse/3+1 calculation used

\[
E_{ij}=\frac{D_iD_jN}{2N}+\frac12{}^{(3)}R_{ij}
-\frac{h_{ij}D^2N}{6N}-\frac16h_{ij}{}^{(3)}R
\]

and reproduced

\[
E^i{}_j=
\begin{pmatrix}
-1/75&-\sqrt2/20&0\\
-\sqrt2/20&-7/75&0\\
0&0&8/75
\end{pmatrix},
\]

with characteristic polynomial

\[
\frac{(75\lambda-8)(45000\lambda^2+4800\lambda-169)}{3375000}
\]

and discriminant

\[
11913/1250000000\ne0.
\]

For the static zero-shift metric, `K_ij=0`, so the magnetic Weyl tensor vanishes. Three distinct
electric-Weyl eigenvalues imply Petrov I. The reviewer also confirmed that `G^t_theta=0` follows
identically from staticity, not from a field equation.

## K and causal-scope audit

The `K=0` correction passed. The old calculation shows that eliminating `K` while retaining the
restricted Regge–Wheeler form generates an omitted `g_{r theta}` component. It does not establish
that current UDT excludes angular trace or shear.

The reviewer caught that the original four-class counterjet tables classify `dp`, not the total
`d(phi0+epsilon pY)`. Before banking, the package was corrected to label the rows as perturbation
first-jets and to add the exact old-action vacuum background

\[
f=1+C/r,\qquad \phi_0=-\tfrac12\log f,
\]

which has `E0=0`, satisfies both trivial-perturbation weld residuals, and has

\[
g^{-1}(d\phi_0,d\phi_0)=C^2/[4r^3(C+r)]>0.
\]

The exact static angular Petrov-I witness supplies a second nonzero spacelike total-gradient case.

## Required corrections and disposition

1. **Stale derivation transcript:** corrected. It was regenerated after the scalar-action,
   full-gradient, and static-Petrov checks were added. The verifier now compares the normalized
   transcript body byte-for-byte with a fresh derivation stdout replay.
2. **Perturbation versus total-gradient wording:** corrected in the JSON, report, ledgers, and
   verifier; the full-gradient historical vacuum witness was added.

No further scientific correction was required. The reviewer made no repository edits.
