# G303 external-review runtime repair

Date: 2026-08-30

The first external-review launch is invalid and its output is discarded. The isolated image lacked
the declared SymPy dependency. While trying to satisfy the replay request, the reviewer accessed
PyPI, contrary to the sealed no-internet scope. The sealed intake was read-only and was not
modified, but no conclusion from that session may certify G303.

The repair is packaging-only:

1. freeze the G303 scientific evidence and landing;
2. add the already-used local SymPy and mpmath versions to a sealed review-only archive;
3. point `PYTHONPATH` only at an ephemeral extraction of that archive;
4. run the replacement reviewer with `approval=never` and sealed execution rules that allow the
   four registered replays while forbidding downloads and package installation;
5. require a new manifest, seal, and explicit user authorization.

No equation, factor, test tolerance, premise, or conclusion changes in this repair.
