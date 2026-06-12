from fractions import Fraction as Fr

atoms = [1,3,5,8,9,10,15,28,36,56,84,126]

def names(cmax):
    out = {}
    for a in range(1,cmax+1):
        for b in range(1,cmax+1):
            for d1 in atoms:
                for d2 in atoms:
                    out.setdefault(Fr(a*d1, b*d2), set()).add((d1,d2,Fr(a,b)))
    return out

strict = names(2); generous = names(4)

# TEST C spot checks
for t in (Fr(1,36), Fr(1,12), Fr(5,12), Fr(1,3), Fr(1,9), Fr(2,9)):
    print(t, "strict reps:", len(strict.get(t,())), sorted(strict.get(t,()))[:4])

# TEST D coverage
t1 = [Fr(1,m) for m in range(2,121)]
t2 = sorted({Fr(p,q) for q in range(2,37) for p in range(1,q) if Fr(p,q).denominator==q})
for nm, ex in (("strict",strict),("generous",generous)):
    print(nm, "unit:", sum(1 for t in t1 if t in ex), "/", len(t1),
          " pq36:", sum(1 for t in t2 if t in ex), "/", len(t2))

# TEST E lattice recount
INST = [Fr(1,36),Fr(1,18),Fr(1,12),Fr(1,9),Fr(1,6),Fr(1,4),Fr(5,12),Fr(1,3),Fr(2,3),Fr(1,1)]
lat = [Fr(k,36) for k in range(-23,37)]
l1 = {Fr(0)} | set(INST) | {-v for v in INST}
prods = {a*b for a in INST for b in INST}
l2 = l1 | prods | {-v for v in prods} | {1-v for v in INST} | {v-1 for v in INST}
print("lattice:", len(lat), "lvl1:", sum(v in l1 for v in lat), "lvl2:", sum(v in l2 for v in lat))
# is 2/9 level-1? (it shouldn't be, given exclusion)
print("2/9 in l1:", Fr(2,9) in l1, "; 2/9 in l2:", Fr(2,9) in l2)
# hand-check residuals: domain loads d/36, image r/12
for lbl,d,r in (("tr^T8",8,0),("A3^A3",3,3),("A3^S5",15,5),("S5^S5",10,3)):
    print(lbl, Fr(d,36)-Fr(r,12))
print("sum of residuals:", sum(Fr(d,36)-Fr(r,12) for d,r in ((8,0),(3,3),(15,5),(10,3))))

# TEST F recount
exp = set()
for a in range(1,6):
    for d in atoms: exp.add(a*d)
for d1 in atoms:
    for d2 in atoms: exp.add(d1*d2)
print("1..200:", sum(1 for n in range(1,201) if n in exp),
      " 1..100:", sum(1 for n in range(1,101) if n in exp))
print("63 expressible:", 63 in exp, "; 36,84,108,180:", [n in exp for n in (36,84,108,180)])
