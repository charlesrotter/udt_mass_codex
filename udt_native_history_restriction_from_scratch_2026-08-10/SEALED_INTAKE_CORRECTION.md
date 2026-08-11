# Sealed-intake correction

The preregistered `verify_preregistration.py` is preserved unchanged as historical evidence. It
correctly resolves the ten frozen sources in repository layout, but the external intake relocated
those sources below `sources/`, so that historical verifier was not transport-correct.

`verify_sealed_intake.py` is the append-only correction. It detects exactly one complete layout:
repository-relative sources beside the package, or manifest-relative sources below the sealed
intake's `sources/` directory. It verifies all ten frozen SHA-256 identities and rejects either
protected source family. This is a packaging correction and changes no scientific premise or
preregistered candidate set.

After the G61 result is incorporated into the live premise registry, its current working-tree hash
properly differs from the frozen G60 source identity. `verify_fixed_base_sources.py` therefore
replays all ten identities from the preregistered Git base, while `verify_sealed_intake.py` replays
the transported copies. The historical verifier remains unchanged.
