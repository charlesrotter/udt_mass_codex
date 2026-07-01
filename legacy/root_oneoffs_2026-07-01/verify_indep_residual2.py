#!/usr/bin/env python3
"""
INDEPENDENT verifier part 3b: localize the (r,r) residual; separate genuine body
inconsistency from core/edge FD-spike artifact; clean (t,t) check via Misner-Sharp.
Driver: Claude blind verifier. 2026-06-15. DATA-BLIND.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, numpy as np, torch
import complete_metric_batched as cm
torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"

# closed-form G (from part 3, hardcoded -- verified there):
#  G^t_t = G^r_r = (-2 phip r - e^{2phi} + 1) e^{-2phi}/r^2
def Gtt_rr(rr, phi, phip):
    return (-2*phip*rr - np.exp(2*phi) + 1)*np.exp(-2*phi)/rr**2

mat_xi = mat_kap = 1.0
rc = 0.05; SPAN = 14.0; ri = rc + SPAN
P, K8, N = 0.4, 0.05, 1400

rg = torch.linspace(rc, ri, N, device=DEV).unsqueeze(0)
o = cm.selfconsistent_batched(rg, mat_xi, mat_kap, p=P, kap8=K8, iters=160, relax=0.4, tol=1e-11)
rr = o['r'][0].cpu().numpy(); Th = o['Th'][0].cpu().numpy(); phi = o['phi'][0].cpu().numpy()
# use the ENGINE's own profile derivatives where available (Thp committed), my own phi deriv
Thp = o['Thp'][0].cpu().numpy()
phip = np.gradient(phi, rr)

# stress (mixed): T^t_t=-rho, T^r_r=p_r
X = np.exp(-2*phi)*Thp**2; Y = np.sin(Th)**2/rr**2
rho = (mat_xi/2)*(X+2*Y)+(mat_kap/2)*(2*X*Y+Y**2)
pr  = (mat_xi/2)*(X-2*Y)+(mat_kap/2)*(2*X*Y-Y**2)

G = Gtt_rr(rr, phi, phip)
res_tt = G - K8*(-rho)
res_rr = G - K8*(pr)

# locate where Theta winds (body) vs unwound (exterior)
body = np.abs(Thp) > 1e-2*np.max(np.abs(Thp))
print("="*78); print("LOCALIZE the (r,r) residual on the #52 soliton (N=%d)"%N); print("="*78)
print(f"  Theta range: {Th.min():.3f}..{Th.max():.3f};  Thp peak at r={rr[np.argmax(np.abs(Thp))]:.3f}")
print(f"  body extent (|Thp|>1%% peak): r in [{rr[body].min():.3f}, {rr[body].max():.3f}]")

# strip the 3 deepest-core points and 3 outer edge points (FD-spike zone)
core_zone = rr < rr[0] + 0.5     # near the deep clamped core
edge = (np.arange(N) < 5) | (np.arange(N) > N-6)
clean = (~edge)
print("\n  WHERE is the max (r,r) residual?")
i_rr = np.argmax(np.abs(res_rr[clean]))
ri_rr = rr[clean][i_rr]
print(f"    overall max|res_rr|={np.max(np.abs(res_rr[clean])):.3e} at r={ri_rr:.4f}  "
      f"(core_zone? {ri_rr < rr[0]+0.5})")

# residual EXCLUDING the deep-core spike (r > rc+1.0): the genuine smooth body
smooth = (rr > rc + 1.0) & (~edge)
sb = smooth & body
se = smooth & (~body)
print("\n  EXCLUDING deep-core (r>rc+1.0), the smooth region:")
print(f"    BODY (Thp winds):     max|res_rr|={np.max(np.abs(res_rr[sb])):.3e}  mean={np.mean(np.abs(res_rr[sb])):.3e}")
print(f"    EXTERIOR(Thp unwound):max|res_rr|={np.max(np.abs(res_rr[se])):.3e}  mean={np.mean(np.abs(res_rr[se])):.3e}")
print(f"    BODY (t,t):           max|res_tt|={np.max(np.abs(res_tt[sb])):.3e}")
print(f"    EXTERIOR (t,t):       max|res_tt|={np.max(np.abs(res_tt[se])):.3e}")

# the predicted (r,r) residual IF the only cause is EOS-softening:
# G^r_r = G^t_t = k8 T^t_t (where (t,t) holds) = -k8 rho.  Then res_rr = G-k8 pr
#  = -k8 rho - k8 pr = -k8 (rho+pr).  So PREDICTED res_rr = -k8*(p_r+rho).
pred_res_rr = -K8*(pr + rho)
print("\n  TEST the root cause: is res_rr == -k8 (p_r+rho)  [i.e. purely EOS-softening]?")
print(f"    max|res_rr - (-k8(p_r+rho))| over smooth body = "
      f"{np.max(np.abs(res_rr[sb] - pred_res_rr[sb])):.3e}")
print(f"    typical |k8(p_r+rho)| in body = {np.median(np.abs(K8*(pr+rho)[sb])):.3e}")
print("    -> if these match, the (r,r) violation IS exactly the p_r+rho softening,")
print("       NOT an FD/engine artifact.  (residual=k8*EOS-gap, analytic.)")

# convergence of the EOS-prediction match and of the smooth-body residual
print("\n  CONVERGENCE (smooth body, r>rc+1.0), excluding core/edge spikes:")
for Nx in [700, 1400, 2800]:
    rgx = torch.linspace(rc, ri, Nx, device=DEV).unsqueeze(0)
    ox = cm.selfconsistent_batched(rgx, mat_xi, mat_kap, p=P, kap8=K8, iters=160, relax=0.4, tol=1e-11)
    rx = ox['r'][0].cpu().numpy(); Tx = ox['Th'][0].cpu().numpy(); px = ox['phi'][0].cpu().numpy()
    Tpx = ox['Thp'][0].cpu().numpy(); ppx = np.gradient(px, rx)
    Xx = np.exp(-2*px)*Tpx**2; Yx = np.sin(Tx)**2/rx**2
    rhox = (mat_xi/2)*(Xx+2*Yx)+(mat_kap/2)*(2*Xx*Yx+Yx**2)
    prx = (mat_xi/2)*(Xx-2*Yx)+(mat_kap/2)*(2*Xx*Yx-Yx**2)
    Gx = Gtt_rr(rx, px, ppx)
    rrr = Gx - K8*prx
    bx = (np.abs(Tpx) > 1e-2*np.max(np.abs(Tpx))) & (rx > rc+1.0) & (np.arange(Nx)>5) & (np.arange(Nx)<Nx-6)
    eos_x = -K8*(prx+rhox)
    print(f"    N={Nx:5d}: smooth-body mean|res_rr|={np.mean(np.abs(rrr[bx])):.4e}  "
          f"max|res_rr - k8*EOS|={np.max(np.abs(rrr[bx]-eos_x[bx])):.3e}")
