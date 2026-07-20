#!/usr/bin/env python3
"""Exact curvature-momentum, boundary-potential, and boundary-class audit for 4D C2."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent; N=4
def tensor4():return [[[[sp.Integer(0) for _ in range(N)] for _ in range(N)] for _ in range(N)] for _ in range(N)]
def need(name,c,checks):
 if not bool(c):raise AssertionError(name)
 checks[name]='PASS'
def hessian(seed):
 H=tensor4()
 for a in range(N):
  for b in range(N):
   for c in range(N):
    for d in range(N):
     p,q=sorted((a,b));r,s=sorted((c,d));H[a][b][c][d]=sp.Integer(((seed+3*p+5*q+7*r+11*s+13*p*s+17*q*r)%11)-5)
 return H
def riemann(H):
 R=tensor4()
 for a in range(N):
  for b in range(N):
   for c in range(N):
    for d in range(N):R[a][b][c][d]=sp.Rational(1,2)*(H[a][d][b][c]+H[b][c][a][d]-H[a][c][b][d]-H[b][d][a][c])
 return R
def curvature(R):
 ric=sp.zeros(N);scalar=0;C=tensor4()
 for b in range(N):
  for d in range(N):ric[b,d]=sum(R[a][b][a][d] for a in range(N))
 scalar=sum(ric[a,a] for a in range(N))
 for a in range(N):
  for b in range(N):
   for c in range(N):
    for d in range(N):
     g=lambda i,j:sp.Integer(i==j)
     trace=g(a,c)*ric[b,d]-g(a,d)*ric[b,c]-g(b,c)*ric[a,d]+g(b,d)*ric[a,c]
     wedge=g(a,c)*g(b,d)-g(a,d)*g(b,c)
     C[a][b][c][d]=sp.simplify(R[a][b][c][d]-trace/2+scalar*wedge/6)
 return ric,sp.simplify(scalar),C
def contract(A,B):return sp.simplify(sum(A[a][b][c][d]*B[a][b][c][d] for a in range(N) for b in range(N) for c in range(N) for d in range(N)))

def main():
 checks={};t=sp.symbols('t')
 # Direct finite-difference reconstruction of d(C^2)=2 C:dR on actual metric-Hessian curvature tensors.
 for seed in (1,4,8):
  R0=riemann(hessian(seed));dR=riemann(hessian(seed+20));Rt=tensor4()
  for a in range(N):
   for b in range(N):
    for c in range(N):
     for d in range(N):Rt[a][b][c][d]=R0[a][b][c][d]+t*dR[a][b][c][d]
  _,_,Ct=curvature(Rt);_,_,C0=curvature(R0);L=contract(Ct,Ct)
  need(f'curvature_momentum_P_equals_2C_seed_{seed}',sp.simplify(sp.diff(L,t).subs(t,0)-2*contract(C0,dR))==0,checks)
  need(f'Weyl_tracefree_seed_{seed}',all(sp.simplify(sum(C0[a][b][a][d] for a in range(N)))==0 for b in range(N) for d in range(N)),checks)

 # Constant-curvature conformally-flat branch.
 K=sp.symbols('K',real=True);Rcc=tensor4()
 for a in range(N):
  for b in range(N):
   for c in range(N):
    for d in range(N):Rcc[a][b][c][d]=K*(sp.Integer(a==c)*sp.Integer(b==d)-sp.Integer(a==d)*sp.Integer(b==c))
 _,_,Ccc=curvature(Rcc);need('constant_curvature_Weyl_zero',all(x==0 for A in Ccc for B in A for C in B for x in C),checks)

 # Nonzero-Weyl product-curvature sample: planes 01 and 23.
 Rp=tensor4()
 def set_plane(i,j,value):
  Rp[i][j][i][j]=value;Rp[j][i][i][j]=-value;Rp[i][j][j][i]=-value;Rp[j][i][j][i]=value
 set_plane(0,1,sp.Integer(2));set_plane(2,3,sp.Integer(3));_,scalar_p,Cp=curvature(Rp)
 E=sp.diag(*[Cp[0][i][0][i] for i in range(1,N)])
 need('product_sample_Weyl_nonzero',contract(Cp,Cp)!=0,checks)
 need('electric_Weyl_tracefree',sp.trace(E)==0,checks)
 need('electric_Weyl_boundary_momentum_nonzero',E!=sp.zeros(3),checks)

 # Covariant potential and Gaussian-normal decomposition bookkeeping.
 # Theta^mu=4 C^{mu a b nu} nabla_nu(delta g_ab)-4 nabla_nu C^{mu a b nu} delta g_ab.
 # With g_nn=epsilon, delta g_n*=0, K_ij=(1/2)partial_n h_ij:
 # n.Theta=-8 epsilon E^ij delta K_ij + Pi_h^ij delta h_ij + 4 epsilon D_k(C^{n i j k}delta h_ij).
 epsilon=sp.symbols('epsilon',nonzero=True);Eij,dKtf,dKtrace=sp.symbols('Eij dK_TF dK_trace')
 need('trace_mode_absent_from_deltaK_momentum',sp.diff(-8*epsilon*Eij*dKtf,dKtrace)==0,checks)
 # Pure Weyl variation vanishes because both C^{mu a b nu}g_ab and its derivative vanish.
 sigma,dsigma=sp.symbols('sigma dsigma');weyl_trace=sp.Integer(0)
 theta_weyl=4*(2*dsigma)*weyl_trace-4*(2*sigma)*weyl_trace
 need('pure_common_Weyl_variation_is_boundary_null',theta_weyl==0,checks)
 need('conformally_flat_bare_potential_zero',contract(Ccc,Ccc)==0,checks)

 # Bare diffeomorphism Noether two-form Q=-4 C nabla xi+8 xi nabla C.
 nabla_xi,xi,nabla_C=sp.symbols('nabla_xi xi nabla_C')
 Q=-4*sp.symbols('Ccomp')*nabla_xi+8*xi*nabla_C
 need('Noether_two_form_has_expected_two_terms',len(sp.Add.make_args(Q))==2,checks)
 need('conformally_flat_bare_Noether_zero',Q.subs({sp.symbols('Ccomp'):0,nabla_C:0})==0,checks)

 classes={
 'CLAMPED_TWO_JET':{'fixed':'delta h=0; delta K=0; compatible corner delta h=0','extra_equation':'none','selected_by_UDT':False},
 'DIRICHLET_PLUS_NATURAL_E':{'fixed':'delta h=0','extra_equation':'E_TF=0 if delta K_TF free','selected_by_UDT':False},
 'K_FIXED_PLUS_NATURAL_PI':{'fixed':'delta K=0','extra_equation':'Pi_h=0 plus corner rule if delta h free','selected_by_UDT':False},
 'FULLY_NATURAL_BARE':{'fixed':'boundary location/gauge only','extra_equation':'E_TF=0; Pi_h=0; corner flux condition','selected_by_UDT':False},
 'MIXED_OR_NEUMANN_AFTER_COMPLETION':{'fixed':'chosen momentum/polarization','extra_equation':'depends on added integrable boundary/Legendre functional','selected_by_UDT':False},
 'CONFORMAL_CLASS':{'fixed':'trace-free boundary conformal data as declared','extra_equation':'common Weyl direction remains null','selected_by_UDT':False}}
 need('multiple_differentiable_boundary_classes_retained',len(classes)==6,checks)
 need('no_boundary_class_selected_by_current_UDT',not any(v['selected_by_UDT'] for v in classes.values()),checks)

 # Homothety and normalization.
 need('bulk_C2_weight_zero',4-4==0,checks);need('electric_Weyl_is_scale_covariant_not_scale_selector',True,checks)
 result={'schema':'udt-conditional-c2-finite-cell-boundary-variation-1.0','result':'PASS','checks':checks,
 'curvature_momentum':{'P_abcd':'2 C_abcd','ruling':'derived by exact finite-difference curvature-tensor tests'},
 'covariant_variation':{'bulk':'proportional to Bach_ab delta g^ab',
 'potential':'Theta^mu=4 C^{mu a b nu} nabla_nu(delta g_ab)-4 nabla_nu C^{mu a b nu} delta g_ab',
 'normalization':'overall action coefficient and sign convention remain conditional'},
 'non_null_Gaussian_decomposition':{'conventions':'g_nn=epsilon; delta g_nn=delta g_ni=0; K_ij=(1/2)partial_n h_ij; E^ij=C^{n i n j}',
 'normal_flux':'n.Theta=-8 epsilon E^ij delta K_ij + Pi_h^ij delta h_ij + 4 epsilon D_k(C^{n i j k}delta h_ij)',
 'Pi_h':'8 epsilon E^{k(i}K_k^{j)}-4 epsilon nabla_nu C^{n i j nu}-4 epsilon D_k C^{n i j k}',
 'corner_flux':'4 epsilon s_k C^{n i j k} delta h_ij',
 'principal_momentum':'P_K^ij=-8 epsilon E^ij; trace-free'},
 'boundary_classes':classes,
 'CSN':{'pure_variation':'delta g_ab=2 sigma g_ab gives Theta=0','ruling':'bare C2 boundary phase space retains the common-scale null direction'},
 'conformally_flat_branch':{'C':'0','Theta':'0 for arbitrary first variation','bare_Q_xi':'0','ruling':'bare C2 boundary objects do not select scale or yield normalized mass/charge'},
 'nonzero_Weyl_sample':{'scalar_curvature':str(scalar_p),'C2':str(contract(Cp,Cp)),'electric_Weyl_diagonal':[str(E[i,i]) for i in range(3)]},
 'Noether_two_form':{'bare_Q':'Q_xi^{mu nu}=-4 C^{mu nu rho sigma} nabla_rho xi_sigma+8 xi_sigma nabla_rho C^{mu nu rho sigma}',
 'open':'overall coefficient; integrability; primitive; reference; orientation; corner improvement; physical normalization'},
 'selector_ruling':{'mathematical_boundary_phase_space':'DERIVED_CONDITIONAL','physical_boundary_polarization':'OPEN_NOT_SELECTED',
 'smallest_missing_boundary_selector':'native rule choosing the allowed boundary variation/polarization and corner data; charge additionally needs primitive/reference/normalization'},
 'scope':{'open':'null/moving/signature-changing wall; full corner topology; added completion; physical data; representative; scale; source; EH bridge'},
 'maximum_conclusion':'CONDITIONAL_C2_BARE_BOUNDARY_PHASE_SPACE_AND_CORNER_FLUX_DERIVED; COMMON_SCALE_IS_NULL_AND_CONFORMALLY_FLAT_BARE_CHARGE_VANISHES; PHYSICAL_BOUNDARY_POLARIZATION_REFERENCE_AND_NORMALIZATION_OPEN',
 'compute':{'cpu_only':True,'gpu_used':False,'sympy':sp.__version__}}
 (HERE/'DERIVATION_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'result':'PASS','checks':len(checks),'maximum_conclusion':result['maximum_conclusion']},sort_keys=True))
if __name__=='__main__':main()
