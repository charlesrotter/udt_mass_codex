# ADVERSARIAL REVIEW 1 — part 2: the budget-infimum construction (inf = 0),
# the protective full-budget bound, inclusion-chain generality, missing-class probes.
# Fresh code; no probe code imported. Reviewer: Claude (Fable 5), 2026-08-07.
import mpmath as mp

mp.mp.dps = 60
ETA = mp.matrix([[-1, 0], [0, 1]])


def D(d):
    return mp.matrix([[mp.e**(-d), 0], [0, mp.e**d]])


def B(w):
    return mp.matrix([[mp.cosh(w), mp.sinh(w)], [mp.sinh(w), mp.cosh(w)]])


def strain(M):
    return ETA * M.T * ETA * M


def depth_and_label(M):
    """lambda_t (small strain eigenvalue), its depth, and eta-causal label of its eigline."""
    C = strain(M)
    lam, V = mp.eig(mp.matrix(C))
    lams = [l.real for l in lam]
    if any(abs(l.imag) > mp.mpf('1e-40') for l in lam):
        return None, None, 'COMPLEX'  # off regular stratum
    i_min = lams.index(min(lams))
    v = mp.matrix([V[0, i_min], V[1, i_min]])
    sig = (-v[0].real**2 + v[1].real**2)
    label = 'timelike' if sig < 0 else 'spacelike'
    lam_t = min(lams)
    return lam_t, -mp.log(lam_t) / 2, label


print("=== BUDGET INFIMUM: greedy chain, total depth budget -> 0 ===")
for budget in ['0.1', '0.01', '0.001']:
    b = mp.mpf(budget)
    legs_depth = [b / 2**k for k in range(1, 11)]  # sum < b
    M = D(legs_depth[0])
    used = legs_depth[0]
    twist_total = mp.mpf(0)
    ok = True
    hist = []
    lam_t, dep, lab = depth_and_label(M)
    for epsk in legs_depth[1:]:
        # append twisted tiny leg B(w) D(epsk) B(-w); grow w until depth gains >= 1
        target = dep + 1
        w = mp.mpf(1)
        for _ in range(400):
            Mtry = B(w) * D(epsk) * B(-w) * M
            lam2, dep2, lab2 = depth_and_label(Mtry)
            if lab2 == 'timelike' and dep2 is not None and dep2 >= target:
                break
            w = w * mp.mpf('1.3')
        M = Mtry
        used += epsk
        twist_total += w
        lam_t, dep, lab = lam2, dep2, lab2
        if lab != 'timelike':
            ok = False
        hist.append((float(dep), float(lam_t)))
    print(f"budget {budget}: total depth used = {mp.nstr(used, 8)}, "
          f"final lambda_t = {mp.nstr(lam_t, 3)}, final depth = {mp.nstr(dep, 6)}, "
          f"all truncations timelike-labeled = {ok}")
    print(f"   truncation depths: {[round(h[0], 2) for h in hist]}")
print("=> chains with TOTAL DEPTH BUDGET <= any epsilon accumulate to the wall: inf = 0.")
print("   (Boost legs are zero-depth isometries: strain = I, verified in part 1.)")

print()
print("=== PROTECTIVE FULL BUDGET: depth_comp <= sum(|d_i|) + sum(|w_i|) ===")
# operator-norm bound: lambda_max(C) <= sigma_max(M)^2 and log sigma_max subadditive.
import random
random.seed(7)
viol = 0
for trial in range(200):
    nlegs = random.randint(2, 6)
    M = mp.eye(2)
    full = mp.mpf(0)
    for _ in range(nlegs):
        d = mp.mpf(random.uniform(0.01, 1.5))
        wv = mp.mpf(random.uniform(-3, 3))
        M = B(wv) * D(d) * B(-wv) * M
        full += abs(d) + 2 * abs(wv)   # each twisted leg = B(w)[0-depth] D(d) B(-w)[0-depth]
    lam_t, dep, lab = depth_and_label(M)
    if lab == 'timelike' and dep is not None and dep > full + mp.mpf('1e-30'):
        viol += 1
print(f"violations of depth <= full(depth+twist)-budget over 200 random chains: {viol}")
print("=> a budget that also charges non-compact twist rapidity IS wall-protective")
print("   (accumulation to the wall forces total full-budget -> oo).")

print()
print("=== INCLUSION CHAIN generality: non-class oscillatory profile ===")
# A(u) = u^{3/2} * (2+sin(1/u))/3 : not in classes (i)-(iii). n_eff=3/2:
# optical should DIVERGE (>= u^{-3/2}/3 integrand), proper CONVERGE (<= sqrt(3) u^{-3/4}).
f_prop = lambda uu: (uu**mp.mpf(1.5) * (2 + mp.sin(1/uu)) / 3)**mp.mpf(-0.5)
prop_tail = mp.quad(f_prop, [mp.mpf('1e-8'), mp.mpf('1e-4'), 1])
print("proper integral (u in [1e-8,1]) converged value ~", mp.nstr(prop_tail, 6))
opt_partial = []
for lo in ['1e-2', '1e-4', '1e-6']:
    f_opt = lambda uu: 1 / (uu**mp.mpf(1.5) * (2 + mp.sin(1/uu)) / 3)
    opt_partial.append(mp.quad(f_opt, [mp.mpf(lo), 1]))
print("optical partials as cutoff->0:", [mp.nstr(x, 4) for x in opt_partial], "(diverging)")
print("=> matches the GENERAL theorem: A->0 gives A<1 near wall, so")
print("   1/A > 1/sqrt(A) > 1: optical-finite => proper-finite => chart/areal-finite,")
print("   for EVERY A->0 profile (not only classes (i)-(iii)); converses fail (n=3/2, n=3).")

print()
print("=== MISSING-CLASS probe: wall at infinite radius with POWER-LAW decay ===")
# class (ii') A = r^-alpha (r>=1): all class-(ii) column entries persist EXCEPT the
# d_A variant r/(1+z) = r sqrt(A) = r^(1-alpha/2): -> oo (alpha<2), 1 (alpha=2), 0 (alpha>2)
for alpha in [1, 2, 3]:
    print(f"alpha={alpha}: r*sqrt(A) = r^{1 - alpha / 2} as r->oo ->",
          "oo" if alpha < 2 else ("finite const" if alpha == 2 else "0"))
print("proper/optical/areal/z/d_L/d_A=r all still DIVERGENT for any alpha>0 (A<=1 near wall,")
print("integrands >= 1 over infinite range); infall also divergent (dr/dtau -> c*e, infinite range).")
