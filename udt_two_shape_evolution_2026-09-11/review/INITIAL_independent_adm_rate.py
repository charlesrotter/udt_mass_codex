#!/usr/bin/env python3
"""Source/data-first TI2 calculation; imports no author TI2 implementation."""
import json
import platform
import sympy as S

p,r,px,rx,pxx,rxx=S.symbols('p r p_X r_X p_XX r_XX',real=True)
s=S.symbols('s',real=True,nonzero=True)
deps={p:px,r:rx,px:pxx,rx:rxx}
def dx(f): return S.expand(sum(S.diff(f,q)*v for q,v in deps.items()))
def simp(f): return S.factor(f)
def mat_simp(M): return M.applyfunc(simp)
def inner(M,N): return sum(M[i,j]*N[i,j] for i in range(3) for j in range(3))
def eps(i,j,k): return S.LeviCivita(i,j,k)
def spatial(M,k,i,j): return dx(M[i,j]) if k==0 else S.Integer(0)

d=p*p+r*r
k=(d-s*s)/(2*s)
K=S.Matrix([[k,0,0],[0,s-p,-r],[0,-r,s+p]])
tau=S.trace(K)
Kdot=mat_simp(tau*K-2*K*K)
taudot=simp(S.trace(Kdot)+2*S.trace(K*K))
# Flat Ricci variation with h=gamma_T=-2K, all spatial derivatives retained.
Rdot=S.zeros(3)
for i in range(3):
  for j in range(3):
    Rdot[i,j]=dx(dx(K[i,j]))
    if i==0: Rdot[i,j]-=dx(dx(K[0,j]))
    if j==0: Rdot[i,j]-=dx(dx(K[0,i]))
    if i==j==0: Rdot[i,j]+=dx(dx(tau))
Rdot=mat_simp(Rdot)
E=mat_simp(tau*K-K*K)
Edot=mat_simp(Rdot+taudot*K+tau*Kdot-Kdot*K-K*Kdot-2*K*K*K)
B=S.Matrix(3,3,lambda i,j:sum(eps(i,a,b)*spatial(K,a,b,j) for a in range(3) for b in range(3)))
# epsilon_i^{ab},dot=(tau delta_im - 2K_im)epsilon_m^{ab};
# Gamma^a_bj,dot=-(partial_b K_aj+partial_j K_ab-partial_a K_bj).
def Gdot(a,b,j):
  return -spatial(K,b,a,j)-spatial(K,j,a,b)+spatial(K,a,b,j)
Bdot_volume=mat_simp((tau*S.eye(3)-2*K)*B)
Bdot_partial=S.Matrix(3,3,lambda i,j:sum(eps(i,a,b)*spatial(Kdot,a,b,j) for a in range(3) for b in range(3)))
Bdot_connection=S.Matrix(3,3,lambda i,j:-sum(eps(i,a,b)*Gdot(c,a,j)*K[b,c] for a in range(3) for b in range(3) for c in range(3)))
Bdot=mat_simp(Bdot_volume+Bdot_partial+Bdot_connection)
# Each of the two gamma inverse factors contributes 2K; symmetry gives the factor4.
inverse_term=4*inner(K*E,B)
J=simp(inner(E,B))
Jdot=simp(inner(Edot,B)+inner(E,Bdot)+inverse_term)
P=simp(16*J)
Pdot=simp(16*Jdot)
checks={
 'hamiltonian':simp(tau*tau-S.trace(K*K)),
 'momentum_X':simp(dx(K[0,0])-dx(tau)),
 'tau_dot_constraint':simp(taudot-tau*tau),
 'E_trace':simp(S.trace(E)),
 'B_trace':simp(S.trace(B)),
 'E_trace_derivative':simp(S.trace(Edot)+2*S.trace(K*E)),
 'B_trace_derivative':simp(S.trace(Bdot)+2*S.trace(K*B)),
 'B_symmetry':list(mat_simp(B-B.T)),
 'Bdot_symmetry':list(mat_simp(Bdot-Bdot.T)),
 'initial_TI1_correspondence':simp(P+32*k*(p*rx-r*px)),
}
for key,value in checks.items():
  assert all(x==0 for x in value) if isinstance(value,list) else value==0, (key,value)
harmonic={pxx:-p,rxx:-r}
Pdot_h=simp(Pdot.subs(harmonic))
L=simp(Pdot_h/P)
ee=S.symbols('epsilon',real=True)
scaled={p:ee*p,r:ee*r,px:ee*px,rx:ee*rx}
L0=S.limit(L.subs(scaled,simultaneous=True),ee,0)
rate_remainder=simp(Pdot_h-L0*P)
anchor={p:S.Rational(1,8),r:S.Rational(1,12),px:-S.Rational(1,10),rx:S.Rational(1,7),s:-S.Rational(2,3)}
controls={
 'omit_inverse_contraction_error':simp((-16*inverse_term).subs(anchor)),
 'omit_B_connection_error':simp((-16*inner(E,Bdot_connection)).subs(anchor)),
 'omit_B_volume_error':simp((-16*inner(E,Bdot_volume)).subs(anchor)),
 'omit_Ricci_spatial_variation_error':simp((-16*inner(Rdot.subs(harmonic),B)).subs(anchor)),
 'one_component_Pdot':simp(Pdot_h.subs({r:0,rx:0})),
 'zero_Pdot':simp(Pdot_h.subs({p:0,r:0,px:0,rx:0})),
 'aligned_Pdot':simp(Pdot_h.subs({r:3*p,rx:3*px},simultaneous=True)),
}
for key,val in controls.items():
  assert val!=0 if key.startswith('omit_') else val==0,(key,val)
result={
 'python':platform.python_version(),'sympy':S.__version__,
 'scope':'Exact general-symbol ADM/Gauss-Codazzi derivative; harmonic restriction only after full derivative',
 'Kdot':str(Kdot),'Ric3_dot':str(Rdot),'E':str(E),'B':str(B),
 'Edot':str(Edot),'Bdot':str(Bdot),'P':str(P),'Pdot_general':str(Pdot),
 'Pdot_harmonic':str(Pdot_h),'L':str(L),'L0':str(L0),'S':str(rate_remainder),
 'checks':{q:str(v) for q,v in checks.items()},'controls':{q:str(v) for q,v in controls.items()},
 'anchor':{q:str(v.subs(anchor)) for q,v in {'P':P,'Pdot':Pdot_h,'L':L,'L0':L0,'S':rate_remainder}.items()},
 'equation_terms':{q:str(simp(v.subs(harmonic))) for q,v in {'Ricci_variation':16*inner(Rdot,B),'E_algebraic':16*inner(Edot-Rdot,B),'B_volume':16*inner(E,Bdot_volume),'B_partial':16*inner(E,Bdot_partial),'B_connection':16*inner(E,Bdot_connection),'inverse_contraction':16*inverse_term}.items()},
 'status':'PASS'
}
print(json.dumps(result,indent=2,sort_keys=True))
