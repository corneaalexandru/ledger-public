# Troubleshooting

## Python Is Missing

Install Python from:

```text
https://www.python.org/downloads/
```

Then reopen Terminal and try again.

## Google Packages Are Missing

Run:

```bash
python3 -m pip install -r requirements-google.txt
```

The macOS launcher also does this automatically when needed.

## Google Setup Runs Every Time

Setup is skipped when `.env` contains a valid Google Sheet ID and the credentials file exists.

Check:

```text
.env
credentials/ledger-service-account.json
```

## Google Access Fails

Make sure:

- The Google Sheets API is enabled in the Google Cloud project.
- The JSON file is a service-account key.
- The Google Sheet is shared with the JSON file's `client_email`.
- The service account has Editor access.

Then rerun:

```bash
python3 scripts/setup_google.py --force
```

## Port 8765 Is Busy

Run on another port:

```bash
LEDGER_PORT=8770 ./start_ledger_public.command
```

## macOS Blocks The Launcher

Right-click `start_ledger_public.command`, choose `Open`, then confirm.

## Browser Does Not Open

Open this manually:

```text
http://127.0.0.1:8765
```

If you used a different port, replace `8765`.

## Print To PDF Looks Wrong

In the browser print dialog:

- Use A4.
- Disable browser headers and footers when possible.
- Use the app's print icon from the page you want to export.
