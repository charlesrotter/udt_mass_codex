import math
pi=math.pi; me=0.51099895
pdg={'u':2.16,'d':4.67,'s':93.4,'c':1270,'b':4180,'t':172690}
targets={q:pdg[q]/me for q in pdg}

print("NULL TEST v2 -- top range extended so top is reachable (a 1..300, b 1..12, k 0..7)")
print(f"{'q':>2} {'ratio':>10} {'#<=6%':>8} {'#<=2%':>8} {'#<=1%':>8}")
for q,tg in targets.items():
    c6=c2=c1=0
    for a in range(1,301):
        for b in range(1,13):
            for k in range(0,8):
                e=abs((a/b)*pi**k/tg-1)
                if e<=0.06:c6+=1
                if e<=0.02:c2+=1
                if e<=0.01:c1+=1
    print(f"{q:>2} {tg:>10.1f} {c6:>8} {c2:>8} {c1:>8}")

print("\nBASE-MASS-SPECIFIC NULL TEST -- pi-FREE integers only {n*m_e, n 1..50} vs u,d ratios")
for q in ['u','d']:
    tg=targets[q]
    hits6=[n for n in range(1,51) if abs(n/tg-1)<=0.06]
    hits2=[n for n in range(1,51) if abs(n/tg-1)<=0.02]
    nearest=min(range(1,51),key=lambda n:abs(n/tg-1))
    print(f"  {q}: ratio={tg:.3f}  integers within 6%={hits6}  within 2%={hits2}  nearest int={nearest} (err {(nearest/tg-1)*100:+.1f}%)")

print("\nHow many quarks does the SIMPLE integer ladder {1..50}*m_e hit within 6%?")
for q,tg in targets.items():
    hits=[n for n in range(1,200000) if n<=400 and abs(n/tg-1)<=0.06]
    print(f"  {q}: ratio={tg:.1f} -> integers within 6%: {hits if hits else 'none in 1..400'}")

# u,d uncertainty: PDG u=2.16+0.49-0.26, d=4.67+0.48-0.17 -> is 4m_e/9m_e inside?
print("\nu,d within PDG uncertainty?")
print(f"  4 m_e = {4*me:.3f}; PDG u = 2.16 (+0.49 -0.26) -> range [1.90, 2.65]  -> 2.044 INSIDE: {1.90<=4*me<=2.65}")
print(f"  9 m_e = {9*me:.3f}; PDG d = 4.67 (+0.48 -0.17) -> range [4.50, 5.15]  -> 4.599 INSIDE: {4.50<=9*me<=5.15}")
