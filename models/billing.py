from pydantic import BaseModel


class Bill(BaseModel):
    bill_id: str
    account_number: str
    bill_date: str
    due_date: str
    amount_due: float
    amount_paid: float
    status: str  # Unpaid, Paid, Overdue, Partial


class Payment(BaseModel):
    payment_id: str
    account_number: str
    payment_date: str
    amount: float
    method: str  # Credit Card, ACH, Check


class PaymentRequest(BaseModel):
    amount: float
    method: str
