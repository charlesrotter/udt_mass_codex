# UDT finite-cell variational principle and boundary generator — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-14 |
| Mode | Analytic DERIVE + self-CAS; DATA-BLIND |
| Driver | **DISCLOSED NON-COLD** — historical fold/action/EH/H3 records were visible |
| MAP frozen first | `UDT_FINITE_CELL_BOUNDARY_MAP.md`, SHA-256 `6b6c8ffa57cabdc0d4a6028b107fda22a1224b4aaaffed0fe74cee9ffaaa5cae` |
| Symbolic audit | `verify_udt_finite_cell_boundary.py` — 23/23 checks pass with SymPy 1.13.3 |
| GPU | Not used; no determined nonlinear problem emerged |
| Independent verification | **OPEN** |
| Build-on grade | **PROVISIONAL CANDIDATE**, not banked and not canon |

**Owner clarification, 2026-07-15:** the \(S^2\) carrier is a historical working posit adopted
after derivation attempts failed, now explicitly **REOPENED**. It may emerge, remain postulated,
or be replaced. See UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md. The frozen MAP remains
unchanged for audit integrity.

**\(X_{\max}\) clarification, 2026-07-15:** existence of one universal unattainable distance is a
WORKING POSIT; whether it is an independent constant or a derived whole-system scale is OPEN. See
UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md.

Primary current sources: `LIVE.md`, `CANON.md`, `UDT_ELEGANT_FRAME.md`, `SIMPLE_METRIC_MACRO.md`,
`simple_metric_L_wall_regularity_closure_results.md`, `node05_seal_parity_regrade_results.md`,
`universe_cell_fold_jc_sigma_results.md`, `native_geometric_action_results.md`,
`r1_route_fork_native_derivation.md`, `d2c_gp_composite_conditions.md`, and the H3 static-mass
dispatch/results. Historical action claims are adjudicated, not presumed current.

## 0. Result

\[
\boxed{
\begin{gathered}
\text{The current UDT premises do not force a unique finite-cell action or native mass charge.}\\
\text{They do force a sharper boundary taxonomy and expose a variation-class obstruction.}
\end{gathered}}
\]

More precisely:

1. The **WR-L macro wall**, the **canonical odd fold**, and the **H3 numerical boundary** are
   different objects. Identifying them is **INCONSISTENT-SCOPE** under their present stamps.
2. The canonical odd fold can be implemented as an exact quotient, a one-copy physical boundary,
   or a matched two-side interface. These produce different admissibility and boundary equations.
3. In the historical round $(Z,\mu)$ action family, an exact odd-depth quotient permits only the
   Branch-G, $\mu=0$ slice. Branch P does not descend under the mirror in a neighborhood of the
   fold.
4. A one-copy boundary with the canonical free flux also selects $\mu=0$ under the standard
   first-order/value-boundary variational class. The historical two-side jump cancellation does
   not establish that one-copy result because it belongs to a different variation class.
5. Boundary primitives and total derivatives change the endpoint momenta or transversality
   equation without changing the bulk Euler equations. No current UDT premise selects the
   physically distinguished primitive.
6. The WR-L profile is neither an extremal nor a finite-action configuration of the live
   shift-clean radial kinetic action. This does not falsify WR-L; it proves that WR-L wall
   regularity has not supplied its dynamics.
7. The H3 lapse/flux identity remains exact under its named **CONDITIONAL** action and carrier
   premises, but it is not promoted to an unconditional finite-cell mass theorem.

The smallest missing object is therefore not another boundary condition. It is a **finite-cell
off-shell action principle with a distinguished boundary primitive and variation class**.

## 1. The three “walls” are not one surface

The canonical static odd fold obeys

\[
\phi(r_s)=0,
\qquad A(r_s)=e^{-2\phi(r_s)}=1,
\]

with $\rho'(r_s)=0$ and $\phi'(r_s)$ free in the historical round-static cell class.

The WR-L macro wall obeys

\[
A(r)=1-\frac{r}{X}\longrightarrow0,
\qquad
\phi(r)=-\frac{1}{2}\ln A\longrightarrow+\infty.
\]

No finite additive re-centering maps $\phi=0$ to $\phi=+\infty$. Moreover the canon audit states
that the WR-L wall is a causal horizon with an interior beyond it, not a hard end of space. It is
therefore not the odd-fold quotient boundary. The H3 pinned/free-mask boundary is a numerical
control and is neither of these.

This is a **DERIVED object-identity result**, not an action verdict. A future construction may
relate the objects through additional geometry, but the relation is not presently supplied.

## 2. What an exact fold quotient requires

Use the recorded general round kinetic family, per angular factor,

\[
L_{P}=\frac{Z}{2}\rho^2\phi'^2+2-2e^{-2\phi}\rho'^2
+2\mu\rho\rho'\phi',
\]

\[
L_{G}=\frac{Z}{2}\rho^2\phi'^2+2-2\rho'^2
+2\mu\rho\rho'\phi'.
\]

Route A is $\mu=0$; the historical Route-B point is $(Z,\mu)=(8,2)$.

At the static odd depth mirror,

\[
I:(\phi,\phi',\rho,\rho')
\mapsto(-\phi,+\phi',\rho,-\rho').
\]

Direct substitution gives

\[
\boxed{I^*L_P-L_P
=-4\sinh(2\phi)\rho'^2-4\mu\rho\rho'\phi',}
\]

\[
\boxed{I^*L_G-L_G=-4\mu\rho\rho'\phi'.}
\]

These defects are quadratic in first derivatives. They cannot be the derivative of a local
value-only primitive $F(\phi,\rho,r)$, whose derivative is at most linear in $\phi',\rho'$.
Allowing a derivative-dependent primitive generically produces second derivatives; eliminating
them returns to the value-only case, up to inert degeneracies.

Consequently, within this local first-order family:

\[
\boxed{
\text{exact odd-fold quotient}
\quad\Longrightarrow\quad
\text{Branch G and }\mu=0.
}
\]

Branch P fails because of the uncompensated $e^{-2\phi}\rho'^2$ term even at $\mu=0$. Route B
also fails in Branch G because its mixing term is mirror-odd. Both defects vanish at the fixed
surface when $\phi=0$ and $\rho'=0$, but equality at one surface is not descent of an action on
a neighborhood.

This does **not** prove that Branch G, $\mu=0$ is the native UDT action. It is a conditional
selection inside the recorded family **if exact off-shell quotient symmetry is adopted**.

## 3. One-copy boundary and two-side matching are inequivalent

For a first-order one-copy action,

\[
\delta S
=\int E_i\delta q^i\,dr
+\left[p_\phi\delta\phi+p_\rho\delta\rho+\delta B\right]_{r_s},
\]

with

\[
p_\phi=Z\rho^2\phi'+2\mu\rho\rho',
\qquad
p_\rho=-4e^{-2\phi}\rho'+2\mu\rho\phi'.
\]

At the odd fold, $\delta\phi=0$ because $\phi$ is odd, while the even field $\rho$ has a free
boundary value. With $\rho'=0$,

\[
p_\phi=Z\rho_s^2\phi'_s,
\qquad
p_\rho=2\mu\rho_s\phi'_s.
\]

Therefore, for a standard value-only $B$ and a genuinely free flux $\phi'_s$,

\[
\boxed{\text{one-copy differentiability}\Longrightarrow\mu=0.}
\]

A derivative-dependent boundary action, an added boundary field, or a boundary law tying
$\phi'_s$ to $\rho_s$ could evade this. Each is an additional action premise and would remove
or modify the statement that the flux is freely output.

The historical matched-mirror calculation instead gives

\[
[p_\rho]=8\cosh(2\phi_s)\rho'_s,
\qquad
[p_\phi]=-4\mu\rho_s\rho'_s.
\]

Thus $\rho'_s=0$ makes both jumps vanish for every $\mu$; this is the known Route-B cancellation.
It is correct as a **two-side matching result**. It does not show that the action descends to an
exact quotient, nor that a one-copy action is differentiable. The prior record moved among these
three readings without possessing a theorem that they coincide.

### Adjudication

- **VM matched interface:** historical cancellation confirmed.
- **VB one-copy physical boundary:** $\mu=0$ selected under the stated standard boundary class.
- **VQ exact quotient:** Branch G and $\mu=0$ selected inside the recorded family.
- Which reading is native is **OPEN**.

## 4. A boundary value does not determine a boundary action

For a movable endpoint $b$, the general first variation may be written

\[
\delta S\big|_b
=(p_i+B_{,i})\,\delta\bar q^i
+(-H+B_{,b})\,\delta b,
\qquad
H=p_iq'^i-L.
\]

Therefore

\[
H=0
\]

is derived only when the endpoint is free, the applicable endpoint fields have their specified
natural/essential variations, and the chosen boundary primitive has $B_{,b}=0$. In general,

\[
H=B_{,b}.
\]

The historical $E_{\rm ang}=2$ transversality result remains valid under its recorded free-endpoint,
integrand-physical, and zero-target boundary posture. It is not a theorem of finite-cell ontology
alone.

The primitive ambiguity is exact. For example,

\[
L\mapsto L+\frac{d}{dr}(\alpha\phi)
\]

leaves every bulk Euler equation unchanged but sends

\[
p_\phi\mapsto p_\phi+\alpha.
\]

At a Dirichlet odd fold, $\delta\phi=0$, so this shift is invisible to endpoint differentiability
there while changing the object one would call the raw dilation flux. Likewise

\[
L\mapsto L+\frac{d}{dr}(\gamma r)=L+\gamma
\]

leaves the bulk equations unchanged but shifts

\[
H\mapsto H-\gamma,
\]

and hence the free-endpoint closure. A full action may compensate these changes with a specified
$B$; that is precisely the missing information. The bulk metric and fold pins do not choose the
representative.

## 5. WR-L does not currently supply the missing action

For

\[
A=1-\frac{r}{X},
\qquad
\phi=-\frac{1}{2}\ln\left(1-\frac{r}{X}\right),
\qquad
\phi'=\frac{1}{2(X-r)},
\]

the live shift-clean vacuum equation gives

\[
(r^2\phi')'
=\frac{r(2X-r)}{2(X-r)^2}\ne0.
\]

So WR-L is not an extremal of the live $R1$ radial kinetic action

\[
S_{R1}=\int dr\,\frac{Z}{2}r^2\phi'^2.
\]

With $\epsilon=X-r$,

\[
L_{R1}\sim\frac{ZX^2}{8\epsilon^2},
\qquad
p_\phi\sim\frac{ZX^2}{2\epsilon}.
\]

Both the action integral and the momentum diverge at the WR-L wall. The uncompensated angular
term is proportional to $A$ there and cannot cancel this divergence.

As a narrow inverse-variational diagnostic only, suppose one assumes

\[
L=\frac{Z}{2}r^2W(\phi)\phi'^2
\]

and demands that WR-L be an exact extremal. Writing

\[
f(\phi)=\frac{(1-e^{-2\phi})^2}{e^{-2\phi}},
\]

the Euler equation reduces to $W'f+2Wf'=0$, and therefore fixes

\[
W(\phi)\propto
\frac{e^{-4\phi}}{(1-e^{-2\phi})^4}.
\]

On WR-L this produces

\[
L=\frac{ZX^2}{8r^2},
\]

which is finite at the wall but divergent at the seat. This weight also breaks the simple global
depth-shift form by singling out $\phi=0$. It is **not proposed as UDT physics**. It demonstrates
that reverse-engineering an action from the selected wall profile merely moves the singularity and
requires an unforced action-class premise.

Thus WR-L remains a **DERIVED kinematic/wall selector under its axioms**, while its compatible
off-shell dynamics remain **OPEN**.

## 6. What can honestly be called a charge

### 6.1 Historical native-action flux

Given the recorded $(Z,\mu)$ action, the conjugate dilation flux is

\[
q_\phi=p_\phi=Z\rho^2\phi'+2\mu\rho\rho'.
\]

At the odd fold it reduces to $Z\rho_s^2\phi'_s$. This is **DERIVED given that action
representative and variation class**. Because $Z$, $\mu$, the primitive, and the fold reading
are not all fixed, it is not yet a uniquely normalized native mass.

### 6.2 Conditional H3 finite-volume charge

Under unrestricted EH plus the working-\(S^2\), CHOSE minimal physical-metric completion,

\[
D^2N=\kappa_gN\rho_4
\]

and therefore, for every smooth finite volume,

\[
\boxed{
\frac{2}{\kappa_g}\oint_{\partial V}D_iN\,dS^i
=2\int_VN\rho_4\,dV.
}
\]

This exact identity needs no spatial infinity and no physical wall. It is therefore already the
cleanest finite-volume result available. What remains conditional is the unrestricted-EH action,
the carrier identity/completion, and the identification of its normalized boundary generator with
native UDT mass.

No derivation currently identifies $q_\phi$ with this lapse charge. Doing so would require the
missing off-shell action and normalization bridge, not a numerical calibration.

## 7. The smallest closure package

The present gap cannot be closed by another endpoint value alone. UDT must supply one native
finite-cell action statement containing:

1. **Fold ontology:** exact off-shell quotient VQ, one-copy boundary VB, matched interface VM, or
   causal-horizon VH;
2. **Off-shell functional:** fields, local invariants, measure, derivative order, and carrier
   completion;
3. **Boundary primitive:** the differentiating $B$, allowed endpoint variations, and whether fold
   location varies;
4. **Charge normalization:** a reference rule that makes the boundary generator invariant under
   allowed total-derivative improvements.

If the canon intends an **exact off-shell quotient**, the current calculation supplies an immediate
tooth: the historical Branch-P action and Route-B mixing do not descend; Branch G, $\mu=0$ is the
only survivor inside that recorded family. If instead the canon intends a **physical one-copy
boundary**, its boundary action must be stated or derived. Those are the two clean analytic forks.

Only after one fork is selected does a determined nonlinear solve exist. GPU numerics cannot choose
between them.

## 8. Status ledger

| Claim | Status |
|---|---|
| Odd fold and WR-L wall are different surfaces | **DERIVED** |
| H3 numerical boundary is not physical wall evidence | **DERIVED provenance/scope** |
| Branch-P mirror defect above | **DERIVED**, exact within recorded round first-order family |
| Exact quotient selects Branch G, $\mu=0$ inside that family | **CONDITIONAL DERIVED** on VQ |
| One-copy free-flux boundary selects $\mu=0$ | **CONDITIONAL DERIVED** on VB + standard value-boundary class |
| Two-side Route-B cancellation | **CONFIRMED**, but VM-scoped |
| $H=0$ / $E_{\rm ang}=2$ from finite-cell ontology alone | **NOT DERIVED**; needs free-endpoint and primitive premises |
| WR-L is not an extremal/finite-action field of live $R1$ kinetic | **DERIVED** |
| Unique native boundary mass from current premises | **OPEN / UNDERDETERMINED** |
| H3 lapse/flux identity | **CONDITIONAL DERIVED**, unchanged |

## 9. Self-audit

- No GR field equation is imported as native. EH appears only in the already-named conditional H3
  branch.
- No Standard Model, quantum, fluid, Q-ball, boson-star, fitted cutoff, effective correction, or
  invented coupling is used.
- The $(Z,\mu)$ actions and inverse weight are logical diagnostics inside recorded or explicitly
  narrow classes, not new UDT proposals.
- Exact quotient, one-copy boundary, matched interface, horizon, and numerical box remain separate.
- All nonlinear exponential factors are retained; no linearization is used.
- A fresh independent derivation and adversarial check remain required before banking.

## 10. Reproduction

Run:

```bash
python3 verify_udt_finite_cell_boundary.py
```

The script verifies 23 exact statements: object identity, mirror defects, one-side momenta,
two-side jumps, total-derivative shifts, WR-L Euler residual and divergences, and the narrow
inverse-kinetic diagnostic. Passing it verifies the encoded algebra only, not the choice of native
action, boundary ontology, or physical charge normalization.
