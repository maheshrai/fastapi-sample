from pydantic import BaseModel


class Customer(BaseModel):
    account_number: str
    name: str
    email: str | None
    phone: str | None
    service_status: str
    rate_plan: str
    account_since: str
    balance_due: float


class Meter(BaseModel):
    meter_id: str
    account_number: str
    meter_type: str
    last_read_kwh: float
    last_read_date: str


class UsageRecord(BaseModel):
    read_date: str
    kwh_used: float
    cost: float
