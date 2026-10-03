# Local proof completion review

Reviewed DERIVATION_COMPLETION.md, REFERENCES.md and check_candidate.py after
the frozen exposed review. No initial candidate or source-first file was edited.

The signature/geometry gate is resolved by the explicit local proof. In
particular S_X is an entire matrix function, so null X, Jordan blocks and
indefinite signature introduce no division or missing branch. The normal metric
is even in X; reflection is therefore an actual local isometry. An isometry's
differential intertwines parallel transport, giving the midpoint-reflection
differential and preparation transvection exactly. Equality of local isometry
one-jets entails equality on their common exponential neighborhood. The stated
one-parameter transvection composition follows there.

The Killing-jet signs are consistent. Differentiating the ordinary vector-field
bracket at o yields R(X,Y)Z by Bianchi. Fundamental fields of the left action
reverse the group bracket, yielding [X,Y]=-R(X,Y); the isotropy action then
gives [H,X]=HX. The local p+h split and inverse-function argument suffice for
G=exp(Z)h and its half-log. This uses the metric at o, not a Killing-form
normalization. The local proof also justifies analyticity of the actual interval,
including its null set. No global Riemannian theorem is silently required.

The references are method attribution, with their Riemannian scope accurately
disclosed. I evaluated the explicit proof rather than independently re-opening
each web source; that omission does not create an uninspected load-bearing
technical premise in this review.

The separate check script reconstructs all free-associative coefficients from
the saved commutator representation and compares against its separately arranged
product/log, before finite controls. That is the required meaningful algebraic
gate. It remains a parent check, not a new independent reviewer.

I also audited the supplied plane-wave setup: transverse preparation at u=0
parallel-transports U to U_v=-1/2-L² sum(lambda_i n_i²)/2. The proposed
B geodesic v=-b/2-sum(x_i x_i')/2 supplies exactly that initial value, retains
unit norm and solves the original geodesic equations. Its endpoint action uses
the signed actual delta-u for the later return. The coordinate Christoffel
curvature/parallelness check addresses realizability and the curvature sign.
The trigonometric/hyperbolic series are their analytic local branches.

No defect found in the completion or check design. Final disposition awaits
actual check outputs and final coefficient/prose correspondence, rather than
assuming a planned check passed.
