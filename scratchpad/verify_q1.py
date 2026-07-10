"""Q1: is seal machinery byte-identical to base mirror when seal None/{}/explicit-mirror?"""
import torch, cell_solver_f2d as M
torch.set_default_dtype(torch.float64)
torch.manual_seed(1)

Nr, Nth = 16, 8
prm = (8.0, 1.0, 1.0, 1)
ctx = M.make_ctx(Nr, Nth, rc=0.5, device="cpu")

# non-trivial seed: base seed + random perturbation so BCs are NOT satisfied (stress the compare)
u = M.seed(ctx)
u = u + 0.05 * torch.randn_like(u)

F_none = M.residual(u, ctx, prm, seal=None)
F_empty = M.residual(u, ctx, prm, seal={})
F_mir = M.residual(u, ctx, prm, seal=dict(phi="mirror", matter="mirror"))

print("len F_none  =", F_none.numel())
print("len F_empty =", F_empty.numel())
print("len F_mir   =", F_mir.numel())
print("max|F_none - F_empty| =", float((F_none - F_empty).abs().max()))
print("max|F_none - F_mir  | =", float((F_none - F_mir).abs().max()))
print("bytewise none==empty  :", bool(torch.equal(F_none, F_empty)))
print("bytewise none==mirror :", bool(torch.equal(F_none, F_mir)))

# also test with a SECOND independent random seed at alpha!=0 (source-on path)
u2 = M.seed(ctx) + 0.1 * torch.randn_like(u)
prm2 = (8.0, 1.0, 1.0, 1, -1.0, -0.5)
Fa = M.residual(u2, ctx, prm2, seal=None)
Fb = M.residual(u2, ctx, prm2, seal=dict(phi="mirror", matter="mirror"))
print("alpha=-1 bytewise none==mirror:", bool(torch.equal(Fa, Fb)), "max diff",
      float((Fa - Fb).abs().max()))
