# GRC1 fidelity independent check declaration

Question: do the original reciprocal spherical metric and actually released
quartic clock geodesics support the candidate curvature/sign/optical statements
and the finite proper-arrival derivatives? Metric-led supplied controls only.

Exact part: smooth f(r)>0, r>0, regular angular chart, c_E=1. Compute the
Levi-Civita connection and selected curvature contractions from the original4D
diagonal metric, then specialize to the free quartic and Kottler controls. Test
the null radial/nonradial contrast and an actual finite boosted plane which
violates directional S despite unboosted signs and zero null Ricci. Exact
symbolic equality is the criterion. A few controls do not prove universal S.

Floating part: free-and-explored lambda=1, r0=1/4, f=1-r^4, fixed released
worldline prepared at rest in its local static frame. The source proves this is
parallel preparation; independently verify that cancellation symbolically.
Integrate the original proper-time geodesic equations for (t,r,t',r'), without
inserting the conserved energy relation into the evolution. Integrate only to
proper time0.7, safely inside the patch. Exact radial optical function
rstar=(atanh r+atan r)/2 supplies outgoing/return null incidence. Solve the
outgoing incidence independently for emissions0,+h,-h; finite-difference actual
arrival proper times and actual returned central times. Two float64 resolutions
(rtol1e-11/1e-12, atol1e-13/1e-14, maxstep0.003/0.0015,
h0.0002/0.0001) check sensitivity. Require slope refinement and endpoint agreement
<2e-9, original normalized tangent and Killing-energy residuals<1e-10, and original
incidence residual<1e-12. These are diagnostics, not rigorous error or interval
bounds. The analytic sign proof remains load-bearing, rather than tolerance.

Compare independently computed derivatives with saved producer raw arrivals and
their reported derivatives. No producer routine is imported. Producer candidates
and raw stdout are exposed; producer code not yet read at implementation time.

One short CPU process, one BLAS thread, 2GiB virtual limit, existing TPS1 capture,
no CPU/wall killing timeout, manual interruption honored. Parent cleared the
slot after A's last check. Unique output under review_fidelity/checks; expected
under1MiB. No GPU, production evolution, installs, empirical fit, protected work,
global stability, matter, optical brightness or native admission. A symbolic or
numeric failure is preserved for diagnosis rather than overwritten.
