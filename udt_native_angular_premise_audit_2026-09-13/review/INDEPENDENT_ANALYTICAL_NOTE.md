# Independent center-constraint check

Prepared and executed before any NEW NAP1 candidate/code/result exposure. This note explains the source-first frozen implementation and actual result; it does not adopt a physical response law.

LSR1 supplies the quadratic Cartesian metric jet with zero first derivatives at the center. Extract its Hessian H_ab,cd by exact polynomial polarization, then compute

    partial_d Gamma^a_bc = (eta^aa/2)(H_ac,bd + H_ab,cd - H_bc,ad),
    R_abcd = eta_aa(partial_c Gamma^a_db - partial_d Gamma^a_cb),
    Ric_bd = sum_a eta^aa R_ab ad.

These are the original Levi-Civita definitions in the source sign convention. The center quadratic connection products vanish because every first metric derivative vanishes. The check does not substitute the claimed Ricci formula into curvature construction. Unit vectors used for polarization evaluate the formal quadratic polynomial solely to extract its coefficients; they are not purported full-metric points inside the positive neighborhood.

The full curvature map is linear in the six coefficients consisting of c2 plus five independent tracefree S entries: inverse center metric is fixed eta and first derivatives are zero. Exact verification on the six coefficient basis vectors therefore checks the displayed identity for every real coefficient, using linearity, rather than relying on random-sample coverage. Zero and one mixed rational case are additional controls. The outputs are

    Ric_00=3c2, Ric_0i=0, Ric_ij=-3c2 delta_ij+3S_ij,
    R=-12c2,
    TF_g(Ric)=diag(0,3S).

The computed linear TF map has rank five and its c2 column is zero. It follows within this supplied-jet class that TF Ric=0 iff S=0, with no constraint on c2 from this center condition.

A direct DDR specialization gives another check. For u=e0 and unit spatial n use the actual full source tangent H=2(u-flat tensor u-flat+n-flat tensor n-flat), including its factor two and Lorentz raising in the contraction. The original computed Ricci gives

    <Ric,H>_g=6 n^T S n.

Three coordinate n recover the three diagonal entries. The three rational directions (3e_i+4e_j)/5 recover each off-diagonal entry once diagonals vanish. Hence these six actual stationary-clock planes already force S=0 on this restricted image. They are not claimed to span all nine general tracefree response directions: the full G310/G311 theorem remains separately source-owned.

For a response E=a Ric+b Rg, <E,H>=6a n^T S n, since H is traceless. With a nonzero this makes S=0 necessary and sufficient for the pointwise center DDR balance, FOR THIS RESPONSE CLASS. This algebra does not establish class membership. G301's entire conditional naturality, local metric curvature/two-jet, symmetric rank-two, flat differentiability, exact weight-one homogeneity, scale and principal gates remain load-bearing. Current filter-only GR and Local Metric Sufficiency do not by themselves supply them. Nor does the center condition imply a full-neighborhood equation, determine c2, restrict higher jets or grant LSR1 native admission.

Run evidence: 8 exact cases, 6 coefficient-basis cases, 6,307 assertions including original Riemann symmetries and Bianchi, TF rank5, exit0, empty stderr, 0.0916843069717288 seconds. This is an independently implemented source-first exact arithmetic check plus linearity argument, not a fresh proof of every inherited LSR1/G301/G310/G311 theorem. The unrelated algebraic check length2/density2=1/f verifies the completion operation on a formal jet example; it is not a physical selection or exact higher-order area certificate.
