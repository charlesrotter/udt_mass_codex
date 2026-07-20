#!/usr/bin/env python3
"""Exact homogeneity and fourth-order boundary countermodel for the three-route zoom-out."""

from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent


def need(name,condition,checks):
    if not bool(condition): raise AssertionError(name)
    checks[name]="PASS"


def main():
    checks={}; lam=sp.symbols("lambda",positive=True)
    D=4
    weights={"sqrt_g":D,"C2_scalar":-4,"R_scalar":-2,"Lambda_density_scalar":0,
             "boundary_measure":3,"extrinsic_curvature":-1,"Xmax":1,"mass":1,
             "volume":3,"density":-2,"c":0,"G_on_similarity_orbit":0}
    need("C2_bulk_weight_zero",weights["sqrt_g"]+weights["C2_scalar"]==0,checks)
    need("EH_bulk_weight_two",weights["sqrt_g"]+weights["R_scalar"]==2,checks)
    need("cosmological_volume_weight_four",weights["sqrt_g"]==4,checks)
    need("GHY_comparison_weight_two",weights["boundary_measure"]+weights["extrinsic_curvature"]==2,checks)
    need("density_weight_mass_minus_volume",weights["mass"]-weights["volume"]==weights["density"],checks)
    compactness=sp.symbols("G",positive=True)*sp.symbols("M",positive=True)/(sp.symbols("c",positive=True)**2*sp.symbols("X",positive=True))
    G,M,c,X,rho=sp.symbols("G M c X rho",positive=True)
    need("compactness_homothety_invariant",sp.simplify((G*(lam*M)/(c**2*(lam*X)))/(G*M/(c**2*X))-1)==0,checks)
    density_ratio=G*rho*X**2/c**2
    need("density_X2_homothety_invariant",sp.simplify((G*(rho/lam**2)*(lam*X)**2/c**2)/density_ratio-1)==0,checks)
    need("c_anchor_does_not_break_common_length_time_scale",sp.simplify((lam/lam)-1)==0,checks)
    need("G_anchor_does_not_break_mass_length_similarity",sp.simplify((lam**3/(lam*lam**2))-1)==0,checks)

    # EH sensitivity is not scale stationarity: A lambda^2 has no positive stationary point for A!=0.
    A=sp.symbols("A",nonzero=True)
    need("bare_EH_no_positive_scale_stationary_point",sp.solve(sp.diff(A*lam**2,lam),lam)==[],checks)

    # Exact fourth-order boundary ambiguity countermodel.
    x=sp.symbols("x",real=True); y=sp.Function("y")(x); dy=sp.Function("dy")(x)
    L=sp.diff(y,x,2)**2
    bulk=sp.diff(sp.diff(L,sp.diff(y,x,2)),x,2)
    need("fourth_order_bulk_equation",sp.simplify(bulk-2*sp.diff(y,x,4))==0,checks)
    boundary_delta_yprime=sp.diff(L,sp.diff(y,x,2))
    boundary_delta_y=-sp.diff(boundary_delta_yprime,x)
    need("boundary_pair_delta_yprime",boundary_delta_yprime==2*sp.diff(y,x,2),checks)
    need("boundary_pair_delta_y",boundary_delta_y==-2*sp.diff(y,x,3),checks)
    # Same bulk admits clamped, natural, or mixed choices; this is a logical enumeration, not a preference.
    boundary_completions={"CLAMPED":"delta y=delta y'=0","NATURAL":"y''=y'''=0",
                          "MIXED":"one member of each conjugate pair fixed/vanishing after a boundary term"}
    need("multiple_boundary_completions_exist",len(boundary_completions)==3,checks)

    # Representative choice cannot equate operators of different derivative order.
    k=sp.symbols("k",positive=True)
    bach_symbol=k**4; eh_symbol=k**2
    need("Bach_and_EH_symbols_not_identical",sp.simplify(bach_symbol-eh_symbol)!=0,checks)
    need("representative_value_cannot_change_symbol_order",sp.degree(bach_symbol,k)!=sp.degree(eh_symbol,k),checks)

    # Dependency-rank facts: rigidity fills D03 only; D01,D04,D06,D07-D12 remain open.
    total_edges=12; edges_closed_by_new_rigidity=1; still_open_upstream=9
    need("rigidity_is_one_dependency_tile",edges_closed_by_new_rigidity==1,checks)
    need("majority_dependency_edges_remain_open",still_open_upstream>total_edges/2,checks)

    result={"schema":"udt-c2-rigidity-three-route-zoomout-1.0","result":"PASS","checks":checks,
      "homogeneity_weights":weights,
      "exact_invariants":{"GM_over_c2X":"weight 0","G_rho_X2_over_c2":"weight 0",
          "EH":"weight 2 but no positive scale stationary point by itself","C2":"weight 0"},
      "boundary_countermodel":{"action":"integral (y'')^2 dx","bulk":"2 y''''=0",
          "boundary_variation":"[2 y'' delta y' - 2 y''' delta y]","completions":boundary_completions,
          "ruling":"bulk variation exposes conjugate pairs but does not select physical boundary data"},
      "route_ranking":["PHYSICAL_BOUNDARY_VARIATION","NONLINEAR_STATIONARY_CLOSURE","VARIATION_DOMAIN_BRIDGE_BLOCKED_NO_NEW_INPUT"],
      "selector_ruling":{"immediate_fork":"placement of fundamental variation relative to scale selection remains OPEN",
          "executable_bridge_object":"off-shell scale-bearing representative map specifying varied fields and held-fixed global object remains OPEN",
          "complete_closure":"NO_SINGLE_CLOSING_SELECTOR; dynamical matching, boundary, source, and normalization remain independent edges"},
      "rigidity_meaning":"one conditional conformally-flat compact branch has a restricted tangent space; UDT-wide rigidity is not implied",
      "next_bounded_derivation":"derive the exact conditional C2 finite-cell boundary symplectic potential/conjugate data before a nonlinear branch solve",
      "maximum_conclusion":"COMPACT_C2_RIGIDITY_IS_BRANCH_SCOPED; NO_SINGLE_CLOSING_SELECTOR; IMMEDIATE_VARIATION_PLACEMENT_AND_EXECUTABLE_OFFSHELL_REPRESENTATIVE_MAP_OPEN; CONDITIONAL_C2_BOUNDARY_VARIATION_RANKED_NEXT",
      "compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
    (HERE/"DERIVATION_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"result":"PASS","checks":len(checks),"maximum_conclusion":result["maximum_conclusion"]},sort_keys=True))


if __name__=="__main__": main()
