from fastapi import HTTPException
from faker import Faker
import random
from datetime import date, timedelta
from models.billing import Bill, Payment, PaymentRequest

fake = Faker()

BILL_STATUSES = ["Paid", "Unpaid", "Overdue", "Partial"]
PAYMENT_METHODS = ["Credit Card", "ACH", "Check"]

# In-memory store
_BILLS: dict[str, list[Bill]] = {}
_PAYMENTS: list[Payment] = []


def _seed_bills(account_number: str, count: int = 12) -> list[Bill]:
    rng = random.Random(account_number)
    bills = []
    for i in range(count):
        bill_date = (date.today().replace(day=1) - timedelta(days=i * 30))
        due_date = bill_date + timedelta(days=21)
        amount_due = round(rng.uniform(80, 400), 2)
        status = rng.choice(BILL_STATUSES)
        amount_paid = amount_due if status == "Paid" else (round(rng.uniform(0, amount_due), 2) if status == "Partial" else 0.0)
        bills.append(Bill(
            bill_id=f"BILL-{account_number}-{i+1:03d}",
            account_number=account_number,
            bill_date=bill_date.isoformat(),
            due_date=due_date.isoformat(),
            amount_due=amount_due,
            amount_paid=amount_paid,
            status=status,
        ))
    return bills


def _get_or_create_bills(account_number: str) -> list[Bill]:
    if account_number not in _BILLS:
        _BILLS[account_number] = _seed_bills(account_number)
    return _BILLS[account_number]


async def get_bills(account_number: str, limit: int) -> list[Bill]:
    return _get_or_create_bills(account_number.upper())[:limit]


async def get_bill(account_number: str, bill_id: str) -> Bill:
    bills = _get_or_create_bills(account_number.upper())
    bill = next((b for b in bills if b.bill_id == bill_id), None)
    if not bill:
        raise HTTPException(status_code=404, detail=f"Bill {bill_id} not found")
    return bill


async def create_payment(account_number: str, req: PaymentRequest) -> Payment:
    payment = Payment(
        payment_id=fake.bothify(text="PAY-########"),
        account_number=account_number.upper(),
        payment_date=date.today().isoformat(),
        amount=req.amount,
        method=req.method,
    )
    _PAYMENTS.append(payment)
    return payment
