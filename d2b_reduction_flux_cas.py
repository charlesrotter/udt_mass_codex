#!/usr/bin/env python3
"""D2b check 1 — Branch G round-static reduction, flux structure, fold pins.

Sources (cited, every object taken from the banked record):
- Constrained two-player action skeleton: S = ∫ c√h [ (Z/2)φ'² + R⁽²⁾[h] + 𝒦_branch + L_m ],
  K_AB = ½ e^{−φ} ∂_r h_AB, 𝒦 = K_AB K^AB − K², 𝒦_G = e^{2φ}𝒦 (φ-free), 𝒦_P = 𝒦.
  [native_field_equations_constrained_two_player_results.md:85-113]
- Banked P reduction on h=ρ²Ω: L_P = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2.
  [universe_cell_vacuum_impossibility_results.md:39]
Everything below is derived from these; the G-branch statements are NEW (R1/R2/T1 are
P-scoped and are NOT used).
"""
import sympy as sp

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

r, theta, psi = sp.symbols('r theta psi', positive=True)
Z, lam, a = sp.symbols('Z lambda a', real=True, nonzero=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)

# ---------- 1. Reduce both branches on h = rho(r)^2 * (round S2) ----------
h = sp.Matrix([[rho**2, 0], [0, rho**2*sp.sin(theta)**2]])
hp = h.diff(r)
hinv = h.inv()
K = sp.Rational(1,2)*sp.exp(-phi)*hp                     # K_AB
Kmix = hinv*K                                            # K^A_B
KK = sp.trace((hinv*K)*(hinv*K))                         # K_AB K^AB
trK = sp.trace(Kmix)
scriptK = sp.simplify(KK - trK**2)                       # 𝒦
check("K_AB K^AB - K^2 = -2 e^{-2phi} rho'^2/rho^2",
      sp.simplify(scriptK + 2*sp.exp(-2*phi)*rho.diff(r)**2/rho**2) == 0)

sqrth = rho**2*sp.sin(theta)                             # √h
R2 = 2/rho**2                                            # R⁽²⁾ of a 2-sphere radius rho
# per-4pi reduced Lagrangians (integrate sin(theta) over sphere / 4pi -> factor 1)
L_P = sp.simplify(rho**2*(sp.Rational(1,2)*Z*phi.diff(r)**2 + R2 + scriptK))
L_G = sp.simplify(rho**2*(sp.Rational(1,2)*Z*phi.diff(r)**2 + R2 + sp.exp(2*phi)*scriptK))
check("L_P reduction reproduces the BANKED (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2",
      sp.simplify(L_P - (Z/2*rho**2*phi.diff(r)**2 - 2*sp.exp(-2*phi)*rho.diff(r)**2 + 2)) == 0)
check("L_G reduction = (Z/2)rho^2 phi'^2 - 2 rho'^2 + 2   [NEW: the G round reduction]",
      sp.simplify(L_G - (Z/2*rho**2*phi.diff(r)**2 - 2*rho.diff(r)**2 + 2)) == 0)

# ---------- 2. Shift symmetry: exact for G (any lambda), broken for P ----------
shift = {phi: phi + lam}
check("L_G(phi+lambda) - L_G = 0 exactly (global shift EXACT in G)",
      sp.simplify(L_G.subs(phi, phi+lam).doit() - L_G) == 0)
dP = sp.simplify(L_P.subs(phi, phi+lam).doit() - L_P)
check("L_P(phi+lambda) - L_P = -2(e^{-2lambda}-1)e^{-2phi} rho'^2  (shift BROKEN in P)",
      sp.simplify(dP + 2*(sp.exp(-2*lam)-1)*sp.exp(-2*phi)*rho.diff(r)**2) == 0)

# ---------- 3. G Euler-Lagrange equations, with a GENERIC phi-blind matter sector ----------
# banked carrier is rho'-free and phi-blind [round_matter_reduction_results.md:14; fold doc budget cond.]
Lm = sp.Function('Lm')(rho)          # generic phi-blind, rho'-free matter (covers banked carrier's rho-dependence;
                                     # its own internal fields f enter as spectators for the phi/rho EL structure)
L_tot = L_G + Lm
EL_phi = sp.simplify(sp.diff(sp.diff(L_tot, phi.diff(r)), r) - sp.diff(L_tot, phi))
check("G phi-EL with ANY phi-blind matter: (Z rho^2 phi')' = 0  (SOURCE-FREE, exact)",
      sp.simplify(EL_phi - sp.diff(Z*rho**2*phi.diff(r), r)) == 0)
Flux = Z*rho**2*phi.diff(r)
check("Flux Phi = Z rho^2 phi' is EXACTLY CONSTANT on-shell in G (dPhi/dr = phi-EL)",
      sp.simplify(sp.diff(Flux, r) - EL_phi) == 0)
EL_rho = sp.simplify(sp.diff(sp.diff(L_tot, rho.diff(r)), r) - sp.diff(L_tot, rho))
check("G rho-EL: -4 rho'' - Z rho phi'^2 - dLm/drho = 0  (matter DOES gravitate in G, via h)",
      sp.simplify(EL_rho - (-4*rho.diff(r,2) - Z*rho*phi.diff(r)**2 - sp.diff(Lm, rho))) == 0)

# ---------- 4. Conserved H (autonomy) and fold values ----------
H = sp.simplify(phi.diff(r)*sp.diff(L_tot, phi.diff(r)) + rho.diff(r)*sp.diff(L_tot, rho.diff(r)) - L_tot)
Em = sp.Symbol('E_m')  # for the banked carrier E_m = -Lm here (rho'-free): H = (Z/2)rho^2phi'^2 - 2rho'^2 - 2 + E_m
check("H = (Z/2)rho^2 phi'^2 - 2 rho'^2 - 2 - Lm   (E_m = -Lm for rho'-free matter)",
      sp.simplify(H - (Z/2*rho**2*phi.diff(r)**2 - 2*rho.diff(r)**2 - 2 - Lm)) == 0)
# dH/dr = 0 on shell (solve EL for rho'' and phi'' ... phi-EL gives phi'' in terms of others)
phipp = sp.solve(EL_phi, phi.diff(r,2))[0]
rhopp = sp.solve(EL_rho, rho.diff(r,2))[0]
dH = sp.simplify(sp.diff(H, r).subs({phi.diff(r,2): phipp, rho.diff(r,2): rhopp}))
check("dH/dr = 0 on-shell (autonomous, matter included)", sp.simplify(dH) == 0)

# ---------- 5. Fold pins in G (Weierstrass-Erdmann, mirror extension) ----------
# momenta: pi_phi = Z rho^2 phi' ; pi_rho = -4 rho'  (rho'-free matter adds nothing)
# EVEN fold r -> 2rc - r, phi->phi, rho->rho: mirror extension has phi'->-phi', rho'->-rho'
#   [pi_phi] = 2 Z rho^2 phi' = 0 => phi'(rc)=0 ;  [pi_rho] = -8 rho' = 0 => rho'(rc)=0
# ODD fold r -> 2rs - r, phi -> 2a - phi (GENERAL reflection point a), rho->rho:
#   check it is a bulk symmetry of L_G for ANY a (it is NOT for P, for ANY a):
check("odd fold phi->2a-phi is an EXACT bulk symmetry of L_G for EVERY a",
      sp.simplify(L_G.subs(phi, 2*a - phi).doit() - L_G) == 0)
dPodd = sp.simplify(L_P.subs(phi, 2*a - phi).doit() - L_P)
sol_a = sp.solve(sp.simplify(dPodd.subs({rho.diff(r): 1})), a)   # any a making P invariant?
check("odd fold is NOT a bulk symmetry of L_P for ANY a (residual != 0 when rho' != 0)",
      len([s for s in sol_a if s.is_real]) == 0 or sp.simplify(dPodd) != 0)
#   mirror extension under odd fold: phi_tilde'(rs) = +phi'(rs) => [pi_phi] = 0 IDENTICALLY (phi' FREE);
#   rho_tilde'(rs) = -rho'(rs) => [pi_rho] = -8 rho'(rs) = 0 => rho'(rs)=0 pinned. Continuity: phi(rs)=a.
print("   (odd-fold pin algebra: [pi_phi]=0 identically -> phi' free; [pi_rho]=-8rho'=0 -> rho'(rs)=0;")
print("    phi-continuity -> phi(rs)=a. In P the canon fold forces a=0; in G, a is a SHIFT-GAUGE MODULUS.)")

# ---------- 6. NON-ROUND: 𝒦_G is phi-free for a GENERAL symmetric transverse h_AB ----------
h11, h12, h22 = [sp.Function(n)(r) for n in ('h11','h12','h22')]
hg = sp.Matrix([[h11, h12], [h12, h22]])
hgp = hg.diff(r); hginv = hg.inv()
Kg = sp.Rational(1,2)*sp.exp(-phi)*hgp
KKg = sp.trace((hginv*Kg)*(hginv*Kg)); trKg = sp.trace(hginv*Kg)
scriptKGgen = sp.simplify(sp.exp(2*phi)*(KKg - trKg**2))
check("NON-ROUND: e^{2phi}(K_ABK^AB - K^2) is phi-FREE for general symmetric h_AB(r)",
      phi not in scriptKGgen.atoms(sp.Function) or sp.simplify(sp.diff(scriptKGgen, phi)) == 0)
# hence phi enters the FULL G action ONLY via (Z/2)√h phi'^2  (R2[h], 𝒦_G, L_m all phi-free)
# => phi-EL: d/dr( Z A(r) phi' ) = 0 with A(r) = ∮√h dΩ > 0 : the SAME constant-flux structure.
print("   (=> full G action phi-dependence = kinetic term only; phi-EL = (Z A(r) phi')' = 0, A=∮√h>0:")
print("    the constant-flux/deadness argument is NOT round-scoped within the constrained frame.)")

print()
print("ALL PASS" if all(c for _, c in ok) else "SOME FAILED")
