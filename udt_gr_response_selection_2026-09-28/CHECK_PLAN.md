# GRS1 exact-check plan

Frozen before execution of the author checks. Mathematical exploration preceded
this plan: inverse-metric variation, normal-coordinate scaling and the scalar-flat
metric below were selected analytically. There was no numerical/observational
search or fitting. The expected conclusions are disclosed, not blind predictions.

Question: do the displayed local identities and comparison witness hold exactly,
and are the premises of the conditional classification kept separate from UDT
ownership? Quantifier: general smooth finite metric jets for the analytic proof;
the computations cover the explicitly stated homogeneous diagonal metric family
and algebraic controls only. No sample census certifies the general theorem.

Frame: metric-led differential geometry, signature (-+++), Levi-Civita connection,
Ric_ab = d_c Gamma^c_ab - d_b Gamma^c_ac + Gamma^c_cd Gamma^d_ab
- Gamma^c_bd Gamma^d_ac. Free-and-explored comparison metric
diag(-N(t)^2,A(t)^2,A(t)^2,A(t)^2), N,A>0. It is not a UDT cosmology or a
preferred-observer assumption. EH and R^2 are unadopted comparison functionals.
Physical source, boundary law, observations, propagation/stability and global
completion are omitted. Compactly supported variations justify integrations by
parts. The homogeneous variational check uses density per unit coordinate spatial
volume (equivalently a comparison torus); it establishes only reduced identities,
not sufficiency of symmetry-reduced variations for the full field equations.

1. Compute connection and Ricci directly from the original metric; contract R.
2. Compute E_R and E_R2 using the analytic first-variation formula. Independently
   differentiate the reduced Lagrangian N A^3 f(R) with respect to both N and A,
   retaining the lapse until after variation; compare both Euler derivatives.
3. Check divergence of each response and trace E_R2=6 box R on this family.
4. At N=1,A=sqrt(t), t>0, check R=0, E_R2=0 and TF(Ric)!=0. Retain exact values.
5. Use N=1,A=t (nonconstant R) to reject omission of derivative terms. Check the
   response computed from lambda^2 g has weights 0 (EH) and -2 (R^2), not by
   substituting the desired answer into a scaling rule.
6. Reject wrong TF coefficient 1/3 in four dimensions and scalar-only response
   falsely treated as a nontrivial reciprocal equation. Explicitly show a constant
   trace term cannot be selected by reciprocal testing.
7. Enumerate weighted jet monomials through order8 as a finite regression of the
   degree2 argument; analytic flattening-ray proof owns arbitrary finite order.

Use Python3/SymPy exact arithmetic, no tolerance or floating-point certification.
One author CPU thread, capture900s/2048MiB; reviewer at most2CPU/1536MiB so combined
cap4CPU/4GiB is respected with the premise audit's single process. Preserve all
failures and exact commands, stdout/stderr, versions and runtime. No overwrite of
check captures. Maximum claim: exact stated examples and a reviewed conditional
argument. Fresh reviewer source-first reconstruction precedes candidate exposure.
