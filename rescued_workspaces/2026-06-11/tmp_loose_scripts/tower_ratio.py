import numpy as np, torch
torch.set_default_dtype(torch.float64); dev='cuda' if torch.cuda.is_available() else 'cpu'
m=1.0; r0=1e-3; RMAX=400.0
# big box + fine near-threshold; dense E-grid near E=1 to resolve tiny binding energies
R=np.concatenate([np.geomspace(r0,1.0,4000), np.linspace(1.0,40,6000)[1:], np.linspace(40,RMAX,8000)[1:]])
def spec(kappa,NE=20000):
    E=torch.linspace(0.004,0.9998,NE).to(dev); L=abs(kappa); s=-0.5+L
    G=torch.full_like(E,r0**s); F=torch.zeros_like(E)
    def dz(r,G,F):
        ph=0.5*np.log((2.0+r)/r); pp=-1.0/(r*(2.0+r)); e1=np.exp(ph); e2=np.exp(2*ph)
        return (pp-kappa/r)*G+(E*e2+m*e1)*F,(pp+kappa/r)*F-(E*e2-m*e1)*G
    for i in range(len(R)-1):
        r=R[i];h=R[i+1]-R[i];rm=r+.5*h;rn=r+h
        a1,b1=dz(r,G,F);a2,b2=dz(rm,G+.5*h*a1,F+.5*h*b1);a3,b3=dz(rm,G+.5*h*a2,F+.5*h*b2);a4,b4=dz(rn,G+h*a3,F+h*b3)
        G=G+h/6*(a1+2*a2+2*a3+a4);F=F+h/6*(b1+2*b2+2*b3+b4)
        if i%150==0:
            n=torch.sqrt(G*G+F*F)+1e-300;G/=n;F/=n
    q=torch.sqrt(torch.clamp(torch.tensor(m*m,device=dev)-E*E,min=1e-12))
    res=((G+(E+m)/q*F)/(torch.sqrt(G*G+F*F)+1e-300)).cpu().numpy();Ev=E.cpu().numpy();out=[]
    for i in range(NE-1):
        a,b=res[i],res[i+1]
        if np.isfinite(a) and np.isfinite(b) and a*b<0: out.append(Ev[i]+(Ev[i+1]-Ev[i])*a/(a-b))
    return out
print("chasing the binding-energy tower ratio (big box rmax=400); is there a universal asymptote?")
print(f"  candidates: 2/3=0.6667  1/phi=0.6180  1-1/e=0.6321  3/5=0.6  e^-1/2=0.6065")
for k in [-1,-2]:
    S=spec(k); B=[1-e for e in S]
    rat=[B[i+1]/B[i] for i in range(len(B)-1)]
    print(f"\n k={k}: {len(S)} levels")
    print("   E_n   :", ", ".join(f"{e:.6f}" for e in S[:14]))
    print("   B_n   :", ", ".join(f"{b:.5f}" for b in B[:14]))
    print("   B+1/B :", ", ".join(f"{r:.4f}" for r in rat[:13]))
    # also test Rydberg: B_n ~ 1/(n+d)^2 -> 1/sqrt(B) linear in n
    inv=[1/np.sqrt(b) for b in B if b>1e-7]
    dd=np.diff(inv)
    print("   d(1/sqrtB) (const=>Rydberg):", ", ".join(f"{x:.3f}" for x in dd[:12]))
