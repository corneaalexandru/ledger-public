# Install And Run

## macOS

Double-click:

```text
start_ledger_public.command
```

If macOS blocks it:

1. Right-click `start_ledger_public.command`.
2. Choose `Open`.
3. Confirm.

The launcher updates the app, installs missing Google requirements, opens setup once when needed, then starts Ledger.
When setup is missing, it opens the browser setup page at:

```text
http://127.0.0.1:8765/setup
```

## Terminal

```bash
git clone https://github.com/corneaalexandru/ledger-public.git
cd ledger-public
python3 -m pip install -r requirements-google.txt
python3 server.py --setup --open
```

## Google Sheet Database

1. Create a blank Google Sheet in Google Drive.
2. In Google Cloud, create or choose a project.
3. Enable the Google Sheets API for that project.
4. Create a service account and download a JSON key.
5. Upload that key in the web setup page or save it as `credentials/ledger-public-service-account.json`.
6. Share the Google Sheet with the `client_email` from that JSON key as Editor.
7. Paste the Google Sheet URL or spreadsheet ID into setup.
8. Enter Project Currency plus local profile name, surname, and email.

Ledger creates and seeds the required tabs directly in Google Sheets format. Do not upload or convert an XLSX workbook. The starter tabs include mock register rows plus reference categories, account types, FX rates, classification rules, and setup instructions.

The wizard writes:

```text
.env
.ledger_public_setup/google_configured
.ledger_profile.json
```

Those setup files are ignored by Git and should stay private.

## Terminal Fallback

The browser setup is recommended. The terminal wizard remains available for headless installs:

```bash
python3 scripts/setup_google.py --force
```

## Stop The Server

In the terminal window running Ledger Public, press:

```text
Ctrl+C
```

## Change Port

```bash
LEDGER_PORT=8770 ./start_ledger_public.command
```

Then open:

```text
http://127.0.0.1:8770
```
