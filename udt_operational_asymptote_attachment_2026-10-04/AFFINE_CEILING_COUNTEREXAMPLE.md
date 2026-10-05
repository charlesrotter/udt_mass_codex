# A finite affine limit is not a universal ceiling in this conditional family

Discovery belongs to /root/oaa_math's independent source-first work. Its actual
nonradial incidences at60/100digits show an above-limit approach for

    m=1, a=3001/1000, H=9/50, E=1,
    b_* = -(999/1000) a/sqrt(f(a)).

These satisfy the conditional source bounds a>3m, positive Omega² and f(a),
and a strict source-ray margin. This is an allowed circular test geodesic, not
a claimed stable orbit, real source population or admitted UDT cosmology.
Choose t_*=0, u_infinity=U_infinity(b_*), phi_0=-P_infinity(b_*).
Then the limiting equations hold exactly; their nonzero Jacobian supplies the
actual late branch. No early-epoch or image/winding uniqueness follows.

Write S=sqrt(1+H²b_*²), J=S C(b_*) and

    B=J/H-E/(H² S), D_o=1/H+B/R+O(R^-2).

Parent check_ceiling_exact.py supplies a distinct exact rational sign proof,
not only a second floating-point evaluation. For r>=a>3m, w(r)=s(r)/S
increases, is positive and remains below1. Hence S/s decreases. On each of
nine rational subintervals of [a,6], the exact rational lower bound q_j at
the right endpoint satisfies q_j² w(r_right)²<=1. Therefore

    J = -a+integral_a^infinity(S/s-1)dr
      > sum_j (r_right-r_left) q_j - 6 = J_lower.

The omitted tail is strictly positive. A rational S_lower=14/5 has
S_lower²<S². The script checks exactly H S_lower J_lower-E>0, hence

    B > J_lower/H-E/(H² S_lower) > 0.

All inputs, nine rational bounds and the positive rational lower bound for B
are in CEILING_EXACT_RESULT.json; no floating-point tolerance owns this sign.
Consequently sufficiently late receptions lie above1/H while approaching it.
This refutes a universal below-limit/maximum interpretation of1/H across the
declared conditional family. It does not refute the particular b_*=0 tail,
whose opposite sign was proved, or a differently specified physical distance.
No full-history reversal, observational exclusion or native UDT failure follows.
