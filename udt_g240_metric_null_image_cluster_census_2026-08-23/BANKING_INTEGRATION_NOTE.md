# G240 banking integration note

Date: 2026-08-23

G240 preregistered and was externally reviewed against the exact 222-row premise registry whose
SHA-256 is
`c39015df67dd616bea5891a6dae51048ad0645797c51d85da8165b7a631e427e`.
That byte-exact registry is retained in both authorized sealed-review intakes and is bound by
`SOURCE_MANIFEST.tsv` and `TRANSMISSION_RECORD.md`.

After external repair acceptance, live banking adds the G240 premise row. The resulting 223-row
registry SHA-256 is
`fbb513a7ce86a32a75d7598acf3a090e7483dece944cc33c3df5735174356a67`.
Therefore `verify_package.py --no-write` correctly fails closed if it is pointed at the later live
repository while still asked to verify the frozen preregistration source manifest. This is expected
evidence immutability, not an R1 replay failure and not permission to refresh the frozen hash.

The two scopes are verified separately:

- G240 package/sealed replay: exact frozen 222-row source universe, externally accepted;
- live integrated premise surface: exact 223-row registry, checked by
  `verify_current_scientific_premises.py` and the repository test suite.

Do not rewrite `SOURCE_MANIFEST.tsv` to the 223-row hash or represent the later live registry as the
source reviewed in G240.
