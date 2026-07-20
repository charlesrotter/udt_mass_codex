#!/usr/bin/env python3
"""Direct all-component coordinate Bach tensor for the conditional metric.

The implementation is functional and uses scalar forward automatic differentiation through four
eta derivatives.  It does not infer the Bach gate from the reduced Galerkin gradient.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import torch
from torch.func import jacfwd
ROOT=Path(__file__).resolve().parents[1];PARENT=ROOT/"c2_nonlinear_stationary_solution_space_2026-07-20";sys.path.insert(0,str(PARENT))
from stationary_c2_engine import DTYPE,DIMENSION,ETA_INDEX,fields_from_coefficients

def metric_point(eta:torch.Tensor,coeff:torch.Tensor,layout)->torch.Tensor:
 lapse,radial,fiber,shift=fields_from_coefficients(eta,coeff,layout);z=eta*0;q=torch.sin(eta)*torch.cos(eta);c2=torch.cos(eta)**2;s2=torch.sin(eta)**2
 coframe=torch.stack((torch.stack((lapse,z,z,z)),torch.stack((z,radial,z,z)),torch.stack((z,z,q,-q)),torch.stack((fiber*shift,z,fiber*c2,fiber*s2))))
 signature=torch.diag(torch.tensor([-1.,1.,1.,1.],dtype=DTYPE));return coframe.T@signature@coframe

def connection_point(eta,coeff,layout):
 g=metric_point(eta,coeff,layout);dg=jacfwd(metric_point,argnums=0)(eta,coeff,layout);inv=torch.linalg.inv(g);z=eta*0
 return torch.stack([torch.stack([torch.stack([sum(inv[a,e]*((dg[e,c] if b==ETA_INDEX else z)+(dg[e,b] if c==ETA_INDEX else z)-(dg[b,c] if e==ETA_INDEX else z)) for e in range(DIMENSION))/2 for c in range(DIMENSION)]) for b in range(DIMENSION)]) for a in range(DIMENSION)])

def curvature_point(eta,coeff,layout):
 g=metric_point(eta,coeff,layout);inv=torch.linalg.inv(g);gamma=connection_point(eta,coeff,layout);dgamma=jacfwd(connection_point,argnums=0)(eta,coeff,layout);z=eta*0
 rup=torch.stack([torch.stack([torch.stack([torch.stack([(dgamma[a,b,d] if c==ETA_INDEX else z)-(dgamma[a,b,c] if d==ETA_INDEX else z)+sum(gamma[a,e,c]*gamma[e,b,d]-gamma[a,e,d]*gamma[e,b,c] for e in range(DIMENSION)) for d in range(DIMENSION)]) for c in range(DIMENSION)]) for b in range(DIMENSION)]) for a in range(DIMENSION)])
 ricci=torch.stack([torch.stack([sum(rup[a,b,a,d] for a in range(DIMENSION)) for d in range(DIMENSION)]) for b in range(DIMENSION)]);scalar=torch.einsum("ab,ab->",inv,ricci);rlow=torch.einsum("ae,ebcd->abcd",g,rup)
 weyl=torch.stack([torch.stack([torch.stack([torch.stack([rlow[a,b,c,d]-(g[a,c]*ricci[b,d]-g[a,d]*ricci[b,c]-g[b,c]*ricci[a,d]+g[b,d]*ricci[a,c])/2+scalar*(g[a,c]*g[b,d]-g[a,d]*g[b,c])/6 for d in range(DIMENSION)]) for c in range(DIMENSION)]) for b in range(DIMENSION)]) for a in range(DIMENSION)])
 return g,inv,gamma,ricci,weyl

def weyl_point(eta,coeff,layout):return curvature_point(eta,coeff,layout)[4]

def divergence_point(eta,coeff,layout):
 _,inv,gamma,_,weyl=curvature_point(eta,coeff,layout);dweyl=jacfwd(weyl_point,argnums=0)(eta,coeff,layout);z=eta*0
 return torch.stack([torch.stack([torch.stack([sum(inv[d,e]*((dweyl[a,c,b,d] if e==ETA_INDEX else z)-sum(gamma[p,e,a]*weyl[p,c,b,d]+gamma[p,e,c]*weyl[a,p,b,d]+gamma[p,e,b]*weyl[a,c,p,d]+gamma[p,e,d]*weyl[a,c,b,p] for p in range(DIMENSION))) for d in range(DIMENSION) for e in range(DIMENSION)) for b in range(DIMENSION)]) for c in range(DIMENSION)]) for a in range(DIMENSION)])

def bach_point(eta,coeff,layout):
 _,inv,gamma,ricci,weyl=curvature_point(eta,coeff,layout);div=divergence_point(eta,coeff,layout);ddiv=jacfwd(divergence_point,argnums=0)(eta,coeff,layout);ricci_up=torch.einsum("ac,bd,cd->ab",inv,inv,ricci);z=eta*0
 return torch.stack([torch.stack([sum(inv[c,f]*((ddiv[a,c,b] if f==ETA_INDEX else z)-sum(gamma[p,f,a]*div[p,c,b]+gamma[p,f,c]*div[a,p,b]+gamma[p,f,b]*div[a,c,p] for p in range(DIMENSION))) for c in range(DIMENSION) for f in range(DIMENSION))+sum(.5*ricci_up[c,d]*weyl[a,c,b,d] for c in range(DIMENSION) for d in range(DIMENSION)) for b in range(DIMENSION)]) for a in range(DIMENSION)])

def bach_tensor_profile(values:np.ndarray,layout,nodes:int)->dict[str,object]:
 # The toric chart degenerates at the primitive caps.  The registered physical boundary is open,
 # so the direct bulk-component gate uses a fixed interior buffer rather than mistaking float64
 # cancellation in a singular coordinate basis for a Bach residual.
 buffer=.02;roots,_=np.polynomial.legendre.leggauss(nodes);etas=buffer+(roots+1)*(np.pi/2-2*buffer)/2;coeff=torch.tensor(values,dtype=DTYPE);items=[];inverses=[]
 for value in etas:
  eta=torch.tensor(value,dtype=DTYPE);items.append(bach_point(eta,coeff,layout).detach().numpy());inverses.append(torch.linalg.inv(metric_point(eta,coeff,layout)).detach().numpy())
 bach=np.asarray(items);inv=np.asarray(inverses);antisym=bach-np.swapaxes(bach,1,2);trace=np.einsum("...ab,...ab->...",inv,bach)
 return {"nodes":nodes,"eta_interval":[buffer,float(np.pi/2-buffer)],"boundary_status":"OPEN_NOT_TESTED","derivative_method":"scalar forward automatic differentiation through the direct coordinate Weyl divergence","raw_component_inf":float(np.max(np.abs(bach))),"symmetry_error_inf":float(np.max(np.abs(antisym))),"trace_error_inf":float(np.max(np.abs(trace))),"bach":bach.tolist()}
