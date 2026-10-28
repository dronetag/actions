"""Upload dist/* with twine and verify each file on the index.

After each upload attempt, the file is downloaded again from the simple index.
A file passes only when the index serves exactly the built file (same
SHA-256). So a failed upload passes only when the identical file is already
on the index ("already exists" - indexes report it as 400 or 409). Every other
result fails the job: an upload error with no file, or a file with other
content (for example a partial upload after an HTTP 500, which the index keeps
and then reports as "already exists").

Environment: PYPI_REPOSITORY (the ~/.pypirc section for twine), PYPI_SIMPLE_URL
(the simple index, e.g. https://pypi.example.com/simple/), PYPI_USER, PYPI_PASS.
"""

import base64
import hashlib
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def project_of(filename: str) -> str:
    """PEP 503 name of a wheel or sdist file."""
    stem = filename.removesuffix(".whl").removesuffix(".tar.gz").removesuffix(".zip")
    name = stem.split("-")[0]
    return re.sub(r"[-_.]+", "-", name).lower()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url)
    user, password = os.environ.get("PYPI_USER", ""), os.environ.get("PYPI_PASS", "")
    if user:
        token = base64.b64encode(f"{user}:{password}".encode()).decode()
        request.add_header("Authorization", f"Basic {token}")
    with urllib.request.urlopen(request, timeout=300) as response:
        return response.read()


def index_file(simple_url: str, filename: str) -> bytes | None:
    """The file as the index serves it, or None when the index does not list it."""
    page_url = urllib.parse.urljoin(simple_url, project_of(filename) + "/")
    try:
        page = fetch(page_url).decode()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    for href, text in re.findall(r'href="([^"]+)"[^>]*>([^<]+)<', page):
        if text.strip() == filename:
            return fetch(urllib.parse.urljoin(page_url, href.split("#")[0]))
    return None


def main() -> int:
    repository = os.environ["PYPI_REPOSITORY"]
    simple_url = os.environ["PYPI_SIMPLE_URL"].rstrip("/") + "/"
    files = sorted(p for p in Path("dist").iterdir() if p.is_file())
    if not files:
        print("::error::dist/ is empty - nothing to upload")
        return 1
    failed = []
    for path in files:
        built = path.read_bytes()
        result = subprocess.run(
            ["python3", "-m", "twine", "upload", "--repository", repository,
             "--disable-progress-bar", str(path)],
            capture_output=True, text=True,
        )
        print((result.stdout + result.stderr).strip())
        uploaded = result.returncode == 0
        # The index can need a moment before it lists a new file
        served = None
        for _ in range(6 if uploaded else 1):
            served = index_file(simple_url, path.name)
            if served is not None:
                break
            time.sleep(5)
        if served is None:
            reason = "is not on the index after the upload" if uploaded else (
                f"upload failed (twine exit {result.returncode}) and the index does not have it")
            print(f"::error file={path}::{path.name} {reason}")
            failed.append(path.name)
        elif sha256(served) != sha256(built):
            print(f"::error file={path}::{path.name} on the index is {len(served)} B sha256 "
                  f"{sha256(served)[:16]}, the build is {len(built)} B sha256 {sha256(built)[:16]}"
                  " - the index holds a different or partial file; remove it and upload again")
            failed.append(path.name)
        else:
            state = "uploaded" if uploaded else "already on the index (upload refused)"
            print(f"{path.name}: {state}, verified ({len(built)} B, sha256 {sha256(built)[:16]})")
    if failed:
        print(f"::error::{len(failed)} of {len(files)} files are not correct on the index: {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
