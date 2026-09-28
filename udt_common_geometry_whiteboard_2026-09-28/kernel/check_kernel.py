#!/usr/bin/env python3
"""Exact conditional geometry anchors; no observational input or physical-law fit."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[k]='2'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
from pathlib import Path
import datetime as dt
import hashlib,json,platform,time
import sympy as s

P=Path(__file__).resolve().parent
checks={}


def zero(name,expr):
    value=s.simplify(s.trigsimp(s.expand(expr)))
    if value!=0:raise AssertionError((name,value))
    checks[name]={'kind':'exact symbolic identity','residual':str(value)}


def nonzero(name,expr):
    value=s.simplify(s.expand(expr))
    if value==0:raise AssertionError((name,'negative check failed to reject'))
    checks[name]={'kind':'deliberately wrong identity rejected','nonzero_residual':str(value)}


def connection(g,coords):
    n=len(coords);gi=g.inv()
    return [[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(n))/2)
             for c in range(n)] for b in range(n)] for a in range(n)]


def curvature(G,coords,a,b,c,d):
    return s.simplify(s.diff(G[a][d][b],coords[c])-s.diff(G[a][c][b],coords[d])+
        sum(G[a][c][e]*G[e][d][b]-G[a][d][e]*G[e][c][b] for e in range(len(coords))))


def main():
    started=time.monotonic();out=P/'CHECK_RESULT.json'
    if out.exists():raise RuntimeError('Refuse to overwrite check evidence')
    f,L=s.symbols('f L',positive=True);b=s.symbols('b',real=True)
    h=f**2*s.Matrix([[-1,-b],[-b,L**2-b**2]])
    m=f**2*L;J=s.diag(1,1/m);hs=J.T*h*J
    zero('pair_original_determinant',h.det()+f**4*L**2)
    zero('pair_completed_determinant',hs.det()+1)
    zero('pair_positive_clock_square',-hs[0,0]-f**2)
    zero('pair_shift_retained',hs[0,1]/hs[0,0]-b/m)
    zero('pair_calibrated_spatial_factor',hs[1,1]-hs[0,1]**2/hs[0,0]-f**(-2))
    zero('pair_q_readout',(1/f-f)/(1/f+f)-(1-f**2)/(1+f**2))

    t,x,y,z,te,C,kappa=s.symbols('t x y z te C kappa',real=True)
    ff=s.Function('f')(t);coords=[t,x,y,z];g=s.diag(-ff**2,ff**2,ff**2,ff**2)
    G=connection(g,coords)
    K=s.Matrix([C/ff**2,C/ff**2,0,0]);U=s.Matrix([1/ff,0,0,0])
    zero('proper_clock_unit',(U.T*g*U)[0]+1)
    zero('null_metric',(K.T*g*K)[0])
    zero('metric_frequency',-(U.T*g*K)[0]-C/ff)
    for a in range(4):
        geod=(sum(K[j]*s.diff(K[a],coords[j]) for j in range(4))+
              sum(G[a][j][k]*K[j]*K[k] for j in range(4) for k in range(4)))
        zero(f'original_affine_geodesic_component_{a}',geod)
    # Original Riemann components, computed before choosing a Jacobi solution.
    Ryt=curvature(G,coords,2,0,2,0)
    Ryx=curvature(G,coords,2,1,2,1)
    Ry_tx=curvature(G,coords,2,0,2,1)+curvature(G,coords,2,1,2,0)
    tide=s.simplify(C**2/ff**4*(Ryt+Ryx+Ry_tx))
    expected=C**2*(2*s.diff(ff,t)**2-ff*s.diff(ff,t,2))/ff**6
    zero('original_metric_screen_tide',tide-expected)
    def affine(expr):return C/ff**2*s.diff(expr,t)
    D=ff*(t-te)
    zero('jacobi_original_equation',affine(affine(D))+tide*D)
    zero('jacobi_vertex',D.subs(t,te))
    zero('jacobi_unit_source_frequency',affine(D).subs(t,te).subs(C,ff.subs(t,te))-1)
    H=s.diff(ff,t)/ff**2
    omega=C/ff
    zero('normalized_redshift_gradient',-affine(s.log(omega))/omega-H)
    nonzero('catch_missing_frequency_normalization',-affine(s.log(omega))-H)
    # The conformal CK field is partial_t; its normalized base has unit stationary time leg.
    zero('conformal_killing_time_factor',s.diff(g[0,0],t)-2*s.diff(ff,t)/ff*g[0,0])
    zero('normalized_base_stationary',s.diff(g[0,0]/ff**2,t))

    eta=s.symbols('eta',real=True)
    Dboost=s.cosh(eta)-s.sinh(eta)
    zero('observer_longitudinal_Doppler',s.expand_trig(Dboost).rewrite(s.exp)-s.exp(-eta))
    zero('received_ratio_not_gamma',1/s.exp(-eta)-s.exp(eta))
    DA,DB,R,A0,A1=s.symbols('DA DB R A0 A1',positive=True)
    zero('observer_area_ratio_covariance',(DA**2*A0)/(DB**2*A1)-(DA/DB)**2*(A0/A1))

    a1,a2,s1,s2=s.symbols('a1 a2 s1 s2',real=True)
    l1,l2=s.symbols('l1 l2',positive=True)
    logR=lambda start,span:kappa*((start+span)**2-start**2)
    zero('carried_chain_rule_log',logR(t,l1)+logR(t+l1,l2)-logR(t,l1+l2))
    nonzero('catch_uncarried_same_epoch_product',logR(t,l1)+logR(t,l2)-logR(t,l1+l2))
    zero('finite_forward_at_zero_expansion_epoch',logR(0,l1)-kappa*l1**2)
    zero('later_future_return',logR(l1,l1)-3*kappa*l1**2)
    nonzero('catch_return_as_inverse',logR(l1,l1)+logR(0,l1))
    zero('same_segment_inverse',kappa*(0-l1**2)+logR(0,l1))
    nonzero('catch_depth_sign',logR(0,l1)-(-logR(0,l1)))

    HH=s.symbols('H',real=True);avec=s.Matrix(s.symbols('a0:3',real=True))
    Sxx,Syy,Sxy,Sxz,Syz=s.symbols('Sxx Syy Sxy Sxz Syz',real=True)
    Sig=s.Matrix([[Sxx,Sxy,Sxz],[Sxy,Syy,Syz],[Sxz,Syz,-Sxx-Syy]])
    B=lambda n:HH+(avec.T*n)[0]+(n.T*Sig*n)[0]
    axes=[s.eye(3)[:,j] for j in range(3)]
    zero('all_direction_mean_moment',sum(B(n)+B(-n) for n in axes)/6-HH)
    for j,n in enumerate(axes):zero(f'directional_odd_part_{j}',(B(n)-B(-n))/2-avec[j])
    zero('zero_mean_shear_trace',s.trace(Sig))
    # G415 epsilon=0 background: derivative with respect to proper time N dt.
    N=s.Function('N')(t)
    Hxi=-1/(4*N*t);Hy=1/(2*N*t);Hz=Hy;Havg=(Hxi+Hy+Hz)/3
    zero('G415_background_average',Havg-1/(4*N*t))
    zero('G415_background_shear_xi',Hxi-Havg+1/(2*N*t))
    nonzero('catch_axial_potential_implies_all_direction',Hxi-Hy)

    # Same clocks, different screen tide: ultrastatic R x R x S2 control.
    th,ph=s.symbols('th ph',real=True);gg=s.diag(-1,1,1,s.sin(th)**2);cc=[t,z,th,ph]
    GG=connection(gg,cc)
    zero('ultrastatic_acceleration',GG[2][0][0])
    zero('ultrastatic_curved_screen_tide',curvature(GG,cc,3,2,3,2)-1)
    zero('ultrastatic_flat_screen_tide',curvature(GG,cc,1,2,1,2))
    ell=s.symbols('ell',real=True)
    zero('ultrastatic_curved_jacobi',s.diff(s.sin(ell),ell,2)+s.sin(ell))
    zero('ultrastatic_flat_jacobi',s.diff(ell,ell,2))

    # Endpoint controls f=(1-t)^(-p), t<1; exact positive-variable integrals.
    v=s.symbols('v',positive=True)
    extents={}
    for p in [s.Rational(1,4),s.Rational(3,4),s.Integer(1)]:
        proper=s.integrate(v**(-p),(v,0,1));aff=s.integrate(v**(-2*p),(v,0,1))
        extents[str(p)]={'f_endpoint':'infinity','proper_integral':str(proper),'affine_integral':str(aff),
            'interpretation':'supplied conformal-flat comparison; not a selected UDT completion'}
    assert extents['1/4']['proper_integral']=='4/3' and extents['1/4']['affine_integral']=='2'
    assert extents['3/4']['proper_integral']=='4' and extents['3/4']['affine_integral']=='oo'
    assert extents['1']['proper_integral']=='oo' and extents['1']['affine_integral']=='oo'
    result={'status':'PASS_EXACT_CONDITIONAL_ANCHORS','utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'python':platform.python_version(),'sympy':s.__version__,'dtype':'symbolic exact, no floating grid',
        'runtime_seconds':time.monotonic()-started,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'contract_sha256':hashlib.sha256((P/'CHECK_CONTRACT.md').read_bytes()).hexdigest(),
        'checks':checks,'endpoint_extents':extents,
        'limits':'Same reused context; finite exact anchors support hand arguments, not global metric extension, physical identification, native admission, or fresh review.'}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
