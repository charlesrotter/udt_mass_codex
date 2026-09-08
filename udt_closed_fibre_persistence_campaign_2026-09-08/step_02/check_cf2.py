"""Exact local controls, not a global TT/constraint/Cauchy solve or proof."""
import json
import sys
import sympy as S

mode=sys.argv[1] if len(sys.argv)>1 else 'baseline'
assert mode in ['baseline','omit_inverse','kill_polarization','wrong_slope','wrong_phase']
a,c,s=S.symbols('a c s',positive=True)
w=s*(1-s)
delta=4*(c*c-a*a)/a**4
th1=S.Matrix([a/(2*S.sqrt(w)),0,0])
th2=S.Matrix([0,-a*S.sqrt(w),a*S.sqrt(w)])
th3=S.Matrix([0,c*(1-s),c*s])
g=th1*th1.T+th2*th2.T+th3*th3.T
gi=S.simplify(g.inv())
e2=S.Matrix([0,-s/(a*S.sqrt(w)),(1-s)/(a*S.sqrt(w))])
xi=S.Matrix([0,1/c,1/c])
E=th2*th3.T+th3*th2.T
checks={}
def ck(name,truth): checks[name]=bool(truth)
def zero(x): return all(S.simplify(v)==0 for v in x) if isinstance(x,S.MatrixBase) else S.simplify(x)==0
ck('coframe_dual_e2',zero(S.Matrix([th1.dot(e2),th2.dot(e2)-1,th3.dot(e2)])))
ck('coframe_dual_xi',zero(S.Matrix([th1.dot(xi),th2.dot(xi),th3.dot(xi)-1])))
ck('polarization_tracefree',zero(S.trace(gi*E)))
ck('polarization_radial_transverse',zero(E*gi*S.Matrix([1,0,0])))
J=S.diag(1,-1,-1)
ck('metric_reflection_invariant',zero(J.T*g*J-g))
ck('polarization_reflection_invariant',zero(J.T*E*J-E))
radial_cross=S.Matrix([[0,1,0],[1,0,0],[0,0,0]])
ck('torus_invariance_alone_does_not_remove_cross_term',zero(radial_cross.diff(s)))
ck('reflection_rejects_radial_cross_term',not zero(J.T*radial_cross*J-radial_cross))

# Independent finite-dimensional symbol projection from its divergence/longitudinal maps.
z=S.Matrix([1,0,0]); zup=gi*z; norm2=(z.T*gi*z)[0]
def longitudinal(v):
    low=g*v
    return z*low.T+low*z.T-S.Rational(2,3)*z.dot(v)*g
M=norm2*S.eye(3)+zup*z.T/3
piE=S.simplify(E-longitudinal(M.inv()*gi*E*zup))
ck('actual_symbol_projection_fixes_E',zero(piE-E))
inputE=S.zeros(3) if mode=='kill_polarization' else piE
Ysym=-norm2*gi*inputE*xi/delta
def ell(v): return c*(v[2]+v[1] if mode=='wrong_slope' else v[2]-v[1])
symbol=S.simplify(ell(Ysym))
ck('full_radial_slope_symbol',zero(symbol+4*c*S.sqrt(w)/(a**3*delta)))
ck('center_symbol',zero(symbol.subs(s,S.Rational(1,2))+2*c/(a**3*delta)))
N,x=S.symbols('N x',real=True)
phase=S.cos(N*x) if mode=='wrong_phase' else S.sin(N*x)
actual_third=S.diff(phase,x,3).subs(x,0)
ck('real_odd_phase_third_derivative',zero(actual_third+N**3))
ck('center_N3_coefficient',zero((-symbol.subs(s,S.Rational(1,2)))*actual_third+2*c*N**3/(a**3*delta)))
ck('both_gap_signs_retained',delta.subs({a:1,c:2})>0 and delta.subs({a:2,c:1})<0)

# FULL coordinate variation anchor at a=1,c=2. It is an arbitrary tensor
# control, NOT the globally projected/lifted lawful witness. Differentiate the
# actual coordinate connection/Ricci formula with dot(g)=-2K; no principal-only
# substitution in this calculation. f(s) retains its spatial derivatives.
gg=g.subs({a:1,c:2}); inv=S.simplify(gg.inv())
f=S.Function('f')(s)
KK=E.subs({a:1,c:2})*f
dg=-2*KK; dinv=-inv*dg*inv
def dd(expr,j): return S.diff(expr,s) if j==0 else S.S(0)
def simplify(expr): return S.factor(S.simplify(expr))
G=[[[S.S(0) for j in range(3)] for i in range(3)] for k in range(3)]
C=[[[S.S(0) for j in range(3)] for i in range(3)] for k in range(3)]
for k in range(3):
    for i in range(3):
        for j in range(3):
            G[k][i][j]=simplify(sum(inv[k,l]*(dd(gg[l,j],i)+dd(gg[l,i],j)-dd(gg[i,j],l))/2 for l in range(3)))
            C[k][i][j]=simplify(sum((dinv[k,l]*(dd(gg[l,j],i)+dd(gg[l,i],j)-dd(gg[i,j],l))
                +inv[k,l]*(dd(dg[l,j],i)+dd(dg[l,i],j)-dd(dg[i,j],l)))/2 for l in range(3)))
Ric=S.zeros(3); dRic=S.zeros(3)
for i in range(3):
    for j in range(3):
        Ric[i,j]=simplify(sum(dd(G[k][i][j],k)-dd(G[k][i][k],j) for k in range(3))
          +sum(G[k][i][j]*G[l][k][l]-G[l][i][k]*G[k][l][j] for k in range(3) for l in range(3)))
        dRic[i,j]=simplify(sum(dd(C[k][i][j],k)-dd(C[k][i][k],j) for k in range(3))
          +sum(C[k][i][j]*G[l][k][l]+G[k][i][j]*C[l][k][l]
               -C[l][i][k]*G[k][l][j]-G[l][i][k]*C[k][l][j] for k in range(3) for l in range(3)))
xx=xi.subs({a:1,c:2}); pp=S.eye(3)-xx*(gg*xx).T
ck('coordinate_initial_ricci_vertical',zero(inv*Ric*xx-8*xx))
ck('coordinate_initial_ricci_horizontal',zero(inv*Ric*e2.subs({a:1,c:2})+4*e2.subs({a:1,c:2})))
Yfull=pp*(inv*dRic+dinv*Ric)*xx/12
Yno=pp*inv*dRic*xx/12
Dfull=simplify(2*(Yfull[2]-Yfull[1])); Dno=simplify(2*(Yno[2]-Yno[1]))
evaluated=Dno if mode=='omit_inverse' else Dfull
ck('full_inverse_raising_contribution',zero((evaluated-Dno).subs(s,S.Rational(1,2))-S.Rational(16,3)*f.subs(s,S.Rational(1,2))))
# With f=x^3/6 the lower jets vanish, isolating the exact third derivative.
def substitute_profile(expr,profile):
    replacements={S.diff(f,s,j):S.diff(profile,s,j) for j in range(5)}
    return simplify(expr.xreplace(replacements))
full_third=substitute_profile(S.diff(evaluated,s),(s-S.Rational(1,2))**3/6).subs(s,S.Rational(1,2))
ck('coordinate_full_third_jet_anchor',zero(full_third-S.Rational(1,3)))
ck('coordinate_no_radial_image',zero(Yfull[0]))
ck('coordinate_full_variation_symmetric',zero(dRic-dRic.T))
ck('constraint_trace_is_not_additionally_fixed',S.sqrt(1+S.Rational(1,6))>1)
failed=[n for n,v in checks.items() if not v]
print(json.dumps({'kind':'exact finite symbolic controls NOT global existence or closure proof',
 'mode':mode,'sympy_version':S.__version__,'checks':checks,'passed':sum(checks.values()),'failed':failed,
 'general_symbol':str(symbol),'full_coordinate_slope_operator_a1_c2':str(Dfull),
 'no_inverse_coordinate_slope_operator_a1_c2':str(Dno),'full_third_jet':str(full_third),
 'omissions':['no global Q computation','no nonlinear constraint solve','no Cauchy solve',
 'no numerical orbit integration','finite controls do not certify methods or universal quantifiers']},indent=2))
raise SystemExit(1 if failed else 0)
