"""BOUNDED NODE-3 F4 TEST -- omega-augmented Jacobi/Derrick on SAVED fixed phi(r) backgrounds.
1-D linear algebra ONLY. No nonlinear solve, no field generation, single process.
Reduced Theta-energy from the node23_precompute_map DERIVED operator (L2), both P16 branches.
"""
import os, sys, math, numpy as np, torch
torch.set_default_dtype(torch.float64)
REPO = "/home/udt-admin/udt_mass_codex"
sys.path.insert(0, REPO)
import cell_solver_f2d as F2D

# ---- cell Cheb grid operators (rebuild the f2d cell grid: r in [0, r_p]) ----
def cell_grid(Nr):
    zeta, Dz = F2D._cheb(Nr)          # ascending zeta in [-1,1]; node0=zeta=-1=r=0(core), node-1=seal
    ccw = F2D._cc_weights(Nr)         # Clenshaw-Curtis weights on [-1,1]
    return (torch.tensor(zeta), torch.tensor(Dz), torch.tensor(ccw))

def load_cell(fname):
    d = torch.load(os.path.join(REPO, fname), map_location="cpu", weights_only=False)
    w = d["w"]; Nr = d["Nr"]; Nth = d["Nth"]; Na = d["Na"]; prm = d["prm"]
    i = 0
    phi_c = w[i:i+Nr]; i += Nr
    rho_c = w[i:i+Nr]; i += Nr
    i += Nr*Nth            # skip u
    i += Na               # skip phi_amb
    i += Na               # skip rho_amb
    r_p = float(w[i]); r_sU = float(w[i+1])
    return dict(fname=fname, phi=phi_c.clone(), rho=rho_c.clone(), r_p=r_p, r_sU=r_sU,
                Nr=Nr, prm=tuple(prm), tag=d["tag"])

# =========================================================================================
# REDUCED THETA-ENERGY (node23_precompute_map, L2, DERIVED CAS operator)
#   E[Theta;Om2] = INT_0^{r_p} dr (xi/2) rho^2 [ Wk(r) Theta'^2 + sin^2Theta ( N^2/rho^2 - Wb(r) Om2 ) ]
#   measure sqrt(-g)_radial = rho^2 (angular integrated to a const, dropped)
#   Branch B (raw/physical):   Wk = e^{-2phi}   (radial kinetic e^{-2phi}Theta'^2)
#                              Wb = e^{+2phi}    (omega-binding rho^2 e^{2phi} Om2 sin^2Theta)
#   Branch A (phi-blind):      Wk = 1           (kinetic stripped to Theta'^2)
#                              Wb = 1            (omega-binding depth-uniform)
#   Om2 = omega^2/c^2  (FREE spin parameter, units 1/length^2; c absorbed in natural units)
# =========================================================================================
def build_weights(fld, branch):
    phi = fld["phi"]; rho = fld["rho"]
    e2m = torch.exp(-2.0*phi); e2p = torch.exp(2.0*phi)
    if branch == "B":
        Wk = e2m; Wb = e2p
    elif branch == "A":
        Wk = torch.ones_like(phi); Wb = torch.ones_like(phi)
    return Wk, Wb, rho

def trial_theta(Nr, kind="linear"):
    # monotone Theta(0)=pi, Theta(r_p)=0 on ascending zeta grid (node0=core r=0, node-1=seal)
    zeta, _, _ = cell_grid(Nr)
    x = (zeta + 1.0)/2.0            # 0 at core .. 1 at seal
    if kind == "linear":
        th = math.pi*(1.0 - x)
    elif kind == "cos":
        th = math.pi*torch.cos(math.pi*x/2.0)**2   # smooth, flat ends
    return th

def energy(theta_full, fld, branch, Om2, N, XI):
    """Discrete reduced Theta-energy via Clenshaw-Curtis quadrature + Cheb derivative (solver style)."""
    zeta, Dz, ccw = cell_grid(fld["Nr"])
    L = fld["r_p"]
    sc = 2.0/L                                   # d/dr = (2/L) Dz
    Wk, Wb, rho = build_weights(fld, branch)
    thp = sc*(Dz @ theta_full)                   # Theta'(r)
    s2 = torch.sin(theta_full)**2
    dens = (XI/2.0)*rho**2*( Wk*thp**2 + s2*( N**2/rho**2 - Wb*Om2 ) )
    return (ccw * dens).sum() * (L/2.0)          # dr = (L/2) dzeta

def jacobi_lammin(fld, branch, Om2, N, XI, kind="linear"):
    """Lowest eigenvalue of Hessian of E wrt INTERIOR Theta (Dirichlet endpoints pinned)."""
    Nr = fld["Nr"]
    th0 = trial_theta(Nr, kind)
    thc = th0[0].item(); ths = th0[-1].item()    # pinned core & seal values
    interior0 = th0[1:-1].clone()
    def E_of_interior(u):
        th = torch.cat([torch.tensor([thc]), u, torch.tensor([ths])])
        return energy(th, fld, branch, Om2, N, XI)
    H = torch.func.hessian(E_of_interior)(interior0)
    H = 0.5*(H + H.T)
    ev = torch.linalg.eigvalsh(H)
    return float(ev[0]), float(ev[-1])

def omega_ceiling(fld, branch, N):
    """Om2_ceil = smallest Om2 making the winding potential P(r)=N^2 - rho^2 Wb Om2 go <0 somewhere
    (B(r)=0 flip / ergoregion onset per node23 Q5). Returns Om2 where P first hits 0."""
    Wk, Wb, rho = build_weights(fld, branch)
    P_coeff = (rho**2 * Wb)                       # P = N^2 - Om2 * P_coeff  (per node)
    Om2_ceil = float((N**2 / P_coeff).min())      # first r where P=0
    return Om2_ceil

# ---- Derrick width-scan: Theta_lam(r)=Theta0(r/lam) concentrates winding into [0, lam*r_p] ----
def derrick_curve(fld, branch, Om2, N, XI, kind="linear", nlam=25, nfine=400):
    phi = fld["phi"].numpy(); rho = fld["rho"].numpy()
    zeta, _, _ = cell_grid(fld["Nr"]); zeta = zeta.numpy()
    L = fld["r_p"]
    r_nodes = L*(zeta+1.0)/2.0
    rf = np.linspace(0.0, L, nfine)
    phif = np.interp(rf, r_nodes, phi); rhof = np.interp(rf, r_nodes, rho)
    if branch == "B":
        Wkf = np.exp(-2*phif); Wbf = np.exp(2*phif)
    else:
        Wkf = np.ones_like(phif); Wbf = np.ones_like(phif)
    def th0(x):   # x in [0,1] fraction of r_p ; monotone pi->0
        if kind == "linear": return math.pi*(1.0 - x)
        return math.pi*np.cos(math.pi*x/2.0)**2
    lams = np.linspace(0.15, 1.6, nlam)
    Es = []
    for lam in lams:
        xarg = np.clip((rf/L)/lam, 0.0, 1.0)      # profile concentrated in [0, lam*r_p]
        th = th0(xarg)
        thp = np.gradient(th, rf)
        s2 = np.sin(th)**2
        dens = (XI/2.0)*rhof**2*( Wkf*thp**2 + s2*(N**2/rhof**2 - Wbf*Om2) )
        Es.append(np.trapz(dens, rf))
    return lams, np.array(Es)

# =========================================================================================
if __name__ == "__main__":
    FIELDS = ["E2b_A1Z1_P2_W4_wall.pt", "E2b_A1Z8_P2_W2_wall.pt", "E2b_A3Z1_P2_W2_wall.pt"]
    print("="*90)
    print("STEP 1 -- fields + sign(phi_core) confirmation")
    print("="*90)
    flds = []
    for fn in FIELDS:
        f = load_cell(fn); flds.append(f)
        Z,XI,KAP,N = f["prm"]
        phic = float(f["phi"][0]); phis = float(f["phi"][-1])
        print(f"\n{fn}  tag={f['tag']}  prm(Z,xi,kap,N)={f['prm']}")
        print(f"  r_p={f['r_p']:.4g}  r_sU={f['r_sU']:.4g}  Nr={f['Nr']}")
        print(f"  phi_core={phic:+.5f}  phi_seal={phis:+.5f}")
        print(f"  e^-2phi_core={math.exp(-2*phic):.4e}   e^+2phi_core={math.exp(2*phic):.4e}")
        print(f"  e^-2phi_seal={math.exp(-2*phis):.4e}   e^+2phi_seal={math.exp(2*phis):.4e}")
        print(f"  rho_core={float(f['rho'][0]):.4e}  rho_seal={float(f['rho'][-1]):.4e}")
        print(f"  phi_core<0 (e^2phi core-suppressed)? {phic<0}")

    print("\n"+"="*90)
    print("STEP 3+4 -- Jacobi lambda_min(Om2) sweep, both branches, each field, both trials")
    print("="*90)
    for f in flds:
        Z,XI,KAP,N = f["prm"]
        XI = float(XI); N = int(N)
        print(f"\n########## {f['fname']}  (N={N}, xi={XI}) ##########")
        for branch in ["B","A"]:
            ceil = omega_ceiling(f, branch, N)
            # sweep Om2 from 0 to 3x ceiling
            grid = np.concatenate([[0.0], np.linspace(0.05,1.0,8)*ceil, np.linspace(1.2,3.0,5)*ceil])
            print(f"  --- Branch {branch}   Om2_ceiling(P->0 flip) = {ceil:.4e} ---")
            for kind in ["linear","cos"]:
                lam0 = jacobi_lammin(f, branch, 0.0, N, XI, kind)[0]
                row = []
                crossed = None
                for Om2 in grid:
                    lm,_ = jacobi_lammin(f, branch, float(Om2), N, XI, kind)
                    row.append((Om2, lm))
                    if crossed is None and lam0 < 0 and lm >= 0:
                        crossed = Om2
                print(f"    trial={kind:6s}  lam_min(Om2=0)={lam0:+.4e}")
                for Om2,lm in row:
                    flag = ""
                    if Om2 > ceil: flag = " (>ceiling: ansatz-broken)"
                    print(f"        Om2={Om2:.3e} (Om2/ceil={Om2/ceil:5.2f})  lam_min={lm:+.4e}{flag}")
                if lam0 >= 0:
                    verdict = "static already PD (no collapse mode at this trial)"
                elif crossed is not None and crossed <= ceil:
                    verdict = f"*** CROSSES to >=0 at Om2={crossed:.3e} (<=ceiling) -> CLASS(1) candidate"
                elif crossed is not None:
                    verdict = f"crosses only ABOVE ceiling (Om2={crossed:.3e}) -> CLASS(2)"
                else:
                    # check if lam_min moves up at all with Om2
                    dlam = row[-1][1]-lam0
                    verdict = (f"never crosses in [0,3xceil]; d(lam_min)={dlam:+.3e} "
                               f"({'restoring but insufficient CLASS(2)' if dlam>1e-12*abs(lam0)+1e-30 else 'no restoring effect CLASS(3)'})")
                print(f"        VERDICT[{branch},{kind}]: {verdict}")

    print("\n"+"="*90)
    print("STEP 3 (Derrick corroboration) -- E(lam;Om2), Branch B, linear trial")
    print("="*90)
    for f in flds:
        Z,XI,KAP,N = f["prm"]; XI=float(XI); N=int(N)
        ceil = omega_ceiling(f,"B",N)
        print(f"\n{f['fname']}  Branch B  Om2_ceil={ceil:.3e}")
        for Om2 in [0.0, 0.5*ceil, ceil, 2.0*ceil]:
            lams, Es = derrick_curve(f, "B", float(Om2), N, XI, "linear")
            imin = int(np.argmin(Es))
            interior = 0 < imin < len(lams)-1
            print(f"  Om2={Om2:.3e}: E min at lam={lams[imin]:.3f} "
                  f"({'INTERIOR stationary' if interior else 'boundary (collapse/expand)'})  "
                  f"E(0.15)={Es[0]:.3e} E(1.0)={Es[len(lams)//2]:.3e} E(1.6)={Es[-1]:.3e}")
