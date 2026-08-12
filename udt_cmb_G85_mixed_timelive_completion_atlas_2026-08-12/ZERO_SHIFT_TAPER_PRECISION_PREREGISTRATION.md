# G85 zero-shift taper precision correction — preregistration

Date: 2026-08-12

The calculation package is retained, but one condition requires a sharper type statement before
external review.

For the zero-shift local bifurcate construction, writing `h=A*h_tilde` is sufficient only when
`h_tilde` is smooth in the regular `U,V` completion chart (the stationary subcase
`h_tilde=h_tilde(A,angles)` is included). Arbitrary dependence on the singular static coordinate
`tau=log(V/U)` is not automatically smooth.

The correction will:

- add `Kruskal_smooth` to the zero-shift taper condition in the production atlas;
- distinguish that local zero-shift condition from the global shift-supported time-live taper;
- update exact/report/status wording, independent verification, catch proofs, and hashes; and
- preserve the preregistered `196 x 5` universe and all four class counts unchanged.

No new computation family, physical selection, topology, scale, endpoint, or dynamic law is added.
