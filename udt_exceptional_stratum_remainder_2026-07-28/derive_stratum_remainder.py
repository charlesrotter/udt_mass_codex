#!/usr/bin/env python3
# derive_stratum_remainder.py — gate (d): exceptional-stratum remainder.
#
# Contract: udt_exceptional_stratum_remainder_2026-07-28/PREREGISTRATION.md
# (frozen targets T-d1..T-d4, falsifiers F-d1..F-d3, maximum conclusion).
# Parents:
#   P-OWN = udt_higher_isometry_plane_ownership_audit_2026-07-28/EXACT_DERIVATION.md
#           (family §1, G3 §2, D3 §3, witness §6, two-free-lines §7)
#   P-SEL = udt_alpha_plane_selector_theorem_2026-07-28/EXACT_DERIVATION.md
#           (certificate, stratum derivation, conventions)
#   P-CAP = udt_cap_gluing_selector_2026-07-28/AUDIT_REPORT.md (commit 5291b63; CITED
#           for scope only — c = 1 forced for complete two-cap members; NOT assumed
#           in any derivation below)
#   G01/G02 = CURRENT_SCIENTIFIC_PREMISES.tsv rows G01, G02 (founded phi additive log
#           depth; pair action diag(e^-phi, e^+phi) — unit determinant), sourced to
#           udt_founded_phi_complete_coframe_extension_audit_2026-07-25/.
#
# Setting: alpha = 0 stratum, S := b*u + f^2 = c constant (c > 0 on principal orbits).
# Deterministic, CPU-only, sympy. Zero-residual gates. JSON summary written next to
# this script. Exit 0 iff all checks pass.

import json
import os
import sys

import sympy as sp

CHECKS = []


def rec(name, ok, detail=""):
    CHECKS.append({"name": name, "passed": bool(ok), "detail": detail})
    print(("PASS  " if ok else "FAIL  ") + name + (("  :: " + detail) if detail else ""))
    return ok


def is0(e):
    """Zero-residual gate for a scalar expression."""
    e = sp.sympify(e)
    r = sp.simplify(sp.expand(sp.together(e)))
    if r == 0:
        return True
    r = sp.simplify(sp.trigsimp(r))
    return r == 0


def mat0(M):
    return all(is0(x) for x in M)


# =====================================================================
# Part 0 — family objects (P-OWN §1–§2), symbolic point-jet layer
# =====================================================================
u, b, cE, cc, lam = sp.symbols("u b c_E c lam", positive=True)
f = sp.Symbol("f", real=True)
alp = sp.Symbol("alpha", real=True)
chi, df, db = sp.symbols("chi df db", real=True)

Q = 1 / u - alp**2 * u
# Complete orbit Gram in ordered basis (K, V, Y) — P-OWN §2, taken as the family's
# registered presentation (CHOSE-inherited).
G3 = sp.Matrix(
    [
        [-cE**2 * u, -cE * alp * u, -cE * alp * u * f],
        [-cE * alp * u, Q, Q * f],
        [-cE * alp * u * f, Q * f, Q * f**2 + b],
    ]
)
rec("P0_G3_det_parent", is0(G3.det() - (-b * cE**2)),
    "det G3 = -b c_E^2 (P-OWN §2) reproduced from the family")

G_KV = G3.extract([0, 1], [0, 1])
G_KY = G3.extract([0, 2], [0, 2])

# alpha = 0 specialization
G_KV0 = G_KV.subs(alp, 0)
G_KY0 = G_KY.subs(alp, 0)
rec("P0_GKV_alpha0", mat0(G_KV0 - sp.diag(-cE**2 * u, 1 / u)),
    "G_KV|a=0 = diag(-c_E^2 u, 1/u) — verified from the family")

# stratum substitution S = b u + f^2 = c  =>  b = (c - f^2)/u
b_st = (cc - f**2) / u
G_KY0_st = G_KY0.subs(b, b_st)
rec("P0_GKY_alpha0_stratum", mat0(G_KY0_st - sp.diag(-cE**2 * u, cc / u)),
    "G_KY|a=0,stratum = diag(-c_E^2 u, c/u) — verified from the family")

# =====================================================================
# Part 1 — T-d1: area-value provenance
# =====================================================================
det_KV = sp.simplify(G_KV0.det())
det_KY = sp.simplify(G_KY0_st.det())
rec("Td1_det_GKV_value", is0(det_KV + cE**2), "det G_KV = -c_E^2 exactly")
rec("Td1_det_GKY_value", is0(det_KY + cE**2 * cc), "det G_KY = -c_E^2 c exactly")

# (a) u-cancellation is exactly the G02 unit-determinant pair action:
#     with u = e^{-2 phi}, the clock leg carries weight e^{-2 phi} and the ruler leg
#     e^{+2 phi}; their product is 1, so det G_KV has no phi-dependence at all.
phi = sp.Symbol("phi", real=True)
det_KV_phi = det_KV.subs(u, sp.exp(-2 * phi))
rec("Td1_pair_unit_det_phi_independence",
    is0(sp.diff(det_KV_phi, phi)) and is0(det_KV_phi + cE**2),
    "u = e^{-2phi}: det G_KV = -c_E^2 with zero phi-derivative (G02 unit-det action)")

# (b) primitivity (P-OWN §7) leaves only SIGN freedom in V and Y; a sign flip is the
#     congruence diag(1,-1), which preserves the Gram determinant (and the diagonal
#     Gram entrywise).
Ssign = sp.diag(1, -1)
rec("Td1_sign_irrelevance",
    is0((Ssign.T * G_KV0 * Ssign).det() - G_KV0.det())
    and mat0(Ssign.T * G_KV0 * Ssign - G_KV0),
    "V -> -V congruence: Gram (and det) unchanged; same for Y")

# (c) the clock normalization does NOT cancel from the absolute value: K -> lam K
#     scales BOTH dets by lam^2; the ratio is invariant.
Lk = sp.diag(lam, 1)
det_KV_lam = (Lk.T * G_KV0 * Lk).det()
det_KY_lam = (Lk.T * G_KY0_st * Lk).det()
rec("Td1_K_rescaling_scales_dets",
    is0(det_KV_lam - lam**2 * det_KV) and is0(det_KY_lam - lam**2 * det_KY),
    "K -> lam K: both dets scale by lam^2 (absolute value not clock-free)")
rec("Td1_ratio_clock_free",
    is0(det_KY_lam / det_KV_lam - cc) and is0(det_KY / det_KV - cc),
    "det G_KY / det G_KV = c — invariant under K-rescaling and c_E; DERIVED core")

# (d) equivalent normalization-free form: at alpha = 0 the ratio is the free-circle
#     norm ratio (no clock enters at all).
rec("Td1_norm_ratio_form",
    is0(G_KY0_st[1, 1] / G_KV0[1, 1] - cc),
    "g(Y,Y)/g(V,V) = c on the stratum — clock-free discriminator core")

# (e) relabel map (present the SAME metric with Y as the vertical circle):
#     u~ = 1/g(Y,Y), cE~^2 = -g(K,K) g(Y,Y), f~ = g(V,Y)/g(Y,Y), b~ = g(H~,H~) with
#     H~ = V - f~ Y.  All computed from Gram data (metric-native).
gKK = -cE**2 * u
gVV = 1 / u
gYY = cc / u
gVY = f / u  # = G3[1,2] at alpha=0 on the stratum, checked below in Part 3
u_t = 1 / gYY
cE2_t = -gKK * gYY
f_t = gVY / gYY
b_t = sp.simplify(gVV - 2 * f_t * gVY + f_t**2 * gYY)
S_t = sp.simplify(b_t * u_t + f_t**2)
rec("Td1_relabel_map",
    is0(u_t - u / cc) and is0(cE2_t - cc * cE**2) and is0(f_t - f / cc)
    and is0(b_t - b_st / cc) and is0(S_t - 1 / cc),
    "relabel: u~=u/c, c_E~^2=c c_E^2, f~=f/c, b~=b/c, S~=1/c  (c -> 1/c)")
rec("Td1_relabel_c1_fixed_point",
    all(is0(x) for x in [
        (u_t - u).subs(cc, 1), (cE2_t - cE**2).subs(cc, 1),
        (f_t - f).subs(cc, 1), (b_t - b_st).subs(cc, 1), (S_t - 1).subs(cc, 1)]),
    "at c = 1 the relabel fixes every presentation scalar (u,f,b,c_E,S)")

# (f) cap-cycle Gram: v± = (V ∓ Y)/2 is the P-CAP convention basis change; the cap
#     cycles v- = (V+Y)/2, v+ = (V-Y)/2 (unimodular with the lattice).  Their inner
#     product measures the c-defect.
g_vm_vp = sp.simplify((gVV - gYY) / 4)
rec("Td1_cap_cycle_inner_product",
    is0(g_vm_vp - (1 - cc) / (4 * u)),
    "g(v-,v+) = (1-c)/(4u): the cap cycles are g-orthogonal exactly at c = 1")

# =====================================================================
# Part 2 — T-d2: all-orders identity at c = 1 (functional layer)
# =====================================================================
s = sp.Symbol("s", real=True)
u_s = sp.Function("u", positive=True)(s)
f_s = sp.Function("f", real=True)(s)
b_c1 = (1 - f_s**2) / u_s  # S = 1  <=>  b = (1-f^2)/u  (verified as an identity)
rec("Td2_b_forced_at_c1",
    is0(b_c1 * u_s + f_s**2 - 1),
    "S = b u + f^2 = 1  <=>  b = (1-f^2)/u — 'forced' identity at c = 1")

GKV_s = sp.diag(-cE**2 * u_s, 1 / u_s)
GKY_s = sp.diag(-cE**2 * u_s, f_s**2 / u_s + b_c1)
Dmat = GKY_s - GKV_s
jet_ok = True
for k in range(6):
    jet_ok = jet_ok and mat0(sp.diff(Dmat, s, k))
rec("Td2_gram_and_jets_identical",
    jet_ok,
    "G_KY - G_KV = 0 entrywise and all X-jets to order 5 = 0 (identically in u,f)")

# response matrices are then identical too (any-order certificate sees equal input)
D_KV_s = sp.simplify(GKV_s.inv() * sp.diff(GKV_s, s))
D_KY_s = sp.simplify(GKY_s.inv() * sp.diff(GKY_s, s))
rec("Td2_response_identical", mat0(D_KV_s - D_KY_s),
    "D_KV = D_KY identically at c = 1")

# hidden-asymmetry hunt in the correspondence (K,V) <-> (K,Y):
#   off-diagonal Gram entries both vanish at alpha=0 (no asymmetric cross term);
#   sign freedom of the primitive generators leaves the Gram invariant (Td1 check);
#   K is shared.  The correspondence carries no data beyond V |-> Y.
rec("Td2_no_offdiagonal_asymmetry",
    is0(G_KV0[0, 1]) and is0(G_KY0_st[0, 1]),
    "g(K,V) = g(K,Y) = 0 at alpha = 0: correspondence has no hidden cross-term")

# =====================================================================
# Part 3 — T-d3: ambient inventory (general c on the stratum, then c = 1)
# =====================================================================
b_gc = (cc - f_s**2) / u_s
# full orbit Gram (functions of s) at alpha=0 on the stratum
G3_s = sp.Matrix(
    [
        [-cE**2 * u_s, 0, 0],
        [0, 1 / u_s, f_s / u_s],
        [0, f_s / u_s, f_s**2 / u_s + b_gc],
    ]
)
rec("Td3_gVY_value", is0(G3.subs(alp, 0)[1, 2] - f / u),
    "g(V,Y) = f/u at alpha = 0 — computed from the family G3")
rec("Td3_gYY_stratum", is0(sp.simplify(G3_s[2, 2]) - cc / u_s),
    "g(Y,Y) = c/u on the stratum")

# complement geometry: H = Y - f V (V-presentation), H~ = V - (f/c) Y (Y-presentation)
gHH = sp.simplify(G3_s[2, 2] - 2 * f_s * G3_s[1, 2] + f_s**2 * G3_s[1, 1])
rec("Td3_H_norm", is0(gHH - b_gc), "g(H,H) = b (consistency)")
f_tt = f_s / cc
gHtHt = sp.simplify(G3_s[1, 1] - 2 * f_tt * G3_s[1, 2] + f_tt**2 * G3_s[2, 2])
rec("Td3_Htilde_norm", is0(gHtHt - b_gc / cc),
    "g(H~,H~) = b/c — equals b exactly at c = 1")
gH_Ht = sp.simplify(
    G3_s[1, 2] - f_tt * G3_s[2, 2] - f_s * G3_s[1, 1] + f_s * f_tt * G3_s[1, 2]
)
rec("Td3_H_Htilde_pairing", is0(gH_Ht - (-f_s * b_gc / cc)),
    "g(H,H~) = -f b / c — a symmetric pair scalar (equal under relabel)")

# mixed D3 entries (full three-direction response), alpha = 0, stratum
D3_s = sp.simplify(G3_s.inv() * sp.diff(G3_s, s))
fp = sp.diff(f_s, s)
rec("Td3_D3_mixing_entries",
    is0(D3_s[1, 2] - cc * fp / (cc - f_s**2))
    and is0(D3_s[2, 1] - fp / (cc - f_s**2)),
    "(D3)_{V->Y} = c f'/(c - f^2), (D3)_{Y->V} = f'/(c - f^2)")
rec("Td3_D3_mixing_ratio_is_c",
    is0(D3_s[1, 2] - cc * D3_s[2, 1]),
    "ratio of the two mixing entries = c (normalization-free; = 1 at c = 1)")
rec("Td3_D3_mixing_difference",
    is0(D3_s[1, 2] - D3_s[2, 1] - (cc - 1) * fp / (cc - f_s**2)),
    "difference = (c-1) f'/(c - f^2): vanishes identically at c = 1")

# swap-invariance of the ENTIRE ambient orbit Gram at c = 1 (the master fact):
P3 = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])  # K fixed, V <-> Y
G3_c1 = G3_s.subs(cc, 1)
rec("Td3_P_invariance_G3_c1", mat0(P3.T * G3_c1 * P3 - G3_c1),
    "P^T G3 P = G3 identically at c = 1 (all profiles)")
rec("Td3_P_invariance_G3_jets_c1",
    all(mat0(P3.T * sp.diff(G3_c1, s, k) * P3 - sp.diff(G3_c1, s, k))
        for k in range(1, 5)),
    "same for all s-jets of G3 (orders 1..4)")
D3_c1 = sp.simplify(D3_s.subs(cc, 1))
rec("Td3_P_invariance_D3_c1", mat0(P3 * D3_c1 * P3 - D3_c1),
    "P D3 P^{-1} = D3 at c = 1: no mixed-entry asymmetry survives")
# and the generic-c defect of that invariance is exactly the norm gap:
defect = sp.simplify(P3.T * G3_s * P3 - G3_s)
rec("Td3_P_defect_is_norm_gap",
    is0(defect[1, 1] - (cc - 1) / u_s) and is0(defect[2, 2] - (1 - cc) / u_s)
    and all(is0(defect[i, j]) for i in range(3) for j in range(3) if i != j)
    and is0(defect[0, 0]),
    "P-defect of G3 = diag(0, (c-1)/u, (1-c)/u): supported ONLY on the norm gap")

# =====================================================================
# Part 4 — T-d4: exchange-isometry characterization
# =====================================================================
# (A) NECESSITY.  Let Phi be an isometry with Phi_*(span(K,V)) = span(K,Y).
#     P-OWN §7: exactly two free primitive circle lines, {V, Y}.  Phi_* maps the
#     Killing lattice to itself and free primitive circles to free primitive circles.
#     The compact primitive free elements of span(K,Y) are ±Y (any a K + b Y with
#     a != 0 generates a noncompact group since K's flow is unbounded in t), so
#     Phi_* V = ±Y; injectivity on the lattice then forces Phi_* Y = ±V.
#     Isometry scalar matching across the induced orbit-space map sigma:
#         g(Y,Y)(sigma(s)) = g(V,V)(s)   and   g(V,V)(sigma(s)) = g(Y,Y)(s):
us_, ut_ = sp.symbols("u_source u_target", positive=True)
e1 = cc / ut_ - 1 / us_       # g(Y,Y)∘sigma = g(V,V)
e2 = 1 / ut_ - cc / us_       # g(V,V)∘sigma = g(Y,Y)
resid = sp.simplify(sp.together(e2.subs(ut_, cc * us_)) * cc * us_ - (1 - cc**2))
rec("Td4_necessity_algebra", is0(resid),
    "e1 => u_target = c u_source; then e2 => (1 - c^2)/(c u) = 0 => c^2 = 1")
sols = sp.solve([e1, e2], [ut_, cc], dict=True)
pos_sols = [S_ for S_ in sols if S_[cc].is_positive]
rec("Td4_necessity_solve",
    len(pos_sols) == 1 and sp.simplify(pos_sols[0][cc] - 1) == 0
    and sp.simplify(pos_sols[0][ut_] - us_) == 0,
    "unique positive solution: c = 1 and u∘sigma = u  (swap => c = 1, depth-matching)")

# (B) SUFFICIENCY (constructive).  Principal region in adapted coordinates
#     (t, s, phi_-, phi_+) with v± the cap-cycle lattice basis (V = v_- + v_+,
#     Y = v_- - v_+; unimodular by P-OWN §7 / P-CAP), X chosen orthogonal to orbits
#     (Category-A cohomogeneity-one normal form), alpha = 0 (no dt cross terms).
n_s = sp.Function("n", positive=True)(s)
gmm = (1 + 2 * f_s + cc) / (4 * u_s)
gpp = (1 - 2 * f_s + cc) / (4 * u_s)
gmp = (1 - cc) / (4 * u_s)
g4 = sp.Matrix(
    [
        [-cE**2 * u_s, 0, 0, 0],
        [0, n_s, 0, 0],
        [0, 0, gmm, gmp],
        [0, 0, gmp, gpp],
    ]
)
# consistency: rebuild G3(K,V,Y) from the (K, v-, v+) block
A = sp.Matrix([[1, 0, 0], [0, 1, 1], [0, 1, -1]])  # columns = K, V, Y in (K,v-,v+)
G3_rebuilt = A.T * sp.Matrix([[-cE**2 * u_s, 0, 0], [0, gmm, gmp], [0, gmp, gpp]]) * A
rec("Td4_normal_form_consistency", mat0(sp.simplify(G3_rebuilt - G3_s)),
    "(K,v-,v+) normal-form block reproduces the family G3(K,V,Y) on the stratum")

J = sp.diag(1, 1, 1, -1)  # (t,s,phi-,phi+) -> (t,s,phi-,-phi+): the lattice map P
cong = sp.simplify(J.T * g4 * J - g4)
rec("Td4_sufficiency_congruence_c1", mat0(cong.subs(cc, 1)),
    "J^T g J = g identically at c = 1 for ARBITRARY profiles u(s), f(s), n(s)")
rec("Td4_congruence_defect_generic",
    is0(cong[2, 3] - (-2 * gmp)) and is0(cong[3, 2] - (-2 * gmp))
    and all(is0(cong[i, j]) for i in range(4) for j in range(4)
            if (i, j) not in [(2, 3), (3, 2)]),
    "the only congruence defect is -2 g(v-,v+) = -(1-c)/(2u): zero iff c = 1")
# J swaps the planes: J(V) = Y, J(Y) = V, J(K) = K; det J = -1 (orientation-reversing)
Kv = sp.Matrix([1, 0, 0, 0])
Vv = sp.Matrix([0, 0, 1, 1])
Yv = sp.Matrix([0, 0, 1, -1])
rec("Td4_J_swaps_planes",
    mat0(J * Vv - Yv) and mat0(J * Yv - Vv) and mat0(J * Kv - Kv)
    and sp.simplify(J.det() + 1) == 0,
    "J: V <-> Y, K fixed; det J = -1 (cap-fixing, orientation-reversing)")
# cap compatibility: J fixes v- and reverses v+ — each cap-closing cycle line is
# preserved, so J extends over both caps of a complete member.
vm = sp.Matrix([0, 0, 1, 0])
vp = sp.Matrix([0, 0, 0, 1])
rec("Td4_J_cap_cycles",
    mat0(J * vm - vm) and mat0(J * vp + vp),
    "J v- = v-, J v+ = -v+: both cap-closing cycle lines preserved (cap-fixing)")

# (C) classification of ALL lattice swaps: M(V) = s1 Y, M(Y) = s2 V.  Gram
#     invariance at c = 1 forces s1 s2 = +1, i.e. det M = -1: every plane swap is
#     torus-orientation-reversing wherever f != 0.
G2_c1 = sp.Matrix([[1 / u, f / u], [f / u, 1 / u]])
swap_class_ok = True
for s1 in (1, -1):
    for s2 in (1, -1):
        M = sp.Matrix([[0, s2], [s1, 0]])
        inv_ok = mat0(M.T * G2_c1 * M - G2_c1)
        swap_class_ok = swap_class_ok and (inv_ok == (s1 * s2 == 1))
rec("Td4_swap_orientation_class", swap_class_ok,
    "Gram-preserving lattice swaps at c=1 are exactly s1 s2 = +1 (det = -1), "
    "for f != 0: every swap is orientation-reversing")

# (D) witness control (P-OWN §6): f = cos 2eta, u = 1 + eps(1 - f^2), b = (1-f^2)/u
eta, eps = sp.symbols("eta epsilon", positive=True)
f_w = sp.cos(2 * eta)
u_w = 1 + eps * (1 - f_w**2)
b_w = (1 - f_w**2) / u_w
rec("Td4_witness_on_stratum", is0(b_w * u_w + f_w**2 - 1),
    "witness: S = 1 exactly (c = 1) — the swap construction applies")
rec("Td4_witness_even_profile",
    is0(sp.trigsimp(u_w.subs(eta, sp.pi / 2 - eta) - u_w)),
    "witness u is even under eta -> pi/2 - eta (also admits cap-SWAPPING maps); "
    "evenness is sufficient-not-necessary for the plane swap (see control)")

# (E) NON-symmetric c = 1 numeric control (preregistered method requirement):
#     u = 1 + (3/10) sin^2(2 eta) + (1/10) sin^2(2 eta) cos(eta), f = cos 2 eta,
#     b = (1 - f^2)/u.  Smooth, positive, ASYMMETRIC under eta -> pi/2 - eta.
u_ct = 1 + sp.Rational(3, 10) * sp.sin(2 * eta) ** 2 \
         + sp.Rational(1, 10) * sp.sin(2 * eta) ** 2 * sp.cos(eta)
f_ct = sp.cos(2 * eta)
b_ct = (1 - f_ct**2) / u_ct
rec("Td4_control_on_stratum", is0(b_ct * u_ct + f_ct**2 - 1),
    "control: S = 1 exactly (c = 1 member)")
asym = sp.trigsimp(u_ct.subs(eta, sp.pi / 2 - eta) - u_ct)
asym_vals = [complex(sp.N(asym.subs(eta, pt), 30)).real
             for pt in (sp.pi / 6, sp.pi / 5)]
rec("Td4_control_asymmetric",
    all(abs(v) > 1e-6 for v in asym_vals),
    "u(pi/2 - eta) - u(eta) at eta = pi/6, pi/5: %.6g, %.6g (nonzero => genuinely "
    "asymmetric; eta -> pi/2 - eta is NOT an isometry of this member)"
    % tuple(asym_vals))

# control: plane-restricted data identical (T-d2 instantiated), incl. jets
gYY_ct = f_ct**2 / u_ct + b_ct
diff_ct = sp.trigsimp(gYY_ct - 1 / u_ct)
rec("Td4_control_plane_data_identical",
    is0(diff_ct) and all(is0(sp.diff(diff_ct, eta, k)) for k in range(1, 5)),
    "g(Y,Y) - g(V,V) = 0 and all eta-jets vanish for the asymmetric control")

# control: ambient candidates evaluated numerically at eta = pi/6, pi/5
amb = {}
for tag, pt in (("pi_over_6", sp.pi / 6), ("pi_over_5", sp.pi / 5)):
    subs = {eta: pt}
    gVY_v = float(sp.N((f_ct / u_ct).subs(subs), 30))
    gVV_v = float(sp.N((1 / u_ct).subs(subs), 30))
    gYY_v = float(sp.N(gYY_ct.subs(subs), 30))
    # D3 mixing entries with X = d/deta (c = 1)
    up = sp.diff(u_ct, eta)
    fpn = sp.diff(f_ct, eta)
    DVY = float(sp.N((1 * fpn / (1 - f_ct**2)).subs(subs), 30))
    DYV = DVY  # c = 1: proven equal; recompute independently below
    G3ct = sp.Matrix([[-u_ct, 0, 0],
                      [0, 1 / u_ct, f_ct / u_ct],
                      [0, f_ct / u_ct, gYY_ct]])
    D3ct = G3ct.inv() * sp.diff(G3ct, eta)
    DVY_direct = float(sp.N(D3ct[1, 2].subs(subs), 30))
    DYV_direct = float(sp.N(D3ct[2, 1].subs(subs), 30))
    gvmvp_v = float(sp.N(((1 / u_ct - gYY_ct) / 4).subs(subs), 30))
    amb[tag] = {
        "g_VY": gVY_v, "g_VV": gVV_v, "g_YY": gYY_v,
        "D3_VY": DVY_direct, "D3_YV": DYV_direct,
        "g_vminus_vplus": gvmvp_v,
    }
rec("Td4_control_ambient_symmetric",
    all(abs(d["g_VV"] - d["g_YY"]) < 1e-25 and abs(d["D3_VY"] - d["D3_YV"]) < 1e-25
        and abs(d["g_vminus_vplus"]) < 1e-25 and abs(d["g_VY"]) > 1e-3
        for d in amb.values()),
    "control ambient data: g(V,V)=g(Y,Y), D3 mixing entries equal, g(v-,v+)=0, "
    "while g(V,Y)=f/u is NONZERO — a pair scalar, not a discriminator; "
    "values: " + json.dumps(amb))

# control: the swap isometry exists DESPITE the asymmetry (Td4 congruence at c=1
# holds for arbitrary profiles, hence for this one); exhibit the numeric congruence.
g4_ct = g4.subs([(cc, 1), (cE, 1)]).subs(u_s, u_ct).subs(f_s, f_ct).subs(n_s, 1)
cong_ct = sp.trigsimp(J.T * g4_ct * J - g4_ct)
rec("Td4_control_swap_isometry", mat0(cong_ct),
    "asymmetric control: J^T g J - g = 0 exactly — the plane-swap isometry exists "
    "for this NON-symmetric profile (cap-fixing class; the cap-swapping class is "
    "excluded by the asymmetry check above)")

# =====================================================================
# Summary / JSON
# =====================================================================
n_pass = sum(1 for x in CHECKS if x["passed"])
all_ok = n_pass == len(CHECKS)

result = {
    "package": "udt_exceptional_stratum_remainder_2026-07-28",
    "script": "derive_stratum_remainder.py",
    "date": "2026-07-28",
    "contract": "PREREGISTRATION.md (T-d1..T-d4, F-d1..F-d3)",
    "setting": "registered family (CHOSE), alpha = 0, S := b u + f^2 = c constant, "
               "principal orbits; clock = K conditional; c_E enters as the "
               "registered clock normalization",
    "n_checks": len(CHECKS),
    "n_passed": n_pass,
    "checks": CHECKS,
    "targets": {
        "T_d1": {
            "grade": "DERIVED-WITHIN-REGISTRATION",
            "derived_core": "det G_KY / det G_KV = c = g(Y,Y)/g(V,V): fixed by G02 "
                            "unit-determinant pair action (u-cancellation) + P-OWN §7 "
                            "primitivity (no rescaling; sign irrelevant); invariant "
                            "under K-rescaling; clock-free. c != 1 => the two planes "
                            "are objectively distinguished (and isometrically "
                            "inequivalent, by T-d4 necessity).",
            "registration_residue": "the ABSOLUTE value -c_E^2 rides the registered "
                            "clock normalization c_E (clock = K is a LINE result; no "
                            "derived clock scale exists): K -> lam K rescales both "
                            "dets. The leg 'det G_P = -c_E^2 exactly' is therefore "
                            "legitimate only WITHIN the registered presentation; it "
                            "is not a naked CHOSE (no NEW dial beyond the inherited "
                            "registration) but it is the first certificate leg that "
                            "load-bears on c_E.",
            "no_2pi_dial": "the lattice normalization is the torus group structure "
                            "itself (primitivity is scale-free); the only hidden "
                            "dial is the c_E placement.",
            "scope": "c != 1 members are NON-COMPLETE (principal-orbit-only): "
                     "complete two-cap members have c = 1 exactly "
                     "(P-CAP, banked, commit 5291b63 — cited, not assumed).",
        },
        "T_d2": {
            "status": "PROVED (all-orders identity at c = 1)",
            "statement": "under the correspondence (K,V) <-> (K,Y) (K shared; V |-> Y, "
                         "both primitive, sign-irrelevant), G_KY = G_KV = "
                         "diag(-c_E^2 u, 1/u) as matrix functions on the region; all "
                         "X-jets of every entry agree identically; hence every "
                         "plane-restricted certificate of every order evaluates "
                         "equally on the two planes.",
            "falsifier": "F-d1 NOT fired",
        },
        "T_d3": {
            "inventory": [
                {"quantity": "g(V,Y) = f/u", "nonzero_generic": True,
                 "relabel": "invariant pair scalar (symmetric)",
                 "certificate_grade": True, "discriminates_unordered": False},
                {"quantity": "norm ratio g(Y,Y)/g(V,V) = c", "nonzero_generic": True,
                 "relabel": "c -> 1/c",
                 "certificate_grade": True,
                 "discriminates_unordered": "iff c != 1 (T-d1 core); = 1 at c = 1"},
                {"quantity": "complement norms g(H,H) = b vs g(H~,H~) = b/c",
                 "relabel": "swap", "certificate_grade": True,
                 "discriminates_unordered": "iff c != 1; equal at c = 1"},
                {"quantity": "g(H,H~) = -f b/c", "relabel": "invariant pair scalar",
                 "certificate_grade": True, "discriminates_unordered": False},
                {"quantity": "mixed D3 entries c f'/(c-f^2) vs f'/(c-f^2)",
                 "relabel": "swap (ratio c -> 1/c)", "certificate_grade": True,
                 "discriminates_unordered": "iff c != 1; equal at c = 1"},
                {"quantity": "orientation pairing (Hopf vs anti-Hopf Euler sign; "
                             "sign of vol(K,X,V,Y); F-holonomy sign)",
                 "relabel": "sign flip", "certificate_grade": False,
                 "reason": "requires a CHOSE orientation — a metric does not orient; "
                           "not well-defined from (g, K, line, X)",
                 "discriminates_unordered": "only relative to a chosen orientation"},
                {"quantity": "cap data: V = v- + v+ vs Y = v- - v+",
                 "relabel": "relative cap-cycle sign flip",
                 "certificate_grade": False,
                 "reason": "each cap cycle is canonical only up to sign; the "
                           "relative sign is orientation-class data",
                 "discriminates_unordered": False},
            ],
            "master_fact": "at c = 1 the ENTIRE ambient orbit Gram G3 and all its "
                           "X-jets are invariant under the swap P (K fixed, V <-> Y): "
                           "the P-defect of G3 is diag(0,(c-1)/u,(1-c)/u), supported "
                           "only on the norm gap. By T-d4 the swap is realized by an "
                           "actual isometry at c = 1, so NO metric-native datum of "
                           "any construction distinguishes the planes there. No "
                           "candidate is promoted to a selector.",
        },
        "T_d4": {
            "classification": "swap isometry exists  <=>  c = 1 "
                              "(alpha = 0 stratum, registered family)",
            "necessity": "Phi_* V = ±Y, Phi_* Y = ±V forced (two free lines, P-OWN "
                         "§7; compact primitive elements of span(K,Y) are ±Y); norm "
                         "matching across the induced orbit-space map gives "
                         "u∘sigma = u and c = 1. No assumption on Phi's action on K "
                         "and no restriction on the isometry algebra needed.",
            "sufficiency": "constructive: in cap-cycle coordinates the lattice map "
                           "J = diag(1,1,1,-1) (V <-> Y, K and t and s fixed) is an "
                           "isometry for EVERY c = 1 profile — g(v-,v+) = (1-c)/(4u) "
                           "= 0 is the entire obstruction. Cap-fixing, torus- and "
                           "space-orientation-reversing (det = -1 forced for f != 0); "
                           "extends to the metric completion of complete members "
                           "(isometry of a dense region extends to the completion — "
                           "Category-A standard).",
            "witness": "P-OWN §6 witness: on-stratum (S = 1) and even-profile; the "
                       "general construction covers it; evenness is "
                       "sufficient-not-necessary (asymmetric numeric control admits "
                       "the swap).",
            "cap_swapping_subclass": "isometries that also exchange the two caps "
                       "additionally require the depth profile to be symmetric under "
                       "the orbit-interval reflection (u∘sigma = u with sigma the "
                       "reflection); the asymmetric control excludes them while "
                       "still admitting the cap-fixing swap.",
            "open_remainder": "structure of the FULL swap-isometry group (beyond "
                       "existence) not classified; members whose isometry algebra "
                       "strictly exceeds the registered R x T^2 are covered by the "
                       "necessity argument (topology-only) and by the constructive "
                       "sufficiency, but their extra isometries are not classified "
                       "(P-OWN §8 territory).",
        },
    },
    "stratum_subclassification": {
        "c_neq_1": "planes isometrically INEQUIVALENT (T-d4 necessity) and "
                   "distinguished by the clock-free norm/det ratio (T-d1 core, "
                   "DERIVED); selection of span(K,V) by the VALUE leg is "
                   "DERIVED-WITHIN-REGISTRATION; occurs only on non-complete "
                   "members (P-CAP).",
        "c_eq_1": "selection PROVABLY IMPOSSIBLE: a plane-swapping isometry exists "
                  "for every profile (complete or principal-only); the "
                  "certificate-silent-but-possibly-selectable middle class is "
                  "EMPTY on the stratum.",
    },
    "falsifiers": {
        "F_d1": "NOT FIRED — T-d2 proved: no jet distinguishes at c = 1",
        "F_d2": "NOT FIRED as 'CHOSE and unusable' — the leg has a DERIVED "
                "clock-free core (the ratio/norm comparison) which breaks c != 1 "
                "silence unconditionally; the frozen ABSOLUTE-value form is "
                "honestly downgraded to DERIVED-WITHIN-REGISTRATION (c_E "
                "load-bearing).",
        "F_d3": "NOT FIRED at this stage — all zero-residual gates pass; the "
                "independent-implementation adjudication belongs to the blind "
                "verifier pass (not this script).",
    },
    "limits": [
        "family + registration CHOSE (P06/P07/P14-class); every conclusion scoped "
        "to it",
        "clock = K conditional (P-OWN §5 family-wide only)",
        "no certificate leg is ADOPTED here — adoption is Charles's; the extended "
        "value/ratio leg is recorded, not adopted",
        "cohomogeneity-one normal form (orbit-orthogonal transversal; adapted "
        "torus coordinates) and isometry-extension-to-completion are Category-A "
        "standard mathematics, machine-checked where expressible",
        "no physics: no branch, no alpha value, no action, no source, no mass",
    ],
    "all_passed": all_ok,
}

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "DERIVATION_RESULT.json"), "w") as fh:
    json.dump(result, fh, indent=1)

print()
print("checks passed: %d / %d" % (n_pass, len(CHECKS)))
print("T-d1 grade: DERIVED-WITHIN-REGISTRATION (ratio core DERIVED, clock-free)")
print("T-d2: PROVED — all-orders plane-restricted identity at c = 1 (F-d1 not fired)")
print("T-d3: no metric-native ambient discriminator at c = 1 (master P-invariance); "
      "tagged inventory recorded, nothing promoted")
print("T-d4: swap isometry exists <=> c = 1 (constructive; necessity topology-only)")
sys.exit(0 if all_ok else 1)
