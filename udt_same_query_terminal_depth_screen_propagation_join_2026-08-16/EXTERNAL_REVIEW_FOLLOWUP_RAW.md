## Finding

A residual nomenclature defect remained: the first review and requested landing used
`CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED`, while the repaired package used
`CONDITIONAL_SAME_QUERY_TERMINAL_DEPTH_OWNER_DERIVED`. This was not a mathematical regression, but
it was literal landing drift.

## Verdict

1. Repair 1 is effective. The production and independent controls now explicitly use
   `phi_pair(z)=z^2` with regular `W(z)=exp(z) I`, and check finite endpoint depth,
   `dot(phi_pair)=0`, nonzero screen/log-area rate, and noninjectivity across `z=-1,1`.
2. Repair 2 is effective. The caustic control uses `W(z)=z I`, proves rank loss through
   `det W(0)=0`, exhibits optical-trace pole `2/z`, and independently rejects inversion at the
   singular point.
3. Repair 3 is effective. Equation (7) is now well-formed TeX.
4. Repair 4 is effective. `verify_package.py` replays in a temporary directory and writes back only
   under explicit `--write-result`.

No regression is visible in the already accepted central algebra. The original
`CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED` landing remains justified in substance. On one supplied
matched regular query,

```text
delta(lambda;lambda0) = phi_pair(lambda) - phi_pair(lambda0)
a_eff = tr(Wdot W^-1)/(2 phidot_pair)
```

hold only on regular intervals with `phidot_pair != 0`; there is no continuation claim through
turning points or caustics and no promotion to physical-history selection, branch selection, or a
universal/global law.

This file preserves the substantive follow-up verdict. Temporary intake-path citations were
omitted because they are not durable repository references.
