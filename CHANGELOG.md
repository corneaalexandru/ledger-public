# Changelog

Ledger Public follows the private Ledger development stream. Public releases contain the same shared UI/core behavior where it is safe to publish, without private data or credentials.

## 2026-06-22

- Fixed drawer date picker placement so low date fields keep the calendar header visible instead of clipping inside the drawer body.
- Restored app-styled date pickers across transaction, trade, portfolio plan, and exit-phase edit forms while keeping ISO text entry and avoiding native calendar clipping.
- Added transaction activity/native-currency totals for not-accountable filtered slices and preserved compatible Transaction filters when switching register tabs or refining cards.
- Renamed the Metrics tabs to Statement, moved Planning target diagnostics into Transactions > Statement, removed Planning > Metrics, and added account country breakdowns to Accounts > Statement.

## 2026-06-21

- Tightened shared register metric-card spacing so the cards sit evenly between tabs and the following section headings.
- Removed the Navy Translucent theme mode and kept theme cycling to Dark, Navy, and Light.
- Made shared metric cards clickable where they can drill into a real filtered register or Portfolio/Transactions target subpage.
- Added the shared topbar text-size control and moved the monthly target category/month model blocks into Transactions > Metrics with the Overview-style line format.
- Removed the compact asterisk progress meters from Metrics rows and refreshed the static asset cache so the text-only metrics layout is restored.

## 2026-06-20

- Mirrored the shared Ledger UI, health-indicator, theme, and static cache updates into Ledger Public.
- Added deleted-date traceability display for transactions, accounts, and trades, including visible fallbacks when older deleted rows have no recorded timestamp.
- Fixed dark/Navy form field contrast in searchable combo boxes, category/subcategory inputs, and select option lists.
- Added a third Navy theme mode beside Dark and Light, with a dedicated deep-blue background/surface palette and sidebar cycle support.
- Made Navy the first-load default theme and moved theme preference storage to a fresh key so older auto-saved Dark preferences do not override the new default.
- Clarified the Monte Carlo compact card by showing planned investment, capital at work, and projected growth separately from the ending projection value.
- Aligned compact chart card headers with their right-side controls and renamed the Monte Carlo investment basis to projected invested capital.
- Changed Planning target variance to show under-ceiling spending as positive and over-ceiling spending as negative across monthly and yearly tables.
- Defaulted register pagination to 100 rows and standardized transaction row height to the Deleted tab rhythm.
- Standardized the Portfolio Instruments table row height with the main register tables.
- Added Portfolio Instruments footer pagination and brought Planning/Portfolio support tables onto the standard register row height.
- Extended the standard register row height to Transactions target monthly tables.
- Added shared footer pagination and scrollable table bodies to Planning, target, and Portfolio support tables.
- Centralized Trade Returns, Portfolio Performance, and Portfolio Funding chart cards under Overview > Charts with source-prefixed chart titles.
- Converted Portfolio, Planning, Statements Import, and supporting summary tables to the shared minimal table shell with consistent headers, spacing, footer navigation, and row density.
- Aligned Portfolio Overview, Performance, Funding, Planning Targets, Exit Strategy, and Monthly Plan table offsets so their headers and bodies follow the same visual rhythm.
- Standardized Statement Import queue rows and repaired the import table layout so selection controls, headers, amounts, matches, and targets no longer drift or overlap.
- Tightened metric-section spacing and restored insight/progress bars to fixed, proportional rendering instead of frozen or oversized markers.
- Aligned Settings inline input/select heights to the compact currency-field rhythm.
- Removed the animated loading skeleton and simplified loading screens to a plain text loading label.
- Reduced shared table row height and then set the universal minimal table body row height to 60px across the project.
- Renamed Insights tabs/sections to Metrics and converted metric pages to the same text-forward style as Overview Metrics.
- Aligned shared table panel header actions so buttons sit on the same baseline as section titles.
- Fixed Intelligence Threshold defaults so missing or collapsed-minimum local settings restore and persist the intended thresholds instead of showing `1`/`0` values.

## 2026-06-19

- Treated explicit `uncategorized` transaction categories as data-health issues and kept public transaction summaries aligned with that rule.
- Reordered transaction insight panels to Category Spend, Currency Flow, and Income Sources, and pinned income target achieved bars to the dark progress color.
- Corrected income target bars so achieved progress stays dark and only above-target surplus renders green, including zero-target surplus rows.
- Standardized table typography tokens so Portfolio, Trades, Planning, import, and data tables share one primary/subtitle font treatment.
- Rendered compact indicator bars as crisp SVG fixed-height strokes, and kept income surplus green only on the over-target segment.

## 2026-06-18

- Changed insight-list indicator bars to a uniform fixed width so the first/highest row no longer visually dominates the breakdown.
- Removed the document side rail and grouped Overview, Settings, About, and Changelog lists into clearer categorized sections with consistent text color.
- Added consistent spacing between compact list icons and labels across the grouped document-style rows.

## 2026-06-17

- Replaced the expanded README screenshot gallery with eight light-mode key views for setup, overview, accounts, transactions, targets, trades, portfolio, and planning.
- Fixed public local-store filtering so frontend control parameters such as trade risk thresholds no longer remove valid starter rows from API responses.
- Mirrored the shared Statements Import UI wording so queued rows show records, target identifiers, and target sheets instead of transaction-only labels.
- Rounded fractional trade quantities to six decimal places in shared trade-table displays.
- Mirrored the shared statement drawer so imported trade confirmations can open from trade detail records when available.
- Added the shared Source statement-file column to Trades so linked trade confirmations are visible directly in the table.
- Rounded visible trade quantities to two decimal places in shared tables, detail drawers, and statement-import labels while keeping source precision for stored values.
- Aligned the Transactions Targets tab with the detailed monthly target payload used by shared monthly target actuals.
- Kept the full Transactions tab strip visible in overall/all-period views so later filters such as Top Up, Review, and Deleted no longer fall off the edge.

## 2026-06-15

- Added a browser setup flow that captures the Google service-account key, Google Sheet URL, Project Currency, and local profile name/surname/email before seeding.
- Expanded starter Google Sheets with richer mock income, expense, transfer, account, trade, portfolio, category, FX, classification-rule, and setup-reference rows.
- Updated install documentation to spell out Google Sheets API enablement, service-account creation, Sheet sharing, and native Google Sheets setup.
- Expanded the README screenshot gallery to cover setup, account details, Insights, chart views, Targets in all/year/month modes, Statements Import, Trades, Portfolio, Planning, Settings, and About.
- Added release checks for the new web setup first-run path so clean installs do not create local CSV or spreadsheet artifacts.
- Changed target progress bars to use visible dark-gray achieved fills in dark mode instead of near-black fills that disappear on the black background.
- Removed the separate setup-guide button and moved the Google Cloud, Sheet sharing, and Ledger setup instructions into the web checklist.
- Standardized native Google Sheet setup so all Ledger tabs get the same grid size, row height, column width, frozen header row, and header styling.
- Switched Google Sheet converted amount cells to native Google Sheets currency formulas instead of treating starter FX rows as the conversion source.
- Added launcher port fallback so an occupied default port automatically rolls to the next free port.

## 2026-06-14

- Added total rows to the monthly target income and expense category model tables so each breakdown shows target, actual, and share or over-ceiling totals.
- Reduced data-health noise by treating valid zero FX values as present, ignoring deleted rows, checking stale prices only for active trades, and treating explicit manual transactions as linked.
- Hardened the SQLite snapshot cache with WAL mode and a longer busy timeout for concurrent local UI reads.
- Aligned shared schema metadata with the app's `txn_` and `trd_` ID prefixes and full Google Sheet column ranges.

## 2026-06-13

- Moved drawer scrolling into a padded body region and let email previews expand naturally so imported statement scrollbars no longer float through preview content.
- Kept subpage tab bars and Settings/About dividers in normal page flow so they no longer float over scrolled content.
- Collapsed Portfolio name/code quick filters so `Portfolio 1` and `P1` render as one portfolio identity.
- Prevented imported statement PDF previews from trapping scroll inside transaction drawers.
- Changed account and transaction country edit fields to plain two-letter country-code inputs without browser/datalist autofill suggestions.
- Kept scroll position inside register tables when opening or closing detail drawers from any row.
- Improved print/PDF output with landscape A4 layout, compact matching typography, fitted tables, and cleaner print headers.
- Expanded Financial Health scoring with retained-capital shortfall, ledger leakage, and compounding deficit inputs.
- Matched Portfolio quick filters to register behavior with removable chips for portfolio, provider, ticker, and funding fields.
- Moved the shared account `country_code` schema next to account type so native Google Sheets expose Country in the expected place.
- Removed the legacy local file writer so Ledger Public uses native Google Sheets as the supported setup path.
- Labeled the Settings content as the General settings subpage under the page header.
- Replaced the public starter-file workflow with native Google Sheet setup that creates and seeds tabs directly.
- Seeded account country codes in the public starter rows so the Accounts Country column is populated immediately.
- Flattened Overview insights into one continuous bordered bullet list and removed the group headers.
- Added a Settings header/content divider so the page matches the About page boundary treatment.

## 2026-06-12

- Added account country support across the Accounts Google Sheet schema, API filters, table, details, and edit form.
- Standardized Overview, Settings, and About bullet sections with the same left-border document-list treatment.
- Removed the repeated single-month target recap row so month drilldowns open directly on category models.
- Converted the Overview headline metrics from cards into the same plain bullet-list style as the supporting sections.
- Added persistent transaction drawer back controls so statement attachments, details, and edit views can switch without closing the drawer.
- Added a weighted Financial Health score to Overview using liquidity, cashflow, savings, target discipline, debt, concentration, capital momentum, and data quality.
- Bounded target progress bars so red over-target segments scale inside the available period column instead of spilling into adjacent values.
- Removed the duplicate structural overspending review signal from Overview while keeping the existing Risk metric.
- Moved structural overspending from the Overview headline row into Risk bullets and promoted Liquid Capital in its place.
- Reduced Overview to five headline insight cards and moved supporting metrics into Settings-style bullet sections.
- Kept active transaction filter chips such as category filters when changing the selected day, month, or year.
- Corrected yearly and monthly target row bars to show expense ceiling progress with red over-ceiling extension and fixed bar alignment.
- Reordered Settings bullets into a cleaner profile, project, source truth, sync, connections, thresholds, and preferences flow.
- Tightened Settings inline inputs and action buttons so fields match text scale and threshold units no longer duplicate.
- Removed the remaining profile username/password fields and password hashing so Ledger opens without a login/authentication module.
- Added compact target progress bars beside year and month labels in target summary tables.
- Matched Settings to the plain About bullet-list style.
- Standardized Settings and About into simpler line-by-line document rows.
- Removed the redundant label, filename, and release-history text above the About changelog content.
- Removed the duplicate divider line below detail drawer headers.
- Extended monthly target progress bars with a red proportional over-target segment.
- Kept transaction date, month, and year quick filters active when switching to Insights or Targets.
- Fixed monthly target drilldowns so month rows stay in Targets and keep the top period selector in sync.
- Flattened Settings into one page and standardized Settings/About into one-card-per-item insight grids.
- Added grey planned and black achieved progress bars to monthly target category rows.
- Moved About into its own sidebar page below Settings and removed the raw markdown opener from the changelog view.
- Reworked Settings sections into compact cards and added Settings > Profile for name, surname, and email.
- Removed the browser username/password setup flow from the launcher and kept the profile store informational only.

## 2026-06-11

- Normalized Google Sheets date serials back to ISO dates when reading native Google Sheets rows.
- Recalculated transaction conversions from edited statement amounts even when the disabled sanitized amount field is not submitted.
- Renamed the visible transaction base column to Project Amount.
- Added INR as a supported Project Currency and shipped a static changelog fallback for stale server routes.
- Added switchable Project Currency support, setup-time Project Currency selection, expanded starter currency references, and a hardened Settings changelog loader.
- Added Settings > About with copyright, license, contact, disclaimer, and changelog subpages linked to `CHANGELOG.md`.
- Added Google Sheets mode using a user-owned spreadsheet and service-account JSON.
- Added native Google Sheet starter seeding with mock data and reference tabs.
- Added one-time setup wizard in `scripts/setup_google.py`.
- Updated `start_ledger_public.command` to pull the latest app version, install Google requirements when missing, run setup once, and start in Google mode.
- Added release guards for credentials, `.env`, runtime data, backups, and private markers.
