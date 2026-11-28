"""Package the tested OKO executable with the verified Windows Vosk dependencies."""
from pathlib import Path
import hashlib
import re
import tempfile
import zipfile

import bsdiff4
import py7zr

STAGING = Path(__file__).resolve().parent
OUTPUT = Path("release-1.8.11")
BASE_EXE = Path("release-base/OKO-1.8.10-preview-win-x64.exe")
BASE_ARCHIVE = Path("downloads/OKO-1.8.4-Vosk-offline.7z")
EXPECTED_EXE = "7ec7cc47ed1b2cd1c3c373b741d7042b583fcc03dba247d5898dff11284791c8"
ROOT = "OKO-1.8.11-Vosk/"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(path, expected):
    if digest(path) != expected:
        raise ValueError(f"Checksum mismatch for {path.name}")


verify(BASE_EXE, "d164a1a1802e89962986addfdc92344b92a3d407058b83b4775bc7fa8b43f8ac")
verify(BASE_ARCHIVE, "52a44bcc01a2fef86127e821971ec07b94bce692991448599f1aa9a3813ad309")
OUTPUT.mkdir(exist_ok=True)
exe = OUTPUT / "OKO-1.8.11-preview-win-x64.exe"
delta = b"".join(piece.read_bytes() for piece in sorted((STAGING / "chunks").glob("*.bsdiff")))
exe.write_bytes(bsdiff4.patch(BASE_EXE.read_bytes(), delta))
verify(exe, EXPECTED_EXE)
bundle = OUTPUT / "OKO-1.8.11-Vosk-offline.zip"
manual = (STAGING / "ПРОЧИТАЙ.txt").read_bytes()
contents = {"OKO.exe": EXPECTED_EXE, "ПРОЧИТАЙ.txt": hashlib.sha256(manual).hexdigest()}
with tempfile.TemporaryDirectory(prefix="oko-1811-release-") as scratch:
    with py7zr.SevenZipFile(BASE_ARCHIVE) as source:
        source.extractall(scratch)
    base = Path(scratch) / "OKO-1.8.4-Vosk"
    for line in (base / "SHA256SUMS.txt").read_text().splitlines():
        expected, name = line.split("  ", 1)
        verify(base / name, expected)
        if name.startswith(("speech-assets/", "LICENSES/")) or name == "THIRD-PARTY.txt":
            contents[name] = expected
    assert len(contents) == 25
    assert any(name.endswith("libvosk.dll") for name in contents)
    assert any(name.endswith("model.conf") for name in contents)
    assert not re.search(rb"pvk_[A-Za-z0-9_-]{20,}", exe.read_bytes() + manual)
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
        for name in sorted(contents):
            if name == "OKO.exe":
                archive.write(exe, ROOT + name, compress_type=zipfile.ZIP_STORED)
            elif name == "ПРОЧИТАЙ.txt":
                archive.writestr(ROOT + name, manual)
            else:
                archive.write(base / name, ROOT + name)
        archive.writestr(ROOT + "SHA256SUMS.txt",
                         "".join(f"{v}  {k}\n" for k, v in sorted(contents.items())))
with zipfile.ZipFile(bundle) as archive:
    assert set(archive.namelist()) == {ROOT + n for n in contents} | {ROOT + "SHA256SUMS.txt"}
    for name, expected in contents.items():
        with archive.open(ROOT + name) as stream:
            assert hashlib.file_digest(stream, "sha256").hexdigest() == expected, name
(OUTPUT / "SHA256SUMS.txt").write_text(f"{digest(bundle)}  {bundle.name}\n{EXPECTED_EXE}  {exe.name}\n")
print(f"Verified {bundle.name}: {len(contents)} files, {bundle.stat().st_size} bytes, SHA-256 {digest(bundle)}")
