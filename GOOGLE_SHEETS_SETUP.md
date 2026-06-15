# Google Sheets Setup

Ledger Public uses a user-owned Google Sheet as its database.

## 1. Create The Ledger Sheet

Create a blank native Google Sheet in Google Drive.

Copy the spreadsheet ID from the URL:

```text
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
```

## 2. Enable The Google Sheets API

In Google Cloud:

1. Create or choose a project.
2. Open **APIs & Services > Library**.
3. Search for **Google Sheets API**.
4. Click **Enable**.

Ledger Public uses the Sheets API to create tabs, write headers, seed starter rows, and read/write register data.

## 3. Create A Service Account

In the same Google Cloud project:

1. Open **IAM & Admin > Service Accounts**.
2. Create a service account for Ledger Public.
3. Open the service account, choose **Keys**, then create a new JSON key.
4. Save the JSON file locally. The browser setup will copy it into:

```text
credentials/ledger-public-service-account.json
```

## 4. Share The Sheet

Open the JSON file and find `client_email`.

Share the Google Sheet with that email as Editor.

The service account is not your normal Google account. Sharing the Sheet with your own email is not enough; it must be shared with the service-account `client_email`.

## 5. Run The Browser Setup

On macOS, double-click:

```text
start_ledger_public.command
```

Or run manually:

```bash
python3 -m pip install -r requirements-google.txt
python3 server.py --setup --open
```

The setup page asks for:

- Service-account JSON file.
- Google Sheet URL or spreadsheet ID.
- Project Currency.
- Profile name, surname, and email.

It writes `.env` once:

```env
LEDGER_STORE=google
LEDGER_SPREADSHEET_ID=your_google_sheet_id_here
GOOGLE_APPLICATION_CREDENTIALS=credentials/ledger-public-service-account.json
LEDGER_PROJECT_CURRENCY=EUR
```

It also writes `.ledger_public_setup/google_configured` and `.ledger_profile.json`. These files are ignored by Git.

The setup page creates and seeds the required Ledger tabs directly in native Google Sheets format. Starter content includes mock accounts, transactions, trades, portfolio plans, category references, account types, FX rates, classification rules, and setup instructions.

Supported Project Currency values are EUR, USD, AED, RON, GBP, CHF, CAD, AUD, INR, and JPY.

## Why Native Google Sheets

Google Sheets is the live database for Ledger Public. Using the Sheets API keeps the user-owned Sheet as the source of truth and lets setup create or repair tabs in place.

## Terminal Fallback

Use this only when browser setup is not practical:

```bash
python3 scripts/setup_google.py --force
```

## 6. Start Ledger

```bash
python3 server.py --store google --open
```

After setup, the launcher starts Ledger directly. To re-run terminal setup:

```bash
python3 scripts/setup_google.py --force
```
