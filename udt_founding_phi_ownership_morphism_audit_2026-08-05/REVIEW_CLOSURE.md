# Fresh adversarial review closure

The fresh zero-context reviewer returned `ACCEPTED_WITH_REPAIRS`.

It accepted the source-level retyping, the nonvacuous factorization witnesses, the presentation-orbit
argument, the `K` versus physical `eta` distinction, the append-only source correction, all ten
route grades, and the maximum conclusion. It found one bounded sign mismatch in the stationary
positive branch: the draft called `log(N(q)/N(p))` the signed depth even though the frozen source
convention makes `N(q)/N(p)` the lapse ratio and
`delta_K=log(N(p)/N(q))`.

The repair changes no route, premise, or headline conclusion. The derivation and report now state

```text
q_K(p,q)=N(q)/N(p),
delta_K(p,q)=-log q_K(p,q)=log(N(p)/N(q)).
```

Both implementations now keep the lapse and depth ratios explicitly inverse. The primary replay is
34/34, the independent replay is 24/24, and the fail-closed verifier is 39/39 with 19/19 exercised
mutation rejections, including a new stationary-sign catch.
