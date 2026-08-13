# Method map — clean angular-pattern restart

## What the reconnaissance found

Astroquery/VizieR can supply object catalogs but did not expose a complete measured angular
correlation curve plus covariance for the relevant BOSS/DESI analyses. The inspected publications
either provide fitted angular-peak summaries, leave the underlying curves available only by author
request, or obtain corrections/covariances from cosmology-generated mocks.

Those products remain useful later as labeled comparisons. They are not primary evidence here.

The locally present official BOSS DR12 clustering release already contains every field needed for a
fresh observer-coordinate measurement: measured sky positions, measured redshifts, observational
weights, and footprint/completeness random catalogs. No further bulk acquisition is justified.

## Why BOSS is primary

- final mature DR12 clustering release;
- separate North/South catalogs and randoms;
- raw pre-reconstruction observer-coordinate inputs already local;
- footprint randoms are documented by the collaboration;
- avoids DESI DR1's currently documented angular-completeness limitations in all but selected BGS
  samples.

DESI BGS remains a valuable independent replication after the BOSS method and covariance are locked.

## Phase structure

### R0 — current package

Freeze provenance, ontology, grids, weight lanes, estimator, nulls, uncertainty posture, and
conclusion ceiling. No pattern is evaluated.

### R1 — ingestion and null controls

Validate schemas and inputs, produce shell/cap population tables, create deterministic random
partitions, and prove estimator normalization on random-only controls. This phase may not inspect a
galaxy feature.

### R2 — central pattern atlas

Compute every registered shell/cap/weight/random-density curve with all angular bins retained.
Report what is present. Do not fit a peak, period, UDT scale, or physical interpretation.

### R3 — uncertainty and independent replay

Construct data-only spatial resampling covariances at every frozen block resolution and reproduce
the load-bearing pair counts through an independent implementation. No significance statement
precedes this phase.

### R4 — later scientific comparison

Only after R0-R3 are banked may a separately preregistered comparison ask how the one complete UDT
pair relation maps the observed pattern. SNe, `X_max`, CMB, and bootstrap parameters remain outside
the present package.

## Resource guard

Charles's hard ceiling for new downloads is below 2 TB. R0 uses no new survey download. Any later
acquisition must first record the URL, exact expected bytes, checksum availability, and why the
already local 36.6 GB BOSS+DESI corpus is insufficient.

