# Security Notes

This repository is designed to be safe for public sharing.

## Included

- Static UI files.
- Local Python server.
- Public-safe Google Sheets adapter code.
- Starter seed data with mock rows only.
- `.env.example` with placeholder values only.
- One-time setup wizard.

## Not Included

- `.env` files.
- Google service-account JSON files.
- Real Google Sheet IDs.
- OAuth tokens.
- Real statement imports.
- Real bank exports.
- Private ledger data.

## Ignored User Files

These stay local and must not be committed:

```text
.env
.ledger_public_setup/
credentials/*.json
google_ledger_backups/
local_ledger_backups/
```

Legacy local runtime folders are also ignored so older installs cannot accidentally commit personal rows.

## Before Publishing Changes

Run:

```bash
python3 scripts/check_public_release.py
```

Do not commit anything private. Keep personal data in the user's Google Sheet and credentials in ignored local files.
