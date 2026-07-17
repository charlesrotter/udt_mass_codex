# UDT CSN finite-boundary charge selection — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | grok at 64af120; pre-existing dirty work preserved |
| Mode | Analytic DERIVE + dependency-free exact audit; DATA-BLIND |
| MAP frozen first | UDT_CSN_BOUNDARY_CHARGE_SELECTION_MAP.md, SHA-256 97f40ed9d67c830b4f9a9771a94cd088d7ee37e749e60e4f7f5d64cf90ad50f9 |
| Exact verifier | verify_udt_csn_boundary_charge_selection.py — 21/21 checks pass |
| GPU | Not used; no determined nonlinear problem emerged |
| Independent verification | OPEN |
| Build-on grade | PROVISIONAL ANALYTIC RESULT; not banked and not canon |

## 0. Result

\[
\boxed{
\begin{gathered}
\text{CSN forces inverse-length weight for a static boundary energy, not its coefficient.}\\
\text{Differentiability and flat-reference subtraction still leave arbitrary }k/X\text{ charge shifts.}\\
\text{The Euler }4/X\text{ is a one-sided WR-L static-patch readout, not a native finite-cell charge.}
\end{gathered}}
\]

The last statement follows from the live boundary ontology:

- the WR-L \(A=0\) surface is a causal horizon with continuation, not presently a hard boundary;
- the canonical odd fold has \(A=1\), where the Euler primitive vanishes;
- at a smoothly matched internal interface, oppositely oriented primitive contributions cancel.

Therefore the boundary lead in the preceding electron-calibration result is **RE-GRADED**:

\[
\boxed{
\text{right dimensional scaling = DERIVED;}
\qquad
\text{physical applicability and normalization = OPEN.}
}
\]

## 1. What CSN actually fixes at a reciprocal boundary

Restrict first to a local static endpoint functional depending on \(A,A'\), and \(r\). Under the
global common-scale orbit

\[
r\mapsto\lambda r,\qquad
A\mapsto A,\qquad
A'\mapsto\lambda^{-1}A',
\]

the combinations

\[
u=A,\qquad v=rA'
\]

are dimensionless. A boundary energy per unit \(c\,dt\) must have inverse-length weight. Hence the
most general first-jet scale-homogeneous form is

\[
\boxed{
B(A,A',r)=\frac{\gamma}{r}\,b(A,rA').
}
\]

CSN fixes the prefactor \(1/r\). It does not fix the dimensionless function \(b(u,v)\) or the
normalization \(\gamma\).

Allowing \(A''\) or higher boundary jets enlarges the class to

\[
B=\frac{\gamma}{r}
b(A,rA',r^2A'',\ldots)
\]

and therefore cannot restore uniqueness without an additional derivative/boundary premise.

This is a **DERIVED homogeneity classification in the stated reduced class**, not a proof that every
such \(b\) has a full covariant lift.

## 2. Differentiability constrains derivatives, not the charge value

The conditional conformal bulk gives

\[
\delta S_C\big|_\partial
=P_0\delta A+P_1\delta A',
\]

where

\[
P_1=2\gamma W,
\qquad
P_0=-\frac{4\gamma W}{r}-2\gamma W'.
\]

For

\[
B=\frac{\gamma}{r}b(A,v),
\qquad v=rA',
\]

at fixed endpoint \(r\),

\[
\delta B
=\frac{\gamma}{r}b_A\,\delta A
+\gamma b_v\,\delta A'.
\]

Therefore

\[
\boxed{
\delta(S_C+B)\big|_\partial
=\left(P_0+\frac{\gamma}{r}b_A\right)\delta A
+\left(P_1+\gamma b_v\right)\delta A'.
}
\]

On WR-L,

\[
A=0,\qquad v=-1,\qquad P_0=P_1=0.
\]

The common endpoint classes imply:

| Variation class | WR-L differentiability condition |
|---|---|
| fixed \(A,A'\) | none |
| fixed \(A\), free \(A'\) | \(b_v(0,-1)=0\) |
| free \(A\), fixed \(A'\) | \(b_A(0,-1)=0\) |
| free \(A,A'\) | \(b_A(0,-1)=b_v(0,-1)=0\) |

None fixes \(b(0,-1)\), the value that enters a charge.

## 3. Exact nonuniqueness after flat subtraction

Even add the reference convention

\[
B(1,0,r)=0.
\]

For every real \(k\), consider only as a reduced inverse-problem counterfamily

\[
b_k(A,v)=k(1-A^2).
\]

It satisfies

\[
b_k(1,0)=0,
\]

and at the WR-L wall data,

\[
b_k(0,-1)=k,
\qquad
\partial_A b_k(0,-1)=0,
\qquad
\partial_v b_k(0,-1)=0.
\]

Thus it passes even the free-jet differentiability conditions at WR-L while producing

\[
\boxed{B_{\rm WR-L}=\frac{\gamma k}{X}.}
\]

Different \(k\) give the same bulk equation, the same WR-L solution, the same flat reference value,
and the same endpoint stationarity, but different charge readouts.

This counterfamily is not proposed as a covariant UDT boundary action. It proves the narrower and
sufficient statement:

\[
\boxed{
\text{CSN + reduced differentiability + flat subtraction do not determine the charge.}
}
\]

A full covariance theorem could shrink the family, but no such UDT boundary theorem has yet been
derived. Overall action multiplication would still leave a separate normalization freedom.

## 4. Why varying \(1/X\) does not select \(X\)

For a static boundary value \(B_X=\gamma k/X\), the action over a coordinate-time interval is

\[
S_B=c\,\Delta t\,\frac{\gamma k}{X}.
\]

The CSN-invariant duration is

\[
\Delta\tau=\frac{c\,\Delta t}{X}.
\]

Therefore

\[
\boxed{S_B=\gamma k\,\Delta\tau,}
\]

which is independent of \(X\) at fixed dimensionless duration.

Varying \(X\) while artificially holding \(\Delta t\) fixed compares different clock calibrations
and produces a spurious \(X\)-equation. A per-coordinate-time readout scales as \(1/X\), but it
becomes a physical energy only after a clock/mass normalization is selected.

This agrees with the prior scale-orbit theorem: a CSN-respecting boundary action cannot by itself
choose an absolute member of the orbit.

## 5. Regrade of the Euler \(4/X\) term

The exact reciprocal primitive is

\[
r^2E_4=\frac{d}{dr}[4(A-1)A'].
\]

Writing it in the boundary form above gives

\[
b_E(A,v)=4(A-1)v.
\]

### 5.1 One-sided WR-L static patch

At \(r=X\),

\[
A=0,\qquad v=-1,
\]

so

\[
b_E(0,-1)=4,
\qquad
B_E=\frac{4}{X}
\]

up to the suppressed normalization.

But the bare primitive also has

\[
\partial_A b_E(0,-1)=-4,
\qquad
\partial_v b_E(0,-1)=-4.
\]

It is not a freely differentiable standalone boundary functional at that endpoint. A complete Euler
topological boundary/corner completion must be varied as a whole.

### 5.2 Canonical odd fold

The canonical fold has

\[
\phi=0,\qquad A=e^{-2\phi}=1.
\]

Therefore, regardless of \(A'\),

\[
\boxed{b_E(1,v)=0.}
\]

The one-sided WR-L \(4/X\) is not the Euler value of the canonical fold.

### 5.3 Internal horizon/interface

The live WR-L \(A=0\) surface is a causal horizon with a region beyond it. If it is an internal
matching surface of a smooth completion, a total derivative split at the surface contributes the
same primitive with opposite orientations:

\[
\mathcal P_{\rm left}-\mathcal P_{\rm right}=0
\]

when the completed invariant is continuous. Null-limit boundary and corner terms must still be
audited, but a one-sided primitive cannot be assumed to survive.

Hence:

\[
\boxed{
\frac4X
\text{ is CONDITIONAL on treating the WR-L static-patch edge as a one-copy endpoint.}
}
\]

That treatment is not the current live ontology.

## 6. Multiplicative normalization remains independent

Even if a future full-covariance and boundary theorem uniquely selected the functional form, the
vacuum equation is unchanged under

\[
S\mapsto\alpha S,\qquad \alpha\ne0,
\]

while the canonical boundary generator scales as

\[
Q\mapsto\alpha Q.
\]

An accepted electron mass could legitimately calibrate this final overall normalization after all
dimensionless structure is derived. It cannot presently distinguish:

- different allowed boundary improvements;
- WR-L horizon versus fold/interface ontology;
- different carrier coefficient ratios;
- different matter-to-geometry coupling laws.

Thus more than one freedom remains.

## 7. Consequence for the electron path

The clean calibration algebra remains true:

\[
\beta_e=\frac{Gm_e}{c^2X},
\qquad
X=\frac{Gm_e}{c^2\beta_e}.
\]

What changes is the candidate provenance of \(\beta_e\):

\[
\boxed{
\beta_e\text{ cannot presently be obtained from the one-sided WR-L Euler primitive.}
}
\]

The viable analytic routes are now:

1. derive a genuine one-copy finite-cell boundary ontology and its complete covariant boundary
   action;
2. derive the charge on the canonical fold/quotient rather than substituting the WR-L horizon;
3. derive \(\beta_e\) from a full scale-setting matter–geometry solution whose total charge is
   defined without treating the horizon as a hard wall.

Route 3 is the path most directly compatible with the current live WR-L scope. It still requires a
native matter-scale completion; the reopened \(S^2\) carrier cannot be assumed.

## 8. Status ledger

| Claim | Status |
|---|---|
| First-jet CSN boundary form \(B=\gamma b(A,rA')/r\) | **DERIVED in reduced class** |
| CSN fixes \(b\) or its coefficient | **FALSE** |
| Differentiability fixes \(b(0,-1)\) | **FALSE in tested endpoint classes** |
| Flat subtraction plus differentiability fixes charge | **EXCLUDED by explicit counterfamily** |
| Per-time boundary readout has \(1/X\) weight | **DERIVED** |
| Complete scale-neutral time-slab action selects \(X\) | **FALSE** |
| Euler one-sided WR-L primitive is \(4/X\) | **DERIVED conditional geometry** |
| Euler primitive at canonical \(A=1\) fold | **ZERO** |
| One-sided WR-L Euler value is a native global charge | **NOT DERIVED / ontology mismatch** |
| Matched internal primitive survives | **NO, under smooth opposite-orientation matching** |
| One accepted \(m_e\) can fix final overall normalization | **CONDITIONAL possibility** |
| Present boundary sector yields \(\beta_e\) | **OPEN / not yet formable** |

## 9. Frontier

\[
\boxed{
\begin{gathered}
\text{WR-L conformal bulk charge = ZERO in the tested branch.}\\
\text{One-sided Euler }4/X\text{ = CONDITIONAL STATIC-PATCH READOUT, RE-GRADED.}\\
\text{CSN boundary weight = DERIVED; function, ontology, and normalization = OPEN.}\\
\text{Electron calibration remains viable only after a full normalized matter/global charge exists.}
\end{gathered}}
\]

## 10. Verification scope

The dependency-free script checks 21 exact statements: CSN boundary weight, endpoint derivative
coefficients, the arbitrary-\(k\) counterfamily, Euler values and derivatives, the canonical-fold
zero, internal-interface orientation cancellation, dimensionless clock scaling, and multiplicative
charge ambiguity. It does not prove a full covariant boundary classification, null-horizon
completion, quotient action, carrier, \(G\), or \(\beta_e\).

