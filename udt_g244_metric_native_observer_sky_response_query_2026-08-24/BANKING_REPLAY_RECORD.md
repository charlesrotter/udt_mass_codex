# G244 banking replay record

Date: 2026-08-24

After the append-only G244 premise and startup integration:

- the live registry contains 227 data rows and exactly one `G244` row;
- removing exactly that row reconstructs the preregistration registry SHA-256
  `1cad6bf0a437157a87013f0ac718a6e54213f093a6088670ed5ad7e233668126`;
- `python3 verify_package.py --no-write` returns `PASS` with all 13 checks true;
- the production and independent routes retain 1,024/5,000 exact matrix cases and
  1,024/5,000 exact phase cases;
- 14/14 hostile mutations remain caught;
- `python3 verify_current_scientific_premises.py` returns `PASS` for the 227-row authority.
- the full repository suite returns `149 passed, 1 xfailed` (the documented HABIT-pin xfail).

This is provenance and startup integration evidence only. It changes no G244 scientific result.
