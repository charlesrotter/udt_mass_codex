# Topology Classes the Closed-Cell Closure Admits

Date: 2026-06-13. Agent a35e82d660eaf218d; blind verifier
ab449c89db47f7f1d (its objection became the central finding). Scripts:
topo_classes_zoo.py (13/13), topo_d3_junction.py (7/7),
topo_doubling_fork.py (4/4). HYPOTHESIS-GRADE where flagged; needs a
second verifier on the doubling fork before canon. Topology only — no
dynamics, no mass-matching, no integer-invention.

## Result: genus is rigid; a WINDING family is possible and hinges on ONE open fact

- ESTABLISHED topology: the closed cell is the DOUBLE of a radial
  collar S^2 x I across the seal (mirror fold); angular factor = the
  2-sphere, chi=2, genus 0. The banked integral(omega_H1)=4pi is BOTH
  the Gauss-Bonnet number (chi=2 => g=0) AND the fundamental class
  (degree-1 wrap, generator of H^2(S^2,Z)). The transgression
  d[(ln f)omega_H1] is EXACT — its whole content is the seal endpoint
  value 4pi*[ln f]_seal, invisible to the bulk EL.
- GENUS tower => COLLAPSES to g=0 (sphere). SOLID: axis regularity =>
  two regular poles, each Poincare-Hopf index +1, total 2 = chi =>
  chi=2 => g=0 uniquely; higher genus (chi<=0) cannot carry two-pole
  axis regularity. NO GENUS FAMILY.
- WINDING / CHERN tower => FORK-DEPENDENT (the headline). Finite
  action does NOT cut it (integral n*omega = 4pi k finite for all k).
  chi=0 for every closed orientable 3-manifold, so it cannot decide;
  the decision is the INNER-END (matter-cell CORE) closure:
    * core caps regularly (areal r->0) => S^3, H^2=0 => winding killed
      => ONE rigid class (no family);
    * core is a finite second seal => S^2 x S^1, H^2=Z => a discrete
      INTEGER (Chern) FAMILY of particle types;
    * core glues with a p-fold twist => lens space L(p,q), H^2=Z/p =>
      a FINITE family of p types.
- The intrinsic chi=2 / 4pi class (where the banked N=3, q=1/3 live —
  two locks: C(N,3)=1 unique at N=3; C(N^2,2)=4N^2 => N=3; re-stated,
  NOT extended; {3,5,7} stays rejected #35) SURVIVES every branch (it
  is the Euler class of TS^2, not a bounding class).

## D3 CORRECTION to registry #36 (verifier-confirmed)

#36 placed the transgression in the sigma-ODD/Dirichlet sector via a
"radial orientation reversal." OVERTURNED. The same-minus involution
sigma:(a,b)->(-a,-b) is TIME-REVERSAL — it touches ONLY the time row;
r, theta, phi, f, omega_H1 are all sigma-INVARIANT. So
Theta=(ln f)omega_H1 is sigma-EVEN and glues SYMMETRICALLY (NOT
antisymmetrically). The topological 2-form sits in the sigma-EVEN
(static-geometry) sector, NOT odd/Dirichlet. Topology is invisible to
dynamics because the transgression is EXACT, not because of parity.

## The deciding open fact = the next push

DERIVE THE MATTER-CELL CORE CLOSURE: the areal radius at the
phi->-infinity core, from the metric's own radial profile. r->0 =>
S^3 => ONE rigid particle topology (no family); finite r => S^2 x S^1
=> an integer family of particle types; p-twist => a finite p-family.
Canon pins the UNIVERSE cell core (->S^3, rigid) but leaves the MATTER
(particle) cell core OPEN. This single radial-endpoint calculation
converts the winding-family hypothesis into a result and answers
"how many particle types / are there families."
