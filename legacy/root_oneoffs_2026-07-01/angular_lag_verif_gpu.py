import torch, math
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
N=4096
g=torch.Generator(device=dev).manual_seed(7)
r=torch.rand(N,device=dev,generator=g)*5+0.1
th=torch.rand(N,device=dev,generator=g)*math.pi*0.98+0.01
ph=torch.rand(N,device=dev,generator=g)*2*math.pi
phir=torch.rand(N,device=dev,generator=g)*2-1   # arbitrary phi(r)
xi=1.0
# hedgehog n=(sin th cos ph, sin th sin ph, cos th); d_t=d_r=0
# X = g^{th th}|d_th n|^2 + g^{ph ph}|d_ph n|^2
# d_th n = (cos th cos ph, cos th sin ph, -sin th): |.|^2 = 1
# d_ph n = (-sin th sin ph, sin th cos ph, 0): |.|^2 = sin^2 th
# g^{thth}=1/r^2, g^{phph}=1/(r^2 sin^2 th)
X = (1.0)/r**2 + (th.sin()**2)/(r**2*th.sin()**2)   # = 2/r^2
# T_{mn}=xi dn_m.dn_n + g_{mn}L, L=-xi/2 X
# mixed: T^t_t = g^{tt}T_tt. dn_t=0 => T_tt=g_tt L => T^t_t=L = -xi/2 X = -xi/r^2
# T^r_r: dn_r=0 => T^r_r = L = -xi/r^2.  T^th_th: g^{thth}(xi*1 + g_thth L)= xi/r^2 + L
L = -0.5*xi*X
Ttt = L
Trr = L
Tthth = (1.0/r**2)*(xi*1.0) + L  # g^{thth}*xi*|d_th n|^2 + L
rho=-Ttt; pr=Trr
print("max|p_r+rho| =", (pr+rho).abs().max().item())
print("max|T^th_th| =", Tthth.abs().max().item())
print("max|rho-xi/r^2| =", (rho-xi/r**2).abs().max().item())
print("phi-independence: T^t_t has no phir dependence by construction (analytic)")
