from fastapi import APIRouter
from models.outage import Outage, OutageReport
import services.outage_service as svc

router = APIRouter(prefix="/outages", tags=["Outages"])


@router.get("", response_model=list[Outage])
async def list_outages(status: str | None = None, zip_code: str | None = None):
    """List outages, optionally filtered by status or zip code."""
    return await svc.list_outages(status, zip_code)


@router.get("/{outage_id}", response_model=Outage)
async def get_outage(outage_id: str):
    """Get details for a specific outage."""
    return await svc.get_outage(outage_id)


@router.post("", status_code=202)
async def report_outage(report: OutageReport):
    """Report a new outage for a customer's service address."""
    return await svc.report_outage(report)
