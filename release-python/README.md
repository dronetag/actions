# dronetag/actions/release-python

Release python packages built in (standard) `dist/` directory.

**inputs:**
- `version:` version in format `X.Y[.Z][-xxxx.N]`. It will be updated in
             pyproject.toml in case it wasn't already.


**Upload check:** the action uploads each file in `dist/` with twine, then
downloads it again from the simple index and compares the SHA-256 with the
built file. The job fails unless the index serves exactly the built file.

- A refused upload ("already exists", HTTP 400 or 409) passes only when the
  index already has the identical file. A rerun of a release job is safe.
- A partial or empty file on the index fails the job, with both sizes and
  hashes in the error. Example: an index with a full disk answers HTTP 500,
  keeps a truncated file, and then answers "already exists" to the retry.
- The simple index is `https://<pypi-host>/simple/`, or `https://pypi.org/simple/`
  for PyPI. Set `pypi-simple-url` when the index uses another path.

## Usage

```yaml
    # Release should happen once build is done and commit tagged.
    # There is an option to have this in a separate workflow bound
    # not to the tag event (because tags created by actions don't
    # trigger) but to have this workflow as the trigger by:
    # on: {workflow_run: {workflows: ["Release"], types: completed}, workflow_dispatch: {}}
    - name: Release
      uses: dronetag/actions/release-python@main
      with:
        pypi-name: dronetag
        pypi-host: ${{ secrets.PRIV_PIP_HOST }}
        pypi-user: ${{ secrets.PRIV_PIP_USER }}
        pypi-pass: ${{ secrets.PRIV_PIP_PASSWORD }}
```
