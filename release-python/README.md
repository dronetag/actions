# dronetag/actions/release-python

Release python packages built in (standard) `dist/` directory.

**inputs:**
- `version:` version in format `X.Y[.Z][-xxxx.N]`. It will be updated in
             pyproject.toml in case it wasn't already.
