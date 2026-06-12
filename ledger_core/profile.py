from __future__ import annotations

import json
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_PROFILE_FILE = ".ledger_profile.json"
PROFILE_FIELDS = ("name", "surname", "email")


class ProfileStore:
    def __init__(self, root: Path, *, file_name: str = DEFAULT_PROFILE_FILE) -> None:
        self.root = Path(root)
        self.path = self.root / file_name

    def read(self) -> dict[str, Any]:
        payload = self._read_payload()
        return public_profile(payload)

    def update(self, values: dict[str, Any]) -> dict[str, Any]:
        current = self._read_payload()
        next_payload = {
            "version": 1,
            **{field: clean_profile_value(values.get(field, current.get(field, ""))) for field in PROFILE_FIELDS},
            "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        }
        self._write_payload(next_payload)
        return public_profile(next_payload)

    def _read_payload(self) -> dict[str, Any]:
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return payload if isinstance(payload, dict) else {}

    def _write_payload(self, payload: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        try:
            self.path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass


def clean_profile_value(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def public_profile(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": True,
        "profile": {
            **{field: clean_profile_value(payload.get(field, "")) for field in PROFILE_FIELDS},
            "updated_at": str(payload.get("updated_at") or ""),
        },
    }
