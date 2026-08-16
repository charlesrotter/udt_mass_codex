# G111 correction record

## First production attempt

The first symbolic implementation treated all nine ordered spatial second derivatives
`e_i(e_j phi)` as algebraically independent. That is false in the noncommuting R17 frame. The
result failed exact Riemann pair exchange and the first Bianchi identity, so no outcome was
accepted or interpreted.

For the R17 convention

```text
[e1,e2]=2 e3,  [e2,e3]=2 e1,  [e3,e1]=2 e2,
```

the scalar two-jet must obey

```text
q12=q21+2 p3,
q13=q31-2 p2,
q23=q32+2 p1.
```

The implementation was repaired to use only the six independent ordered second derivatives and
to construct the other three from these Maurer--Cartan compatibility relations. The repaired
symbolic tensor passes both Riemann antisymmetries, pair exchange, and the first Bianchi identity
exactly. `run_catch_proofs.py` deliberately restores the wrong sign in one relation and confirms
that the verifier rejects it.

## Evidence status

This was a caught algebraic implementation error, not a change to the preregistered geometry,
control census, or conclusion. The failed output was not banked. The correction is retained here
because silently presenting only the successful route would weaken the audit trail.
