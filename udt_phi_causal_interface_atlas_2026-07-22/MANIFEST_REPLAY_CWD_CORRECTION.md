# Manifest replay working-directory correction

The first manual manifest replay was invoked from repository root:

```text
sha256sum --check udt_phi_causal_interface_atlas_2026-07-22/MANIFEST.sha256
```

The manifest intentionally contains package-relative basenames, so that invocation could not find
its entries. The registered correction is to replay from the package directory:

```text
(cd udt_phi_causal_interface_atlas_2026-07-22 && sha256sum --check MANIFEST.sha256)
```

This is a command working-directory correction only. No scientific artifact, classification,
tolerance, candidate, or hash expectation was changed in response.
