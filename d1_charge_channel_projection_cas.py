"""
CAS for the charge-channel-projection MAP.
Data-blind. No target-fitting: we compute native objects and REPORT.
sympy only, exact.
"""
import sympy as sp

th, ph = sp.symbols('theta phi', real=True)

# --- hedgehog / degree-1 map n : S^2(space) -> S^2(target) ---
n = sp.Matrix([sp.sin(th)*sp.cos(ph),
               sp.sin(th)*sp.sin(ph),
               sp.cos(th)])

n_th = n.diff(th)
n_ph = n.diff(ph)

# winding density (the pullback area form coefficient) = n . (d_th n x d_ph n)
cross = n_th.cross(n_ph)
w_density = sp.simplify(n.dot(cross))
print("TASK-A: total winding density n.(dn x dn) =", w_density)          # expect sin(theta)

total = sp.integrate(sp.integrate(w_density, (ph, 0, 2*sp.pi)), (th, 0, sp.pi))
print("        total flux INT w = ", sp.simplify(total), " ; degree (1/4pi)INT =", sp.simplify(total/(4*sp.pi)))

# --- PER-TARGET-AXIS decomposition of the unit winding ---
# w_density = sum_a n_a * (dn x dn)_a. Compute each axis' contribution.
print("\nTASK-B: per-target-axis winding shares (does the unit degree split into equal thirds?)")
shares = []
for a in range(3):
    term = sp.simplify(n[a]*cross[a])                    # a-th channel of n.(dn x dn), NO sum
    Ia = sp.integrate(sp.integrate(term, (ph, 0, 2*sp.pi)), (th, 0, sp.pi))
    Ia = sp.simplify(Ia)
    shares.append(Ia)
    print(f"        channel a={a+1}:  INT n_a (dn x dn)_a = {Ia}   = (deg) {sp.simplify(Ia/(4*sp.pi))}")
print("        sum of channels =", sp.simplify(sum(shares)), " (must equal total flux", sp.simplify(total), ")")
print("        each channel / total =", [sp.simplify(s/total) for s in shares])

# --- SO(3) isotropic second moment <n_a n_b> over the round sphere ---
print("\nTASK-C: SO(3) isotropy second moment <n_a n_b> = INT n_a n_b dOmega / INT dOmega")
dOmega = sp.sin(th)
norm = sp.integrate(sp.integrate(dOmega,(ph,0,2*sp.pi)),(th,0,sp.pi))
M = sp.zeros(3,3)
for a in range(3):
    for b in range(3):
        M[a,b] = sp.simplify(sp.integrate(sp.integrate(n[a]*n[b]*dOmega,(ph,0,2*sp.pi)),(th,0,sp.pi))/norm)
print("        <n_a n_b> =")
sp.pprint(M)
print("        diagonal entries (each component's share):", [M[i,i] for i in range(3)])
print("        trace <|n|^2> =", sp.simplify(M.trace()), " (unit-vector constraint => sums to 1)")

# --- eta algebra: is eta = (1/2) q^2 native? keep every factor explicit ---
print("\nTASK-D: eta = 1/2 q^2 factor audit (report, do NOT target 1/18)")
q = sp.symbols('q', positive=True)          # public channel fraction (SYMBOL, not fixed)
Z, rho_s = sp.symbols('Z rho_s', positive=True)
# corpus interface chain: B = p/2 ; isotropy factor = 1/3 ; eta = B * (1/3) with p = q
p = q
B = p/2                                       # phi=0 interface extrinsic-curvature budget DK*R = p/2
iso = sp.Rational(1,3)                         # round-S2 isotropy share <n_a^2>
eta_chain = sp.simplify(B*iso)                # = q/2 * 1/3
print("        interface-chain eta = (p/2)*(1/3) with p=q :", eta_chain, "= q^2/2 only if the 1/3 factor IS q:",
      sp.simplify(eta_chain.subs(q, sp.Rational(1,3))), "at q=1/3")
# native seal energy (DERIVED object, D1 verifier): U_seal = 2 - q^2/(2 Z rho_s^2)
eta_seal = q**2/(2*Z*rho_s**2)
print("        native seal quadratic coefficient eta_seal = q^2/(2 Z rho_s^2)")
print("        eta_seal == (1/2) q^2  iff  Z rho_s^2 = ", sp.solve(sp.Eq(eta_seal, q**2/2), Z*rho_s**2))
# the L2 kinetic 1/2 and the seal 1/2 are the two native 1/2 candidates
print("        native 1/2 present in: L2 kinetic (xi/2) and U_seal (.../2) -> the 1/2 itself IS native")

# --- readout comparison: which native readout gives what ---
print("\nTASK-E: native SCALAR charge readouts")
print("        degree readout (1/4pi)INT omega_H1 =", sp.simplify(total/(4*sp.pi)), " (FULL unit)")
print("        Hopf Q_H (Whitehead, integer)      = 1 (FULL unit, by construction)")
print("        single-channel share               =", sp.simplify(shares[0]/total), " (requires SELECTING one axis)")
