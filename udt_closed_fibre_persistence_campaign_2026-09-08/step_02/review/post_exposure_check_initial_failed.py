"""Post-exposure reproduction, independently assembled anchors, actual mutants."""
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import sys
import sympy as S

HERE=pathlib.Path(__file__).resolve().parent
AUTHOR=HERE.parent
spec=importlib.util.spec_from_file_location('sealed_independent',HERE/'independent_check.py')
ind=importlib.util.module_from_spec(spec);spec.loader.exec_module(ind)

def execute(source,mode='baseline'):
    out=io.StringIO();err=io.StringIO();old=sys.argv
    ns={'__name__':'__main__','__file__':str(AUTHOR/'check_cf2.py')}
    code=0
    try:
      sys.argv=[str(AUTHOR/'check_cf2.py'),mode]
      with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        try:exec(compile(source,'CF2_POST_EXPOSURE_IN_MEMORY','exec'),ns)
        except SystemExit as ex:code=ex.code or 0
    finally:sys.argv=old
    return {'mode':mode,'returncode':code,'stdout':out.getvalue(),'stderr':err.getvalue()},ns

source=(AUTHOR/'check_cf2.py').read_text()
pins={n:hashlib.sha256((AUTHOR/n).read_bytes()).hexdigest()==h for h,n in re.findall(r'^    ([0-9a-f]{64})  (.+)$',(AUTHOR/'CANDIDATE_FREEZE.md').read_text(),re.M)}
assert all(pins.values())
records=[]
for mode in ['baseline','omit_inverse','kill_polarization','wrong_slope','wrong_phase']:
    rec,ns=execute(source,mode)
    rec['stdout_matches_author']=rec['stdout'].encode()==(AUTHOR/f'check_{mode}.stdout').read_bytes()
    rec['stderr_matches_author']=rec['stderr'].encode()==(AUTHOR/f'check_{mode}.stderr').read_bytes()
    rec['saved_receipt_returncode_matches']=rec['returncode']==json.loads((AUTHOR/f'check_{mode}.json').read_text())['returncode']
    assert rec['stdout_matches_author'] and rec['stderr_matches_author'] and rec['saved_receipt_returncode_matches']
    rec['summary']=json.loads(rec['stdout'])['failed']
    records.append(rec)
    if mode=='baseline':baseline_ns=ns

# Fresh rational-jet recomputation from the sealed review implementation, using
# the author's polarization convention. No author differential code is called.
s=S.symbols('s',positive=True);f=S.Function('f')(s)
gg=ind.geometry(s,S.Integer(1),S.Integer(2))
w=s*(1-s)
theta2=S.Matrix([0,-S.sqrt(w),S.sqrt(w)])
theta3=S.Matrix([0,2*(1-s),2*s])
E=theta2*theta3.T+theta3*theta2.T
K=E*f
anchors=[]
for ss in [S.Rational(1,2),S.Rational(1,5),S.Rational(4,5),S.Rational(1,10)]:
    F0,F1,F2=S.symbols('F0 F1 F2')
    subs={S.diff(f,s,2):F2,S.diff(f,s):F1,f:F0}
    gj=[gg.diff(s,j).subs(s,ss) for j in range(3)]
    kj=[K.diff(s,j).xreplace(subs).subs(s,ss) for j in range(3)]
    directR,directS=ind.ricci_direct_jet(*gj,*kj)
    covS=ind.ricci_covariant_jet(*gj,*kj)
    assert S.simplify(covS-directS)==S.zeros(3)
    inv=gj[0].inv();xx=S.Matrix([0,S.Rational(1,2),S.Rational(1,2)])
    pp=S.eye(3)-xx*(gj[0]*xx).T
    y=pp*(inv*covS+2*inv*kj[0]*inv*directR)*xx/12
    slope=S.factor(2*(y[2]-y[1]))
    # Parse only the saved scalar output; independently assembled all-tensor
    # comparisons above are not a replay of its implementation.
    ans_s=baseline_ns['s'];ans_f=baseline_ns['f']
    expected=baseline_ns['Dfull'].xreplace({S.diff(ans_f,ans_s,2):F2,S.diff(ans_f,ans_s):F1,ans_f:F0}).subs(ans_s,ss)
    assert S.simplify(slope-expected)==0
    # Compare all 9 author dRic entries at each independent rational jet.
    saved_tensor=baseline_ns['dRic'].applyfunc(lambda v:v.xreplace({S.diff(ans_f,ans_s,2):F2,S.diff(ans_f,ans_s):F1,ans_f:F0}).subs(ans_s,ss))
    assert S.simplify(saved_tensor-covS)==S.zeros(3)
    anchors.append({'s':str(ss),'slope':str(slope),'all9_dRic_match':True,'all9_independent_routes_match':True})

# Actually execute false-pass probes, preserving their full source and streams.
insert='xx=xi.subs({a:1,c:2}); pp=S.eye(3)-xx*(gg*xx).T'
assert source.count(insert)==1
mutations={
 'discard_Ricci_lower_jets':source.replace(insert,"dRic=dRic.applyfunc(lambda v:v.xreplace({f:S.S(0),S.diff(f,s):S.S(0)}))\n"+insert),
 'reverse_TT_projection_sign':source.replace('piE=S.simplify(E-longitudinal(M.inv()*gi*E*zup))','piE=S.simplify(E+longitudinal(M.inv()*gi*E*zup))')
}
assert all(src!=source for src in mutations.values())
mutant_records=[]
for name,src in mutations.items():
    rec,ns=execute(src)
    rec.update(name=name,source=src,source_sha256=hashlib.sha256(src.encode()).hexdigest())
    rec['author_suite_false_pass']=rec['returncode']==0 and json.loads(rec['stdout'])['passed']==21
    assert rec['author_suite_false_pass'] and not rec['stderr']
    if name=='discard_Ricci_lower_jets':
      sf=ns['s'];ff=ns['f']
      def profile(expr,p):return S.simplify(expr.xreplace({S.diff(ff,sf,j):S.diff(p,sf,j) for j in range(3)}))
      const=profile(ns['Dfull'],S.Integer(1)).subs(sf,S.Rational(1,2))
      linear=profile(ns['Dfull'],sf-S.Rational(1,5)).subs(sf,S.Rational(1,5))
      rec['independent_fixture_catches']={'constant_center_expected':'-4/3','constant_center_mutant':str(const),'linear_one_fifth_expected':'1','linear_one_fifth_mutant':str(linear)}
      assert const!=-S.Rational(4,3) and linear!=1
    else:
      g=ns['g'];gi=ns['gi'];z=ns['z'];zu=ns['zup'];norm=ns['norm2'];M=ns['M']
      F=z*z.T-norm*g/3
      plus=S.simplify(F+ns['longitudinal'](M.inv()*gi*F*zu))
      divergence=S.simplify(plus*zu)
      assert any(S.simplify(x)!=0 for x in divergence)
      rec['independent_fixture_catches']={'nontransverse_tracefree_input':'ds tensor ds - |ds|^2 gamma/3','wrong_projection_divergence':[str(x) for x in divergence]}
    mutant_records.append(rec)

# Focused genuine suite failures when the missing fixtures are appended.
# These are reviewer probes, not an author repair or re-review cycle.
cut="failed=[n for n,v in checks.items() if not v]"
lower_guards="""constant_anchor=substitute_profile(Dfull,S.Integer(1)).subs(s,S.Rational(1,2))
linear_anchor=substitute_profile(Dfull,s-S.Rational(1,5)).subs(s,S.Rational(1,5))
ck('reviewer_constant_profile',zero(constant_anchor+S.Rational(4,3)))
ck('reviewer_linear_profile',zero(linear_anchor-1))
"""
projection_guard="""reviewer_F=z*z.T-norm2*g/3
reviewer_bad=reviewer_F+longitudinal(M.inv()*gi*reviewer_F*zup)
ck('reviewer_nontransverse_projection',zero(reviewer_bad*zup))
"""
focused=[]
for name,guard in [('discard_Ricci_lower_jets',lower_guards),('reverse_TT_projection_sign',projection_guard)]:
    src=mutations[name].replace(cut,guard+cut)
    rec,_=execute(src)
    rec.update(name=name,source=src,source_sha256=hashlib.sha256(src.encode()).hexdigest())
    assert rec['returncode']==1 and not rec['stderr']
    assert all(n.startswith('reviewer_') for n in json.loads(rec['stdout'])['failed'])
    focused.append(rec)

print(json.dumps({'status':'PASS_WITH_PRESERVED_FALSE_PASSES','exposure':'POST_SOURCE_FIRST_SEAL','freeze_pins':pins,'author_replays':records,'independent_full_operator_anchors':anchors,'actual_false_pass_probes':mutant_records,'focused_reviewer_catches':focused,'limits':'No numerical global TT/constraint/Cauchy solve; shared engine; replays are same-code regression; reviewer fixtures do not change author files.'},indent=2))
