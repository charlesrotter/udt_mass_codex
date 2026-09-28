"""Bounded actual author-artifact mutations, preserving every failure payload."""
from pathlib import Path
import json,subprocess,sys
root=Path(__file__).resolve().parents[2]
pkg=root/'udt_machian_global_clock_feasibility_2026-09-28'
review=pkg/'review'
author=pkg/'check_machian.py'
source=author.read_text()
outdir=review/'mutations'
outdir.mkdir(exist_ok=False)
cases=[
 ('fixed_mass', 'Q.subs(L,G*M/(q*c**2))', 'Q.subs(L,G*M/(2*q*c**2))', 'fixed_mass_scale'),
 ('fixed_density', 'L,c*S.sqrt(q/(C*G*rho))', 'L,2*c*S.sqrt(q/(C*G*rho))', 'density_scale'),
 ('elapsed_time','fl=lam*f(t/lam)','fl=f(t/lam)','rescaled_arrival_map'),
 ('label_density','(lam*(mu1+mu2)/J2)/(lam*(mu1+mu2)/J1)','(2*lam*(mu1+mu2)/J2)/(lam*(mu1+mu2)/J1)','measure_normalization_transfer_ratio'),
 ('Friedmann','rhoc=3*H**2/(8*S.pi*G)','rhoc=6*H**2/(8*S.pi*G)','flat_friedmann_compactness_identity'),
 ('dust_density','rhoE=c*c/(4*S.pi*G*a*a)','rhoE=c*c/(8*S.pi*G*a*a)','static_original_Einstein_equation'),
 ('Lambda','Lambda=1/a**2','Lambda=2/a**2','static_original_Einstein_equation'),
 ('volume','vol=S.integrate(a**3*S.sin(chi)**2*S.sin(theta),(phi,0,2*S.pi),(theta,0,S.pi),(chi,0,S.pi))','vol=4*S.pi*a**3/3','S3_volume'),
 ('clock_ratio','Z=S.diff(arrival,t)','Z=2*S.diff(arrival,t)','static_tick_ratio')]
records=[]
for name,before,after,catch in cases:
 assert source.count(before)==1,(name,source.count(before))
 target=outdir/(name+'.py')
 target.write_text(source.replace(before,after))
 runner="from pathlib import Path; p=Path("+repr(str(target))+"); exec(compile(p.read_text(),"+repr(str(author)) +",'exec'),{'__file__':"+repr(str(author)) +",'__name__':'__main__'})"
 cmd=[sys.executable,'-c',runner]
 run=subprocess.run(cmd,cwd=root,capture_output=True,timeout=10)
 (outdir/(name+'.stdout')).write_bytes(run.stdout)
 (outdir/(name+'.stderr')).write_bytes(run.stderr)
 # Reject only the intended explicit assertion, not an arbitrary import/error.
 assert run.returncode==1,(name,run.returncode,run.stderr.decode())
 assert 'AssertionError' in run.stderr.decode() and catch in run.stderr.decode(),(name,run.stderr.decode())
 records.append(dict(name=name,changed_expression=[before,after],command=cmd,returncode=run.returncode,expected_assertion=catch,expected_failure_observed=True))
print(json.dumps(dict(status='PASS_EXPECTED_FAILURES',total=len(records),records=records,
 scope='Actual mutated producer payloads; unchanged science/source files; author replay is regression only'),indent=2))
