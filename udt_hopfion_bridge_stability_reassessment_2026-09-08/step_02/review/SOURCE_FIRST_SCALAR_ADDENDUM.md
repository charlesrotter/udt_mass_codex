# Pre-exposure scalar and domain completion

The local transverse quotient may be used without assuming closed xi orbits.
In y=w2 phi1-w1 phi2 its metric is E dx^2+G dy^2,
E=1/[4x(1-x)F], G=x(1-x)/F^3. Its Gaussian curvature is
K_B=-[2 sqrt(EG)]^-1 partial_x[G'/sqrt(EG)]. The standard local
submersion/Koszul curvature identity with geodesic unit fibres and
d eta=2 horizontal area gives the horizontal sectional curvature K_B-3;
both vertical sectional curvatures are1 (the Sasaki identity). Thus
R=2(K_B-3)+4=2K_B-2. These are local geometric method identities, not
new physical laws or an assumed global circle quotient.

Direct differentiation gives

    R=24 w1 w2/F-8(w1+w2)-2,
    R'=-24 w1 w2(w1-w2)/F^2,
    |grad R|^2=2304 w1^2 w2^2(w1-w2)^2 x(1-x)/F^3.

Hence for unequal positive weights first drift is nonzero everywhere on the
dense interior0<x<1 and zero on the two axis circles. Equal weights give zero
globally. The all-family result remains restricted to a global simple gap:
R(0)=16w1-8w2-2, R(1)=16w2-8w1-2 must both lie strictly on the same side of6.
Equal weights require w!=1. At w=1 the metric is round and no distinguished
simple Ricci line is supplied. Zero radicand also remains excluded.

The finite direct-block check uses (w1,w2)=(2,3) at an interior point. Inspection
of this scalar formula reveals that R(0)=6 for that pair: it is a local
gap-open check within a globally gap-closing boundary control, not a globally
admitted strict-gap witness. This distinction was identified after that
fixture ran and is preserved. The other unequal pair(1/4,1/2) and its swap
have a global positive gap; equal(1/2,1/2) does too. No outcome was discarded.

The first attempted all-weight direct symbolic block calculation timed out
at60.005965651s, with no substantive stdout. Its source is preserved.
The narrowed finite fixture implementation succeeded in9.307558334s.
The scalar identities above are checked by a separate bounded symbolic
calculation; the submersion/Koszul step is analytic method reasoning, not
claimed to be proved by that algebra script.
