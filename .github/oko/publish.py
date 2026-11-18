"""Publish an already-verified compiled EXE; no application source is stored here."""
from pathlib import Path
import hashlib, shutil, tempfile
import bsdiff4, py7zr

ROOT=Path.cwd()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify(path,digest):
    if sha(path)!=digest:raise RuntimeError('Checksum mismatch: '+str(path))
old_exe=ROOT/'downloads/OKO-1.8.2-preview.exe'
old_archive=ROOT/'downloads/OKO-1.8.2-Vosk-offline.7z'
verify(old_exe,'0a43174599ba933c6e426a96a69368cce5354ec16244f2dd5bf320ce19a67dba')
verify(old_archive,'6ee1adc3405f875480091597b33576f84cdc60bdd1dc6548312849ffb895c561')
new_exe=ROOT/'downloads/OKO-1.8.3-preview.exe'
new_exe.write_bytes(bsdiff4.patch(old_exe.read_bytes(),b''.join(p.read_bytes() for p in sorted((ROOT/'.github/oko/1.8.3').glob('part-*.bsdiff')))))
verify(new_exe,'384308df21e2e5fbe07e465a9948d1ce3db9a9cb0192f48b7a4a3f15c0e3bdd9')
with tempfile.TemporaryDirectory(prefix='oko-release-') as scratch:
    folder=Path(scratch)
    with py7zr.SevenZipFile(old_archive) as archive:archive.extractall(folder)
    source=folder/'OKO-1.8.2-Vosk'
    for line in (source/'SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split('  ',1);verify(source/name,digest)
    target=folder/'OKO-1.8.3-Vosk';source.rename(target)
    shutil.copy2(new_exe,target/'OKO.exe')
    readme=target/'ПРОЧИТАЙ.txt';text=readme.read_text(encoding='utf-8-sig').replace('1.8.2','1.8.3')
    text+='\nСценарий: Олл-ин или дуэль вынесены в отдельный раскрывающийся блок; порядок прохода находится в Проходе по игрокам.\n'
    readme.write_text(text,encoding='utf-8-sig')
    manifest=target/'SHA256SUMS.txt'
    manifest.write_text(''.join(sha(p)+'  '+p.relative_to(target).as_posix()+'\n' for p in sorted(target.rglob('*')) if p.is_file() and p!=manifest))
    if list(target.rglob('oko-settings.json')) or list(target.rglob('settings.json')):raise RuntimeError('Private settings in package')
    new_archive=ROOT/'downloads/OKO-1.8.3-Vosk-offline.7z'
    with py7zr.SevenZipFile(new_archive,'w',filters=[{'id':py7zr.FILTER_LZMA2,'preset':7}]) as archive:archive.writeall(target,arcname=target.name)
    if new_archive.stat().st_size>=100*1024*1024:raise RuntimeError('Archive exceeds repository file limit')
    print('Verified EXE:',sha(new_exe))
    print('Offline archive:',new_archive.stat().st_size,sha(new_archive))
checksums=ROOT/'downloads/SHA256SUMS.txt'
text='\n'.join(line for line in checksums.read_text().splitlines() if 'OKO-1.8.3-' not in line)+'\n'
for path in [new_exe,new_archive]:text+=sha(path)+'  '+path.name+'\n'
checksums.write_text(text)
for path in (ROOT/'.github/oko/staged').rglob('*'):
    if path.is_file():
        destination=ROOT/path.relative_to(ROOT/'.github/oko/staged');destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
print('Ready to commit verified binaries and documentation.')
