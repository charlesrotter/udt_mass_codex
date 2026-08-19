# G170 external-review transmission record

Date: 2026-08-19

Charles explicitly authorized the sealed 31-file intake:

```text
/tmp/udt_g170_endpoint_relative_review_v23hsc3c
```

with `REVIEW_SCOPE.json` SHA-256:

```text
175d2ac6915269f3ef2a52621a500de765a8c55d0511dd9628f0431796fa98fa
```

After being informed of the credential-exposure risk, Charles separately authorized a read-only
mount of the local Codex authentication file. The successful reviewer run used a fresh ephemeral
external Codex `gpt-5.4`, high reasoning, web search disabled, approvals disabled, and an outer
mount sandbox exposing only the sealed intake, system runtime, resolver data, the read-only
authentication file, and a separate return directory. The repository and protected packages were
not mounted. The scope hash was rechecked unchanged after return.

The reviewer returned:

```text
ENDPOINT_RELATIVE_REPAIR_VALID_BUT_CALIBRATION_CARRY_STILL_LOAD_BEARING
```

Raw return SHA-256:

```text
082b9207559f9e412b0f6ec595f051a9b2831776fca5adb72868bbd0fff937a3
```

Transcript SHA-256:

```text
b72071d46b9ab44d4db90e2c30b621b4378063bba02882ad11ff42dcbf966d80
```

The return was accepted and triggered the bounded repair registered in
`REPAIR_PREREGISTRATION.md`.

## Repair-only follow-up

Charles explicitly authorized the corrected sealed 37-file intake:

```text
/tmp/udt_g170_endpoint_relative_review_4trovjya
```

with `REVIEW_SCOPE.json` SHA-256:

```text
4d57e43ae70bd1740b2fc5bbc3bf6823153eee38c6ae43b7663e4456a5b7e768
```

The follow-up retained the scientific landing and calibration-scope repair but found that the
sealed verifier's SymPy dependency was unavailable in the minimal external sandbox.

Raw follow-up SHA-256:

```text
2d3be594fcbf0c2330d495606b4f3c19db0215131a6f5b99d10f8495abbf943f
```

Follow-up transcript SHA-256:

```text
00b93696d1f71390a7f15bdc70eb5211a4440d5c94ca60ab5af8ca6f0088bf9b
```

## Final repair-only follow-up

Charles explicitly authorized the corrected sealed 41-file intake:

```text
/tmp/udt_g170_endpoint_relative_review_tugn7ht0
```

with `REVIEW_SCOPE.json` SHA-256:

```text
4a93b3863e0f926b5a4d001a68e2765bd4beb9a89fd7036298ea37f979664696
```

The reviewer successfully ran the dependency-free sealed replay and retained the theorem, but
required explicit propagation of `-S` to both standard-library child processes.

Raw final-follow-up SHA-256:

```text
867bba598174b7f54bad4248a65910c6404692c48f530a74596e6411c63f1b93
```

Final-follow-up transcript SHA-256:

```text
0258aa802d3cf60a8c55ec088f80e07e41edac93c5e131f4d22b802f40fefa12
```

## Final mechanical closure review

Charles explicitly authorized the corrected sealed 45-file intake:

```text
/tmp/udt_g170_endpoint_relative_review_dt0ufwhj
```

with `REVIEW_SCOPE.json` SHA-256:

```text
08f0da27039e123844e6fc889d3a3e3d9acaf63a5a1f4decbf1a31ee4050cf02
```

The reviewer ran the intake-contained verifier under `python3 -S`, observed both child `no_site`
flags as true, found no in-scope defect, and retained the consistent-calibration endpoint-relative
theorem unchanged.

Raw mechanical-closure return SHA-256:

```text
5a84ac9536436712d0bc13eb990fdeaa0be82f8bf92af72ce03993a2958b69cd
```

Mechanical-closure transcript SHA-256:

```text
52e7a0bd0bfee304478673ddd51047d6569aa309588230b88f5496fc52748363
```
