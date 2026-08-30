# G305 commands

From this package directory:

```bash
python3 derive_global_hopf_bridge.py
python3 verify_global_hopf_bridge_independent.py
python3 run_global_hopf_catches.py
python3 verify_package.py
python3 build_review_intake.py
```

The production and independent scripts write only their registered JSON outputs inside this
package. The verifier writes `PACKAGE_VERIFICATION_RESULT.json`. The intake builder writes a fresh
sealed repair-only review intake under `/tmp`; run the same three standard-library verifiers from a
writable ephemeral copy to certify its alternate source layout.
