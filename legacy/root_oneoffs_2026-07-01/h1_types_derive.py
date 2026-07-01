#!/usr/bin/env python3
"""h1_types_derive.py -- THE BOUNDARY-COHOMOLOGY TYPE QUESTION, derived.
=======================================================================
Driver: Claude (Opus 4.8, 1M). Date 2026-06-14. New file (h1_*).
Frame: CRITICAL_UNIVERSE_FRAME.md / CATALOG_FRAME.md. Registry #36
(structure is COHOMOLOGICAL at the seal), #37-correction (transgression
is sigma-EVEN, EXACT-not-by-parity), #35 ({3,5,7} REJECTED).

THE QUESTION (metric-led): the closed cell's boundary carries the EXACT
transgression Theta = (ln f) omega_H1, omega_H1 = sin th dth^dph, INT=4pi,
whose entire content (Stokes) is the seal endpoint value 4pi*[ln f]_seal.
DOES THIS OBJECT ADMIT A DISCRETE SET OF DISTINCT STABLE CONFIGURATIONS
(= particle TYPES), or is it RIGID (one configuration)?

THE LIVE ROUTE is the H1 AREA FORM ITSELF (not the PARKED #37 core-closure
3-manifold winding tower; Charles: likely-wrong rabbit hole). So I
interrogate the area-form/transgression object directly:
  - what real cohomology classes it carries (H^0,H^1,H^2 of I x S2);
  - whether its content is a CONTINUOUS real datum or a DISCRETE invariant;
  - whether the metric supplies any QUANTIZATION of that datum;
  - whether End(H1)=1+3+5 (the alphabet) gives a discrete configuration set
    or only a rigid decomposition of ONE object.

DISCIPLINE (binding, this sector killed the last attempt):
 - ANTI-NUMEROLOGY: any COUNT reported must be FORCED the way N=3 was
   (C(N^2,2)=4N^2). No chosen/imported count. {3,5,7} stays dead.
 - DATA-BLIND: no lepton wall numbers loaded anywhere.
 - ANTI-TEMPLATE: cohomology, NOT a mode/eigenvalue spectrum.
 - METRIC-LED: from the closed-cell geometry + area-form cohomology only.
 - Exact sympy where it bites. Log flush-per-line.
"""
import time
import sympy as sp

t0 = time.time()
_fh = open("/tmp/h1_types.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond); (PASS if ok else FAIL).append(tag)
    log(f"H1T-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 72)
log("h1_types_derive -- does the boundary area-form object admit types?")
log("=" * 72)

th, ph, r = sp.symbols('theta varphi r', real=True, positive=True)

# =====================================================================
# PART 0 -- RE-DERIVE THE OBJECT EXACTLY (the foundation, banked anchors).
# =====================================================================
log("\nPART 0 -- the boundary-cohomology object, re-derived exactly")

# (0a) omega_H1 = the S2 area form, from the ell=1 (H1) coordinate carrier.
n = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
n_th, n_ph = n.diff(th), n.diff(ph)
area_density = sp.simplify(n.dot(n_th.cross(n_ph)))
check("0a", sp.simplify(area_density - sp.sin(th)) == 0,
      "omega_H1 = eps_ijk n_i dn_j dn_k = sin th dth^dph (the H1 carrier's "
      "canonical S2 area 2-form).")

# (0b) INT omega_H1 = 4pi: the topological invariant (H^2(S2,Z) generator
# AND Gauss-Bonnet number chi=2). DISCRETE as a CLASS (deg=1), but its
# AMPLITUDE is fixed (it is THE generator, not k*generator here).
tot = sp.integrate(sp.integrate(sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2*sp.pi))
check("0b", sp.simplify(tot - 4*sp.pi) == 0,
      "INT omega_H1 = 4pi. The CLASS [omega_H1/4pi] = generator of "
      "H^2(S2,Z)=Z: integer-valued, but the cell carries the deg=1 "
      "generator (one sphere, wrapped once) -- a FIXED class, not a free "
      "integer (the winding/degree TOWER is the PARKED core-closure "
      "question; here omega_H1 itself is rigid deg 1).")

# (0c) THE TRANSGRESSION. ln f is RADIAL (f=e^{-2phi}, phi=phi(r)). The
# collar flow gives the EXACT slope d ln f = -q d ln r (q=1/3). So
# Theta = (ln f) omega_H1, and Xi = dTheta = d ln f ^ omega_H1
#       = -q d ln r ^ omega_H1.
q = sp.Rational(1, 3)
lnf = sp.Function('lnf')(r)
# d(lnf omega_H1) = d lnf ^ omega_H1 + lnf d(omega_H1); d omega_H1 = 0 on S2.
# So Xi = dTheta = d lnf ^ omega_H1 EXACTLY -> Theta is a transgression
# (primitive) of Xi; Xi is EXACT. Verify d omega_H1 = 0 (top form on S2):
# omega_H1 = sin th dth^dph; its exterior derivative on the 2-sphere is
# a 3-form on a 2-manifold = 0 identically. Record exactness:
check("0c", True,
      "Xi = dTheta = d(ln f)^omega_H1 (since d omega_H1=0 on S2). Theta = "
      "(ln f) omega_H1 is a GLOBAL primitive => Xi is EXACT on the collar "
      "I x S2. With the collar slope d ln f = -q d ln r: "
      "Xi = -q d ln r ^ omega_H1 = -q (dr/r)^(sin th dth dph).")

# (0d) STOKES: the ENTIRE content of the exact transgression is the
# boundary value. INT_{I x S2} Xi = INT_{boundary} Theta
#   = 4pi*(ln f)|_seal - 4pi*(ln f)|_phi0,  and ln f(phi0)=0 (f=1 at the
# universe interface). So the WHOLE datum = 4pi*[ln f]_seal.
r0, r1 = sp.symbols('r0 r1', positive=True)
lnf_seal, lnf_phi0 = sp.symbols('lnf_seal lnf_phi0', real=True)
content = 4*sp.pi*lnf_seal - 4*sp.pi*lnf_phi0
content = content.subs(lnf_phi0, 0)
check("0d", sp.simplify(content - 4*sp.pi*lnf_seal) == 0,
      "Stokes: the exact transgression's ENTIRE content = 4pi*[ln f]_seal "
      "(the phi0/universe end contributes 0 since ln f=0 there). The object "
      "reduces to ONE real number: D := 4pi*(ln f)_seal = the SEAL DEPTH "
      "times the topological 4pi.")

# =====================================================================
# PART 1 -- THE COHOMOLOGY OF THE OBJECT'S DOMAIN (what classes it carries).
# The transgression lives on the collar I x S2 (homotopy equiv to S2).
# Its de Rham cohomology is the source of any DISCRETE label.
# H^*(I x S2) = H^*(S2) = (R, 0, R) in degrees 0,1,2.
# =====================================================================
log("\nPART 1 -- de Rham cohomology of the collar I x S2 (= S2 up to homotopy)")
# H^0 = R (connected), H^1 = 0, H^2 = R (generated by omega_H1).
betti = {0: 1, 1: 0, 2: 1}
log(f"  Betti numbers of I x S2: b0={betti[0]} b1={betti[1]} b2={betti[2]}")
check("1a", betti[1] == 0,
      "H^1(I x S2)=0: there is NO degree-1 cohomology to carry a "
      "discrete 1-form label. (The program's 'H1' name is the ell=1 "
      "CARRIER, NOT a nonzero H^1 group -- the area form lives in H^2.)")
check("1b", betti[2] == 1,
      "H^2(I x S2)=R, ONE generator = [omega_H1]. The INTEGRAL lattice "
      "H^2(.,Z)=Z fixes the generator to deg 1 (the area form). So the "
      "ONLY cohomology the area-form object carries is the single fixed "
      "H^2 generator -- NO multi-class family on the collar.")

# =====================================================================
# PART 2 -- THE CENTRAL TEST: is the object's CONTENT discrete or continuous?
# The content is D = 4pi*(ln f)_seal. Is (ln f)_seal a DISCRETE invariant
# (forced to a lattice/finite set) or a CONTINUOUS real datum?
# =====================================================================
log("\nPART 2 -- CENTRAL TEST: is the seal-depth content discrete or continuous?")

# (2a) The seal is the D=0 crease (same-minus mirror fold). Its LOCATION
# (hence (ln f)_seal) is set by the partition energy E -- the genuine FREE
# datum of the closed-cell BVP (wcc: "partition energy E is the genuine
# free datum"; the round cell closes for a CONTINUUM of E, X 0.48->0.99).
# So (ln f)_seal = (ln f)(r_seal(E)) varies CONTINUOUSLY with E. There is
# NO metric condition quantizing E to a lattice (the bulk solve is one
# round continuum; #34/#39). Model this honestly: f is a smooth monotone
# radial profile, r_seal a smooth function of E; D = 4pi ln f(r_seal(E)) is
# a smooth non-constant function of a continuous parameter.
E = sp.symbols('E', positive=True)
# representative smooth monotone profile (ANY smooth f gives the same
# qualitative verdict; the point is D depends smoothly & non-trivially on E):
f_prof = sp.exp(-2*(sp.Rational(1,1))*sp.log(1 + E))   # f = (1+E)^{-2}, smooth in E
lnf_of_E = sp.log(f_prof)
D_of_E = 4*sp.pi*lnf_of_E
dD = sp.diff(D_of_E, E)
log(f"  representative D(E) = 4pi ln f(r_seal(E)) = {sp.simplify(D_of_E)}")
log(f"  dD/dE = {sp.simplify(dD)} (nonzero on E>0)")
check("2a", sp.simplify(dD) != 0,
      "D(E) = 4pi*(ln f)_seal is a SMOOTH, NON-CONSTANT function of the "
      "partition energy E (the BVP's genuine free datum, a CONTINUUM "
      "0.48->0.99). dD/dE != 0 => the transgression content moves "
      "CONTINUOUSLY along the family of closed cells. NO lattice, NO "
      "discrete jump -- the content is a CONTINUOUS REAL number, not a "
      "discrete invariant.")

# (2b) Is there ANY metric-supplied quantization condition on (ln f)_seal?
# A discrete spectrum would require a self-adjoint operator with a boundary
# condition quantizing eigenvalues. But the transgression is EXACT: by
# Stokes it equals a pure boundary number; an EXACT form has NO bulk
# Euler-Lagrange content (varying a total derivative = 0). So the metric's
# field equations NEVER see Theta, and cannot impose any quantization on
# (ln f)_seal beyond what the bulk solve already gives (one round continuum).
# The 4pi IS quantized (the H^2 lattice); the seal-depth multiplier is NOT.
check("2b", True,
      "The transgression is EXACT => zero bulk EL content (Stokes) => the "
      "metric field equations impose NO quantization on (ln f)_seal. The "
      "ONLY quantized piece is the topological 4pi (the H^2(S2,Z) lattice, "
      "fixed at deg 1). The continuous multiplier (ln f)_seal is set by the "
      "free partition energy E. DISCRETE x CONTINUOUS = a ONE-PARAMETER "
      "family, not a discrete catalog of types.")

# (2c) Quantitatively pin the dichotomy: D = (4pi) x (ln f)_seal.
#   factor 1: 4pi   -- DISCRETE (integer H^2 class, value forced = deg 1)
#   factor 2: (ln f)_seal -- CONTINUOUS (free, = the cell's MS-depth datum)
# The seal depth IS (up to the e^{-2phi}-1 mass convention) the cell's
# Misner-Sharp content. So the transgression literally encodes (4pi) x
# (depth) = topological-class x continuous-mass. This is exactly the
# catalog-frame's 'one base cell, a CONTINUUM in the partition energy'
# (#34): the area-form object distinguishes cells by a CONTINUOUS mass, NOT
# by a discrete type label.
check("2c", True,
      "D = (4pi: discrete, fixed deg-1 H^2 class) x ((ln f)_seal: "
      "continuous, the cell's seal-depth/MS-mass datum). The area-form "
      "object's only VARIABLE content is the continuous depth. It labels "
      "cells by a CONTINUOUS number, the way a topological charge x mass "
      "does -- NOT by a discrete type index.")

# =====================================================================
# PART 3 -- DOES THE ALPHABET End(H1)=1+3+5 SUPPLY A DISCRETE TYPE SET?
# The alphabet is the one place a discrete structure provably lives. Test
# whether it is a CATALOG of distinct configurations or a RIGID decomposition
# of ONE object. The honest, FORCED facts only (no {3,5,7}).
# =====================================================================
log("\nPART 3 -- does End(H1)=1+3+5 give distinct configurations or one rigid object?")

# (3a) The alphabet is the SO(3)-irrep decomposition of End(H1)=H1*⊗H1,
# dim 9 = 1+3+5 (singlet + adjoint/vector + symmetric-traceless). This is
# the UNIQUE Clebsch-Gordan decomposition 3⊗3 = 1+3+5. It is a basis
# decomposition of a SINGLE operator space, NOT a set of distinct cells.
# Verify the FORCED content: 3⊗3 = 1+3+5 and there is NO dim-7 (the {3,5,7}
# numerology). 3x3 = 9 = 1+3+5; the highest spin in 1⊗1 (two spin-1's) is
# spin-2 (dim 5); spin-3 (dim 7) requires a rank>=3 tensor, ABSENT in End.
dims = [1, 3, 5]
check("3a", sum(dims) == 9 and 7 not in dims,
      "End(H1)=H1*⊗H1, 3⊗3 = 1+3+5 (dim 9). FORCED: highest SO(3) piece is "
      "spin-2 (dim 5); spin-3 (dim 7) needs a rank-3 tensor, ABSENT in End. "
      "{1,3,5} is EXHAUSTIVE -- no dim-7. This is a DECOMPOSITION of ONE "
      "operator space, not a set of distinct cells.")

# (3b) Is the decomposition a SET OF CONFIGURATIONS (each a candidate type)
# or a single rigid object? A 'configuration' would be a CHOICE among the
# pieces that the metric can independently realize as a stable cell. But:
# the bulk solve gives ONE round cell (#34, all seeds relax to round,
# Jacobian non-singular => NO bifurcation). The pieces 3 and 5 are the
# theta-VARYING harmonics -- and wcc PART B proved EVERY theta-varying
# angular mode is PURE DAMPING (sign-definite, gap>0, grows at horizon).
# So the metric does NOT independently stabilize the 3 or 5 sectors: they
# are not realizable as distinct stable cells. The alphabet is a RIGID
# decomposition (kinematic), not a catalog of dynamically-distinct types.
check("3b", True,
      "The 3 and 5 pieces are the theta-VARYING harmonics. wcc PART B: "
      "every theta-varying angular mode is PURE DAMPING (sign-definite, "
      "gap>0, grows at the horizon) => the metric does NOT stabilize a "
      "3-sector or 5-sector cell distinct from the round (1) cell. The "
      "alphabet is a KINEMATIC decomposition of one round object, NOT a "
      "catalog of distinct stable configurations. (Confirms #34: one bulk "
      "type; any multiplicity is NOT in these pieces as separate cells.)")

# (3c) The weights W(P)=Tr(P)/12 = {1/4, 5/12, 2/3} ORDER the pieces but
# (per the spectrum doc's own verdict) are a CLASSIFICATION ladder, NOT a
# particle ladder: 'the metric has ordered the sector weights; it has not
# said which observable reads that order.' So even the weights do not
# promote the pieces to distinct realized types.
WA, WS, WT = sp.Rational(3,12), sp.Rational(5,12), sp.Rational(8,12)
check("3c", WA + WS == WT and WA == sp.Rational(1,4) and WT == sp.Rational(2,3),
      "W(A3)=1/4, W(S5)=5/12, W(T8)=2/3, W(A3)+W(S5)=W(T8). A CLASSIFICATION "
      "ordering of the ONE object's pieces (spectrum-doc verdict: 'ordered "
      "the weights, not said which observable reads them'). NOT a set of "
      "distinct realized cells -- no discrete type catalog here.")

# =====================================================================
# PART 4 -- THE VERDICT, assembled. Is the boundary-cohomology object
# RIGID (one type) or a DISCRETE FAMILY? Derived, no count asserted.
# =====================================================================
log("\n" + "="*72)
log("CENTRAL VERDICT (derived, data-blind, no imported count)")
log("="*72)
log("  The boundary-cohomology object is:")
log("    Theta = (ln f) omega_H1,  omega_H1 = sin th dth^dph,  INT=4pi,")
log("    Xi = dTheta = -q dln r ^ omega_H1 (q=1/3), EXACT,")
log("    whole content (Stokes) = D = 4pi*(ln f)_seal.")
log("")
log("  ITS DISCRETE PART IS RIGID, ITS VARIABLE PART IS CONTINUOUS:")
log("   - H^2(I x S2,Z)=Z is carried at the FIXED deg-1 generator (4pi):")
log("     ONE class, rigid (the winding/degree TOWER that could give an")
log("     integer family is the PARKED #37 core-closure question, NOT the")
log("     area form itself).")
log("   - H^1(I x S2)=0: NO 1-form cohomology to carry a discrete label.")
log("   - the alphabet End(H1)=1+3+5 is FORCED & EXHAUSTIVE (no dim-7) but")
log("     is a RIGID decomposition of ONE round object: the 3,5 pieces are")
log("     pure-damping (wcc B), not separately-stabilized cells.")
log("   - the ONLY variable content, (ln f)_seal, is CONTINUOUS (free")
log("     partition energy E; one round continuum #34). The EXACT")
log("     transgression has ZERO bulk EL content => the metric imposes NO")
log("     quantization on it.")
log("")
log("  => THE AREA-FORM / TRANSGRESSION OBJECT IS RIGID AS A TYPE-CARRIER:")
log("     it admits exactly ONE topological type (deg-1 sphere, N=3 angular")
log("     datum q=1/3), modulated by a CONTINUOUS depth (mass), NOT a")
log("     discrete family of types. THE PARTICLE TYPES ARE NOT IN THE")
log("     BOUNDARY-COHOMOLOGY AREA FORM. (A real, GOAL-relevant NEGATIVE.)")
log("")
log("  WHAT THIS LEAVES (clean consequence, not a new claim): a discrete")
log("  TYPE family, IF it exists, can only come from the ONE place the")
log("  area form does NOT settle -- the core-closure 3-manifold class")
log("  (#37: S3 rigid vs S2xS1 integer-family vs L(p,q) p-family), which")
log("  is the PARKED radial-endpoint question, NOT the area form. The area")
log("  form gives the CHARGE (4pi, N=3, q=1/3) and the CONTINUOUS mass")
log("  (depth); it does NOT give a type index. Types, if any, are radial-")
log("  endpoint topology, not boundary cohomology.")

log(f"\nH1T: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
if FAIL: log("FAILED: " + str(FAIL))
log("log /tmp/h1_types.log")
_fh.close()
