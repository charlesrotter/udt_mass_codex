# Source-freeze path repair

The preregistration manifest originally pointed to live `CURRENT_SCIENTIFIC_PREMISES.tsv` at SHA-256
`d51c637251f9cc0a6bb27bc71d3bf6aa61462a85cc551fada8f866749587a843`.

Before banking G165 into that live registry, its exact preregistration-time bytes were copied into
`SOURCE_FREEZE_CURRENT_SCIENTIFIC_PREMISES.tsv`. The manifest path now points to that byte-identical
snapshot. The hash and scientific input are unchanged; only the path was repaired so later live
registry updates cannot invalidate the frozen evidence universe.
