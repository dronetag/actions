# dronetag/actions/release-python

Action that releases to private or public PYPI using the most
standard tool `setuptools`.


**inputs:**
- `version:` version in format `X.Y[.Z][-xxxx.N]`. It will be updated in
             pyproject.toml in case it wasn't already.
- `pypi_pass`: Password for the PyPI repository
- `github_token`: GitHub token
- `pypi_name`: Name of PyPI repository
- `pypi_host`: Host of PyPI repository
- `pypi_user`: Username for PyPI repository