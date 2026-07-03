"""s2_aggregate.py -- collect per-rung checkpoints into the stage-2 table + audit lists."""
import json, os, glob
import numpy as np

SCRATCH = os.path.dirname(os.path.abspath(__file__))
ORDER = [f"B{n:02d}" for n in range(23)] + ['A00', 'A08', 'A09', 'A10', 'A11', 'SM2', 'SZ1']
R = {}
for tag in ORDER:
    f = os.path.join(SCRATCH, f"s2_rung_{tag}.json")
    R[tag] = json.load(open(f))

print("="*145)
print("MAIN TABLE: per rung x column -- pair (n_neg(S_u), n_pos(V^)) at M_rung and 2*M_rung "
      "(pinned v0=0 convention; raw route = banked convention)")
print("="*145)
hdr = (f"{'tag':4s} {'side':10s} {'N':>2s} {'a*':>14s} {'Up_c':>10s} {'M_rung':>6s} "
       f"{'FREE':>10s} {'ANCH':>10s} {'FIXD':>10s} {'stab':>5s} {'reprod':>8s}")
print(hdr)
for tag in ORDER:
    r = R[tag]
    ps = r['pair_stability']
    pf = lambda c: f"({ps[c]['pair_M'][0]},{ps[c]['pair_M'][1]})"
    st = ''.join('Y' if ps[c]['grid_stable'] else 'N' for c in ('FREE', 'ANCHORED', 'FIXED'))
    print(f"{tag:4s} {r['side']:10s} {r['N']:2d} {r['a']:14.10f} {r['Up_c']:+10.5f} "
          f"{r['M_rung']:6d} {pf('FREE'):>10s} {pf('ANCHORED'):>10s} {pf('FIXED'):>10s} "
          f"{st:>5s} {r['reproduction']['verdict']:>8s}")

print()
print("="*145)
print("PER-RUNG DETAIL (dense M=1600 unless noted): identities, translation, lowest-3 full-form "
      "eigenvalues (lumped-mass normalization, CHOSE flagged; magnitudes carry the near-singular-V^ caveat)")
print("="*145)
for tag in ORDER:
    r = R[tag]
    print(f"\n--- {tag} (side={r['side']} N={r['N']} m={r['m']} Z={r['Z']}) "
          f"r_s={r['r_s']:.4f} rho_s={r['rho_s']:.6f} q={r['q']:.6f} "
          f"U'(rho_c)={r['Up_c']:+.6f} lam_seal={r['lam_seal']:.3f} M_rung={r['M_rung']}")
    rep = r['reproduction']
    dets = {k: f"{v['rel']:.1e}" for k, v in rep.items() if isinstance(v, dict)}
    print(f"    reproduction {rep['verdict']} (rel: {dets})")
    for col in ('FREE', 'ANCHORED', 'FIXED'):
        d8, d16 = r['dense'][f'{col}/M800'], r['dense'][f'{col}/M1600']
        bM = r['bigM'][f"{col}/M{r['M_rung']}"]; b2M = r['bigM'][f"{col}/M{2*r['M_rung']}"]
        idok8 = (d8['identity_haynsworth'] and (d8['identity_hyperbolic'] in (True, None)))
        idok16 = (d16['identity_haynsworth'] and (d16['identity_hyperbolic'] in (True, None)))
        pair_d8, pair_d16 = tuple(d8['pair']), tuple(d16['pair'])
        line = (f"  [{col:8s}] pair: M800={pair_d8} M1600={pair_d16} "
                f"M{bM['M']}={tuple(bM['pair'])} M{b2M['M']}={tuple(b2M['pair'])} | "
                f"identities(H,hyp) M800={'OK' if idok8 else 'VIOL'} M1600={'OK' if idok16 else 'VIOL'} | "
                f"finiteQmV: {d8['finite_part_nnegQ_minus_nnegV']},{d16['finite_part_nnegQ_minus_nnegV']},"
                f"{bM['finite_part_nnegQ_minus_nnegV']},{b2M['finite_part_nnegQ_minus_nnegV']}")
        print(line)
        print(f"             low3(full,M1600)={['%.3e' % x for x in d16['near0_full'][:3]]} "
              f"low3(S_u,M1600)={['%.3e' % x for x in d16['Su_low3']]} "
              f"Vmin|eig| M1600={d16['V_min_abs_eig']:.3e} bigM={bM['V_min_abs_eig']:.3e}")
        if col in ('FREE', 'ANCHORED'):
            print(f"             translation: RQ M800={d8['translation_RQ']:+.3e} M1600={d16['translation_RQ']:+.3e} "
                  f"bigM={bM['translation_RQ']:+.3e} 2M={b2M['translation_RQ']:+.3e} "
                  f"eig_id={d16['translation_eig']:+.3e}(ovl {d16['translation_overlap']:.2f}) "
                  f"defl-diag(dense16,bigM,2M)=({d16['inertia_full_raw'][0]-d16['inertia_full_deflated'][0]},"
                  f"{bM['translation_resolved_negative']},{b2M['translation_resolved_negative']})")
            bz = d16['near0_beyond_translation'][0]
            print(f"             almost-zero beyond translation (M1600): {bz:+.3e} "
                  f"|ratio to translation eig|={abs(bz/d16['translation_eig']):.2f} "
                  f"|ratio to Up_c|={abs(bz/r['Up_c']):.3f}")
        if col == 'FIXED' and 'inertia_Su_v0deleted' in d16:
            print(f"             FIXED v0-deleted diagnostic: nneg(S_u)={d16['inertia_Su_v0deleted'][0]} "
                  f"(kept-side primary: {d16['inertia_Su'][0]})")

print()
print("="*100)
print("BELOW-SIDE FREE-COLUMN SEQUENCES vs N (raw sequences, no fits)")
print("="*100)
ns = list(range(23))
su = [R[f'B{n:02d}']['pair_stability']['FREE']['pair_M'][0] for n in ns]
vp = [R[f'B{n:02d}']['pair_stability']['FREE']['pair_M'][1] for n in ns]
print("N        :", ns)
print("n_neg(Su):", su)
print("n_pos(V^):", vp)
for col in ('ANCHORED', 'FIXED'):
    su2 = [R[f'B{n:02d}']['pair_stability'][col]['pair_M'][0] for n in ns]
    vp2 = [R[f'B{n:02d}']['pair_stability'][col]['pair_M'][1] for n in ns]
    print(f"{col}: n_neg(Su): {su2}")
    print(f"{col}: n_pos(V^): {vp2}")

print()
print("="*100)
print("ABOVE-vs-BELOW ROW-PAIRS at equal N (FREE column, M_rung pairs)")
print("="*100)
for N, atag in ((0, 'A00'), (8, 'A08'), (9, 'A09'), (10, 'A10'), (11, 'A11')):
    btag = f'B{N:02d}'
    pa = R[atag]['pair_stability']; pb = R[btag]['pair_stability']
    print(f"N={N:2d}: above {atag} FREE={tuple(pa['FREE']['pair_M'])} ANCH={tuple(pa['ANCHORED']['pair_M'])} "
          f"FIXD={tuple(pa['FIXED']['pair_M'])}  Up_c={R[atag]['Up_c']:+.5f} | "
          f"below {btag} FREE={tuple(pb['FREE']['pair_M'])} ANCH={tuple(pb['ANCHORED']['pair_M'])} "
          f"FIXD={tuple(pb['FIXED']['pair_M'])}  Up_c={R[btag]['Up_c']:+.5f}")

print()
print("="*100)
print("GAPS / WOBBLES / FLAGS (complete list)")
print("="*100)
issues = []
for tag in ORDER:
    r = R[tag]
    if r['reproduction']['verdict'] != 'PASS':
        issues.append(f"{tag}: reproduction {r['reproduction']['verdict']} "
                      f"(worst rel {r['reproduction']['worst_rel']:.2e}; tol {r['reproduction']['tol_pass']:.0e})")
    for col in ('FREE', 'ANCHORED', 'FIXED'):
        if not r['pair_stability'][col]['grid_stable']:
            issues.append(f"{tag}/{col}: pair NOT grid-stable "
                          f"{r['pair_stability'][col]['pair_M']} vs {r['pair_stability'][col]['pair_2M']}")
        for Mk in ('M800', 'M1600'):
            d = r['dense'][f'{col}/{Mk}']
            if not d['identity_haynsworth']:
                issues.append(f"{tag}/{col}/{Mk}: Haynsworth count mismatch")
            if d['identity_hyperbolic'] is False:
                issues.append(f"{tag}/{col}/{Mk}: hyperbolic count mismatch")
            if not d['V_sturm_match']:
                issues.append(f"{tag}/{col}/{Mk}: Sturm vs dense V^ mismatch")
            if d['V_tridiag_maxoff'] != 0.0:
                issues.append(f"{tag}/{col}/{Mk}: V^ not tridiagonal")
            if d['inertia_full_raw'][2] > 0:
                issues.append(f"{tag}/{col}/{Mk}: {d['inertia_full_raw'][2]} tolerance-zero eig(s) in full count")
            if d['block_nneg'] != d['inertia_full_raw'][0]:
                issues.append(f"{tag}/{col}/{Mk}: block({d['block_nneg']}) != dense({d['inertia_full_raw'][0]})")
            if col in ('FREE', 'ANCHORED') and d['inertia_full_deflated'][0] != d['block_nneg_deflated']:
                issues.append(f"{tag}/{col}/{Mk}: deflation dense({d['inertia_full_deflated'][0]}) "
                              f"!= bordered({d['block_nneg_deflated']})")
        for Mk in (r['M_rung'], 2*r['M_rung']):
            b = r['bigM'][f'{col}/M{Mk}']
            if b['nzero_Q'] > 0:
                issues.append(f"{tag}/{col}/M{Mk}: {b['nzero_Q']} near-singular pivot(s) in block route")
            for fl in b['block_flags']:
                issues.append(f"{tag}/{col}/M{Mk}: block flag {fl}")
            if b['nzero_V'] > 0:
                issues.append(f"{tag}/{col}/M{Mk}: V^ Sturm n_zero={b['nzero_V']}")
        # finite-part consistency across all four grids
        f_parts = [r['dense'][f'{col}/M800']['finite_part_nnegQ_minus_nnegV'],
                   r['dense'][f'{col}/M1600']['finite_part_nnegQ_minus_nnegV'],
                   r['bigM'][f"{col}/M{r['M_rung']}"]['finite_part_nnegQ_minus_nnegV'],
                   r['bigM'][f"{col}/M{2*r['M_rung']}"]['finite_part_nnegQ_minus_nnegV']]
        if len(set(f_parts)) > 1:
            issues.append(f"{tag}/{col}: finite part n_neg(Q)-n_neg(V^) varies across grids: {f_parts}")
    # translation-resolved sign wobbles across grids (FREE)
    dd = [r['dense']['FREE/M1600']['inertia_full_raw'][0] - r['dense']['FREE/M1600']['inertia_full_deflated'][0],
          r['bigM'][f"FREE/M{r['M_rung']}"]['translation_resolved_negative'],
          r['bigM'][f"FREE/M{2*r['M_rung']}"]['translation_resolved_negative']]
    if len(set(dd)) > 1:
        issues.append(f"{tag}/FREE: translation-resolved near-zero sign varies across grids "
                      f"(defl-diag M1600,bigM,2M = {dd}) [pre-named deflation-residual background]")
if issues:
    for i in issues: print(" -", i)
else:
    print(" (none)")

json.dump({t: R[t] for t in ORDER}, open(os.path.join(SCRATCH, 's2_final_table.json'), 'w'),
          indent=1, default=str)
print("\nsaved s2_final_table.json")
shots = json.load(open(os.path.join(SCRATCH, 's2_shot_log.json')))
print(f"IVP shots used: {len(shots)}")
