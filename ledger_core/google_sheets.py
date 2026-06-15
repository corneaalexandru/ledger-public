from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from ledger_core.fx import DEFAULT_CONVERTER, FXConverter
from ledger_core.local_csv import LocalCsvLedgerStore
from ledger_core.schemas import SHEETS
from ledger_core.store import next_id, normalize_ids


GOOGLE_SCOPES = ("https://www.googleapis.com/auth/spreadsheets",)
STANDARD_SHEET_ROW_COUNT = 1000
STANDARD_SHEET_MIN_COLUMN_COUNT = 26
STANDARD_SHEET_ROW_HEIGHT = 28
STANDARD_SHEET_COLUMN_WIDTH = 140
SHEET_IMPORT_ALIASES = {
    # Older public seeds used this shortened tab name. Native Google Sheet setup
    # writes the canonical tab directly.
    "portfolio_monthly_investment_plan": "portfolio_monthly_investment_pl",
}
GOOGLE_DATE_FIELDS = {
    "mip_phase_end_date_target",
    "price_as_of",
    *{header for headers in SHEETS.values() for header in headers if header.endswith("_date")},
}
GOOGLE_SHEETS_DATE_EPOCH = date(1899, 12, 30)


@dataclass(frozen=True)
class GoogleSheetsConfig:
    spreadsheet_id: str
    credentials_path: Path


class GoogleSheetsLedgerStore:
    def __init__(
        self,
        config: GoogleSheetsConfig,
        *,
        sheets: dict[str, list[str]] | None = None,
        fx: FXConverter | None = None,
        starter_rows: dict[str, list[dict]] | None = None,
    ) -> None:
        self.config = config
        self.sheets = sheets or SHEETS
        self.fx = fx or DEFAULT_CONVERTER
        self.starter_rows = starter_rows or {}
        self._normalizer = LocalCsvLedgerStore(Path("."), sheets=self.sheets, fx=self.fx)
        self._service = None

    @property
    def service(self) -> Any:
        if self._service is None:
            self._service = build_sheets_service(self.config.credentials_path)
        return self._service

    def list_rows(self, sheet_name: str) -> list[dict]:
        return self._list_rows_from_tab(sheet_name, sheet_name)

    def _list_rows_from_tab(self, tab_name: str, sheet_name: str) -> list[dict]:
        headers = self.sheets[sheet_name]
        values = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.config.spreadsheet_id,
                range=f"{quote_sheet_name(tab_name)}!A1:{column_name(len(headers))}",
                valueRenderOption="UNFORMATTED_VALUE",
            )
            .execute()
            .get("values", [])
        )
        if not values:
            return []
        sheet_headers = [str(value).strip() for value in values[0]]
        if not any(sheet_headers):
            sheet_headers = headers
        rows = []
        for raw_row in values[1:]:
            row = {
                header: google_sheet_value(header, raw_row[index] if index < len(raw_row) else "")
                for index, header in enumerate(sheet_headers)
            }
            rows.append(self._normalizer.normalize_row(sheet_name, {header: row.get(header, "") for header in headers}))
        return rows

    def write_rows(self, sheet_name: str, rows: list[dict]) -> None:
        headers = self.sheets[sheet_name]
        values = [headers]
        for row_index, row in enumerate(rows, start=2):
            normalized = self._normalizer.normalize_row(sheet_name, row)
            normalized.update(google_formula_values(sheet_name, row_index, headers))
            values.append([normalized.get(header, "") for header in headers])
        tab = quote_sheet_name(sheet_name)
        body = {"values": values}
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.config.spreadsheet_id,
            range=f"{tab}!A:{column_name(len(headers))}",
            body={},
        ).execute()
        self.service.spreadsheets().values().update(
            spreadsheetId=self.config.spreadsheet_id,
            range=f"{tab}!A1",
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()

    def upsert_row(self, sheet_name: str, id_field: str, row_id: str, values: dict) -> dict:
        rows = self.list_rows(sheet_name)
        for index, row in enumerate(rows):
            if str(row.get(id_field, "")) == str(row_id):
                rows[index] = self._normalizer.normalize_row(sheet_name, {**row, **values})
                self.write_rows(sheet_name, rows)
                return rows[index]
        raise KeyError(f"{row_id} was not found.")

    def append_row(self, sheet_name: str, id_field: str, prefix: str, values: dict, defaults: dict | None = None) -> dict:
        rows = self.list_rows(sheet_name)
        row_id = str(values.get(id_field) or next_id(rows, id_field, prefix)).strip()
        if any(str(row.get(id_field)) == row_id for row in rows):
            raise ValueError(f"{row_id} already exists.")
        defaults = defaults or {}
        row = {header: values.get(header, defaults.get(header, "")) for header in self.sheets[sheet_name]}
        row[id_field] = row_id
        row = self._normalizer.normalize_row(sheet_name, row)
        rows.append(row)
        self.write_rows(sheet_name, rows)
        return row

    def soft_delete(self, sheet_name: str, id_field: str, ids: list[str]) -> dict:
        return self._mutate_status(sheet_name, id_field, ids, "deleted")

    def restore(self, sheet_name: str, id_field: str, ids: list[str]) -> dict:
        return self._mutate_status(sheet_name, id_field, ids, "accountable")

    def refresh(self) -> dict:
        return {"ok": True, "mode": "google_sheets", "spreadsheet_id": self.config.spreadsheet_id}

    def ensure_sheets(self, *, seed_empty: bool = False) -> dict:
        metadata = self.service.spreadsheets().get(spreadsheetId=self.config.spreadsheet_id).execute()
        existing = {
            sheet["properties"]["title"]: sheet["properties"]["sheetId"]
            for sheet in metadata.get("sheets", [])
        }
        alias_rows = {}
        for sheet_name, alias in SHEET_IMPORT_ALIASES.items():
            if sheet_name not in existing and alias in existing:
                alias_rows[sheet_name] = self._list_rows_from_tab(alias, sheet_name)

        requests = [
            {"addSheet": {"properties": {"title": sheet_name}}}
            for sheet_name in self.sheets
            if sheet_name not in existing
        ]
        if requests:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.config.spreadsheet_id,
                body={"requests": requests},
            ).execute()
            metadata = self.service.spreadsheets().get(spreadsheetId=self.config.spreadsheet_id).execute()
            existing = {
                sheet["properties"]["title"]: sheet["properties"]["sheetId"]
                for sheet in metadata.get("sheets", [])
            }

        created = {request["addSheet"]["properties"]["title"] for request in requests}
        available = set(existing) | created
        seeded_sheets = []
        for sheet_name, headers in self.sheets.items():
            rows = self.list_rows(sheet_name) if sheet_name in available else []
            if sheet_name in alias_rows and not rows:
                self.write_rows(sheet_name, alias_rows[sheet_name])
            elif seed_empty and not rows and self.starter_rows.get(sheet_name):
                self.write_rows(sheet_name, self.starter_rows[sheet_name])
                seeded_sheets.append(sheet_name)
            else:
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.config.spreadsheet_id,
                    range=f"{quote_sheet_name(sheet_name)}!A1",
                    valueInputOption="USER_ENTERED",
                    body={"values": [headers]},
                ).execute()
        self.standardize_sheet_layouts(existing)
        return {
            "ok": True,
            "sheets": list(self.sheets),
            "imported_aliases": sorted(alias_rows),
            "seeded_sheets": seeded_sheets,
        }

    def standardize_sheet_layouts(self, sheet_ids: dict[str, int] | None = None) -> None:
        sheet_ids = sheet_ids or {
            sheet["properties"]["title"]: sheet["properties"]["sheetId"]
            for sheet in self.service.spreadsheets().get(spreadsheetId=self.config.spreadsheet_id).execute().get("sheets", [])
        }
        column_count = max(STANDARD_SHEET_MIN_COLUMN_COUNT, *(len(headers) for headers in self.sheets.values()))
        requests = []
        for sheet_name in self.sheets:
            sheet_id = sheet_ids.get(sheet_name)
            if sheet_id is None:
                continue
            requests.extend(standard_sheet_layout_requests(sheet_id, column_count))
        if requests:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.config.spreadsheet_id,
                body={"requests": requests},
            ).execute()

    def _mutate_status(self, sheet_name: str, id_field: str, ids: list[str], ledger_status: str) -> dict:
        row_ids = normalize_ids(ids)
        rows = self.list_rows(sheet_name)
        found = set()
        for row in rows:
            if str(row.get(id_field, "")) in row_ids:
                found.add(str(row.get(id_field, "")))
                row["ledger_status"] = ledger_status
                if "review_status" in row:
                    row["review_status"] = "review_done" if ledger_status == "deleted" else "review_required"
        missing = [row_id for row_id in row_ids if row_id not in found]
        if missing:
            raise KeyError(f"Not found: {', '.join(missing)}")
        self.write_rows(sheet_name, rows)
        return {"ok": True, "count": len(row_ids), f"{id_field}s": row_ids}


def build_sheets_service(credentials_path: Path):
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError as error:
        raise RuntimeError(
            "Google Sheets mode requires Google client packages. Run: python3 -m pip install -r requirements-google.txt"
        ) from error

    credentials = service_account.Credentials.from_service_account_file(
        str(credentials_path),
        scopes=GOOGLE_SCOPES,
    )
    return build("sheets", "v4", credentials=credentials, cache_discovery=False)


def google_formula_values(sheet_name: str, row_number: int, headers: list[str]) -> dict[str, str]:
    if sheet_name == "accounts_register":
        return account_formula_values(row_number, headers)
    if sheet_name == "transactions_register":
        return transaction_formula_values(row_number, headers)
    if sheet_name == "portfolio_strategy_instruments":
        return portfolio_formula_values(row_number, headers)
    return {}


def account_formula_values(row_number: int, headers: list[str]) -> dict[str, str]:
    if not {"account_currency", "balance_native"}.issubset(headers):
        return {}
    formulas = {}
    if "amount_usd_converted" in headers:
        formulas["amount_usd_converted"] = spot_fx_formula(
            row_number,
            headers,
            currency_header="account_currency",
            amount_header="balance_native",
            target_currency="USD",
        )
    if "amount_eur_converted" in headers:
        formulas["amount_eur_converted"] = spot_fx_formula(
            row_number,
            headers,
            currency_header="account_currency",
            amount_header="balance_native",
            target_currency="EUR",
        )
    return formulas


def transaction_formula_values(row_number: int, headers: list[str]) -> dict[str, str]:
    if not {"statement_currency", "sanitized_statement_amount"}.issubset(headers):
        return {}
    formulas = {}
    if "amount_usd_converted" in headers:
        formulas["amount_usd_converted"] = historical_fx_formula(row_number, headers, "USD")
    if "amount_eur_converted" in headers:
        formulas["amount_eur_converted"] = historical_fx_formula(row_number, headers, "EUR")
    return formulas


def portfolio_formula_values(row_number: int, headers: list[str]) -> dict[str, str]:
    if not {"current_value_currency", "current_value_native", "current_value_eur"}.issubset(headers):
        return {}
    return {
        "current_value_eur": spot_fx_formula(
            row_number,
            headers,
            currency_header="current_value_currency",
            amount_header="current_value_native",
            target_currency="EUR",
        )
    }


def spot_fx_formula(
    row_number: int,
    headers: list[str],
    *,
    currency_header: str,
    amount_header: str,
    target_currency: str,
) -> str:
    currency_ref = cell_ref(headers, currency_header, row_number)
    amount_ref = cell_ref(headers, amount_header, row_number)
    normalized_currency = f"UPPER({currency_ref})"
    return (
        f'=IF(OR({currency_ref}="",{amount_ref}=""),"",'
        f'IF({normalized_currency}="{target_currency}",{amount_ref},'
        f'IFERROR({amount_ref}*GOOGLEFINANCE("CURRENCY:"&{normalized_currency}&"{target_currency}"),"")))'
    )


def historical_fx_formula(row_number: int, headers: list[str], target_currency: str) -> str:
    currency_ref = cell_ref(headers, "statement_currency", row_number)
    amount_ref = cell_ref(headers, "sanitized_statement_amount", row_number)
    posted_date_ref = cell_ref(headers, "posted_date", row_number) if "posted_date" in headers else ""
    transaction_date_ref = cell_ref(headers, "transaction_date", row_number) if "transaction_date" in headers else ""
    if transaction_date_ref and posted_date_ref:
        date_source = f'IF({transaction_date_ref}<>"",{transaction_date_ref},{posted_date_ref})'
    else:
        date_source = transaction_date_ref or posted_date_ref or "TODAY()"
    fx_date = f"MIN({date_source},TODAY())"
    normalized_currency = f"UPPER({currency_ref})"
    googlefinance_call = (
        f'GOOGLEFINANCE("CURRENCY:"&{normalized_currency}&"{target_currency}",'
        f'"price",{fx_date}-7,{fx_date})'
    )
    converted_amount = f"LET(fx,{googlefinance_call},{amount_ref}*INDEX(fx,ROWS(fx),2))"
    return (
        f'=IF(OR({currency_ref}="",{amount_ref}="",{date_source}=""),"",'
        f'IF({normalized_currency}="{target_currency}",{amount_ref},'
        f'IFERROR({converted_amount},"")))'
    )


def cell_ref(headers: list[str], header: str, row_number: int) -> str:
    return f"${column_name(headers.index(header) + 1)}{row_number}"


def standard_sheet_layout_requests(sheet_id: int, column_count: int) -> list[dict]:
    return [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {
                        "rowCount": STANDARD_SHEET_ROW_COUNT,
                        "columnCount": column_count,
                        "frozenRowCount": 1,
                    },
                },
                "fields": "gridProperties(rowCount,columnCount,frozenRowCount)",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": 0,
                    "endIndex": STANDARD_SHEET_ROW_COUNT,
                },
                "properties": {"pixelSize": STANDARD_SHEET_ROW_HEIGHT},
                "fields": "pixelSize",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": column_count,
                },
                "properties": {"pixelSize": STANDARD_SHEET_COLUMN_WIDTH},
                "fields": "pixelSize",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": column_count,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.88, "green": 0.94, "blue": 0.90},
                        "horizontalAlignment": "LEFT",
                        "verticalAlignment": "MIDDLE",
                        "textFormat": {"bold": True},
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,textFormat)",
            }
        },
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": STANDARD_SHEET_ROW_COUNT,
                        "startColumnIndex": 0,
                        "endColumnIndex": column_count,
                    }
                }
            }
        },
    ]


def column_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name or "A"


def quote_sheet_name(sheet_name: str) -> str:
    return "'" + sheet_name.replace("'", "''") + "'"


def google_sheet_value(header: str, value: Any) -> Any:
    if value is None:
        return ""
    if header not in GOOGLE_DATE_FIELDS:
        return value
    return google_date_serial_to_iso(value) or value


def google_date_serial_to_iso(value: Any) -> str:
    if isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        serial = float(value)
    elif isinstance(value, str) and value.strip().replace(".", "", 1).isdigit():
        serial = float(value.strip())
    else:
        return ""
    whole_days = int(serial)
    if abs(serial - whole_days) > 0.000001:
        return ""
    parsed = GOOGLE_SHEETS_DATE_EPOCH + timedelta(days=whole_days)
    if not 1900 <= parsed.year <= 2200:
        return ""
    return parsed.isoformat()
