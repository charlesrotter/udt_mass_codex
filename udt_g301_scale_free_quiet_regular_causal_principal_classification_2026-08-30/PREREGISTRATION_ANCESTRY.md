# G301 preregistration ancestry

Recorded: 2026-08-30, immediately before the result commit.

- Result-parent `HEAD`: `d964e00438013dc1aac544eb0131e83f05d46859`
- Scientific preregistration: `accfc6b9`
- Repair preregistration: `d964e004`
- `git merge-base --is-ancestor accfc6b9 HEAD`: exit 0
- `git merge-base --is-ancestor d964e004 HEAD`: exit 0

Therefore both the scientific scope and repairs R1--R5 were committed ancestors before the result
tree was banked.
