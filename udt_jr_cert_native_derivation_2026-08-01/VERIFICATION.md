# Verification record

## Final grade

`CLOSED-PASS_BOUNDED`

Retained outcome:

`NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED`

## Preregistration and sources

- initial 172-path preregistration: committed at `b59d6c7`;
- append-only 414-path transitive closure: committed at `148db3b`;
- exact governing union: 586 unique paths, zero overlap;
- frozen bytes independently replayed: 16,514,116;
- source bases, Git blobs, SHA-256 values, byte counts, ten package enumerations, and sorted union:
  pass.

## Primary checks

- exact arbitrary-`phi` Cartan/Levi/Bianchi control: pass;
- exact seal family and two-/four-derivative variation controls: pass;
- E01–E08 coverage: 8/8, zero pass;
- B01–B06 coverage: 6/6, zero pass;
- launch-guard truth table: 4/4;
- primary verifier: pass, 14/14 structural mutations rejected;
- source anchors: 14/14 present and hash-exact.

## Fresh cold checks

`COLD_VERIFIER_CHECK.py` imports neither production implementation. It independently reads exact
base-tree blobs, computes curvature by a different full-Riemann contraction, reconstructs the seal
and boundary controls, probes every route's source semantics, and exercises fail-closed mutations.

- run 1: 118/118 checks, 20/20 mutations rejected;
- run 2: 118/118 checks, 20/20 mutations rejected;
- results and raw records byte-identical across the reruns;
- source or premise conflicts: zero;
- unauthorized solve/certificate: rejected;
- universal-no-go promotion: rejected.

Cold artifact SHA-256:

```text
1ad975fb0903a8ed413a45638401e7fc2ccfe51c0b75f0e0448d3b76c82a6935  COLD_VERIFIER_CHECK.py
aa6333d797c6e0cb497cff9ef7bd8ad45ed6e82dd2b3e57eca0d9794ff1aaa84  COLD_VERIFIER_RESULT.json
67627eb069762efc49db797719fb8e33dfdbef330a43694ba3080887447b06dc  COLD_VERIFIER_RAW.jsonl
801bbf0cf2acadabde8209fceb5586cb1200d085baa2c98a6bceb89036bfeb09  COLD_VERIFIER_REPORT.md
```

The cold verifier records one nonblocking tooling caveat: the primary mutations are structural.
The independent cold mutations close the missing semantic promotion classes.

## Repository gates

- six hard-frozen manifests: pass;
- frozen package paths: 133;
- current premise controller: 18 premise guards, 9 startup controls, 754 candidate dispositions;
- tests: 70 passed, 1 known xfailed;
- primary `grok` checkout: clean and untouched.

## Four gates

1. preregistered: yes;
2. full or bounded: complete for the exact 586-path registered universe, not future laws;
3. independent: yes, by the fresh cold implementation;
4. premise-audited: yes, all 20 rows and all conditional/open scopes retained.
