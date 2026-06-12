import math, fractions
pi = math.pi
me = 0.51099895

# ---- TASK 1: arithmetic verification ----
print("="*70)
print("TASK 1: ARITHMETIC vs PDG")
print("="*70)
pdg = {'u':2.16,'d':4.67,'s':93.4,'c':1270,'b':4180,'t':172690}
# base
m_u = 4*me; m_d = 9*me
print(f"m_u = 4 m_e        = {m_u:.4f}  PDG {pdg['u']}  err {(m_u/pdg['u']-1)*100:+.1f}%  (pi-FREE)")
print(f"m_d = 9 m_e        = {m_d:.4f}  PDG {pdg['d']}  err {(m_d/pdg['d']-1)*100:+.1f}%  (pi-FREE)")
# generation
m_s = m_d*2*pi**2
m_c = m_u*6*pi**4
m_b = m_s*9*pi**2/2
m_t = m_c*14*pi**2
for nm,v in [('s',m_s),('c',m_c),('b',m_b),('t',m_t)]:
    print(f"m_{nm} = {v:.1f}  PDG {pdg[nm]}  err {(v/pdg[nm]-1)*100:+.1f}%")

# ratio checks
print("\nRatios (claimed sub-2%):")
for lab,formula,val in [("m_s/m_d","2pi^2",2*pi**2),("m_c/m_u","6pi^4",6*pi**4),
                        ("m_b/m_s","9pi^2/2",9*pi**2/2),("m_t/m_c","14pi^2",14*pi**2)]:
    print(f"  {lab} = {formula} = {val:.2f}")
print(f"  PDG m_s/m_d={pdg['s']/pdg['d']:.2f}  m_c/m_u={pdg['c']/pdg['u']:.2f}  m_b/m_s={pdg['b']/pdg['s']:.2f}  m_t/m_c={pdg['t']/pdg['c']:.2f}")

# ---- TASK 2: NULL TEST ----
print()
print("="*70)
print("TASK 2: NULL TEST  family {(a/b) pi^k : a 1..200, b 1..12, k 0..6}")
print("="*70)
targets = {'u':pdg['u']/me,'d':pdg['d']/me,'s':pdg['s']/me,'c':pdg['c']/me,
           'b':pdg['b']/me,'t':pdg['t']/me}
print(f"{'q':>2} {'ratio':>10} {'#<=6%':>8} {'#<=2%':>8} {'#<=1%':>8}  density per 1% near target")
for q,tg in targets.items():
    c6=c2=c1=0
    for a in range(1,201):
        for b in range(1,13):
            for k in range(0,7):
                cand=(a/b)*pi**k
                e=abs(cand/tg-1)
                if e<=0.06: c6+=1
                if e<=0.02: c2+=1
                if e<=0.01: c1+=1
    print(f"{q:>2} {tg:>10.1f} {c6:>8} {c2:>8} {c1:>8}")

# total family size & unique values for context
print()
vals=set()
for a in range(1,201):
    for b in range(1,13):
        for k in range(0,7):
            vals.add(round((a/b)*pi**k,9))
print(f"Family total enumerations = {200*12*7}, unique values = {len(vals)}")

# ---- TASK 4: are the sector-factor decompositions forced? ----
print()
print("="*70)
print("TASK 4: sector factors back-solved from measured ratios")
print("="*70)
# Each ratio = 2pi^2 * SF.  Solve SF from PDG ratio and from claimed value.
for lab,claimed_SF,claimed_val,pdgratio in [
    ("s/d  (down 1->2)", 1,        2*pi**2,      pdg['s']/pdg['d']),
    ("c/u  (up 1->2)",   3*pi**2,  6*pi**4,      pdg['c']/pdg['u']),
    ("b/s  (down 2->3)", 9/4,      9*pi**2/2,    pdg['b']/pdg['s']),
    ("t/c  (up 2->3)",   7,        14*pi**2,     pdg['t']/pdg['c']),
]:
    sf_from_pdg = pdgratio/(2*pi**2)
    print(f"{lab}: claimed SF={claimed_SF:.4f}  SF implied by PDG ratio={sf_from_pdg:.4f}")
