"""
INDEPENDENT blind adversarial re-derivation of UDT modified field equations.
Driver-level verifier. No constructor code reused. sympy from scratch.
Refute, don't confirm. Data-blind.
"""
import sympy as sp

r, t, th, ph = sp.symbols('r t theta phi_ang', real=True)
c0 = sp.symbols('c0', positive=True)
phi = sp.Function('phi')(r)   # the position field

print("="*70)
print("CLAIM 1: light speeds")
print("="*70)

# Metric diag(-e^{-2phi}c0^2, e^{2phi}, r^2, r^2 sin^2 th)
gtt = -sp.exp(-2*phi)*c0**2
grr = sp.exp(2*phi)

# Coordinate null radial speed: ds^2=0 => gtt dt^2 + grr dr^2 = 0
# (dr/dt)^2 = -gtt/grr
v_coord2 = sp.simplify(-gtt/grr)
print("coord (dr/dt)^2 =", v_coord2, "   expected c0^2 e^{-4phi}")
print("  matches c0^2 e^{-4phi}:", sp.simplify(v_coord2 - c0**2*sp.exp(-4*phi))==0)

# Locally measured: proper length / proper time
# proper radial length dl = sqrt(grr) dr ; proper time dtau = sqrt(-gtt)/c0 * dt
# v_local = dl/dtau = sqrt(grr) dr / (sqrt(-gtt)/c0 dt) = c0 sqrt(grr/(-gtt)) (dr/dt)
# with (dr/dt) = sqrt(-gtt/grr):
v_local = c0*sp.sqrt(grr/(-gtt))*sp.sqrt(-gtt/grr)
print("v_local (this metric) =", sp.simplify(v_local))

# General diagonal: gtt=-N(r)^2 c0^2? Use N,L arbitrary
N = sp.Function('N')(r); L = sp.Function('L')(r)
gtt_g = -N**2 ; grr_g = L**2
# proper time uses sqrt(-gtt); proper length sqrt(grr); coord speed sqrt(-gtt/grr)
# locally measured = sqrt(grr)*(dr) / (sqrt(-gtt)*dt) where dr/dt=sqrt(-gtt/grr)
dr_dt = sp.sqrt(-gtt_g/grr_g)
v_loc_gen = sp.simplify(sp.sqrt(grr_g)*dr_dt/sp.sqrt(-gtt_g))
print("v_local arbitrary diagonal N,L (in c0=1 proper units) =", v_loc_gen,
      "  => constant (=1), independent of N,L:", v_loc_gen==1)
