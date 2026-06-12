#!/usr/bin/env python3
"""Script 3: universe-side medium and global exterior-driven formation.
Global source-free domain (y_dgn, Y]; ALL data at the outer shell Y
(where cosmic structure lives). Reference exterior monopole: the mirrored
collar continuation F = y^-q (q=1/3), f<1 for y>1 (universe side, CANON C-2).
Medium angular amplitude A at Y, zero angular momentum at Y (momentum
develops via EL). Integrate inward through the f=1 crossing; formation =
seal (kappa->1) strictly inside the crossing with F>1 collar.
"""
import numpy as np
from scipy.integrate import solve_ivp
from exterior_cavity_s2c_flows import Hfun, Wpfun

SQ3 = np.sqrt(3.0)
Q = 1.0/3.0

def rhs(y, w):
    F, g, a, h = w
    k = SQ3*a/F
    return [g/y**2, -Hfun(k), h/y**2, 2*SQ3*Wpfun(k)]

def ev_seal(y, w): return abs(SQ3*w[2]/w[0]) - (1-1e-8)
ev_seal.terminal = True

def global_flow(Y, A, hY=0.0, FY=None, gY=None, ymin=1e-8, rtol=1e-11):
    FY = Y**(-Q) if FY is None else FY
    gY = -Q*Y**(1-Q) if gY is None else gY
    w0 = [FY, gY, A, hY]
    sol = solve_ivp(rhs, [Y, ymin], w0, events=[ev_seal], rtol=rtol, atol=1e-15,
                    method='DOP853', dense_output=True)
    out = {}
    # f=1 crossing of the monopole (the emergent interface)
    ys = np.geomspace(max(sol.t[-1], ymin), Y, 30000)
    W = sol.sol(ys)
    Fv, gv, av, hv = W
    cross = np.where(np.diff(np.sign(Fv - 1)))[0]
    y1 = ys[cross[-1]] if len(cross) else None
    out['y_interface'] = y1
    if y1 is not None:
        i1 = cross[-1]
        out['jet'] = dict(F=Fv[i1], gamma=-gv[i1], a1=av[i1], c=-hv[i1],
                          kappa1=SQ3*av[i1]/Fv[i1])
    if len(sol.t_events[0]):
        ysl = sol.t_events[0][0]
        out['y_seal'] = ysl
        out['F_seal'] = sol.y_events[0][0][0]
        if y1 is not None and ysl < y1:
            out['type'] = 'FORM'      # seal inside the f=1 crossing: cavity
        else:
            out['type'] = 'EXT_DGN'   # medium degenerates before delivering
    else:
        out['type'] = 'NOFORM'        # rides to ymin: saturating (B/y, infinite action)
        out['kinf'] = abs(SQ3*sol.y[2, -1]/sol.y[0, -1])
    out['minF_inside'] = Fv[ys <= (y1 or Y)].min() if y1 else None
    out['kmax_outside'] = (np.abs(SQ3*av/Fv)[ys >= (y1 or ys[0])]).max()
    return out

def A_threshold(Y, lo=1e-8, hi=None, iters=50, **kw):
    hi = hi or 0.4*Y**(-Q)/SQ3   # cap: kappa(Y) < 0.4
    tlo = global_flow(Y, lo, **kw)['type']
    thi = global_flow(Y, hi, **kw)['type']
    if tlo != 'NOFORM' or thi == 'NOFORM': return None, tlo, thi
    for _ in range(iters):
        mid = np.sqrt(lo*hi)
        if global_flow(Y, mid, **kw)['type'] == 'NOFORM': lo = mid
        else: hi = mid
    return np.sqrt(lo*hi), tlo, thi

if __name__ == '__main__':
    print("=== A. anatomy of a supercritical global flow (Y=3) ===")
    Astar, _, _ = A_threshold(3.0)
    print(f"A*(Y=3) = {Astar:.8f}   [medium amplitude at the structure shell]")
    for fac, lab in [(0.9, 'sub'), (1.1, 'super'), (3.0, 'strong')]:
        r = global_flow(3.0, Astar*fac)
        j = r.get('jet')
        js = (f"interface y1={r['y_interface']:.4f} gamma={j['gamma']:.4f} "
              f"a1={j['a1']:.5f} c={j['c']:.5f} kappa1={j['kappa1']:.4f}") if j else "no f=1 crossing"
        seal = f" seal y={r.get('y_seal', float('nan')):.5f} F_seal={r.get('F_seal', float('nan')):.4f}" \
               if 'y_seal' in r else f" kinf={r.get('kinf', float('nan')):.4f}"
        print(f"  {lab:6s} A={Astar*fac:.6f}: {r['type']:7s} {js}{seal} kmax_out={r['kmax_outside']:.4f}")

    print("\n=== B. delivered-jet consistency with matter-side threshold curve ===")
    r = global_flow(3.0, Astar*1.0000001)
    j = r['jet']
    print(f"  delivered at f=1 crossing: gamma={j['gamma']:.6f}, c={j['c']:.6f}, a1={j['a1']:.6f}")
    print(f"  matter-side c*(gamma=1/3, a1=0) = 0.0350572 ; delivered c at A* should sit near the")
    print(f"  mixed-class threshold (a1 != 0 lowers it; trade-off slope ~0.91)")
    print(f"  effective momentum-mode content beta=(a1+c)/3 = {(j['a1']+j['c'])/3:.6f} vs c*/3 = {0.03506/3:.6f}")

    print("\n=== C. lever law: A*(Y) ===")
    Ys = [1.5, 2.0, 3.0, 5.0, 8.0, 12.0]
    As = []
    for Yv in Ys:
        Ast, tl, th = A_threshold(Yv)
        As.append(Ast)
        print(f"  Y={Yv:5.1f}: A* = {Ast if Ast else 'none ('+tl+'/'+th+')'}")
    Ys_f = [y for y, a in zip(Ys, As) if a]
    As_f = [a for a in As if a]
    p = np.polyfit(np.log(Ys_f), np.log(As_f), 1)
    print(f"  fit A* ~ Y^p: p = {p[0]:.4f}  (bare lever: -2; cosmic-background-dressed expected ~ -2+corr)")
    # also scaled threshold: medium kappa at Y
    print("  threshold in medium kappa(Y) = sqrt3 A*/F(Y):")
    for Yv, Ast in zip(Ys_f, As_f):
        print(f"    Y={Yv:5.1f}: kappa*(Y) = {SQ3*Ast/Yv**(-Q):.6f}")

    print("\n=== D. universe-side degeneration cap (delivery window) ===")
    Yv = 3.0
    lo, hi = Astar, 0.99/SQ3*Yv**(-Q)*2
    # find smallest A with EXT_DGN
    found = None
    for A in np.geomspace(Astar, 10*Astar, 40):
        r = global_flow(Yv, A)
        if r['type'] == 'EXT_DGN': found = A; break
    print(f"  Y=3: first EXT_DGN at A ~ {found if found else '>10 A* (window at least 10x)'}")

    print("\n=== E. mirror asymmetry (honest universe-side derivation notes) ===")
    # same |phi| profile mirrored: action density ratio between f and 1/f sides
    # radial: (y^2/4) f'^2 with f -> 1/f: ratio = f^{-4} * (f'^2 ratio: (1/f)' = -f'/f^2)
    # => radial density maps to (y^2/4) f'^2 / f^4 : ratio 1/f^4
    # angular per-solid-angle potential: P = F W(kappa) -> (1/F) W(kappa_mirror)...
    print("  radial C1 density under f->1/f: multiplied by f^-4 (e^{8 phi}); NOT symmetric")
    print("  angular stiffness P = F W(kappa): universe side (F<1) is SOFTER by factor F")
    print("  kappa = sqrt3 a/F: same orthonormal amplitude a costs MORE kappa on f<1 side")
    print("  => the universe side degenerates (kappa->1) at smaller amplitude: the delivery cap")

    print("\n=== F. reference demanded global medium (banked-collar continuation) ===")
    # kappa_dem(y) = H^{-1}(2s y^-q) on BOTH sides; amplitude at Y:
    import mpmath as mp
    for Yv in [2.0, 5.0, 12.0]:
        rhsv = (2.0/9.0)*Yv**(-1/3)
        kdem = mp.findroot(lambda kk: mp.log((1+kk)/(1-kk))/(2*kk) - 1 - rhsv, 0.6)
        Adem = float(Yv**(-1/3)*kdem/mp.sqrt(3))
        i = Ys_f.index(Yv) if Yv in Ys_f else None
        comp = f" vs A*({Yv}) = {As_f[i]:.6f} -> ratio {Adem/As_f[i]:.2f}" if i is not None else ""
        print(f"  Y={Yv:5.1f}: demanded medium A_dem = {Adem:.6f}{comp}")
