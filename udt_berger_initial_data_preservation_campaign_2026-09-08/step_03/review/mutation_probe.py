"""Post-exposure actual author-program mutations; all text/streams retained."""
import contextlib,hashlib,io,json,pathlib,traceback
import sympy as s
p=pathlib.Path(__file__).resolve().parent
source_path=p.parent/'check_bi3.py'
original=source_path.read_text()
saved=json.loads((p/'candidate_snapshots/author_mutations_01.stdout').read_text())
assert hashlib.sha256(original.encode()).hexdigest()==saved['original_sha256']
expected_replacements=[
 ('z=(E-m*m+r*r+w*w)/(2*m)','z=(E-m*m-r*r-w*w)/(2*m)'),
 ('G[j][j][l]*K[l,i]+G[j][i][l]*K[j,l]','s.S.Zero'),
 ('tangent[i,j]+[b1,b2][i]*normal[j]','tangent[i,j]'),
 ('Q[1][0,j]+Q[2][1,j]','Q[1][0,j]+Q[2][0,j]'),
 ("zero('full Ricci variation of realized two-jet'","Sdot=-Sdot\nzero('full Ricci variation of realized two-jet'")]
results=[]
def execute(name,source):
    out,err=io.StringIO(),io.StringIO()
    namespace={'__name__':'__main__','__file__':str(source_path)}
    failure=None
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        try:exec(compile(source,'<BI3 reviewer mutation '+name+'>','exec'),namespace)
        except Exception as exc:
            failure={'type':type(exc).__name__,'message':str(exc)}
            traceback.print_exc()
    result=dict(name=name,mutant_sha256=hashlib.sha256(source.encode()).hexdigest(),
                mutant_source=source,stdout=out.getvalue(),stderr=err.getvalue(),failure=failure,
                rejected=failure is not None)
    return result,namespace
for item,(before,after) in zip(saved['results'],expected_replacements):
    assert original.count(before)==1
    source=original.replace(before,after,1)
    assert source==item['mutant_source']
    result,namespace=execute(item['name'],source)
    assert result['failure']==item['failure'],result['name']
    assert result['failure']['type']=='AssertionError'
    results.append(result)

before='Bdot=Sdot+2*h*B'
assert original.count(before)==1
extra,ns=execute('delete_inverse_metric_derivative',original.replace(before,'Bdot=Sdot',1))
assert extra['failure'] is None
printed=json.loads(extra['stdout'])
assert printed['status']=='PASS' and len(printed['checks'])==55
# Independent full endomorphism-rate anchor from connection variation plus d gamma^-1.
eps,h,pv,qv=ns['eps'],ns['h'],ns['p'],ns['q']
expectedS=s.Matrix([[0,0,0],[0,0,eps],[0,eps,0]])
expectedB=s.diag(pv*qv-qv*qv/2,pv*qv-qv*qv/2,qv*qv/2)
diff=s.simplify(ns['Bdot']-(expectedS+2*h*expectedB))
assert diff[2,2]==-h*qv*qv
assert diff!=s.zeros(3)
extra.update(author_harness_result='FALSE_PASS_FOR_FULL_BDOT',independent_anchor='REJECTED',
             independent_full_Bdot_difference=str(diff),
             scoped_drift_effect='None: the omitted term is diagonal at K=h gamma. Original candidate retains it correctly.')
results.append(extra)
print(json.dumps(dict(status='PASS',original_sha256=saved['original_sha256'],
    replayed_author_rejections=5,additional_full_Bdot_false_passes=1,
    source_identity_caveat='Mutant internal __file__ hash identifies unchanged original; enclosing digest and complete source identify actual executed mutant.',
    results=results,
    verdict_scope='The five frozen author catches reproduce. A sixth program passes all55 author checks after deleting the diagonal raising term; independent full-tensor anchor catches it. This limits harness coverage, not local realization or original drift correctness.'),indent=2))
