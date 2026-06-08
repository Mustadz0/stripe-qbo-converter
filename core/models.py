from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional


class StripeTxType(Enum):
    CHARGE = "charge"
    REFUND = "refund"
    PAYOUT = "payout"
    ADJUSTMENT = "adjustment"
    FEE = "fee"
    TRANSFER = "transfer"
    OTHER = "other"


@dataclass
class StripeTransaction:
    date: str
    tx_type: StripeTxType
    gross_amount: Decimal
    fee: Decimal
    net_amount: Decimal
    currency: str
    description: str
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    stripe_id: Optional[str] = None
    status: str = "completed"
    raw: dict = field(default_factory=dict)


@dataclass
class QBOEntry:
    date: str
    description: str
    amount: Decimal
    memo: str = ""
    tx_type: str = "Expense"
    account: str = "Stripe Clearing"
    customer: str = ""
    class_name: str = ""
    doc_number: str = ""
