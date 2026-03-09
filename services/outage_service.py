from fastapi import HTTPException
from faker import Faker
import random
from datetime import datetime, timedelta
from models.outage import Outage, OutageReport

fake = Faker()

STATUSES = ["Active", "Active", "Resolved", "Scheduled"]
CAUSES = ["Equipment Failure", "Severe Weather", "Planned Maintenance", "Vehicle Accident", "Animal Contact", "Unknown"]

# In-memory store
_OUTAGES: dict[str, Outage] = {}
_REPORTS: list[dict] = []


def _generate_outage(outage_id: str) -> Outage:
    f = Faker()
    f.seed_instance(outage_id)
    rng = random.Random(outage_id)

    status = rng.choice(STATUSES)
    started_at = datetime.now() - timedelta(hours=rng.randint(1, 72))
    estimated_restore = started_at + timedelta(hours=rng.randint(1, 8))
    resolved_at = estimated_restore if status == "Resolved" else None

    return Outage(
        outage_id=outage_id,
        status=status,
        cause=rng.choice(CAUSES),
        affected_customers=rng.randint(10, 5000),
        started_at=started_at.strftime("%Y-%m-%dT%H:%M:%S"),
        estimated_restore=estimated_restore.strftime("%Y-%m-%dT%H:%M:%S"),
        resolved_at=resolved_at.strftime("%Y-%m-%dT%H:%M:%S") if resolved_at else None,
        zip_codes=[f.zipcode() for _ in range(rng.randint(1, 4))],
    )


# Pre-seed 10 outages
for i in range(1, 11):
    oid = f"OUT-{i:05d}"
    _OUTAGES[oid] = _generate_outage(oid)


async def list_outages(status: str | None, zip_code: str | None) -> list[Outage]:
    results = list(_OUTAGES.values())
    if status:
        results = [o for o in results if o.status.lower() == status.lower()]
    if zip_code:
        results = [o for o in results if zip_code in o.zip_codes]
    return results


async def get_outage(outage_id: str) -> Outage:
    outage = _OUTAGES.get(outage_id.upper())
    if not outage:
        raise HTTPException(status_code=404, detail=f"Outage {outage_id} not found")
    return outage


async def report_outage(report: OutageReport) -> dict:
    report_id = fake.bothify(text="RPT-########")
    _REPORTS.append({
        "report_id": report_id,
        "account_number": report.account_number.upper(),
        "description": report.description,
        "reported_at": datetime.now().isoformat(),
    })
    return {"report_id": report_id, "message": "Outage reported. A crew will be dispatched shortly."}
