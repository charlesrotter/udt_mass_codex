#!/usr/bin/env python3
"""
WP-HE1 — Asymptotics as phi -> +infty (hard native edge).
Path A (areal D=r) and Path B (free D_A): vacuum + dilated source.
MAP: macro_native_edge_HARD_MAP.md
No shooting grids; CAS leading balances only.
"""
from __future__ import annotations

import sympy as sp

print("=" * 70)
print("WP-HE1 ASYMPTOTICS φ → +∞")
print("=" * 70)

r = sp.symbols("r", positive=True)
Z = sp.symbols("Z", positive=True)
q, c0, v, w, A, B, rs = sp.symbols("q c0 v w A B r_star", real=True)
rho0 = sp.symbols("rho0", positive=True)

# =============================================================================
# PATH A: D_A = r fixed, EH empty, R1 kinetic + optional dilated dust
# Vacuum: (r^2 phi')' = 0
# With dilated L_m = -rho(r) r^2 e^{-2 phi}  (areal measure ~ r^2)
# =============================================================================
print("\n" + "-" * 70)
print("PATH A — areal D_A=r")
print("-" * 70)

phi = sp.Function("phi")
ph = phi(r)
php = sp.diff(ph, r)
phpp = sp.diff(ph, r, 2)
rho = sp.Function("rho")

# Vacuum EL: d/dr(Z r^2 phi') = 0
elA_vac = sp.diff(Z * r**2 * php, r)
print("\n[A1] Vacuum EL_phi ~ d/dr(Z r^2 phi') =", elA_vac)
print("     Solution: phi = c0 - q/r  (Coulomb)")
print("     As r->0+: phi -> ±∞ if q≠0, but that is CENTER singularity, not outer edge.")
print("     As r->∞: phi -> c0 finite. NO outer φ→∞ in vacuum Path A Coulomb.")

# Can phi->∞ at finite r_*>0?
# Suppose phi ~ -alpha log(r_*-r) as r->r_*- with alpha>0 => phi->+∞
# Then phi' ~ alpha/(r_*-r), phi'' ~ alpha/(r_*-r)^2
s = sp.symbols("s", positive=True)  # s = r_star - r
alpha = sp.symbols("alpha", positive=True)
# d/dr = -d/ds
# phi = -alpha log(s)  => phi->+∞ as s->0+
# php = d phi/dr = -alpha/s * ds/dr = alpha/s
# phpp = d/dr (alpha/s) = alpha/s^2 * (-ds/dr wait) ds/dr=-1, d(1/s)/dr = d(1/s)/ds * ds/dr = (-1/s^2)(-1)=1/s^2
# php = alpha/s, phpp = alpha/s^2
php_as = alpha / s
phpp_as = alpha / s**2
# el ~ Z d/dr(r^2 phi') = Z (2 r phi' + r^2 phi'')
# near r=r_star, r~r_star fixed
el_lead = sp.simplify(2 * rs * php_as + rs**2 * phpp_as)
print("\n[A2] Outer blowup ansatz phi = -alpha log(r_*-r), s=r_*-r:")
print("     (2 r phi' + r^2 phi'') ~", el_lead, "  (order 1/s^2, nonzero)")
print("     Vacuum EL requires this = 0 => IMPOSSIBLE for alpha>0.")
print("     => Path A vacuum CANNOT develop phi->+∞ at finite outer r_*.")

# With dilated dust: L = (Z/2) r^2 (phi')^2 - rho(r) r^2 e^{-2 phi}
# EL_phi: d/dr(Z r^2 phi') - 2 rho r^2 e^{-2 phi} = 0   (since ∂L_m/∂phi = 2 rho r^2 e^{-2phi} for L_m=-rho r^2 e^{-2phi})
# Using convention: d/dr(Z r^2 phi') = 2 rho r^2 e^{-2 phi}
print("\n[A3] Dilated dust on Path A: d/dr(Z r^2 phi') = 2 rho r^2 e^{-2 phi}")
# Near s->0, phi~-alpha log s, e^{-2 phi} = e^{2 alpha log s} = s^{2 alpha}
# RHS ~ 2 rho rs^2 s^{2 alpha} -> 0 if alpha>0
# LHS ~ Z * d/dr(r^2 alpha/s) ~ Z rs^2 * alpha/s^2  (order 1/s^2)
# 1/s^2 vs s^{2 alpha} -> cannot balance unless rho blows up faster than any power
print("     LHS ~ O(1/s^2); RHS ~ rho * s^{2 alpha} -> 0 for bounded rho, alpha>0.")
print("     => Finite rho CANNOT balance vacuum blowup. Need rho ~ s^{-2-2alpha} or harder.")
# If rho also dilates only by e^{-2phi}, profile f(r) bounded: still RHS->0
print("     Bounded profile f(r) with L_m ∝ f(r) e^{-2phi}: still RHS->0; NO finite-r outer blowup.")

# What if approach is phi ~ beta / s^mu?
mu, beta = sp.symbols("mu beta", positive=True)
# phi = beta / s^mu => php = beta mu / s^{mu+1}, phpp = beta mu (mu+1)/s^{mu+2}
php2 = beta * mu / s ** (mu + 1)
phpp2 = beta * mu * (mu + 1) / s ** (mu + 2)
el2 = sp.simplify(2 * rs * php2 + rs**2 * phpp2)
print("\n[A4] Stronger blowup phi = beta / (r_*-r)^mu:")
print("     (2r phi'+r^2 phi'') ~", el2)
print("     Still ~ s^{-(mu+2)} ≠ 0; vacuum cannot cancel.")
print("     Dilated bounded rho: RHS ~ e^{-2 beta / s^mu} is BEYOND all powers (exp small).")
print("     => Even worse imbalance (RHS tinier). Dilated dust suppresses source at edge.")

print("\n[A5] Path A CONCLUSION:")
print("     Outer φ→+∞ at finite r_* is INCOMPATIBLE with Path A vacuum EL.")
print("     Dilated dust with bounded profile makes it harder, not easier.")
print("     Only outer φ→+∞ in Path A Coulomb is at the CENTER r=0 (q>0 or sign).")

# =============================================================================
# PATH B: free D_A, EH + kinetic ± dilated dust
# =============================================================================
print("\n" + "-" * 70)
print("PATH B — free D_A + EH + kinetic")
print("-" * 70)

DA = sp.Function("D_A")
D = DA(r)
Dp = sp.diff(D, r)
Dpp = sp.diff(D, r, 2)

# EL from earlier (vacuum):
# EL_phi = -Z D^2 phpp - 2 Z D Dp php + 4 D exp(-2phi) Dpp = 0
# EL_D = (Z D exp(2phi) php^2 - 8 D php^2 + 4 D phpp + 8 Dp php - 4 Dpp) exp(-2phi) = 0

# Leading as phi -> +∞ with D, Dp, Dpp remaining finite nonzero:
# EL_phi: e^{-2phi} Dpp term -> 0, so -Z D^2 phpp - 2 Z D Dp php ≈ 0
# => d/dr(D^2 php) ≈ 0  if Z D != 0  => D^2 php ≈ const = Q
# If D finite nonzero at edge, php ~ Q/D^2 stays finite => phi CANNOT -> ∞ in finite Δr
print("\n[B1] If D_A, D_A', D_A'' stay finite as phi->+∞:")
print("     EL_phi => e^{-2phi} D'' term drops => d/dr(D_A^2 phi')≈0 => phi' ~ C/D_A^2 finite")
print("     => phi grows at most linearly in r if C≠0, needs INFINITE r to reach phi=∞.")
print("     => NO finite-r outer edge if transverse radius stays finite and smooth.")

# Need D_A -> 0 or D'' blow up for phi->∞ at finite r
print("\n[B2] For finite-r blowup, need singular transverse geometry or derivatives.")
print("     Cases:")

# Case D -> D* finite, php ~ alpha/s
print("\n  Case B2a: D->D*>0 finite, phi=-alpha log s, D'' finite:")
# EL_phi ~ -Z D*^2 (alpha/s^2) - 2 Z D* Dp (alpha/s) + 4 D* e^{2 alpha log s} Dpp
# = -Z D*^2 alpha/s^2 + O(1/s) + 4 D* s^{2 alpha} Dpp
# Leading -1/s^2 cannot cancel unless D->0 or alpha=0
print("     EL_phi ~ -Z D*^2 alpha/s^2 + ... + O(s^{2alpha})")
print("     Unbalanced 1/s^2 unless alpha=0. FAIL.")

# Case D -> 0 as s^nu
nu = sp.symbols("nu", positive=True)
print("\n  Case B2b: D ~ k s^nu, phi = -alpha log s, as s->0+:")
k = sp.symbols("k", positive=True)
# php = alpha/s, phpp = alpha/s^2
# Dp = k nu s^{nu-1} * ds/dr = -k nu s^{nu-1}
# Dpp = d/dr Dp = -k nu (nu-1) s^{nu-2} * (-1) = k nu (nu-1) s^{nu-2}
# EL_phi = -Z D^2 phpp - 2 Z D Dp php + 4 D exp(-2phi) Dpp
# D^2 = k^2 s^{2nu}
# -Z k^2 s^{2nu} * alpha/s^2 = -Z k^2 alpha s^{2nu-2}
# -2 Z (k s^nu) (-k nu s^{nu-1}) (alpha/s) = 2 Z k^2 nu alpha s^{nu} s^{nu-1} s^{-1}
#   = 2 Z k^2 nu alpha s^{2nu-2}
# 4 (k s^nu) s^{2 alpha} * k nu (nu-1) s^{nu-2} = 4 k^2 nu (nu-1) s^{nu + 2 alpha + nu - 2}
#   = 4 k^2 nu (nu-1) s^{2nu+2alpha-2}
term1 = -Z * k**2 * alpha * s ** (2 * nu - 2)
term2 = 2 * Z * k**2 * nu * alpha * s ** (2 * nu - 2)
term3 = 4 * k**2 * nu * (nu - 1) * s ** (2 * nu + 2 * alpha - 2)
# exp(-2phi)=s^{2 alpha}
print("     term1 (kin phi''):", term1)
print("     term2 (kin mix):  ", term2)
print("     term3 (EH D''):   ", term3)
# Balance powers: kinetic terms ~ s^{2nu-2}; EH ~ s^{2nu+2alpha-2}
# For EH to matter, need 2nu+2alpha-2 = 2nu-2 => alpha=0 contradiction
# So EH is SUBDOMINANT (higher power if alpha>0: 2nu+2alpha-2 > 2nu-2)
# Leading: (term1+term2) = Z k^2 alpha s^{2nu-2} (-1 + 2 nu) = 0
# => -1+2 nu = 0 => nu = 1/2
bal = sp.simplify(term1 + term2)
print("     kin sum:", bal, " => vanishes if nu=1/2 (for alpha≠0, k≠0)")
print("     EH subdominant when alpha>0 (extra s^{2alpha}).")
print("     => Candidate: D_A ~ k sqrt(r_*-r), phi ~ -alpha log(r_*-r)")

# Check EL_D leading for nu=1/2
print("\n[B3] EL_D at nu=1/2, phi=-alpha log s:")
# inside: Z D e^{2phi} php^2 - 8 D php^2 + 4 D phpp + 8 Dp php - 4 Dpp = 0
# e^{2phi} = e^{-2 alpha log s} = s^{-2 alpha}
# php=alpha/s, phpp=alpha/s^2
# D = k s^{1/2}, Dp = -k (1/2) s^{-1/2}, Dpp = k (1/2)(-1/2) s^{-3/2} * (-1)? 
# d/dr = -d/ds; Dp = dD/dr = k*(1/2)*s^{-1/2}*(-1) = - (k/2) s^{-1/2}
# Dpp = d/dr Dp = -(k/2)*(-1/2)*s^{-3/2}*(-1) = -(k/2)(1/2) s^{-3/2} = -k/4 s^{-3/2}
# Wait: d/ds s^{-1/2} = (-1/2) s^{-3/2}; d/dr = -d/ds => d/dr s^{-1/2} = +1/2 s^{-3/2}
# Dp = -(k/2) s^{-1/2}
# Dpp = -(k/2) * (1/2) s^{-3/2} = -k/4 s^{-3/2}

# Z D e2 php^2 = Z k s^{1/2} * s^{-2alpha} * alpha^2 / s^2 = Z k alpha^2 s^{1/2 - 2alpha - 2}
# -8 D php^2 = -8 k s^{1/2} alpha^2 / s^2 = -8 k alpha^2 s^{1/2-2}
# 4 D phpp = 4 k s^{1/2} alpha / s^2 = 4 k alpha s^{1/2-2}
# 8 Dp php = 8 (-k/2 s^{-1/2}) (alpha/s) = -4 k alpha s^{-1/2-1} = -4 k alpha s^{-3/2}
# -4 Dpp = -4 (-k/4 s^{-3/2}) = k s^{-3/2}

# Powers:
# s^{1/2-2alpha-2} = s^{-3/2 - 2alpha} from first term - most singular if alpha>0? 
# -3/2-2alpha < -3/2 for alpha>0, so first term dominates unless Z alpha =0
print("     Dominant EL_D piece ~ Z D e^{2phi} (phi')^2 ~ s^{-3/2 - 2 alpha}")
print("     Other pieces ~ s^{-3/2} or weaker.")
print("     For alpha>0 this BLOWS and does not cancel (only one such term).")
print("     => nu=1/2 log-blowup FAIL EL_D unless alpha=0.")

# Try phi = beta / s^mu with D = k s^nu
print("\n[B4] Power blowup phi = beta/s^mu, D = k s^nu — leading power hunt")
# php = beta mu / s^{mu+1}, phpp = beta mu(mu+1)/s^{mu+2}
# Dp = -k nu s^{nu-1}, Dpp = k nu(nu-1) s^{nu-2}  [with d/dr=-d/ds: 
# D=k s^nu, dD/ds = k nu s^{nu-1}, dD/dr = -k nu s^{nu-1}
# d2D/dr2 = d/dr(-k nu s^{nu-1}) = -k nu (nu-1) s^{nu-2} * (-1) = k nu(nu-1) s^{nu-2}

# EL_phi terms powers in s:
# -Z D^2 phpp ~ s^{2nu} * s^{-(mu+2)} = s^{2nu - mu - 2}
# -2 Z D Dp php ~ s^nu * s^{nu-1} * s^{-(mu+1)} = s^{2nu - mu - 2}
# 4 D e^{-2phi} Dpp : e^{-2phi} = exp(-2 beta / s^mu) is ESSENTIALLY ZERO faster than any power if beta>0
print("     If phi = +beta/s^mu -> +∞, then e^{-2phi} = exp(-2 beta/s^mu) is beyond power-suppressed.")
print("     EH piece in EL_phi (~ e^{-2phi} D'') is NEGLIGIBLE.")
print("     EL_phi reduces to kinetic: d/dr(D^2 phi')=0.")
print("     With D~s^nu, phi~s^{-mu}: D^2 phi' ~ s^{2nu} * s^{-(mu+1)} = s^{2nu-mu-1}")
print("     d/dr of that ~ s^{2nu-mu-2} — set exponent balance only if this is const:")
print("     need 2nu - mu - 1 = 0 => mu = 2nu - 1 for flux const nonzero.")
print("     Flux const C: if C≠0, integrate phi ~ int C/D^2 dr — near s=0,")
print("     int s^{-2nu} ds converges at 0 if -2nu > -1 i.e. nu < 1/2,")
print("     GIVES FINITE phi change, not phi->∞.")
print("     For phi->∞ need int^s C/D^2 diverge: -2nu <= -1 => nu >= 1/2.")
print("     Combined with mu=2nu-1>=0 => nu>=1/2. At nu=1/2, mu=0 (log case already failed EL_D).")
print("     At nu>1/2, mu>0, D^2 phi'~s^{2nu-mu-1}=s^0=const, phi~ int s^{-2nu} ds")
print("     ~ s^{1-2nu}/(1-2nu) -> ∞ as s->0 if nu>1/2. GOOD for phi->∞.")

print("\n[B5] EL_D with e^{2phi} (phi')^2 term when phi->+∞:")
print("     e^{2phi} (phi')^2 is ENORMOUS (exp(+2 beta/s^mu) * powers).")
print("     Dominates EL_D unless coefficient D*Z -> 0 fast enough that product finite.")
print("     D * e^{2phi} * (phi')^2 ~ s^nu * exp(2 beta/s^mu) * s^{-2mu-2} -> ∞ for any nu, beta>0, mu>0.")
print("     => EL_D CANNOT hold for free D_A with phi->+∞ at finite r if Z≠0 and D not identically 0.")
print("     Only escape: Z=0 (drop kinetic) or D≡0 (degenerate metric) or abandon free-D_A EH form.")

print("\n[B6] Path B CONCLUSION:")
print("     Under current Path B vacuum (EH + R1 kinetic, Z>0):")
print("     phi->+∞ at finite chart radius with nondegenerate D_A is BLOCKED by EL_D")
print("     (catastrophic e^{2phi}(phi')^2 term).")
print("     Dilated dust adds e^{-2phi} sources -> 0 at edge; cannot cancel e^{2phi} blowup.")

# Path A vs B summary table
print("\n" + "=" * 70)
print("SUMMARY TABLE")
print("=" * 70)
print(
    """
| Setting | Outer φ→∞ at finite r_* |
|---------|-------------------------|
| Path A vacuum Coulomb | NO (only center r=0) |
| Path A + dilated bounded ρ | NO (source vanishes at edge) |
| Path B vacuum, D smooth finite | NO (needs infinite r) |
| Path B vacuum, D→0 + φ→∞ | EL_D blocked by e^{2φ}(φ')² |
| Path B + dilated dust | Source thins; does not fix EL_D block |

HE1 RESULT: Hard edge φ→∞ at finite r is NOT supported by current Path A/B bulk.
Next theory step: modify bulk / gauge / edge definition (E-hard-2/3/4), not more IVP.
"""
)
print("DONE HE1")
