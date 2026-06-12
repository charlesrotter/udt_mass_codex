import numpy as np
from scipy.integrate import solve_ivp

# Form-T radial Dirac in inside-out well, conv-B (binding): phi = +A exp(-(mu r)^2)
# G' = (phi' - kappa/r) G + (E e^{2phi} + m e^{phi}) F
# F' = (phi' + kappa/r) F - (E e^{2phi} - m e^{phi}) G
# m=1 exterior gap; bound states 0<E<m. IC: G ~ r^{|kappa|}, F subdominant.

m = 1.0

def make_rhs(E, A, mu, kappa):
    def phi(r):
        return A*np.exp(-(mu*r)**2)
    def dphi(r):
        return -2*A*mu**2*r*np.exp(-(mu*r)**2)
    def rhs(r, y):
        G, F = y
        ph = phi(r); dph = dphi(r)
        e1 = np.exp(ph); e2 = np.exp(2*ph)
        dG = (dph - kappa/r)*G + (E*e2 + m*e1)*F
        dF = (dph + kappa/r)*F - (E*e2 - m*e1)*G
        return [dG, dF]
    return rhs

def shoot(E, A, mu, kappa, r0=1e-6, rmax=40.0):
    ak = abs(kappa)
    # near-origin series: G ~ r^ak, F subdominant.
    # Leading: F/G determined by lower-component coupling. Use small-r expansion.
    # From F' = (phi'+kappa/r)F - (E e2 - m e1)G, with phi~A, e1~e^A, e2~e^{2A} near 0.
    # G = r^ak. The particular F ~ -(E e2 - m e1) r^{ak+1}/( (ak+1)+kappa )  approx.
    ph0 = A; e1 = np.exp(ph0); e2 = np.exp(2*ph0)
    G0 = r0**ak
    # solve algebraically for subdominant F at r0: treat F=c r^{ak+1}
    # F' = (ak+1)c r^ak ; RHS leading: (kappa/r)*c r^{ak+1} - (E e2 - m e1) r^ak
    # (ak+1)c = kappa c - (E e2 - m e1)  => c(ak+1-kappa) = -(E e2 - m e1)
    denom = (ak+1-kappa)
    c = -(E*e2 - m*e1)/denom if denom!=0 else 0.0
    F0 = c*r0**(ak+1)
    sol = solve_ivp(make_rhs(E,A,mu,kappa), [r0, rmax], [G0,F0],
                    rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.1)
    # normalize by growing magnitude to read sign of decaying tail
    G_end = sol.y[0,-1]; F_end = sol.y[1,-1]
    # asymptotic decaying solution should have G,F -> 0. Mismatch = G_end (after scaling)
    scale = np.max(np.abs(sol.y))
    return G_end/scale, sol

def find_states(A, mu, kappa, nE=4000, Emin=1e-4, Emax=0.9999):
    Es = np.linspace(Emin, Emax, nE)
    vals = []
    for E in Es:
        v,_ = shoot(E,A,mu,kappa)
        vals.append(v)
    vals = np.array(vals)
    roots=[]
    for i in range(len(Es)-1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i+1]) and vals[i]*vals[i+1]<0:
            # bisect
            a,b = Es[i],Es[i+1]
            fa,_=shoot(a,A,mu,kappa);
            for _ in range(60):
                mid=0.5*(a+b)
                fm,_=shoot(mid,A,mu,kappa)
                if not np.isfinite(fm): break
                if fa*fm<0: b=mid
                else: a=mid; fa=fm
            roots.append(0.5*(a+b))
    return roots

if __name__=="__main__":
    print("Scan A (depth), mu=range^-1. Ground-state E for |kappa|=1,2,3.")
    print(f"{'A':>5} {'mu':>5} | {'E1':>9} {'E2':>9} {'E3':>9} | {'E2/E1':>7} {'E3/E1':>7}")
    for A in [1.0,2.0,3.0,4.0,5.0,6.0,8.0]:
        for mu in [0.5,1.0,2.0]:
            gs={}
            for k in [1,2,3]:
                # for given |kappa|, scan both kappa signs? bound usually kappa<0 or >0; test kappa=-|k| (s-like) and +|k|
                roots_m = find_states(A,mu,-k)
                roots_p = find_states(A,mu,+k)
                allr = sorted(roots_m+roots_p)
                gs[k]=allr[0] if allr else None
            if all(gs[k] is not None for k in [1,2,3]):
                E1,E2,E3=gs[1],gs[2],gs[3]
                print(f"{A:5.1f} {mu:5.1f} | {E1:9.5f} {E2:9.5f} {E3:9.5f} | {E2/E1:7.3f} {E3/E1:7.3f}")
            else:
                avail={k:gs[k] for k in gs}
                print(f"{A:5.1f} {mu:5.1f} | not all bound: {avail}")
