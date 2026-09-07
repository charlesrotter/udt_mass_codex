"""Independent exact tensor differentiation; no PC2 author inputs/imports."""
import hashlib
import itertools
import json
import pathlib
import platform
import sympy as s

ROOT = pathlib.Path('/home/udt-admin/udt_mass_codex')
I = range(4)
checks = []

def guard(name, ok, detail=None):
    record = dict(name=name, passed=bool(ok))
    if detail is not None:
        record['detail'] = detail
    checks.append(record)
    if not ok:
        print(json.dumps(dict(status='FAIL', checks=checks), default=str))
        raise SystemExit(1)

def nz(expr):
    return s.cancel(s.expand(expr))

def geometry(coords, g):
    gi = g.inv()
    G = {(a,b,c): nz(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+
         s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in I))
         for a,b,c in itertools.product(I, repeat=3)}
    R = {(a,b,c,d): nz(s.diff(G[d,b,c],coords[a])-s.diff(G[d,a,c],coords[b])+
         sum(G[d,a,e]*G[e,b,c]-G[d,b,e]*G[e,a,c] for e in I))
         for a,b,c,d in itertools.product(I, repeat=4)}
    ric = {(b,c): nz(sum(R[a,b,c,a] for a in I))
           for b,c in itertools.product(I, repeat=2)}
    Q = {(a,b,c,d): nz(sum(g[d,e]*R[a,b,c,e] for e in I))
         for a,b,c,d in itertools.product(I, repeat=4)}

    def nabla(T, rank):
        result = {}
        for args in itertools.product(I, repeat=rank+1):
            a, indices = args[0], args[1:]
            value = s.diff(T[indices], coords[a])
            for slot, index in enumerate(indices):
                for e in I:
                    value -= G[e,a,index]*T[indices[:slot]+(e,)+indices[slot+1:]]
            result[args] = nz(value)
        return result

    def wave(T, rank):
        second = nabla(nabla(T,rank),rank+1)
        return {indices:nz(sum(gi[c,d]*second[(c,d)+indices]
                for c,d in itertools.product(I,repeat=2)))
                for indices in itertools.product(I,repeat=rank)}
    return gi, G, R, ric, Q, nabla, wave

def commutator_control(name, coords, g, vv, vacuum):
    gi,G,R,ric,Q,nabla,wave = geometry(coords,g)
    v = {(a,): vv[a] for a in I}
    A = nabla(v,1)
    direct = wave(A,2)
    gradwave = nabla(wave(v,1),1)
    dQ = nabla(Q,4)
    dric = nabla(ric,2)
    ric_term, curvature_term, derivative_term = {}, {}, {}
    divergence_bianchi = []
    for a,b in itertools.product(I,repeat=2):
        ric_term[a,b] = nz(sum(ric[a,d]*gi[d,c]*A[c,b]
                            for c,d in itertools.product(I,repeat=2)))
        curvature_term[a,b] = nz(-2*sum(gi[c,d]*R[d,a,b,e]*A[c,e]
                              for c,d,e in itertools.product(I,repeat=3)))
        derivative_term[a,b] = nz(-sum(gi[c,e]*gi[d,f]*dQ[c,e,a,b,f]*v[d,]
                              for c,d,e,f in itertools.product(I,repeat=4)))
        for f in I:
            divergence_bianchi.append(nz(sum(gi[c,e]*dQ[c,e,a,b,f]
                 for c,e in itertools.product(I,repeat=2))-dric[f,a,b]+dric[b,a,f]))
    identity = {k:nz(direct[k]-gradwave[k]-ric_term[k]-curvature_term[k]-derivative_term[k])
                for k in direct}
    guard(name+'_full_wave_commutator', all(x==0 for x in identity.values()))
    guard(name+'_differential_bianchi_sign', all(x==0 for x in divergence_bianchi))
    guard(name+'_ricci_class', all(x==0 for x in ric.values()) == vacuum)
    guard(name+'_curvature_sign_mutant_caught', any(nz(2*x)!=0 for x in curvature_term.values()))
    guard(name+'_curvature_factor1_mutant_caught', any(x!=0 for x in curvature_term.values()))
    if not vacuum:
        guard(name+'_drop_differentiated_curvature_caught', any(x!=0 for x in derivative_term.values()))
    else:
        guard(name+'_homogeneous_vacuum_identity', all(nz(direct[k]-gradwave[k]-curvature_term[k])==0 for k in direct))
    return dict(metric=g.tolist(), covector=vv,
                ricci={str(k):v for k,v in ric.items() if v!=0},
                direct_minus_gradwave={str(k):nz(direct[k]-gradwave[k]) for k in direct if nz(direct[k]-gradwave[k])!=0},
                curvature_term={str(k):v for k,v in curvature_term.items() if v!=0},
                differentiated_curvature_term={str(k):v for k,v in derivative_term.items() if v!=0})

u,v,x,y = s.symbols('u v x y', real=True)
H=x**3-3*x*y**2+u*(x**2-y**2)
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
pp = commutator_control('vacuum_variable_curvature',(u,v,x,y),g,
                       [u*x+v, x*y+u, y+u*v, v*x],True)
t,z,r,h = s.symbols('t z r h', real=True)
gg=s.diag(-1,(1+t**2)**2,1,1)
off = commutator_control('off_equation_source_control',(t,z,r,h),gg,
                        [t*z+1,z+t,t*r,h+t*z],False)

# Independently compare the geometric scalar and its full spacelike data formula.
# This is one exact witness/control, not the propagation theorem.
c=s.Integer(2)
N=s.expand(s.diff(H,x,2)**2+s.diff(H,x,y)**2)
alog=s.Matrix([s.diff(N,z)/(4*N) for z in (u,v,x,y)])
q_ambient=nz((alog.T*g.inv()*alog)[0])
L=H+2*c
gamma_inv=s.diag(1/L,1,1)
spatial=s.Matrix([alog[0],alog[2],alog[3]])
q_slice=nz((spatial.T*gamma_inv*spatial)[0]-alog[0]**2/L)
guard('q_full_spacelike_formula',nz(q_ambient-q_slice)==0)
guard('q_drop_normal_subtraction_mutant_caught',nz((spatial.T*gamma_inv*spatial)[0]-q_ambient)!=0)
guard('q_positive_initial_control',q_ambient.subs({u:0,x:1,y:0})==s.Rational(1,4))
guard('nonzero_root_control',N.subs({u:0,x:1,y:0})==36)
guard('spacelike_control',L.subs({u:0,x:1,y:0})==5)

# A homogeneous scalar-wave defect needs its normal data as well as its value.
defect=t
guard('missing_normal_data_hostile',defect.subs(t,0)==0 and s.diff(defect,t).subs(t,0)==1 and -s.diff(defect,t,2)==0)

sources=[
 'AGENTS.md','CLAUDE.md','CROSS_MODEL_VERIFY.md',
 '.claude/skills/no-shortcuts/SKILL.md','.claude/skills/completeness-map/SKILL.md',
 '.claude/skills/solution-space-not-imposition/SKILL.md','.claude/skills/verifier-before-record/SKILL.md',
 'CURRENT_SCIENTIFIC_PREMISES.tsv',
 'udt_phase_current_product_persistence_campaign_2026-09-07/WORK_ORDER.md',
 'udt_phase_current_product_persistence_campaign_2026-09-07/step_02/QUESTION.md',
 'udt_phase_current_product_persistence_campaign_2026-09-07/step_01/CANDIDATE_ARGUMENT.md',
 'udt_phase_current_product_persistence_campaign_2026-09-07/step_01/REVIEW_RECORD.md',
 'udt_phase_current_product_persistence_campaign_2026-09-07/step_01/review/PHASE_B_ADVERSARIAL_REVIEW.md',
 'startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md',
 'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/EXACT_DERIVATION.md',
 'udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md',
 'udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md',
 'udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/EXACT_DERIVATION.md',
 'udt_g335_local_pair_response_persistence_2026-09-03/EXACT_DERIVATION.md',
 'udt_g313_curvature_phase_current_candidate_2026-09-06/CANDIDATE_ARGUMENT.md',
 'udt_g353_g356_conditional_banking_2026-09-06/BANKING_RECORD.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_03/CANDIDATE_ARGUMENT.md',
 'udt_g351_g352_content_bridge_campaign_2026-09-06/step_04/CANDIDATE_ARGUMENT.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}
print(json.dumps(dict(status='PASS',checks=checks,python=platform.python_version(),
 sympy=s.__version__,vacuum_control=pp,off_equation_control=off,
 initial_scalar=dict(N=N,q=q_ambient,q_slice=q_slice),source_sha256=hashes),indent=2,default=str))
