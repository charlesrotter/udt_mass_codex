"""Vβ-4: spot-check the numerical residual JSON."""
import json
with open("/home/udt-admin/UDT/dispatch_S67_004_ponder/outputs/numerical_residual_verification.json") as f:
    data = json.load(f)

print(f"Verdict: {data['verdict']}")
print(f"Aggregate: {json.dumps(data['aggregate'], indent=2)}")
print()
print("Per-profile/mode canonical-window data:")
for pname, pres in data["profiles"].items():
    print(f"\n{pname}: dphi_full = {pres['delta_phi_full']:.4f}, n_modes = {pres['n_modes_found']}")
    for tag, mdata in pres["modes"].items():
        E_ = mdata["E_pick"]
        w = mdata["windows"].get("canonical")
        if w:
            alpha = w["fit_alpha"]
            swing = w["U_log_swing"]
            bound = w["IBP_bound_log_swing"]
            ratio = w["obs_log_swing_over_bound"]
            holds = w["bound_holds_at_log_swing"]
            kdr = w["k_max_times_dr"]
            print(f"  {tag:5s} E={E_:8.3f}  alpha={alpha:+7.4f}  swing={swing:.3e}  bound={bound:.3e}  obs/bound={ratio:.3f}  holds={holds}  k*dr={kdr:.3f}")
