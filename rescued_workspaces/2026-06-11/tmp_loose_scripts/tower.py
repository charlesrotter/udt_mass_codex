# all-orders reachability of the corrected off-diagonal Dirac spin-2 vertex, from kappa=-1
import importlib.util, sys
spec=importlib.util.spec_from_file_location("d","/home/udt-admin/UDT_m_e/da_discharge_i_dirac.py")
import io,contextlib
m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):   # suppress its prints
    spec.loader.exec_module(m)
h=m.h_tensor("m0")
KS=list(range(-7,8)); KS.remove(0)
def step(frontier):
    nxt=set()
    for k in frontier:
        for kp in KS:
            t1,t2=m.dirac_channel(kp,k,h)
            if abs(t1)>1e-12 or abs(t2)>1e-12: nxt.add(kp)
    return nxt
reach={-1}; order=0; hist=[set(reach)]
while order<8:
    new=step(reach); order+=1
    grown=reach|new
    hist.append(set(new))
    if grown==reach: break
    reach=grown
print("reachable channels by cumulative order, from kappa=-1:")
cum={-1}
for o,s in enumerate(hist):
    cum|=s
    print(f"  order {o}: new={sorted(s)}   cumulative={sorted(cum)}")
print(f"\nFINAL reachable set: {sorted(reach)}")
print(f"  kappa=-4 in reachable set (any order)?  {-4 in reach}")
print(f"  |kappa|<=3 ceiling?  max|kappa|={max(abs(k) for k in reach)}  -> {'CEILING at 3' if max(abs(k) for k in reach)<=3 else 'NO ceiling (unbounded tower)'}")
print(f"  l-parity of reachable: l-values={sorted(set(m.l_of(k) for k in reach))} (all even => l-parity conserved)")
