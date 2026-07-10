"""VERIFIER-2 TASK 1: is the alpha-source a DEAD knob (false null)?
Test at FINITE I_r (NOT the drained endpoint). Compute residual with prm alpha=0
vs alpha=-1 vs alpha=-2 (ASRC_C=-0.5) at a FIXED field. Does the phi-row block change?
"""
import torch, math
import cell_solver_f2d as M
torch.set_default_dtype(torch.float64)

Nr, Nth = 16, 8
ctx = M.make_ctx(Nr, Nth, rc=0.5, device="cpu")
Z, XI, KAP, N = 8.0, 1.0, 1.0, 1
ASRC = -0.5

def prm(alpha):
    return (Z, XI, KAP, N) if alpha == 0.0 else (Z, XI, KAP, N, alpha, ASRC)

# ---- build a NON-drained field with finite I_r: seed with moderate amplitude ----
for amp in [0.02, 0.2, 0.5]:
    u = M.seed(ctx, amp=amp)
    Ir = M.fields(u, ctx, prm(0.0))["Ir"]
    print(f"amp={amp}: I_r mean={float(Ir.mean()):.4e} max={float(Ir.max()):.4e}")

amp = 0.2
u = M.seed(ctx, amp=amp)
Q0 = M.fields(u, ctx, prm(0.0))
Ir = Q0["Ir"]; phi = Q0["phi"]
print(f"\nUsing amp={amp}: I_r mean={float(Ir.mean()):.4e}  phi range=[{float(phi.min()):.4f},{float(phi.max()):.4f}]")

# residual at the SAME field u for each alpha
r0  = M.residual(u, ctx, prm(0.0))
rm1 = M.residual(u, ctx, prm(-1.0))
rm2 = M.residual(u, ctx, prm(-2.0))

print(f"\nlen(F)={r0.numel()}  (should be identical shape across alpha)")
print(f"max|F(a=-1) - F(a=0)| overall = {float((rm1-r0).abs().max()):.4e}")
print(f"max|F(a=-2) - F(a=0)| overall = {float((rm2-r0).abs().max()):.4e}")

# The phi-ODE interior rows are rows[0] = Q['phi_ode'][1:-1] => indices 0..Nr-3
nphi = Nr - 2
dphi_m1 = (rm1[:nphi] - r0[:nphi])
dphi_m2 = (rm2[:nphi] - r0[:nphi])
print(f"\nphi-interior block (first {nphi} residual rows):")
print(f"  max|Delta phi-row (a=-1)| = {float(dphi_m1.abs().max()):.6e}")
print(f"  max|Delta phi-row (a=-2)| = {float(dphi_m2.abs().max()):.6e}")

# --- hand check of the term magnitude at one interior node ---
# added term in phi_ode:  phi_ode -= ASRC_C*ALPHA*XI*exp(ALPHA*phi)*Ir/Z
# residual phi-interior row i corresponds to phi_ode index i+1 (since [1:-1])
alpha = -1.0
term = ASRC * alpha * XI * torch.exp(alpha * phi) * Ir / Z   # this is SUBTRACTED from phi_ode
# residual(a) - residual(0) on phi_ode rows = -(term)  [since phi_ode = base - term]
predicted = -term[1:-1]
print(f"\nHAND CHECK (alpha=-1) at interior nodes:")
print(f"  ASRC_C*ALPHA*XI*e^(ALPHA*phi)*Ir/Z at node1 = {float(term[1]):.6e}")
print(f"  predicted Delta-residual (= -term)  node1  = {float(predicted[0]):.6e}")
print(f"  actual    Delta-residual            node1  = {float(dphi_m1[0]):.6e}")
print(f"  max|predicted - actual| over phi-interior  = {float((predicted - dphi_m1).abs().max()):.3e}")

# proportionality check: does Delta scale with exp(alpha*phi)*Ir between a=-1 and a=-2?
term2 = ASRC * (-2.0) * XI * torch.exp(-2.0 * phi) * Ir / Z
predicted2 = -term2[1:-1]
print(f"\nHAND CHECK (alpha=-2): max|predicted-actual| over phi-interior = "
      f"{float((predicted2 - dphi_m2).abs().max()):.3e}")

print("\nVERDICT-DATA: alpha-source term is", "LIVE (residual changes proportionally)"
      if float(dphi_m1.abs().max()) > 1e-12 else "DEAD (no change at finite I_r)")
