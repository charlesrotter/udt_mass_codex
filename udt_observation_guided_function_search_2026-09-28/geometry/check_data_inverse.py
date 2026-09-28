#!/usr/bin/env python3
"""Exposed, fixed-fit compatibility analysis; no fitting or native-law claim."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/udt_geometry_mpl')
import csv
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import scipy
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
DATA=ROOT.parent/'data'
FIT=DATA/'results/full_fits.json'
DIA=DATA/'results/diagnostics.json'


def central(coefs,x):
    x=np.asarray(x)
    p=sum(c*x**j for j,c in enumerate(coefs,1))
    pp=sum(j*c*x**(j-1) for j,c in enumerate(coefs,1))
    P=1+sum(j*c*x**j for j,c in enumerate(coefs,1))
    Pp=sum(j*j*c*x**(j-1) for j,c in enumerate(coefs,1))
    F=x*np.exp(p)
    E=np.exp(x-p)/P
    dec=-pp-Pp/P
    AP=np.exp(x)*x/P
    return F,P,E,dec,AP


def jacobian(coefs,x):
    F,P,E,dec,AP=central(coefs,x)
    Pp=sum(j*j*c*x**(j-1) for j,c in enumerate(coefs,1))
    logE=np.array([-x**j*(1+j/P) for j in range(1,len(coefs)+1)])
    dq=np.array([-j*x**(j-1)-(j*j*x**(j-1)*P-Pp*j*x**j)/(P*P)
                 for j in range(1,len(coefs)+1)])
    logAP=np.array([-j*x**j/P for j in range(1,len(coefs)+1)])
    return E*logE,dq,AP*logAP


def exact_domains(coefs):
    x=sp.symbols('x',real=True)
    cs=[sp.Rational(str(c)) for c in coefs]
    p=sum(c*x**j for j,c in enumerate(cs,1));P=sp.Poly(1+x*sp.diff(p,x),x)
    intervals=P.intervals(eps=sp.Rational(1,10**20))
    roots=[{'rational_interval':[str(lo),str(hi)],'decimal_midpoint':str(sp.N((lo+hi)/2,50)),
            'multiplicity':mult,'positive':bool(lo>0)} for (lo,hi),mult in intervals]
    critical=[]
    for (lo,hi),mult in sp.Poly(sp.diff(P.as_expr(),x),x).intervals(eps=sp.Rational(1,10**20)):
        mid=(lo+hi)/2
        if mid>=0:critical.append({'x':str(sp.N(mid,40)),'P':str(sp.N(P.as_expr().subs(x,mid),40))})
    return {'coefficients_exact_decimals':[str(v) for v in cs],'P':str(P.as_expr()),
            'real_root_isolations':roots,'nonnegative_critical_points':critical,
            'P_at_zero':str(P.eval(0)),
            'positive_root_count':sum(v['positive'] for v in roots)}


def spline_domain(summary,xmin,xmax):
    knots=np.log1p(np.array([.001,.1,.3,.6,1.,2.3]))
    spl=CubicSpline(knots,np.array(summary['beta']),bc_type='natural')
    mag=5/np.log(10.)
    records=[]; inside_roots=[]
    for i in range(len(knots)-1):
        # scipy local polynomial S=c0*y^3+c1*y^2+c2*y+c3, y=x-x_i.
        pp=np.polynomial.Polynomial([spl.c[2,i],2*spl.c[1,i],3*spl.c[0,i]])/mag
        poly=1+np.polynomial.Polynomial([knots[i],1])*pp
        a=xmin if i==0 else knots[i]
        b=xmax if i==len(knots)-2 else knots[i+1]
        a=max(a,xmin);b=min(b,xmax)
        roots=[]
        for v in poly.roots():
            if abs(v.imag)<1e-10:
                xx=float(v.real+knots[i]); roots.append(xx)
                if a<=xx<=b:inside_roots.append(xx)
        test=[a,b]
        for v in poly.deriv().roots():
            if abs(v.imag)<1e-10 and a<=v.real+knots[i]<=b:test.append(float(v.real+knots[i]))
        vals=[float(poly(v-knots[i])) for v in test]
        records.append({'interval_index':i,'valid_intersection':[float(a),float(b)],
                        'P_real_roots_global_x':roots,'minimum_P_in_intersection':min(vals)})
    # Literal scipy extrapolation uses the terminal polynomial, not a native tail.
    final_i=len(knots)-2
    pp=np.polynomial.Polynomial([spl.c[2,final_i],2*spl.c[1,final_i],3*spl.c[0,final_i]])/mag
    poly=1+np.polynomial.Polynomial([knots[final_i],1])*pp
    extrap=[float(v.real+knots[final_i]) for v in poly.roots()
            if abs(v.imag)<1e-10 and v.real+knots[final_i]>=knots[-1]]
    return {'knots_x':knots.tolist(),'records':records,'roots_in_data_interval':inside_roots,
            'minimum_P_in_data_interval':min(r['minimum_P_in_intersection'] for r in records),
            'literal_terminal_polynomial_extrapolation_roots':extrap,
            'terminal_cubic_coefficient':float(spl.c[0,-1]),
            'scope':'float64 fixed-coefficient polynomial analysis; spline global extension is not physically justified'}


def main():
    fits=json.loads(FIT.read_text());dia=json.loads(DIA.read_text())
    xmin=math.log1p(dia['primary_z_min']);xmax=math.log1p(dia['primary_z_max'])
    domains={f:exact_domains(fits[f]['beta'][1:]) for f in ['F2','F3']}
    a,b=fits['F2']['beta'][1:]
    star=brentq(lambda x:1+a*x+2*b*x*x,1.,4.,xtol=1e-14)
    Fstar=star*math.exp(a*star+b*star*star)
    derivativeP=a+4*b*star
    coefficientH=math.exp(star-a*star-b*star*star)/(-derivativeP)
    f2={'x_star':star,'z_star':math.expm1(star),'F_star':float(Fstar),'P_prime_star':derivativeP,
        'a_scale_star':math.exp(-star),'H_over_h0_leading_C_over_xstar_minus_x':coefficientH,
        'proper_lookback_h0_at_star':quad(lambda x:math.exp(a*x+b*x*x-x)*(1+a*x+2*b*x*x),0,star,
                                        epsabs=1e-12,epsrel=1e-12)[0],
        'affine_extent_h0_at_star':quad(lambda x:math.exp(a*x+b*x*x-2*x)*(1+a*x+2*b*x*x),0,star,
                                     epsabs=1e-12,epsrel=1e-12)[0],
        'curved_turning_point_kappa':1/float(Fstar)**2,
        'curved_turning_limit_E':math.exp(star)/math.sqrt(-float(Fstar)*math.exp(a*star+b*star*star)*derivativeP)}
    # Tail terms are classified analytically, point-estimate only.
    f3={'Fprime_positive_all_x_ge_0':domains['F3']['positive_root_count']==0,
        'cubic_exponent_c':fits['F3']['beta'][3],'c_sigma':fits['F3']['sigma'][3],
        'tail':'c>0 forces F, e^-x F, proper-lookback and affine integrals to diverge; H and flat curvature tend to zero. Fixed extrapolated central coefficients only.'}
    rows=[];jac_checks=[]
    for family in ['F2','F3']:
        coefs=np.array(fits[family]['beta'][1:]);vc=np.array(fits[family]['parameter_covariance'])[1:,1:]
        for z in [.05,.1,.3,.6,1.,2.,dia['primary_z_max']]:
            x=math.log1p(z);F,P,E,q,AP=central(coefs,x);J=jacobian(coefs,x)
            sigmas=[math.sqrt(max(float(j@vc@j),0)) for j in J]
            rows.append({'family':family,'z':z,'x':x,'F':float(F),'P':float(P),'E':float(E),
                         'sigma_E_local':sigmas[0],'q_dec':float(q),'sigma_q_dec_local':sigmas[1],
                         'AP':float(AP),'sigma_AP_local':sigmas[2]})
            for eps in [1e-4,1e-5,1e-6]:
                fd=np.empty((3,len(coefs)))
                for j in range(len(coefs)):
                    plus=coefs.copy();minus=coefs.copy();plus[j]+=eps;minus[j]-=eps
                    vp=central(plus,x);vm=central(minus,x)
                    fd[:,j]=(np.array(vp[2:])-np.array(vm[2:]))/(2*eps)
                jac_checks.append({'family':family,'z':z,'epsilon':eps,
                    'scaled_max_error':float(np.max(np.abs(fd-np.array(J))/(1+np.abs(J))))})
    with (ROOT/'data_inverse_values.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
    spline=spline_domain(fits['F4'],xmin,xmax)
    sens=[]
    for r in json.loads((DATA/'results/sensitivity.json').read_text()):
        if r['family'] in ['F2','F3']:
            sens.append({'variant':r['variant'],'family':r['family'],'shape_coefficients':r['beta'][1:],
                         'shape_sigma':r['sigma'][1:]})
    # Plots show coefficient uncertainty only on the measured interval.
    fig,axs=plt.subplots(1,3,figsize=(14,4.2),constrained_layout=True)
    xx=np.linspace(xmin,xmax,300)
    for family,color in [('F2','#2463a6'),('F3','#a14392')]:
        coefs=np.array(fits[family]['beta'][1:]);vc=np.array(fits[family]['parameter_covariance'])[1:,1:]
        F,P,E,q,AP=central(coefs,xx)
        j=np.array([xx**power for power in range(1,len(coefs)+1)]).T
        sig=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',j,vc,j),0))
        axs[0].plot(np.expm1(xx),F,label=family,color=color)
        axs[0].fill_between(np.expm1(xx),F*np.exp(-sig),F*np.exp(sig),alpha=.16,color=color)
        lim=star-.015 if family=='F2' else 9.
        xt=np.linspace(0,lim,800);ft,pt,et,qt,apt=central(coefs,xt)
        axs[1].plot(xt,et,label=family,color=color)
        lam=[quad(lambda u: math.exp(sum(c*u**j for j,c in enumerate(coefs,1))-2*u)
                  *(1+sum(j*c*u**j for j,c in enumerate(coefs,1))),0,float(v),
                  epsabs=1e-10,epsrel=1e-10)[0] for v in xt[::8]]
        axs[2].plot(xt[::8],lam,label=family,color=color)
    axs[0].set(xlabel='redshift z',ylabel='normalized geometric screen radius F',title='Fit interval; local 1 sigma coefficient bands')
    axs[1].set(xlabel='x = log(1+z)',ylabel='H / h0',title='Literal flat-history extrapolations',yscale='log')
    axs[2].set(xlabel='x = log(1+z)',ylabel='h0 times past affine extent',title='Finite versus divergent affine tail',yscale='symlog')
    for ax in axs[1:]:
        ax.axvspan(0,xmax,color='grey',alpha=.12,label='data x range (nearby limit included)')
        ax.axvline(star,ls=':',color='#2463a6',lw=1)
    for ax in axs:ax.legend(fontsize=8);ax.grid(alpha=.2)
    fig.suptitle('Conditional supplied homogeneous metrics; no native UDT selection or tail evidence',fontsize=11)
    fig.savefig(ROOT/'conditional_inverse_comparison.png',dpi=180)
    fig.savefig(ROOT/'conditional_inverse_comparison.svg')
    input_paths=[FIT,DIA,DATA/'fit_empirical.py',DATA/'results/sensitivity.json']
    output={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths},
            'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,'matplotlib':matplotlib.__version__},
            'data_domain':{'x_min':xmin,'x_max':xmax,'z_max':dia['primary_z_max']},
            'exact_point_estimate_domains':domains,'F2_endpoint':f2,'F3_tail':f3,'F4_domain':spline,
            'jacobian_step_checks':jac_checks,'sensitivity_coefficients_no_refits':sens,
            'scope':'Exposed fixed coefficients; inverse restricted to supplied homogeneous class. No native selection, new data test, retuning or global-tail confidence.',
            'passed':domains['F2']['positive_root_count']==1 and star>xmax
                     and f3['Fprime_positive_all_x_ge_0'] and not spline['roots_in_data_interval']
                     and max(r['scaled_max_error'] for r in jac_checks if r['epsilon']==1e-6)<1e-7}
    print(json.dumps(output,indent=2,allow_nan=False))
    if not output['passed']:raise SystemExit(1)


if __name__=='__main__':main()
