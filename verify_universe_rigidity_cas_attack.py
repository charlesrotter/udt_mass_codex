"""BLIND ADVERSARIAL VERIFIER — T1 'two-mirror rigidity' CAS attack.
System (confirmed from cell_solver_round.py / round_matter_reduction_results.md / native_geometric_action_results.md):
  P: phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
     rho'' = 2 phi' rho'  - (Z/4) rho e^{2phi} phi'^2 + S(r)
Checks:
 1. Reconstruct BOTH EOMs from the banked native action (round, W=1, Route A) + phi-blind matter -> phi-EOM matter-free.
 2. Claim (i): (Z rho^2 phi')' = 4 e^{-2phi} rho'^2 identically ON the phi-EOM, for ANY S in rho''.
 3. Z-independence (incl. Z<0) and source-sign flip.
 4. Route-B fork: action gains 2 e^phi K phi' -> new flux Phi~ = Z rho^2 phi' + 4 rho rho'; same RHS.
 5. Reproduce the banked matter source sign from L_m of round_matter_reduction_results.md.
"""
import sympy as sp

r = sp.symbols('r', real=True)
Z, xi, kappa, N, Ir, I4t = sp.symbols('Z xi kappa N I_r I_4theta', real=True, positive=False)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
S = sp.Function('S')(r)          # arbitrary phi-blind source (enters rho'' only)

p, pp = phi.diff(r), phi.diff(r, 2)
q, qq = rho.diff(r), rho.diff(r, 2)

def EL(L, f):
    return sp.diff(L, f.diff(r)).diff(r) - sp.diff(L, f)

# ---------- 1. Banked native action, round P (W=1): sqrt(h)=rho^2 (per solid angle), R2=2/rho^2,
#             K_AB = e^{-phi} rho rho' Omega_AB -> Kcal = K_ABK^AB - K^2 = -2 e^{-2phi} rho'^2/rho^2
L_geo = (Z/2)*rho**2*p**2 + 2 - 2*sp.exp(-2*phi)*q**2      # sqrt(h)[ (Z/2)phi'^2 + R2 + Kcal ]
# phi-blind matter, generic M(rho) (no phi anywhere):
M = sp.Function('M')(rho)
L = L_geo + M

el_phi = sp.simplify(EL(L, phi))
el_rho = sp.simplify(EL(L, rho))

# solve each for the second derivative
pp_sol = sp.solve(sp.Eq(el_phi, 0), pp)[0]
qq_sol = sp.solve(sp.Eq(el_rho, 0), qq)[0]

pp_claim = 4*sp.exp(-2*phi)*q**2/(Z*rho**2) - 2*p*q/rho
qq_claim_geo = 2*p*q - (Z/4)*rho*sp.exp(2*phi)*p**2

print("== 1. EOMs from the banked action ==")
print("phi-EOM matches solver form (matter ABSENT):", sp.simplify(pp_sol - pp_claim) == 0)
res_rho = sp.simplify(qq_sol - qq_claim_geo)
print("rho-EOM = geo + matter source; matter part  =", sp.simplify(res_rho))
print("   (expected (e^{2phi}/4) dM/drho):", sp.simplify(res_rho - sp.exp(2*phi)/4*sp.diff(M, rho)) == 0)

# ---------- 5. banked L_m reproduces the banked source sign
L_m = -(xi/2)*(rho**2*Ir) - (kappa*N**2/2)*(I4t/rho**2)    # rho-dependent pieces only
el_rho_m = EL(L_geo + L_m, rho)
qq_m = sp.solve(sp.Eq(el_rho_m, 0), qq)[0]
S_banked = sp.exp(2*phi)/4*(xi*rho*Ir - kappa*N**2*I4t/rho**3)
print("== 5. banked matter source (e^{2phi}/4)(xi rho I_r - kappa N^2 I_4t/rho^3):",
      sp.simplify(qq_m - qq_claim_geo - S_banked) == 0)

# ---------- 2. Claim (i): Phi' identity uses ONLY the phi-EOM; S arbitrary
Phi = Z*rho**2*p
Phip = Phi.diff(r)
# substitute the phi-EOM (claimed form); rho'' NEVER appears in Phi' -> S cannot enter
Phip_on_shell = Phip.subs(pp, pp_claim)
print("== 2. Phi' on the phi-EOM ==")
print("Phi' == 4 e^{-2phi} rho'^2 :", sp.simplify(Phip_on_shell - 4*sp.exp(-2*phi)*q**2) == 0)
print("Phi' contains rho''? ->", Phip.has(qq), "(False => S can NEVER enter the identity)")

# ---------- 3. Z-independence / sign forks
print("== 3. forks ==")
print("Phi' result contains Z?:", sp.simplify(Phip_on_shell).has(Z), "(False => holds for Z<0 too)")
# flipped source sign in the phi-equation:
pp_flip = -4*sp.exp(-2*phi)*q**2/(Z*rho**2) - 2*p*q/rho
print("flipped-sign phi-eq: Phi' == -4 e^{-2phi} rho'^2 :",
      sp.simplify(Phip.subs(pp, pp_flip) + 4*sp.exp(-2*phi)*q**2) == 0,
      "(one-signed either way -> two-mirror rigidity survives the flip)")

# ---------- 4. Route-B fork: + sqrt(h) * 2 e^phi K phi' with K = 2 e^{-phi} rho'/rho -> +4 rho rho' phi'
L_B = 4*rho**2*p**2 + 4*rho*q*p + 2 - 2*sp.exp(-2*phi)*q**2 + M     # Z=8 forced in route B
el_phi_B = EL(L_B, phi)
PhiB = 8*rho**2*p + 4*rho*q            # conjugate momentum dL/dphi'
# EL says d/dr(dL/dphi') = dL/dphi  ->  PhiB' = 4 e^{-2phi} rho'^2 (matter still absent: M has no phi)
lhs = PhiB.diff(r) - 4*sp.exp(-2*phi)*q**2
print("== 4. Route B ==")
print("phi-EL(route B) == d/dr(PhiB) - 4e^{-2phi}rho'^2 :", sp.simplify(el_phi_B - lhs) == 0)
print("   => route-B flux PhiB = Z rho^2 phi' + 4 rho rho' (Z=8), SAME nonneg RHS;")
print("      mirror seal phi'=rho'=0 both ends -> PhiB=0 both ends -> rigidity STILL follows;")
print("      phi'=0-ONLY seals: PhiB(ends)=4 rho rho' != 0 possible -> monotone argument does NOT close.")

# ---------- rigidity chain (route A), stated as verified algebra:
# Phi(in)=Phi(out)=0 (phi'=0 ends, rho>0), Phi'>=0 -> Phi==0 -> rho'==0 pointwise (e^{-2phi}>0 on compact,
# phi in C^1 -> bounded) -> phi' = Phi/(Z rho^2) == 0 -> rho''=S -> S==0 pointwise.
print("== rigidity chain uses: rho>0 on [in,out]; phi,rho in C^1, EOM a.e.; Phi in AC (no phi-coupled surface source) ==")
