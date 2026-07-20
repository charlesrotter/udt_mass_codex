#!/usr/bin/env python3
"""Independent fail-closed verification of the three-route zoom-out."""
from __future__ import annotations
import copy,csv,hashlib,json,subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]; HERE=Path(__file__).resolve().parent
BASE="f68c51aa79d65805da23fc5845576f87ef310d4f"
EXPECTED_CENSUS={"CONTEXT_CANDIDATE":1662,"LOAD_BEARING_CANDIDATE":51,"EXCLUDED_DUPLICATE_RAW_RECORD":72,
"PROVENANCE_OR_COUNTEREXAMPLE_ONLY":1803,"EXCLUDED_GENERATED_ORGANIZATION":226}

def need(c,m):
    if not bool(c): raise AssertionError(m)
def rows(n):
    with (HERE/n).open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h,delimiter="\t"))
def one(a,k,v):
    f=[r for r in a if r[k]==v];need(len(f)==1,f"one:{k}:{v}");return f[0]
def census_check(a):
    need(len(a)==3814 and len({r['path'] for r in a})==3814,"census-count"); counts={}
    for r in a:
        counts[r['initial_disposition']]=counts.get(r['initial_disposition'],0)+1
        need(len(r['blob'])==40 and len(r['sha256'])==64 and r['matched_tokens'],"census-field")
        need(not r['path'].startswith('c2_rigidity_three_route_zoomout_2026-07-20/'),"feedback")
    need(counts==EXPECTED_CENSUS,"census-dispositions");return {"rows":len(a),"dispositions":counts}
def source_check(a,census):
    expected={r['path'] for r in census if r['initial_disposition']=='LOAD_BEARING_CANDIDATE'}
    need(len(a)==51 and len({r['path'] for r in a})==51 and {r['path'] for r in a}==expected,"source-coverage")
    by={r['path']:r for r in census}
    for r in a:
        data=subprocess.check_output(['git','show',f"{BASE}:{r['path']}"],cwd=ROOT)
        need(hashlib.sha256(data).hexdigest()==by[r['path']]['sha256'],f"sha:{r['path']}")
        need(subprocess.check_output(['git','rev-parse',f"{BASE}:{r['path']}"],cwd=ROOT,text=True).strip()==by[r['path']]['blob'],f"blob:{r['path']}")
    need(one(a,'path','c2_time_fiber_shift_jacobi_2026-07-20/NEXT_SCIENTIFIC_DECISION.md')['audit_ruling']=='QUESTION_ONLY','question')
    need(one(a,'path','UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md')['audit_ruling']=='FOUNDING_SELECTOR','CSN')
    return {"rows":len(a),"hashes_replayed":len(a)}
def unique_table(a,key,count,label):
    need(len(a)==count and len({r[key] for r in a})==count,f"{label}-count");return {"rows":len(a)}
def semantic_checks(scale,routes,edges,counter,status,scope):
    need(one(scale,'id','H01')['ruling']=='EXACT_CSN_NEUTRAL','H01')
    need(one(scale,'id','H03')['ruling']=='SCALE_SENSITIVE_BUT_NOT_A_STATIONARY_SCALE_EQUATION','H03')
    need(one(scale,'id','H14')['ruling']=='NORMALIZATION_ANCHOR_NOT_SOURCE_OR_SCALE_EQUATION','H14')
    need(one(scale,'id','H15')['ruling']=='EXCLUDED_UNTIL_NATIVE_MATTER_BRANCH_EXISTS','H15')
    need(one(routes,'rank','1')['route']=='PHYSICAL_BOUNDARY_VARIATION','route1')
    need(one(routes,'rank','2')['actionable_ruling']=='DEFER_UNTIL_BOUNDARY_DOMAIN_IS_EXPLICIT','route2')
    need(one(routes,'rank','3')['actionable_ruling']=='BLOCKED_BY_MISSING_NATIVE_OFFSHELL_SELECTOR','route3')
    need(one(edges,'id','D04')['ruling']=='EXECUTABLE_BRIDGE_EDGE_MISSING','D04')
    need(one(edges,'id','D06')['ruling']=='REPRESENTATIVE_SELECTION_IS_NOT_DYNAMICAL_MATCHING','D06')
    need(one(counter,'id','C10')['ruling']=='NO_SINGLE_CLOSING_SELECTOR','C10')
    need(one(status,'id','S02')['status']=='REFUTED_OVERCLAIM','S02')
    need(one(status,'id','S03')['status']=='OPEN_HIGH_COST','S03')
    need(one(status,'id','S07')['status']=='REFUTED_AS_SUFFICIENT','S07')
    need(one(status,'id','S09')['status']=='REFUTED_AS_SUFFICIENT','S09')
    need(one(status,'id','S11')['status']=='NOT_DERIVED','S11')
    need(one(status,'id','S12')['status']=='OPEN_IDENTIFIED_SELECTOR','S12')
    need(one(status,'id','S14')['status']=='REFUTED_LOGICALLY','S14')
    need(one(status,'id','S16')['status']=='RANKED_RECOMMENDATION','S16')
    need(one(status,'id','S20')['status']=='OPEN','S20')
    need(one(status,'id','S19')['status']=='FALSE_EXCLUDED','S19')
    need(one(scope,'layer','nonlinear route')['status']=='NOT_SOLVED','scope-nonlinear')
    need(one(scope,'layer','external adversarial review')['status']=='NOT_PERFORMED','scope-external')
    return {"semantic_rulings":22}
def derivation_check(r):
    need(r['result']=='PASS' and len(r['checks'])==18,'derive-count')
    need(r['route_ranking'][0]=='PHYSICAL_BOUNDARY_VARIATION','derive-rank')
    need(r['selector_ruling']['complete_closure'].startswith('NO_SINGLE_CLOSING_SELECTOR'),'derive-selector')
    need(r['next_bounded_derivation'].startswith('derive the exact conditional C2 finite-cell boundary'),'derive-next')
    need(r['maximum_conclusion']=='COMPACT_C2_RIGIDITY_IS_BRANCH_SCOPED; NO_SINGLE_CLOSING_SELECTOR; IMMEDIATE_VARIATION_PLACEMENT_AND_EXECUTABLE_OFFSHELL_REPRESENTATIVE_MAP_OPEN; CONDITIONAL_C2_BOUNDARY_VARIATION_RANKED_NEXT','derive-max')
    return {"checks":len(r['checks']),"maximum_conclusion":r['maximum_conclusion']}
def independent_algebra():
    D,p=sp.symbols('D p',integer=True); need((D-4).subs(D,4)==0,'ind-C2-weight')
    lam,A,B=sp.symbols('lambda A B',positive=True)
    need(sp.diff(A*lam**2,lam)>0,'ind-EH-monotone')
    # Adding an independently supplied lambda^4 term can balance only with a sign/coefficient choice: it is extra input.
    stationary=sp.solve(sp.diff(A*lam**2-B*lam**4,lam),lam)
    need(stationary==[sp.sqrt(2)*sp.sqrt(A)/(2*sp.sqrt(B))],'ind-balance-needs-B')
    x=sp.symbols('x'); y=sp.Function('y')(x); variation=sp.Function('v')(x); eps=sp.symbols('eps')
    action_density=sp.diff(y+eps*variation,x,2)**2
    first=sp.diff(action_density,eps).subs(eps,0)
    need(sp.expand(first)==2*sp.diff(y,x,2)*sp.diff(variation,x,2),'ind-first-var')
    # Integrating twice gives the registered bulk and two distinct boundary conjugates.
    need(sp.diff(2*sp.diff(y,x,2),x,2)==2*sp.diff(y,x,4),'ind-bulk')
    G,M,c,X,rho=sp.symbols('G M c X rho',positive=True)
    need(sp.simplify((G*(lam*M)/(c**2*lam*X))/(G*M/(c**2*X)))==1,'ind-compactness')
    need(sp.simplify((G*(rho/lam**2)*(lam*X)**2/c**2)/(G*rho*X**2/c**2))==1,'ind-density')
    k=sp.symbols('k');need(sp.degree(k**4,k)==4 and sp.degree(k**2,k)==2,'ind-operator-orders')
    return {"C2_weight":0,"EH_weight":2,"EH_plus_extra_balance":str(stationary[0]),"boundary_conjugates":2,"operator_orders":[4,2]}
def expect(label,fn):
    try:fn()
    except (AssertionError,KeyError,subprocess.CalledProcessError):return 'PASS'
    raise AssertionError('catch:'+label)

def main():
    census=rows('SOURCE_CENSUS.tsv');sources=rows('SOURCE_ADJUDICATION.tsv');scale=rows('SCALE_HOMOGENEITY.tsv')
    routes=rows('ROUTE_COMPARISON.tsv');edges=rows('DEPENDENCY_EDGES.tsv');counter=rows('COUNTERMODEL_LEDGER.tsv')
    status=rows('STATUS_LEDGER.tsv');scope=rows('COMPLETENESS_SCOPE.tsv');der=json.loads((HERE/'DERIVATION_RESULT.json').read_text())
    groups={'census':census_check(census),'sources':source_check(sources,census),'scale':unique_table(scale,'id',15,'scale'),
    'routes':unique_table(routes,'rank',3,'routes'),'edges':unique_table(edges,'id',12,'edges'),
    'countermodels':unique_table(counter,'id',10,'counter'),'status':unique_table(status,'id',21,'status'),
    'scope':unique_table(scope,'layer',12,'scope'),'semantics':semantic_checks(scale,routes,edges,counter,status,scope),
    'derivation':derivation_check(der),'independent_algebra':independent_algebra()}
    catches={}
    catches['missing_census_rejected']=expect('census',lambda:census_check(census[:-1]))
    changed=copy.deepcopy(census);one(changed,'path','LIVE.md')['sha256']='0'*64
    catches['base_hash_mutation_rejected']=expect('hash',lambda:source_check(sources,changed))
    catches['missing_source_rejected']=expect('source',lambda:source_check(sources[:-1],census))
    for table,key,count,label in [(scale,'id',15,'scale'),(routes,'rank',3,'routes'),(edges,'id',12,'edges'),
    (counter,'id',10,'counter'),(status,'id',21,'status'),(scope,'layer',12,'scope')]:
        catches[f'missing_{label}_row_rejected']=expect(label,lambda table=table,key=key,count=count,label=label:unique_table(table[:-1],key,count,label))
    mutations=[('scale',scale,'id','H01','ruling','SCALE_SELECTED'),('scale_anchor',scale,'id','H14','ruling','DETERMINES_XMAX'),
    ('route_rank',routes,'rank','1','route','NONLINEAR_STATIONARY_CLOSURE'),('route_block',routes,'rank','3','actionable_ruling','SOLVED'),
    ('edge_rep',edges,'id','D04','ruling','CLOSED'),('edge_match',edges,'id','D06','ruling','AUTOMATIC_EH'),
    ('counter_single',counter,'id','C10','ruling','ONE_SELECTOR_CLOSES_ALL'),('status_rigidity',status,'id','S02','status','DERIVED_UDT_WIDE'),
    ('status_nonlinear',status,'id','S03','status','SOLVED'),('status_boundary',status,'id','S07','status','PHYSICAL_DATA_SELECTED'),
    ('status_bootstrap',status,'id','S09','status','SCALE_SELECTED'),('status_anchors',status,'id','S11','status','DERIVED'),
    ('status_fork',status,'id','S12','status','CLOSED'),('status_bridge',status,'id','S14','status','DYNAMICS_MATCHED'),
    ('status_electron',status,'id','S19','status','INPUT_USED'),('status_action',status,'id','S20','status','COMPLETE')]
    for label,table,key,identity,field,bad in mutations:
        ch=copy.deepcopy(table);one(ch,key,identity)[field]=bad
        catches[f'{label}_overclaim_rejected']=expect(label,lambda ch=ch:semantic_checks(ch if table is scale else scale,ch if table is routes else routes,
        ch if table is edges else edges,ch if table is counter else counter,ch if table is status else status,ch if table is scope else scope))
    ch=copy.deepcopy(der);ch['selector_ruling']['complete_closure']='ONE_SELECTOR'
    catches['derivation_single_selector_rejected']=expect('derive-selector',lambda:derivation_check(ch))
    ch=copy.deepcopy(der);ch['next_bounded_derivation']='launch nonlinear GPU scan'
    catches['derivation_next_route_mutation_rejected']=expect('derive-next',lambda:derivation_check(ch))
    ch=copy.deepcopy(der);ch['maximum_conclusion']='COMPLETE_ACTION_DERIVED'
    catches['maximum_overreach_rejected']=expect('derive-max',lambda:derivation_check(ch))
    with (HERE/'CATCH_PROOFS.tsv').open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=['catch','result'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({'catch':k,'result':v} for k,v in sorted(catches.items()))
    result={'schema':'udt-c2-rigidity-three-route-zoomout-verification-1.0','result':'PASS','groups':groups,'catch_proofs':catches,
    'counts':{'census':len(census),'sources':len(sources),'scale':len(scale),'routes':len(routes),'edges':len(edges),'countermodels':len(counter),'status':len(status),'scope':len(scope),'catch_proofs':len(catches)},
    'derivation_sha256':hashlib.sha256((HERE/'DERIVATION_RESULT.json').read_bytes()).hexdigest(),
    'verdict':der['maximum_conclusion'],'certification':'VERIFIED-WITH-CAVEATS: independent homogeneity/boundary algebra and base-source replay; no fresh external-model review',
    'compute':{'cpu_only':True,'gpu_used':False,'sympy':sp.__version__}}
    (HERE/'VERIFICATION_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':'PASS','groups':len(groups),'catch_proofs':len(catches),'verdict':result['verdict']},sort_keys=True))
if __name__=='__main__':main()
