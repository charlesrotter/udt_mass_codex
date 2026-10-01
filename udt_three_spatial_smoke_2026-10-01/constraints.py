"""Original 3+1 vacuum constraints, evaluated from the metric and its velocity."""
import torch

def original_constraints(engine,g,v):
    gamma=g[...,1:,1:];inverse=torch.linalg.inv(gamma)
    dgamma=torch.stack(engine.gradients(gamma),dim=-3)
    lower=(dgamma.transpose(-3,-2)+dgamma.movedim(-3,-1)-dgamma)/2
    conn=torch.einsum('...ad,...dbc->...abc',inverse,lower)
    dc=torch.stack(engine.gradients(conn),dim=-4)
    ricci=torch.einsum('...kkij->...ij',dc)-torch.einsum('...jkik->...ij',dc)
    ricci+=torch.einsum('...kkl,...lij->...ij',conn,conn)-torch.einsum('...kil,...lkj->...ij',conn,conn)
    beta=g[...,0,1:]
    lapse2=-g[...,0,0]+torch.einsum('...i,...ij,...j->...',beta,inverse,beta)
    dbeta=torch.stack(engine.gradients(beta),dim=-2)
    extrinsic=(-v[...,1:,1:]+dbeta+dbeta.transpose(-2,-1)-2*torch.einsum('...kij,...k->...ij',conn,beta))/(2*torch.sqrt(lapse2)[...,None,None])
    mixed=torch.einsum('...jk,...ki->...ji',inverse,extrinsic)
    trace=torch.einsum('...ii->...',mixed)
    hamiltonian=torch.einsum('...ij,...ij->...',inverse,ricci)+trace**2-torch.einsum('...ij,...ji->...',mixed,mixed)
    dmixed=torch.stack(engine.gradients(mixed),dim=-3)
    momentum=torch.einsum('...jji->...i',dmixed)
    momentum+=torch.einsum('...jjk,...ki->...i',conn,mixed)-torch.einsum('...kji,...jk->...i',conn,mixed)
    momentum-=torch.stack(engine.gradients(trace),dim=-1)
    return hamiltonian,momentum,lapse2
