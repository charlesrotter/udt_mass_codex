#!/usr/bin/env python3
"""Source/version correspondence plus separate standard-library saved-readout arithmetic."""
from pathlib import Path
import json,hashlib,math,csv,io
P=Path(__file__).resolve().parent;R=P.parent
freeze=json.loads((P/'CANDIDATE_FREEZE.json').read_text());amend=json.loads((P/'OUTPUT_CAPTURE_AMENDMENT.json').read_text())
for n,h in freeze['sha256'].items():
    target=P/'INITIAL_check_broader.py' if n.endswith('/check_broader.py') else R/n
    assert hashlib.sha256(target.read_bytes()).hexdigest()==h,n
assert hashlib.sha256((P/'check_broader.py').read_bytes()).hexdigest()==amend['current_code_sha256']
for n,h in json.loads((P/'SOURCE_PINS.json').read_text())['sha256'].items():
    assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
old=json.loads((P/'checks/broader_initial.stdout').read_text());d=json.loads((P/'checks/broader_complete_capture.stdout').read_text())
projected=json.loads(json.dumps(d))
for x in projected['reverse']:x.pop('forward_input')
assert projected==old,'A supposedly output-only amendment changed an original payload value'
assert d['status']=='PASS' and d['check_count']==len(d['checks'])==1269
assert len(d['records'])==8 and len(d['events'])==len(d['reverse'])==4
for stem,message in [('mutant_drop_cross','lambda_time_constraint'),('mutant_source_epoch','actual_source_frequency')]:
    v=json.loads((P/f'checks/{stem}.stdout').read_text());r=json.loads((P/f'checks/{stem}.json').read_text())
    assert v['status']=='FAIL' and message in v['failure'] and r['returncode']==1 and not r['timeout']

def det(m):return m[0][0]*m[1][1]-m[0][1]*m[1][0]
def close(a,b,tol=2e-7):assert abs(a-b)<=tol*(1+abs(b)),(a,b,tol)
rows=[]
for x in d['records']:
    endpoint=max(abs(a-b) for a,b in zip(x['state'][:3],[1.7,1.2,.7]));close(endpoint,x['endpoint_residual'],1e-15);assert endpoint<=2e-8
    area=abs(det(x['screen_map']));close(area,x['area'],2e-13);close(math.prod(x['widths']),area,2e-13)
    rows.append({'profile':x['epsilon'],'source_clock':x['source_clock'],'te':x['te'],'to':x['to'],'clock_ratio':x['R'],'source_sky':json.dumps(x['source_sky']),'arrival_sky':json.dumps(x['arrival_sky']),'width1':x['widths'][0],'width2':x['widths'][1],'area':area,'endpoint_residual':endpoint})
reverse_errors=[]
for x in d['reverse']:
    f=x['forward_input'];af=abs(det(f['screen_map']));ar=abs(det(x['reverse_map']));close(ar,x['reverse_area'],2e-13)
    close(af/ar,f['R']**2);reverse_errors.append(abs(af/ar-f['R']**2))

def gauss_weight(n,x):
    p0=1.;p1=x
    for j in range(2,n+1):p0,p1=p1,((2*j-1)*x*p1-(j-1)*p0)/j
    derivative=n*(x*p1-p0)/(x*x-1)
    return 2/((1-x*x)*derivative*derivative)
for e in d['events']:
    a,b=[r for r in d['records'] if r['epsilon']==e['profile']]
    duration=b['arrival_clock']-a['arrival_clock'];close(duration,e['arrival_duration'],2e-14)
    close(duration/.8,e['mean_Z'],2e-14)
    for n in (8,16):
        value=.4*sum(gauss_weight(n,node['s']/.4-1)*node['R'] for node in e['nodes'] if node['n']==n)
        close(value,e[f'quad{n}'],2e-12)
    modes,amps,phases=d['profiles'][e['profile']]
    q=sum(a*math.cos(.75*n*.7+ph) for n,a,ph in zip(modes,amps,phases));close(q,e['Q_A'],2e-14)
with (P/'MAIN_RECORDS.tsv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
events=[{k:v for k,v in e.items() if k!='nodes'} for e in d['events']]
with (P/'EVENT_RECORDS.tsv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(events[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(events)
print(json.dumps({'status':'PASS','source_and_initial_freeze_correspondence':True,'output_amendment_preserves_all_original_payload_values_exactly':True,'main_records':8,'event_records':4,'guards':1269,'reverse_ratio_max_abs':max(reverse_errors),'independent_arithmetic':'Standard-library saved determinants, durations and Legendre-recursion Gauss weights; no new trajectory or source-theorem reproof.','original_endpoint_max_all_calls':max(x['error'] for x in d['checks'] if x['name']=='original_endpoint'),'actual_Ricci_fd_max':max(x['error'] for x in d['checks'] if x['name']=='original_Ricci_reduction_with_actual_metric_derivatives')},indent=2))
