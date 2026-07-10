"""H4 N4rev: run the corrected+MMS-validated turnkey pipeline on the REAL H3 shell-projected
stress. Certifies the SIGN of dm (=-dq) [Zf-independent] + the far-field regime vs crit=1/2 ln(32/Zf).
Data-blind; no labels/masses; native 2K->phi only. model_stress() NOT used."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/home/udt-admin/udt_mass_codex')          # turnkey at repo root
sys.path.insert(0, '/home/udt-admin/udt_mass_codex/h4_scripts')
from n4rev_response_TURNKEY import run, mms_Lphi

# ---- load REAL shell-projected transverse stress from the H3 Q_H=1 field ----
D = np.load('/home/udt-admin/udt_mass_codex/h4_scripts/stress_rtheta_h3.npz')
rc = D['rc']; thc = D['thc']; Ttt = D['Tthth']; Tpp = D['Tphph']    # (nr,nth)
w = np.sin(thc)
def shellavg(fld_rt): return (fld_rt * w[None, :]).sum(1) / w.sum()  # sin-weighted theta avg -> 1D
Tthth0 = shellavg(Ttt); Tphph0 = shellavg(Tpp)

# trim to the halo/far-field window r in [0.3, 6.0] (avoid the /r^4 core singularity in the flux density;
# the far-field flux + monopole is what CF2 reads). r>0 keeps L_bare well-posed (roots {1,2}).
sel = (rc >= 0.3) & (rc <= 6.0)
r = rc[sel]; Tthth0 = Tthth0[sel]; Tphph0 = Tphph0[sel]
def si(f): return 4 * np.pi * np.trapezoid(r**2 * f, r)
print(f"REAL stress on r in [{r[0]:.3f},{r[-1]:.3f}] (n={len(r)}): "
      f"trace int={si(Tthth0+Tphph0):+.2f} shear int={si(Tthth0-Tphph0):+.2f}")

print("\n### MMS re-validation of the S3 screened-phi stage (expect rate ~4) ###")
mms_Lphi()

print("\n### SIGN CERTIFICATION (dm=-dq); dq sign is Zf-independent ###")
for Zf in (1.0, 8.0):
    # sign uses any phi_amb (S1/S2 do not depend on phi_amb); use a shallow default for the print
    dq, C1 = run(r=r, Tthth=Tthth0, Tphph=Tphph0, Zf=Zf, phi_amb=3.0)
    print(f"   -> Zf={Zf}: dq={dq:+.4e}  delta_m=-dq={-dq:+.4e}  "
          f"{'NEGATIVE-mass (FINDING)' if -dq < 0 else 'POSITIVE-mass'}\n")

print("### FAR-FIELD REGIME SWEEP vs crit=1/2 ln(32/Zf) ###")
for Zf in (1.0, 8.0):
    crit = 0.5 * np.log(32 / Zf)
    print(f"-- Zf={Zf}: crit={crit:.3f} (phi_amb<crit=SHALLOW/screened-oscillatory; >crit=DEEP/clean 1/r) --")
    for pa in (0.5, 1.0, 1.5, crit, 2.0, 3.0):
        dq, C1 = run(r=r, Tthth=Tthth0, Tphph=Tphph0, Zf=Zf, phi_amb=pa)
