# Handoff manifest scope

MANIFEST.sha256 pins the campaign evidence existing at seal, including this
scope note, initial candidates/objections, final reviews, source ledgers,
stdout/stderr/JSON capture records and the three current tracking documents.
Paths are relative to the repository root. Generate with sha256sum on the
explicit scoped file list and verify from that root with:

    sha256sum --check --quiet udt_observational_route_selection_campaign_2026-09-07/MANIFEST.sha256

Excluded to avoid circularity: MANIFEST.sha256 itself and the later
manifest_verification.{stdout,stderr,json} capture triple. Git commit and
push receipts are publication evidence, not mathematical evidence and not
self-referential payloads of this manifest. Later legitimate tracking updates
can change LIVE/HANDOFF/current program; authenticate their frozen versions
from this package's containing git commit, not by rewriting the manifest.

Public PDFs and the two schema-only CSV downloads remain temporary read-only
source material; precise official URLs, versions/record identifiers, sizes and
SHA hashes are retained in SOURCE_LEDGER.md and fetch records. They are not
represented as raw experimental data certification. No protected payloads,
unrelated dirt, backup or archive disk is hashed or incorporated here.

The full349-row audit was actually run before status changes. Final scoped
startup validation authenticates the updated tracking but is not another full
replay. Original scientific source, grade, canon and fixed-manuscript identity
is checked separately in PRESERVATION_CHECK.json/final_preservation.*. Review
independence axes and omitted checks remain in each actual review; checksums
cannot establish truth, independent authorship or blinded chronology.
