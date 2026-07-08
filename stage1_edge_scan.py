"""
Stage 1 edge-existence scan (matter_filled_background_closure_DESIGN.md).

OBSERVE, do not target. Data-blind. Bounded 1-D ODE.

Native two-player Branch-P interior, matter ON via a PRESCRIBED localized I_r(r)
(amplitude A_m = the matter-amount knob, a ledgered recon STAND-IN, P5):

  phi'' = (4/Z) e^{-2phi} rho'^2/rho^2  -  2 phi' rho'/rho  +  (alpha*xi/Z) e^{alpha*phi} I_r
  rho'' = 2 phi' rho'  -  (Z/4) rho e^{2phi} phi'^2  +  (xi/4) e^{2phi} rho I_r

Finite core BC: rho(rc)=rho_c>0, phi(rc)=phi_c, mirror core slopes phi'(rc)=rho'(rc)=0
(the matter source breaks the vacuum triviality). I_4th/L4 term set to 0 for this
scan (scoped-out; the phi-source restoring channel is the I_r question).

Question (M1 recon-only): for which (alpha, A_m) does a finite v=e^{-phi/2} -> 0 edge
appear (the thing vacuum NEVER gives)?  Classify each run: EDGE / SATURATE / RUNAWAY / COLLAPSE.
Look for a critical A_m or a bounded window.  M2: repeat for 3 I_r shapes.
"""
import numpy as np
from scipy.integrate import solve_ivp

XI = 1.0
RC = 0.1          # finite core radius
RHO_C = RC        # rho(rc)=rc (areal-ish core seed)
RMAX = 40.0       # bounded integration span
PHI_CAP = 18.0    # |phi| cap; events fire before the extreme-stiffness region
                  # (v=e^{-phi/2} spans ~1.2e-4 .. ~8e3 -> ample to declare edge/runaway)

def make_Ir(shape, A_m, w=1.0):
    """Prescribed localized I_r(r) >= 0, peak ~ at the core, amplitude A_m."""
    if shape == "gauss":
        return lambda r: A_m * np.exp(-((r - RC) / w) ** 2)
    if shape == "exp":
        return lambda r: A_m * np.exp(-(r - RC) / w)
    if shape == "cos2":   # compact bump on [RC, RC+pi*w], zero outside
        return lambda r: A_m * np.where(r < RC + np.pi * w,
                                        np.cos((r - RC) / (2 * w)) ** 2, 0.0)
    raise ValueError(shape)

def rhs(r, y, Z, alpha, Ir, phi_c):
    phi, phip, rho, rhop = y
    if rho <= 1e-9:
        return [0, 0, 0, 0]
    Irr = Ir(r)
    e_m2 = np.exp(-2 * phi)
    e_p2 = np.exp(2 * phi)
    e_al = np.exp(alpha * phi)
    phipp = (4.0 / Z) * e_m2 * rhop**2 / rho**2 - 2 * phip * rhop / rho \
            + (alpha * XI / Z) * e_al * Irr
    rhopp = 2 * phip * rhop - (Z / 4.0) * rho * e_p2 * phip**2 \
            + (XI / 4.0) * e_p2 * rho * Irr
    return [phip, phipp, rhop, rhopp]

def classify(Z, alpha, shape, A_m, phi_c=0.0, w=1.0):
    Ir = make_Ir(shape, A_m, w)
    y0 = [phi_c, 0.0, RHO_C, 0.0]

    # events: v=0  <=> phi -> +PHI_CAP ; rho->0 collapse ; phi->-PHI_CAP runaway
    def ev_edge(r, y, *a):   return y[0] - PHI_CAP        # phi up to +cap  => v->0
    def ev_collapse(r, y, *a): return y[2] - 1e-6         # rho -> 0
    def ev_runaway(r, y, *a): return y[0] + PHI_CAP       # phi -> -cap     => v->inf
    for ev in (ev_edge, ev_collapse, ev_runaway):
        ev.terminal = True
    ev_edge.direction = 1
    ev_collapse.direction = -1
    ev_runaway.direction = -1

    try:
        sol = solve_ivp(rhs, [RC, RMAX], y0, args=(Z, alpha, Ir, phi_c),
                        events=(ev_edge, ev_collapse, ev_runaway),
                        method="LSODA", rtol=1e-6, atol=1e-8, dense_output=False)
    except Exception:
        return ("FAIL", np.nan)
    if not sol.success and len(sol.t_events[0]) == 0 and \
       len(sol.t_events[1]) == 0 and len(sol.t_events[2]) == 0:
        return ("FAIL", np.nan)
    if len(sol.t_events[0]) > 0:
        return ("EDGE", sol.t_events[0][0])          # finite v->0 edge  <-- the x_max signature
    if len(sol.t_events[1]) > 0:
        return ("COLLAPSE", sol.t_events[1][0])
    if len(sol.t_events[2]) > 0:
        return ("RUNAWAY", sol.t_events[2][0])
    # reached RMAX with |phi|<cap and rho>0 -> saturating/bounded
    return ("SATURATE", sol.y[0, -1])

def scan(coarse=True):
    if coarse:
        alphas = [-2.0, -1.0, 0.0, 1.0, 2.0]
        A_ms = [0.0, 0.01, 0.1, 1.0, 10.0, 100.0]
        shapes = ["gauss"]
        Zs = [1.0]
    else:
        alphas = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]
        A_ms = [0.0] + list(np.round(np.logspace(-3, 3, 19), 4))  # ~1e-3 .. 1e3 + vacuum
        shapes = ["gauss", "exp", "cos2"]
        Zs = [1.0, 8.0]

    print("=" * 78)
    print("STAGE-1 EDGE-EXISTENCE SCAN  (EDGE = finite v=e^{-phi/2}->0, the x_max signature)")
    print("phi_c=0, core mirror, I_4th=0.  Outcome vs A_m (matter amount).")
    print("=" * 78)
    edge_summary = []
    for Z in Zs:
        for shape in shapes:
            print(f"\n### Z={Z}  I_r-shape={shape}")
            print(f"{'alpha':>6} | outcomes across A_m (log-spaced 1e-3..1e3; first col A_m=0 vacuum)")
            for alpha in alphas:
                row = []
                edge_Ams = []
                for A_m in A_ms:
                    kind, val = classify(Z, alpha, shape, A_m)
                    tag = {"EDGE": "E", "SATURATE": ".", "RUNAWAY": "R",
                           "COLLAPSE": "C", "FAIL": "x"}[kind]
                    row.append(tag)
                    if kind == "EDGE":
                        edge_Ams.append(A_m)
                print(f"{alpha:>6} | {''.join(row)}   " +
                      (f"EDGE@A_m in [{min(edge_Ams):.3g},{max(edge_Ams):.3g}]" if edge_Ams else "no edge"))
                if edge_Ams:
                    edge_summary.append((Z, shape, alpha, min(edge_Ams), max(edge_Ams)))
    print("\n" + "=" * 78)
    print("EDGE REGIONS FOUND (Z, shape, alpha, A_m_min, A_m_max):")
    if edge_summary:
        for e in edge_summary:
            print(f"  Z={e[0]} {e[1]:>5} alpha={e[2]:+.1f}  A_m in [{e[3]:.3g}, {e[4]:.3g}]")
    else:
        print("  NONE — no finite v->0 edge anywhere in the scanned (alpha, A_m) x 3-shapes x Z grid.")
    print("Legend: E=edge(v->0)  .=saturate  R=runaway(phi->-inf,v->inf)  C=collapse(rho->0)  x=fail")
    print("A_m grid:", ["vac"] + [f"{a:g}" for a in A_ms[1:]])

if __name__ == "__main__":
    import sys
    scan(coarse=("full" not in sys.argv))
