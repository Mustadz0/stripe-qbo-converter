import csv
from decimal import Decimal
from io import StringIO
from pathlib import Path
from typing import List, Union

from .models import StripeTransaction, StripeTxType


COLUMNS_BALANCE = {
    "date": ["date", "created", "created_utc"],
    "type": ["type", "transaction_type", "report_category"],
    "gross": ["gross", "amount", "gross_amount"],
    "fee": ["fee", "stripe_fee", "processing_fee", "fees"],
    "net": ["net", "net_amount"],
    "currency": ["currency"],
    "description": ["description", "statement_descriptor", "memo"],
    "customer_email": ["customer_email", "email", "recipient"],
    "status": ["status", "state"],
    "id": ["id", "transaction_id", "stripe_id"],
}

COLUMNS_PAYOUTS = {
    "date": ["date", "arrival_date", "created"],
    "type": ["type"],
    "gross": ["amount", "gross_amount", "total"],
    "fee": ["fee", "stripe_fee"],
    "net": ["net", "net_amount"],
    "currency": ["currency"],
    "description": ["description", "statement_descriptor"],
    "status": ["status"],
    "id": ["id", "payout_id"],
}


class StripeCSVParser:
    def __init__(self, csv_content: Union[str, Path]):
        self.csv_content = csv_content
        self.rows: List[StripeTransaction] = []

    def _find_column(self, headers: List[str], candidates: List[str]) -> int:
        for i, h in enumerate(headers):
            hl = h.strip().lower()
            for c in candidates:
                if c in hl:
                    return i
        return -1

    def _normalize_type(self, raw_type: str) -> StripeTxType:
        t = raw_type.strip().lower()
        if "charge" in t:
            return StripeTxType.CHARGE
        if "refund" in t:
            return StripeTxType.REFUND
        if "payout" in t or "transfer" in t:
            return StripeTxType.PAYOUT
        if "fee" in t or "adjustment" in t:
            return StripeTxType.ADJUSTMENT
        return StripeTxType.OTHER

    def _parse_decimal(self, val: str) -> Decimal:
        if not val or val.strip() == "":
            return Decimal("0")
        cleaned = val.strip().replace(",", "")
        if cleaned.startswith("$"):
            cleaned = cleaned[1:]
        return Decimal(cleaned)

    def parse(self, fmt: str = "auto") -> List[StripeTransaction]:
        content = self.csv_content
        if isinstance(content, Path):
            text = content.read_text(encoding="utf-8-sig")
        else:
            text = content

        reader = csv.DictReader(StringIO(text))
        headers = reader.fieldnames or []
        rows = list(reader)

        col_map = self._detect_format(headers) if fmt == "auto" else COLUMNS_BALANCE

        for row in rows:
            tx = self._row_to_tx(row, col_map)
            if tx:
                self.rows.append(tx)
        return self.rows

    def _detect_format(self, headers: List[str]) -> dict:
        hl = [h.lower() for h in headers]
        score_balance = sum(
            1 for cands in COLUMNS_BALANCE.values() if any(c in h for h in hl for c in cands if c in h)
        )
        score_payouts = sum(
            1 for cands in COLUMNS_PAYOUTS.values() if any(c in h for h in hl for c in cands if c in h)
        )
        return COLUMNS_BALANCE if score_balance >= score_payouts else COLUMNS_PAYOUTS

    def _row_to_tx(self, row: dict, col_map: dict) -> Optional[StripeTransaction]:
        row_lower = {k.lower(): v for k, v in row.items()}

        def g(key):
            candidates = col_map.get(key, [])
            for c in candidates:
                for rk, rv in row_lower.items():
                    if c in rk:
                        return rv
            return ""

        raw_type = g("type") or "other"
        gross_str = g("gross") or "0"
        fee_str = g("fee") or "0"
        net_str = g("net") or "0"

        gross = abs(self._parse_decimal(gross_str))
        fee = abs(self._parse_decimal(fee_str))
        net_raw = self._parse_decimal(net_str)

        raw_type_lower = raw_type.strip().lower()
        is_refund = "refund" in raw_type_lower
        is_payout = "payout" in raw_type_lower or "transfer" in raw_type_lower

        if is_refund:
            gross = -abs(net_raw) if net_raw else gross
            fee = Decimal("0")
            net = gross
        elif is_payout:
            gross = -abs(net_raw) if net_raw else -gross
            net = gross
            fee = Decimal("0")
        else:
            net = net_raw if net_raw else gross - fee

        return StripeTransaction(
            date=g("date"),
            tx_type=self._normalize_type(raw_type),
            gross_amount=gross,
            fee=fee,
            net_amount=net,
            currency=g("currency") or "usd",
            description=g("description"),
            customer_email=g("customer_email"),
            status=g("status") or "completed",
            stripe_id=g("id"),
            raw=row,
        )
