#!/usr/bin/env python3
"""
complete_metric_sweep_stageB.py -- STAGE B of the complete-metric deep-negative-phi
SOLUTION-SPACE SWEEP.  OBSERVE mode (report WHAT IS THERE; NOT targeting a fermion,
a critical point, or any particular cell).

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  Frame + premise ledger:
complete_metric_sweep_setup.md (incl. the STAGE-B ADDENDUM: kappa8 PRIMARY axis,
TEST-BOTH dual reading, the discriminator, the MANDATORY physical-vs-numerical guard).
Engine: complete_metric_batched.py (committed, immutable, #43/#44-cross-checked) for
the PHYSICS; the inner solves are BATCHED (the whole grid in one selfconsistent call
-- that is the architecture Stage A built; B=1 wastes the V100).  DATA-BLIND (sizes/
masses in units L=sqrt(kappa/xi)=1; NEVER compared to wall numbers in this push).

WHAT STAGE B DOES (the charter's #1 directive, never before executed with L4):
  ONE batched sweep over (kappa8 PRIMARY x depth p x seed shape), each member
  relaxed to two-way self-consistency with the COMPLETE action (L2+L4+seal+phi
  back-reaction), READ TWICE (Path 1 real critical threshold / Path 2 free dial).
  Per member: existence/convergence; SHAPE (relax-to-round vs persist; turns);
  BIFURCATION (round-cell Jacobian min|eig|, eigvalsh -- zero-crossing = branch);
  SUBSTRUCTURE (turn/node count); #38 K_theta angular-completion WITH L4;
  Misner-Sharp mass + metric deficit.

THE MANDATORY GUARD (run first): the Stage-A kappa8~0.1 "over-collapse" had
res_th~4e9 -- a SOLVER BLOWUP signature.  A solver breakdown is NOT a critical point.
We resolve PHYSICAL-vs-NUMERICAL with an INDEPENDENT order parameter (the metric
deficit min(e^{-2phi}) = 1 - m_closed/r -> 0 is a genuine horizon/existence boundary)
+ a convergence study (N, iters, relax) + bisection of the boundary + its scaling.

NUMERICS (principle 2): full nonlinear EL + nonlinear MS t-eq.  NO linearization as
a result.  Sanctioned function-replacement only.  V100 pitfall honored (the committed
engine's LU path; no broadcast-Cholesky solve_triangular).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time, json
import numpy as np
import torch
import complete_metric_batched as cm
import complete_metric_stageB_fast as fb   # PCR-accelerated, same physics (cross-checked)

torch.set_default_dtype(torch.float64)
DEV = cm.DEV
TWO_PI = 2.0*math.pi
PI = math.pi
t0 = time.time()
OUT = {}

def hdr(s):
    print("\n" + "="*78, flush=True); print(s, flush=True); print("="*78, flush=True)

XI = KAP = 1.0; L = math.sqrt(KAP/XI)
rc = 0.05; SPAN = 14.0; ri = rc + SPAN*L
N_DEF = 600
print(f"[device] {DEV}, torch {torch.__version__}  cell [{rc},{ri}]={SPAN}L  N={N_DEF}", flush=True)

# --- PROVENANCE: the PCR fast engine must reproduce the committed dense engine ---
_rc = torch.linspace(rc, rc+SPAN*L, 600, device=DEV).unsqueeze(0)
_od = cm.selfconsistent_batched(_rc, XI, KAP, p=0.4, kap8=0.05, iters=45, relax=0.45, tol=1e-10)
_of = fb.selfconsistent_fast(_rc, XI, KAP, p=0.4, kap8=0.05, iters=45, relax=0.45, tol=1e-10, theta_iters=20)
_dTh = (_od['Th'] - _of['Th']).abs().max().item()
_dM  = abs(_od['M_MS'].item() - _of['M_MS'].item())
print(f"[xcheck fast-vs-committed @p=0.4,k8=0.05] max|dTh|={_dTh:.2e}  |dM_MS|={_dM:.2e}", flush=True)
assert _dTh < 1e-6 and _dM < 1e-6, "fast engine deviates from committed engine!"
OUT['engine_xcheck'] = dict(dTh=_dTh, dM_MS=_dM)


# ===========================================================================
# Seed builder (INITIAL DATA only; the solver settles freely).
# ===========================================================================
def make_seed(r1, seed, l_seed, seed_amp):
    base = PI*0.5*(1 - torch.tanh((r1 - (rc + 2*L))/(0.8*L)))
    x = (r1 - rc)/(ri - rc)
    if seed == 'round':
        Th = base
    elif seed == 'extranode':
        Th = base + seed_amp*torch.sin((l_seed+2)*PI*x)*torch.exp(-2*x)
    elif seed == 'twocore':
        Th = base + seed_amp*torch.exp(-((x-0.55)/0.10)**2)
    else:  # legendre-shaped radial proxy
        Th = base + seed_amp*torch.sin((l_seed+1)*PI*x)*torch.exp(-1.5*x)
    Th = torch.clamp(Th, 0.0, PI)
    Th[:, 0] = PI; Th[:, -1] = 0.0
    return Th


def solve_batch(plist, k8list, seeds=None, N=N_DEF, iters=70, relax=0.45, tol=1e-10):
    """Batch many (p,kap8,seed) members into ONE selfconsistent call.  Because the
    committed selfconsistent_batched takes scalar p and kap8 (the depth/coupling are
    used scalar-wise inside phi_from_source), we batch members that share (p,kap8)
    and loop the (p,kap8) pairs -- but each pair's seed-set is one batched call.
    For the round grid we batch ALL (p,kap8) of one p together is not possible (p
    scalar), so we group by unique (p,kap8).  Returns list of per-member dicts."""
    raise NotImplementedError  # replaced by explicit grouped loop below


def diagnose_member(r1, Th, phi, p, kap8):
    """Read-outs from a single (1,N) converged member."""
    Tn = Th[0].cpu().numpy(); rn = r1[0].cpu().numpy(); pn = phi[0].cpu().numpy()
    # width
    w = float('nan')
    for i in range(len(Tn)-1):
        a, b = Tn[i], Tn[i+1]
        if (a-PI/2)*(b-PI/2) <= 0 and a != b:
            t = (PI/2-a)/(b-a); w = rn[i] + t*(rn[i+1]-rn[i]); break
    # deficit (order parameter)
    Thp = cm.grad_central(Th, r1)
    _, m_areal, m_closed = cm.phi_from_source(r1, Th, Thp, phi, XI, KAP, p, kap8)
    deficit = (1.0 - (m_closed/r1))[0].cpu().numpy()
    min_def = float(np.min(deficit))
    # energies / mass
    E2, E4 = cm.energy_pieces(r1, Th, phi, XI, KAP)
    M_MS = float(m_areal[0, -1] - m_areal[0, 0])
    # substructure: monotonicity reversals
    d = np.diff(Tn); d = d[np.abs(d) > 1e-9]
    turns = int(np.sum(np.diff(np.sign(d)) != 0)) if len(d) else 0
    return dict(p=p, kap8=kap8, width=((w-rc)/L) if w==w else float('nan'),
                min_deficit=min_def, M_MS=M_MS, E2=float(E2), E4=float(E4),
                turns=turns, phi0=float(pn[0]))


def run_pk(p, kap8, seed='round', l_seed=0, seed_amp=0.0, N=N_DEF, iters=70,
           relax=0.45, tol=1e-10):
    r1 = torch.linspace(rc, rc+SPAN*L, N, device=DEV).unsqueeze(0)
    Th_init = None if seed == 'round' else make_seed(r1, seed, l_seed, seed_amp)
    o = fb.selfconsistent_fast(r1, XI, KAP, p=p, kap8=kap8, iters=iters,
                               relax=relax, tol=tol, Th_init=Th_init, theta_iters=20)
    d = diagnose_member(r1, o['Th'], o['phi'], p, kap8)
    d['res'] = o['hist'][-1][3]
    d['converged'] = (d['res'] < 1e-6) and (d['min_deficit'] > 1e-6)
    d['exists'] = d['converged'] and (d['width']==d['width']) and (d['width'] > 0.05)
    o['_diag'] = d
    return o, d


def batch_seeds_pk(p, kap8, seed_specs, N=N_DEF, iters=70, relax=0.45, tol=1e-10):
    """All seeds at ONE (p,kap8) batched into a single selfconsistent call."""
    B = len(seed_specs)
    r1 = torch.linspace(rc, rc+SPAN*L, N, device=DEV).unsqueeze(0).expand(B, N).contiguous()
    Th_init = torch.zeros(B, N, device=DEV)
    for k, (seed, ls, sa) in enumerate(seed_specs):
        Th_init[k] = make_seed(r1[k:k+1], seed, ls, sa)[0]
    o = fb.selfconsistent_fast(r1, XI, KAP, p=p, kap8=kap8, iters=iters,
                               relax=relax, tol=tol, Th_init=Th_init, theta_iters=20)
    diags = []
    for k in range(B):
        d = diagnose_member(r1[k:k+1], o['Th'][k:k+1], o['phi'][k:k+1], p, kap8)
        d['res'] = o['hist'][-1][3]
        d['converged'] = (d['res'] < 1e-6) and (d['min_deficit'] > 1e-6)
        d['exists'] = d['converged'] and (d['width']==d['width']) and (d['width'] > 0.05)
        d['seed'] = f"{seed_specs[k][0]}{seed_specs[k][1]}"
        diags.append((d, o['Th'][k:k+1], o['phi'][k:k+1], r1[k:k+1]))
    return diags


def fluct_eigs(rg, Th0, ph):
    """Second-variation Hessian about the profile; eigvalsh on GPU.  min|eig|->0 =
    bifurcation.  (Stage-A-cross-checked vs the #44 breathing tower.)"""
    N = len(rg)
    def edens(T, Tp):
        s=np.sin(T); s2=s*s; s4=s2*s2; e_m=np.exp(-ph); e2p=np.exp(2*ph)
        e2=(TWO_PI*XI/3)*e_m*(rg**2*s2*Tp**2+2*rg**2*Tp**2+4*e2p*s2)
        e4=(TWO_PI*KAP/3)*e_m*((2*rg**2*s4+2*rg**2*s2)*Tp**2+e2p*s4)/rg**2
        return e2+e4
    Tp0 = np.gradient(Th0, rg); h = 1e-6
    eP=(edens(Th0,Tp0+h)-2*edens(Th0,Tp0)+edens(Th0,Tp0-h))/h**2
    eQ=(edens(Th0+h,Tp0)-2*edens(Th0,Tp0)+edens(Th0-h,Tp0))/h**2
    epp=edens(Th0+h,Tp0+h);epm=edens(Th0+h,Tp0-h);emp=edens(Th0-h,Tp0+h);emm=edens(Th0-h,Tp0-h)
    eR=(epp-epm-emp+emm)/(4*h**2)
    Veff = eQ - np.gradient(eR, rg)
    s=np.sin(Th0);s2=s*s;s4=s2*s2
    W=(TWO_PI/3)*np.exp(3*ph)*(XI*(rg**2*s2+2*rg**2)+KAP*(2*s4+2*s2))
    n=N-2; Hm=np.zeros((n,n)); Wm=np.zeros((n,n))
    for i in range(1,N-1):
        Pr=0.5*(eP[i]+eP[i+1]); Pl=0.5*(eP[i-1]+eP[i])
        hr=rg[i+1]-rg[i]; hl=rg[i]-rg[i-1]; hc=0.5*(hr+hl); k=i-1
        Hm[k,k]=(Pr/hr+Pl/hl)/hc+Veff[i]
        if k+1<n: Hm[k,k+1]=-Pr/hr/hc
        if k-1>=0: Hm[k,k-1]=-Pl/hl/hc
        Wm[k,k]=W[i]
    Hm=0.5*(Hm+Hm.T); Winv=1.0/np.sqrt(np.diag(Wm))
    A=(Hm*Winv[:,None])*Winv[None,:]; A=0.5*(A+A.T)
    ev = torch.linalg.eigvalsh(torch.as_tensor(A, device=DEV)).cpu().numpy()
    return np.sort(ev)


# ===========================================================================
# TASK 2 (GUARD, FIRST) -- kappa8~0.1: PHYSICAL or NUMERICAL? then SHARP/SMOOTH?
# ===========================================================================
hdr("TASK 2 -- kappa8~0.1 FEATURE: PHYSICAL-vs-NUMERICAL GUARD, then SHARP-vs-SMOOTH")
print("Order parameters vs kappa8 at p=0.4: width/L; min_deficit=min(e^{-2phi})", flush=True)
print("(HORIZON order param ->0 = genuine existence boundary); M_MS; res (large=SOLVER", flush=True)
print("breakdown, NOT a critical point); round-cell min|eig| (bifurcation).", flush=True)
print(f"\n  {'kappa8':>9} {'width/L':>9} {'min_def':>10} {'M_MS':>9} {'res':>9} "
      f"{'min|eig|':>10} {'state':>14}", flush=True)
p_guard = 0.4
# fine resolution RIGHT AT the feature window [0.05,0.07] found in Stage A.
fine_k8 = [1e-2,3e-2,5e-2,5.5e-2,5.8e-2,6.0e-2,6.2e-2,6.5e-2,7e-2,8e-2,1e-1,1.5e-1]
guard_rows = []
for k8 in fine_k8:
    o, d = run_pk(p_guard, k8, N=600, iters=90, relax=0.30)
    rn=o['r'][0].cpu().numpy(); Tn=o['Th'][0].cpu().numpy(); pn=o['phi'][0].cpu().numpy()
    try: mineig = float(np.min(np.abs(fluct_eigs(rn,Tn,pn))))
    except Exception: mineig=float('nan')
    state = ("soliton" if d['exists'] else
             ("HORIZON(phys)" if (d['min_deficit']<=1e-6 and d['res']<1e-3) else "solver-blowup"))
    d['mineig']=mineig; d['state']=state; guard_rows.append(d)
    print(f"  {k8:>9.3g} {d['width']:>9.4f} {d['min_deficit']:>10.3e} {d['M_MS']:>9.4f} "
          f"{d['res']:>9.1e} {mineig:>10.3e} {state:>14}", flush=True)
OUT['guard_p0.4'] = [{k:v for k,v in r.items()} for r in guard_rows]

print("\n  CONVERGENCE STUDY at kappa8=0.058 (just below feature), p=0.4 (real soliton = grid-stable):", flush=True)
print(f"  {'N':>6} {'iters':>6} {'relax':>6} {'width/L':>9} {'min_def':>10} {'res':>9} {'state':>14}", flush=True)
conv_rows=[]
# probe just BELOW the feature (kappa8=0.058, where a soliton still exists) -- a
# real soliton must be grid-stable; a numerical artifact would move with N/iters.
for (N,it,rx) in [(400,90,0.30),(600,120,0.25),(900,150,0.20),(1300,200,0.15)]:
    o,d = run_pk(p_guard, 0.058, N=N, iters=it, relax=rx)
    state=("soliton" if d['exists'] else ("HORIZON(phys)" if (d['min_deficit']<=1e-6 and d['res']<1e-3) else "solver-blowup"))
    conv_rows.append(dict(N=N,iters=it,relax=rx,width=d['width'],min_deficit=d['min_deficit'],res=d['res'],state=state))
    print(f"  {N:>6} {it:>6} {rx:>6.2f} {d['width']:>9.4f} {d['min_deficit']:>10.3e} {d['res']:>9.1e} {state:>14}", flush=True)
OUT['guard_convergence_k8_0.1']=conv_rows

print("\n  EXISTENCE-BOUNDARY BISECTION in kappa8 (p=0.4): kappa8* where min(e^{-2phi})->0", flush=True)
lo, hi = 0.05, 0.07
for _ in range(10):
    mid=0.5*(lo+hi); _,d = run_pk(p_guard, mid, N=600, iters=120, relax=0.22)
    if d['min_deficit']>1e-4 and d['res']<1e-4: lo=mid
    else: hi=mid
k8star=0.5*(lo+hi)
print(f"    kappa8* (existence boundary, p=0.4) = {k8star:.5f}  (bracket [{lo:.5f},{hi:.5f}])", flush=True)
OUT['k8star_p0.4']=k8star
print(f"    order-parameter approach to kappa8*:", flush=True)
print(f"    {'k8star-k8':>10} {'width/L':>9} {'min_def':>10} {'min|eig|':>10} {'res':>9}", flush=True)
scal=[]
for frac in [0.30,0.15,0.07,0.03,0.01]:
    k8=k8star*(1-frac); o,d=run_pk(p_guard,k8,N=600,iters=140,relax=0.22)
    rn=o['r'][0].cpu().numpy();Tn=o['Th'][0].cpu().numpy();pn=o['phi'][0].cpu().numpy()
    try: me=float(np.min(np.abs(fluct_eigs(rn,Tn,pn))))
    except Exception: me=float('nan')
    scal.append(dict(d_k8=k8star-k8,width=d['width'],min_def=d['min_deficit'],mineig=me,res=d['res']))
    print(f"    {k8star-k8:>10.4f} {d['width']:>9.4f} {d['min_deficit']:>10.3e} {me:>10.3e} {d['res']:>9.1e}", flush=True)
OUT['k8star_scaling']=scal


# ===========================================================================
# TASK 1 -- THE SWEEP (kappa8 x depth p x seed) -> MAP of stable types
# ===========================================================================
hdr("TASK 1 -- THE SWEEP: (kappa8 x depth p x seed) -> the MAP of stable types")
k8_axis = [0.0,1e-3,1e-2,3e-2,5e-2,8e-2,1e-1,1.3e-1,1.6e-1]
p_axis  = [0.2,0.4,0.8,1.2,1.6,2.0]
seed_specs = [('round',0,0.0),('extranode',1,0.4),('twocore',0,0.5),
              ('legendre',1,0.4),('legendre',2,0.4)]
print(f"  kappa8 axis: {k8_axis}", flush=True)
print(f"  depth p axis: {p_axis} (phi(core)~-p, deep negative)", flush=True)
print(f"  seeds: {[s[0]+str(s[1]) for s in seed_specs]}", flush=True)
print(f"\n  Per cell: shaped/composite seed RELAX-TO-ROUND (one continuum) or PERSIST", flush=True)
print(f"  (distinct type)?  + existence (deficit>0).  DATA-BLIND M_MS recorded.\n", flush=True)
print(f"  {'p':>4} {'kap8':>6} {'seed':>11} {'exists':>7} {'width/L':>8} {'turns':>5} "
      f"{'->round?':>9} {'M_MS':>8} {'min_def':>9}", flush=True)
sweep=[]; round_prof={}
for p in p_axis:
    for k8 in k8_axis:
        diags = batch_seeds_pk(p, k8, seed_specs, N=N_DEF, iters=55, relax=0.45)
        # round is index 0
        d_r, Th_r, phi_r, r1_r = diags[0]
        Tn_r = Th_r[0].cpu().numpy()
        round_prof[(p,k8)] = (Th_r, phi_r, r1_r, d_r)
        for k,(d, Th_k, phi_k, r1_k) in enumerate(diags):
            if k==0:
                relaxed=True; dev=0.0
            else:
                Tn_k = Th_k[0].cpu().numpy()
                dev = float(np.max(np.abs(Tn_k - Tn_r)))
                relaxed = dev < 1e-3
            tag = "round" if relaxed else "DISTINCT"
            rec=dict(p=p,kap8=k8,seed=d['seed'],exists=d['exists'],width=d['width'],
                     turns=d['turns'],relaxed_to_round=relaxed,dev_from_round=dev,
                     M_MS=d['M_MS'],min_deficit=d['min_deficit'],res=d['res'])
            sweep.append(rec)
            print(f"  {p:>4.1f} {k8:>6.3g} {d['seed']:>11} {str(d['exists']):>7} "
                  f"{d['width']:>8.4f} {d['turns']:>5} {tag:>9} {d['M_MS']:>8.4f} {d['min_deficit']:>9.2e}", flush=True)
OUT['sweep']=sweep


# ===========================================================================
# BIFURCATION MAP: round-cell min|eig| over (p, kap8) [exists only]
# ===========================================================================
hdr("BIFURCATION MAP -- round-cell Jacobian min|eig| over (p, kap8) [exists only]")
print("  Zero-crossing = branch to a distinct stable type (pre-L4 #34 never crossed).", flush=True)
hl='p\\kap8'
print(f"\n  {hl:>8}", *[f"{k8:>9.3g}" for k8 in k8_axis], flush=True)
bif={}
for p in p_axis:
    row=[]
    for k8 in k8_axis:
        Th_r,phi_r,r1_r,d_r = round_prof[(p,k8)]
        if not d_r['exists']:
            row.append(float('nan')); continue
        rn=r1_r[0].cpu().numpy();Tn=Th_r[0].cpu().numpy();pn=phi_r[0].cpu().numpy()
        try: me=float(np.min(np.abs(fluct_eigs(rn,Tn,pn))))
        except Exception: me=float('nan')
        row.append(me); bif[(p,k8)]=me
    print(f"  {p:>8.1f}", *[f"{v:>9.3e}" for v in row], flush=True)
OUT['bifurcation_mineig']={f"{p}_{k8}":bif.get((p,k8)) for p in p_axis for k8 in k8_axis}


# ===========================================================================
# #38 FLIP RE-RUN WITH L4
# ===========================================================================
hdr("#38 FLIP DIAGNOSTIC RE-RUN WITH L4 (does L4 bound the forced angular completion?)")
print("  #38 (pre-L4): radial gradient FORCES an angular completion (K_theta large neg", flush=True)
print("  toward the seal) and 'NO bounding term exists'.  L4 adds +2 kappa X Y (>=0)", flush=True)
print("  to p_r+rho and +2k(s^4+s^2)T'^2 stiffness to the angular EL.  TEST: with L4,", flush=True)
print("  does any shaped seed PERSIST as a distinct existing type, and does round-cell", flush=True)
print("  min|eig| ever cross zero?", flush=True)
n_distinct = sum(1 for s in sweep if (not s['relaxed_to_round']) and s['exists'])
n_shaped = sum(1 for s in sweep if s['seed']!='round0' and s['exists'])
allmineig=[v for v in bif.values() if v==v]
print(f"\n  shaped/composite seeds that PERSISTED as a distinct existing type: "
      f"{n_distinct} / {n_shaped} existing shaped attempts", flush=True)
print(f"  round-cell min|eig| over existing map: [{min(allmineig):.3e},{max(allmineig):.3e}], "
      f"any <=0? {any(v<=0 for v in allmineig)}", flush=True)
OUT['n38_flip']=dict(n_distinct_persisting=n_distinct,n_shaped_existing=n_shaped,
                     mineig_min=min(allmineig),mineig_max=max(allmineig),
                     any_zero_crossing=any(v<=0 for v in allmineig))


# ===========================================================================
# SAVE
# ===========================================================================
hdr("STAGE B SWEEP COMPLETE")
def jclean(o):
    if isinstance(o,dict): return {k:jclean(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [jclean(v) for v in o]
    if isinstance(o,(np.bool_,)): return bool(o)
    if isinstance(o,(np.integer,)): return int(o)
    if isinstance(o,(np.floating,)): return float(o)
    if isinstance(o,float) and (o!=o): return None
    return o
with open("complete_metric_sweep_stageB_data.json","w") as fh:
    json.dump(jclean(OUT), fh, indent=1)
print(f"  total wall time {time.time()-t0:.1f}s", flush=True)
print(f"  GUARD: kappa8* existence boundary (p=0.4) = {OUT['k8star_p0.4']:.5f}", flush=True)
print(f"  SWEEP: {len(sweep)} members; distinct-persisting shaped types = {n_distinct}", flush=True)
print(f"  BIFURCATION: round-cell min|eig| zero-crossing anywhere? {OUT['n38_flip']['any_zero_crossing']}", flush=True)
print(f"  data -> complete_metric_sweep_stageB_data.json", flush=True)
