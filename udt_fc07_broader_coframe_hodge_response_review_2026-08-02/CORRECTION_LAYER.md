# Append-only correction layer

Date: 2026-08-02

This file supersedes only the overbroad readings listed below. The parent package at
`udt_fc07_broader_coframe_hodge_response_audit_2026-08-02/` remains byte-identical with manifest
SHA-256 `5f9cbe9eeae15b82e9d79d290cbc0e8d056b8d8cd7af20c2b1818070c164ae36`.

## 1. Rank-one statement

Correct reading:

```text
formal/free affine two-scalar coefficient class
modulo combinations universally exact for arbitrary independent (phi,sigma)
has quotient dimension one.
```

For

```text
omega=(a0+a1 phi+a2 sigma)dphi+(b0+b1 phi+b2 sigma)dsigma,
```

the sole formal curl coefficient is `b1-a2`. Its kernel has dimension five. The alternating
representative is

```text
lambda=(phi dsigma-sigma dphi)/2.
```

This is not a promise that every fixed configuration realizes a one-dimensional quotient. For the
globally single-valued fixed control `sigma=2 phi`, `lambda=0` identically. Pullback may collapse
the formal direction or change its closed/exact status.

## 2. Exact versus harmonic separation

The universal compact-boundaryless statement is fully robust:

```text
Pi_H(df)=0.
```

The cold review did not find that separation to be an ansatz artifact. Only the attempted
extrapolation of **pointwise raw-ruler/harmonic line ownership** beyond the parent's declared
lower-triangular family fails under the chosen mathematical upper-right countercontrol.

## 3. Mapping-torus descent

Under

```text
tau(s,y,z)=(s+1,-y,-z),
```

`ds+dpsi` and `ds+f(y)dz` are global because `psi` is even and `f` is odd. The metric and local
orthonormal coframe descend with transition

```text
diag(1,-1,-1).
```

The displayed screen rows `dy,dz` are local rows related by that transition, not individually
global one-forms on the quotient.

Both counterexamples require `epsilon!=0`. The exact-connection control changes the harmonic
representative within one cohomology class. The nonclosed control gives

```text
d eta1 != 0,
delta eta1=0,
Pi_H(eta1)=[1/(1+epsilon^2/2)]ds.
```

## 4. Physical status

The two upper-right examples are chosen, off-shell mathematical pair-embedding countercontrols.
They lie outside the registered positive-triangular complete-`phi` extension class. They do not:

- refute the parent theorem in its lower-triangular scope;
- show that the founded UDT pair admits or selects the upper-right embeddings;
- derive a complete frame, Cartan response, equation, or source.

The safe wording is “counterexample to extrapolation beyond the parent scope,” not “ownership
correction” without qualification.

## 5. Alternating candidate status

The priority phrase “first exact orchestra motif” is withdrawn. The source freeze was not a
repository-history priority census. The retained statement is:

```text
an exact bounded alternating two-scalar candidate in this FC07 audit.
```

The base loop is a harmonic witness. The separate screen-dependent curl witness proves local
nonclosed/coexact capability, not a harmonic coefficient. No connection or curvature has been
shown to produce the candidate.

## 6. Verification repair

The correction verifier replaces two weak parent checks:

- the reference-shift identity is evaluated on nontrivial polynomial functions with exact rational
  arithmetic rather than compared tautologically;
- actual pullbacks of the exact/nonclosed controls and the screen-row transition are tested rather
  than inferred from monodromy determinants.

Historical source replay now validates the bytes of each recorded Git blob. Current-path equality
is reported separately. This preserves the source freeze even after `LIVE.md` legitimately moves.

## 7. Final corrected grade

`COLD_REVIEW_PASS_AFTER_REQUIRED_CORRECTIONS`.

The cold review upgrades the parent same-session verification caveat, but it does not broaden the
scientific scope. Selection, complete-frame naturality, physical admissibility, Cartan/curvature
production, density, bootstrap return, action, carrier, source, mass, and matter remain open.
