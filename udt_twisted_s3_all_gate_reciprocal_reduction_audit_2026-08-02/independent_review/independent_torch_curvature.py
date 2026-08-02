import json
import torch
from fractions import Fraction

torch.set_default_dtype(torch.float64)


def q_and_dq(s):
    x, y, z = s.unbind()
    r2 = x*x + y*y + z*z
    d = 1 + r2
    q = torch.stack(((1-r2)/d, 2*x/d, 2*y/d, 2*z/d))
    # Independent closed-form Jacobian of the stereographic map.
    coords = torch.stack((x, y, z))
    dq0 = -4*coords/(d*d)
    eye = torch.eye(3, dtype=s.dtype, device=s.device)
    dqv = 2*eye/d - 4*coords[:, None]*coords[None, :]/(d*d)
    dq = torch.cat((dq0[None, :], dqv), dim=0)
    return q, dq


def metric(s, lam=0, a=1.0, profile="primary"):
    q, dq = q_and_dq(s)
    q0, q1, q2, q3 = q.unbind()
    dq0, dq1, dq2, dq3 = dq.unbind()
    sig1 = q0*dq1-q1*dq0-q2*dq3+q3*dq2
    sig2 = q0*dq2-q2*dq0-q3*dq1+q1*dq3
    sig3 = q0*dq3-q3*dq0-q1*dq2+q2*dq1
    if profile == "primary":
        u = 3+q0*q0+2*q1*q1+4*q2*q2+8*q3*q3
    elif profile == "constant":
        u = 4 + 0*s[0]
    elif profile == "repeated":
        u = 3+q0*q0+q1*q1+4*q2*q2+8*q3*q3
    else:
        raise ValueError(profile)
    zero = torch.zeros((), dtype=s.dtype, device=s.device)
    tau = torch.cat((torch.ones(1, dtype=s.dtype, device=s.device), a*sig3))
    e1 = torch.cat((zero[None], sig1))
    e2 = torch.cat((zero[None], sig2))
    e3 = torch.cat((zero[None], sig3))
    return -torch.outer(tau,tau)/u + u*torch.outer(e3,e3) + (u**lam)*(torch.outer(e1,e1)+torch.outer(e2,e2))


def gamma(s, lam=0, a=1.0, profile="primary"):
    g = metric(s, lam, a, profile)
    gi = torch.linalg.inv(g)
    dgs = torch.func.jacrev(metric)(s, lam, a, profile) # i,j, spatial-k
    dg = torch.zeros((4,4,4), dtype=s.dtype, device=s.device)
    dg = torch.cat((torch.zeros((4,4,1), dtype=s.dtype, device=s.device), dgs), dim=2)
    out=[]
    for up in range(4):
      o1=[]
      for lo1 in range(4):
        o2=[]
        for lo2 in range(4):
          total=0.0
          for k in range(4):
            total = total + gi[up,k]*(dg[k,lo2,lo1]+dg[k,lo1,lo2]-dg[lo1,lo2,k])/2
          o2.append(total)
        o1.append(torch.stack(o2))
      out.append(torch.stack(o1))
    return torch.stack(out)


def ricci(s, lam=0, a=1.0, profile="primary"):
    ga = gamma(s,lam,a,profile)
    dgas = torch.func.jacrev(gamma)(s,lam,a,profile) # up,lo1,lo2, spatial-k
    dga = torch.cat((torch.zeros((4,4,4,1),dtype=s.dtype,device=s.device),dgas),dim=3)
    out=[]
    for first in range(4):
      row=[]
      for second in range(4):
        total=0.0
        for index in range(4):
          total = total+dga[index,first,second,index]-dga[index,first,index,second]
          for other in range(4):
            total = total+ga[index,first,second]*ga[other,index,other]-ga[other,first,index]*ga[index,second,other]
        row.append(total)
      out.append(torch.stack(row))
    return torch.stack(out)


def invariants(s, lam=0, a=1.0, profile="primary"):
    mixed=torch.linalg.inv(metric(s,lam,a,profile))@ricci(s,lam,a,profile)
    return torch.stack((torch.trace(mixed),torch.trace(mixed@mixed),torch.trace(mixed@mixed@mixed)))


def run(point,lam=0,a=1.0,profile="primary"):
    s=torch.tensor(point)
    inv=invariants(s,lam,a,profile)
    jac=torch.func.jacrev(invariants)(s,lam,a,profile)
    return {"point":point,"lambda":lam,"a":a,"profile":profile,"invariants":inv.tolist(),"jacobian":jac.tolist(),"determinant":torch.linalg.det(jac).item(),"singular_values":torch.linalg.svdvals(jac).tolist()}


if __name__ == "__main__":
    cases=[
      ((1/5,1/7,1/11),0,1.0,"primary"),
      ((1/3,-1/5,1/7),0,1.0,"primary"),
      ((1/5,1/7,1/11),0,1.0,"constant"),
      ((1/5,1/7,1/11),0,0.0,"primary"),
      ((0.0,0.0,0.0),0,4.0,"primary"),
    ]
    print(json.dumps([run(*c) for c in cases],indent=2))
