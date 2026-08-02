# Preregistration clarification — transition graph before fixed subspace

Date: 2026-08-01  
Timing: after the preregistration commit and initial source orientation; before derivation outputs or
candidate adjudication

The original exact-control paragraph risks conflating two different objects.

For a transition or monodromy matrix `M`, the native overlap/closed-identification descent law is

```text
v_plus = M v_minus.
```

It defines the endpoint-pair compatibility fiber

```text
Graph(M) = {(v_minus,v_plus): v_plus=M v_minus}.
```

Different registered matrices may therefore parameterize different graph subspaces even when their
dimensions agree.

The stronger condition

```text
(M-I)v=0
```

is the fixed subspace `ker(M-I)`.  It follows only after a separately required invariant,
base-constant, or parallel section identifies `v_plus` and `v_minus` in one presentation.  This
audit may not add that requirement merely to obtain a more selective result.  Curvature or holonomy
likewise constrains a parallel section only when parallelism is independently owned.

Accordingly:

- `Graph(M)` is the primary choice-free descent control;
- `ker(M-I)` is retained only as a conditional fixed/parallel-section diagnostic;
- passing the local-fiber gate does not require fiber dimension to change—distinct nonempty graph
  subspaces suffice;
- no transition matrix or completion is thereby selected or made physical.

All original candidates, source scope, premise firewalls, and maximum conclusion remain unchanged.
