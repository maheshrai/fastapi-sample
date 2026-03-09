from pydantic import BaseModel


class Outage(BaseModel):
    outage_id: str
    status: str          # Active, Resolved, Scheduled
    cause: str | None
    affected_customers: int
    started_at: str
    estimated_restore: str | None
    resolved_at: str | None
    zip_codes: list[str]


class OutageReport(BaseModel):
    account_number: str
    description: str | None = None
