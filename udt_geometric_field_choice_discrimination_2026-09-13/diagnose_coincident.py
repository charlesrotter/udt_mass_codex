from pathlib import Path
import sympy as s,json,sys
t=s.symbols('t',positive=True)
q0,p0,r0,s0=s.symbols('q0 p0 r0 s0',real=True)
nu=s.sqrt(7)/2
q=(q0+p0)*t*t/3+(2*q0-p0)/(3*t)
r=s.sqrt(t)*(r0*s.cos(nu*s.log(t))+(s0-r0/2)*s.sin(nu*s.log(t))/nu)
e=s.sqrt(2)*s.Matrix([s.diff(q,t),s.diff(r,t)])
M=e.subs(t,1).col_join(e).jacobian([q0,p0,r0,s0])
raw=M.det(); coincident=M.subs(t,1); simplified=s.simplify(raw)
checks={'entries_finite':not any(x.has(s.nan,s.zoo,s.oo,-s.oo) for x in coincident),
 'repeated_original_rows':coincident[:2,:]==coincident[2:,:],
 'original_matrix_determinant_zero':coincident.det()==0,
 'original_matrix_rank_two':coincident.rank()==2,
 'simplified_determinant_at_one_zero':simplified.subs(t,1)==0,
 'determinant_limit_zero':s.limit(raw,t,1)==0}
result={'question':'finite coincident map versus singular symbolic determinant representation',
 'raw_determinant':str(raw),'raw_substitution':str(raw.subs(t,1)),
 'simplified_determinant':str(simplified),'coincident_matrix':str(coincident),
 'rank':coincident.rank(),'checks':checks,'all_pass':all(checks.values())}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result));sys.exit(0 if result['all_pass'] else 1)
