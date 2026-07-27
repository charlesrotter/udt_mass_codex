# Append-only preregistration correction

Date: 2026-07-27

The frozen `SOURCE_UNIVERSE.tsv` row `S02` contains an incorrect abbreviated title and an
incorrect journal locator. The primary paper actually inspected is:

- J. L. Synge, “A Characteristic Function in Riemannian Space and its Application to the
  Solution of Geodesic Triangles,” *Proceedings of the London Mathematical Society*,
  s2-32(1), 241–258 (1931), DOI `10.1112/plms/s2-32.1.241`.

The preregistered source identity—Synge's 1931 characteristic/world-function construction—has not
changed. The frozen preregistration files remain untouched; all current source tables use the
corrected bibliographic identity.

Access grades are also recorded explicitly in `SOURCE_VERIFICATION.tsv`. A metadata or abstract
check is not treated as full-text authority. Sources `S06` and `S11` are not load-bearing beyond
their accessible primary metadata/abstract scope; stronger propositions are carried by the cited
full-text sources.
