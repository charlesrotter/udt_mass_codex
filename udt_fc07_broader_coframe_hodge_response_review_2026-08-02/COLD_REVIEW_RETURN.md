# Fresh zero-context cold adversarial return

Date: 2026-08-02  
Mode: read-only; no repository mutation; no primary derivation import or execution  
Actual reviewed tip: `6beae10c4367daf9dbbbd92f0935f5618efa2b89`

## Verdict

`PASS_AFTER_REQUIRED_CORRECTIONS`.

No load-bearing algebraic contradiction was found. The defensible result is a bounded mathematical
availability theorem and two countercontrols—not a selected UDT response.

## Independent findings

### Compact Hodge theorem

For compact boundaryless Riemannian `(Sigma,q)`, smooth single-valued `f`, and harmonic `h`,

```text
<df,h>=<f,delta h>=0,
```

so `Pi_H(df)=0`. No `b1=1` premise is needed for this theorem. For smooth
`F:R->R`, `F(phi)dphi=dH(phi)`. Boundaries, noncompactness, circle-valued/twisted scalars, singular
`F`, and time-live/non-Riemannian domains remain outside scope.

### Formal six-direction census

The general formal affine one-form is

```text
omega=(a0+a1 phi+a2 sigma)dphi+(b0+b1 phi+b2 sigma)dsigma,
domega=(b1-a2)dphi wedge dsigma.
```

The formal/free coefficient space is six-dimensional, its universally exact kernel is
five-dimensional, and its quotient is one-dimensional, represented by

```text
lambda=(phi dsigma-sigma dphi)/2,
dlambda=dphi wedge dsigma.
```

This is not a configuration-uniform quotient dimension. After pullback to a fixed configuration,
functional dependence or `dphi wedge dsigma=0` can change the actual classification.

### Reference and constructive witnesses

Constant shifts give

```text
Delta lambda=(A dsigma-B dphi)/2=d[(A sigma-B phi)/2].
```

For `phi=sin(2 pi s)` and `sigma=cos(2 pi s)`, both are single-valued while

```text
lambda=-pi ds,
integral lambda=-pi.
```

On the minus-identity mapping torus, `cos(2 pi y),cos(2 pi z)` descend and give

```text
dlambda=4 pi^2 sin(2 pi y)sin(2 pi z)dy wedge dz != 0.
```

The base loop supplies the harmonic witness. The screen-dependent curl supplies coexact
capability; it does not itself prove a harmonic component.

### Upper-right controls

Assume explicitly `epsilon!=0` and

```text
tau(s,y,z)=(s+1,-y,-z).
```

`ds+dpsi` descends because `psi(-y)=psi(y)`. `ds+f(y)dz` descends because `f` is odd and
`tau*dz=-dz`. Both metrics are positive with determinant one.

For `g=psi_y`,

```text
q^-1=[[1+g^2,-g,0],[-g,1,0],[0,0,1]],
(ds+dpsi)^sharp=partial_s.
```

Thus `delta(ds+dpsi)=0`, while `delta ds=psi_yy` up to the registered codifferential sign.

For `eta1=ds+f(y)dz`,

```text
q^-1=[[1+f^2,0,-f],[0,1,0],[-f,0,1]],
eta1^sharp=partial_s,
ds^sharp=(1+f^2)partial_s-f partial_z.
```

Both forms are coclosed, but `d eta1=f'(y)dy wedge dz!=0`. Since `ds` spans the harmonic line,

```text
Pi_H(eta1)=[1/(1+epsilon^2/2)]ds.
```

The metric and local orthonormal coframe descend with transition `diag(1,-1,-1)`. The displayed
`dy,dz` rows are not individually global one-forms.

### UDT status

The controls are chosen mathematical off-shell spatial countercontrols outside the registered
positive-triangular complete-`phi` extension class. They show only that lower-triangular pointwise
ownership cannot be extrapolated to arbitrary chosen upper-right pair embeddings. They do not
refute the parent theorem in scope or prove that physical UDT admits or selects either control.

`sigma=log(D/D0)` remains relative to the supplied oriented screen split and unimodular descent.
Full observer naturality, split-free extension, Cartan/curvature production, equation, action,
source, carrier, bootstrap return, mass, and density relation remain open.

## Evidence identity

- 51/51 parent package entries pass.
- Parent package-manifest SHA-256:
  `5f9cbe9eeae15b82e9d79d290cbc0e8d056b8d8cd7af20c2b1818070c164ae36`.
- Parent source-manifest SHA-256:
  `6e78d809cd77edf7ebf986397421f53471bb043c6ced5e8dcb0533b5245fac88`.
- All 15 recorded Git blobs pass. Fourteen current files remain identical; `LIVE.md` legitimately
  advanced after the freeze.

## Maximum defensible conclusion

Compact-boundaryless exact-form obstruction; one alternating direction in the formal affine
two-scalar class; separate constructive harmonic and coexact witnesses; and two minus-identity
mathematical countercontrols showing non-extension of lower-triangular pointwise ownership.
Selection, complete-frame naturality, physical admissibility, and density remain open.
