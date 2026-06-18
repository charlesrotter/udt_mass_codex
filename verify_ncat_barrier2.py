#!/usr/bin/env python3
"""Probe whether degree-1 is metastable (barrier) or BC-held. Use a regular
unwinding path that KEEPS poles at 0/pi (so no fake pole divergence): shrink the
polar winding into a thin shell that can then be pushed off the seal. Compare
energy of (a) full degree-1, (b) degree pushed toward the core / seal, (c) vacuum.
Also relax from VACUUM seed to see if degree-1 is even reached (it won't be if it's
a separate basin)."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, torch
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
PI=math.pi
exec(open('/home/udt-admin/udt_mass_codex/verify_ncat_barrier.py').read().split('C=Cell()')[0])  # reuse Cell/energy/grads/realized_deg
C=Cell()

# Regular unwinding: keep G(theta=0)=0, G(theta=pi)=pi at every r EXCEPT let the
# radial profile push the texture toward the seal and "off" the cell. Param: the
# texture lives only for r> r0(t); inside r0 it's vacuum (G=0 for all theta but
# poles... ) -- but G(pi)=pi forced. The honest regular homotopy on a CONTRACTIBLE
# ball that removes a pi_2 texture is: slide the map's image to avoid a point.
# Simplest physical proxy: radial Neumann FREE relax from vacuum seed:
def pole_only(G):
    G=G.clone();G[:,0]=0.0;G[:,-1]=PI;return G

print("[B-3] Relax from VACUUM-ish seed (G=small) with poles fixed 0/pi, deep-cell:")
G=(0.01*C.TH).requires_grad_(True)
# can't fix poles to 0/pi AND start at vacuum -- poles force a winding. Start G=theta*0.02
opt=torch.optim.Adam([G],lr=0.02)
for it in range(8000):
    opt.zero_grad();E=energy(G,C);E.backward();opt.step()
    with torch.no_grad():G.data.copy_(pole_only(G.data))
with torch.no_grad():
    print(f"   final E={energy(G,C).item():.4f} deg(seal)={realized_deg(G.data,C,C.Nr-2):+.3f}")

print("\n[B-4] Energy vs radial LOCATION of the texture (poles regular throughout):")
print("   Build G(r,th)=theta for r in a window [r0,r0+w], =0 below, =pi-... -- but")
print("   poles need G(pi)=pi at ALL r. The ONLY regular way to have deg=0 at a shell")
print("   is G independent of theta there (constant), which violates G(0)=0,G(pi)=pi.")
print("   => CONCLUSION: with poles pinned 0/pi at every r, EVERY shell carries deg=1.")
print("   The degree is carried by the POLAR BC. Whether that BC is 'held' or native")
print("   is the real question (axis B verdict).")

# Quantify the barrier height the RIGHT way: lowest-energy path from deg=1 to deg=0
# must pass through a configuration where some shell has a near-singular gradient
# (the hedgehog core punches through). Estimate min over a 1-param family that
# nucleates a vacuum core of radius rho and pushes the winding outward:
print("\n[B-5] Nucleate-vacuum-core path (regular, poles only nonzero where texture is):")
print("   rho   E(rho)     note")
for rho_idx in [0,5,10,20,40,60,80,99]:
    G=C.TH.clone()
    # for r below r[rho_idx]: collapse winding to 0 (G=0 all theta -> but then poles
    # mismatch). Use G = theta * ramp(r) where ramp=0 for r<r0, 1 above:
    ramp=torch.clamp((C.R-C.r[rho_idx])/(0.5),0,1)
    G=ramp*C.TH
    G=pole_only(G)  # re-impose poles -> reintroduces winding at poles for r<r0
    E=energy(G,C).item()
    print(f"  {C.r[rho_idx].item():5.2f}  {E:10.2f}  deg(core)={realized_deg(G,C,1):+.2f} deg(seal)={realized_deg(G,C,C.Nr-2):+.2f}")
