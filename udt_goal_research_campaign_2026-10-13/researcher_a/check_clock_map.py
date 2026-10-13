"""Finite physical-clock map for a supplied dynamic reciprocal spherical metric."""
import sympy as s,json,platform
te,L=s.symbols('s L',positive=True) # emission time = s-1
qo=s.sqrt(te**2+2*L);to=qo-1;qe=te
# tau'(t)=sqrt(q); ratio includes varying reception time, not fixed labels.
Z_map=s.simplify(s.sqrt(qo/qe)*s.diff(to,te))
Z_freq=s.sqrt(qe/qo)
Z_NAR=s.sqrt(qo/qe)
# affine k=(1,q); Gamma^t_tt=q'/2q, Gamma^t_rr=-q'/2q³,
# Gamma^r_tr=-q'/2q; radial k derivative = q'=1.
q=s.symbols('q',positive=True)
checks={
'incidence':s.simplify(((to+1)**2-te**2)/2-L)==0,
'actual_map_equals_frequency':s.simplify(Z_map-Z_freq)==0,
'not_NAR_reciprocal':s.simplify(Z_map*Z_NAR-1)==0,
'affine_t_equation':s.simplify(1/(2*q)-q*q/(2*q**3))==0,
'affine_r_equation':s.simplify(1-2*q/(2*q))==0,
'null_equation':s.simplify(-q+q*q/q)==0,
'exp_integrated_mismatch':s.simplify(Z_map/Z_NAR-qe/qo)==0,
}
result={'python':platform.python_version(),'sympy':s.__version__,'checks':checks,'passed':all(checks.values()),'Z_actual':str(Z_map),'Z_NAR':str(Z_NAR),'exp_M':str(s.simplify(Z_map/Z_NAR)),'domain':'s=1+te>0,L>0,r_e>0; outward regular rays; q=1+t','meaning':'Actual finite ray incidence and proper clock map, exact symbolic; supplied control only.'}
print(json.dumps(result,indent=2));assert all(checks.values())
