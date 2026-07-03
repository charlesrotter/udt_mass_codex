"""bv13: probe the n_pos(V^) off-by-one.
V^ is tridiagonal in my scheme -> Sturm-count inertia at shift 0 for very large M (no eigensolver).
Variants: (a) v_0 = 0 imposed (the claimed Q^ reduction);  (b) v_0 FREE (natural at core).
Also: top-of-spectrum margins at M=1600 (how close the missing mode is to 0), and the WKB phase
Theta/pi = (1/pi) int e^phi sqrt((Z/4)phi'^2 - U''(rho)/4)_+ dr for both rungs.
"""
import numpy as np, json
from scipy.linalg import eigh_tridiagonal

Z = 8.0
BG = np.load("bv13_bg.npz")
INFO = json.load(open("bv13_bg.json"))

def makeU(a, m=3.0):
    def U(rho):  return 2.0*rho**m*np.exp(-a*(rho*rho-1.0))
    def Up(rho): return U(rho)*(m/rho - 2.0*a*rho)
    def Upp(rho):return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp

def background(tag, r):
    rr = BG[tag+"_r"]; Y = BG[tag+"_y"]
    return [np.interp(r, rr, Y[i]) for i in range(4)]

def vhat_tridiag(tag, M, v0_free=False):
    info = INFO[tag]; a = info["a"]; r_s = info["r_s"]
    U, Up, Upp = makeU(a)
    h = r_s/M
    rm = (np.arange(M)+0.5)*h
    phi, phip, rho, rhop = background(tag, rm)
    ckv = -2.0*np.exp(-2.0*phi)
    cmv = 0.5*Z*phip**2 - 0.5*Upp(rho)
    # nodes v_0..v_M ; element j couples (j, j+1):
    # kinetic ckv/h*(v_{j+1}-v_j)^2 ; mass cmv*h*((v_j+v_{j+1})/2)^2
    n = M+1
    d = np.zeros(n); e = np.zeros(n-1)
    d[:-1] += ckv/h + cmv*h/4.0
    d[1:]  += ckv/h + cmv*h/4.0
    e[:]   += -ckv/h + cmv*h/4.0
    if not v0_free:
        d = d[1:]; e = e[1:]
    return d, e

def sturm_counts(d, e, shift=0.0):
    # LDL^T sturm sequence for tridiagonal T - shift I: count negative pivots
    n = len(d)
    nneg = 0; nzero = 0
    piv = d[0]-shift
    if piv < 0: nneg += 1
    if piv == 0: nzero += 1; piv = 1e-300
    for i in range(1, n):
        piv = (d[i]-shift) - e[i-1]**2/piv
        if piv < 0: nneg += 1
        elif piv == 0: nzero += 1; piv = 1e-300
    return nneg, n-nneg-nzero, nzero

print("=== n_pos(Vhat) vs M (Sturm at 0), variant (a) v0=0 and (b) v0 free ===")
for tag in ("N0", "N5"):
    for M in (800, 1600, 3200, 6400, 12800, 25600, 51200):
        row = {}
        for v0f in (False, True):
            d, e = vhat_tridiag(tag, M, v0_free=v0f)
            nneg, npos, nz = sturm_counts(d, e)
            row["v0free" if v0f else "v0dir"] = (nneg, npos, nz)
        print(f"[{tag} M={M:6d}] v0=0: n_neg={row['v0dir'][0]:6d} n_pos={row['v0dir'][1]}   "
              f"v0 free: n_neg={row['v0free'][0]:6d} n_pos={row['v0free'][1]}")

print("\n=== top eigenvalues of Vhat (v0=0) at M=1600 (margins) ===")
for tag in ("N0", "N5"):
    d, e = vhat_tridiag(tag, 1600)
    n = len(d)
    w = eigh_tridiagonal(d, e, select="i", select_range=(n-8, n-1), eigvals_only=True)
    print(f"[{tag}] top-8 eigenvalues:", np.array2string(w, precision=4))
    dv, ev = vhat_tridiag(tag, 1600, v0_free=True)
    nv = len(dv)
    wv = eigh_tridiagonal(dv, ev, select="i", select_range=(nv-8, nv-1), eigvals_only=True)
    print(f"[{tag}] top-8 (v0 free):  ", np.array2string(wv, precision=4))

print("\n=== WKB phase Theta/pi (own quadrature; oscillatory region only) ===")
for tag in ("N0", "N5"):
    info = INFO[tag]; a = info["a"]; U, Up, Upp = makeU(a)
    r = np.linspace(0.0, info["r_s"], 400001)
    phi, phip, rho, rhop = background(tag, r)
    arg = 0.25*Z*phip**2 - 0.25*Upp(rho)
    integ = np.exp(phi)*np.sqrt(np.clip(arg, 0.0, None))
    theta = np.trapezoid(integ, r)
    print(f"[{tag}] Theta/pi = {theta/np.pi:.4f}   (claimed n_pos(Vhat): {1 if tag=='N0' else 7})")
