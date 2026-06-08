#!/usr/bin/env python3
"""
Stripe → QuickBooks CSV Converter
CLI: Convert Stripe CSV exports to QuickBooks-compatible format.

Usage:
  python cli.py input.csv -o output.csv -f bank
  python cli.py input.csv -f sales_receipt --preview
  python cli.py input.csv --summary
"""

import argparse
import sys
from pathlib import Path

from core.parser import StripeCSVParser
from core.transformer import QBOTransformer


def main():
    ap = argparse.ArgumentParser(
        description="Convert Stripe CSV → QuickBooks CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py stripe_export.csv -o qbo_ready.csv
  python cli.py stripe_export.csv -f sales_receipt -o receipts.csv
  python cli.py stripe_export.csv -f journal -o journal.csv
  python cli.py stripe_export.csv --summary
  python cli.py stripe_export.csv -f bank --preview
        """,
    )
    ap.add_argument("input", type=Path, help="Path to Stripe CSV export")
    ap.add_argument("-o", "--output", type=Path, help="Output CSV path")
    ap.add_argument(
        "-f",
        "--format",
        choices=["bank", "sales_receipt", "journal", "combined"],
        default="bank",
        help="Output format (default: bank)",
    )
    ap.add_argument("--preview", action="store_true", help="Print first 10 rows instead of saving")
    ap.add_argument("--summary", action="store_true", help="Show transaction summary only")
    ap.add_argument("--delimiter", default="auto", help="CSV delimiter (default: auto-detect)")

    args = ap.parse_args()

    if not args.input.exists():
        print(f"Error: file not found: {args.input}")
        sys.exit(1)

    print(f"Parsing: {args.input}")
    parser = StripeCSVParser(args.input)
    transactions = parser.parse()
    print(f"  Found {len(transactions)} transactions\n")

    transformer = QBOTransformer(transactions)

    if args.summary:
        s = transformer.summary()
        print("=" * 50)
        print("  SUMMARY")
        print("=" * 50)
        print(f"  Transactions : {s['transactions']}")
        print(f"  Gross Charges: ${s['charges']:,.2f}")
        print(f"  Fees         : ${s['fees']:,.2f}")
        print(f"  Refunds      : ${s['refunds']:,.2f}")
        print(f"  Payouts      : ${s['payouts']:,.2f}")
        print(f"  Net Revenue  : ${s['net_revenue']:,.2f}")
        print("=" * 50)
        return

    format_map = {
        "bank": transformer.to_bank_transactions,
        "sales_receipt": transformer.to_sales_receipts,
        "journal": transformer.to_journal_entries,
        "combined": transformer.to_combined,
    }

    output = format_map[args.format]()

    if args.preview:
        lines = output.strip().split("\n")
        print(f"--- Preview ({args.format}) ---")
        for line in lines[:11]:
            print(line)
        if len(lines) > 11:
            print(f"... and {len(lines) - 11} more rows")
        return

    output_path = args.output or args.input.with_stem(args.input.stem + "_qbo").with_suffix(".csv")

    output_path.write_text(output, encoding="utf-8-sig")
    print(f"[OK] Saved: {output_path}")

    rows = output.strip().count("\n")
    print(f"  Format: {args.format} | {rows} lines")


if __name__ == "__main__":
    main()
