# G285 external-review transmission record

Date: 2026-08-27

- reviewer: external Codex `gpt-5.4`, high reasoning;
- authorized intake: `/tmp/udt_g285_review_05d4oarg`;
- intake mounted read-only at `/intake`;
- writable replay and return paths isolated at `/work` and `/return`;
- repository and protected packages not mounted;
- web search disabled; authentication file mounted read-only solely to launch the reviewer;
- 37 manifest payloads, all byte/hash verified before launch;
- `REVIEW_SCOPE.json` SHA-256:
  `10db4a9f43fe9532db5ad980e4c3f8330b99a7666e43e305785a18b8868caf73`;
- `REVIEW_MANIFEST.tsv` SHA-256:
  `b35d7848200ce76f8746f87234e07a4e71139ddd6280e9a604d924c51c9f7163`;
- detached seal SHA-256:
  `accfdbd9c66e15cd3402327fdf13be98c054ef329da69f1568b65cccbc101403`;
- raw returned report SHA-256:
  `65731e6a05b72ef7df32176314d64c9d0d035c8fe287e7c947e5462b077d8ebd`;
- full capture SHA-256:
  `2abb5a0779be6bb04621298768ad2d890ec456c771fd7af57d2e960f5c844307`;
- all five registered G285 commands replayed successfully;
- verdict: `ACCEPT_WITH_REPAIRS`;
- bounded scientific landing: supported unchanged;
- scientific defects: none;
- repairs: regrade the new G285 computations and counts as type-schema/retyping evidence rather
  than fresh witness-level exact derivation and independent geometric verification.
