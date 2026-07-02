"""Stage B analysis (no IVP shots): full per-rung table, integer census, same-sign-run
record, frozen fits F1/F2/F3 (d(N)) + G1/G2 (L(N)) with residual structure."""
import json
import numpy as np

SCR = "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad"
rj = json.load(open(f"{SCR}/stageB_rungs.json"))
sw = json.load(open(f"{SCR}/stageB_sweep.json"))
ab = json.load(open(f"{SCR}/stageB_above.json"))
rungs = rj["rungs"]

# ---------------- full per-rung table
print("=== BELOW-STUCK CONFIRMED RUNGS (A1 m=3 Z=8) ===")
hdr = ("N_d N_p  a*            d           q        rho_s    r_s        L_proper  chi      "
       "dphi      2m/rho(seal)  H_drift   floorrange_Nd        floorrange_Np")
print(hdr)
for r in rungs:
    fr_d = r["N_delta_floor_range"]; fr_p = r["N_rhop_floor_range"]
    print(f"{r['N_delta']:3d} {r['N_rhop']:3d}  {r['a_star']:.10f}  {r['d_star']:.6e}  "
          f"{r['q']:8.5f} {r['rho_s']:8.5f} {r['r_s']:10.4f} {r['L_proper']:9.4f} {r['chi']:8.4f} "
          f"{r['dphi_carried']:9.6f}  {r['ms_seal_2m_over_rho']:.10f}  {r['H_drift']:.1e}  "
          f"[{fr_d[0]:.1e},{fr_d[1]:.1e}]  [{fr_p[0]:.1e},{fr_p[1]:.1e}]")

# plateau spans in decades
print("\nplateau spans (decades) per rung: N_delta, N_rhop:")
for r in rungs:
    fd = r["N_delta_floor_range"]; fp = r["N_rhop_floor_range"]
    sd = abs(np.log10(fd[0]/fd[1])); sp = abs(np.log10(fp[0]/fp[1]))
    flag = "" if (sd >= 2 and sp >= 2) else "  <-- SPAN <2 DECADES"
    print(f"  N={r['N_delta']:2d}: {sd:.2f}, {sp:.2f}{flag}")

# recheck mismatches
mm = [r for r in rungs if r["N_delta"] != r["N_delta_recheck200k"] or r["N_rhop"] != r["N_rhop_recheck200k"]]
print(f"\n200k-recheck mismatches: {len(mm)}")
eq = [r for r in rungs if r["N_delta"] != r["N_rhop"]]
print(f"N_delta != N_rhop rungs: {len(eq)}")

# ---------------- integer census
Ns = [r["N_delta"] for r in rungs]
lo, hi = min(Ns), max(Ns)
present = sorted(set(Ns))
missing = [n for n in range(lo, hi + 1) if n not in Ns]
dupes = [n for n in present if Ns.count(n) > 1]
print(f"\n=== INTEGER CENSUS (confirmed below-stuck rungs) ===")
print(f"covered range: N = {lo}..{hi}")
print(f"present: {present}")
print(f"missing in range: {missing if missing else 'NONE'}")
print(f"duplicated N: {dupes if dupes else 'NONE'}")

# ---------------- same-sign runs between brackets (below-stuck sweep record)
rows = sorted(sw["rows"], key=lambda r: -r[0])
brs = sw["brackets"]
br_mid = [0.5 * (b[0] + b[1]) for b in brs]
print(f"\n=== SAME-SIGN RUN RECORD (below-stuck sweep, {len(rows)} pts, {len(brs)} brackets) ===")
# gaps between consecutive brackets measured in # of sampled points with no sign change
gaps = []
for (b1, b2) in zip(brs, brs[1:]):
    pts_between = [r for r in rows if b2[0] < r[0] < b1[1]]
    if len(pts_between) >= 2:
        gaps.append((b1[1], b2[0], len(pts_between)))
for g in sorted(gaps, key=lambda x: -x[2])[:15]:
    print(f"  same-sign run: d in ({g[1]:.4e}, {g[0]:.4e}), {g[2]} consecutive same-sign samples")

# ---------------- frozen fits
N = np.array([r["N_delta"] for r in rungs], float)
d = np.array([r["d_star"] for r in rungs], float)
L = np.array([r["L_proper"] for r in rungs], float)

def report(name, form, Nf, yf, pred, params):
    res = yf - pred
    rel = res / yf
    s = np.sign(res)
    flips = int(np.sum(s[1:] * s[:-1] < 0))
    runsig = "".join("+" if x > 0 else "-" for x in s)
    rms_rel = float(np.sqrt(np.mean(rel ** 2)))
    print(f"\n{name}: {form}")
    print(f"  params: {params}")
    print(f"  rel-RMS = {rms_rel:.3e}; residual signs ({len(s)} pts, {flips} flips): {runsig}")
    print(f"  max|rel res| = {np.max(np.abs(rel)):.3e} at N={Nf[np.argmax(np.abs(rel))]:.0f}")
    return rms_rel

m1 = N >= 1
print("\n=== FROZEN FITS: d(N) === (N=0 excluded from F1/F3 — form undefined at N=0; stated)")
# F1 power: log d = log C - p log N   (N>=1)
A = np.vstack([np.ones(m1.sum()), np.log(N[m1])]).T
c, presid, *_ = np.linalg.lstsq(A, np.log(d[m1]), rcond=None)
C1, p1 = np.exp(c[0]), -c[1]
report("F1", "d = C*N^-p (fit N=1..22)", N[m1], d[m1], C1 * N[m1] ** (-p1), f"C={C1:.6e}, p={p1:.6f}")

# F2 exponential: log d = log C - lam N  (all N incl 0)
A = np.vstack([np.ones(len(N)), N]).T
c, *_ = np.linalg.lstsq(A, np.log(d), rcond=None)
C2, lam = np.exp(c[0]), -c[1]
report("F2", "d = C*exp(-lam*N) (fit N=0..22)", N, d, C2 * np.exp(-lam * N), f"C={C2:.6e}, lam={lam:.6f}")
# F2 variant excluding N=0 (for symmetry of comparison, reported too)
A = np.vstack([np.ones(m1.sum()), N[m1]]).T
c, *_ = np.linalg.lstsq(A, np.log(d[m1]), rcond=None)
C2b, lamb = np.exp(c[0]), -c[1]
report("F2 (N>=1 subset)", "d = C*exp(-lam*N)", N[m1], d[m1], C2b * np.exp(-lamb * N[m1]),
       f"C={C2b:.6e}, lam={lamb:.6f}")

# F3 log form: log d = log C - p*log(log(N+1))  (N>=1; ln(0+1)=0 undefined)
A = np.vstack([np.ones(m1.sum()), np.log(np.log(N[m1] + 1.0))]).T
c, *_ = np.linalg.lstsq(A, np.log(d[m1]), rcond=None)
C3, p3 = np.exp(c[0]), -c[1]
report("F3", "d = C*(ln(N+1))^-p (fit N=1..22)", N[m1], d[m1], C3 * np.log(N[m1] + 1.0) ** (-p3),
       f"C={C3:.6e}, p={p3:.6f}")

print("\n=== FROZEN FITS: L(N) ===")
# G1 linear (all N)
A = np.vstack([np.ones(len(N)), N]).T
c, *_ = np.linalg.lstsq(A, L, rcond=None)
al, be = c
report("G1", "L = alpha + beta*N (fit N=0..22)", N, L, al + be * N, f"alpha={al:.6f}, beta={be:.6f}")

# G2 power (N>=1)
A = np.vstack([np.ones(m1.sum()), np.log(N[m1])]).T
c, *_ = np.linalg.lstsq(A, np.log(L[m1]), rcond=None)
Cg, pg = np.exp(c[0]), c[1]
report("G2", "L = C*N^p (fit N=1..22)", N[m1], L[m1], Cg * N[m1] ** pg, f"C={Cg:.6f}, p={pg:.6f}")

# successive spacing tables (raw, for the record)
print("\nraw d ratios d(N+1)/d(N):")
print("  " + " ".join(f"{d[i+1]/d[i]:.4f}" for i in range(len(d) - 1)))
print("raw L differences L(N+1)-L(N):")
print("  " + " ".join(f"{L[i+1]-L[i]:.4f}" for i in range(len(L) - 1)))

# ---------------- above-side rungs vs below ladder
print("\n=== ABOVE-STUCK RUNGS vs BELOW LADDER (same N) ===")
below_by_N = {r["N_delta"]: r for r in rungs}
for r in ab["rungs"]:
    nb = below_by_N.get(r["N_delta"])
    if nb:
        print(f"  N={r['N_delta']:2d}: above d'={r['dp_star']:.6e} a*={r['a_star']:.10f} "
              f"q={r['q']:.5f} rho_s={r['rho_s']:.5f} L={r['L_proper']:.4f} | "
              f"below d={nb['d_star']:.6e} a*={nb['a_star']:.10f} q={nb['q']:.5f} "
              f"rho_s={nb['rho_s']:.5f} L={nb['L_proper']:.4f}")
        print(f"        ratios above/below: d'/d={r['dp_star']/nb['d_star']:.5f} "
              f"q={r['q']/nb['q']:.5f} rho_s={r['rho_s']/nb['rho_s']:.5f} L={r['L_proper']/nb['L_proper']:.5f}")
