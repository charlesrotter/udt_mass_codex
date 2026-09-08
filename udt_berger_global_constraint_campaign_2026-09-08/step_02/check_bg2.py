#!/usr/bin/env python3
"""Exact principal-symbol checks PLUS full lower-order tensor anchor.

Reuses the saved/replayed independent BI1 Koszul tensor, not a cloned utility.
Symbol-only mode intentionally demonstrates two or more real false passes.
No finite check claims global TT existence or nonlinear constraint realization.
"""
import argparse
import json
import platform
from pathlib import Path
import sympy as s

parser=argparse.ArgumentParser()
parser.add_argument('--mutant',default='none',choices=['none','Q_plus',
    'no_laplacian','omit_raising','omit_derivative_index','wrong_image_block'])
parser.add_argument('--symbol-only',action='store_true')
args=parser.parse_args()
checks=[]
def check(name,actual,expected=0):
    r=s.simplify(actual-expected)
    entries=list(r) if isinstance(r,s.MatrixBase) else [r]
    checks.append({'name':name,'pass':all(x==0 for x in entries),'residual':str(r)})

def L0(z,v):
    return z*v.T+v*z.T-s.Rational(2,3)*z.dot(v)*s.eye(3)

def project(z,F):
    M=z.dot(z)*s.eye(3)+z*z.T/3
    sign=1 if args.mutant=='Q_plus' else -1
    return s.simplify(F+sign*L0(z,M.inv()*F*z))

def Ssymbol(z,F):
    lap=0 if args.mutant=='no_laplacian' else 1
    return z*(F*z).T+(F*z)*z.T-lap*z.dot(z)*F-s.trace(F)*z*z.T

def direct_connection_symbol(z,F):
    Gdot=lambda i,j,k:-s.I*(z[i]*F[j,k]+z[j]*F[i,k]-z[k]*F[i,j])
    return s.Matrix(3,3,lambda i,j:s.simplify(sum(
        s.I*z[k]*Gdot(i,j,k)-s.I*z[i]*Gdot(k,j,k) for k in range(3))))

f0,f1,f2,f3,f4=s.symbols('f0:5',real=True)
F=s.Matrix([[f0,f2,f3],[f2,f1,f4],[f3,f4,-f0-f1]])
Ffull=F+s.symbols('tr',real=True)*s.eye(3)/3
zfixtures=[s.Matrix(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,2,3)]]
for idx,z in enumerate(zfixtures):
    A=project(z,F)
    check(f'Q_tracefree_{idx}',s.trace(A))
    check(f'Q_transverse_{idx}',A*z,s.zeros(3,1))
    check(f'Q_idempotent_{idx}',project(z,A),A)
    v=s.Matrix(s.symbols('v0:3',real=True))
    check(f'Q_longitudinal_kernel_{idx}',project(z,L0(z,v)),s.zeros(3))
    check(f'full_principal_Ricci_from_connection_{idx}',Ssymbol(z,Ffull),
          direct_connection_symbol(z,Ffull))
    check(f'principal_on_TT_{idx}',Ssymbol(z,A),-z.dot(z)*A)
    # Five TF coordinates -> rank2 TT projector, not a global moduli count.
    matrix=s.Matrix([A[0,0],A[1,1],A[0,1],A[0,2],A[1,2]]).jacobian([f0,f1,f2,f3,f4])
    check(f'TT_symbol_rank_{idx}',matrix.rank(),2)

gap=s.symbols('Delta',nonzero=True,real=True)
xi=s.Matrix([0,0,1]); horizontal=s.diag(1,1,0)
E=s.Matrix([[0,0,0],[0,0,1],[0,1,0]])
z=s.Matrix([1,0,0])
check('chosen_polarization_fixed',project(z,E),E)
check('nonzero_full_operator_leading_image',horizontal*Ssymbol(z,project(z,E))*xi/gap,
      s.Matrix([0,-1/gap,0]))
Ez=s.diag(1,-1,0)
check('vertical_frequency_silent_control',horizontal*Ssymbol(xi,project(xi,Ez))*xi,
      s.zeros(3,1))

anchors={}
if not args.symbol_only:
    # Original BI1 independently differentiated Koszul tensor replayed unchanged.
    root=Path(__file__).resolve().parents[2]
    here=Path(__file__).resolve().parent
    replay=(here/'inherited_fulltensor_replay.stdout').read_bytes()
    prior=(root/'udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/source_first_run.stdout').read_bytes()
    check('inherited_anchor_replay_byte_identity',int(replay==prior),1)
    saved=json.loads(replay)
    p,q=s.symbols('p q',positive=True)
    x,y,z0,u,v,w=s.symbols('x y z u v w',real=True)
    names=dict(zip(['p','q','x','y','z','u','v','w'],[p,q,x,y,z0,u,v,w]))
    expected_S=s.sympify(saved['homogeneous_Ricci_dot'],locals=names)
    expected_Bdot=s.sympify(saved['homogeneous_endomorphism_dot'],locals=names)
    K=s.Matrix([[x,u,v],[u,y,w],[v,w,z0]])
    I=range(3)
    br=s.MutableDenseNDimArray.zeros(3,3,3)
    for i,j,k,value in [(0,1,2,q),(1,2,0,p),(2,0,1,p)]:
        br[i,j,k]=value; br[j,i,k]=-value
    G=s.MutableDenseNDimArray.zeros(3,3,3)
    for i in I:
        for j in I:
            for k in I:
                G[i,j,k]=(br[i,j,k]-br[j,k,i]+br[k,i,j])/2
    D1=s.MutableDenseNDimArray.zeros(3,3,3)
    for r in I:
        for i in I:
            for j in I:
                D1[r,i,j]=-sum(G[r,i,m]*K[m,j]+G[r,j,m]*K[i,m] for m in I)
    D2=s.MutableDenseNDimArray.zeros(3,3,3,3)
    for r in I:
        for t in I:
            for i in I:
                for j in I:
                    deriv_index=0 if args.mutant=='omit_derivative_index' else sum(
                        G[r,t,m]*D1[m,i,j] for m in I)
                    D2[r,t,i,j]=-deriv_index-sum(G[r,i,m]*D1[t,m,j]
                                                 +G[r,j,m]*D1[t,i,m] for m in I)
    lap=0 if args.mutant=='no_laplacian' else 1
    S=s.Matrix(3,3,lambda i,j:s.expand(sum(-D2[r,i,r,j]-D2[r,j,r,i]
                                         +lap*D2[r,r,i,j] for r in I)))
    lh,lv=p*q-q*q/2,q*q/2
    B=s.diag(lh,lh,lv)
    Bd=S if args.mutant=='omit_raising' else S+2*K*B
    check('full_all_nine_Ricci_derivatives_independent_Koszul',S,expected_S)
    check('full_all_nine_raised_Ricci_derivatives',Bd,expected_Bdot)
    eig=lh if args.mutant=='wrong_image_block' else lv
    Y=(horizontal*(S+2*eig*K)*xi)/(lv-lh)
    if args.mutant=='omit_raising':
        Y=horizontal*S*xi/(lv-lh)
    check('full_image_block_independent_Koszul',Y,horizontal*expected_Bdot*xi/(lv-lh))
    kappa=horizontal*K*xi
    Pdot=Y*xi.T+xi*(Y-2*kappa).T
    expected_Pdot=(horizontal*expected_Bdot*(xi*xi.T)+(xi*xi.T)*expected_Bdot*horizontal)/(lv-lh)
    check('full_nonsymmetric_projector_blocks',Pdot,expected_Pdot)
    h=s.symbols('h',nonzero=True,real=True)
    pure={x:h,y:h,z0:h,u:0,v:0,w:0}
    check('full_baseline_inverse_metric_term_not_zero',Bd.subs(pure),2*h*B)
    check('image_projector_difference_retained',Pdot[0,2]-Pdot[2,0],2*v)
    anchors={'all_six_homogeneous_components':'formal diagnostics, not constrained witnesses',
             'S':str(S),'Bdot':str(Bd),'Y':str(Y),'Pdot':str(Pdot),
             'inherited_actual_independence':'reused sealed prior Koszul argument/code, not new fresh context',
             'limitations':'Homogeneous full anchor alone does not certify all inhomogeneous lower-order identities.'}

result={'kind':'exact_symbol_plus_full_tensor_anchors_not_global_existence_proof',
        'python':platform.python_version(),'sympy':s.__version__,
        'mutant':args.mutant,'symbol_only':args.symbol_only,
        'checks':checks,'count':len(checks),'pass':all(c['pass'] for c in checks),
        'anchors':anchors,'omissions':['global TT projection functional theorem',
            'oscillatory remainder estimate','BG1 nonlinear IFT realization',
            'explicit N or amplitude/lifetime bounds','genericity or orbit closure']}
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['pass'] else 1)
