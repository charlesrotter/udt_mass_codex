import numpy as np, sympy as sp
from VERIF_indep_gr import eval_indep, comp_keys
import axisym_einstein_analytic as GE
rs, ths = sp.symbols('rs ths')
rng=np.random.default_rng(7)
worst=0.0
for trial in range(5):
    rv=float(rng.uniform(0.5,5.0)); thv=float(rng.uniform(0.3,2.8))
    ca=rng.uniform(-0.4,0.4,4)
    fields={
      'a': ca[0]*sp.exp(-rs/3)*sp.cos(ths)+0.05*rs+ca[1]*sp.sin(2*ths),
      'b': ca[2]*sp.exp(-(rs-1)**2)+0.1*sp.cos(2*ths)+0.07*sp.sin(ths)*rs,
      'c': ca[3]*sp.sin(ths)**2*sp.exp(-rs/4)+0.06*sp.cos(ths),
      'd': -0.09*sp.cos(ths)*sp.exp(-rs/5)+0.03*rs*sp.sin(ths)+ca[0]*0.2*sp.sin(3*ths),
    }
    vals={}
    for nm,expr in fields.items():
        sub={rs:rv,ths:thv}
        vals[nm]=float(expr.subs(sub))
        vals[nm+'_r']=float(sp.diff(expr,rs).subs(sub))
        vals[nm+'_t']=float(sp.diff(expr,ths).subs(sub))
        vals[nm+'_rr']=float(sp.diff(expr,rs,2).subs(sub))
        vals[nm+'_tt']=float(sp.diff(expr,ths,2).subs(sub))
        vals[nm+'_rt']=float(sp.diff(expr,rs,ths).subs(sub))
    mine=eval_indep(rv,thv,vals)
    comm=GE.Gmix_components(rv,thv,vals['a'],vals['b'],vals['c'],vals['d'],
        vals['a_r'],vals['b_r'],vals['c_r'],vals['d_r'],
        vals['a_t'],vals['b_t'],vals['c_t'],vals['d_t'],
        vals['a_rr'],vals['b_rr'],vals['c_rr'],vals['d_rr'],
        vals['a_tt'],vals['b_tt'],vals['c_tt'],vals['d_tt'],
        vals['a_rt'],vals['b_rt'],vals['c_rt'],vals['d_rt'])
    for k in comp_keys:
        d=abs(mine[k]-comm.get(k,np.nan)); worst=max(worst,d)
    print(f"trial {trial} r={rv:.2f} th={thv:.2f}  max_comp_diff={max(abs(mine[k]-comm.get(k,np.nan)) for k in comp_keys):.2e}  G^r_th={mine[(1,2)]:+.3e}")
print(f"\nWORST abs diff across all trials/components: {worst:.2e}")
