# FSR1 same-premise basis clarification follow-up

After the first verdict was sealed, parent flagged that a reader might infer
abstract group inequivalence from the declared-basis distinction. The first
FINAL_REVIEW already excludes that inference. The initial candidate's wording
is mathematically defensible as a statement about the named actions, but an
explicit basis qualification improves it. This is a bounded correction to
presentation, not a new physical premise, equation or search.

The initial FINAL_REVIEW, MAINTAINED_REVIEW, RECORD and review manifest are
preserved byte-for-byte in review/initial_verdict. The original seven candidate/
maintained snapshots remain in review/initial. Parent additionally preserves the
pre-qualification candidate/code/check-plan versions in basis_repair_initial.
No failed scientific result is removed by the follow-up.

## Independent exact argument

Use the parent's displayed rational matrix and calculate its inverse directly:

    C = [[1/2,1/2],[-1,1]],  det C=1,
    C^-1 = [[1,-1/2],[1,1/2]].

With K=[[0,1],[1,0]], direct column pairing gives

    C^T K C = diag(-1,1) = eta2.

For a>0 and D=diag(a^-1,a), direct multiplication yields

    C^-1 D C = [[A,B],[B,A]],
    A=(a+a^-1)/2,  B=(a^-1-a)/2,
    A^2-B^2=1, A>0.

Therefore this conjugate preserves eta2 and is a proper future Lorentz boost;
a=exp(delta) gives A=cosh(delta), B=-sinh(delta). The equality holds at a=1
without any singular case. This proves the mathematical representation relation
for all positive a, rather than by a finite sample.

It also remains true that D^T eta2 D=diag(-a^-2,a^2) on the original declared
clock/ruler basis. A change of basis transforms every tensor representing that
physical description. In particular, the same C gives

    C^T eta2 C = [[3/4,-5/4],[-5/4,3/4]],

which is different from eta2. Converting K to diagonal Lorentz form cannot by
itself retain the original metric/readout identification unchanged. Thus basis
equivalence does not prove that the source's finite metric deformation and the
unit-frame transport are the same physically specified operation, nor provide
an event-moving neighborhood identity, response functional or field law.

This matrix derivation is an independent analytic check after parent target
exposure. Final revised files and any repaired execution inspected are recorded
in FINAL_REVIEW/RECORD; the old verdict is not retroactively relabeled as review
of the future revised bytes.
