# dronetag/actions/release

Commit (optional) and tag the current commit. After that - create a github release.

## Usage

```yaml
    # Changelog was constructed in some of previous steps
    # most likely dronetag/action/semantic-release was run
    # with: changelog: true (which is the default so far)
    - name: Release
      if: ${{ steps.semantic.outputs.existed == 'false' && steps.semantic.outputs.release == 'true' }}
      uses: dronetag/actions/release@main
      with:
        github-token: ${{ github.token }}
        version: ${{ steps.semantic.outputs.version }} # expected semver format X.Y.Z[-xxx.N]
        changelog: ${{ steps.semantic.outputs.changelog }}
        commit-changelog: false
        # git-add: place filenames (such as updated version files) here to be included in (optional) release commit
```

## Output

No outputs