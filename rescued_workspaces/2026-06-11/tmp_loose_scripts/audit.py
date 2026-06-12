import math
pi = math.pi

targets = {"pion":264.14, "muon":206.768, "proton":1836.15}
# the claimed forms
claims = {"pion":(84,1,1), "muon":(20,3,3), "proton":(6,1,5)}  # (a,b,k)

def val(a,b,k): return (a/b)*pi**k

print("=== TASK 1: density of {(a/b) pi^k} near each target ===")
for name,t in targets.items():
    within05=[]; within01=[]
    for k in range(0,7):
        for a in range(1,101):
            for b in range(1,10):
                v=val(a,b,k)
                err=abs(v-t)/t
                if err<0.005:
                    within05.append((a,b,k,v,err))
                    if err<0.001:
                        within01.append((a,b,k,v,err))
    # dedupe by value (a/b can repeat e.g 2/2=1/1)
    def dedupe(L):
        seen=set(); out=[]
        for a,b,k,v,e in L:
            r=round(a/b,6)
            key=(r,k)
            if key in seen: continue
            seen.add(key); out.append((a,b,k,v,e))
        return out
    w05=dedupe(within05); w01=dedupe(within01)
    print(f"\n{name} target ratio={t}")
    print(f"  candidates within 0.5%: {len(w05)} (unique a/b,k)")
    print(f"  candidates within 0.1%: {len(w01)}")
    ca,cb,ck=claims[name]
    cv=val(ca,cb,ck); ce=abs(cv-t)/t
    print(f"  CLAIMED form {ca}/{cb}*pi^{ck} = {cv:.4f}  err={ce*100:.3f}%")
    # show a few closest
    allc=sorted(dedupe(within05),key=lambda x:x[4])[:8]
    print("  closest 8:")
    for a,b,k,v,e in allc:
        print(f"    {a}/{b}*pi^{k} = {v:.4f}  err={e*100:.3f}%")
