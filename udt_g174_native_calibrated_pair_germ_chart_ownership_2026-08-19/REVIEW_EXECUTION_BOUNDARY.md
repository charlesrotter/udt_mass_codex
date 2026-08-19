# G174 review execution boundary

The external reviewer may inspect only the sealed intake built from this package and the exact 12
files in `SOURCE_MANIFEST.tsv`. It may execute the included verification scripts in a writable
temporary directory.

It must not edit the repository, continue the research, use the internet, inspect unlisted files,
or access protected packages. Repository-side verification and sealed-intake replay are different
gates and must not be conflated.
