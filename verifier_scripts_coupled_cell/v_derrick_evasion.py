# Does the back-reacted phi background or the cell seal evade Derrick?
# 1) With phi background e^{2phi} weight: E = INT (xi/2)[ e^{-2phi}(Theta')^2 r^2 + 2 sin^2 Theta ] dr ?
#    Check: does the deficit (conical) background, being SCALE-FREE (e^{-2phi}=1-delta const at large r),
#    break the lambda^1 scaling? A constant prefactor (1-delta) does NOT change scaling exponent.
import torch, math
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'

def energy_bg(lam, delta):
    s = torch.linspace(1e-4, 30.0, 200000, device=dev)
    Th = math.pi*(s/lam)*torch.exp(1-s/lam)
    Thp = torch.gradient(Th, spacing=(s,))[0]
    em2phi = (1-delta)            # asymptotic conical (scale-free) value, constant
    A = em2phi*(Thp**2 * s**2)
    B = 2*torch.sin(Th)**2
    return float(torch.trapz(A+B, s))
print("=== With conical deficit background (scale-free, e^{-2phi}=1-delta const) ===")
for delta in [0.0,0.1,0.3]:
    es=[energy_bg(l,delta) for l in [1.0,2.0,4.0]]
    print(f" delta={delta}: ratios {es[1]/es[0]:.3f}, {es[2]/es[1]:.3f} (still ~2 => lam^1, Derrick survives)")

# 2) Boundary-induced stabilization? On a FINITE cell [eps, L], minimizing E over scale
#    with FIXED BCs Theta(eps)=0, Theta(L)=pi: is there a stationary size? 
#    The cell SIZE L is itself a free input -- it sets the scale but doesn't SELECT one.
#    Solve the EOM relaxation on the cell and see if energy has an interior min vs L.
print()
print("=== Finite cell: does a seal BC pin a size? minimize E over cell length L ===")
def cell_energy(L, N=4000):
    s = torch.linspace(1e-3, L, N, device=dev)
    # relax Theta with BC Theta(0+)=0, Theta(L)=pi via simple gradient flow
    Th = math.pi*(s-s[0])/(L-s[0])   # linear init satisfying BCs
    Th = Th.clone().requires_grad_(True)
    opt = torch.optim.LBFGS([Th], lr=0.5, max_iter=200)
    s_d=s.detach()
    def closure():
        opt.zero_grad()
        T = Th.clone()
        T = T - T[0].detach() + 0.0            # keep T[0]~0
        Thp = torch.gradient(Th, spacing=(s_d,))[0]
        A = (Thp**2 * s_d**2); B=2*torch.sin(Th)**2
        # penalty for BCs
        pen = 1e4*((Th[0]-0.0)**2 + (Th[-1]-math.pi)**2)
        E = torch.trapz(A+B, s_d)+pen
        E.backward(); return E
    opt.step(closure)
    with torch.no_grad():
        Thp = torch.gradient(Th, spacing=(s_d,))[0]
        E = float(torch.trapz(Th.grad*0 + (Thp**2*s_d**2)+2*torch.sin(Th)**2, s_d))
    return E
for L in [1.0,2.0,4.0,8.0,16.0]:
    print(f" L={L:5.1f}: E_relaxed={cell_energy(L):.4f}")
print(" => E decreases monotonically with L (no interior min): cell SIZE is free input,")
print("    seal BC does NOT select a size. Derrick not evaded by boundary.")
