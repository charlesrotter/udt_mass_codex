# From founding positional dilation to UDT dynamics — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | grok at 64af120 |
| Mode | Analytic DERIVE + self-CAS; DATA-BLIND |
| Exposure | DISCLOSED, not cold: prior repository action work was visible and is audited rather than inherited |
| MAP frozen first | UDT_FOUNDING_TO_DYNAMICS_MAP.md, SHA-256 a2b67b1f4d55502e7989946a09e2ab50488522cc2a4e14cdd6b421790dc383b5 |
| Symbolic verifier | verify_udt_founding_to_dynamics.py — **24/24 checks pass**, SymPy 1.13.3 |
| GPU | Not used and not needed |
| Independent verification | **OPEN**; cold verification dispatch supplied separately |
| Build-on grade | **PROVISIONAL ANALYTIC RESULT**, not banked and not canon |

Observer-dependent gravitational-mass amplification is excluded. The historical round-\(S^2\)
carrier is used only conditionally and remains reopened. WR-L is unchanged.

## 0. Result

\[
\boxed{
\begin{gathered}
\text{The founding positional-dilation postulate determines kinematic metric relations,}\\
\text{but it does not determine what functional UDT extremizes or what dynamical quantity it
conserves.}\\
\text{Even after locality/covariance choices are added, an allowed nonlinear action family
remains.}\\
\text{Carrier covariance fixes a conditional stress tensor, not the geometric operator or
finite-cell charge.}
\end{gathered}}
\]

The exact status is:

- **Q1 — dynamical completion:** **UNDERDETERMINED**. Action existence, independent fields,
  variation class, measure, derivative order, and boundary functional are not fixed.
- **Q2 — carrier completion:** **CONDITIONAL MINIMAL branch plus ALLOWED FAMILY**. A clean
  physical-metric completion exists after extra premises, but the flat-static \(E_2+E_4\) energy
  does not select its time sector or source coupling uniquely.
- **Q3 — finite-cell mass:** **OPEN**. The finite-cell parity fixes a boundary value, not a
  boundary generator or charge normalization.
- **\(M_N=2E_4=E_2+E_4\):** reproduced exactly under the existing conditional unrestricted-metric
  action, but not promoted to native UDT.

This is not a failure to perform the derivation. It is the derivation’s forcedness result.

## 1. Kinematics defines admissible configurations, not their dynamics

R1/R2/R3 give, in a gradient-adapted frame,

\[
g_{tt}=-e^{-2\phi}c^2,\qquad
g_{\parallel\parallel}=e^{2\phi}.
\]

Write the resulting kinematic restriction schematically as

\[
C[g,\phi]=0.
\]

This says which metric components are mutually admissible. It does not supply a map

\[
\text{history}\longmapsto S[\text{history}]
\]

or an update law. In particular,

\[
C[g,\phi]=0
\quad\not\Rightarrow\quad
\delta S[g,\phi]=0
\]

for any distinguished \(S\).

The missing information is not merely a coefficient. The foundation leaves open:

- the transverse metric and shift;
- whether \(\phi\) is an independent scalar, a metric coordinate, or a constrained variable;
- whether the full metric is varied or reciprocity is built in before variation;
- locality, measure, derivative order, time sector, and boundary functional.

Therefore a full covariant variation cannot be written without first selecting structures the
postulate presently leaves free.

## 2. Explicit nonlinear counterfamily

The underdetermination persists even after adding a generous conditional completion. Choose:

- a local metric or spatial metric \(\mathcal G^{AB}\);
- its invariant measure \(d\mu\);
- \(\phi\) as a scalar on that chosen configuration space;
- an action depending only on first derivatives and respecting \(\phi\mapsto\phi+C\).

Using the working length \(X\), define

\[
Y=X^2\mathcal G^{AB}\nabla_A\phi\nabla_B\phi,
\]

and the exact nonlinear family

\[
\boxed{
S_F[\phi]
=\int d\mu\,X^{-2}F(Y).
}
\]

Its full Euler operator is

\[
\boxed{
\nabla_A\left(2F_Y\nabla^A\phi\right)=0.
}
\]

Two explicit analytic, reversal-even members are

\[
F_1(Y)=\frac12Y,
\qquad
F_2(Y)=\frac12Y+\frac{\alpha}{4}Y^2.
\]

They obey the same R1 shift rule and the same chosen covariance/locality assumptions, but give

\[
\nabla_A\nabla^A\phi=0,
\]

versus

\[
\nabla_A\left[
\left(1+\alpha X^2\nabla_B\phi\nabla^B\phi\right)\nabla^A\phi
\right]=0.
\]

These are distinct full nonlinear operators for every nonzero \(\alpha\). The second member is not
proposed as UDT physics; it is a countermodel to uniqueness. No founding or derived premise fixes
\(\alpha=0\) or forbids the higher power.

This establishes:

\[
\boxed{
\text{R1/R2/R3 plus locality and covariance still do not select a unique bulk functional.}
}
\]

Other choices—higher derivatives, a bilocal relational action, or no action principle—widen the
space further. They are not needed for the proof.

## 3. What can be conserved, conditionally

For the chosen shift-invariant \(S_F\), the conditional bulk current is

\[
J^A=2F_Y\nabla^A\phi,
\qquad
\nabla_AJ^A=0
\]

on solutions. Different \(F\) gives a different current constitutive law.

This does not yet give UDT a native conserved charge:

1. R1 may be a common-depth gauge redundancy rather than a physical global symmetry.
2. The static finite-cell seal imposes \(\phi=0\). A common shift
   \(\phi\mapsto\phi+C\) does not preserve that fixed boundary representative.
3. The normal derivative at the seal is free, so the boundary flux is not set to zero.
4. For a time-live region,
   \[
   \frac{dQ_\phi}{dt}=-\oint_{\partial\Sigma}J^i\,dS_i,
   \]
   and no current conservation follows without a boundary rule fixing or cancelling the flux.

Thus:

\[
\boxed{
\text{dilation current = CONDITIONAL on an action and boundary symmetry;
native global dilation charge = OPEN.}}
\]

Within the conditional \(S^2\) carrier model, Hopf class is topologically preserved under smooth
fixed-boundary evolution. That is a property of the chosen carrier configuration space, not a
dynamical conservation law derived from positional dilation.

## 4. The static carrier does not fix its time-live action

Given the historical round-\(S^2\) carrier, the strongest minimal spacetime completion is

\[
S_m^{\rm cov}
=-\int d^4x\sqrt{-g}\left[
\frac{\xi}{2}g^{\mu\nu}\partial_\mu\mathbf n\cdot\partial_\nu\mathbf n
+\frac{\kappa_4}{4}F_{\mu\nu}F^{\mu\nu}
\right].
\]

This is unique only after CHOOSING:

- a four-dimensional local scalar action;
- full physical-metric coupling;
- no foliation field or extra carrier invariant;
- the stated derivative inventory;
- no explicit \(\phi\)-dependent weights.

Those premises are not consequences of the flat-static energy.

For example, after choosing a unit clock/foliation field \(u^\mu\), the family

\[
S_m^{(\alpha_2,\alpha_4)}
=\int d^4x\,N\sqrt\gamma\left[
\frac{\alpha_2\xi}{2}|u^\mu\partial_\mu\mathbf n|^2
+\frac{\alpha_4\kappa_4}{2}
\gamma^{ij}(u^\mu F_{\mu i})(u^\nu F_{\nu j})
-\rho_2-\rho_4
\right]
\]

has the same flat-static \(E_2+E_4\) for every \(\alpha_2,\alpha_4\), because all time terms vanish
when the carrier is static. The cold foundation does not supply \(u^\mu\) or select the coefficients.
Full local Lorentz/spacetime covariance would select a particular recombination, but adopting that
as the carrier-action principle is itself the missing premise.

Likewise, on the branch where R1 constrains the metric comparison but is **not** separately imposed
as an exact bulk-action shift, adapted-frame weights \(W_2(\phi)\) and \(W_4(\phi)\) with
\(W_2(0)=W_4(0)=1\) reproduce the supplied flat-static reference while changing backreaction away
from \(\phi=0\). Exact bulk R1 would restrict such weights, but that is itself an additional branch
and still would not select the time coefficients or geometric action. Calling
\(W_2=W_4=1\) “minimal” is therefore a legitimate conditional choice, not a derivation from the
static functional.

\[
\boxed{
\text{Static \(E_2+E_4\) does not determine time derivatives, lapse dependence, or source variation.}
}
\]

## 5. What carrier covariance does derive—conditionally

Under the minimal physical-metric completion, on a static slice define

\[
X_n=D_i\mathbf n\cdot D^i\mathbf n,
\qquad
Y_n=F_{ij}F^{ij},
\]

\[
\rho_2=\frac{\xi}{2}X_n,
\qquad
\rho_4=\frac{\kappa_4}{4}Y_n.
\]

Metric variation gives

\[
S_{ij}^{(2)}
=\xi\left(D_i\mathbf n\cdot D_j\mathbf n-\frac12\gamma_{ij}X_n\right),
\]

\[
S_{ij}^{(4)}
=\kappa_4\left(F_i{}^kF_{jk}-\frac14\gamma_{ij}Y_n\right).
\]

In three spatial dimensions,

\[
S_2=-\rho_2,\qquad S_4=+\rho_4,
\]

so

\[
\boxed{\rho+S=2\rho_4.}
\]

This algebra is exact and is the successful part of the carrier-covariance route. It derives the
stress combination **given** the carrier and physical-metric action.

It does not determine which geometric equation contains that combination.

## 6. Reciprocal tangent variation is not unrestricted lapse variation

This is the decisive variation-domain result.

In the constrained reciprocal metric, an allowed \(\phi\) variation changes the clock and parallel
length together:

\[
\delta g_{tt}=-2g_{tt}\,\delta\phi,
\qquad
\delta g_{\parallel\parallel}
=2g_{\parallel\parallel}\,\delta\phi.
\]

Therefore the carrier contribution to the \(\phi\) equation is proportional to

\[
-T^t{}_t+T^\parallel{}_\parallel
=\rho+p_\parallel.
\]

Decompose the carrier energy into channels containing the parallel direction:

\[
\rho_{2\parallel}
=\frac{\xi}{2}|D_\parallel\mathbf n|^2,
\]

\[
\rho_{4\parallel}
=\frac{\kappa_4}{2}
\sum_{a\perp\parallel}F_{\parallel a}^2.
\]

Direct algebra gives

\[
\boxed{
\rho+p_\parallel
=2\left(\rho_{2\parallel}+\rho_{4\parallel}\right).
}
\]

The same result follows by substituting

\[
N=e^{-\phi},
\qquad
\sqrt{\gamma_\parallel}=e^\phi.
\]

The static measure \(N\sqrt\gamma\) is \(\phi\)-independent; only carrier contractions containing
the parallel inverse metric vary. Purely transverse channels do not source this tangent equation.

By contrast, the conditional lapse identity uses the full spatial trace:

\[
\rho+S=2\rho_4.
\]

For a general three-dimensional H3 carrier,

\[
\rho+p_\parallel
\ne
\rho+S.
\]

No symmetry or virial identity in the foundation equates the pointwise directional energy
\(\rho_{2\parallel}+\rho_{4\parallel}\) with the full \(\rho_4\).

Hence:

\[
\boxed{
\begin{gathered}
\text{vary reciprocal metric first}\ \Rightarrow\ \rho+p_\parallel,\\
\text{vary unrestricted metric and derive lapse equation}\ \Rightarrow\ \rho+S,\\
\text{the two routes are not equivalent without an additional theorem or premise.}
\end{gathered}}
\]

Carrier covariance therefore does not let the static mass readout bypass Q1. It supplies a
conditional stress tensor, but the variation domain still decides which stress combination sources
geometry.

## 7. The \(M_N=2E_4\) consistency test

Under the separate CONDITIONAL premises:

1. unrestricted four-dimensional metric variation;
2. local metric-only two-derivative geometric minimality;
3. the corresponding EH-form bulk action and finite boundary normalization;
4. minimal physical-metric carrier coupling;
5. staticity;

the lapse equation is

\[
D^2N=\frac{\kappa_gN}{2}(\rho+S).
\]

Using the carrier identity above,

\[
D^2N=\kappa_gN\rho_4.
\]

The divergence theorem and the chosen normalization give

\[
M_N
=\frac{2}{\kappa_g}\oint D_iN\,dS^i
=2\int N\rho_4\,dV.
\]

In weak backreaction \(N=1+O(\kappa_g)\), while three-dimensional stationary scaling gives

\[
E(\lambda)=\lambda E_2+\lambda^{-1}E_4,
\qquad
\left.\frac{dE}{d\lambda}\right|_{\lambda=1}=0
\Longrightarrow E_2=E_4.
\]

Consequently,

\[
M_N=2E_4+O(\kappa_g)=E_2+E_4+O(\kappa_g).
\]

The mandatory consistency test is therefore classified as:

| Branch | Result |
|---|---|
| Conditional unrestricted metric + minimal carrier | **REPRODUCED exactly** at the lapse-identity level |
| Reciprocal constrained variation | **SYSTEMATICALLY DIFFERENT source:** \(\rho+p_\parallel\) |
| Founding positional dilation without a geometric action | **CANNOT FORM \(M_N\):** operator and boundary normalization absent |

The identity remains a strong conditional result. It is not a native theorem of R1/R2/R3.

## 8. Finite-cell parity does not select a charge

Take the exact one-dimensional finite-cell model

\[
L_0=\frac{Z}{2}(\phi')^2.
\]

For any constant \(a\),

\[
L_a=L_0+\frac{d}{dr}(a\phi)
=\frac{Z}{2}(\phi')^2+a\phi'.
\]

Both give the same bulk equation,

\[
Z\phi''=0,
\]

but their endpoint momenta are

\[
p_0=Z\phi',
\qquad
p_a=Z\phi'+a.
\]

At the odd Dirichlet seal, \(\phi=0\) and \(\delta\phi=0\), so both actions are differentiable there
and parity does not select \(a\). Thus the raw boundary flux can be shifted without changing the
bulk dynamics or the stated boundary value.

Likewise, adding \(d(\gamma r)/dr\) leaves the bulk equation unchanged while shifting the endpoint
Hamiltonian used in a movable-wall condition.

\[
\boxed{
\text{finite-cell value/parity data do not determine the boundary primitive or mass generator.}
}
\]

A native finite-cell charge requires the complete action including its distinguished boundary
functional and allowed endpoint variations.

## 9. \(X\) is not yet a dynamical eigenvalue

The working universal \(X\) supplies a global ruler and asymptotic structure. It does not by itself
define:

- which configurations are compared at fixed \(X\);
- whether \(X\) is varied;
- the native total mass;
- the boundary transversality equation;
- a second independent relation if \(c\) and \(X\) are joint outputs.

The dimensional expressions

\[
X=\beta\frac{GM_{\rm total}}{c^2},
\qquad
c^2=\beta\frac{GM_{\rm total}}X
\]

remain one equation. No action means no eigenvalue problem that could determine \(\beta\), \(c\),
or \(X\).

## 10. Answers to the central lay question

### What does a UDT configuration extremize?

\[
\boxed{\text{Nothing unique has yet been derived from the founding postulate.}}
\]

The corrected H3 carrier extremizes the **chosen conditional static**
\(E_2+E_4\) functional. WR-L satisfies its separate residual/wall selector. Neither fact identifies
the full UDT dynamical action.

### What does UDT conserve?

- Dilation flux: **conditional** on a selected shift-invariant action and boundary treatment.
- Hopf class: **conditional topological property** of the reopened \(S^2\) carrier under smooth
  fixed-boundary evolution.
- Finite-cell gravitational mass/charge: **OPEN**.
- A universal whole-system energy: **not yet defined natively**.

## 11. Status ledger

| Claim | Status |
|---|---|
| R1/R2/R3 determine reciprocal metric kinematics | **DERIVED with recorded regularity/P8 qualifications** |
| They force an action principle | **NOT DERIVED** |
| They force a unique local action after covariance choices | **FALSIFIED by exact counterfamily** |
| Bulk shift current exists | **CONDITIONAL on selected action** |
| Global dilation charge exists in finite cell | **OPEN; boundary flux/primitive unresolved** |
| Physical-metric \(S^2\) carrier stress | **DERIVED given conditional carrier action** |
| Carrier covariance fixes full backreaction | **NO; geometric operator and variation class remain open** |
| Reciprocal tangent source | **DERIVED conditionally:** \(\rho+p_\parallel\) |
| Unrestricted lapse source | **DERIVED under separate conditional action:** \(\rho+S=2\rho_4\) |
| The two source routes are equivalent | **NOT DERIVED; generally unequal** |
| \(M_N=2E_4\) | **CONDITIONAL-DERIVED**, not native |
| Native finite-cell charge | **OPEN due boundary-functional ambiguity** |
| \(S^2\) is fundamental | **REOPENED** |
| Observer-dependent mass amplification | **QUARANTINED** |
| \(X,c,M_{\rm total}\) closure | **OPEN** |

## 12. Smallest missing founding content

The derivation does not ask for another detailed mechanism. It identifies a short list of logical
inputs without which dynamics cannot be unique:

1. **Dynamical principle:** action, update rule, or another extremization statement.
2. **Off-shell configuration space:** constrained reciprocal metric versus unrestricted metric.
3. **Covariance/locality/order rule:** what invariants and derivatives are admissible.
4. **Boundary principle:** the distinguished finite-cell primitive and allowed variations.
5. **Carrier decision:** whether matter emerges, remains an independent carrier, or is replaced.

If UDT adopts the conditional unrestricted-metric, local, two-derivative minimality package, the H3
mass chain is already available. If it does not, a different geometric action must be derived before
mass can be defined. The present postulates do not decide between those branches.

\[
\boxed{
\text{Kinematics is established. Dynamics remains underdetermined at one precise seam:
the native variational principle.}
}
\]
