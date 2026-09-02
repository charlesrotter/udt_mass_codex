# G326 sealed replay precondition

The sealed intake is deliberately read-only. Before running `REPLAY_COMMANDS.txt`, make a writable
ephemeral copy without changing the intake:

```bash
mkdir -p /work/g326_review_writable
cp -r /intake/. /work/g326_review_writable/
chmod -R u+w /work/g326_review_writable
cd /work/g326_review_writable
```

Then run the four lines in `REPLAY_COMMANDS.txt` literally. Generated files go only under
`.review_runtime/` in the writable copy. The sealed intake itself remains read-only throughout.

This is an execution precondition, not a scientific premise and not permission to edit evidence.
