import numpy as np

# Diagonalize H(q,m) = -(1/sin) d/dth(sin d/dth) + (m - q cos th)^2/sin^2 th
# on a grid, for each azimuthal eigenvalue m. Check eigenvalues = l(l+1) - q^2.

def H_eigs(q, m, N=2000):
    # interior grid avoiding poles
    th = np.linspace(1e-4, np.pi-1e-4, N)
    dth = th[1]-th[0]
    s = np.sin(th)
    # build operator on f(th) with measure; use symmetric form via u = sqrt(sin) f? 
    # Simpler: discretize -1/s d/dth(s d/dth) f + V f  with finite differences (non-symmetric ok for eigenvalues)
    V = (m - q*np.cos(th))**2 / s**2
    A = np.zeros((N,N))
    for i in range(1,N-1):
        sp = 0.5*(s[i]+s[i+1])
        sm = 0.5*(s[i]+s[i-1])
        A[i,i-1] = -sm/(s[i]*dth**2)
        A[i,i+1] = -sp/(s[i]*dth**2)
        A[i,i]   = (sm+sp)/(s[i]*dth**2) + V[i]
    # crude Dirichlet at ends (states vanish at poles for these potentials)
    A=A[1:-1,1:-1]
    ev = np.linalg.eigvals(A)
    ev = np.sort(ev.real)
    return ev[:6]

for q in [0.0, 0.5, 1.0]:
    print(f"--- q={q} ---")
    # collect lowest eigenvalues across several m, infer l-spectrum
    allv=[]
    mvals = np.arange(-3+ (0.5 if abs(q-0.5)<1e-9 else 0.0), 3.01, 1.0) if abs(q-0.5)<1e-9 else np.arange(-3,3.01,1.0)
    # For q half-integer, m is half-integer; for integer q, m integer
    for m in mvals:
        ev = H_eigs(q, m)
        allv.extend(ev.tolist())
    allv=np.array(sorted(allv))
    # eigenvalue should be l(l+1)-q^2 ; so l(l+1)=ev+q^2
    # report distinct lowest few
    seen=[]
    for v in allv:
        ll = v + q*q
        # solve l(l+1)=ll -> l=(-1+sqrt(1+4ll))/2
        l = (-1+np.sqrt(1+4*ll))/2
        if all(abs(l-x)>0.05 for x in seen):
            seen.append(l)
        if len(seen)>=4: break
    print("  inferred l (=j):", [round(x,3) for x in seen])
