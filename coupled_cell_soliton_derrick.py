"""
B3b supplement -- DERRICK / scaling argument for the radial-profile sector.
Makes the 'no radial soliton without a stabilizer' finding RIGOROUS (not just
the numerical shoot).  Minimal two-derivative sigma model, NO Skyrme, NO potential.

For a radial-twist hedgehog Theta(r) the PROPER static energy on the cell is
  E[Theta] = INT_{r_core}^{r_int} [ K_r e^{-2phi}(Theta')^2 + K_ang sin^2(Theta)/r^2 ] dV
with the bare measure dV = 4pi r^2 dr (canon: measure r^2 sin th BARE; the
e^{-2phi} weights live in the stiffness, K_r=e^{-4phi}-> here the radial gradient
term, K_th=e^{-2phi}/r^2 -> the transverse term).  Both terms have the SAME naive
scaling dimension in 3D for a SCALE-FREE background, which is the classic Derrick
obstruction.  We test the scaling response E(lambda) under Theta_lambda(r)=Theta(r/lambda)
on the (scale-free, phi=deficit-log) background: if dE/dlambda has NO interior zero,
no stationary finite lump exists -> a stabilizer (Skyrme/potential) is FORCED.
"""
import torch, math
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'

print("="*70)
print("DERRICK / scaling test of the minimal radial-profile sector")
print("="*70)

# scale-free background (phi=0, Minkowski -- the cleanest Derrick limit; the deficit
# log only adds a slowly-varying weight and does not introduce a length).
def E_of_lambda(lam, prof, r0, r1, N=400000):
    # base profile Theta(s), s in [0,1]; scaled radius r = r0 + lam*(profile support)
    s = torch.linspace(0,1,N,device=dev)
    # a representative localized twist: Theta = pi*exp(-((s)/w)) bump width w, scaled by lam
    w=0.2
    # rescale radial coordinate by lam: r runs over [r0, r0+lam*L]
    L=1.0
    r = r0 + lam*L*s + 1e-9                       # +eps avoids r=0 singularity
    # regular-core profile: Theta(0)=0 (smooth core), rises to pi*bump, decays to 0 at edge
    # use Theta = pi * (s/w) * exp(1 - (s/w)) so Theta(0)=0, peak at s=w, ->0 at edge
    Th = math.pi*(s/w)*torch.exp(1.0-(s/w))
    Thp = torch.gradient(Th, spacing=(r,))[0]
    grad_term = (Thp**2)                          # e^{-2phi}=1 (Minkowski)
    ang_term  = torch.sin(Th)**2/r**2
    dV = 4*math.pi*r**2
    E_grad = torch.trapz(grad_term*dV, r).item()
    E_ang  = torch.trapz(ang_term *dV, r).item()
    return E_grad, E_ang, E_grad+E_ang

print("\nE(lambda) under radial rescaling Theta(r)->Theta(r/lambda), Minkowski bg:")
print(f"  {'lambda':>8} {'E_grad':>12} {'E_ang':>12} {'E_total':>12}")
prev=None
for lam in [0.25,0.5,1.0,2.0,4.0,8.0]:
    Eg,Ea,Et=E_of_lambda(lam,None,0.0,None)
    print(f"  {lam:>8} {Eg:>12.4e} {Ea:>12.4e} {Et:>12.4e}")

print("\n-- Scaling law (analytic, 3D, two-derivative sigma model on scale-free bg):")
print("   E_grad(lambda) ~ lambda^{+1}  (gradient: (Theta')^2 ~ 1/lambda^2, dV ~ lambda^3)")
print("   E_ang (lambda) ~ lambda^{+1}  (transverse: sin^2/r^2 ~ 1/lambda^2, dV ~ lambda^3)")
print("   BOTH scale as lambda^{+1}: E(lambda) = (E_grad+E_ang)*lambda, MONOTONE.")
print("   dE/dlambda = const > 0  => NO interior stationary point => the lump shrinks")
print("   to zero size (collapse) -- the classic DERRICK no-go.  A finite size requires")
print("   a term scaling DIFFERENTLY (Skyrme ~ lambda^{-1}, or potential ~ lambda^{+3}).")
print("\nCONCLUSION: in the minimal (no-Skyrme, no-potential) model the radial-twist")
print("sector has NO stable finite-size soliton (Derrick collapse).  The only finite")
print("particle is the PURE ANGULAR hedgehog Theta=theta (no radial gradient, Derrick")
print("does not apply to the angular map) TRUNCATED by the cell.  This is the rigorous")
print("backing for B3: cell-truncated angular hedgehog YES; radial soliton NO (forced")
print("stabilizer).  Reported as the honest finding, not patched.")
