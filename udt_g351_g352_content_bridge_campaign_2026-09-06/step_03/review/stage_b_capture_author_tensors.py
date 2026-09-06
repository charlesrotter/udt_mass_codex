"""Expose computed candidate arrays for comparison; this is author-code replay."""
import argparse, contextlib, io, json, pathlib, runpy, sys
p=argparse.ArgumentParser(); p.add_argument('--repo',type=pathlib.Path,required=True)
a=p.parse_args(); repo=a.repo.resolve()
candidate=repo/'udt_g351_g352_content_bridge_campaign_2026-09-06/step_03/check_harmonic_wave.py'
sys.argv=[str(candidate)]
out=io.StringIO()
with contextlib.redirect_stdout(out): ns=runpy.run_path(str(candidate),run_name='__main__')
def sparse(T): return {''.join(map(str,k)):str(v) for k,v in T.items() if v!=0}
print(json.dumps({'label':'Exposed author-code array capture, not independent computation',
    'candidate_stdout':json.loads(out.getvalue()),
    'Gamma':sparse(ns['G']),'R':sparse(ns['R']),'W':sparse(ns['W']),
    'starW':sparse(ns['D']),'B':sparse(ns['B']),
    'Ricci':[[str(z) for z in ns['Ric'].row(i)] for i in range(4)]},indent=2))
