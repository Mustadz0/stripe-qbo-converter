import csv
from datetime import datetime
from io import StringIO
from typing import List

from .models import StripeTransaction, StripeTxType


class QBOTransformer:
    """Converts parsed Stripe transactions → QuickBooks-compatible CSV"""

    OUTPUT_FORMATS = {
        "bank": "Bank Transactions",
        "sales_receipt": "Sales Receipts",
        "journal": "Journal Entries",
        "combined": "Combined (Bank + Fees)",
    }

    def __init__(self, transactions: List[StripeTransaction]):
        self.transactions = transactions

    def _fmt_date(self, raw: str) -> str:
        """Normalize dates to MM/DD/YYYY for QBO"""
        for fmt in (
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m/%d/%y",
            "%d/%m/%Y",
        ):
            try:
                return datetime.strptime(raw[:19], fmt).strftime("%m/%d/%Y")
            except (ValueError, IndexError):
                continue
        return raw[:10]

    def to_bank_transactions(self) -> str:
        """Output: Date, Description, Amount, Memo"""
        out = StringIO()
        w = csv.writer(out)
        w.writerow(["Date", "Description", "Amount", "Memo"])
        for tx in self._iter_bank_entries():
            w.writerow([tx["Date"], tx["Description"], tx["Amount"], tx["Memo"]])
        return out.getvalue()

    def to_sales_receipts(self) -> str:
        """Output for sales receipt import"""
        out = StringIO()
        w = csv.writer(out)
        w.writerow(
            [
                "Date",
                "Customer",
                "Item",
                "Item Amount",
                "Item Description",
                "Memo",
            ]
        )
        for tx in self.transactions:
            d = self._fmt_date(tx.date)
            if tx.tx_type == StripeTxType.CHARGE:
                w.writerow([
                    d,
                    tx.customer_email or tx.customer_name or "Stripe Customer",
                    "Sales",
                    tx.gross_amount,
                    tx.description[:100] if tx.description else "",
                    f"Stripe charge: {tx.stripe_id or ''}",
                ])
                w.writerow([
                    d,
                    tx.customer_email or tx.customer_name or "Stripe Customer",
                    "Stripe Fee",
                    tx.fee,
                    "Payment processing fee",
                    f"Stripe fee: {tx.stripe_id or ''}",
                ])
        return out.getvalue()

    def to_journal_entries(self) -> str:
        """Output journal entries for importing to QBO"""
        out = StringIO()
        w = csv.writer(out)
        w.writerow(["Date", "Account", "Debit", "Credit", "Memo", "Name"])
        for tx in self.transactions:
            d = self._fmt_date(tx.date)
            if tx.tx_type == StripeTxType.CHARGE:
                w.writerow([d, "Stripe Clearing", tx.gross_amount, "0", tx.description[:100], tx.customer_email or ""])
                w.writerow([d, "Sales Income", "0", tx.gross_amount, tx.description[:100], tx.customer_email or ""])
                if tx.fee > 0:
                    w.writerow([d, "Stripe Fee Expense", tx.fee, "0", "Payment processing fee", tx.customer_email or ""])
                    w.writerow([d, "Stripe Clearing", "0", tx.fee, "Payment processing fee", tx.customer_email or ""])
            elif tx.tx_type == StripeTxType.REFUND:
                w.writerow([d, "Sales Income", abs(tx.gross_amount), "0", f"Refund: {tx.description[:80]}", tx.customer_email or ""])
                w.writerow([d, "Stripe Clearing", "0", abs(tx.gross_amount), f"Refund: {tx.description[:80]}", tx.customer_email or ""])
        return out.getvalue()

    def to_combined(self) -> str:
        """Bank + fee entries in one sheet"""
        out = StringIO()
        w = csv.writer(out)
        w.writerow(["Date", "Description", "Amount", "Memo", "Type"])
        for tx in self._iter_bank_entries():
            w.writerow([tx["Date"], tx["Description"], tx["Amount"], tx["Memo"], "Bank"])
        for fee_tx in self._iter_fee_entries():
            w.writerow([fee_tx["Date"], fee_tx["Description"], fee_tx["Amount"], fee_tx["Memo"], "Fee"])
        return out.getvalue()

    def _iter_bank_entries(self):
        for tx in self.transactions:
            d = self._fmt_date(tx.date)
            if tx.tx_type == StripeTxType.CHARGE:
                yield {
                    "Date": d,
                    "Description": f"Stripe: {tx.description[:80]}" if tx.description else "Stripe payment",
                    "Amount": tx.net_amount,
                    "Memo": f"Charge {tx.stripe_id or ''} | {tx.customer_email or ''}",
                }
            elif tx.tx_type == StripeTxType.PAYOUT:
                yield {
                    "Date": d,
                    "Description": f"Stripe payout: {tx.description[:80]}" if tx.description else "Stripe payout to bank",
                    "Amount": tx.net_amount,
                    "Memo": f"Payout {tx.stripe_id or ''}",
                }
            elif tx.tx_type == StripeTxType.REFUND:
                yield {
                    "Date": d,
                    "Description": f"Refund: {tx.description[:80]}" if tx.description else "Stripe refund",
                    "Amount": tx.net_amount,
                    "Memo": f"Refund {tx.stripe_id or ''}",
                }
            elif tx.tx_type == StripeTxType.ADJUSTMENT:
                yield {
                    "Date": d,
                    "Description": f"Adjustment: {tx.description[:80]}" if tx.description else "Stripe adjustment",
                    "Amount": tx.gross_amount,
                    "Memo": f"Adj {tx.stripe_id or ''}",
                }

    def _iter_fee_entries(self):
        for tx in self.transactions:
            if tx.fee > 0 and tx.tx_type in (StripeTxType.CHARGE, StripeTxType.REFUND):
                d = self._fmt_date(tx.date)
                fee_sign = -1 if tx.tx_type == StripeTxType.REFUND else 1
                yield {
                    "Date": d,
                    "Description": "Stripe processing fee",
                    "Amount": fee_sign * tx.fee,
                    "Memo": f"Fee for {tx.stripe_id or ''}",
                }

    def summary(self) -> dict:
        total_charges = sum(
            t.gross_amount for t in self.transactions if t.tx_type == StripeTxType.CHARGE
        )
        total_fees = sum(t.fee for t in self.transactions)
        total_refunds = abs(
            sum(
                t.gross_amount
                for t in self.transactions
                if t.tx_type == StripeTxType.REFUND
            )
        )
        total_payouts = abs(
            sum(
                t.gross_amount
                for t in self.transactions
                if t.tx_type == StripeTxType.PAYOUT
            )
        )
        tx_count = len(self.transactions)
        return {
            "transactions": tx_count,
            "charges": float(total_charges),
            "fees": float(total_fees),
            "refunds": float(total_refunds),
            "payouts": float(total_payouts),
            "net_revenue": float(total_charges - total_refunds - total_fees),
        }
