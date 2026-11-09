# Implementation notes

**Q1 2026 net income:** **-$44,480.14** (January 1–March 31, inclusive).

**Accounting decisions.** Use only posted entries within the inclusive accounting-date range. Ignore draft and void entries, and balance-sheet accounts. Group by account subtype. Revenue and other income are credit minus debit; COGS and operating expenses are debit minus credit. Contra-revenue naturally subtracts from revenue. Include inactive accounts and zero-balance account rows. Do not smooth January rent or recognize the $12,000 deferred subscription billing early; use posted recognition entries. Keep exact `Decimal` arithmetic and serialize money as strings.

**Verification.** The Q1 ledger was independently reconciled at account level: revenue $37,850.50, COGS $14,272.75, gross profit $23,577.75, operating expenses $68,100.07, operating income -$44,522.32, other income $42.18, net income -$44,480.14. Pytest cases cover account values, date boundaries, 2025/2027 ranges, void/draft filtering, inactive marketing, rent, software credits, and API validation. **Execution status:** Tests and frontend build have not been executed in this environment; run the README commands before submission and update this note with actual results.

**AI assistance and skepticism.** AI assisted with architecture, implementation and test drafting. We did not trust the initial financial totals without independent line-by-line Decimal reconciliation, especially contra-revenue, inactive marketing and the software credit. This describes verification, not a fabricated AI error.

**With more time.** Run the full stack on macOS, add browser-level integration coverage and an optional transaction drill-down. Record the required <=5-minute walkthrough separately. Follow the official two-hour coding limit; do not claim unmeasured elapsed development time.
