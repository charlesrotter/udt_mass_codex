# GRS1 discovery and repair history

Author selected the action comparison, scalar-flat witness and finite-jet
flattening argument analytically before freezing CHECK_PLAN.md. These are
exposed mathematical choices, not preregistered observational predictions.
The current literature and G301/G310/G312 were known. A separate source-first
reviewer independently reconstructed the same two routes before seeing the
candidate; its exposure and one self-correction are preserved under review/.

## Author check repair 1 — sensitive negative control

Initial exact run `checks/author_exact` exited1 at the assertion that the
algebraic-only R^2 response has nonzero divergence on A=t. Initial code is
preserved verbatim at initial_check/check_response.py; stdout/stderr and capture
metadata remain in place. No candidate equation or physical premise changed.

Reason: on that particular metric Ric_00=0. The incorrect response obtained by
dropping Hessian/box terms differs from the correct response, but its divergence
accidentally vanishes: div(2R Ric-(R^2/2)g)_b = 2 Ric_ab nabla^a R. Thus that
metric detects a response mismatch but is blind to the divergence defect.

Smallest repair: retain A=t as an explicit false-pass control and add A=t^2,
whose wrong response has divergence (-864/t^5,0,0,0). The exact Lagrangian-versus-
response comparisons still use general N(t),A(t), including lapse variation.
This is a same-premise diagnostic repair, not a changed target or discarded
failure. The rerun uses a new capture/output stem. The original analytic
candidate and pre-execution plan remain unchanged for review.
