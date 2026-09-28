"""Candidate-exposed, author-code/output-unexposed independent exact checks."""
import json
import platform
import sympy as s

checks=[]
def eq(name,actual,expected):
 residual=s.simplify(actual-expected)
 assert residual==0,(name,residual)
 checks.append(dict(name=name,kind='exact_identity',residual=str(residual)))
def wrong(name,actual,proposed):
 assert s.simplify(actual-proposed)!=0,name
 checks.append(dict(name=name,kind='wrong_formula_rejected',actual=str(actual),wrong=str(proposed)))

# Independent geometric route: R x round S3 product, orthonormal-frame
# spatial Gauss curvature tensor. No author implementation or outputs read.
K, a, c, G, rho, Lam=s.symbols('K a c G rho Lambda',positive=True)
eta=s.diag(-1,1,1,1)
def delta(i,j):return s.Integer(i==j)
def R(i,j,k,l):
 if 0 in (i,j,k,l):return s.Integer(0)
 return K*(delta(i,k)*delta(j,l)-delta(i,l)*delta(j,k))
Ric=s.Matrix(4,4,lambda j,l:sum(eta[i,k]*R(i,j,k,l) for i in range(4) for k in range(4)))
Scal=sum(eta[i,j]*Ric[i,j] for i in range(4) for j in range(4))
Ein=Ric-Scal*eta/2
eq('Gauss_Ricci_product_time',Ric[0,0],0)
for i in range(1,4):eq('Gauss_Ricci_spatial_'+str(i),Ric[i,i],2*K)
eq('Gauss_scalar',Scal,6*K)
eq('Gauss_Einstein_time',Ein[0,0],3*K)
for i in range(1,4):eq('Gauss_Einstein_spatial_'+str(i),Ein[i,i],-K)
# Dust U=(c,0,0,0) has T_00=rho*c^2 in this orthonormal basis.
T=s.diag(rho*c**2,0,0,0)
residual=Ein+Lam*eta-8*s.pi*G*T/c**4
sol=s.solve([residual[0,0],residual[1,1]],(rho,Lam),dict=True)[0]
eq('independently_solved_Lambda',sol[Lam],K)
eq('independently_solved_dust_density',sol[rho],K*c**2/(4*s.pi*G))
for i in range(4):eq('full_diagonal_field_residual_'+str(i),residual[i,i].subs(sol),0)
wrong('incorrect_dust_coefficient',sol[rho],K*c**2/(8*s.pi*G))
wrong('incorrect_Lambda',sol[Lam],2*K)

chi,theta=s.symbols('chi theta',real=True)
V=s.integrate(s.sin(chi)**2,(chi,0,s.pi))*s.integrate(s.sin(theta),(theta,0,s.pi))*2*s.pi*a**3
M=sol[rho].subs(K,1/a**2)*V
eq('round_S3_volume_from_volume_form',V,2*s.pi**2*a**3)
eq('proper_dust_mass',M,s.pi*c**2*a/(2*G))
eq('dust_compactness',G*M/(c**2*a),s.pi/2)
rho_vac=c**2/(8*s.pi*G*a**2)
Qtotal=G*(M+rho_vac*V)/(c**2*a)
eq('if_vacuum_included_compactness_changes',Qtotal,3*s.pi/4)
wrong('vacuum_mass_silently_included',Qtotal,s.pi/2)

# Ultrastatic product: spatial path travel time is length/c; endpoint
# proper clocks are t. Constants in time block make its connection vanish.
te,ell=s.symbols('te ell',positive=True)
to=te+ell/c
eq('stationary_null_clock_Z',s.diff(to,te),1)
alpha=s.symbols('alpha',positive=True)
eq('finite_antipodal_delay',s.limit((a*alpha)/c,alpha,s.pi,dir='-'),s.pi*a/c)
ellvar=s.symbols('ellvar',real=True)
jacobi=a*s.sin(ellvar/a)
eq('round_sphere_Jacobi_equation',s.diff(jacobi,ellvar,2)+jacobi/a**2,0)
eq('first_antipodal_Jacobi_zero',jacobi.subs(ellvar,s.pi*a),0)
# A moving observer is not a dust-rest clock: a local orthonormal tangent
# U/c=(5/4,3/4,0,0), k=(1,1,0,0) has omega=1/2, versus rest omega=1.
moving_u=s.Matrix([s.Rational(5,4),s.Rational(3,4),0,0])
null_k=s.Matrix([1,1,0,0])
eq('moving_observer_unit_norm',(moving_u.T*eta*moving_u)[0],-1)
moving_frequency=-(moving_u.T*eta*null_k)[0]
wrong('all_observers_have_Z_one',1/moving_frequency,s.Integer(1))

# Homothety: direct cancellation for arbitrary coordinate metric and jets.
lam,g_inv,dg=s.symbols('lambda g_inv dg',positive=True)
eq('generic_connection_scale_cancellation',(g_inv/lam**2)*(lam**2*dg),g_inv*dg)
Ne,No=s.symbols('Ne No',positive=True)
eq('clock_normalization_ratio',(lam*No)/(lam*Ne),No/Ne)
we,wo=s.symbols('omega_e omega_o',positive=True)
eq('same_affine_tangent_frequency_ratio',(lam*we)/(lam*wo),we/wo)
eq('same_phase_covector_frequency_ratio',(we/lam)/(wo/lam),we/wo)
tau=s.symbols('tau',positive=True)
f=tau+tau**3+2
f_lam=lam*f.subs(tau,tau/lam)
eq('nonlinear_arrival_matched_event',s.diff(f_lam,tau).subs(tau,lam*te),s.diff(f,tau).subs(tau,te))
wrong('unmatched_label_clock_ratio',s.diff(f_lam,tau).subs({lam:3,tau:5}),s.diff(f,tau).subs(tau,5))
f2=tau**2+tau
f2_lam=lam*f2.subs(tau,tau/lam)
P=s.diff(f2.subs(tau,f),tau)
Pscaled=s.diff(f2_lam.subs(tau,f_lam),tau).subs(tau,lam*te)
eq('ICN_relay_product_matched_events',Pscaled,P.subs(tau,te))
eq('ICN_beta_homothety',(Pscaled-1)/(Pscaled+1),((P-1)/(P+1)).subs(tau,te))
F=tau+tau**3+2
radar=c*(F-tau)/2
scaled=c*(lam*F-lam*tau)/2
eq('radar_length_scale',scaled,lam*radar)

w,Q,qstar=s.symbols('w Q qstar',real=True)
C=lam**(w-1)*Q-qstar
eq('constraint_derivative_at_root',s.diff(C,lam).subs(Q,qstar/lam**(w-1)),(w-1)*qstar/lam)
eq('weight_one_identity',C.subs({w:1,Q:qstar}),0)
wrong('fixed_mass_scale_blind',(lam**(w-1)*Q).subs({lam:3,w:0,Q:1}),s.Integer(1))
H=s.symbols('H',positive=True)
RH=c/H
rhoH=3*H**2/(8*s.pi*G)
MH=s.Rational(4,3)*s.pi*rhoH*RH**3
eq('Friedmann_defined_compactness',G*MH/(c**2*RH),s.Rational(1,2))
eq('Friedmann_compactness_H_derivative',s.diff(G*MH/(c**2*RH),H),0)
print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
 total=len(checks),checks=checks,
 exposure='Candidate and sources read; author code and outputs unread',
 limitations='Product/Gauss curvature route differs from coordinate Ricci; shared standard geometry and SymPy; illustrative wrong-formula controls are not full harness mutation audit'),indent=2))
