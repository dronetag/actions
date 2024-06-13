# dronetag/actions/release

Commit (optional) and tag the current commit. Optionally, create a github release.

## Usage

```yaml
    # Changelog was constructed in some of previous steps
    # most likely dronetag/action/semantic-release was run
    # with: changelog: true (which is the default so far)
    - name: Release
      if: steps.semantic.outputs.existed == 'false' && steps.semantic.outputs.release == 'true'
      uses: dronetag/actions/release@main
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}
        version: ${{ steps.semantic.outputs.version }} # expected semver format X.Y.Z[-xxx.N]
        changelog: ${{ steps.semantic.outputs.changelog }}
        commit-changelog: false
        tag-only: ${{ steps.semantic.outputs.prerelease }}  # do not create github releases for development releases (optional, default 'false')
        # git-add: place filenames (such as updated version files) here to be included  (optional) release commit
```

## Output

No outputs
