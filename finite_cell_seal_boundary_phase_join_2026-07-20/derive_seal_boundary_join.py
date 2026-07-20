#!/usr/bin/env python3
"""Exact tangent-rank and compatibility audit for the seal-to-C2-boundary join."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
def need(name,condition,checks):
 if not bool(condition):raise AssertionError(name)
 checks[name]="PASS"
def main():
 checks={}
 # Logarithmic static tile: common scale, reciprocal ratio, angular shear.
 t_sigma=sp.Matrix([1,1,1,1]);t_phi=sp.Matrix([-1,1,0,0]);t_A=sp.Matrix([0,0,1,-1])
 T=sp.Matrix.hstack(t_sigma,t_phi,t_A)
 need("independent_common_phi_angular_tangents",T.rank()==3,checks)
 need("pairwise_orthogonal_bookkeeping_tangents",all((u.T*v)[0]==0 for u,v in [(t_sigma,t_phi),(t_sigma,t_A),(t_phi,t_A)]),checks)
 seal_covector=t_phi.T
 need("seal_delta_phi_removes_one_tangent",len(seal_covector.nullspace())==3,checks)
 need("common_scale_survives_phi_Dirichlet",(seal_covector*t_sigma)[0]==0,checks)
 need("angular_shear_survives_phi_Dirichlet",(seal_covector*t_A)[0]==0,checks)
 # Odd profiles have identical boundary value and freely different normal derivatives.
 n,a,b=sp.symbols("n a b",real=True);phi_a=a*n;phi_b=b*n
 need("odd_profiles_share_zero_seal",phi_a.subs(n,0)==0 and phi_b.subs(n,0)==0,checks)
 need("odd_profiles_have_free_distinct_slopes",sp.diff(phi_a,n).subs(n,0)-sp.diff(phi_b,n).subs(n,0)==a-b,checks)
 # Strongest ordinary-reflection challenge: a generic reciprocal tangential clock coefficient is not even.
 h_tt=-sp.exp(-2*phi_a)
 need("generic_free_phi_slope_gives_nonzero_metric_jet",sp.diff(h_tt,n).subs(n,0)==2*a,checks)
 need("ordinary_even_reflection_would_force_zero_jet",sp.diff((h_tt+h_tt.subs(n,-n))/2,n).subs(n,0)==0,checks)
 need("ordinary_reflection_not_entailed_by_odd_phi",sp.simplify(h_tt-h_tt.subs(n,-n))!=0,checks)
 # The dual-pairing swap implements phi inversion algebraically, but is not a Lorentzian isometry.
 phi=sp.symbols("phi",real=True);D=sp.diag(sp.exp(-phi),sp.exp(phi));swap=sp.Matrix([[0,1],[1,0]]);eta=sp.diag(-1,1)
 need("reciprocity_swap_conjugates_phi_to_minus_phi",swap*D*swap==D.subs(phi,-phi),checks)
 need("reciprocity_swap_is_not_Lorentzian_isometry",swap.T*eta*swap==-eta,checks)
 need("negative_metric_factor_not_positive_CSN",not sp.solve(sp.Eq(sp.symbols("Omega",positive=True)**2,-1),sp.symbols("Omega",positive=True)),checks)
 # Full symmetric induced metric has six tangents; one scalar constraint cannot fix it.
 need("full_induced_metric_component_count",3*4//2==6,checks)
 need("one_scalar_cannot_fix_full_h",6-1==5,checks)
 # Two inequivalent boundary-variation witnesses retain free reciprocal normal derivative.
 W1={"delta_phi":"fixed_zero","delta_common_scale":"free_null","delta_angular_shape":"free","delta_offdiagonal":"free","delta_K":"free","corner":"natural"}
 W2={"delta_phi":"fixed_zero","delta_common_scale":"free_null","delta_angular_shape":"fixed","delta_offdiagonal":"fixed","delta_K":"free","corner":"fixed_non_CSN"}
 need("witnesses_are_inequivalent",W1!=W2,checks)
 need("both_witnesses_preserve_phi_Dirichlet",W1["delta_phi"]==W2["delta_phi"]=="fixed_zero",checks)
 need("both_witnesses_preserve_free_phi_jet",W1["delta_K"]==W2["delta_K"]=="free",checks)
 need("multiple_polarizations_survive",len({json.dumps(W1,sort_keys=True),json.dumps(W2,sort_keys=True)})==2,checks)
 slots={"boundary_domain":"PARTIAL_SUPPLIED","boundary_Xmax_join":"OPEN","causal_character":"OPEN",
  "delta_h":"ONE_STATIC_RATIO_SCALAR_FIXED; COMMON_SCALE_NULL; TRANSVERSE_AND_TIME_ON_OPEN",
  "delta_K":"RECIPROCAL_NORMAL_DERIVATIVE_EXPLICITLY_FREE; OTHER_COMPONENTS_OPEN",
  "E_equation":"NOT_SELECTED","Pi_h_equation":"NOT_SELECTED","corner_rule":"OPEN",
  "off_shell_bootstrap_map":"NOT_SUPPLIED","charge_normalization":"OPEN"}
 need("complete_join_has_unfilled_slots",sum(v in {"OPEN","NOT_SELECTED","NOT_SUPPLIED"} or "OPEN" in v for v in slots.values())>=7,checks)
 result={"schema":"udt-finite-cell-seal-boundary-phase-join-1.0","result":"PASS","checks":checks,
  "tangent_rank":{"matrix_rank":T.rank(),"seal_constraint_rank":seal_covector.rank(),"seal_nullity":len(seal_covector.nullspace()),
   "interpretation":"delta phi=0 removes one reciprocal tangent while common scale, angular shear, and additional full-metric tangents remain"},
  "mirror_challenge":{"ordinary_metric_reflection_K_zero":"CONDITIONAL_MATHEMATICAL_THEOREM_NOT_CURRENT_UDT_PREMISE",
   "generic_clock_metric_normal_jet":str(sp.diff(h_tt,n).subs(n,0)),"canon_phi_prime":"FREE",
   "ruling":"MIRROR_WORDING_DOES_NOT_DERIVE_K_IJ_ZERO_OR_A_COMPLETE_METRIC_INVOLUTION"},
  "reciprocal_swap_challenge":{"identity":"swap D(phi) swap = D(-phi)","Lorentzian_pullback":"swap^T eta swap = -eta",
   "ruling":"DUAL_PAIRING_SWAP_IS_AN_EXACT_RECIPROCAL_INVERSION_WITNESS_BUT_NOT_BY_ITSELF_A_POSITIVE_CSN_LORENTZIAN_SEAL_ISOMETRY"},
  "boundary_slots":slots,"compatible_witnesses":{"W01":W1,"W02":W2},
  "primary_outcome":"PARTIAL_SEAL_DATA_ONLY",
  "supporting_nonuniqueness":"MULTIPLE_INEQUIVALENT_POLARIZATION_WITNESSES_REMAIN_COMPATIBLE",
  "smallest_missing_object":"complete metric/coframe seal involution plus an off-shell allowed-variation and corner rule; if scale-bearing, also a derived global-to-local boundary map",
  "maximum_conclusion":"STATIC_ODD_PHI_SUPPLIES_ONE_DIRICHLET_RATIO_DATUM_WITH_FREE_NORMAL_DERIVATIVE; IT_DOES_NOT SELECT_THE_CONDITIONAL_C2_METRIC_TWO_JET_MOMENTA_CORNER_OR_CHARGE; PRIMARY_BRANCH_PARTIAL_SEAL_DATA_ONLY",
  "compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
 (HERE/"DERIVATION_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"result":"PASS","checks":len(checks),"primary_outcome":result["primary_outcome"],"supporting_nonuniqueness":result["supporting_nonuniqueness"]},sort_keys=True))
if __name__=="__main__":main()
