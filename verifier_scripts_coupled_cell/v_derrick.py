# CLAIM 5 ATTACK: Derrick scaling for radial twist Theta(r) in 3D.
# Energy functional for O(3) sigma hedgehog with radial profile Theta(r):
#   E = INT [ (xi/2)( (Theta')^2 + 2 sin^2(Theta)/r^2 ) ] * (measure) dr  (3D, *4pi r^2)
# Standard hedgehog: gradient (Theta')^2 + angular 2 sin^2 Theta /r^2.
# E[Theta] = 4pi (xi/2) INT_0^inf [ (Theta')^2 r^2 + 2 sin^2 Theta ] dr   (flat measure)
import sympy as sp
r,lam,xi = sp.symbols('r lambda xi', positive=True)
Th = sp.Function('Theta')

# --- ANALYTIC dimension count under x->lambda x i.e. Theta_lam(r)=Theta(r/lambda) ---
# Term A (gradient): INT (Theta')^2 r^2 dr.  Sub r=lambda s:
#   Theta_lam(r)=Theta(r/lam); Theta_lam'(r)=Theta'(r/lam)/lam.
#   INT (Theta'(r/lam)/lam)^2 r^2 dr ; r=lam s, dr=lam ds, r^2=lam^2 s^2:
#   = INT Theta'(s)^2/lam^2 * lam^2 s^2 * lam ds = lam * INT Theta'(s)^2 s^2 ds  => ~ lam^1
# Term B (angular): INT 2 sin^2(Theta_lam) dr = INT 2 sin^2(Theta(r/lam)) dr
#   = lam INT 2 sin^2(Theta(s)) ds  => ~ lam^1
print("ANALYTIC: gradient term ~ lambda^1 ; angular term ~ lambda^1  => E(lam)=lam*E1")
print("  dE/dlam = E1 = const > 0  (both terms positive) => NO interior stationary point.")
print("  => Derrick collapse: E monotone increasing, minimized at lam->0 (shrink). CONFIRMED.")
print()

# --- NUMERICAL with a DIFFERENT probe profile (independent of study's) ---
import torch, math
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
def energy(lam, profile):
    s = torch.linspace(1e-4, 30.0, 200000, device=dev)
    ds = s[1]-s[0]
    Th = profile(s/lam)                 # Theta(r/lam)
    Thp = torch.gradient(Th, spacing=(s,))[0]
    A = (Thp**2 * s**2)                 # gradient * r^2 measure
    B = 2*torch.sin(Th)**2              # angular
    return float(torch.trapz(A+B, s))
# probe 1 (study-like bump): Theta=pi*(r/w)*exp(1-r/w)
prof1 = lambda r: math.pi*(r/1.0)*torch.exp(1-r/1.0)
# probe 2 (DIFFERENT: arctan kink) Theta = pi*(1 - 1/(1+r^2))  -> 0..pi
prof2 = lambda r: math.pi*(1 - 1/(1+r**2))
# probe 3 (gaussian twist)
prof3 = lambda r: math.pi*torch.exp(-(r-2)**2)
for name,prof in [("study-bump",prof1),("arctan-kink",prof2),("gaussian",prof3)]:
    es=[energy(l,prof) for l in [0.5,1.0,2.0,4.0]]
    print(f" {name:12s}: E(lam=0.5,1,2,4)= {[round(e,4) for e in es]}  ratios E2/E1={es[2]/es[1]:.3f} E4/E2={es[3]/es[2]:.3f} (lam^1 => ~2.0)")
