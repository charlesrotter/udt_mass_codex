# G252 external review

Date: 2026-08-24

Fresh external Codex `gpt-5.4` returned `ACCEPT_WITH_REPAIRS`.

The reviewer found no load-bearing scientific defect and retained the bounded conditional theorem.
It found one evidence-packaging defect: the three source verification paths worked in the
repository but did not accept the sealed `sources/` relocation. Consequently the two scientific
replays and package verifier failed inside the original sealed intake, although all 28 payload
hashes matched and the hostile replay passed.

Until the preregistered repair is implemented and externally accepted, gates 3 and 4 are failed as
delivered. The scientific landing remains retained but not fully certified.
