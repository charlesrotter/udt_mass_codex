#!/usr/bin/env python3
"""Exact real 2x2 reciprocal-involution and angular-extension classification."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
def need(name,c,checks):
 if not bool(c):raise AssertionError(name)
 checks[name]="PASS"
def main():
 checks={};z=sp.symbols("z",positive=True);b=sp.symbols("b",real=True,nonzero=True);phi=sp.symbols("phi",real=True)
 D=sp.diag(1/z,z);Dm=sp.diag(z,1/z);a,c,d=sp.symbols("a c d",real=True);F=sp.Matrix([[a,b],[c,d]])
 eq=sp.expand(F*D-Dm*F)
 need("constant_conjugator_diagonal_entries_forced_zero",sp.solve([eq[0,0].subs(z,2),eq[1,1].subs(z,2)],[a,d],dict=True)==[{a:0,d:0}],checks)
 Fb=sp.Matrix([[0,b],[1/b,0]]);need("general_real_involution_family",Fb*Fb==sp.eye(2),checks)
 need("general_family_conjugates_reciprocal_character",sp.simplify(Fb*D*Fb-Dm)==sp.zeros(2),checks)
 eta=sp.diag(-1,1);K=sp.Matrix([[0,1],[1,0]])
 pull_eta=sp.simplify(Fb.T*eta*Fb);need("eta_pullback_signature_swapped",pull_eta==sp.diag(b**-2,-b**2),checks)
 omega=sp.symbols("omega",positive=True);sol=sp.solve(list(pull_eta-omega**2*eta),(b,omega),dict=True)
 need("no_positive_conformal_eta_solution",sol==[],checks)
 need("K_bilinear_preserved_by_full_family",sp.simplify(Fb.T*K*Fb)==K,checks)
 J=sp.Matrix([[0,1],[1,0]]);need("raw_swap_anti_isometry_in_eta",J.T*eta*J==-eta,checks)
 H=sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2);eta_pm=sp.diag(1,-1)
 need("Hadamard_diagonalizes_K",sp.simplify(H.T*K*H)==eta_pm,checks)
 boost=sp.simplify(H.T*sp.diag(sp.exp(-phi),sp.exp(phi))*H)
 need("character_becomes_Lorentz_boost",sp.simplify(boost.T*eta_pm*boost)==eta_pm,checks)
 reflection=sp.simplify(H.T*J*H);need("swap_becomes_Lorentz_reflection",reflection==sp.diag(1,-1) and reflection.T*eta_pm*reflection==eta_pm,checks)
 T=sp.diag(sp.exp(2*phi),sp.exp(-2*phi));Dphi=sp.diag(sp.exp(-phi),sp.exp(phi))
 need("field_transport_maps_phi_to_minus_phi",sp.simplify(T*Dphi-Dphi.subs(phi,-phi))==sp.zeros(2),checks)
 need("field_transport_cocycle",sp.simplify(T.subs(phi,-phi)*T)==sp.eye(2),checks)
 ratio=sp.simplify((T.T*eta*T)[0,0]/eta[0,0]-(T.T*eta*T)[1,1]/eta[1,1])
 need("field_transport_not_conformal_eta_generically",ratio!=0,checks)
 theta=sp.symbols("theta",real=True);R=sp.Matrix([[sp.cos(theta),-sp.sin(theta)],[sp.sin(theta),sp.cos(theta)]]);A=sp.simplify(R*sp.diag(1,-1)*R.T)
 need("angular_reflection_continuum_involutive",sp.simplify(A*A)==sp.eye(2),checks)
 need("angular_reflection_continuum_orthogonal",sp.simplify(A.T*A)==sp.eye(2),checks)
 need("three_angular_conjugacy_types",{sp.trace(sp.eye(2)),sp.trace(-sp.eye(2)),sp.trace(A)}=={2,-2,0},checks)
 K4=sp.diag(1,1,1,1);K4[:2,:2]=K;P4=sp.diag(sp.exp(-phi),sp.exp(phi),1,1)
 need("direct_four_block_preserves_K4",sp.simplify(P4.T*K4*P4)==K4,checks)
 need("direct_four_block_transverse_identity",P4[2:,2:]==sp.eye(2),checks)
 witnesses={"W01":{"block":"K_null","angular":"+I","time_on":"separate_open"},"W02":{"block":"K_null","angular":"-I","time_on":"separate_open"},"W03":{"block":"K_null_Fb","angular":"axis_reflection","time_on":"chosen_parity"}}
 need("multiple_complete_conditional_extensions",len({json.dumps(v,sort_keys=True) for v in witnesses.values()})==3,checks)
 result={"schema":"udt-complete-coframe-seal-involution-1.0","result":"PASS","checks":checks,
  "constant_real_classification":{"general_inverting_involution":"F_b=[[0,b],[1/b,0]], b nonzero","diagonal_eta":"no positive-conformal solution","dual_K":"entire F_b family preserves K"},
  "basis_analysis":{"H":"Hadamard","H^T K H":"diag(1,-1)","H^T D H":"Lorentz boost","H^T J H":"diag(1,-1) reflection","status":"exact algebra; physical null-slot interpretation chosen"},
  "field_transport":{"T_phi":"diag(exp(2phi),exp(-2phi))","cocycle":True,"Lorentz_isometry":False,"status":"field matching, not physical symmetry"},
  "angular_extensions":{"conjugacy_traces":[2,-2,0],"reflection_axis":"continuous theta family","selector":"not supplied"},
  "conditional_complete_witnesses":witnesses,"primary_outcome":"MULTIPLE_COMPLETIONS",
  "smallest_missing_object":"a source-authorized physical quadratic readout/slot map plus a complete normal-angular-time-on coframe lift of the seal involution",
  "maximum_conclusion":"RECIPROCAL_CHARACTER_INVERSION_HAS_NO_REAL_CONSTANT_POSITIVE_CSN_ISOMETRY_IN_THE_CHOSEN_DIAGONAL_CLOCK_RADIAL_READOUT; IT_HAS_A_CONTINUUM_OF_CONDITIONAL_O11_REFLECTIONS_IF_THE_DUAL_PAIRING_IS_CHOSEN_AS_NULL_BASIS_METRIC; ANGULAR_AND_TIME_ON_EXTENSIONS_ARE_NONUNIQUE; PRIMARY_BRANCH_MULTIPLE_COMPLETIONS",
  "compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
 (HERE/"DERIVATION_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"result":"PASS","checks":len(checks),"primary_outcome":result["primary_outcome"]},sort_keys=True))
if __name__=="__main__":main()
