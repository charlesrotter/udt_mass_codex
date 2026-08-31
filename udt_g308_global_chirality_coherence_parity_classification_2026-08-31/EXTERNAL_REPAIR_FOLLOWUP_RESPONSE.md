G308_REPAIRS_INCOMPLETE

**Findings**
- `Medium`: R3 is not fully carried through the current sealed evidence language. [RUN_RECORD.md](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/RUN_RECORD.md:20) still labels the 79,200-check path as `Independent replay`, and [RUN_RECORD.md](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/RUN_RECORD.md:26) still presents it that way, even though the regrade is correctly stated in [REPAIR_PREREGISTRATION.md](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/REPAIR_PREREGISTRATION.md:37), [REPAIR_REPORT.md](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/REPAIR_REPORT.md:24), [EVIDENCE_GATES.md](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EVIDENCE_GATES.md:8), and [AUDIT_REPORT.md](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/AUDIT_REPORT.md:52). That misses the stricter “described only as a constructive randomized cross-check” condition.
- `Low`: The new Hodge verifier is genuinely distinct and non-importing, but I could not confirm an ownership-boundary check inside that verifier itself. Its distinct method is visible at [verify_chirality_hodge_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py:147), [verify_chirality_hodge_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py:178), [verify_chirality_hodge_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py:197), [verify_chirality_hodge_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py:259), and its result schema at [verify_chirality_hodge_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py:285), but the only boundary-style output there is [verify_chirality_hodge_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py:304). The unchanged ownership boundary is retained elsewhere at [DERIVATION_RESULT.json](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json:34) and [STATUS_LEDGER.tsv](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/STATUS_LEDGER.tsv:12), so this is not a scientific regression.

**Confirmed**
- R1 runtime portability passed. In a fresh writable copy under `/work`, all six registered package replays ran, and `python3 -S verify_package.py` passed directly in the sealed `frozen_sources/` layout with no symlinks or manual staging.
- R1/R4 resolver behavior is correct. [verify_package.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_package.py:30) resolves from exactly one of repository or sealed layouts, and [verify_package.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_package.py:33) rejects missing and ambiguous cases. [verify_repair_portability.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_repair_portability.py:37) through [verify_repair_portability.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_repair_portability.py:53) exercises repository-only, sealed-only, missing, and ambiguous layouts, and the replay passed.
- R2 method distinctness is real. The old randomized verifier still rebuilds the production-style outer-product candidate at [verify_global_chirality_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_global_chirality_independent.py:136) and [verify_global_chirality_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_global_chirality_independent.py:142); the new verifier does not.
- Byte stability held. `cmp` returned `0` for `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, `HODGE_INDEPENDENT_VERIFICATION.json`, `CATCH_PROOF_RESULT.json`, `PORTABILITY_VERIFICATION_RESULT.json`, and `COHERENCE_CENSUS.tsv`.
- No bounded scientific regression was found. The exact landing is unchanged at [DERIVATION_RESULT.json](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json:9) and [VERIFICATION_RESULT.json](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/VERIFICATION_RESULT.json:7); metric/kernel remain unchanged at [DERIVATION_RESULT.json](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json:11) and [STATUS_LEDGER.tsv](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/STATUS_LEDGER.tsv:13); physical-population ownership remains open at [DERIVATION_RESULT.json](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json:34) and [STATUS_LEDGER.tsv](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/STATUS_LEDGER.tsv:12).

**Commands**
```text
pwd  # exit 0
rg --files /intake  # exit 127
find /intake -maxdepth 2 -type d | sort  # exit 0
find /intake -name 'verify_package.py' -o -name '*resolver*.py' -o -name '*hodge*' -o -name '*orbit*' -o -name '*landing*' -o -name '*metric*' | sort  # exit 0
grep -RIn "79,200\|79200\|121,600\|121600\|constructive randomized\|group-orbit\|Hodge\|globality\|chirality\|pair-reversal\|time-carry\|geodesic\|ownership\|physical-population\|reciprocal kernel" /intake 2>/dev/null | head -n 400  # exit 0
find /intake -maxdepth 3 -type f | sort | sed -n '1,260p'  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/REPAIR_PREREGISTRATION.md  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COMMANDS.md  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_package.py | sed -n '1,220p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_repair_portability.py | sed -n '1,260p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py | sed -n '1,360p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_global_chirality_independent.py | sed -n '1,320p'  # exit 0
rm -rf /work/g308_followup && mkdir -p /work/g308_followup && cp -a /intake/. /work/g308_followup/ && printf '%s\n' /work/g308_followup/udt_g308_global_chirality_coherence_parity_classification_2026-08-31  # rejected, not run
mktemp -d /work/g308_followup.XXXXXX  # exit 0
cp -a /intake/. /work/g308_followup.CpaUlw/  # exit 0
python3 -S derive_global_chirality_coherence.py  # exit 0
python3 -S verify_global_chirality_independent.py  # exit 0
python3 -S verify_chirality_hodge_independent.py  # exit 0
python3 -S run_catch_proofs.py  # exit 0
python3 -S verify_repair_portability.py  # exit 0
python3 -S verify_package.py  # exit 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json /work/g308_followup.CpaUlw/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json; printf 'DERIVATION_RESULT.json %s\n' $?  # exit 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/INDEPENDENT_VERIFICATION.json /work/g308_followup.CpaUlw/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/INDEPENDENT_VERIFICATION.json; printf 'INDEPENDENT_VERIFICATION.json %s\n' $?  # exit 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/HODGE_INDEPENDENT_VERIFICATION.json /work/g308_followup.CpaUlw/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/HODGE_INDEPENDENT_VERIFICATION.json; printf 'HODGE_INDEPENDENT_VERIFICATION.json %s\n' $?  # exit 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/CATCH_PROOF_RESULT.json /work/g308_followup.CpaUlw/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/CATCH_PROOF_RESULT.json; printf 'CATCH_PROOF_RESULT.json %s\n' $?  # exit 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/PORTABILITY_VERIFICATION_RESULT.json /work/g308_followup.CpaUlw/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/PORTABILITY_VERIFICATION_RESULT.json; printf 'PORTABILITY_VERIFICATION_RESULT.json %s\n' $?  # exit 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COHERENCE_CENSUS.tsv /work/g308_followup.CpaUlw/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COHERENCE_CENSUS.tsv; printf 'COHERENCE_CENSUS.tsv %s\n' $?  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/REPAIR_REPORT.md  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/AUDIT_REPORT.md  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EXTERNAL_REVIEW_RESPONSE.md  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/STATUS_LEDGER.tsv  # exit 0
grep -RIn "fully independent\|full independence\|constructive randomized\|constructive cross-check\|79,200\|79200\|121,600\|121600\|independent gate" /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31 2>/dev/null | sed -n '1,260p'  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/RUN_RECORD.md  # exit 0
sed -n '1,240p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/VERIFICATION_RESULT.json  # exit 0
sed -n '1,220p' /intake/frozen_current/CURRENT_SCIENTIFIC_PREMISES.md  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EVIDENCE_GATES.md  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/LAY_REPORT.md  # exit 0
grep -RIn "Independent replay\|implementation-distinct numerical verification\|INDEPENDENT_VERIFICATION\|verify_global_chirality_independent" /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31 2>/dev/null | sed -n '1,220p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/RUN_RECORD.md | sed -n '1,140p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EVIDENCE_GATES.md | sed -n '1,120p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/AUDIT_REPORT.md | sed -n '45,80p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/STATUS_LEDGER.tsv | sed -n '1,40p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/REPAIR_REPORT.md | sed -n '1,120p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/REPAIR_PREREGISTRATION.md | sed -n '1,120p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EXACT_DERIVATION.md | sed -n '214,232p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json | sed -n '1,80p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/VERIFICATION_RESULT.json | sed -n '1,40p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/HODGE_INDEPENDENT_VERIFICATION.json | sed -n '1,40p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/INDEPENDENT_VERIFICATION.json | sed -n '1,40p'  # exit 0
grep -n "physical\|ownership\|member_selected\|population\|selected\|kernel" /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_chirality_hodge_independent.py  # exit 0
```

`python3 verify_current_scientific_premises.py` and `python3 -m pytest -q` were not run because [COMMANDS.md](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COMMANDS.md:17) marks them as repository-only gates, not sealed-package replays.
