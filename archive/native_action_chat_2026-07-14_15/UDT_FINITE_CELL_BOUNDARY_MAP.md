# MAP — finite-cell variational principle and boundary generator

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-14 |
| Mode | MAP, then analytic DERIVE + self-CAS |
| Driver | DISCLOSED NON-COLD — the historical cell, fold, native-action, EH, and H3 records are visible |
| Observing or targeting? | OBSERVING what the current finite-cell and positional-dilation premises force |
| GPU | Not applicable unless a unique nonlinear boundary-value problem first emerges |
| Data | DATA-BLIND; no wall, particle-mass, cosmological, or spectral target loaded |
| Banking | This MAP and its result are local candidates only; independent verification remains required |

This file is frozen before the derivation. Its purpose is to prevent the desired native-mass
charge from selecting the action or boundary law retroactively.

## 1. Question

Do positional dilation, the canonical finite-cell/fold statements, and WR-L wall regularity force
a differentiable finite-cell action

\[
S_{\mathcal C}[\Psi]
=\int_{\mathcal C}L(\Psi,\partial\Psi)
+\int_{\partial\mathcal C}B(\Psi)
\]

and a uniquely normalized boundary generator that may be called native UDT mass?

Accepted outcomes:

1. **FORCED:** the bulk, variation class, boundary functional, and charge are unique up to a
   physically inert constant;
2. **ALLOWED-FAMILY:** the premises narrow the class but leave inequivalent actions or charges;
3. **UNDERDETERMINED:** a named new postulate is required;
4. **INCONSISTENT-SCOPE:** two boundary concepts cannot be identified under their current stamps.

## 2. Boundary taxonomy — never merge these silently

| Object | Recorded condition | Status and scope |
|---|---|---|
| Canonical static odd fold | $\phi(r_s)=0$, $\rho'(r_s)=0$, $\phi'(r_s)$ free | Finite-cell $\mathbb Z_2$ depth mirror; static Branch-P-era derivations |
| Canonical even fold | $\phi'=\rho'=0$, values free | Finite cell; natural/fold regularity in the earlier round-static reduction |
| WR-L macro wall | $A=1-r/X\to0$, $\phi\to+\infty$ | Causal horizon at finite proper and infinite optical distance; interior exists beyond it |
| H3 carrier-box boundary | pinned/free-mask numerical boundary | Solver control, not a physical UDT wall or mass generator |
| H3 flux surface | arbitrary finite surface in the conditional lapse identity | Readout surface; no independent wall ontology required |

Immediate non-identification test:

\[
\text{odd fold: }\phi=0\Rightarrow A=1,
\qquad
\text{WR-L wall: }A=0\Rightarrow\phi=+\infty.
\]

## 3. Premise ledger

| ID | Premise | Status entering this derivation |
|---|---|---|
| P0 | Positional dilation is founding | FOUNDING |
| P1 | R1–R2 give $A=e^{-2\phi}$ after convention | DERIVED given regularity/convention |
| P2 | R3 plus the P8 slot gives reciprocal longitudinal metric | DERIVED given P8 CHOSE |
| P3 | Finite mirrored cells; no spatial infinity | CANON |
| P4 | Static depth mirror makes $\phi$ odd at the odd fold | CANON clarification |
| P5 | Static transverse size $\rho$ is even at the odd fold | WORKING/CANON-supported in the round-static cell class |
| P6 | WR-L selects $A=1-r/X$ inside its residual family | DERIVED under accepted WR-L axioms |
| P7 | WR-L wall is a horizon, not a hard spatial edge | CANON audit precision |
| P8 | The off-shell bulk action is known | OPEN; the previous derivation found an allowed family |
| P9 | The fold involution is an exact off-shell symmetry of the action | OPEN |
| P10 | The fold is instead only a boundary-data identification | OPEN alternative to P9 |
| P11 | Fold position is fixed or freely varied | OPEN variation-class choice |
| P12 | Boundary functional $B$ and reference subtraction | OPEN |
| P13 | $S^2$ carrier and static native $L_2+L_4$ functional | POSIT + adopted native minimal carrier lane |
| P14 | Four-dimensional carrier completion | OPEN; minimal physical-metric completion is CHOSE |
| P15 | Unrestricted EH metric action | CONDITIONAL through added Lovelock-style premises |

## 4. Variation classes to keep separate

### VQ — exact quotient

The fold map $I$ acts on a neighborhood and the action descends to the quotient:

\[
I^*L=L+dY.
\]

This is stronger than equality of the integrand only at the fixed surface.

### VB — boundary-only fold

Only the endpoint data and allowed variations are parity restricted. For a first-order radial
action,

\[
\delta S=\int E_i\,\delta q^i\,dr
+[p_i\delta q^i+\delta B]_{\partial\mathcal C},
\qquad p_i=\frac{\partial L}{\partial q'^i}.
\]

No mirrored bulk is assumed.

### VM — matched two-side interface

Two independent or mirrored domains are retained and momentum jumps are imposed. This is not
automatically equivalent to VQ or VB when the bulk action is not invariant under the mirror.

### VH — horizon limit

The WR-L surface is approached as a causal horizon. Horizon regularity and finite action must be
checked; no endpoint variation or fold charge is presumed.

### VN — numerical box

Pinned/free-mask conditions regulate a solve. They carry no physical boundary-action inference.

## 5. Pre-registered tests

1. **Object identity:** compare $A,\phi$ and causal character at each alleged wall.
2. **Quotient descent:** compute $I^*L-L$ for the recorded $(Z,\mu)$ geometric family in Branch G
   and Branch P. Equality only at the fixed point is insufficient.
3. **Boundary differentiability:** derive momenta and allowed variations for odd $\phi$ and even
   $\rho$ under VB; record every required boundary term.
4. **Two-side versus one-side audit:** do not transfer a VM jump cancellation into VB or VQ without
   proving equivalence.
5. **Moving-endpoint audit:** derive the transversality equation with general $B$; test whether
   $H=0$ is forced or assumes $B=0$ and a free endpoint.
6. **Primitive ambiguity:** apply $L\mapsto L+dF/dr$ and track bulk equations, momenta, Hamiltonian,
   and charge. A native charge is unique only if current premises eliminate the physically active
   $F$ family.
7. **WR-L compatibility:** insert $A=1-r/X$ into the live shift-clean radial action; test its exact
   Euler residual, action convergence, and boundary momentum.
8. **Conditional H3 carry:** preserve the exact lapse/flux identity only under its named action and
   carrier-completion premises.

## 6. Falsification and stopping rules

- Do not construct a boundary term to cancel a discovered divergence and then call it derived.
- Do not identify the odd fold with the WR-L horizon if $A$ or $\phi$ disagree.
- Do not use a desired mass formula to choose a total-derivative representative.
- Do not call a matched-interface jump condition the natural BC of a one-copy quotient unless the
  action actually descends.
- If two actions have the same bulk equations and allowed fields but different boundary generators,
  the native mass is **UNDERDETERMINED**.
- If the result is underdetermination, state the smallest missing postulate rather than adding one.

