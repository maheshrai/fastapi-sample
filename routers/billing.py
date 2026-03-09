from fastapi import APIRouter, Query
from models.billing import Bill, Payment, PaymentRequest
import services.billing_service as svc

router = APIRouter(prefix="/customers", tags=["Billing"])


@router.get("/{account_number}/bills", response_model=list[Bill])
async def get_bills(
    account_number: str,
    limit: int = Query(default=12, le=60, description="Number of bills to return"),
):
    """Get billing history for a customer."""
    return await svc.get_bills(account_number, limit)


@router.get("/{account_number}/bills/{bill_id}", response_model=Bill)
async def get_bill(account_number: str, bill_id: str):
    """Get a specific bill."""
    return await svc.get_bill(account_number, bill_id)


@router.post("/{account_number}/payments", response_model=Payment, status_code=201)
async def create_payment(account_number: str, payment: PaymentRequest):
    """Submit a payment for a customer account."""
    return await svc.create_payment(account_number, payment)
