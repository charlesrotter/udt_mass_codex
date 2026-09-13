#!/usr/bin/env python3
"""Read-only scientific artifact extraction into package-owned new summaries."""
from pathlib import Path
import json,csv,hashlib,datetime
import numpy as np
P=Path(__file__).resolve().parent
full=P/'checks/evolving_repaired.stdout';routes=P/'checks/routes.stdout'
d=json.loads(full.read_text());r=json.loads(routes.read_text());assert d['status']==r['status']=='PASS'
rows=[]
for x in d['records']:
 f=x['frozen_control'];angle=np.arccos(np.clip(np.dot(x['arrival_sky'],f['arrival_sky']),-1,1))*180/np.pi
 rows.append(dict(epsilon=x['epsilon'],source_clock=x['source_clock'],emission_t=x['te'],arrival_t=x['to'],arrival_clock=x['arrival_clock'],R=x['R'],area=x['area'],width_max=x['widths'][0],width_min=x['widths'][1],shape=x['widths'][0]/x['widths'][1],full_flight=x['flight'],frozen_flight=f['flight'],frozen_area=f['area'],frozen_shape=f['widths'][0]/f['widths'][1],arrival_sky_contrast_deg=float(angle),endpoint_residual=x['endpoint_residual']))
with (P/'step_03/FINITE_RECORDS.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
events=[{k:v for k,v in x.items() if k!='quadratures'} for x in d['events']]
for e in events:e['initial_pulse_relative_duration_error']=e['single_initial_pulse_duration_error']/e['arrival_duration']
with (P/'step_05/EVENT_RECORDS.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(events[0]),delimiter='\t');w.writeheader();w.writerows(events)
summary={'sources':{str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [full,routes]},'full_cases':len(rows),'parent_guard_count':len(d['checks']),'route_cases':len(r['records']),'events':events,'max_scaled_errors':{name:max(c['error'] for c in d['checks'] if c['name']==name) for name in sorted(set(c['name'] for c in d['checks']))},'maximum_endpoint_residual':max(x['endpoint_residual'] for x in rows),'scope':'Finite floating-point records; no global, physical or observational claim.'}
(P/'CHECK_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
text=['# CSS finite numerical illustrations','','Computed from saved artifacts; source SHA-256 correspondence is in CHECK_SUMMARY.json.','Times and areas here use supplied dimensionless units L/c_E=1 and L²=1.','These are hypothetical geometry records, not measured physical data.','','| epsilon | initial pulse ratio | whole-event ratio | initial-pulse duration error |','|---:|---:|---:|---:|']
for e in events:text.append(f"| {e['epsilon']:+.1f} | {e['initial_R']:.6f} | {e['mean_R']:.6f} | {100*e['initial_pulse_relative_duration_error']:.2f}% |")
text+=['','All source events span1.2 proper-clock units. The reported error is','(initial-pulse predicted duration - actual duration)/actual duration.','Its positive sign is a property of these cases, not a general sign theorem.','','At the common source epoch s=0, the same instantaneous metric values give:','','| epsilon | full coordinate flight | frozen coordinate flight | forward beam area |','|---:|---:|---:|---:|']
for x in rows:
 if x['source_clock']==0:text.append(f"| {x['epsilon']:+.1f} | {x['full_flight']:.6f} | {x['frozen_flight']:.6f} | {x['area']:.6f} |")
text+=['','The prescribed initial time derivatives differ. Frozen controls coincide at','this epoch; their equality does not imply equal full initial data/developments.','Angles, both widths and all12 records are in step_03/FINITE_RECORDS.tsv.','Local sky comparisons retain each metric’s supplied tetrad/axis marking.','','For the supplied guided loop R=1,L/c_E=1.7,b_*=0,kappa=.02,t_e=1,','opposite proper travel times are10.352768 and11.024121. Their plus-minus','difference is -0.671354; freezing b at its zero initial value gives zero.','The opposite tagged pulse slopes are0.939101 and1.064848. This is the explicit','guide rule, not a free-ray/energy or native dynamical claim.','','Parent output has1044 finite evolving guards; pass counts are procedural','coverage, not independent theorems. Separate reviewer calculations own','independent original-geodesic/finite-angle and full-metric-loop checks.']
(P/'NUMERICAL_RESULTS.md').write_text('\n'.join(text)+'\n')
print(json.dumps({'status':'PASS','finite_records':len(rows),'events':len(events),'source_hashes':summary['sources']}))
