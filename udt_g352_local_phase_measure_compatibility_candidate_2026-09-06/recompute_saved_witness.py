#!/usr/bin/env python3
"""Same-context, implementation-distinct finite recomputation from saved inputs.

Stdlib rational arithmetic only; no import of check_witnesses or SymPy.
This is not an independent reviewer or an independent proof of the general claim.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    saved_path = HERE / "CHECK_RESULT.json"
    raw = saved_path.read_bytes()
    saved = json.loads(raw)
    witness = saved["saved_spherical_witness"]
    assert witness["metric"] == "diag(-1,1,r^2,r^2 sin(angle)^2)"
    covector = list(map(Q, witness["phase_covector_tr"]))
    radii = list(map(Q, witness["radii"]))
    observers = [list(map(Q, pair)) for pair in witness["observers_tr"]]
    frequencies, areas = [], []
    for radius, observer in zip(radii, observers):
        ut, ur = observer
        assert ut > 0 and -ut*ut + ur*ur == -1
        frequencies.append(-sum(u*b for u, b in zip(observer, covector)))
        # At an equatorial label, Cartesian tangent vectors to r*n(a,b)
        # are (0,0,-r) and (0,r,0); the Euclidean cross product has norm r^2.
        tangent_a, tangent_b = (0, 0, -radius), (0, radius, 0)
        cross = [tangent_a[1]*tangent_b[2] - tangent_a[2]*tangent_b[1],
                 tangent_a[2]*tangent_b[0] - tangent_a[0]*tangent_b[2],
                 tangent_a[0]*tangent_b[1] - tangent_a[1]*tangent_b[0]]
        areas.append(abs(cross[0]))
        assert cross[1:] == [0, 0]
    assert frequencies == list(map(Q, witness["omega"]))
    assert areas == list(map(Q, witness["J"]))
    # Unit label amount and unit phase spacing for this arithmetic control.
    # Counts per time divided by directly computed Cartesian area.
    direct_rates = [freq/area for freq, area in zip(frequencies, areas)]
    transfer = direct_rates[1]/direct_rates[0]
    assert direct_rates == list(map(Q, witness["Gamma_coefficients_for_density_over_spacing"]))
    assert transfer == Q(witness["transfer"]) == Q(2, 9)

    # d(x^2/2+x/2)/dx=x+1/2: separate rational evaluation of saved profile.
    assert witness["measure_profile"] == "x+1/2"
    def antiderivative(x):
        return x*x/2 + x/2
    half_mass = antiderivative(Q(1, 2)) - antiderivative(Q(0))
    assert half_mass == Q(witness["profile_left_half_mass"]) == Q(3, 8)
    assert antiderivative(Q(1)) == 1 and half_mass != Q(1, 2)

    # Separate hand-differentiated z=0 control for beta wedge dbeta:
    # beta=(-1,cos z,sin z,0); beta(z=0)=(-1,1,0,0), d_z beta=(0,0,1,0).
    beta, dz_beta = (-1, 1, 0, 0), (0, 0, 1, 0)
    db_yz, db_xz, db_xy = -dz_beta[2], -dz_beta[1], 0
    wedge_xyz = beta[1]*db_yz - beta[2]*db_xz + beta[3]*db_xy
    assert wedge_xyz == Q(saved["checks"]["twist_wedge_123"]["actual"]) == -1

    result = {
        "status": "PASS_SAVED_INPUT_EXACT_RECOMPUTATION__SAME_CONTEXT",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "J_from_cartesian_cross_product": list(map(str, areas)),
        "omega_from_rational_contraction": list(map(str, frequencies)),
        "direct_rates_for_unit_density_and_spacing": list(map(str, direct_rates)),
        "direct_transfer": str(transfer), "profile_left_half_mass": str(half_mass),
        "twist_xyz_at_z0": wedge_xyz,
        "limits": ["Same context, fully exposed to argument/code/results",
                   "Implementation-distinct finite rational anchors, not independent science",
                   "No general Frobenius, global geometry or physical realization certified"],
    }
    (HERE / "RECOMPUTATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("PASS: saved-input rational recomputation; Cartesian areas=(4,9), frequencies=(1,1/2), transfer=2/9")
    print("PASS: equal-total profile has half-patch mass 3/8, not 1/2; twisting control wedge_xyz=-1 at z=0")
    print("SAME CONTEXT: no independent-review claim")


if __name__ == "__main__":
    main()
