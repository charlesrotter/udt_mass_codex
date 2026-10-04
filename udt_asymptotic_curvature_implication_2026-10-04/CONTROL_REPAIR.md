# ACI1 exact-control normalization repair

The original frozen script and failed capture remain unchanged. The exponential
product assertions completed, but the first cosh-product assertion stopped at
an expression that SymPy simplify had not reduced to zero:

    -H^2 [sinh(2Ht)tanh(Ht)-cosh(2Ht)+1] / [2cosh^2(Ht)].

The numerator is exactly zero: sinh(2v)tanh(v)=2sinh^2(v) and
cosh(2v)-1=2sinh^2(v). With real v, cosh(v) is nonzero. This is an exact
representation issue, not a discarded nonzero curvature or a changed metric.

The pinned wrapper changes the assertion normal form to expand_trig, rewrite
in exponentials, then simplify. It applies the same exact normalization to
the three recorded scalar contractions. All metrics, derivatives, tensor
contractions, null paths, expected identities and case limits are unchanged.
Assertions still require exact zero; no floating tolerance or accepted residual
is introduced. The repaired execution gets a separate capture and its source
hashes are frozen before execution. The initial failure is not counted as a pass.
