# M1 DATA-PROVENANCE RECON — x_max SCALE lane (BAO leg + Pantheon+ confirm)

Date: 2026-08-07. Agent: M1 recon (read-only; nothing on the scratch disk modified;
no correlations computed). Governing doc: `udt_xmax_scale_observational_MAP_2026-08-07.md`
(§0 ontology rule, §2 V-BAO design, §4 forbidden-imports F-IMPORT-LCDM, CP5 ruling:
astroquery permitted, ~100 GiB total budget, no bulk downloads at recon, <~1 GiB now).
Intended use audited against: ANGULAR correlations in thin redshift shells, observable
space (RA/dec/z) only, no distance model.

## 1. On-disk DESI DR1 inventory (`/media/udt-admin/ScratchDisk/Data/desi_dr1`, 30 GiB)

Provenance: DESI DR1 (iron) LSS clustering catalogs (header `DESIDR='dr1'`; DESI data
model). Naming matches the public v1.5 LSScats `*_clustering.dat.fits` /
`*_{0..3}_clustering.ran.fits` pattern = the FULL-SURVEY LSS catalogs AFTER veto masks
and completeness assignment, BEFORE reconstruction. Four tracers, NGC+SGC each, one
data catalog + 4 random files per (tracer, cap). 42 files total.

| Tracer | Caps | N_data (NGC+SGC) | z range | dat size | 4x ran size (per cap) |
|---|---|---|---|---|---|
| BGS_BRIGHT | NGC+SGC | 2,909,876 + 1,047,989 | 0.010 – 0.500 | 340 + 123 MB | 4x1.66 GB + 4x0.68 GB |
| LRG | NGC+SGC | 1,476,135 + 662,492 | 0.400 – 1.100 | 143 + 64 MB | 4x0.99 GB + 4x0.52 GB |
| ELG_LOPnotqso | NGC+SGC | 1,821,322 + 610,750 | 0.800 – 1.600 | 206 + 69 MB | 4x1.18 GB + 4x0.62 GB |
| QSO | NGC+SGC | 793,219 + 430,172 | 0.800 – 3.500 | 83 + 45 MB | 4x1.31 GB + 4x0.74 GB |

Total data rows 9.75M; randoms ~44M rows per random file set (e.g. BGS NGC ran_0 =
13.2M rows; randoms are ~4-5x data density per file, 4 files = ~18x). Continuous z
coverage 0.01–3.5 across tracers (gap: none; overlaps at 0.4–0.5, 0.8–1.1).

Columns (data): TARGETID, RA, DEC, Z, NTILE, PHOTSYS, FRAC_TLOBS_TILES, WEIGHT_ZFAIL,
WEIGHT_SYS, WEIGHT, WEIGHT_COMP, NX, WEIGHT_FKP (+ per-tracer extras: BGS dereddened
fluxes g/r/z/W1/W2; ELG WEIGHT_SN+WEIGHT_RF; QSO WEIGHT_RF). Columns (randoms): same
weight set + TARGETID_DATA (the data galaxy each random inherited attributes from —
the signature of the "shuffled" random-redshift method). No XY/Z cartesian columns,
no displacement/recon columns anywhere — PRE-RECONSTRUCTION CONFIRMED (DESI recon
products carry a distinct `...MGrecsym/reciso` tag and cartesian shifts; absent here).

Observed weight behavior (first-200k spot checks): WEIGHT ≈ WEIGHT_COMP × WEIGHT_SYS ×
WEIGHT_ZFAIL (BGS WEIGHT_SYS ≡ 1; ELG/QSO WEIGHT_SYS from RF/SYSNet imaging
regressions, range ~0.68–2.0). WEIGHT_FKP strongly tracer-dependent (BGS mean 0.05,
QSO mean 0.87) — consistent with FKP = 1/(1+NX·P0), NX in comoving (h/Mpc)^3 units.

## 2. Processing-chain audit (for angular correlations in thin z-shells)

Grades: CLEAN / RE-DERIVABLE / CONTAMINATED-AVOIDABLE / CONTAMINATED-FATAL.

| Layer | What it is | Cosmology content | Grade |
|---|---|---|---|
| RA, DEC | astrometry | none | CLEAN |
| Z | Redrock spectro redshift (PCA galaxy/QSO templates fit to spectra) | astrophysical templates, no cosmological model; z is the raw observable of this lane | CLEAN (note: template-fitting provenance, not cosmology) |
| z-range cuts per tracer (e.g. LRG 0.4–1.1) | catalog definition cuts | cuts chosen by DESI for their science, but a z-cut is an observable-space selection | CLEAN (scope-limiting only) |
| WEIGHT_COMP, NTILE, FRAC_TLOBS_TILES | fiber-assignment completeness from tiling geometry | pure survey geometry | CLEAN |
| WEIGHT_ZFAIL | redshift-failure rate vs fiber/hardware | instrumental | CLEAN |
| WEIGHT_SYS (ELG: SYSNet/RF; QSO: RF; LRG: linear; BGS: ≡1) | regression of target density vs IMAGING maps (depth, extinction, stars, seeing) | cosmology-free inputs; CAVEAT: regression can absorb real large-angle clustering power (over-correction) — a systematics risk, not a ΛCDM import; test with/without in M3 | CLEAN (with over-correction caveat) |
| NX | comoving number density n(z) in (h/Mpc)^3, computed with the DESI FIDUCIAL ΛCDM distance-redshift relation | FIDUCIAL COSMOLOGY inside | CONTAMINATED-AVOIDABLE (do not use). Native replacement if density weighting ever needed: dN/dz per steradian — purely observable. RE-DERIVABLE natively. |
| WEIGHT_FKP = 1/(1+NX·P0) | variance-optimal weight; P0 = fiducial power amplitude at k~0.1 h/Mpc | inherits NX's fiducial + a ΛCDM P(k) amplitude choice | CONTAMINATED-AVOIDABLE (optional by construction; standard estimators run without it at modest S/N cost). Do not use. |
| Reconstruction fields | ΛCDM-gravity displacement of galaxies | forbidden outright | ABSENT from these files (confirmed §1) — the on-disk products are pre-recon |
| Randoms: RA/DEC | uniform sampling of the as-observed footprint (tiles+vetoes), subsampled to match completeness | pure geometry | CLEAN |
| Randoms: Z | "shuffled" method — z values drawn from the DATA catalog (TARGETID_DATA present) | observable-space by construction; no n(z) model, no fiducial | CLEAN for z-shell angular use. Known effect: radial-mode suppression at very large line-of-sight scales — irrelevant for ANGULAR correlations within a shell; note for any future dz_BAO use. |
| Randoms: NX, WEIGHT_FKP | as data | fiducial | CONTAMINATED-AVOIDABLE (ignore columns) |

AUDIT VERDICT for the on-disk product: the catalogs are usable NATIVELY. The full
forbidden list (acoustic story, r_d, fiducial z→distance conversion, ΛCDM template
fits, reconstruction) either does not touch these files or sits in two OPTIONAL
columns (NX, WEIGHT_FKP) that we simply never read. The clean estimator: pair counts
in (theta) within thin z-shells, weights = WEIGHT (comp×sys×zfail) only, randoms'
own WEIGHT likewise; every input then RA/dec/z + geometry.

Residual honest caveats (carried to M2 prereg): (i) WEIGHT_SYS over-correction risk —
run with/without as a systematic; (ii) Redrock template provenance on Z; (iii)
P-STATIC-RULER is a premise of the USE, not of the data; (iv) shell width choice
trades signal dilution vs counts — an analysis choice to preregister, not a
contamination; (v) DR1 per-shell S/N for a theta-feature detection is an open M2/M3
question (DESI's own detections integrate over wide z bins in comoving space; thin
observable-space shells are lower S/N — a genuinely harder measurement).

## 3. Wider landscape (metadata only; nothing bulk-downloaded)

**3a. DESI DR1, not on disk** (public listing v1.5, data.desi.lbl.gov confirmed 2026-08-07):
tracers BGS_ANY, BGS_BRIGHT-21.5 (abs-mag-limited BGS), LRG+ELG_LOPnotqso combined; 18 random
files per (tracer,cap) vs our 4; per-cap nz.txt files; frac_tlobs.fits. NO recon/recsym files
in the LSScats directory at all. Cost: extra randoms ~0.6-1.7 GB each (14 more per cap per
tracer ~ 60+ GB — NOT needed; 4 randoms = ~18x data density, ample for w(theta)).
BGS_BRIGHT-21.5 dat is small (~100s MB) — optional later fetch if a luminosity-stable
low-z subsample is wanted. nz.txt files: fiducial-comoving n(z) — contaminated, skip.
DESI DR2: LSS catalogs NOT public yet (as of 2026-08; DR2 cosmology chains only). No action.

**3b. SDSS BOSS DR12** (data.sdss.org/sas/dr12/boss/lss/, listing confirmed): galaxy_DR12v5_
{LOWZ,CMASS,CMASSLOWZTOT,+E2/E3}_{North,South}.fits.gz, 32-216 MB each; random0/random1 files
0.7-3.2 GB each; masks ~2-18 MB. These are the OBSERVED-position (pre-recon) LSS catalogs
(Reid et al. 2016); no recon variants in the public directory. Columns (known data model):
RA/DEC/Z + WEIGHT_SYSTOT/CP/NOZ + WEIGHT_FKP + NZ — same contamination profile as DESI:
FKP/NZ avoidable, rest survey-geometry. z 0.15-0.75. Cost if fetched: ~0.5 GB data + ~4-8 GB
randoms. Value: independent survey/instrument cross-check in the 0.2-0.75 overlap.

**3c. eBOSS DR16** (data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/, listing confirmed):
LRG, LRGpCMASS, ELG, QSO x NGC/SGC; clustering dat 5-16 MB, randoms 0.2-1.3 GB. WARNING:
this directory DOES contain `_rec` (reconstructed) data+random variants for ELG/LRGpCMASS/QSO
— those are CONTAMINATED-FATAL (LCDM displacement fields); the non-rec files are the usable
ones. File choice must be explicit in any fetch. Cost non-rec: ~2-4 GB. Value: QSO z 0.8-2.2
cross-check of DESI QSO.

**3d. Published angular theta_BAO(z) series ("transverse BAO"; audited from Carvalho et al.
1709.00271 full text + series abstracts):** SDSS DR7/DR10/DR11/DR12Q measurements by
Alcaniz/Carvalho/de Carvalho/Bernui et al., ~13-15 points z=0.11-2.225 (KB-scale tables).
HOW model-independent, precisely: (i) measurement = Landy-Szalay w(theta) in thin shells
(dz=0.01-0.02), catalog weights only, NO z->distance conversion, NO reconstruction — CLEAN;
(ii) bump localized by parametric fit w=A+B*theta^nu+C*exp(-(theta-theta_FIT)^2/2sig^2) —
template-LITE (a generic bump, not a LCDM template) — acceptable; (iii) BUT the published
theta_BAO applies a projection correction alpha(z,dz) converting theta_FIT -> theta_BAO,
computed from a FIDUCIAL LCDM P(k) (their Table 2: omega_b h^2=0.0226 etc.). Size of the
contamination: alpha = 0.28%-1.44% for the DR11 dz<=0.01-0.02 shells (their Table 3) — small,
QUANTIFIED, and removable (theta_FIT is tabulated separately). Grade: QUASI-CLEAN /
CONTAMINATED-AVOIDABLE if we use theta_FIT + forward-model the shell width natively; the
low-z points (z=0.11, wide shells) carry larger alpha — check per point before use. Also:
bump-identification criteria partially reference expected-scale reasoning in the earliest
papers (F-IMPORT watch item). Use: CROSS-CHECK ONLY, never primary — our own DESI
measurement is strictly cleaner (we control the correction natively).

**3e. Other:** published DESI/BOSS BAO "measurements" (D_M/r_d, D_V/r_d tables) —
CONTAMINATED-FATAL for this lane (fiducial conversion + LCDM template + recon + r_d
calibration); use for nothing. Lyman-alpha BAO — fatal (continuum fitting + fiducial grids).
WiggleZ final: pre-recon catalogs exist (~100s MB) but shallow/noisy vs DESI — skip.
CMB acoustic peaks — out of scope (different observable, heavier ontology load).

## 4. Recommended acquisition + use plan (budget ~100 GiB; used now: 0 new GiB)

1. PRIMARY: use the on-disk DESI DR1 catalogs AS-IS (30 GiB already local). Inputs to M2:
   RA/DEC/Z + WEIGHT (and its factors for with/without systematics tests) from dat+ran;
   NEVER read NX/WEIGHT_FKP; randoms' Z is shuffled-from-data (clean). All four tracers,
   both caps; z coverage 0.01-3.5.
2. OPTIONAL cross-check fetch (defer to M3, on Charles's go): BOSS DR12 CMASSLOWZTOT
   North+South + random0 (~5 GB) and/or eBOSS DR16 QSO non-rec (~1.5 GB). Explicitly
   EXCLUDE any `_rec` file. Total <10 GiB — comfortably in budget.
3. FETCH-NOTHING items: extra DESI randoms (not needed), nz.txt (contaminated), DR2 (not
   public), published D_X/r_d tables (fatal), Ly-a (fatal).
4. Literature theta_BAO table (KB): transcribe theta_FIT and alpha per point from the
   papers at M3 time for a cross-check panel, carrying the alpha caveat per point.
5. Pantheon+ CONFIRMED on disk and readable: Data/Pantheon+SH0ES.dat = 1701 rows x 47 cols
   (zHD/zCMB/zHEL, m_b_corr, MU_SH0ES, CEPH_DIST, IS_CALIBRATOR all present);
   Data/Pantheon+SH0ES_STAT+SYS.cov = header "1701" + 1701^2 = 2,893,401 elements. Complete.
   SNe provenance notes for M2's ledger: zHD carries peculiar-velocity/flow-model
   corrections (zCMB/zHEL raw columns available as the cleaner input); m_b_corr carries
   BBC bias corrections whose simulations assume a fiducial cosmology (known, to be tagged
   in the V-SNe prereg — standard but not zero).

## 5. Verdict

**BAO leg: VIABLE-NATIVELY** with the on-disk DESI DR1 pre-reconstruction catalogs.
Named residual caveats (none blocking, all tagged for M2 prereg): WEIGHT_SYS
over-correction risk (test with/without); Redrock template provenance of Z; P-STATIC-RULER
premise (of the use, not the data); thin-shell S/N is the real risk — DR1 may yield a
low-significance theta feature per shell (an honest outcome, not a contamination); the
literature theta_BAO series is cross-check-grade only (quantified ~0.3-1.5% LCDM projection
correction). The forbidden-import list is fully avoidable at the catalog level: no acoustic
story, no r_d, no fiducial conversion, no template, no reconstruction enters the planned
observable-space pipeline.
