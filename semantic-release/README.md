## dronetag/actions/semantic-release

This action runs the semantic-release tool in dry-mode and returns current or the next
available version. Hence the behavior is influenced by your `.releaserc` file.

```yaml
    # semantic-release requires that the repository was cloned with
    - name: Checkout repository (full-depth)
      uses: actions/checkout@v4
      with: { fetch-depth: 0 } # Required to determine version

    - name: Get next release version
      uses: dronetag/actions/semantic-release@main
      id: semantic
      with:
        # github-token:: ${{secrets.GITHUB_TOKEN}} # only if .releaserc contains github plugin
```
## Outputs

- `version`: Next version in format X.Y.Z[-<prerelease-branch-name>.N]
- `existed`: Existed will be true if the tag already existed
- `release`: True if current version is a release version
- `prerelease`: True if current version is a pre-release
- `changelog`: Changelog in markdown format


## Configuration (.releaserc)

The recommended content of `.releaserc` is following:
```json
{
	"branches": [
		{ "name": "main" },
		{ "name": "[a-z]+/([a-zA-Z0-9\\-]+)", "prerelease": "${name.replace(/^.*\\//g, '')}"}
	],
	"plugins": [
		[
			"@semantic-release/commit-analyzer",
			{
				"releaseRules": [
					{ "type": "refactor", "release": "patch"},
					{ "type": "perf", "release": "patch" }
				]
			}
		],
		"@semantic-release/release-notes-generator"
	]
}
```

It has `main` branch as the production and all `[fix/feature/...]/<description>`
branches will be pre-release branches.

You will get current version if you run this action on a commit that
has a tag on it. It also sets `outputs.existed='true'`.

If the new version is a pre-release, it will be incremented until it
finds a version that does not exist as a tag in the repository. Hence
pre-release versions will always return a version but on production
branches the action fails if the version already exists as a tag.

If you have _"@semantic-release/release-notes-generator"_ in your .releaserc
and allow changelog generator via `inputs.changelog=true` then a changelog.md
and changelog{version}.md will be available in the repository to your disposition.
The changelog will also be uploaded as an artifact under name `changelog{version}`.
Nevertheless, the changelog will be returned in `outputs.changelog` whether you
specify `inputs.changelog=true` or not.

