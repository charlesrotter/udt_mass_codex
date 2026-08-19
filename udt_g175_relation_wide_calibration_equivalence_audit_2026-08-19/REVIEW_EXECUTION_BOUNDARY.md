# G175 review execution boundary

The reviewer may inspect only the sealed intake built from this package and the eight frozen files
in `SOURCE_MANIFEST.tsv`. It may execute the included read-only verifier with scratch output outside
the intake. It must not edit files, continue the research, use the internet, access the repository,
or inspect protected packages.

`verify_package.py` is the repository outer gate. In a sealed intake it detects
`REVIEW_SCOPE.json` and delegates to `verify_sealed_intake.py`.
