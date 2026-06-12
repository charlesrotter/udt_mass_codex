"""Monopole gauged-Laplacian on S^2: rigorous lowest-eigenvalue scan.

Operator per m-sector (north gauge A = qm(1-cos th) dphi):
  L g = -g'' - cot(th) g' + (m - qm(1-cos th))^2/sin^2(th) g = lam g

Frobenius exponents: g ~ th^{|m|} at th=0, g ~ (pi-th)^{|m-2qm|} at th=pi.
Two-sided shooting with regular series starts; eigenvalue = root of the
log-derivative mismatch at th=pi/2. Scan m in [-2..4], find the lowest
eigenvalue per sector, report global minimum and degeneracy.
"""
import mpmath as mp

mp.mp.dps = 25


def mismatch(lam, mval, qm):
    alpha = abs(mval)               # exponent at 0
    beta_ = abs(mval - 2 * qm)      # exponent at pi

    def Wfun(th):
        return (mval - qm * (1 - mp.cos(th)))**2 / mp.sin(th)**2

    eps = mp.mpf('1e-4')

    # left start: g = th^alpha (1 + c2 th^2), derivative numeric from series
    def gl0(th):
        return th**alpha

    # use small-step numeric ODE from eps with series init (leading order
    # suffices at eps=1e-4 for ~8 digits; refine with Richardson below)
    def shoot(side):
        if side == 'L':
            t0 = eps
            g0 = gl0(t0)
            dg0 = alpha * t0**(alpha - 1) if alpha > 0 else mp.mpf(0)
        else:
            t0 = mp.pi - eps
            g0 = eps**beta_
            dg0 = -(beta_ * eps**(beta_ - 1)) if beta_ > 0 else mp.mpf(0)

        def rhs(th, w):
            return [w[1], (Wfun(th) - lam) * w[0]
                    - mp.cos(th) / mp.sin(th) * w[1]]
        f = mp.odefun(rhs, t0, [g0, dg0], tol=1e-18)
        g, dg = f(mp.pi / 2)
        return dg / g

    return shoot('L') - shoot('R')


def lowest(mval, qm, lo=mp.mpf('0.05'), hi=mp.mpf('6.0'), ngrid=60):
    vals = []
    lams = [lo + (hi - lo) * k / ngrid for k in range(ngrid + 1)]
    prev = None
    roots = []
    for lv in lams:
        cur = mismatch(lv, mval, qm)
        if prev is not None and mp.sign(cur) != mp.sign(prev) \
                and abs(cur) < 1e3 and abs(prev) < 1e3:
            root = mp.findroot(lambda L: mismatch(L, mval, qm),
                               (lams[lams.index(lv) - 1], lv),
                               solver='bisect', tol=1e-12)
            roots.append(root)
            if len(roots) >= 1:
                break
        prev = cur
    return roots[0] if roots else None


for n in (1, 2):
    qm = mp.mpf(n) / 2
    expect = qm * (qm + 1) - qm**2  # j(j+1)-(n/2)^2 at j=n/2
    res = {}
    for mval in range(-2, 5):
        r = lowest(mval, qm)
        res[mval] = r
        print(f"n={n} m={mval:+d}: lowest lam = "
              f"{mp.nstr(r, 10) if r is not None else 'none<6'}")
    finite = [v for v in res.values() if v is not None]
    gmin = min(finite)
    deg = sum(1 for v in finite if abs(v - expect) < 1e-6)
    ok1 = abs(gmin - expect) < 1e-6
    ok2 = deg == n + 1
    print(f"n={n}: global min = {mp.nstr(gmin, 12)} expect {mp.nstr(expect,6)}"
          f" -> {'PASS' if ok1 else 'FAIL'}; degeneracy {deg} "
          f"(expect {n + 1}) -> {'PASS' if ok2 else 'FAIL'}")
