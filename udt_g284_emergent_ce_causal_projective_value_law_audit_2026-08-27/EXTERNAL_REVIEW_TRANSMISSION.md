# G284 external-review transmission record

Date: 2026-08-27

- reviewer: external Codex `gpt-5.4`, high reasoning;
- authorized intake: `/tmp/udt_g284_review_08ulm6o7`;
- intake mounted read-only at `/intake`;
- writable replay and return paths isolated at `/work` and `/return`;
- repository and protected packages not mounted;
- web search disabled; authentication file mounted read-only solely to launch the reviewer;
- `REVIEW_SCOPE.json` SHA-256:
  `2f1a089f9b51b48ec302e551698d0a67d739cf43c0818770453a3c04175199f9`;
- `REVIEW_MANIFEST.tsv` SHA-256:
  `ee43aa4240ad5a4108f6e342cfddc66a260f9c340d0f0d4efab27b24d6a1f3d2`;
- detached seal SHA-256:
  `303658e0dd3c7bc8f87691db5226d16452e106525e4c961ca422465db360cc1a`;
- raw returned report SHA-256:
  `342905b72c7a87d66d7895d9e9a10dd719f76ef0aeca28b5b7c551d40fd98d68`;
- terminal response SHA-256:
  `63c40ae95a6a8cd9a3c38eb8783107c513d5667a3954a361cadf3782214461d2`;
- full capture SHA-256:
  `87110c5a83515e380c8ccffbfb48d32d60ea92ad1e99201b8733f4bebfba87b0`;
- verdict: `ACCEPT-WITH-REPAIRS`;
- bounded scientific landing: supported unchanged;
- scientific defects: none;
- repairs: one dependency/replay packaging repair and one package-verifier evidence repair.

The first review launcher omitted the customary read-only Python site-packages mount. The reviewer
therefore reproduced four of five registered commands and independently confirmed the core algebra,
but the SymPy production command failed before execution. The accepted repairs make the durable
sealed replay dependency-free and make the package verifier execute the registered recomputations;
they do not alter the scientific question or landing.
