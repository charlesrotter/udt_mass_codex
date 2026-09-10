# Follow-up freeze: rotation-sensitive density omission and general tape transform

2026-09-10; CANDIDATE, UNPROMOTED, before follow-up confirmation. The first frozen
construction passed 67 exact checks (saved initial bytes unchanged). Its density-omission
control only separated marked metric coefficients. For the campaign's rotation question,
add a stronger control, analytically discovered after that first run:

    g_λ = -(dt+λ x dy)^2 + λ^2(dx^2+dy^2+dz^2), λ>0, U=∂t.

All constant-v records have T=1, m_v=λ|v| and B_v=x v_y/|v|. Thus deleting m
leaves identical normalized pair records as functions of the same coordinate markings
for all six directions, while the vorticity norm computed directly from the projected
antisymmetric derivative of U should be 1/(2λ²), in convention ω_ab=∇_[a U_b].
This is a targeted exact ambiguity witness, not minimality, physical acquisition or
a derived UDT solution. G166 keeps this in the supplied configuration envelope.

Also check the general actual tape-coordinate Jacobian with a=s_t and ds=a dt+m dσ:

    h'00=-T²(1-aB)²+a²/T²,
    h'01=-T²B(1-aB)-a/T²,
    h'11=T^-2-T²B²,
    det h'=-1.

The fixed-s clock is admissible only when -h'00>0. The original clock has new
components (1,a), retains norm -T², and differs from the fixed-s coordinate clock.

One new standalone SymPy script; no scientific-source implementation imports, no
original script changes. Exact CPU-only algebra, timeout120 seconds, no numerical
tolerance or grid. Preserve command/versions/source hashes/stdout/stderr/exit. Stop
after these bounded checks and hand the candidate to the parent's fresh review.
