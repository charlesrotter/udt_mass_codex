"""BLIND VERIFIER — members M1-M4 with own engine; compare to the
audit's claimed values (members.pkl scalars = the report's numbers).
Plus: weld-jet Taylor of the MS aspect (incl. BACKWARD/exterior side),
deep-cell closure, identity battery."""
import sys, pickle
import numpy as np
sys.path.insert(0, '/tmp/verify_mass')
from vcore import measure, run_flow, P_and_grad, QDEF, QHI, Y1P, Y1PP, Quad
from scipy.integrate import solve_ivp

with open('/tmp/mass_audit/members.pkl', 'rb') as fh:
    mem = pickle.load(fh)

ICS = {}
for tag in ('M1', 'M2', 'M3', 'M4'):
    dat = np.loadtxt(f'/tmp/seal_s1/lib/bg_{tag}.dat', max_rows=1)
    ICS[tag] = (dat[6], -dat[7])

npass = nfail = 0
def chk(name, got, want, tol):
    global npass, nfail
    ok = abs(got - want) <= tol
    npass += ok; nfail += (not ok)
    flag = "PASS" if ok else "FAIL"
    print(f"   [{flag}] {name}: mine {got:.8g}  claim {want:.8g}  "
          f"d={got-want:+.2e}")

SCAL = ['t_stop', 't_seal', 'y_seal', 'A_tot', 'A_kin', 'A_pot',
        'F_seal', 'D', 'M0_seal', 'm_pole_seal', 'E_seal']
for tag in ('M1', 'M2', 'M3', 'M4'):
    g, c = ICS[tag]
    o = measure(g, c, label=tag)
    a = mem[tag]
    print(f"--- {tag} (gamma={g}, c={c:.8f}) ---")
    for s in SCAL:
        ref = abs(a[s])
        chk(s, o[s], a[s], max(2e-5*ref, 2e-6))
    for i in range(4):
        chk(f"dp_dir[{i}]", o['dp_dir'][i], a['dp_dir'][i], 5e-6)
        chk(f"p_seal[{i}]", o['p_seal'][i], a['p_seal'][i], 5e-6)
    chk("fK_lim(half-law, as audit computed)", o['fK_lim'], a['fK_lim'],
        1e-4*abs(a['fK_lim']))
    # identities on MY run
    chk("virial A - (bnd+pot/2)", o['A_vir'] - o['A_tot'], 0.0,
        1e-7*max(1, o['A_tot']))
    chk("weld bnd term = gamma/4", o['bnd_weld'], g/4, 1e-14)
    chk("a(0) = (g^2+c^2)/4", o['E0'] + 0.0, (g*g+c*c)/4, 1e-14)
    for i in range(4):
        chk(f"dp transfer ch{i}", o['dp_dir'][i], o['dp_int'][i],
            3e-6*max(1, abs(o['dp_dir'][i])))
    chk("m_pole_seal vs (y_stop/2)(1-fstop)", o['m_pole_seal'],
        0.5*np.exp(-o['t_stop'])*(1-o['fstop']), 1e-10)
    print()

print("=== C1(c): da/dt = +a at the weld (numeric, own flow) ===")
g, c = ICS['M1']
sol, _ = run_flow(g, c)
def dens_at(t):
    z = sol.sol(t)
    X, Xt = z[0:4], z[4:8]
    P, _ = P_and_grad(X, QDEF)
    return np.exp(-t)*(0.25*(Xt*Xt).sum() + P)
for h in (1e-4, 1e-5, 1e-6):
    da = (dens_at(h) - dens_at(0.0))/h  # one-sided into the cell
    a0 = (g*g + c*c)/4
    print(f"  h={h:.0e}: (da/dt)/a(0) = {da/a0:.8f}  (claim: 1)")

print("\n=== C1(d): MS-aspect Taylor at the weld, BOTH sides ===")
# interior side: dense flow; exterior side: integrate the SAME reduced EL
# backward in t (the in-class C1 continuation)
def rhs8(t, z):
    X, Xt = z[0:4], z[4:8]
    _, gP = P_and_grad(X, QDEF)
    return np.concatenate([Xt, Xt + 2.0*gP])
z0 = np.zeros(8); z0[0] = 1.0; z0[4] = g; z0[5] = -c
solb = solve_ivp(rhs8, (0.0, -0.4), z0, method='DOP853', rtol=1e-12,
                 atol=1e-14, dense_output=True, max_step=0.02)
def m_of_t(tv, sol_, proj):
    z = sol_.sol(tv)
    yv = np.exp(-tv)
    fv = float(z[0:4] @ proj)
    return yv/2*(1-fv), yv
p_w = np.array([g/2, -c/2, 0, 0])
for nm, proj in (("M0 (monopole)", np.array([1.0, 0, 0, 0])),
                 ("m_pole (u=+1)", Y1P)):
    pred1 = float(p_w @ (proj if nm.startswith('m_pole') else
                  np.array([1.0, 0, 0, 0])))
    # build two-sided samples in y around 1
    ts = np.linspace(-0.3, 0.0, 31)[:-1]
    ti = np.linspace(0.0, 0.3, 31)
    ys, ms = [], []
    for tv in ts:
        m, yv = m_of_t(tv, solb, proj); ys.append(yv); ms.append(m)
    for tv in ti:
        m, yv = m_of_t(tv, sol, proj); ys.append(yv); ms.append(m)
    ys = np.array(ys); ms = np.array(ms)
    dy = ys - 1
    # two-sided cubic fit
    Amat = np.vstack([dy, dy**2, dy**3, dy**4]).T
    coef, *_ = np.linalg.lstsq(Amat, ms, rcond=None)
    print(f"  {nm} TWO-SIDED fit: m'(1)={coef[0]:+.8f} (jet pred "
          f"{pred1 if not nm.startswith('m_pole') else float(p_w@Y1P):+.8f})"
          f"  m''(1)/2={coef[1]:+.6f} (pred 0)  m'''(1)/6={coef[2]:+.4f}")
    # one-sided quadratic coefficient estimates via 2nd difference
    for side, sol_, tt in (("interior", sol, +1e-3), ("exterior", solb, -1e-3)):
        m1, y1 = m_of_t(tt, sol_, proj)
        m2, y2 = m_of_t(2*tt, sol_, proj)
        s1 = float(p_w @ (Y1P if nm.startswith('m_pole') else
                          np.array([1.0, 0, 0, 0])))
        # m ~ s1 dy + q2 dy^2: q2 = (m - s1 dy)/dy^2
        q2a = (m1 - s1*(y1-1))/(y1-1)**2
        q2b = (m2 - s1*(y2-1))/(y2-1)**2
        # Richardson toward dy->0 (cubic contamination): q2 ~ q + r*dy
        q2 = (q2a*(y2-1) - q2b*(y1-1))/((y2-1) - (y1-1))
        print(f"     {side}: m''(1)/2 -> {q2:+.6f} (pred 0)")

print("\n=== C3(a): deep-cell closure M0_seal ~ -p_F(seal) + O(y_s) ===")
for tag in ('M1', 'M4'):
    g2, c2 = ICS[tag]
    o = measure(g2, c2, label=tag)
    print(f"  {tag}: M0_seal {o['M0_seal']:+.6f}  -p_F(seal) "
          f"{-o['p_seal'][0]:+.6f}  diff {o['M0_seal']+o['p_seal'][0]:+.6f}"
          f"  y_s/2 = {o['y_seal']/2:.6f}  y_s*(1+g)/2={o['y_seal']*(1+g2)/2:.6f}")

print(f"\nTOTALS: PASS {npass} / {npass+nfail}")
