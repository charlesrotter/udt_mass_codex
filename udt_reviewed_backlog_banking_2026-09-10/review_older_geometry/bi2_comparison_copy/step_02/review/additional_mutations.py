"""Actual additional author-program mutants, retained only under review.

Tests distinguish author assertion rejection from independent saved-control
correspondence. Every mutant has a real file; its self-hash is its actual hash.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import traceback
import sympy as s

r=Path(__file__).resolve().parent
path=r.parent/'check_bi2.py'
original=path.read_text()
sink=io.StringIO()
with contextlib.redirect_stdout(sink):
    ref=runpy.run_path(str(r/'source_first_check.py'))
mutations=[
('drop_spatial_bracket_motion',
 'nd=[n[i]*(tau-2*k[i]) for i in range(3)]',
 'nd=[s.S.Zero for i in range(3)]','assertion'),
('drop_trace_in_mixed_evolution',
 'kd=[r[i]+tau*k[i]-lam for i in range(3)]',
 'kd=[r[i]-lam for i in range(3)]','assertion'),
('keep_covariant_quadratic_in_mixed_evolution',
 'kd=[r[i]+tau*k[i]-lam for i in range(3)]',
 'kd=[r[i]+tau*k[i]-2*k[i]**2-lam for i in range(3)]','assertion'),
('reuse_two_eigenvalue_linear_projector',
 'P3=(s.diag(*rr)-rr[0]*s.eye(3))*(s.diag(*rr)-rr[1]*s.eye(3))/(gaps[0]*gaps[1])',
 'P3=(s.diag(*rr)-rr[0]*s.eye(3))/gaps[0]','assertion'),
('switch_to_a_different_simple_branch',
 'P3=(s.diag(*rr)-rr[0]*s.eye(3))*(s.diag(*rr)-rr[1]*s.eye(3))/(gaps[0]*gaps[1])',
 'P3=(s.diag(*rr)-rr[1]*s.eye(3))*(s.diag(*rr)-rr[2]*s.eye(3))/((rr[0]-rr[1])*(rr[0]-rr[2]))','assertion'),
('delete_unrotated_initial_horizontal_shear',
 'K0=s.Matrix([[mm+dd,ss,0],[ss,mm-dd,0],[0,0,k[2]]])',
 'K0=s.diag(mm,mm,k[2])','assertion'),
('wrong_sign_in_saved_geometric_control_Ricci',
 'rv=[s.factor(2*(v[i]**2-(v[(i+1)%3]-v[(i+2)%3])**2)/(v[0]*v[1]*v[2])) for i in range(3)]',
 'rv=[s.factor(-2*(v[i]**2-(v[(i+1)%3]-v[(i+2)%3])**2)/(v[0]*v[1]*v[2])) for i in range(3)]','independent_controls'),
('falsely_mark_every_control_as_directly_descended',
 'direct_descent=v[0]==v[1]',
 'direct_descent=True','independent_controls')]
results=[]
for name,before,after,expected in mutations:
    assert original.count(before)==1,(name,'mutation target count')
    mutant=original.replace(before,after,1)
    mp=r/'mutants'/(name+'.py')
    mp.parent.mkdir(exist_ok=True)
    with mp.open('x') as f:f.write(mutant)
    out,err=io.StringIO(),io.StringIO()
    failure=None
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        try:
            exec(compile(mutant,str(mp),'exec'),{'__name__':'__main__','__file__':str(mp)})
        except Exception as exc:
            failure=dict(type=type(exc).__name__,message=str(exc))
            traceback.print_exc()
    correspondence=[]
    if failure is None:
        payload=json.loads(out.getvalue())
        assert payload['status']=='PASS'
        assert payload['source_sha256']==hashlib.sha256(mp.read_bytes()).hexdigest()
        for index,control in enumerate(payload['controls']):
            values=list(map(s.Rational,control['squared_sizes']))
            substitution=dict(zip((ref['x'],ref['y'],ref['z']),values))
            B=ref['B'].subs(substitution)
            ricci=[s.factor(B[j,j]) for j in range(3)]
            gaps=[s.factor(ricci[2]-ricci[j]) for j in range(2)]
            direct=ref['Lq'].subs(substitution)==s.zeros(3)
            if list(map(str,ricci))!=control['Ricci']:
                correspondence.append(dict(control=index,field='Ricci',expected=list(map(str,ricci)),reported=control['Ricci']))
            if list(map(str,gaps))!=control['gaps']:
                correspondence.append(dict(control=index,field='gaps',expected=list(map(str,gaps)),reported=control['gaps']))
            if direct!=control['direct_descent']:
                correspondence.append(dict(control=index,field='direct_descent',expected=direct,reported=control['direct_descent']))
    rejected=failure is not None
    independent_rejection=bool(correspondence)
    assert rejected or independent_rejection,(name,'both methods falsely passed')
    if expected=='assertion':assert failure and failure['type']=='AssertionError',(name,failure)
    else:assert not rejected and independent_rejection,(name,failure,correspondence)
    results.append(dict(name=name,mutant_path=str(mp.relative_to(r)),
                        mutant_sha256=hashlib.sha256(mutant.encode()).hexdigest(),
                        author_rejected=rejected,author_failure=failure,
                        independent_control_rejected=independent_rejection,
                        independent_correspondence_failures=correspondence,
                        stdout=out.getvalue(),stderr=err.getvalue()))
print(json.dumps(dict(status='PASS',original_sha256=hashlib.sha256(original.encode()).hexdigest(),
    results=results,count=len(results),author_rejections=sum(v['author_rejected'] for v in results),
    author_false_passes_independently_detected=sum(v['independent_control_rejected'] for v in results),
    qualification='Six additional core defects rejected; two saved-control reporting defects survive author assertions but fail independent correspondence. Frozen original controls were separately verified correct. No completeness claim.'),indent=2))
