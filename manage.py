#!/usr/bin/env python3
"""Manage and launch the Effective Executive server stack.

This helper bootstraps a virtualenv, installs dependencies into it, and
runs commands against the project. It deliberately uses only the Python
standard library so it can be invoked on a fresh checkout.

Usage:
    python3 manage.py setup           # create .venv and install requirements
    python3 manage.py run             # start the server (default: 8000)
    python3 manage.py run --port 9000 # start on a different port
    python3 manage.py dev             # run with --reload for development
    python3 manage.py db upgrade      # run Alembic migrations
    python3 manage.py db revision -m "msg"   # autogenerate a revision
    python3 manage.py shell           # open a Python REPL with the venv
    python3 manage.py import-sqlite path/to/effective_executive.db user@x
    python3 manage.py compose up      # start docker-compose Postgres
    python3 manage.py compose down    # stop docker-compose Postgres
    python3 manage.py clean           # remove .venv

Environment:
    DATABASE_URL   defaults to sqlite:///./effective_executive.db
    PORT           defaults to 8000
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
REQUIREMENTS = ROOT / "requirements.txt"


def _venv_bin(name: str) -> Path:
    return VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / name


def _python() -> Path:
    return _venv_bin("python.exe" if os.name == "nt" else "python")


def _pip() -> Path:
    return _venv_bin("pip.exe" if os.name == "nt" else "pip")


def ensure_venv() -> None:
    if _python().exists():
        return
    print(f"→ Creating venv at {VENV_DIR}", flush=True)
    venv.EnvBuilder(with_pip=True, clear=False, upgrade_deps=False).create(VENV_DIR)


def ensure_deps(force: bool = False) -> None:
    ensure_venv()
    stamp = VENV_DIR / ".requirements.sha"
    current = REQUIREMENTS.read_bytes()
    import hashlib
    sha = hashlib.sha256(current).hexdigest()
    if not force and stamp.exists() and stamp.read_text().strip() == sha:
        return
    print("→ Installing requirements", flush=True)
    subprocess.check_call([str(_pip()), "install", "--upgrade", "pip"])
    subprocess.check_call([str(_pip()), "install", "-r", str(REQUIREMENTS)])
    stamp.write_text(sha)


def _exec(args: list[str], extra_env: dict[str, str] | None = None) -> int:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    return subprocess.call(args, env=env, cwd=str(ROOT))


def cmd_setup(_a) -> int:
    ensure_deps(force=True)
    print("✓ Setup complete. Run: python3 manage.py run")
    return 0


def cmd_run(a) -> int:
    ensure_deps()
    port = str(a.port)
    args = [str(_python()), "-m", "uvicorn", "main:app",
            "--host", a.host, "--port", port]
    if a.reload:
        args.append("--reload")
    print(f"→ Starting server on http://{a.host}:{port}", flush=True)
    return _exec(args, {"PORT": port})


def cmd_dev(a) -> int:
    a.reload = True
    return cmd_run(a)


def cmd_db(a) -> int:
    ensure_deps()
    args = [str(_python()), "-m", "alembic", *a.alembic_args]
    return _exec(args)


def cmd_shell(_a) -> int:
    ensure_deps()
    return _exec([str(_python())])


def cmd_import_sqlite(a) -> int:
    ensure_deps()
    return _exec([str(_python()), "scripts/import_sqlite.py", a.path, a.email])


def cmd_compose(a) -> int:
    if not shutil.which("docker"):
        print("docker not found on PATH", file=sys.stderr)
        return 1
    return _exec(["docker", "compose", *a.compose_args])


def cmd_clean(_a) -> int:
    if VENV_DIR.exists():
        print(f"→ Removing {VENV_DIR}")
        shutil.rmtree(VENV_DIR)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="manage.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("setup", help="Create venv and install requirements").set_defaults(func=cmd_setup)

    pr = sub.add_parser("run", help="Run the server")
    pr.add_argument("--host", default="0.0.0.0")
    pr.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    pr.add_argument("--reload", action="store_true")
    pr.set_defaults(func=cmd_run)

    pd = sub.add_parser("dev", help="Run the server with auto-reload")
    pd.add_argument("--host", default="127.0.0.1")
    pd.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    pd.set_defaults(func=cmd_dev)

    pdb = sub.add_parser("db", help="Run alembic in the venv")
    pdb.add_argument("alembic_args", nargs=argparse.REMAINDER)
    pdb.set_defaults(func=cmd_db)

    sub.add_parser("shell", help="Python REPL inside the venv").set_defaults(func=cmd_shell)

    pi = sub.add_parser("import-sqlite", help="Import a legacy SQLite DB into a user")
    pi.add_argument("path")
    pi.add_argument("email")
    pi.set_defaults(func=cmd_import_sqlite)

    pc = sub.add_parser("compose", help="Pass-through to docker compose")
    pc.add_argument("compose_args", nargs=argparse.REMAINDER)
    pc.set_defaults(func=cmd_compose)

    sub.add_parser("clean", help="Remove the .venv").set_defaults(func=cmd_clean)
    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
    except KeyboardInterrupt:
        sys.exit(130)
