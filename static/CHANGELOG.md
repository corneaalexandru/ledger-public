# Changelog

Ledger development happens in the private `corneaalexandru/ledger` repository first. Public-safe changes are mirrored to `corneaalexandru/ledger-public` before release.

## 2026-06-25

- Moved Theme, Refresh, and Privacy into a compact topbar utility control beside the currency, print, and period controls.
- Added Income by Country and Expenses by Country sections to Transactions > Statement with country drill-downs into the transaction register.
- Added a compact topbar Project Currency switch beside the text-size controls so currency views can be changed from any page.
- Fixed project-currency transaction summaries plus transaction/account amount displays so USD/EUR project views use the sheet's direct converted columns instead of reconverting EUR totals with fallback rates.
- Added ADCB account alert email parsing and expanded PDF text extraction so Revolut transaction-statement PDFs with hex/TJ text streams import instead of landing in unsupported files.

## 2026-06-24

- Counted current-year income bonuses above the monthly target model into yearly actual savings while keeping the yearly income baseline and savings target fixed.
- Added achieved/used percentages beside actual amounts in the single-month income and expense target category detail view.
- Kept target-year monthly income baselines fixed to the modeled plan when current-month bonuses or surplus income exceed the recurring target.
- Limited topbar segmented-control glow to hover so selected font and period controls stay visually quiet at rest.
- Matched the reporting period center segment border model to the font-size stepper so All, Year, and Month states keep a complete outline.

## 2026-06-23

- Matched the font-size stepper hover border behavior to the reporting period selector so active segments show a complete outline.
- Corrected Income Sources labels in Transactions > Statement and removed the category-heavy income-baseline and expense-ceiling rule lists.
- Clarified the Statement pages across Overview, Accounts, Transactions, Trades, and Portfolio, and fixed Overview category concentration so it uses selected-period spending instead of a current-month denominator.
- Kept debt out of account structure breakdowns so country, provider, type, bucket, and currency rows show active assets while liabilities remain in the balance-sheet and credit-risk sections.
- Reduced the Net Worth hero to the standard 64px hero scale so the Overview header matches the compact dashboard rhythm.
- Uppercased visible account register IDs in Overview, search, and account selection fallbacks so `acct_` identifiers display consistently with other register IDs.
- Uppercased visible transaction/trade register IDs across the UI, formatted register names in Statements Import, and tightened the Net Worth hero scale for a calmer Overview ratio.
- Kept table scrollbars from bleeding through open edit drawers and moved sticky drawer actions clear of the drawer scroll thumb.
- Simplified global keyboard shortcuts: `/` focuses search, `P` cycles the reporting period, and `Esc` backs out of panels before clearing active search and filters.
- Added Portfolio > Statement as the first/default Portfolio subpage and constrained statement attachment previews so long source text no longer widens the drawer.
- Polished edit drawers for easier register entry: uppercase visible IDs, labeled account type/bucket choices, hidden non-credit account credit fields, hidden transaction helper amounts, and a reserved scrollbar lane.
- Moved Statement to the first tab position on pages that have a Statement subpage, and placed Transactions > Targets second after Statement.
- Made Accounts, Transactions, and Trades open on the Statement subpage by default.
- Fixed remaining Statement-opening paths so opening Accounts/Transactions/Trades via insight filters no longer lands back on Register, including quick-filter reload paths and transaction quick filters.
- Centralized Statement defaulting so Overview, Accounts, Transactions, and Trades return to Statement when opened from page-entry paths, while explicit Register and Targets tabs stay intentional.
- Fixed the first-open Transactions page crash by guarding Statement renders before account, transaction, or trade data has loaded and by making the Transactions Statement row-count lookup null-safe.
- Changed Statement metric drill-downs so account, transaction, category, heatmap, and trade links apply their filters and open the relevant register table instead of staying on Statement.

## 2026-06-22

- Fixed drawer date picker placement so low date fields keep the calendar header visible instead of clipping inside the drawer body.
- Restored app-styled date pickers across transaction, trade, portfolio plan, and exit-phase edit forms while keeping ISO text entry and avoiding native calendar clipping.
- Added transaction activity/native-currency totals for not-accountable filtered slices and preserved compatible Transaction filters when switching register tabs or refining cards.
- Renamed the Metrics tabs to Statement, moved Planning target diagnostics into Transactions > Statement, removed Planning > Metrics, and added account country breakdowns to Accounts > Statement.

## 2026-06-21

- Tightened shared register metric-card spacing so the cards sit evenly between tabs and the following section headings.
- Added Planning > Metrics and moved the capital-retention and planning diagnostic metric blocks out of Planning > Targets.
- Split Transactions > Metrics spending into category and subcategory metric sections with clickable drill-down filters.
- Merged Trades > Returns into Trades > Metrics and removed the separate Returns tab.
- Fixed Transactions > Metrics so cash-flow summary cards use the selected reporting period instead of current-month totals.
- Removed the Navy Translucent theme mode and kept theme cycling to Dark, Navy, and Light.
- Reorganized existing Metrics sections into the suggested domain groups, keeping the current pages/components while moving monthly target diagnostics under Planning.
- Made Overview, Accounts, Transactions, Trades, Portfolio, Planning, and target-model metric cards clickable where they can drill into a real filtered register or subpage.
- Added a topbar text-size control with decrease, standard, and increase actions, and moved the monthly target category/month model blocks into Transactions > Metrics using the Overview-style line format.
- Removed the compact asterisk progress meters from Metrics rows and refreshed the static asset cache so the text-only metrics layout is restored.

## 2026-06-20

- Improved the Ledger transaction/import read model, theming controls, health indicators, and static cache refreshes for the current UI pass.
- Added deleted-date traceability for transactions, accounts, and trades, including visible fallbacks when an older deleted row has no recorded timestamp.
- Fixed duplicate import handling around deleted or missing registry targets so previously deleted statement records can be selected and force-imported again when needed.
- Preserved statement attachment links during forced imports and used the Ledger import date as the posted date for newly imported transactions.
- Fixed dark/Navy form field contrast in searchable combo boxes, category/subcategory inputs, and select option lists.
- Added a third Navy theme mode beside Dark and Light, with a dedicated deep-blue background/surface palette and sidebar cycle support.
- Made Navy the first-load default theme and moved theme preference storage to a fresh key so older auto-saved Dark preferences do not override the new default.
- Clarified the Monte Carlo compact card by showing planned investment, capital at work, and projected growth separately from the ending projection value.
- Aligned compact chart card headers with their right-side controls and renamed the Monte Carlo investment basis to projected invested capital.
- Changed Planning target variance to show under-ceiling spending as positive and over-ceiling spending as negative across monthly and yearly tables.
- Defaulted register pagination to 100 rows, added custom category/subcategory entry from transaction edit dropdowns, and standardized transaction row height to the Deleted tab rhythm.
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

- Optimized transaction read-model parsing, expanded transaction sheet reads through `A:X`, mapped import appends by live headers, and treated explicit `uncategorized` categories as data-health issues.
- Restored the Trades statement icon to a dedicated Source column so it matches the Transactions register placement.
- Reordered transaction insight panels to Category Spend, Currency Flow, and Income Sources, and pinned income target achieved bars to the dark progress color.
- Corrected income target bars so achieved progress stays dark and only above-target surplus renders green, including zero-target surplus rows.
- Standardized table typography tokens so Portfolio, Trades, Planning, import, and data tables share one primary/subtitle font treatment.
- Standardized the Net Worth compact chart controls to use the same unlabeled pill selector style as the other chart cards.
- Brought Portfolio, Planning, import, insight, and supporting data tables closer to the disciplined Accounts/Transactions register style with quieter spacing, typography, dividers, and fewer inline decorative bars.
- Hid internal account IDs from Accounts register rows when a usable account reference is already displayed, keeping the ID only as a fallback for rows without reference details.
- Reduced visual weight in the Portfolio instruments table with a thinner allocation track, softer allocation text, and monochrome value emphasis.
- Simplified Portfolio instrument row copy and kept the Portfolio funding/performance charts inline-only by removing their expanded view controls.
- Reduced Portfolio Performance and Portfolio Funding table copy to compact decision labels with shorter portfolio, progress, and plan details.
- Replaced the Monte Carlo expanded view with inline Historic and Conservative assumption buttons on the compact projection card.
- Moved Net Worth Forecast assumptions into the compact chart header and removed its expanded chart view.
- Removed the Cash Flow expanded chart view so the Overview chart stays as a compact inline trend.
- Replaced the Net Worth expanded chart with inline History and Forecast controls plus leakage, deficit, income, and forecast context lines in the compact chart.
- Added an inline Monte Carlo scope selector so the compact projection can switch between the plan, portfolios, and individual instruments.
- Split the Portfolio Funding chart period selectors so Cumulative Contributions and Monthly Funding Progress keep independent windows.
- Added a Net/Context toggle to the Net Worth chart so the default view stays as a simple net-worth line while the richer leakage, income, and forecast context appears on demand.
- Replaced the Monte Carlo scope button strip with a compact styled dropdown that matches the surrounding chart controls.
- Softened the compact Monte Carlo projection stroke so scenario lines match the visual weight of the other Overview charts.
- Rendered compact indicator bars as crisp SVG fixed-height strokes, and kept income surplus green only on the over-target segment.
- Standardized portfolio identity labels to compact `P` references across Planning, quick filters, drawers, and chart controls.
- Reshaped the Trades register to match the Portfolio instruments table with compact instrument, portfolio, entry, value, and P/L columns.
- Fixed the compact Trades P/L column so it sorts by the displayed mixed active/closed P/L value instead of an internal unrealized-only field.

## 2026-06-18

- Added the private Docker runtime path and launcher updates so Ledger Private can be restarted through one container instead of accumulating separate Python servers.
- Updated the monthly investment plan and Monte Carlo projection flow for the 60/40 allocation plan, MIP-paced deployment, historical 10-year assumptions, and filtered portfolio/instrument scopes.
- Simplified compact and expanded chart presentation with cleaner external cards, hover-focused line identification, reduced legends, and less visual clutter.
- Reworked detail drawers with compact sectioned forms, sticky save actions, dirty/saving state feedback, searchable dropdown menus, and country dropdowns that avoid browser address autofill.
- Refined register and planning tables with denser rows, quiet status/review chips, softer selected-row styling, transaction import badges, trade status chips, and portfolio allocation meters.
- Fixed the Transactions all-period register so future-dated planned rows remain visible instead of being capped at today's date on first load.
- Removed rounded country/currency table token bubbles and replaced native table checkboxes with a consistent compact square control.
- Refined searchable drawer dropdowns with a separated search header so options no longer sit under the search field.
- Made register tables more monochrome by neutralizing colored row values/statuses and removing checkbox-column dividers.
- Softened shared border tokens, table separators, drawer dividers, and control outlines for a lighter minimalist interface.
- Changed insight-list indicator bars to a uniform fixed width so the first/highest row no longer visually dominates the breakdown.
- Removed the document side rail and grouped Overview, Settings, About, and Changelog lists into clearer categorized sections with consistent text color.
- Added consistent spacing between compact list icons and labels across the grouped document-style rows.

## 2026-06-17

- Added Statements Import support for IBKR trade-confirmation emails and Revolut Securities trade-confirmation PDFs, routing confirmed buys into `trades_register` instead of misclassifying them as income/expense transactions.
- Integrated imported trades with portfolio strategy matching so base symbols such as `VWCE`, `SXRV`, and `XNAS` resolve to strategy tickers, portfolio IDs, and asset names where available.
- Updated the import preview and registry to track the target sheet/identifier for both transactions and trades, and expanded the private `trades_register` range to include review status and notes.
- Rounded fractional trade quantities to six decimal places in imported trade rows and trade-table displays.
- Linked imported trade confirmations back to trade details so IBKR/Revolut statement files open from the trade drawer after import.
- Added the same Source statement-file column to Trades that Transactions uses, so linked trade confirmations are visible directly in the table.
- Fixed transaction search and target inconsistencies so `maria` no longer resolves as a country-only query, future-dated manual rows count in their target month, and transaction writes refresh cached reads after FX updates.
- Rounded visible trade quantities to two decimal places in tables, detail drawers, and statement-import labels while keeping source precision for stored values.
- Aligned the Transactions Targets tab with the detailed monthly target payload and covered manual transfer rows whose transaction date differs from posted date.
- Kept the full Transactions tab strip visible in overall/all-period views so later filters such as Top Up, Review, and Deleted no longer fall off the edge.

## 2026-06-15

- Added a Ledger Public browser setup flow that captures the Google service-account key, Google Sheet URL, Project Currency, and local profile name/surname/email before seeding.
- Expanded Ledger Public starter Google Sheets with richer mock income, expense, transfer, account, trade, portfolio, category, FX, classification-rule, and setup-reference rows.
- Updated public install documentation to spell out Google Sheets API enablement, service-account creation, Sheet sharing, and native Google Sheets setup.
- Expanded the Ledger Public README screenshot gallery to cover setup, account details, Insights, chart views, Targets in all/year/month modes, Statements Import, Trades, Portfolio, Planning, Settings, and About.
- Added release checks for the new web setup first-run path so clean installs do not create local CSV or spreadsheet artifacts.
- Changed target progress bars to use visible dark-gray achieved fills in dark mode instead of near-black fills that disappear on the black background.
- Removed the separate Ledger Public setup-guide button and moved the Google Cloud, Sheet sharing, and Ledger setup instructions into the web checklist.
- Standardized native Google Sheet setup so all Ledger tabs get the same grid size, row height, column width, frozen header row, and header styling.
- Switched public Google Sheet converted amount cells to native Google Sheets currency formulas instead of treating starter FX rows as the conversion source.
- Added private and public launcher port fallback so an occupied default port automatically rolls to the next free port.

## 2026-06-14

- Added total rows to the monthly target income and expense category model tables so each breakdown shows target, actual, and share or over-ceiling totals.
- Reduced data-health noise by treating valid zero FX values as present, ignoring deleted rows, checking stale prices only for active trades, and treating explicit manual transactions as linked.
- Switched the data-health endpoint to raw sheet values so diagnostics can distinguish blank fields from calculated zero values.
- Hardened the SQLite snapshot cache with WAL mode and a longer busy timeout for concurrent local UI reads.
- Normalized trade-price refresh symbols before quote loading so blank, spaced, or non-string sheet values do not break refreshes.
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
- Moved the shared account `country_code` schema next to account type so private repairs and public native Google Sheets expose Country in the expected place.
- Removed the public legacy local file writer so Ledger Public uses native Google Sheets as the supported setup path.
- Labeled the Settings content as the General settings subpage under the page header.
- Auto-repaired older private `accounts_register` sheets by adding the missing `country_code` column during live account reads.
- Replaced the public starter-file workflow with native Google Sheet setup that creates and seeds tabs directly.
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
- Matched Settings to the plain About bullet-list style and set Brokerage Revenue monthly plan targets to zero.
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
- Removed the browser username/password setup flow from private and public launchers and kept the profile store informational only.

## 2026-06-11

- Removed the Docker/container runtime option so Ledger runs through the direct Python launcher path only.
- Normalized Google Sheets date serials back to ISO dates when reading native Google Sheets rows.
- Recalculated public transaction conversions from edited statement amounts even when the disabled sanitized amount field is not submitted.
- Renamed the visible transaction base column to Project Amount.
- Added INR as a supported Project Currency and shipped a static changelog fallback for stale server routes.
- Added switchable Project Currency support across EUR-normalized summaries/charts and hardened the Settings changelog loader.
- Added Settings > About with copyright, license, contact, disclaimer, and changelog subpages linked to `CHANGELOG.md`.
- Added shared private/public release gates and parity checks.
- Added shared `ledger_core` package for schemas, stores, FX helpers, health checks, backups, and report presets.
- Added public-safe `GoogleSheetsLedgerStore` so Ledger Public can use a user-owned Google Sheet.
- Added public Google-first setup plan with native Sheet seeding, one-time wizard, and auto-updating launcher.
- Added macOS launchers for private and public variants.
