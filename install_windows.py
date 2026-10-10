"""Isolated local SearXNG setup based on our existing Windows source and patch."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import os
import secrets
import subprocess
import sys
import tarfile
import urllib.request

COMMIT = '3fdc6d753a339b5f4a7dc5842c94c0d8324726f1'
URL = 'https://codeload.github.com/searxng/searxng/tar.gz/' + COMMIT

def write_launchers(root):
    launcher='$ErrorActionPreference="Stop"\n$env:SEARXNG_SETTINGS_PATH=Join-Path $PSScriptRoot "settings.yml"\nSet-Location (Join-Path $PSScriptRoot "source")\n& (Join-Path $PSScriptRoot ".venv\\Scripts\\python.exe") -m searx.webapp\n'
    (root/'START-SEARXNG.ps1').write_text(launcher,encoding='utf-8')
    python_launcher='from pathlib import Path\nimport os\nimport subprocess\n\nroot = Path(__file__).resolve().parent\nos.environ["SEARXNG_SETTINGS_PATH"] = str(root / "settings.yml")\nos.environ["PYTHONUTF8"] = "1"\nraise SystemExit(subprocess.call([str(root / ".venv/Scripts/python.exe"), "-m", "searx.webapp"], cwd=root / "source"))\n'
    (root/'START-SEARXNG.py').write_text(python_launcher,encoding='utf-8')

def run(args, cwd, log):
    print('RUN', ' '.join(map(str,args)), flush=True)
    result=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    with log.open('a',encoding='utf-8') as stream:
        stream.write('\n$ '+' '.join(map(str,args))+'\n'+result.stdout+'\n')
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}); inspect {log}')

def install(root, port):
    root=root.resolve()
    if root.exists():
        raise FileExistsError('Use a NEW target directory; existing installations are preserved')
    if sys.platform!='win32' or sys.version_info[:2] != (3,11):
        raise ValueError('This documented source uses Windows Python 3.11; select that interpreter explicitly')
    if not 1024 <= port <= 65535:
        raise ValueError('Choose a valid unprivileged loopback port')
    root.mkdir(parents=True)
    log=root/'INSTALLATION.log'
    print('DOWNLOAD',URL,flush=True)
    body=urllib.request.urlopen(URL,timeout=90).read()
    (root/'searxng-source.tar.gz').write_bytes(body)
    source=root/'source'
    source.mkdir()
    skipped_linux_templates=[]
    with tarfile.open(fileobj=io.BytesIO(body),mode='r:gz') as archive:
        members=archive.getmembers()
        prefix=members[0].name.split('/')[0]+'/'
        for member in members:
            if member.isdir() or member.name.rstrip('/')==prefix.rstrip('/'):
                continue
            if member.issym() and member.name.startswith(prefix+'utils/templates/'):
                skipped_linux_templates.append({'path':member.name[len(prefix):],'target':member.linkname})
                continue
            if not member.isfile() or not member.name.startswith(prefix):
                raise ValueError('Unexpected archive member: '+member.name)
            target=source/member.name[len(prefix):]
            if not target.resolve().is_relative_to(source.resolve()):
                raise ValueError('Archive member leaves target')
            target.parent.mkdir(parents=True,exist_ok=True)
            with archive.extractfile(member) as stream:
                target.write_bytes(stream.read())
    patchfile=source/'searx'/'valkeydb.py'
    original=patchfile.read_text('utf-8')
    if original.count('import pwd\n') != 1:
        raise ValueError('Unexpected source version; portability patch not applied')
    patched=original.replace('import pwd\n','try:\n    import pwd\nexcept ImportError:\n    pwd = None\n',1)
    old='        _pw = pwd.getpwuid(os.getuid())\n        logger.exception("[%s (%s)] can\'t connect valkey DB ...", _pw.pw_name, _pw.pw_uid)'
    new='        if pwd is not None and hasattr(os, "getuid"):\n            _pw = pwd.getpwuid(os.getuid())\n            logger.exception("[%s (%s)] can\'t connect valkey DB ...", _pw.pw_name, _pw.pw_uid)\n        else:\n            logger.exception("can\'t connect valkey DB ...")'
    if old not in patched:
        raise ValueError('Unexpected error handler; portability patch not applied')
    patched=patched.replace(old,new,1)
    patchfile.write_text(patched,encoding='utf-8')
    webutils=source/'searx'/'webutils.py'
    original_webutils=webutils.read_text('utf-8')
    if original_webutils.count('result_templates.add(f)') != 1:
        raise ValueError('Unexpected template enumeration; no Windows path patch')
    patched_webutils=original_webutils.replace('result_templates.add(f)','result_templates.add(f.replace(os.sep, "/"))',1)
    static_old='file_list.append(str(f.relative_to(static_path)))'
    if patched_webutils.count(static_old)!=1:
        raise ValueError('Unexpected static asset enumeration; no Windows path patch')
    patched_webutils=patched_webutils.replace(static_old,'file_list.append(f.relative_to(static_path).as_posix())',1)
    webutils.write_text(patched_webutils,encoding='utf-8')
    run([sys.executable,'-m','venv',str(root/'.venv')],root,log)
    python=root/'.venv'/'Scripts'/'python.exe'
    run([str(python),'-m','pip','install','-r',str(source/'requirements.txt'),'tzdata','setuptools','wheel'],root,log)
    run([str(python),'-m','pip','install','--no-deps','--no-build-isolation','-e',str(source)],root,log)
    settings=(f'use_default_settings: true\ngeneral:\n  debug: false\n  instance_name: "SearXNG Lernprojekt"\n'
              f'search:\n  formats: [html, json]\nserver:\n  port: {port}\n  bind_address: "127.0.0.1"\n'
              f'  secret_key: "{secrets.token_hex(32)}"\n  limiter: false\n  image_proxy: true\n'
              'valkey:\n  url: false\noutgoing:\n  request_timeout: 6.0\n  max_request_timeout: 12.0\n')
    (root/'settings.yml').write_text(settings,encoding='utf-8')
    # No production secret or user path is distributed or printed.
    example=settings.split('  secret_key:')[0]+'  secret_key: "DEIN-NEU-ERZEUGTER-SCHLUESSEL"\n'+settings.split('  secret_key:')[1].split('\n',1)[1]
    (root/'settings-ANSICHT.yml').write_text(example,encoding='utf-8')
    write_launchers(root)
    manifest={'upstream_commit':COMMIT,'upstream_url':URL,'source_archive_sha256':hashlib.sha256(body).hexdigest(),
              'python_version':sys.version,'loopback_port':port,'existing_installations_modified':False,
              'service_started':False,'omitted_linux_service_template_links':skipped_linux_templates,
              'windows_patch':{'file':'searx/valkeydb.py','before_sha256':hashlib.sha256(original.encode()).hexdigest(),
              'after_sha256':hashlib.sha256(patchfile.read_bytes()).hexdigest()},
              'windows_template_and_static_patch':{'file':'searx/webutils.py','before_sha256':hashlib.sha256(original_webutils.encode()).hexdigest(),
              'after_sha256':hashlib.sha256(webutils.read_bytes()).hexdigest()},'installation_commands_passed':True,
              'patch_hash_basis':'actual persisted bytes, including Windows line endings'}
    (root/'INSTALLATION.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('INSTALLED; service not started',root,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--target',type=Path,required=True)
    parser.add_argument('--port',type=int,default=8080)
    args=parser.parse_args()
    install(args.target,args.port)
