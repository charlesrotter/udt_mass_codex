# Conditional C2 Finite-Cell Boundary-Variation Audit

Date: 2026-07-20  
Base: `eb06c7b5157ffb893ee3e6cd1d10de0816a07e3a`  
Preregistration commit: `b0a3e7d`  
Mode: CPU-only exact unrestricted variation followed by a bounded non-null boundary decomposition  
Status: **VERIFIED-WITH-CAVEATS** — exact primary algebra, independent curvature-momentum and
component boundary-split reconstruction, 57 base-source hash replays, and exercised fail-closed
catches pass; no fresh external-model review was authorized.

## Result first

The bare conditional four-dimensional `C^2` action tells us what the mathematical boundary phase
space is, but it does **not** tell us which physical boundary data the UDT finite cell uses.

For

`L = sqrt(|g|) C_abcd C^abcd`,

the curvature momentum is

`P^abcd = 2 C^abcd`,

and one covariant representative of the boundary symplectic potential is

`Theta^mu = 4 C^{mu a b nu} nabla_nu(delta g_ab)
            - 4 nabla_nu C^{mu a b nu} delta g_ab`.

The unrestricted bulk equation is proportional to the Bach tensor. That result remains inside the
already frozen `UNIQUE-CONDITIONAL` pre-scale action route; this audit does not promote `C^2` to the
complete native action.

On a fixed non-null boundary piece in Gaussian normal gauge, with

`K_ij=(1/2)partial_n h_ij`, `E^ij=C^{n i n j}`, and `n^2=epsilon`,

the normal flux decomposes as

`n.Theta = -8 epsilon E^ij delta K_ij
           + Pi_h^ij delta h_ij
           + 4 epsilon D_k(C^{n i j k}delta h_ij)`,

where

`Pi_h^ij = 8 epsilon E^{k(i}K_k^{j)}
           -4 epsilon nabla_nu C^{n i j nu}
           -4 epsilon D_k C^{n i j k}`.

The last divergence produces the edge flux

`4 epsilon s_k C^{n i j k}delta h_ij`.

Thus a fourth-order metric action naturally sees both the induced metric and its normal derivative,
plus corner data. The electric-Weyl momentum paired with `delta K` is trace-free.

## The decisive negative

Several inequivalent boundary choices make the variational problem differentiable:

- fix both `h` and `K` (a clamped two-jet wall);
- fix `h` and impose the natural trace-free electric-Weyl equation;
- fix `K` and impose the complementary induced-metric momentum equation;
- leave both free and impose both natural equations plus a corner condition;
- choose a mixed/Neumann polarization after deriving an additional integrable boundary functional;
- declare conformal-class data, for which the common-scale direction remains null.

Current UDT premises select none of them. This is not a failure of the variation. The variation did
its job: it exposed the exact slots a physical finite-cell rule would have to fill.

The smallest missing boundary selector is therefore a native rule specifying the allowed boundary
variation/polarization and its corner data. A physical charge additionally needs an integrable
primitive, reference, orientation, improvement, and normalization.

## CSN and the conformally flat branch

For a local common Weyl variation

`delta g_ab = 2 sigma g_ab`,

both terms in the bare potential vanish by the trace-free Weyl identity. The boundary phase space
therefore retains the CSN common-scale null direction; it does not choose an absolute representative.

More sharply, on a conformally flat branch `C_abcd=0`, both the bare potential and the bare
diffeomorphism Noether two-form vanish. This means the bare conditional `C^2` boundary objects cannot
select scale or furnish a normalized mass there.

It does **not** mean a conformally flat UDT solution is physically empty or has zero mass. Such a
claim would require the missing action completion, reference, source, and normalization.

## Bare Noether object

In the displayed conventions the unnormalized diffeomorphism two-form is

`Q_xi^{mu nu} = -4 C^{mu nu rho sigma} nabla_rho xi_sigma
                +8 xi_sigma nabla_rho C^{mu nu rho sigma}`.

The expression is mathematically derived inside the conditional action. Calling it energy or mass
would be premature: the overall action coefficient, potential improvement, integrability, primitive,
reference solution, boundary orientation, corner completion, and physical normalization remain open.

## Independent algebra

The independent verifier did not call the primary tensor routine. It reconstructed `C^2` on the six
independent orthonormal curvature planes and differentiated with respect to every plane curvature,
recovering `d(C^2)=2 C:dR` in all six directions.

For an algebraic product sample with sectional curvatures `K_01=2` and `K_23=3`, it independently
obtained

`R=10`, `C^2=100/3`, and `E=diag(5/3,-5/6,-5/6)`.

It also used explicit symmetric three-by-three tensors to reconstruct the normal connection terms
and reproduce the `-8 epsilon E:delta K` and `8 epsilon E^{k(i}K_k^{j)}delta h_ij` coefficients.
The tangential product rule and pure-Weyl trace cancellation were checked separately.

## Lay interpretation

We asked what happens when the conditional conformal-curvature law is varied in a universe with a
real edge instead of silently closing the geometry into a smooth cap.

The answer resembles a mechanical system whose endpoint has both a position and a slope. The math
shows the conjugate forces for both, and it shows an extra term wherever boundary pieces meet. But it
does not decide whether nature holds the endpoint position fixed, holds the slope fixed, lets both
adjust naturally, or uses some mixed rule.

So we found the boundary control panel, including all the labeled sockets. We did not yet find the
UDT instruction telling us which switches are connected.

One especially useful clue is that the whole panel goes electrically quiet on the conformally flat
round branch: the bare `C^2` boundary charge is zero there. That closes off the hope that the bare
conditional action's edge term alone secretly selects scale or mass.

## What this changes about the next step

The immediate next object should be a bounded **finite-cell seal to boundary-phase-space join audit**.
It should map the exact existing UDT seal, reciprocity, co-presence, `Xmax`, CSN, and bootstrap
statements—without strengthening them—onto the now explicit slots `h`, `K`, `E`, `Pi_h`, and corner
data.

If those premises populate one unique polarization, that is the missing join. If they populate only
a scalar seal value or admit several polarizations, the honest next numerical work is a comparative
branch census across all admissible boundary classes, not a solve under one favored wall. GPU work
would then become useful for nonlinear solution-space mapping; it is not useful for the exact algebra
completed here.

## Four evidence gates

1. **Preregistered:** yes, commit `b0a3e7d` before derivation.
2. **Full space or bounded scope justified:** unrestricted four-metric variation first; complete
   registered boundary-class census; decomposition bounded to fixed non-null Gaussian-normal pieces.
3. **Independently verified:** yes in-package by a separate six-plane curvature calculation and a
   component normal-split reconstruction; no fresh external-model review.
4. **Every premise audited:** yes for this slice; conditional `C^2`, non-null fixed wall, normal and
   extrinsic-curvature conventions, potential ambiguity, and excluded physical layers are explicit.

The correct grade is **VERIFIED-WITH-CAVEATS**, not a complete UDT boundary theorem.
