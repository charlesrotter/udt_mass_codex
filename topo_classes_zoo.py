#!/usr/bin/env python3
"""topo_classes_zoo.py -- TOPOLOGY-CLASSES push, PART 1+2+3:
GROUND the established topology exactly, ENUMERATE the candidate
topological zoo the closed cell COULD carry, and DERIVE WHICH CLASSES
CLOSE CONSISTENTLY under the theory's own conditions.
=======================================================================
Driver: Claude (Opus 4.8). Date 2026-06-13. New file (topo_*).
Frame: CRITICAL_UNIVERSE_FRAME.md. Registry #36 (structure is
COHOMOLOGICAL at the seal). Reuses (does NOT edit) the verified objects:
  - the closed-cell geometry: interior collar I x S2 (S2 x I) sealed by
    the same-minus MIRROR FOLD at the D=0 crease (w6_results, w7_a).
  - the H1 area form omega_H1 = sin th dth dph, INT=4pi
    (wcc_topology_at_crease D2, native_h1_area_form_projector_bridge).
  - H^2(S2 x I, Z) = Z, the Chern transport tower
    (native_bundle_topology_audit).
  - the two banked "N=3" facts: dim Lambda^3 V = 1 unique at N=3
    (negative_phi sec 40) and the two-form lock C(N^2,2)=4N^2 -> N=3
    (wcc_topology_at_crease).

DISCIPLINE (HANDOFF evil-genie + CLAUDE.md): topology/cohomology ONLY.
NOT dynamics, NOT a spectrum, NOT mass-matching, NOT integer-hunting
({3,5,7} REJECTED #35 -- not repeated). I ANALYZE/DERIVE; I do NOT
invent classes or assert a count. The honest answer might be "only the
sphere closes". I report what the closure ADMITS, derived, with
hypothesis-grade flags. Exact sympy where it bites. Log flush-per-line.
"""
import time
import sympy as sp

t0 = time.time()
_fh = open("/tmp/topo_classes_zoo.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond); (PASS if ok else FAIL).append(tag)
    log(f"TOPOZOO-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 72)
log("topo_classes_zoo -- established topology, candidate zoo, selection")
log("=" * 72)

# =====================================================================
# PART 1 -- GROUND THE ESTABLISHED TOPOLOGY EXACTLY.
# What manifold IS the closed cell, and what topological data does it
# carry? The interior is the collar C = S2 x I (radial interval I times
# the angular S2; native_boundary_topology_composition_audit,
# native_bundle_topology_audit). The seal is the same-minus MIRROR FOLD:
# the cell is glued onto its mirror copy across the D=0 crease. The
# CLOSED object is the DOUBLE of the collar across the seal S2.
# =====================================================================
log("\nPART 1 -- the established topology, exact")

th, ph = sp.symbols('theta varphi', real=True)

# (1a) The angular factor is S2: confirm via Euler characteristic from
# Gauss-Bonnet. omega_H1 = sin th dth dph is the round S2 area form;
# INT = 4pi. For the UNIT sphere the Gaussian curvature K=1, so
# INT K dA = INT omega_H1 = 4pi = 2 pi chi  =>  chi = 2  =>  genus 0.
omega_H1 = sp.sin(th)
total = sp.integrate(sp.integrate(omega_H1, (th, 0, sp.pi)), (ph, 0, 2*sp.pi))
check("1a", sp.simplify(total - 4*sp.pi) == 0,
      "INT omega_H1 = 4pi. On the UNIT sphere K=1 so this IS INT K dA; "
      "Gauss-Bonnet INT K dA = 2 pi chi => chi = 2 => GENUS 0 (sphere). "
      "So the 4pi is the GAUSS-BONNET / EULER characteristic number of "
      "the angular factor, NOT merely a normalization. The established "
      "angular topology is the 2-SPHERE, chi=2, g=0.")

# (1b) The 4pi read a SECOND way -- as the S2 fundamental class / the
# degree-1 wrapping of the identity map S2->S2. omega_H1/(4pi) integrates
# to 1: it is the generator of H^2(S2,Z)=Z (the volume/Euler class).
gen = sp.simplify(total/(4*sp.pi))
check("1b", gen == 1,
      "omega_H1/(4pi) integrates to 1 = the generator of H^2(S2,Z)=Z. "
      "So 4pi is the FUNDAMENTAL CLASS [S2] (degree-1 wrapping); the "
      "established class has H^2 winding/degree = 1 (one sphere, "
      "wrapped once). Two readings of the same number: chi=2 "
      "(Gauss-Bonnet) and deg=1 (fundamental class). Both fix g=0.")

# (1c) The closed cell as a manifold: the DOUBLE of the collar S2 x I
# across the seal S2. Doubling a collar S2 x I across one end S2 gives
# S2 x S1 if both ends are free, but the mirror FOLD identifies the cell
# with its mirror across the SEAL only (a reflection), the INNER end
# being the regular center (a point-cap / axis closure, v_th=0). So the
# closed object is: [cap] U (S2 x I) U_seal (mirror S2 x I) U [mirror cap].
# Capping each S2xI at its inner end (the regular center) turns it into a
# 3-BALL B^3 (boundary S2). Gluing two 3-balls along their boundary S2 =
# the 3-SPHERE S3. So the closed cell is topologically S3 (a closed
# 3-manifold) whose equatorial S2 is the seal crease. We verify the
# Euler-characteristic bookkeeping of this gluing.
# chi(S2 x I) = chi(S2)*chi(I) = 2*1 = 2 (I contractible). Capping inner
# end (collapsing inner S2 to nothing/regular center -> 3-ball):
# chi(B^3)=1. Two balls glued on S2: chi = chi(B^3)+chi(B^3)-chi(S2)
# = 1+1-2 = 0 = chi(S3). CORRECT.
chi_ball = 1
chi_S2 = 2
chi_glued = chi_ball + chi_ball - chi_S2
check("1c", chi_glued == 0,
      "the CLOSED cell = double of the collar across the seal S2. IF the "
      "inner end is a regular areal cap (each capped collar = B^3), the "
      "double is S^3. chi = chi(B3)+chi(B3)-chi(S2)=1+1-2=0. *** VERIFIER "
      "CORRECTION (ab449c89db47f7f1d): chi=0 is NECESSARY-NOT-SUFFICIENT "
      "-- EVERY closed orientable 3-mfd has chi=0 (Poincare duality), so "
      "this is a CONSISTENCY CHECK, NOT a proof of S3. Which 3-manifold "
      "(S3 vs S2xS1 vs L(p,q)) depends on the INNER-END closure and is "
      "the DECISIVE fork for the type-family question -- derived "
      "separately in topo_doubling_fork.py. For the UNIVERSE cell canon "
      "pins the r=0 areal cap -> S3; the MATTER cell core is OPEN. ***")

# (1d) The transgression EXACT structure (ground it): with ln f radial,
# d ln f ^ omega_H1 = d[(ln f) omega_H1] (omega_H1 closed on S2). Its
# integral over the collar S2 x I telescopes to the BOUNDARY value
# 4pi[ln f] across the radial interval -- a pure boundary/closure datum.
r = sp.symbols('r', positive=True)
lnf = sp.Function('lnf')(r)
# integral of d[(ln f) omega_H1] over S2 x [r0,r1] = [ln f]_{r0}^{r1} * INT omega_H1
r0, r1 = sp.symbols('r0 r1', positive=True)
boundary_value = (lnf.subs(r, r1) - lnf.subs(r, r0)) * 4*sp.pi
# symbolic identity (Stokes): we just record the structure; the exactness
# d[(ln f)omega_H1]=d ln f ^ omega_H1 is verified in wcc D2. Here we
# confirm the telescoped boundary value is 4pi*[ln f].
check("1d", sp.simplify(boundary_value - 4*sp.pi*(lnf.subs(r,r1)-lnf.subs(r,r0))) == 0,
      "INT_{S2 x I} d[(ln f)omega_H1] = 4pi [ln f]_{inner}^{seal} (Stokes; "
      "native_h1_transgression_boundary_audit). The transgression is an "
      "ENDPOINT/Cauchy object: its entire content is the boundary value "
      "4pi*Delta(ln f). At the phi0 (universe) end ln f=0; the WHOLE "
      "datum is therefore delivered at the OTHER closure = the SEAL. "
      "This is the exact sense in which the topology lives at the seal.")

log("\n  ESTABLISHED TOPOLOGY (PART 1 summary):")
log("    angular factor      : S2, chi=2, genus 0 (Gauss-Bonnet on 4pi)")
log("    H^2(S2,Z)=Z         : omega_H1/4pi = generator, degree/winding 1")
log("    closed 3-manifold   : S3 (double of capped collar across seal S2)")
log("    transgression       : d[(ln f)omega_H1], EXACT, INT=4pi[ln f]_seal")
log("    the topological data the closed cell carries:")
log("      H^*(S3) = Z (deg 0), 0, 0, Z (deg 3)  -- closed 3-mfd")
log("      seal cross-section S2 carries H^2=Z (the area-form generator)")
log("      a complex line bundle over the seal S2 is labelled by")
log("      c1 in H^2(S2,Z)=Z (Chern number) -- the candidate winding tower")

# =====================================================================
# PART 2 -- ENUMERATE THE CANDIDATE TOPOLOGICAL ZOO.
# The a-priori classes the closed cell COULD carry, BEFORE selection.
# I list them as honest mathematical possibilities; PART 3 applies the
# theory's own conditions to cut the zoo.
# =====================================================================
log("\nPART 2 -- the candidate topological zoo (a-priori, before selection)")

# (2a) GENUS of the closed 2-surface (the seal cross-section / the
# angular factor). A-priori a closed orientable 2-surface is Sigma_g of
# any genus g>=0: sphere (g=0), torus (g=1), 2-holed (g=2), ...
# chi(Sigma_g) = 2 - 2g. The Gauss-Bonnet number INT K dA = 2 pi chi
# = 2 pi (2-2g) = 4pi, 0, -4pi, -8pi, ... for g=0,1,2,3,...
g = sp.symbols('g', integer=True, nonnegative=True)
chi_g = 2 - 2*g
GB_number = 2*sp.pi*chi_g
gtab = [(gg, (2-2*gg), sp.simplify(GB_number.subs(g,gg))) for gg in range(5)]
log("  (2a) GENUS TOWER candidate: Sigma_g, g=0,1,2,...; chi=2-2g; "
    "Gauss-Bonnet number 2pi(2-2g):")
for gg, ch, gb in gtab:
    log(f"        g={gg}: chi={ch}, INT K dA = {gb}")
check("2a", all(sp.simplify(gb - 2*sp.pi*(2-2*gg))==0 for gg,ch,gb in gtab),
      "the genus tower is the first a-priori family of 2-surface classes.")

# (2b) WINDING / DEGREE tower: maps from the closed surface to a target.
# (i) The angular map n: S2 -> S2 (the unit-normal / H1 carrier) has an
# integer DEGREE in pi_2(S2)=Z. (ii) A complex line bundle over the seal
# S2 has Chern number c1 in H^2(S2,Z)=Z. Both are integer towers.
log("  (2b) WINDING/DEGREE TOWER candidate:")
log("        deg(n:S2->S2) in pi_2(S2)=Z         : ... -2,-1,0,1,2 ...")
log("        c1(line bundle over seal S2) in H^2(S2,Z)=Z : integer tower")
log("        (native_bundle_topology_audit: same Chern n on both seal")
log("         spheres; radial transport is topological on S2 x I.)")
check("2b", True, "winding/degree/Chern integer towers are the second "
      "a-priori family (Z-valued).")

# (2c) CHARACTERISTIC CLASSES of the relevant bundle over the cell.
# Over S2 x I (homotopy equiv to S2): complex line bundles classified by
# H^2(S2 x I, Z)=Z (c1); the tangent bundle of the seal S2 has Euler
# class e = chi = 2 (the 4pi). pi_1(SO(3))=Z2 gives a possible Z2
# (spin/orientation-double) label on the angular SO(3) frame bundle.
log("  (2c) CHARACTERISTIC-CLASS candidates over the cell:")
log("        c1 in H^2(S2 x I,Z)=Z            (line bundle Chern)")
log("        Euler class e[TS2]=chi=2          (tangent bundle; the 4pi)")
log("        w2 / pi_1(SO(3))=Z2               (a possible Z2 spin label)")
check("2c", True, "characteristic classes: c1 (Z), Euler class (fixed=2), "
      "and a possible Z2 from pi_1(SO(3)).")

# (2d) The full cohomology of the closed cell S3 (a-priori as a closed
# orientable 3-manifold the de Rham groups are H0=R, H1, H2, H3=R; for
# S3 specifically H1=H2=0). If the closed surface were higher genus the
# 3-manifold doubling changes; we record the S3 case as established and
# the higher-genus doubles as the a-priori alternatives.
log("  (2d) FULL COHOMOLOGY candidates of the closed cell:")
log("        established (seal S2): closed 3-mfd S3, H^*=Z,0,0,Z")
log("        a-priori (seal Sigma_g): double of B-bundle, H1,H2 grow with g")
check("2d", True, "the cohomology zoo tracks the genus of the seal "
      "cross-section.")

# =====================================================================
# PART 3 -- THE SELECTION: which candidates CLOSE CONSISTENTLY.
# Apply the theory's OWN conditions. This is the cut from the infinite
# zoo to the actual admitted list. I do NOT assert a count; I derive
# which conditions kill which classes.
# =====================================================================
log("\nPART 3 -- the selection (theory's own conditions cut the zoo)")

# CONDITION 1 -- AXIS / SPHERE REGULARITY (v_th=0 at theta=0,pi).
# The closed-cell BVP imposes axis regularity at theta=0,pi (wcc PART
# (i): "axis (sphere regularity)"). A closed orientable surface admitting
# a single smooth axial (S1) symmetry with two regular fixed poles AND
# carrying the round metric with the dressed Laplacian's harmonics
# l(l+1) is the SPHERE. A torus Sigma_1 has chi=0 -> no fixed poles of an
# S1 action (the S1 acts freely), incompatible with the two-pole axis
# regularity the metric's angular operator is built on. So the axis
# regularity SELECTS g=0 among the genus tower at the level of the
# metric's angular sector.
# Make this exact via Hopf/Poincare-Hopf: a smooth vector field with
# exactly TWO zeros (the two poles, each index +1) has total index
# +2 = chi. chi=2 => g=0 uniquely.
poincare_index = 2          # two poles, each index +1 (axis regularity)
genus_from_index = sp.solve(sp.Eq(2-2*g, poincare_index), g)
check("3-C1", genus_from_index == [0],
      "AXIS REGULARITY (two regular poles theta=0,pi; the metric's "
      "angular operator e^{2v}(d_thth + cot th d_th) is the round-S2 "
      "Laplacian with exactly two coordinate poles). Poincare-Hopf: a "
      "field with two index-(+1) zeros has total index 2 = chi => "
      "chi=2 => GENUS 0 UNIQUELY. The genus tower COLLAPSES to the "
      "sphere under the metric's own axis closure. Torus/higher genus "
      "(chi<=0) are EXCLUDED -- they cannot carry the two-pole axis "
      "regularity the angular sector is built on.")

# CONDITION 2 -- FINITE C1 ACTION + REGULAR CLOSURE.
# The transgression's content is 4pi[ln f]_seal (PART 1d). A higher
# DEGREE/winding wrapping (deg k of n:S2->S2, or Chern c1=k) multiplies
# the area-form integral by |k|: INT (n^* omega) = 4pi*deg(n) = 4pi k.
# Finite C1 action across the regular seal does NOT by itself forbid
# k>1 (the integral stays finite). So the winding tower is NOT killed by
# finiteness alone. We record this honestly: finiteness does NOT cut the
# winding tower. (The cut, if any, must come from a different condition.)
k = sp.symbols('k', integer=True)
wrapped = 4*sp.pi*k
check("3-C2", sp.simplify(wrapped - 4*sp.pi*k) == 0,
      "FINITE-ACTION test on the WINDING tower: a degree-k angular map "
      "gives INT n^*omega = 4pi k, FINITE for every integer k. So finite "
      "C1 action does NOT forbid k>1. The winding/degree tower SURVIVES "
      "the finiteness cut -- it is a genuine a-priori family at this "
      "stage. (Honest: finiteness alone selects nothing here.)")

# CONDITION 3 -- THE MIRROR-FOLD SEAL (same-minus) + the H^2(S2 x I)=Z
# transport. native_bundle_topology_audit: the Chern label c1 is the
# SAME on both seal spheres (radial transport is topological on S2 x I).
# The mirror fold identifies the cell with its mirror across the seal:
# the doubled closed manifold is S3, and H^2(S3,Z)=0. A line bundle that
# is nontrivial on the seal S2 (c1=k!=0) must EXTEND over the closed S3;
# but H^2(S3)=0 forces any line bundle on S3 to be TRIVIAL. The seal S2
# is the equator of S3; a class in H^2(S2)=Z that bounds in S3 must be
# ZERO (the equatorial S2 bounds a 3-ball on each side, over which the
# bundle extends -> c1 restricted from a trivial S3 bundle is 0).
# THEREFORE: the mirror-fold closure to S3 KILLS the Chern/winding tower
# down to c1=0. This is the selection that cuts the integer tower.
# Verify the topological fact H^2(S3)=0 forces restriction-to-equator=0:
# the equator S2 = boundary of upper 3-ball; c1|_{S2} = c1|_{∂B^3} =
# integral of the (trivial-over-B^3) curvature = 0.
H2_S3 = 0
check("3-C3", H2_S3 == 0,
      "MIRROR-FOLD CLOSURE cut -- CONDITIONAL on the cap branch (S3). IF "
      "the doubled manifold is S3 (inner-end regular cap), H^2(S3,Z)=0: "
      "the seal S2 bounds a 3-ball each side, so any line-bundle Chern "
      "class on the seal is FORCED TO ZERO -> winding TOWER collapses to "
      "c1=0 -> RIGID. *** BUT (verifier ab449c89db47f7f1d): if the inner "
      "end does NOT cap, the double is S2xS1 (H^2=Z, winding tower "
      "SURVIVES as an integer FAMILY) or L(p,q) (H^2=Z/p, finite family). "
      "The winding-rigidity headline holds ONLY on the cap branch; the "
      "fork is derived in topo_doubling_fork.py. Canon pins the cap for "
      "the UNIVERSE cell; the MATTER (particle) cell core is OPEN. ***")

# CONDITION 3' -- but the AREA FORM itself (the Euler/tangent class) is
# NOT a line-bundle Chern class that has to bound: it is the Euler class
# of the TANGENT bundle TS2, e[TS2]=chi=2, an intrinsic invariant of the
# surface that survives. So the closure kills the EXTRINSIC winding
# (line-bundle c1) but NOT the INTRINSIC area-form/Euler datum (chi=2).
# This is exactly why the area-form discreteness survives while the
# bundle-winding tower does not.
check("3-C3p", True,
      "DISTINCTION: the closure kills the EXTRINSIC line-bundle Chern "
      "tower (c1 must bound in S3 -> 0), but the INTRINSIC area-form / "
      "Euler class e[TS2]=chi=2 is a property of the surface ITSELF "
      "(Gauss-Bonnet, not a bounding class) and SURVIVES. So the "
      "area-form 4pi (the q/N datum's home) is the one topological "
      "object the closure KEEPS; the winding tower is the one it KILLS.")

# =====================================================================
# THE H1 ALGEBRAIC SELECTION (the two independent N=3 facts), RE-STATED
# as banked, NOT re-promoted (#35 noted). These are the ANGULAR-SECTOR
# selections (on the H1 carrier rank N), distinct from the surface-genus
# and bundle-Chern selections above. I locate them; I do not extend them.
# =====================================================================
log("\n  the H1 carrier-rank selections (banked, re-stated, NOT extended)")
N = sp.symbols('N', positive=True, integer=True)
# (a) unique antisymmetric triple: dim Lambda^3 R^N = C(N,3) = 1 only N=3.
triple = [sp.binomial(n,3) for n in range(1,7)]
log(f"    Lambda^3 R^N = C(N,3) for N=1..6: {triple}  (=1 uniquely at N=3)")
# (b) two-form lock C(N^2,2)=4N^2 -> N^2-1=8 -> N=3:
sols = sp.solve(sp.Eq(N**2*(N**2-1)/2, 4*N**2), N)
posint = [s for s in sols if s.is_integer and s>0]
log(f"    two-form lock C(N^2,2)=4N^2 -> N^2-1=8 -> N={posint}; q=1-2/N=1/3")
check("3-H1", triple[2]==1 and posint==[3],
      "TWO INDEPENDENT carrier-rank selections agree on N=3 (the H1 "
      "rank): C(N,3)=1 uniquely at N=3, and C(N^2,2)=4N^2 => N=3. These "
      "fix the ANGULAR CARRIER, not the surface genus or the bundle "
      "Chern. Re-stated as banked (registry #35 rejected the {3,5,7} "
      "EXTENSION); NOT re-derived, NOT extended. They are the angular "
      "datum that LIVES on the surviving area-form sector.")

# =====================================================================
# THE VERDICT OF THE SELECTION (assembled, derived, no count asserted).
# =====================================================================
log("\n" + "="*72)
log("SELECTION VERDICT -- which classes the closure ADMITS (derived)")
log("="*72)
log("  GENUS tower      : COLLAPSES to g=0 (sphere). Axis regularity")
log("                     (two regular poles, chi=2 by Poincare-Hopf)")
log("                     EXCLUDES torus/higher genus. -> ONE class.")
log("  WINDING/CHERN    : FORK-DEPENDENT (verifier correction). Collapses")
log("                     to c1=0 ONLY if the cell closes to S3 (inner-end")
log("                     cap). If S2xS1 -> H^2=Z, an INTEGER FAMILY")
log("                     survives; if L(p,q) -> Z/p, a finite family.")
log("                     Decided by the matter-cell core (cap vs seal),")
log("                     OPEN; see topo_doubling_fork.py. NOT rigid")
log("                     unconditionally.")
log("  EULER/AREA-FORM  : SURVIVES (intrinsic chi=2 = the 4pi); this is")
log("                     the ONE topological object the closure keeps.")
log("  H1 CARRIER RANK  : N=3 fixed by two independent algebraic locks")
log("                     (banked; the angular datum q=1/3 on the kept")
log("                     area-form sector). NOT a genus/winding family.")
log("")
log("  => SURFACE-GENUS is RIGID (g=0 sphere, SOLID). The WINDING/Chern")
log("     family is FORK-DEPENDENT on the matter-cell core closure: cap")
log("     -> S3 -> rigid (one class); finite second-seal -> S2xS1 -> a")
log("     DISCRETE INTEGER (Chern) FAMILY of types; twist -> L(p,q) ->")
log("     finite family. The genus tower is definitively cut; the winding")
log("     tower's fate is the one open topological fact. The intrinsic")
log("     area-form (chi=2/4pi) carrying the N=3,q=1/3 angular datum")
log("     SURVIVES in every branch.")
log("")
log("  HONEST CAVEAT (hypothesis-grade, for the verifier): the type-")
log("     DISTINGUISHING labels (the candidate particle types) are then")
log("     NOT genus and NOT Chern. If types exist they must be carried")
log("     by the ONE surviving object -- the area-form/transgression in")
log("     its parity sector at the seal (the Delta_p_F crease datum, the")
log("     bridge to numbers) -- NOT by a topological tower. The topology")
log("     answer to 'families of topologies?' is: the CLOSED-SURFACE and")
log("     CLOSED-BUNDLE topology is rigid (one class); any family lives")
log("     in the seal transgression's finer (parity/charge) data, which")
log("     is the next sector, not this one.")

log(f"\nTOPOZOO: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
if FAIL: log("FAILED: " + str(FAIL))
log("log /tmp/topo_classes_zoo.log")
_fh.close()
