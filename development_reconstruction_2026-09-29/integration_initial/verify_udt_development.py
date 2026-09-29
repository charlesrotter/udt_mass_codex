#!/usr/bin/env python3
"""Check the living development and flag changed dependencies; never regrade science.

This is bounded regression/version correspondence, not a semantic proof. Full
source banking checks remain in verify_current_scientific_premises.py. --draft
reports construction coherence only and cannot satisfy the normal startup gate.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, re
from pathlib import Path
from update_metric_kernel_account import sha256  # Existing byte-hash helper only.

ROOT = Path(__file__).resolve().parent
WORK = 'development_reconstruction_2026-09-29/'
MASTER = 'UDT_DEVELOPMENT.md'
ADAPTERS = ('LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
            'CURRENT_SCIENTIFIC_PREMISES.md', 'MEMORY.md', 'INDEX.md')
PROTECTED = ('udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/')
EDGE_KINDS = {'proof', 'hypothesis', 'context', 'interpretation', 'open_boundary'}

class DevelopmentError(AssertionError):
    pass

def require(ok, msg):
    if not ok:
        raise DevelopmentError(msg)

def orientation(text):
    a='<!-- DEVELOPMENT_ORIENTATION_BEGIN -->'; b='<!-- DEVELOPMENT_ORIENTATION_END -->'
    require(text.count(a)==text.count(b)==1, 'orientation markers missing or duplicated')
    return text.split(a,1)[1].split(b,1)[0].strip()

def program_text(master):
    return ('# Current research program — generated orientation\n\n'
      'The sole maintained scientific argument is [UDT_DEVELOPMENT.md](UDT_DEVELOPMENT.md).\n'
      'This bounded startup view is generated from its opening; edit that source.\n'
      'LIVE.md owns operational status; CURRENT_SCIENTIFIC_PREMISES.tsv owns exact grades.\n\n'
      '<!-- GENERATED_DEVELOPMENT_BEGIN -->\n'+orientation(master)+'\n'
      '<!-- GENERATED_DEVELOPMENT_END -->\n\n'
      '## Current next gate\n\n'
      'Use LIVE.md for the authorized action and return point. After orientation,\n'
      'read the relevant central chapter; open original evidence only when load-bearing.\n')

def affected_nodes(graph, changed_sources=(), changed_ids=(), dispositions=()):
    """Conservative recorded impact, including negative and context descendants."""
    affected={n['id'] for n in graph['nodes'] if set(n.get('sources',())) & set(changed_sources)
              or set(n.get('registry_ids',())) & set(changed_ids)}
    for row in dispositions:
        if row['premise_id'] in changed_ids:
            affected.update(x for x in row['central_location'].split(';') if x)
    while True:
        more={e['to'] for e in graph['edges'] if e['from'] in affected}
        if more <= affected:
            return sorted(affected)
        affected |= more

def validate(root=ROOT, *, draft=False, overrides=None):
    """Overrides are in-memory adversarial fixtures; disk is never mutated by validation."""
    root=Path(root); overrides={} if overrides is None else overrides
    def data(p):
        require(not Path(p).is_absolute() and '..' not in Path(p).parts and not p.startswith(PROTECTED),
                'unsafe/protected dependency path: '+p)
        if p in overrides:
            return overrides[p].encode() if isinstance(overrides[p],str) else overrides[p]
        return (root/p).read_bytes()
    def text(p):return data(p).decode('utf-8')
    def digest(p):return hashlib.sha256(data(p)).hexdigest() if p in overrides else sha256(root/p)
    def rows(p):return list(csv.DictReader(io.StringIO(text(p)),delimiter='\t'))
    graph=json.loads(text(WORK+'DEVELOPMENT_GRAPH.json'))
    master=text(MASTER)
    nodes=graph['nodes']; byid={n['id']:n for n in nodes}
    require(len(byid)==len(nodes), 'duplicate graph node')
    require({f'R{i}' for i in range(1,19)}|{'D1'} <= set(byid), 'missing central argument')
    for n in nodes:
        if n['kind'] in ('argument','definition'):
            require(master.count('<a id="'+n['anchor']+'"></a>')==1, 'missing/duplicate anchor: '+n['id'])
    for e in graph['edges']:
        require(e['from'] in byid and e['to'] in byid and e['kind'] in EDGE_KINDS,'invalid typed edge')
        require(not (byid[e['from']]['kind']=='open_join' and e['kind'] in ('proof','hypothesis')),
                'open join promoted to accepted input')
    for n in nodes:
        for h in n.get('required_conditions',[]):
            require(any(e=={'from':h,'to':n['id'],'kind':'hypothesis'} for e in graph['edges']),
                    'missing required hypothesis edge: '+h+' -> '+n['id'])
    pending=set(byid); done=set()
    while pending:
        ready={n for n in pending if all(e['from'] in done for e in graph['edges'] if e['to']==n)}
        require(bool(ready),'cycle in central dependency graph')
        done |= ready; pending -= ready
    reg=rows('CURRENT_SCIENTIFIC_PREMISES.tsv'); disp=rows(WORK+'CLAIM_DISPOSITIONS.tsv')
    regmap={r['premise_id']:r for r in reg}; dismap={r['premise_id']:r for r in disp}
    require(len(reg)==len(regmap)==len(disp)==len(dismap)==406 and set(regmap)==set(dismap),
            'registry/disposition coverage mismatch')
    changed_ids=[]
    for i,row in dismap.items():
        actual=hashlib.sha256(json.dumps(regmap[i],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        if actual!=row['source_row_sha256']:changed_ids.append(i)
        require(bool(row['disposition'] and row['reason'] and row['reconstruction_depth']), 'unresolved disposition: '+i)
        for a in row['central_location'].split(';'):
            require(a in byid, 'unknown central disposition: '+i+':'+a)
    for n in nodes:
        require(set(n.get('registry_ids',()))<=set(regmap),'unknown registry dependency')
        require(set(n.get('sources',()))<=set(graph['sources_sha256']), 'unversioned source dependency')
    changed_sources=[]
    for p,expected in graph['sources_sha256'].items():
        # data validates scope before digest, including the normal filesystem branch.
        data(p)
        if digest(p)!=expected:changed_sources.append(p)
    impact=affected_nodes(graph,changed_sources,changed_ids,disp)
    require(not changed_sources and not changed_ids,
            'REVIEW_REQUIRED; changed sources='+str(changed_sources)+'; changed rows='+str(changed_ids)+'; affected='+str(impact))
    recent=rows(WORK+'RECENT_DISPOSITIONS.tsv')
    require(recent and len({r['id'] for r in recent})==len(recent), 'missing/duplicate later-work disposition')
    for r in recent:
        data(r['source'])
        require(digest(r['source'])==r['source_sha256'],'later source changed; REVIEW_REQUIRED: '+r['id'])
        require(all(a in byid for a in r['central_location'].split(';')) and bool(r['current_scope']) and bool(r['rederivation_depth']),
                'incomplete later-work disposition: '+r['id'])
    require(text('CURRENT_RESEARCH_PROGRAM.md')==program_text(master),'generated startup orientation is stale')
    normalized=' '.join(master.split())
    for token in ('GR is FILTER ONLY','not a response-law input','Local Metric Sufficiency remains owner-provisional',
        'not established from filter-only GR','CHALLENGED_OWNER_POSTULATE_NOT_DERIVED',
        'OWNER_ADOPTED_PROVISIONAL_POSTULATE','not derived or canonized',
        'Angular-sector cancellation alone owns loud--quiet--loud',
        'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md'):
        require(token in normalized,'central authority qualifier missing: '+token)
    for p in ADAPTERS+(MASTER,'UDT_RESEARCH_ROADMAP.md'):
        t=' '.join(text(p).split())
        for pattern in (r'GR (?:is|remains) (?:a native|an adopted) response-law input',
            r'Einstein (?:equation|arena) (?:is|remains) (?:native|unconditional)',
            r'(?:DDR|Local Metric Sufficiency) (?:is|remains) (?:derived|canonized|unadopted)',
            r'c_eff (?:is|equals) (?:the |a )?local signal speed',
            r'local E is required for every clock comparison',
            r'(?:all UDT|full UDT) (?:is|has been) (?:refuted|proved underdetermined)',
            r'a new physical premise is necessary', r'independent closure is impossible'):
            require(re.search(pattern,t,re.I) is None,'forbidden strengthening: '+p+':'+pattern)
    for p in ('LIVE.md','HANDOFF.md'):
        t=text(p)
        require(t.count('<!-- STARTUP_CURRENT_BEGIN -->')==t.count('<!-- STARTUP_CURRENT_END -->')==1,'current block markers: '+p)
        for protected in PROTECTED:require(protected in t,'protected path missing: '+p)
        require('CDR1' in t and 'UDT_DEVELOPMENT.md' in t and 'Stop for lay discussion' in t,'operational route missing: '+p)
    require('Next:' in text('HANDOFF.md') and '### Next gate' in text('LIVE.md'),'next gate labels missing')
    if not draft:
        record=json.loads(text(WORK+'REVIEW_RECORD.json'))
        require(record['status']=='REVIEWED_WITH_LIMITS','development not reviewed')
        required=set(ADAPTERS)|{MASTER,WORK+'DEVELOPMENT_GRAPH.json',WORK+'CLAIM_DISPOSITIONS.tsv',
            WORK+'RECENT_DISPOSITIONS.tsv','verify_udt_development.py','verify_current_scientific_premises.py',
            'AGENTS.md','CLAUDE.md','UDT_RESEARCH_ROADMAP.md',WORK+'MAINTENANCE.md'}
        require(required<=set(record['accepted_sha256']),'incomplete integration review bindings')
        for p,h in record['accepted_sha256'].items():
            data(p);require(digest(p)==h,'changed reviewed file; REVIEW_REQUIRED: '+p)
        require(len(record['reviewers'])==2 and len({r['context'] for r in record['reviewers']})==2,
                'two actual review contexts required')
        for r in record['reviewers']:
            att=json.loads(text(r['attestation']))
            require(att['context']==r['context'] and att['verdict']=='ACCEPT_WITH_LIMITS','review not accepted')
            require(att['accepted_sha256']==record['accepted_sha256'],'review version mismatch')
            require(digest(r['attestation'])==r['sha256'],'review attestation changed')
    return {'status':'DRAFT_COHERENCE_ONLY' if draft else 'PASS','registry_rows':len(disp),
      'later_returns':len(recent),'central_arguments':18,'source_pins':len(graph['sources_sha256']),
      'scope':'Version, routing and bounded regression checks; not semantic completeness, canon or full-corpus reproof.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--draft',action='store_true')
    args=parser.parse_args()
    try: print(json.dumps(validate(draft=args.draft),indent=2))
    except (AssertionError,OSError,KeyError,ValueError) as exc:
        print('FAIL:',exc);raise SystemExit(1)
