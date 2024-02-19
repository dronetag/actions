# dronetag/actions/commit-and-tag

Commit (optional) and tag the current commit. This action has a few self-regulations.

- it creates a commit only if current HEAD is the tip of the default branch
- it commits only if there are changes present in the repository
- it creates a tag only if the tag does not exist yet (not a failure)

**inputs:**
- `version` version in format `X.Y[.Z][-xxxx.N]` that will be used as the tag vVERSION and in commit message
- `git-add` files separated with space that will be added to the commit
- `commit` whether a commit will be created before tagging (only if on the tip of the default branch)
