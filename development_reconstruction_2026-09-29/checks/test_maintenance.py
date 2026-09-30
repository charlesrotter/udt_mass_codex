#!/usr/bin/env python3
"""Adversarial regression using memory overlays; no source mutations.
Synthetic review attestations test the checker protocol, not scientific review.
"""
import csv,hashlib,io,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import verify_udt_development as v

def dump(obj):return json.dumps(obj,sort_keys=True,ensure_ascii=False)
def h(s):return hashlib.sha256(s.encode()).hexdigest()
class Maintenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.master=(ROOT/v.MASTER).read_text()
        cls.graph=json.loads((ROOT/v.WORK/'DEVELOPMENT_GRAPH.json').read_text())
        cls.required=set(v.ADAPTERS)|{v.MASTER,v.WORK+'DEVELOPMENT_GRAPH.json',v.WORK+'CLAIM_DISPOSITIONS.tsv',
          v.WORK+'RECENT_DISPOSITIONS.tsv','verify_udt_development.py','verify_current_scientific_premises.py',
          'AGENTS.md','CLAUDE.md','UDT_RESEARCH_ROADMAP.md',v.WORK+'MAINTENANCE.md'}
        accepted={p:v.sha256(ROOT/p) for p in cls.required}
        cls.fixture={};reviewers=[]
        for role in ('synthetic_a','synthetic_b'):
            p=v.WORK+'checks/'+role+'.json'
            report=v.WORK+'checks/'+role+'.md'
            cls.fixture[report]='SYNTHETIC REVIEW PROTOCOL FIXTURE, NOT SCIENTIFIC REVIEW.'
            att=dump({'context':role,'verdict':'ACCEPT_WITH_LIMITS','accepted_sha256':accepted,
                      'report_path':report,'report_sha256':h(cls.fixture[report])})
            cls.fixture[p]=att;reviewers.append({'context':role,'attestation':p,'sha256':h(att)})
        cls.fixture[v.WORK+'REVIEW_RECORD.json']=dump({'status':'REVIEWED_WITH_LIMITS','accepted_sha256':accepted,'reviewers':reviewers})
    def check(self,overrides=None):return v.validate(overrides=self.fixture | (overrides or {}))
    def rejects(self,changes,phrase):
        with self.assertRaisesRegex(v.DevelopmentError,phrase):self.check(changes)
    def graph_change(self,fn):
        g=json.loads(dump(self.graph));fn(g);return {v.WORK+'DEVELOPMENT_GRAPH.json':dump(g)}
    def central_change(self,s):
        return {v.MASTER:s,'CURRENT_RESEARCH_PROGRAM.md':v.program_text(s)}
    def test_valid_fixture(self):self.assertEqual(self.check()['registry_rows'],406)
    def test_changed_source_flags_positive_negative_descendants(self):
        p='udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/EXACT_DERIVATION.md'
        affected=v.affected_nodes(self.graph,[p]);self.assertTrue({'R9','R10','R11','R12','R17','R18'}<=set(affected))
        self.rejects({p:(ROOT/p).read_text()+'\nTEST FIXTURE\n'},'REVIEW_REQUIRED.*affected=')
    def test_completed_pair_impact(self):
        p='udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md'
        a=set(v.affected_nodes(self.graph,[p]))
        self.assertTrue({'R4','R5','R6','R7','R8','R13','R14','R18'}<=a)
        self.rejects({p:(ROOT/p).read_text()+'\nTEST'},'REVIEW_REQUIRED.*affected=')
    def test_correction_impact(self):
        p=v.WORK+'SOURCE_CORRECTIONS.md';a=set(v.affected_nodes(self.graph,[p]))
        self.assertTrue({'R9','R10','R11','R12','R17','R18'}<=a)
        self.rejects({p:(ROOT/p).read_text()+'\nTEST'},'REVIEW_REQUIRED.*affected=')
    def test_owner_definition_impact(self):
        p='udt_repository_cleanup_2026-09-27/local_clock_impact_2026-09-29/OWNER_CLARIFICATION.md'
        self.assertTrue({f'R{i}' for i in range(1,19)}<=set(v.affected_nodes(self.graph,[p])))
    def test_old_review_status_support_change(self):
        p='udt_directional_clock_release_2026-09-14/review/REVIEW.md'
        self.assertTrue({'R5','R10','R18'}<=set(v.affected_nodes(self.graph,[p])))
        self.rejects({p:(ROOT/p).read_text()+'\nTEST'},'REVIEW_REQUIRED')
    def test_report_bytes_are_bound(self):
        self.rejects({v.WORK+'checks/synthetic_a.md':'DIFFERENT REPORT'},'review report bytes changed')
    def test_registry_change(self):
        p='CURRENT_SCIENTIFIC_PREMISES.tsv';rows=list(csv.DictReader(io.StringIO((ROOT/p).read_text()),delimiter='\t'))
        next(r for r in rows if r['premise_id']=='G310')['term']+=' TEST'
        out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(rows[0]),delimiter='\t');writer.writeheader();writer.writerows(rows)
        self.rejects({p:out.getvalue()},'changed rows=.*G310')
    def test_lost_coverage(self):
        p=v.WORK+'CLAIM_DISPOSITIONS.tsv';s=(ROOT/p).read_text();self.rejects({p:'\n'.join(s.splitlines()[:-1])+'\n'},'coverage mismatch')
    def test_missing_response_class(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_RESPONSE','to':'R10','kind':'hypothesis'})),'missing required hypothesis')
    def test_missing_optional_source(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_SOURCE','to':'R15','kind':'hypothesis'})),'missing required hypothesis')
    def test_stationary_exclusion_requires_its_sector(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_STATIONARY_CLOCKS','to':'R8S','kind':'hypothesis'})),'missing required hypothesis')
    def test_shared_geometry_source_flags_positive_and_negative(self):
        p='udt_shared_geometry_extension_2026-09-29/INITIAL_DERIVATION.md'
        self.assertTrue({'R8','R8S','R16','R18'}<=set(v.affected_nodes(self.graph,[p])))
        self.rejects({p:(ROOT/p).read_text()+'\nTEST'},'REVIEW_REQUIRED.*affected=')
    def test_additional_owner_meaning_routes_to_core_and_restriction(self):
        p='udt_shared_geometry_extension_2026-09-29/OWNER_CLARIFICATION.md'
        self.assertTrue({'R6','R8','R8S','R10','R17','R18'}<=set(v.affected_nodes(self.graph,[p])))
    def test_lkt_bridge_requires_actual_two_dimensional_geometry(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_LKT2D','to':'R7L','kind':'hypothesis'})),'missing required hypothesis')
    def test_lkt_stationarity_requires_both_additional_hypotheses(self):
        for condition in ('C_LKT_RECIPROCAL','C_LKT_SAME_PHI'):
            with self.subTest(condition=condition):
                self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':condition,'to':'R7E','kind':'hypothesis'})),'missing required hypothesis')
    def test_lkt_scalar_obstruction_requires_full_group_question(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_LKT_CHARACTER','to':'R7C','kind':'hypothesis'})),'missing required hypothesis')
    def test_lkt_source_flags_positive_and_negative_descendants(self):
        p='udt_lorentz_kernel_transport_2026-09-29/INITIAL_CANDIDATE.md'
        self.assertTrue({'R7','R7C','R7L','R7E','R8S','R18'}<=set(v.affected_nodes(self.graph,[p])))
        self.rejects({p:(ROOT/p).read_text()+'\nTEST'},'REVIEW_REQUIRED.*affected=')
    def test_open_join_as_premise(self):
        self.rejects(self.graph_change(lambda g:g['edges'].append({'from':'O_ASSIGNMENT','to':'R1','kind':'proof'})),'open join promoted')
    def test_pcw_proposal_cannot_supply_response_hypothesis(self):
        self.rejects(self.graph_change(lambda g:g['edges'].append({'from':'O_PCW_PROPOSALS','to':'R9','kind':'hypothesis'})),'open join promoted')
    def test_pcw_source_routes_proposal_and_adverse_conclusions_only(self):
        p='udt_physical_connection_whiteboard_2026-09-30/REPAIR.md'
        impact=set(v.affected_nodes(self.graph,[p]))
        self.assertTrue({'O_PCW_PROPOSALS','R18'}<=impact)
        self.assertNotIn('R9',impact)  # Existing DDR proof does not depend on proposed identification.
        self.rejects({p:(ROOT/p).read_text()+'\nTEST'},'REVIEW_REQUIRED.*affected=')
    def test_gca_homothety_route_requires_its_class(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_HOMOTHETY','to':'R10H','kind':'hypothesis'})),'missing required hypothesis')
    def test_gca_conservation_comparison_is_conditional(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_GCA_COMPARISON','to':'R17C','kind':'hypothesis'})),'missing required hypothesis')
    def test_gca_lovelock_requires_its_full_domain(self):
        self.rejects(self.graph_change(lambda g:g['edges'].remove({'from':'C_LOVELOCK','to':'R17L','kind':'hypothesis'})),'missing required hypothesis')
    def test_gca_source_routes_positive_and_negative_uses(self):
        p='udt_gr_commitment_audit_2026-09-29/INITIAL_CANDIDATE.md'
        self.assertTrue({'R10','R10H','R11','R12','R17','R17C','R17L','R18'}<=set(v.affected_nodes(self.graph,[p])))
        self.rejects({p:(ROOT/p).read_text()+'\nTEST'},'REVIEW_REQUIRED.*affected=')
    def test_cycle(self):
        self.rejects(self.graph_change(lambda g:g['edges'].append({'from':'R18','to':'R1','kind':'context'})),'cycle')
    def test_source_path_protected_before_read(self):
        self.rejects(self.graph_change(lambda g:g['sources_sha256'].update({v.PROTECTED[0]+'never_read.txt':'0'*64})),'unsafe/protected')
    def test_stale_generated_orientation(self):
        p='CURRENT_RESEARCH_PROGRAM.md';self.rejects({p:(ROOT/p).read_text()+'\nstale advice'},'orientation is stale')
    def test_unreviewed_body_change(self):
        self.rejects(self.central_change(self.master+'\nNew unreviewed body.'),'changed reviewed file')
    def test_unreviewed_adapter_claim(self):
        self.rejects({'MEMORY.md':(ROOT/'MEMORY.md').read_text()+'\nThis supplied curve is uniquely selected.'},'changed reviewed file')
    def test_gr_import(self):self.rejects(self.central_change(self.master+'\nGR is a native response-law input.'),'forbidden strengthening')
    def test_signal_speed(self):self.rejects(self.central_change(self.master+'\nc_eff is the local signal speed.'),'forbidden strengthening')
    def test_local_response_universal_gate(self):self.rejects(self.central_change(self.master+'\nlocal E is required for every clock comparison.'),'forbidden strengthening')
    def test_restricted_failure_promoted(self):self.rejects(self.central_change(self.master+'\nfull UDT is proved underdetermined.'),'forbidden strengthening')
    def test_missing_class_prose_even_if_not_pattern(self):
        s=self.master.replace('Suppose separately that E belongs to the entire G301 response class:', 'E equals Ric without hypotheses:')
        self.assertNotEqual(s,self.master);self.rejects(self.central_change(s),'changed reviewed file')
    def test_review_version_mismatch(self):
        p=v.WORK+'checks/synthetic_a.json';a=json.loads(self.fixture[p]);a['accepted_sha256'][v.MASTER]='0'*64
        self.rejects({p:dump(a)},'review version mismatch')
    def test_missing_review_context(self):
        p=v.WORK+'REVIEW_RECORD.json';a=json.loads(self.fixture[p]);a['reviewers']=a['reviewers'][:1]
        self.rejects({p:dump(a)},'two actual review contexts')

if __name__=='__main__':unittest.main(verbosity=2)
