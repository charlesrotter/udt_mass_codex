import numpy as np, torch
torch.set_default_dtype(torch.float64); dev='cuda' if torch.cuda.is_available() else 'cpu'
m=1.0; r0=1e-3
R=np.concatenate([np.geomspace(r0,1.0,4000), np.linspace(1.0,40.0,4000)[1:]])
def spec(kappa,NE=5000):
    E=torch.linspace(0.004,0.997,NE).to(dev); L=abs(kappa); s=-0.5+L
    G=torch.full_like(E,r0**s); F=torch.zeros_like(E)
    def dz(r,G,F):
        ph=0.5*np.log((2.0+r)/r); pp=-1.0/(r*(2.0+r)); e1=np.exp(ph); e2=np.exp(2*ph)
        return (pp-kappa/r)*G+(E*e2+m*e1)*F,(pp+kappa/r)*F-(E*e2-m*e1)*G
    for i in range(len(R)-1):
        r=R[i];h=R[i+1]-R[i];rm=r+.5*h;rn=r+h
        a1,b1=dz(r,G,F);a2,b2=dz(rm,G+.5*h*a1,F+.5*h*b1);a3,b3=dz(rm,G+.5*h*a2,F+.5*h*b2);a4,b4=dz(rn,G+h*a3,F+h*b3)
        G=G+h/6*(a1+2*a2+2*a3+a4);F=F+h/6*(b1+2*b2+2*b3+b4)
        if i%200==0:
            n=torch.sqrt(G*G+F*F)+1e-300;G/=n;F/=n
    q=torch.sqrt(torch.clamp(torch.tensor(m*m,device=dev)-E*E,min=1e-12))
    res=((G+(E+m)/q*F)/(torch.sqrt(G*G+F*F)+1e-300)).cpu().numpy();Ev=E.cpu().numpy();out=[]
    for i in range(NE-1):
        a,b=res[i],res[i+1]
        if np.isfinite(a) and np.isfinite(b) and a*b<0: out.append(Ev[i]+(Ev[i+1]-Ev[i])*a/(a-b))
    return out
S={k:spec(k) for k in [-1,-2,-3]}
print("=== eigenvalue towers (dimensionless) ===")
for k in [-1,-2,-3]: print(f" k={k}: "+", ".join(f"{x:.5f}" for x in S[k][:6]))
def koide(ms): ms=np.array(ms); return ms.sum()/np.sqrt(ms).sum()**2
print("\n=== tower law: binding B_n=1-E_n, ratios B_{n+1}/B_n, and 1/sqrt(B_n) linearity (Rydberg=linear in n) ===")
for k in [-1,-2,-3]:
    B=[1-e for e in S[k][:6]]; rat=[B[i+1]/B[i] for i in range(len(B)-1)]
    invsq=[1/np.sqrt(b) for b in B]; dd=np.diff(invsq)
    print(f" k={k}: B={[round(b,4) for b in B]}")
    print(f"        B_{{n+1}}/B_n={[round(r,3) for r in rat]} ; d(1/sqrtB)={[round(x,3) for x in dd]} (const=Rydberg)")
print("\n=== ALL pairwise ratios E_a/E_b > 1, flag near simple rationals / constants ===")
allE=sorted([(e,k,n) for k in S for n,e in enumerate(S[k][:6])])
specials={'1/2':.5,'2/3':.6667,'3/4':.75,'3/5':.6,'4/5':.8,'5/6':.8333,'phi-1':.618,'1/sqrt2':.7071,'1/sqrt3':.5774,'pi/4':.7854,'e/pi':.8653}
hits=[]
for i in range(len(allE)):
    for j in range(i+1,len(allE)):
        r=allE[i][0]/allE[j][0]
        for nm,v in specials.items():
            if abs(r-v)<0.004: hits.append((round(r,4),nm,allE[i][1:],allE[j][1:]))
print(f" {len(hits)} ratio(s) within 0.4% of a flagged special value:")
for h in hits[:20]: print("   ",h)
print("\n=== Koide Q of MANY triplets (flag near 2/3=0.6667, or other special) ===")
import itertools
trips=[]
# one-per-channel (all n combos), and within-channel triplets
for n1 in range(4):
  for n2 in range(4):
    for n3 in range(4):
      if -1 in S and -2 in S and -3 in S and n1<len(S[-1]) and n2<len(S[-2]) and n3<len(S[-3]):
        Q=koide([S[-1][n1],S[-2][n2],S[-3][n3]]); trips.append((Q,('cross',n1,n2,n3)))
for k in S:
  for c in itertools.combinations(range(min(6,len(S[k]))),3):
    Q=koide([S[k][i] for i in c]); trips.append((Q,(k,)+c))
near=sorted([t for t in trips if abs(t[0]-2/3)<0.02], key=lambda t:abs(t[0]-2/3))
print(f" {len(trips)} triplets; {len(near)} within 0.02 of 2/3:")
for t in near[:12]: print(f"   Q={t[0]:.4f}  {t[1]}")
print(f" Koide range over all triplets: [{min(t[0] for t in trips):.4f}, {max(t[0] for t in trips):.4f}]")
print("\n=== BEATS: nearest-neighbor gaps in the full sorted spectrum ===")
Es=sorted(e for k in S for e in S[k][:6]); gaps=np.diff(Es)
print(" sorted:",[round(e,4) for e in Es])
print(" gaps  :",[round(g,4) for g in gaps])
print(" gap ratios:",[round(gaps[i+1]/gaps[i],3) for i in range(len(gaps)-1)])
