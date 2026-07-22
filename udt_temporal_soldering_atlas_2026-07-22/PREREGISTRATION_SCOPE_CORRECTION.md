# Preregistration Scope Correction — Path-Continuation Provenance

Date: 2026-07-22  
Original preregistration commit: `7573136`

## Trigger

After the original preregistration, inspection of the already frozen global-assembly builder showed
that `PATH_ASSEMBLY_CENSUS.tsv.gz` is a reduced projection of the earlier motif/Hopf path-continuation
package. The omitted parent filenames were discovered from source code and filename listing only;
their table contents have not been opened for this audit.

## Frozen addition

Before opening them, add every row/record at base `d7a2469` in:

1. `udt_motif_hopf_correspondence_audit_2026-07-22/COHERENT_IDENTITY_REGISTRY.tsv`
2. `udt_motif_hopf_correspondence_audit_2026-07-22/PATH_FAMILY_ATLAS.tsv.gz`
3. `udt_motif_hopf_correspondence_audit_2026-07-22/PATH_CONTINUATION_SUMMARY.tsv.gz`
4. `udt_motif_hopf_correspondence_audit_2026-07-22/PATH_MOTIF_PERSISTENCE.tsv`
5. `udt_motif_hopf_correspondence_audit_2026-07-22/DISTRIBUTION_ATLAS.tsv.gz`
6. `udt_motif_hopf_correspondence_audit_2026-07-22/DISTRIBUTION_CENSUS.tsv`
7. `udt_motif_hopf_correspondence_audit_2026-07-22/FAMILY_TRANSITION_CENSUS.tsv`
8. `udt_motif_hopf_correspondence_audit_2026-07-22/MIDPOINT_MOTIF_CENSUS.tsv`

These are parent evidence for the already frozen 95,232 path identities, not a second candidate
universe. The corrected audit must build an explicit identity/overlap map and prevent double
counting between parent path rows and the later assembly projection.

All classifications, falsification gates, and the maximum conclusion in the original
preregistration remain unchanged.
