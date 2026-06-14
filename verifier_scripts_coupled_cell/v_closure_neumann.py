import sympy as sp
delta,p,rc,ri = sp.symbols('delta p r_core r_int', positive=True)
# Neumann-seal rs sign:
rsN = delta*rc - rc + rc*sp.exp(-2*p)
val = rsN.subs({delta:sp.Rational(1,10),p:1,rc:sp.Rational(1,1000),ri:1})
print("rs(Neumann seal) numeric =", float(val), " sign:", "NEG" if val<0 else "POS")
# rsN = rc(delta - 1 + e^{-2p}). delta<1 and e^{-2p}<1 => delta-1+e^{-2p} could be neg.
# for delta<1: delta-1<0, +e^{-2p}<1 => sum < e^{-2p} <1 but could be pos if e^{-2p}>1-delta
print("rsN = r_core*(delta - 1 + e^{-2p}); >0 iff e^{-2p} > 1-delta, i.e. shallow core p small")
for p_ in [0.1,0.5,1,2]:
    for d_ in [0.01,0.1,0.5]:
        v=(d_-1+sp.exp(-2*p_))
        print(f"  p={p_} delta={d_}: factor={float(v):+.4f} -> rs {'POS' if v>0 else 'NEG'}")
