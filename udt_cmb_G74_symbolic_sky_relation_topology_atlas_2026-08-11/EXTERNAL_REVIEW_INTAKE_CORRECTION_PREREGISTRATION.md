# G74 external-review intake-layout correction — preregistration

Date: 2026-08-11

## Failure preserved

The first authorized gpt-5.4 launch returned an intake-level `REFUTED` without inspecting the
scientific sources. The 34 manifest-listed payloads were present and independently hash-verified,
but `REVIEW_MANIFEST.tsv` was copied only to the intake root. The reviewer looked for the seal next
to `EXTERNAL_REVIEW_DISPATCH.md`, found it absent, and correctly stopped.

Preserved first-return hashes:

```text
raw         28aa54d37dab95ed15dcac2579927130292034b174f1cecb20dea0f05780bf1d
transcript  b2ff582d38835569208af3891c5453634c62ce97283056c6206b693f5259adcc
```

## Frozen correction

Create a fresh temporary intake from the unchanged `34/34` manifest-listed payloads. Copy the
unchanged manifest itself to

```text
udt_cmb_G74_symbolic_sky_relation_topology_atlas_2026-08-11/REVIEW_MANIFEST.tsv
```

inside that intake before making it read-only. Verify all 34 hashes again. The manifest SHA-256
must remain

```text
2d6b2fe483fdd9776d46534c9c95289827db545684d48fee87d78be59236fa19
```

No payload, scientific claim, threshold, script, result, source set, or review question may change.
The failed first return is provenance only and is not supplied as scientific evidence to the fresh
reviewer.

## Expected result

The fresh reviewer either verifies the seal and reaches the scientific audit or fails closed for a
new, explicitly reported reason. The first intake rejection carries no scientific verdict.
