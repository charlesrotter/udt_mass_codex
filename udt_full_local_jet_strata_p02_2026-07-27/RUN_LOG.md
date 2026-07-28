# P02 run log

Date: 2026-07-27

## P02-A

```text
python3 full_local_jet_atlas_gpu.py --production --package <package> --device cuda:0 --batch 512
python3 verify_full_local_jet_cpu.py CPU_ANCHOR_GPU.json --output CPU_ANCHOR_VERIFICATION.json --step 2e-4
python3 analyze_strata.py --package <package>
```

Result: 23,040 attempts; 15,459 constructed; all constructed finite.  GPU wall
time 2.8749 seconds; peak allocation 304,521,216 bytes.  Independent 64-anchor
CPU check passed.

## P02-B

```text
timeout 900s python3 solve_repeated_tidal_gpu.py --production --package <package> --device cuda:0 --response-base-batch 8 --evaluation-batch 512
python3 verify_repeated_tidal_cpu.py P02B_CPU_ANCHOR_GPU.json --output P02B_CPU_ANCHOR_VERIFICATION.json --step 2e-4
python3 analyze_repeated_tidal.py --package <package>
python3 verify_p02b_package.py --package <package> --output P02B_PACKAGE_VERIFICATION.json
```

Result: 12,594 of 12,594 targets constructed.  GPU wall time 9.0874 seconds;
peak allocation 383,059,968 bytes.  Independent 32-anchor CPU Riemann check
passed.  Independent package replay passed 32 checks and 15 mutation catches.

The unrelated 55-path dirty checkout was preserved and its contents were not
opened.
