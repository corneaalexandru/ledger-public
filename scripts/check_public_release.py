#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PREFIXES = (
    "local_ledger_data/",
    "mock_google_sheet/",
    ".ledger_public_setup/",
    "local_ledger_backups/",
    "google_ledger_backups/",
)
RUNTIME_FILES = {
    "local_ledger_workbook.xlsx",
    "mock_ledger_google_sheet.xlsx",
}
FORBIDDEN_TRACKED_SUFFIXES = (".env", ".json", ".csv", ".xlsx")
FORBIDDEN_TRACKED_PREFIXES = ("credentials/", "local_ledger_backups/", "google_ledger_backups/")
ALLOWED_TRACKED_FILES = {
    ".env.example",
    "credentials/.gitkeep",
    "starter/ledger_starter_workbook.xlsx",
}


def main() -> int:
    run([sys.executable, "-m", "py_compile", "server.py"])
    run([sys.executable, "-m", "py_compile", "scripts/setup_google.py"])
    verify_starter_workbook()
    reject_tracked_runtime_data()
    verify_clean_first_run_requires_google_setup()
    print("Ledger Public release check passed.")
    return 0


def run(command: list[str], cwd: Path = ROOT) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def reject_tracked_runtime_data() -> None:
    result = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE)
    tracked = result.stdout.splitlines()
    bad = [
        path
        for path in tracked
        if path in RUNTIME_FILES or any(path.startswith(prefix) for prefix in RUNTIME_PREFIXES)
    ]
    bad.extend(
        path
        for path in tracked
        if (
            path.endswith(FORBIDDEN_TRACKED_SUFFIXES)
            or any(path.startswith(prefix) for prefix in FORBIDDEN_TRACKED_PREFIXES)
        )
        and path not in ALLOWED_TRACKED_FILES
    )
    if bad:
        raise SystemExit("Runtime data is tracked:\n" + "\n".join(bad))


def verify_starter_workbook() -> None:
    workbook = ROOT / "starter" / "ledger_starter_workbook.xlsx"
    if not workbook.exists():
        raise SystemExit("Missing starter/ledger_starter_workbook.xlsx")
    if workbook.stat().st_size < 1000:
        raise SystemExit("Starter workbook looks too small.")


def verify_clean_first_run_requires_google_setup() -> None:
    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        for path in ROOT.iterdir():
            if path.name in {".git", "local_ledger_data", "mock_google_sheet", ".ledger_public_setup"} or path.name in RUNTIME_FILES:
                continue
            destination = tmp / path.name
            if path.is_dir():
                shutil.copytree(path, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(path, destination)
        result = subprocess.run(
            [sys.executable, "server.py", "--init-only"],
            cwd=tmp,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode == 0:
            raise SystemExit("Default first run should require Google setup, but it succeeded.")
        if "Google mode needs LEDGER_SPREADSHEET_ID" not in result.stdout:
            raise SystemExit("Default first run did not explain missing Google setup:\n" + result.stdout)
        for forbidden in ("local_ledger_data", "local_ledger_workbook.xlsx"):
            if (tmp / forbidden).exists():
                raise SystemExit(f"Default first run created legacy local data: {forbidden}")


if __name__ == "__main__":
    raise SystemExit(main())
