from fastapi import APIRouter, Query
from models.customer import Customer, Meter, UsageRecord
import services.customer_service as svc

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=list[Customer])
async def list_customers(
    name: str | None = None,
    status: str | None = None,
    limit: int = Query(default=20, le=100),
):
    """List customers with optional name/status filters."""
    return await svc.list_customers(name, status, limit)


@router.get("/{account_number}", response_model=Customer)
async def get_customer(account_number: str):
    """Look up a customer by account number."""
    return await svc.get_customer(account_number)


@router.get("/{account_number}/meter", response_model=Meter)
async def get_meter(account_number: str):
    """Get meter details for a customer."""
    return await svc.get_meter(account_number)


@router.get("/{account_number}/usage", response_model=list[UsageRecord])
async def get_usage(
    account_number: str,
    months: int = Query(default=12, le=60, description="Months of history to return"),
):
    """Get monthly usage history for a customer."""
    return await svc.get_usage(account_number, months)
