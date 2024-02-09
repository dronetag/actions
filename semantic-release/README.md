## dronetag/actions/semantic-release

This action runs the semantic-release tool in dry-mode and returns
current or the next available version. Hence the behaviour is influenced
by your `.releaserc` file.

The recommended content of .releaserc is following:
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

If the new version is a pre-release, it will be incremented until it
finds a version that does not exist as a tag in the repository. Hence
pre-release versions will always return a version but on production
branches the action fails if the version already exists as a tag.

If the action is run on a commit that has a tag on it, it will return
this tag together with `outputs.exists='true'`.

If you use "@semantic-release/release-notes-generator" in your .releaserc
then a changelog.md and changelog{version}.md will be available in the
repository to your disposition. Also, the changelog will be returned in
`outputs.changelog` and saved as an artifact under name `changelog{version}`.


**inputs:**
- `github_token`: required only if project's .releaserc uses github plugin

**outputs:**
- `version`: the next version in format `X.Y.Z[-pre-release.N]`
- `changelog`: the changelog in markdown format
- `prerelease`: true if the next version is a pre-release
- `exists`: true if the version already exists as a tag on current commit