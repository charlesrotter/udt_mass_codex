# G327 sealed replay precondition

The sealed intake itself remains read-only. Authenticate it first:

```text
python3 -S verify_review_intake.py
```

Then create a writable ephemeral copy before running the registered commands:

```text
cp -r /intake/. /work/g327_review_writable/
chmod -R u+w /work/g327_review_writable
cd /work/g327_review_writable
```

Run the four lines in `REPLAY_COMMANDS.txt` literally. They write only under `.review_runtime/` and
must not overwrite the sealed or banked evidence files.

The intake contains its exact symbolic dependencies in `VENDORED_SYMPY_RUNTIME.zip`. To prove the
host user site is not supplying them, the reviewer may run the four commands with
`PYTHONNOUSERSITE=1`; the registered programs activate only the sealed archive before importing
SymPy. No install or network access is required.
