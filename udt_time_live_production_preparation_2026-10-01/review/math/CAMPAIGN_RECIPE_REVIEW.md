# Finite campaign recipe extension

This is a later scoped extension of `/root/tpp_math`'s substantive review,
not a revision of its fixed source bindings. The parent requested inspection
of the proposed finite preview before final integration. No campaign was
emitted and no new geometry was evolved by this check.

Let J be cross product with the unit wavevector. On its transverse plane,
J is antisymmetric, J²=-I, and a symmetric traceless T has two independent
components. The tensor U=(JT-TJ)/2 is symmetric and traceless, is transverse,
has the same Frobenius norm as T, and is Frobenius-orthogonal to T. Thus
cos(2theta)T+sin(2theta)U is TT with unchanged norm. It is exactly
R(theta) T R(theta)^T with the spatial Rodrigues rotation about that
wavevector. This is a supplied polarization choice, not a UDT selector.

`check_campaign_modes.py` calls the pure recipe only. It independently forms
the baseline tensors by an SVD transverse basis, then applies Rodrigues
rotations and compares all288 oblique modes. Symmetry, trace, transversality,
normalization, amplitudes and phase offsets pass. The six axial plus72 oblique
datasets give78 supplied datasets and234 proposed24-coarse/24-fine/32-coarse
runs. The test does not prove their physical inequivalence or exhaustive
coverage. Every future conformal initial solve and history retains its own
original constraints, residual/refinement and readout gates.

The proposed source bindings should include the three read specification
templates as well as generated specification hashes; this provenance point
was reported to the parent. It does not alter the tensor construction.
Final dispatch/runtime and integration attestation remain separately scoped.
